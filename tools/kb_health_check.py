from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import kb_manifest_audit
from kb_common import parse_frontmatter


@dataclass
class SearchStats:
    by_kind: dict[str, int]
    total: int
    db_exists: bool
    stale: bool


@dataclass
class TextCacheStats:
    manifest_exists: bool
    items: int
    cached: int
    empty: int
    stale: bool
    generated_at: str


TEXT_CACHE_SKIP_NAMES = {"metadata.json", "source-url.txt", "manifest.json", "archive-index.jsonl"}

# 与 kb_text_cache.py 保持一致：归档与位图类文件无可抽取文本，不进文本缓存。
TEXT_CACHE_SKIP_SUFFIXES = {
    ".zip", ".rar", ".7z", ".tar", ".gz", ".tgz", ".tar.gz",
    ".bz2", ".xz", ".jar", ".iso",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp",
}


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


def count_wiki_links(root: Path) -> tuple[int, list[tuple[str, str]]]:
    wiki_root = root / "wiki"
    active_pages = [p for p in wiki_root.rglob("*.md") if "_trash" not in p.relative_to(wiki_root).parts]
    pages = {p.relative_to(wiki_root).with_suffix("").as_posix() for p in active_pages}
    missing: list[tuple[str, str]] = []
    for page in active_pages:
        text = page.read_text(encoding="utf-8")
        for match in re.finditer(r"\[\[([^\]|#]+)", text):
            target = match.group(1)
            raw_target_exists = target.startswith("raw/") and (root / target).is_file()
            if target not in pages and not raw_target_exists:
                missing.append((rel(root, page), target))
    return len(pages), missing


def search_stats(root: Path) -> SearchStats:
    db_path = root / "search" / "kb_search.sqlite"
    if not db_path.exists():
        return SearchStats(by_kind={}, total=0, db_exists=False, stale=True)

    connection = sqlite3.connect(db_path)
    rows = connection.execute("SELECT kind, COUNT(*) FROM documents GROUP BY kind ORDER BY kind").fetchall()
    total = connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    connection.close()

    db_mtime = db_path.stat().st_mtime
    indexed_roots = [root / "wiki", root / "raw"]
    newest_source_mtime = 0.0
    for indexed_root in indexed_roots:
        if indexed_root.exists():
            for source in indexed_root.rglob("*"):
                if source.is_file():
                    if indexed_root == root / "raw":
                        source_rel = source.relative_to(indexed_root)
                        if "_archive" in source_rel.parts or source.name.endswith(".structure.json"):
                            continue
                    newest_source_mtime = max(newest_source_mtime, source.stat().st_mtime)

    return SearchStats(
        by_kind={str(kind): int(count) for kind, count in rows},
        total=int(total),
        db_exists=True,
        stale=newest_source_mtime > db_mtime,
    )


def text_cache_stats(root: Path) -> TextCacheStats:
    manifest_path = root / "cache" / "text" / "manifest.json"
    if not manifest_path.exists():
        return TextCacheStats(
            manifest_exists=False,
            items=0,
            cached=0,
            empty=0,
            stale=True,
            generated_at="",
        )

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = data.get("items", []) if isinstance(data, dict) else []
    by_raw_path = {str(item.get("raw_path")): item for item in items if item.get("raw_path")}

    cacheable_raw_files = []
    for raw_file in (root / "raw").rglob("*"):
        if (
            raw_file.is_file()
            and raw_file.name not in TEXT_CACHE_SKIP_NAMES
            and not raw_file.name.endswith(".structure.json")
            and raw_file.suffix.lower() not in TEXT_CACHE_SKIP_SUFFIXES
        ):
            cacheable_raw_files.append(raw_file)

    stale = False
    for raw_file in cacheable_raw_files:
        raw_path = rel(root, raw_file)
        item = by_raw_path.get(raw_path)
        if not item:
            stale = True
            continue
        stat = raw_file.stat()
        cache_path = root / str(item.get("cache_path") or "")
        if item.get("mtime_ns") != stat.st_mtime_ns or item.get("bytes") != stat.st_size:
            stale = True
        if not cache_path.exists():
            stale = True

    raw_paths = {rel(root, raw_file) for raw_file in cacheable_raw_files}
    if any(raw_path not in raw_paths for raw_path in by_raw_path):
        stale = True

    cached = sum(1 for item in items if int(item.get("text_length") or 0) > 0)
    return TextCacheStats(
        manifest_exists=True,
        items=len(items),
        cached=cached,
        empty=len(items) - cached,
        stale=stale,
        generated_at=str(data.get("generated_at") or ""),
    )


def case_link_issues(root: Path) -> list[str]:
    issues: list[str] = []
    cases_root = root / "wiki" / "cases"
    if not cases_root.exists():
        return issues

    index_text = (root / "wiki" / "index.md").read_text(encoding="utf-8")
    case_analysis_path = root / "wiki" / "concepts" / "case-analysis.md"
    case_analysis_text = case_analysis_path.read_text(encoding="utf-8") if case_analysis_path.exists() else ""
    case_topic_index_path = root / "wiki" / "concepts" / "case-topic-index.md"
    case_topic_index_text = case_topic_index_path.read_text(encoding="utf-8") if case_topic_index_path.exists() else ""
    golden_index_path = cases_root / "golden-cases-index.md"
    golden_index_text = golden_index_path.read_text(encoding="utf-8") if golden_index_path.exists() else ""
    entrypoint_targets = {
        match.group(1)
        for text in [index_text, case_analysis_text, case_topic_index_text, golden_index_text]
        for match in re.finditer(r"\[\[([^\]|#]+)", text)
    }

    for case_page in case_card_paths(root):
        target = case_page.relative_to(root / "wiki").with_suffix("").as_posix()
        if target not in entrypoint_targets:
            issues.append(
                f"{rel(root, case_page)} not linked from wiki/index.md, concepts/case-analysis.md, or concepts/case-topic-index.md"
            )
    return issues


def case_card_paths(root: Path) -> list[Path]:
    cases_root = root / "wiki" / "cases"
    if not cases_root.exists():
        return []
    cards: list[Path] = []
    for path in sorted(cases_root.rglob("*.md")):
        metadata, _body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if metadata.get("page_role") == "case":
            cards.append(path)
    return cards


def readme_stat_warnings(root: Path, stats: dict[str, int], search: SearchStats) -> list[str]:
    readme = root / "README.md"
    if not readme.exists():
        return ["README.md is missing"]

    text = readme.read_text(encoding="utf-8")
    expected_pairs = {
        "wiki 页面": stats["wiki_pages"],
        "raw 原始文件": stats["raw_files"],
        "manifest 批次": stats["manifest_count"],
        "本地检索索引记录": search.total,
        "实务案例卡片": stats["case_cards"],
    }
    warnings: list[str] = []
    for label, expected in expected_pairs.items():
        pattern = rf"\| {re.escape(label)} \| ([0-9]+) \|"
        match = re.search(pattern, text)
        if not match:
            warnings.append(f"README missing stat row: {label}")
        elif int(match.group(1)) != expected:
            warnings.append(f"README stat stale: {label} readme={match.group(1)} actual={expected}")
    return warnings


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Run a one-command health check for CPA-ZH.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    raw_root = root / "raw"
    wiki_root = root / "wiki"

    manifests = sorted(raw_root.rglob("manifest.json"))
    manifest_issues: list[str] = []
    manifest_items = 0
    for manifest in manifests:
        items = load_manifest(manifest)
        manifest_items += len(items)
        manifest_issues.extend(kb_manifest_audit.audit_manifest(root, manifest))

    wiki_pages, missing_links = count_wiki_links(root)
    search = search_stats(root)
    text_cache = text_cache_stats(root)
    case_issues = case_link_issues(root)

    stats = {
        "wiki_pages": wiki_pages,
        "raw_files": sum(1 for p in raw_root.rglob("*") if p.is_file()),
        "manifest_count": len(manifests),
        "manifest_items": manifest_items,
        "case_cards": len(case_card_paths(root)),
    }
    readme_warnings = readme_stat_warnings(root, stats, search)

    print("# CPA-ZH Health Check")
    print(f"root={root}")
    print()
    print("## Summary")
    print(f"- wiki_pages={stats['wiki_pages']}")
    print(f"- raw_files={stats['raw_files']}")
    print(f"- manifests={stats['manifest_count']}")
    print(f"- manifest_items={stats['manifest_items']}")
    print(f"- case_cards={stats['case_cards']}")
    print(f"- search_index={'present' if search.db_exists else 'missing'} total={search.total} stale={search.stale}")
    print(
        f"- text_cache={'present' if text_cache.manifest_exists else 'missing'} "
        f"items={text_cache.items} cached={text_cache.cached} empty={text_cache.empty} stale={text_cache.stale}"
    )
    print()

    print("## Search Index")
    if search.db_exists:
        for kind, count in sorted(search.by_kind.items()):
            print(f"- {kind}: {count}")
    else:
        print("- missing search/kb_search.sqlite")
    print()

    hard_issues: list[str] = []
    if manifest_issues:
        hard_issues.extend(f"manifest: {issue}" for issue in manifest_issues)
    if missing_links:
        hard_issues.extend(f"missing-link: {page} -> [[{target}]]" for page, target in missing_links)
    if case_issues:
        hard_issues.extend(f"case-link: {issue}" for issue in case_issues)

    warnings: list[str] = []
    if search.stale:
        warnings.append("search index is older than at least one wiki/raw file; run kb_search.py index")
    if not text_cache.manifest_exists:
        warnings.append("text cache is missing; run kb_text_cache.py build")
    elif text_cache.stale:
        warnings.append("text cache is stale; run kb_text_cache.py build")
    warnings.extend(readme_warnings)

    print("## Issues")
    if hard_issues:
        for issue in hard_issues:
            print(f"- ERROR {issue}")
    else:
        print("- none")
    print()

    print("## Warnings")
    if warnings:
        for warning in warnings:
            print(f"- WARN {warning}")
    else:
        print("- none")

    return 1 if hard_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
