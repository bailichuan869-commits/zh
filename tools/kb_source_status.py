from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import kb_manifest_audit


REPORT_PATH = Path("wiki/concepts/source-status-dashboard.md")


@dataclass
class SourceItem:
    manifest_path: str
    item_id: str
    title: str
    document_no: str
    local_file: str
    local_exists: bool
    derived_markdown: str
    derived_exists: bool
    suffix: str
    url: str
    source_type: str
    official_source: str
    official_page_status: str
    text_extraction_status: str
    ocr_status: str
    cache_text_length: int | None
    wiki_page: str
    actions: list[str]


def rel(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def load_manifest(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    return []


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def load_text_cache(root: Path) -> dict[str, dict[str, Any]]:
    manifest = root / "cache" / "text" / "manifest.json"
    if not manifest.exists():
        return {}
    data = load_json(manifest)
    items = data.get("items", [])
    if not isinstance(items, list):
        return {}
    return {str(item.get("raw_path")): item for item in items if item.get("raw_path")}


def metadata_for_item(manifest_path: Path, item: dict[str, Any]) -> dict[str, Any]:
    slug = str(item.get("slug") or "").strip()
    if not slug:
        return {}
    return load_json(manifest_path.parent / slug / "metadata.json")


def first_value(*values: Any) -> str:
    for value in values:
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def cache_text_length(root: Path, local_path: Path, text_cache: dict[str, dict[str, Any]]) -> int | None:
    try:
        raw_path = local_path.relative_to(root).as_posix()
    except ValueError:
        return None
    item = text_cache.get(raw_path)
    if not item:
        return None
    try:
        return int(item.get("text_length") or 0)
    except (TypeError, ValueError):
        return None


def best_cache_text_length(
    root: Path,
    local_path: Path,
    derived_path: Path | None,
    text_cache: dict[str, dict[str, Any]],
) -> int | None:
    if derived_path is not None and derived_path.exists():
        derived_length = cache_text_length(root, derived_path, text_cache)
        if derived_length is not None:
            return derived_length
    return cache_text_length(root, local_path, text_cache) if local_path.exists() else None


def classify_actions(
    *,
    manifest_path: str,
    local_exists: bool,
    derived_exists: bool,
    suffix: str,
    url: str,
    source_type: str,
    official_page_status: str,
    text_extraction_status: str,
    ocr_status: str,
    text_length: int | None,
    official_source: str,
) -> list[str]:
    actions: list[str] = []
    local_source_manifest = manifest_path.startswith("raw/cases/")
    local_source_type = source_type in {"local-lecture", "local-case", "local-note", "local-source"}

    if not local_exists:
        actions.append("missing-local-file")
    text_native_suffixes = {".md", ".txt", ".csv", ".json", ".html", ".htm"}
    if (
        not derived_exists
        and not local_source_type
        and suffix not in text_native_suffixes
        and text_extraction_status not in {"not-required", "raw-only"}
    ):
        actions.append("missing-derived-markdown")
    if not url and not local_source_manifest and not local_source_type:
        actions.append("missing-official-url")
    elif official_page_status not in {"verified", "official", "valid", "local"}:
        if "待复核" in official_source or "待复核" in url or url.rstrip("/") == "https://www.csrc.gov.cn":
            actions.append("verify-official-url")
    if suffix == ".pdf" and (text_length == 0 or text_extraction_status in {"empty", "local_pdf_empty"}):
        actions.append("ocr-pending")
    if ocr_status == "pending" and "ocr-pending" not in actions:
        actions.append("ocr-pending")
    if text_length is None:
        actions.append("not-in-text-cache")
    return actions


def collect_items(root: Path) -> list[SourceItem]:
    text_cache = load_text_cache(root)
    items: list[SourceItem] = []
    for manifest_path in sorted((root / "raw").rglob("manifest.json")):
        for item in load_manifest(manifest_path):
            metadata = metadata_for_item(manifest_path, item)
            local_file = first_value(item.get("local_file"), metadata.get("local_file"))
            local_path = kb_manifest_audit.resolve_local_file(root, local_file) if local_file else manifest_path
            local_exists = bool(local_file and local_path.exists())
            derived_markdown = first_value(item.get("derived_markdown"), metadata.get("derived_markdown"))
            derived_path = kb_manifest_audit.resolve_local_file(root, derived_markdown) if derived_markdown else None
            derived_exists = bool(derived_path and derived_path.exists())
            suffix = local_path.suffix.lower() if local_exists else ""
            url = first_value(item.get("url"), item.get("source_url"), metadata.get("official_url"), metadata.get("url"))
            source_type = first_value(item.get("source_type"), metadata.get("source_type"))
            official_source = first_value(item.get("official_source"), metadata.get("official_source"))
            official_page_status = first_value(item.get("official_page_status"), metadata.get("official_page_status"))
            text_extraction_status = first_value(
                item.get("text_extraction_status"),
                metadata.get("text_extraction_status"),
            )
            ocr_status = first_value(item.get("ocr_status"), metadata.get("ocr_status"))
            text_length = best_cache_text_length(root, local_path, derived_path, text_cache)
            actions = classify_actions(
                manifest_path=rel(root, manifest_path),
                local_exists=local_exists,
                derived_exists=derived_exists,
                suffix=suffix,
                url=url,
                source_type=source_type,
                official_page_status=official_page_status,
                text_extraction_status=text_extraction_status,
                ocr_status=ocr_status,
                text_length=text_length,
                official_source=official_source,
            )
            items.append(
                SourceItem(
                    manifest_path=rel(root, manifest_path),
                    item_id=first_value(item.get("slug"), item.get("filename"), local_path.name),
                    title=first_value(item.get("title"), metadata.get("title"), local_path.stem),
                    document_no=first_value(item.get("document_no"), metadata.get("document_no")),
                    local_file=local_file,
                    local_exists=local_exists,
                    derived_markdown=derived_markdown,
                    derived_exists=derived_exists,
                    suffix=suffix,
                    url=url,
                    source_type=source_type,
                    official_source=official_source,
                    official_page_status=official_page_status or "unknown",
                    text_extraction_status=text_extraction_status or "unknown",
                    ocr_status=ocr_status or "n/a",
                    cache_text_length=text_length,
                    wiki_page=first_value(item.get("wiki_page"), metadata.get("wiki_page")),
                    actions=actions,
                )
            )
    return items


def wiki_link(page: str) -> str:
    if not page:
        return ""
    return f"[[{page}]]"


def render_markdown(root: Path, items: list[SourceItem]) -> str:
    action_counts = Counter(action for item in items for action in item.actions)
    suffix_counts = Counter(item.suffix or "<none>" for item in items)
    verified = sum(1 for item in items if item.official_page_status in {"verified", "official", "valid"})
    with_urls = sum(1 for item in items if item.url)
    with_cache = sum(1 for item in items if item.cache_text_length is not None)
    cached_text = sum(1 for item in items if (item.cache_text_length or 0) > 0)
    with_derived = sum(1 for item in items if item.derived_exists)

    lines = [
        "---",
        "title: 来源状态仪表盘",
        "type: concept",
        "concept_type: maintenance-dashboard",
        f"created: {date.today().isoformat()}",
        f"updated: {date.today().isoformat()}",
        "sources: [kb-source-status]",
        "tags: [maintenance, source-status, archive, ocr, official-link, dual-track]",
        "related: [[concepts/kb-maintenance-workflow]], [[concepts/kb-user-guide]]",
        "domain: sources",
        "topic: dashboards",
        "---",
        "",
        "# 来源状态仪表盘",
        "",
        "本页由 `tools/kb_source_status.py write-report` 生成，用于追踪 raw manifest 来源的官方链接、原件、Markdown 派生件、文本缓存和后续维护动作。",
        "",
        "## 总览",
        "",
        "| 指标 | 数量 |",
        "|---|---:|",
        f"| manifest 条目 | {len(items)} |",
        f"| 有 URL 条目 | {with_urls} |",
        f"| 官方页面已核验 | {verified} |",
        f"| 有 Markdown 派生件 | {with_derived} |",
        f"| 已进入文本缓存 | {with_cache} |",
        f"| 缓存中有可检索正文 | {cached_text} |",
        "",
        "## 文件类型",
        "",
        "| 类型 | 数量 |",
        "|---|---:|",
    ]
    for suffix, count in sorted(suffix_counts.items()):
        lines.append(f"| `{suffix}` | {count} |")

    lines.extend(["", "## 待办类型", "", "| 待办 | 数量 |", "|---|---:|"])
    if action_counts:
        for action, count in sorted(action_counts.items()):
            lines.append(f"| `{action}` | {count} |")
    else:
        lines.append("| 无 | 0 |")

    flagged = [item for item in items if item.actions]
    lines.extend(
        [
            "",
            "## 待处理条目",
            "",
            "| 条目 | 文号 | 来源 | 状态 | 待办 | wiki |",
            "|---|---|---|---|---|---|",
        ]
    )
    if flagged:
        for item in flagged:
            status = (
                f"source={item.official_page_status}; text={item.text_extraction_status}; "
                f"ocr={item.ocr_status}; derived={'ok' if item.derived_exists else 'missing'}"
            )
            source = item.official_source or item.manifest_path
            actions = ", ".join(f"`{action}`" for action in item.actions)
            lines.append(
                f"| {item.title} | {item.document_no} | {source} | {status} | {actions} | {wiki_link(item.wiki_page)} |"
            )
    else:
        lines.append("| 无 |  |  |  |  |  |")

    lines.extend(
        [
            "",
            "## 全部 manifest 条目",
            "",
            "| 条目 | 原件 | Markdown 派生件 | URL | 缓存正文长度 | wiki |",
            "|---|---|---|---|---:|---|",
        ]
    )
    for item in items:
        text_length = "" if item.cache_text_length is None else str(item.cache_text_length)
        url = item.url or ""
        lines.append(
            f"| {item.title} | `{item.local_file}` | `{item.derived_markdown}` | {url} | {text_length} | {wiki_link(item.wiki_page)} |"
        )

    lines.extend(
        [
            "",
            "## 使用说明",
            "",
            "- `missing-local-file`：manifest 指向的原件不存在，应恢复官方 PDF/HTML/DOCX 或补来源说明。",
            "- `missing-derived-markdown`：原件存在但缺少 Markdown 派生件，检索和加工体验会下降。",
            "- `ocr-pending`：PDF 已归档但文本为空，适合后续 OCR 或手工补正文。",
            "- `verify-official-url`：已有来源但官方具体原文页仍需复核。",
            "- `missing-official-url`：manifest 中没有 URL，应补官方来源或本地来源说明。",
            "- `not-in-text-cache`：raw 文件还没有进入 `cache/text/`，运行 `tools/kb.py cache build`。",
            "",
            f"_生成路径：`{rel(root, root / REPORT_PATH)}`_",
        ]
    )
    return "\n".join(lines) + "\n"


def print_summary(items: list[SourceItem]) -> None:
    action_counts = Counter(action for item in items for action in item.actions)
    print(f"items={len(items)}")
    print(f"flagged={sum(1 for item in items if item.actions)}")
    for action, count in sorted(action_counts.items()):
        print(f"{action}={count}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Report CPA-ZH raw source status.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("summary", help="Print source status counts.")
    report_parser = subparsers.add_parser("write-report", help="Write the wiki source status dashboard.")
    report_parser.add_argument("--output", default=str(REPORT_PATH), help="Output path under the knowledge base root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    items = collect_items(root)

    if args.command == "summary":
        print_summary(items)
        return 0
    if args.command == "write-report":
        output = root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_markdown(root, items), encoding="utf-8", newline="\n")
        print(f"written={output}")
        print_summary(items)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
