from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse


ATTACHMENT_SUFFIXES = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".rar", ".7z"}
TEXT_NATIVE_SUFFIXES = {".md", ".txt", ".csv", ".json", ".html", ".htm", ".xml"}
SKIP_RAW_DIRS = {"_archive"}
SKIP_RAW_NAMES = {"metadata.json", "manifest.json", "source-url.txt"}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key.lower() in {"href", "src"} and value:
                self.links.append(value.strip())


@dataclass
class AuditResult:
    manifest_items: int
    attachment_candidates: list[tuple[str, str, str, str]]
    active_non_md_files: list[str]
    missing_markdown: list[str]
    low_markdown: list[tuple[str, int]]
    manifest_missing_derived: list[tuple[str, str, str]]


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def active_raw_file(raw_root: Path, path: Path) -> bool:
    try:
        parts = path.relative_to(raw_root).parts
    except ValueError:
        return False
    return not any(part in SKIP_RAW_DIRS for part in parts)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_manifest(path: Path) -> list[dict]:
    data = load_json(path)
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return [item for item in data["items"] if isinstance(item, dict)]
    return []


def normalize_kb_rel(value: str) -> str:
    value = (value or "").replace("\\", "/").strip()
    prefix = "knowledge-base/CPA-ZH/"
    if value.startswith(prefix):
        return value[len(prefix) :]
    return value


def item_metadata(manifest_path: Path, item: dict) -> dict:
    slug = str(item.get("slug") or "").strip()
    if not slug:
        return {}
    metadata_path = manifest_path.parent / slug / "metadata.json"
    data = load_json(metadata_path)
    return data if isinstance(data, dict) else {}


def first_value(*values: object) -> str:
    for value in values:
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def source_url_for_page(page: Path) -> str:
    source_url = page.parent / "source-url.txt"
    if source_url.exists():
        return source_url.read_text(encoding="utf-8", errors="ignore").strip()
    if page.suffix.lower() == ".md":
        text = page.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r'^source_url:\s*["\']?([^"\'\n]+)', text, re.M)
        if match:
            return match.group(1).strip()
    return ""


def source_role_for_page(page: Path) -> str:
    if page.suffix.lower() != ".md":
        return ""
    text = page.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r'^source_role:\s*["\']?([^"\'\n]+)', text, re.M)
    return match.group(1).strip() if match else ""


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))
    except Exception:
        return []


def attachment_registry(raw_root: Path) -> dict[str, str]:
    registry_path = raw_root / "_archive" / "indexes" / "attachment-registry.csv"
    statuses: dict[str, str] = {}
    for row in read_csv_rows(registry_path):
        url = str(row.get("attachment_url") or "").strip()
        if url:
            statuses[url] = str(row.get("classification") or "archived")
    return statuses


def normalized_archive_relative(raw_root: Path, path: Path) -> str:
    try:
        relative = path.resolve().relative_to(raw_root.resolve())
    except ValueError:
        return ""
    parts = list(relative.parts)
    while parts and parts[0] == "_archive":
        parts.pop(0)
    return Path(*parts).as_posix() if parts else ""


def csv_source_maps(raw_root: Path) -> tuple[dict[str, str], set[str]]:
    page_urls: dict[str, str] = {}
    registered_attachments: set[str] = set()
    for csv_path in (raw_root / "_archive").rglob("*.csv"):
        for row in read_csv_rows(csv_path):
            url = str(row.get("Url") or row.get("url") or "").strip()
            local = str(row.get("LocalFile") or row.get("local_file") or "").strip()
            attachment = str(row.get("attachment_url") or "").strip()
            if attachment:
                registered_attachments.add(attachment)
            if Path(urlparse(url).path).suffix.lower() in ATTACHMENT_SUFFIXES:
                registered_attachments.add(url)
            if not url or not local:
                continue
            path = Path(local)
            if path.is_absolute():
                relative = normalized_archive_relative(raw_root, path)
                if relative:
                    page_urls[relative] = url
    return page_urls, registered_attachments


def markdown_source_maps(raw_root: Path) -> tuple[dict[str, str], dict[str, str]]:
    page_urls: dict[str, str] = {}
    page_roles: dict[str, str] = {}
    for markdown in raw_root.rglob("*.md"):
        if not active_raw_file(raw_root, markdown):
            continue
        text = markdown.read_text(encoding="utf-8", errors="ignore")
        original_match = re.search(r'^original_file:\s*["\']?([^"\'\n]+)', text, re.M)
        url_match = re.search(r'^source_url:\s*["\']?([^"\'\n]+)', text, re.M)
        role_match = re.search(r'^source_role:\s*["\']?([^"\'\n]+)', text, re.M)
        if not original_match:
            continue
        original = normalize_kb_rel(original_match.group(1).strip())
        parts = list(Path(original).parts)
        while parts and parts[0] in {"raw", "_archive"}:
            parts.pop(0)
        if not parts:
            continue
        key = Path(*parts).as_posix()
        if url_match:
            page_urls[key] = url_match.group(1).strip()
        if role_match:
            page_roles[key] = role_match.group(1).strip()
    return page_urls, page_roles


def archive_source_page(raw_root: Path, path: Path) -> bool:
    try:
        parts = path.relative_to(raw_root / "_archive").parts
    except ValueError:
        return False
    return bool(parts) and not parts[0].startswith("_")


def collect_html_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    links: list[str] = []
    if path.suffix.lower() in {".html", ".htm"}:
        parser = LinkParser()
        parser.feed(text)
        links.extend(parser.links)
    links.extend(re.findall(r"https?://[^\s\)\]\"']+", text))
    links.extend(re.findall(r"(?i)(?:href|src)=[\"']([^\"']+)[\"']", text))
    return sorted(set(link.strip().strip("\"'<>") for link in links if link.strip()))


def body_length(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="ignore")
    body = re.sub(r"^---\n.*?\n---\n?", "", text, flags=re.S)
    return len(re.sub(r"\s+", "", body))


def audit(root: Path) -> AuditResult:
    raw_root = root / "raw"
    manifest_local: set[str] = set()
    archived_names: set[str] = set()
    manifest_derived: set[str] = set()
    manifest_urls: set[str] = set()
    manifest_attachment_urls: set[str] = set()
    manifest_items = 0
    manifest_missing_derived: list[tuple[str, str, str]] = []
    registered_status = attachment_registry(raw_root)
    csv_page_urls, csv_attachment_urls = csv_source_maps(raw_root)
    markdown_page_urls, markdown_page_roles = markdown_source_maps(raw_root)

    for manifest_path in sorted(raw_root.rglob("manifest.json")):
        if not active_raw_file(raw_root, manifest_path):
            continue
        for item in load_manifest(manifest_path):
            manifest_items += 1
            metadata = item_metadata(manifest_path, item)
            item_id = first_value(item.get("slug"), item.get("filename"), "<unknown>")
            local_file = normalize_kb_rel(first_value(item.get("local_file"), metadata.get("local_file")))
            derived = normalize_kb_rel(first_value(item.get("derived_markdown"), metadata.get("derived_markdown")))
            url = first_value(item.get("url"), item.get("source_url"), metadata.get("official_url"), metadata.get("url"))
            attachment_url = first_value(item.get("attachment_url"), metadata.get("attachment_url"))
            source_type = first_value(item.get("source_type"), metadata.get("source_type"))

            if local_file:
                manifest_local.add(local_file)
                archived_names.add(Path(local_file).name)
            if derived:
                manifest_derived.add(derived)
            if url:
                manifest_urls.add(url)
            if attachment_url:
                manifest_attachment_urls.add(attachment_url)

            suffix = Path(local_file).suffix.lower()
            if (
                local_file
                and not derived
                and suffix not in TEXT_NATIVE_SUFFIXES
                and source_type not in {"local-lecture", "local-case", "local-note", "local-source"}
            ):
                manifest_missing_derived.append((rel(root, manifest_path), item_id, local_file))

    for path in sorted(raw_root.rglob("*")):
        if not path.is_file() or not active_raw_file(raw_root, path):
            continue
        archived_names.add(path.name)
        if path.suffix.lower() == ".zip":
            try:
                with zipfile.ZipFile(path) as archive:
                    for info in archive.infolist():
                        if not info.is_dir():
                            archived_names.add(Path(info.filename).name)
            except zipfile.BadZipFile:
                pass

    attachment_candidates: list[tuple[str, str, str, str]] = []
    seen_attachment_candidates: set[tuple[str, str]] = set()
    page_suffixes = {".html", ".htm", ".md"}
    for page in sorted(raw_root.rglob("*")):
        if not page.is_file() or not (active_raw_file(raw_root, page) or archive_source_page(raw_root, page)):
            continue
        if page.name in SKIP_RAW_NAMES or page.suffix.lower() not in page_suffixes:
            continue
        if source_role_for_page(page) in {"source-registry", "index-page", "reference-page"}:
            continue
        base_url = source_url_for_page(page)
        lookup = ""
        if not base_url:
            try:
                if archive_source_page(raw_root, page):
                    lookup = page.relative_to(raw_root / "_archive").as_posix()
                else:
                    lookup = page.relative_to(raw_root).as_posix()
                base_url = markdown_page_urls.get(lookup) or csv_page_urls.get(lookup, "")
            except ValueError:
                pass
        if lookup and markdown_page_roles.get(lookup) in {"source-registry", "index-page", "reference-page"}:
            continue
        for link in collect_html_links(page):
            parsed = urlparse(link)
            suffix = Path(parsed.path).suffix.lower()
            if suffix not in ATTACHMENT_SUFFIXES:
                continue
            full_url = urljoin(base_url, link) if base_url else link
            full_url = full_url.strip()
            full_parsed = urlparse(full_url)
            basename = Path(full_parsed.path).name
            if "sources/challenge-knowledge-source-summary" in page.as_posix():
                status = "reference-link"
            elif full_url in registered_status:
                status = registered_status[full_url]
            elif full_url in manifest_urls or full_url in manifest_attachment_urls or full_url in csv_attachment_urls:
                status = "archived"
            elif basename in archived_names:
                status = "archived-by-name"
            elif not base_url and not parsed.scheme:
                status = "unresolved-relative"
            else:
                status = "missing-substantive"
            page_rel = rel(root, page)
            candidate_key = (page_rel, full_url)
            if candidate_key not in seen_attachment_candidates:
                seen_attachment_candidates.add(candidate_key)
                attachment_candidates.append((page_rel, full_url, suffix, status))

    active_non_md_files: list[str] = []
    missing_markdown: list[str] = []
    for path in sorted(raw_root.rglob("*")):
        if not path.is_file() or not active_raw_file(raw_root, path):
            continue
        raw_rel = rel(root, path)
        if path.name in SKIP_RAW_NAMES or raw_rel.endswith(".md") or path.name.endswith(".structure.json"):
            continue
        active_non_md_files.append(raw_rel)
        derived_rel = raw_rel + ".md"
        sidecar = Path(str(path) + ".md")
        if (
            not sidecar.exists()
            and derived_rel not in manifest_derived
            and path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".zip", ".rar", ".7z"}
        ):
            missing_markdown.append(raw_rel)

    low_markdown: list[tuple[str, int]] = []
    for path in sorted(raw_root.rglob("*.md")):
        if not active_raw_file(raw_root, path) or path.name == "README.md":
            continue
        length = body_length(path)
        if length < 80 and source_role_for_page(path) not in {
            "source-registry", "index-page", "reference-page", "attachment-landing", "auxiliary-attachment"
        }:
            low_markdown.append((rel(root, path), length))

    return AuditResult(
        manifest_items=manifest_items,
        attachment_candidates=attachment_candidates,
        active_non_md_files=active_non_md_files,
        missing_markdown=missing_markdown,
        low_markdown=low_markdown,
        manifest_missing_derived=manifest_missing_derived,
    )


def render_markdown(result: AuditResult) -> str:
    unknown_attachments = [row for row in result.attachment_candidates if row[3] in {"missing-substantive", "unresolved-relative"}]
    lines = [
        "# CPA-ZH 双轨归档审计报告",
        "",
        "## 摘要",
        "",
        f"- manifest 条目：{result.manifest_items}",
        f"- 页面内附件链接候选：{len(result.attachment_candidates)}",
        f"- 未登记/未匹配附件链接候选：{len(unknown_attachments)}",
        f"- active raw 非 Markdown 原件：{len(result.active_non_md_files)}",
        f"- 缺 Markdown sidecar/derived_markdown：{len(result.missing_markdown)}",
        f"- manifest 非文本原件缺 derived_markdown：{len(result.manifest_missing_derived)}",
        f"- 低正文量 Markdown：{len(result.low_markdown)}",
        "",
        "## 可能只下载页面、未下载附件",
        "",
        "| 页面 | 附件链接 | 类型 | 状态 |",
        "|---|---|---|---|",
    ]
    if unknown_attachments:
        for page, url, suffix, status in unknown_attachments:
            lines.append(f"| `{page}` | {url} | `{suffix}` | `{status}` |")
    else:
        lines.append("| 无 |  |  |  |")

    lines.extend(
        [
            "",
            "## 缺 Markdown 派生件的原件",
            "",
            "| 原件 |",
            "|---|",
        ]
    )
    if result.missing_markdown:
        for path in result.missing_markdown:
            lines.append(f"| `{path}` |")
    else:
        lines.append("| 无 |")

    lines.extend(
        [
            "",
            "## manifest 缺 derived_markdown 的非文本原件",
            "",
            "| manifest | 条目 | 原件 |",
            "|---|---|---|",
        ]
    )
    if result.manifest_missing_derived:
        for manifest, item_id, local_file in result.manifest_missing_derived:
            lines.append(f"| `{manifest}` | {item_id} | `{local_file}` |")
    else:
        lines.append("| 无 |  |  |")

    lines.extend(
        [
            "",
            "## 低正文量 Markdown",
            "",
            "| Markdown | 正文字符数 |",
            "|---|---:|",
        ]
    )
    if result.low_markdown:
        for path, length in result.low_markdown:
            lines.append(f"| `{path}` | {length} |")
    else:
        lines.append("| 无 | 0 |")
    return "\n".join(lines) + "\n"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Audit CPA-ZH raw/manifest dual-track archive quality.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--output", default="", help="Optional Markdown report path.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    result = audit(root)
    unknown_attachments = [row for row in result.attachment_candidates if row[3] in {"missing-substantive", "unresolved-relative"}]
    print(f"manifest_items={result.manifest_items}")
    print(f"attachment_candidates={len(result.attachment_candidates)}")
    print(f"attachment_unknown={len(unknown_attachments)}")
    print(f"active_non_md_files={len(result.active_non_md_files)}")
    print(f"missing_markdown={len(result.missing_markdown)}")
    print(f"manifest_missing_derived={len(result.manifest_missing_derived)}")
    print(f"low_markdown={len(result.low_markdown)}")
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_markdown(result), encoding="utf-8", newline="\n")
        print(f"written={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
