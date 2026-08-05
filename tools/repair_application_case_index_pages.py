from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kb_raw_structure import split_markdown, update_frontmatter


INDEX_RELATIVE = Path("raw/standards/accounting/application-cases-indexes")
PAGES_RELATIVE = Path("raw/standards/accounting/application-cases-pages")
ATTACHMENTS_RELATIVE = Path("raw/standards/accounting/application-case-attachments")
MAPPING_RELATIVE = Path("raw/indexes/enterprise-accounting-standards-number-mapping.csv")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PREFIX_RE = re.compile(r"^(\d{3})-")


@dataclass(frozen=True)
class MappingRecord:
    title: str
    local_path: str


@dataclass(frozen=True)
class IndexItem:
    title: str
    published_at: str
    page: Path
    attachment: Path | None


@dataclass(frozen=True)
class RepairTarget:
    index_page: Path
    metadata: dict[str, Any]
    raw_frontmatter: str
    body: str
    section_title: str
    items: tuple[IndexItem, ...]


class RepairError(RuntimeError):
    pass


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def clean_line(line: str) -> str:
    line = line.replace("\u00a0", " ").replace("\u3000", " ").replace("\ufeff", "")
    return re.sub(r"[ \t]+", " ", line).strip()


def normalized_title(title: str) -> str:
    normalized = unicodedata.normalize("NFKC", title)
    return "".join(character.casefold() for character in normalized if character.isalnum())


def is_index_page(metadata: dict[str, Any]) -> bool:
    return str(metadata.get("source_role") or "").strip() == "index-page"


def active_index_pages(root: Path) -> list[Path]:
    index_dir = root / INDEX_RELATIVE
    if not index_dir.exists():
        raise RepairError(f"index directory not found: {index_dir}")
    return sorted(index_dir.glob("*.html.md"))


def section_title(metadata: dict[str, Any], path: Path) -> str:
    title = str(metadata.get("title") or path.name)
    match = re.match(r"^[^-]+-(.+?)-index(?:[_ ]\d+)?$", title, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return re.sub(r"-index(?:[_ ]\d+)?(?:\.html\.md)?$", "", title, flags=re.IGNORECASE).strip()


def parse_index_entries(body: str, path: Path) -> list[tuple[str, str]]:
    lines = [clean_line(line) for line in body.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    entries: list[tuple[str, str]] = []
    for line in lines:
        table_match = re.match(r"^\|\s*(.*?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|", line)
        if table_match:
            entries.append((table_match.group(1).replace("\\|", "|").strip(), table_match.group(2)))
    for index, line in enumerate(lines[:-1]):
        published_at = lines[index + 1]
        if line and DATE_RE.fullmatch(published_at):
            entries.append((line, published_at))
    if not entries:
        raise RepairError(f"{path.name}: no case title/date pairs found")
    normalized = [normalized_title(title) for title, _ in entries]
    duplicates = sorted({title for title in normalized if normalized.count(title) > 1})
    if duplicates:
        raise RepairError(f"{path.name}: duplicate case entries found")
    return entries


def load_mapping(root: Path) -> list[MappingRecord]:
    mapping_path = root / MAPPING_RELATIVE
    if not mapping_path.is_file():
        raise RepairError(f"mapping CSV not found: {mapping_path}")
    with mapping_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        records = [
            MappingRecord(title=(row.get("Title") or "").strip(), local_path=(row.get("LocalPath") or "").strip())
            for row in rows
            if (row.get("SourceType") or "").strip() == "application_case"
        ]
    if not records:
        raise RepairError(f"mapping CSV contains no application_case rows: {mapping_path}")
    return records


def match_mapping(title: str, records: list[MappingRecord], index_page: Path) -> MappingRecord:
    key = normalized_title(title)
    matches = [record for record in records if normalized_title(record.title) == key]
    if not matches and title.rstrip().endswith(("...", "…")):
        prefix = normalized_title(re.sub(r"(?:\.\.\.|…)$", "", title.rstrip()))
        matches = [record for record in records if normalized_title(record.title).startswith(prefix)]
    if len(matches) != 1:
        listed = ", ".join(record.local_path or record.title for record in matches) or "<none>"
        raise RepairError(
            f"{index_page.name}: expected exactly one mapping for case '{title}', got {len(matches)} ({listed})"
        )
    return matches[0]


def resolve_page(root: Path, record: MappingRecord, index_page: Path) -> Path:
    page = root / Path(record.local_path)
    expected_dir = (root / PAGES_RELATIVE).resolve()
    try:
        page.resolve().relative_to(expected_dir)
    except ValueError as exc:
        raise RepairError(f"{index_page.name}: mapped page is outside application-cases-pages: {record.local_path}") from exc
    if not page.is_file():
        raise RepairError(f"{index_page.name}: mapped local page does not exist: {record.local_path}")
    return page


def match_attachment(root: Path, page: Path, index_page: Path) -> tuple[Path | None, str | None]:
    prefix_match = PREFIX_RE.match(page.name)
    if not prefix_match:
        raise RepairError(f"{index_page.name}: mapped page has no three-digit prefix: {page.name}")
    prefix = prefix_match.group(1)
    matches = sorted((root / ATTACHMENTS_RELATIVE).glob(f"{prefix}-*.pdf.md"))
    if len(matches) > 1:
        listed = ", ".join(path.name for path in matches)
        raise RepairError(f"{index_page.name}: multiple attachments found for prefix {prefix} ({listed})")
    if matches:
        return matches[0], None
    return None, f"{index_page.name}: no attachment Markdown found for {page.name}"


def collect_targets(root: Path) -> tuple[list[RepairTarget], list[str]]:
    records = load_mapping(root)
    targets: list[RepairTarget] = []
    warnings: list[str] = []
    problems: list[str] = []
    for index_page in active_index_pages(root):
        metadata, raw_frontmatter, body = split_markdown(index_page)
        if not is_index_page(metadata):
            continue
        try:
            items: list[IndexItem] = []
            for title, published_at in parse_index_entries(body, index_page):
                record = match_mapping(title, records, index_page)
                page = resolve_page(root, record, index_page)
                attachment, warning = match_attachment(root, page, index_page)
                if warning:
                    warnings.append(warning)
                items.append(IndexItem(title=title, published_at=published_at, page=page, attachment=attachment))
            targets.append(
                RepairTarget(
                    index_page=index_page,
                    metadata=metadata,
                    raw_frontmatter=raw_frontmatter,
                    body=body,
                    section_title=section_title(metadata, index_page),
                    items=tuple(items),
                )
            )
        except RepairError as exc:
            problems.append(str(exc))
    if problems:
        raise RepairError("\n".join(problems))
    return targets, warnings


def escape_table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def render_body(root: Path, target: RepairTarget) -> str:
    lines = [
        f"# {target.section_title}",
        "",
        "本页为财政部企业会计准则应用案例栏目索引页的本地整理版。原始网页快照见右侧文件信息中的“原始文件”。本页用于栏目追溯，不是案例正文；阅读正文请打开下表中的“本地正文页”。",
        "",
        "| 案例 | 发布日期 | 本地正文页 | 附件 Markdown |",
        "|---|---:|---|---|",
    ]
    for item in target.items:
        page_link = f"[{escape_table_cell(item.page.name)}]({rel(root, item.page)})"
        attachment_link = ""
        if item.attachment is not None:
            attachment_link = f"[{escape_table_cell(item.attachment.name)}]({rel(root, item.attachment)})"
        lines.append(
            f"| {escape_table_cell(item.title)} | {item.published_at} | {page_link} | {attachment_link} |"
        )
    return "\n".join(lines).strip() + "\n"


def repaired_document(root: Path, target: RepairTarget) -> str:
    frontmatter = update_frontmatter(
        target.raw_frontmatter,
        {"content_repaired_role": "readable-index", "index_item_count": len(target.items)},
    )
    return frontmatter + render_body(root, target)


def repair(root: Path, apply: bool) -> dict[str, Any]:
    root = root.resolve()
    targets, warnings = collect_targets(root)
    changed: list[str] = []
    for target in targets:
        document = repaired_document(root, target)
        if document != target.index_page.read_text(encoding="utf-8"):
            target_path = rel(root, target.index_page)
            changed.append(target_path)
            if apply:
                target.index_page.write_text(document, encoding="utf-8", newline="\n")
    return {
        "ok": True,
        "operation": "repair_application_case_index_pages",
        "mode": "apply" if apply else "dry-run",
        "target_count": len(targets),
        "changed_count": len(changed),
        "targets": [
            {"index_page": rel(root, target.index_page), "item_count": len(target.items)} for target in targets
        ],
        "changed": changed,
        "warnings": warnings,
    }


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Repair CPA-ZH application-case index Markdown pages.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--apply", action="store_true", help="Write target .html.md files; default is dry-run.")
    args = parser.parse_args()
    try:
        result = repair(Path(args.root), args.apply)
    except RepairError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "operation": "repair_application_case_index_pages",
                    "mode": "apply" if args.apply else "dry-run",
                    "error_code": "validation_failed",
                    "message": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
