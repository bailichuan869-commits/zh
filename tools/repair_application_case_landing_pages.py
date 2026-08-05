from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from kb_raw_structure import comparable_text, split_markdown, update_frontmatter


LANDING_RELATIVE = Path("raw/standards/accounting/application-cases-pages")
ATTACHMENT_RELATIVE = Path("raw/standards/accounting/application-case-attachments")
SOURCE_PAGE_RE = re.compile(r"^<!--\s*source-page:\s*\d+\s*-->$")
PREFIX_RE = re.compile(r"^(\d{3})-")


@dataclass(frozen=True)
class RepairTarget:
    landing: Path
    attachment: Path
    landing_metadata: dict[str, Any]
    landing_frontmatter: str
    landing_body: str
    attachment_metadata: dict[str, Any]
    attachment_body: str


class RepairError(RuntimeError):
    pass


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def parse_yaml_mapping(text: str) -> dict[str, Any]:
    data = yaml.safe_load(text) or {}
    return data if isinstance(data, dict) else {}


def three_digit_prefix(path: Path) -> str:
    match = PREFIX_RE.match(path.name)
    if not match:
        raise RepairError(f"{path.name}: filename does not start with a three-digit application case prefix")
    return match.group(1)


def is_attachment_landing(metadata: dict[str, Any]) -> bool:
    return str(metadata.get("source_role") or "").strip() == "attachment-landing"


def active_landing_pages(root: Path) -> list[Path]:
    landing_dir = root / LANDING_RELATIVE
    if not landing_dir.exists():
        raise RepairError(f"landing directory not found: {landing_dir}")
    return sorted(landing_dir.glob("*.html.md"))


def matching_attachment(root: Path, landing: Path) -> Path:
    prefix = three_digit_prefix(landing)
    attachment_dir = root / ATTACHMENT_RELATIVE
    matches = sorted(attachment_dir.glob(f"{prefix}-*.pdf.md"))
    if len(matches) != 1:
        listed = ", ".join(path.name for path in matches) or "<none>"
        raise RepairError(f"{landing.name}: expected exactly one matching attachment for prefix {prefix}, got {len(matches)} ({listed})")
    return matches[0]


def collect_targets(root: Path) -> list[RepairTarget]:
    targets: list[RepairTarget] = []
    problems: list[str] = []
    for landing in active_landing_pages(root):
        landing_metadata, landing_frontmatter, landing_body = split_markdown(landing)
        if not is_attachment_landing(landing_metadata):
            continue
        try:
            attachment = matching_attachment(root, landing)
            attachment_metadata, _, attachment_body = split_markdown(attachment)
            if str(attachment_metadata.get("source_role") or "").strip() != "substantive-attachment":
                raise RepairError(f"{landing.name}: matching attachment is not source_role=substantive-attachment")
            if str(attachment_metadata.get("extraction_status") or "").strip() != "ok":
                raise RepairError(f"{landing.name}: matching attachment extraction_status is not ok")
            if not comparable_text(attachment_body):
                raise RepairError(f"{landing.name}: matching attachment body is empty")
            already_repaired = str(landing_metadata.get("content_source_role") or "").strip() == "substantive-attachment"
            if not already_repaired and len(comparable_text(attachment_body)) <= max(200, len(comparable_text(landing_body)) * 3):
                raise RepairError(f"{landing.name}: matching attachment body is not meaningfully longer than landing body")
            targets.append(
                RepairTarget(
                    landing=landing,
                    attachment=attachment,
                    landing_metadata=landing_metadata,
                    landing_frontmatter=landing_frontmatter,
                    landing_body=landing_body,
                    attachment_metadata=attachment_metadata,
                    attachment_body=attachment_body,
                )
            )
        except RepairError as exc:
            problems.append(str(exc))
    if problems:
        raise RepairError("\n".join(problems))
    return targets


def clean_line(line: str) -> str:
    line = line.replace("\u00a0", " ").replace("\u3000", " ").replace("\ufeff", "")
    return re.sub(r"[ \t]+", " ", line).strip()


def is_heading(line: str) -> bool:
    return bool(re.match(r"^#{1,6}\s+\S", line))


def is_source_page_marker(line: str) -> bool:
    return bool(SOURCE_PAGE_RE.match(line))


def is_table_line(line: str) -> bool:
    return line.startswith("|") and line.endswith("|")


def is_compact_table_row(line: str) -> bool:
    if is_accounting_entry(line) or sentence_ended(line):
        return False
    if any(mark in line for mark in ("，", ",", "。", "；", ";", "：", ":")):
        return False
    if line.startswith("项目") and any(label in line for label in ("年份", "成本", "收入", "金额", "信用损失")):
        return True
    if re.match(r"^\d[×xX]\d{2}\s*年", line) and ("-" in line or "（=" in line):
        return True
    if re.match(r"^\d{4}\s*年", line) and len(re.findall(r"\d", line)) >= 6:
        return True
    return False


def is_list_line(line: str) -> bool:
    return bool(
        re.match(
            r"^(?:[-*+]\s+|\d+[.)、]\s+|[（(]?\d+[）)]\s*|[一二三四五六七八九十]+[、.]\s+)",
            line,
        )
    )


def is_accounting_entry(line: str) -> bool:
    return bool(re.search(r"(?:^|[0-9 　,，.．]+)(借|贷)[:：]", line))


def is_unit_line(line: str) -> bool:
    return bool(re.match(r"^单位[:：]", line))


def is_structural_line(line: str) -> bool:
    return (
        is_heading(line)
        or is_source_page_marker(line)
        or is_table_line(line)
        or is_compact_table_row(line)
        or is_list_line(line)
        or is_accounting_entry(line)
        or is_unit_line(line)
    )


def sentence_ended(line: str) -> bool:
    return bool(re.search(r"[。！？；!?;]$|[.][”’）)]?$", line))


def should_join(previous: str, current: str) -> bool:
    if is_structural_line(previous) or is_structural_line(current):
        return False
    if previous.endswith(("：", ":")):
        return False
    if current.startswith(("【例】", "分析：", "分析依据：", "结论：", "会计处理：")):
        return False
    if sentence_ended(previous):
        return False
    return True


def join_text(previous: str, current: str) -> str:
    if previous.endswith("-") and re.search(r"[A-Za-z]-$", previous) and re.match(r"^[A-Za-z]", current):
        return previous[:-1] + current
    if re.search(r"[A-Za-z0-9]$", previous) and re.match(r"^[A-Za-z0-9]", current):
        return previous + " " + current
    return previous + current


def next_nonblank(lines: list[str], index: int) -> str:
    for later in lines[index + 1 :]:
        cleaned = clean_line(later)
        if cleaned:
            return cleaned
    return ""


def previous_nonblank(lines: list[str], index: int) -> str:
    for earlier in reversed(lines[:index]):
        cleaned = clean_line(earlier)
        if cleaned:
            return cleaned
    return ""


def is_page_footer_number(lines: list[str], index: int) -> bool:
    line = clean_line(lines[index])
    if not re.match(r"^\d{1,3}$", line):
        return False
    return (
        not next_nonblank(lines, index)
        or is_source_page_marker(next_nonblank(lines, index))
        or is_source_page_marker(previous_nonblank(lines, index))
    )


def reflow_body(body: str, title: str) -> str:
    lines = body.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks: list[str] = []
    paragraph = ""

    def flush() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(paragraph)
            paragraph = ""

    for index, raw_line in enumerate(lines):
        line = clean_line(raw_line)
        if not line or is_page_footer_number(lines, index):
            continue
        if is_structural_line(line):
            flush()
            blocks.append(line)
            continue
        if paragraph and should_join(paragraph, line):
            paragraph = join_text(paragraph, line)
        else:
            flush()
            paragraph = line
    flush()
    blocks = remove_leading_duplicate_titles(blocks, title)
    return "\n\n".join(blocks).strip() + "\n"


def block_title_text(block: str) -> str:
    return re.sub(r"^#{1,6}\s+", "", block).strip()


def remove_leading_duplicate_titles(blocks: list[str], title: str) -> list[str]:
    if not blocks:
        return blocks
    title_key = comparable_text(title)
    if not title_key:
        return blocks

    output = list(blocks)
    start = 1 if is_heading(output[0]) else 0
    while start < len(output) and is_source_page_marker(output[start]):
        start += 1
    if start >= len(output):
        return output

    for end in range(start, min(len(output), start + 3)):
        candidates = output[start : end + 1]
        if any(is_source_page_marker(block) or is_table_line(block) or is_list_line(block) or is_accounting_entry(block) for block in candidates):
            break
        combined = "".join(block_title_text(block) for block in candidates)
        combined_key = comparable_text(combined)
        if combined_key and combined_key == title_key:
            del output[start : end + 1]
            break
    return output


def repaired_document(root: Path, target: RepairTarget) -> str:
    title = str(target.landing_metadata.get("title") or target.attachment_metadata.get("title") or target.landing.stem)
    body = reflow_body(target.attachment_body, title)
    updates = {
        "attachment_markdown_path": rel(root, target.attachment),
        "attachment_url": target.attachment_metadata.get("attachment_url", ""),
        "content_source_role": "substantive-attachment",
        "content_source_sha256": target.attachment_metadata.get("sha256", ""),
    }
    return update_frontmatter(target.landing_frontmatter, updates) + body


def summarize(root: Path, targets: list[RepairTarget], apply: bool, changed: list[str]) -> dict[str, Any]:
    return {
        "ok": True,
        "operation": "repair_application_case_landing_pages",
        "mode": "apply" if apply else "dry-run",
        "target_count": len(targets),
        "changed_count": len(changed),
        "targets": [
            {
                "landing": rel(root, target.landing),
                "attachment": rel(root, target.attachment),
                "old_chars": len(comparable_text(target.landing_body)),
                "new_chars": len(comparable_text(reflow_body(target.attachment_body, str(target.landing_metadata.get("title") or "")))),
            }
            for target in targets
        ],
        "changed": changed,
    }


def repair(root: Path, apply: bool) -> dict[str, Any]:
    root = root.resolve()
    targets = collect_targets(root)
    changed: list[str] = []
    for target in targets:
        document = repaired_document(root, target)
        old = target.landing.read_text(encoding="utf-8")
        if document != old:
            changed.append(rel(root, target.landing))
            if apply:
                target.landing.write_text(document, encoding="utf-8", newline="\n")
    return summarize(root, targets, apply, changed)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        description="Repair CPA-ZH accounting application-case attachment landing Markdown pages."
    )
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
                    "operation": "repair_application_case_landing_pages",
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
