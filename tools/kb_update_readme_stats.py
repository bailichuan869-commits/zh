from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from datetime import date
from pathlib import Path

from kb_common import parse_frontmatter


def search_counts(root: Path) -> tuple[dict[str, int], int]:
    db_path = root / "search" / "kb_search.sqlite"
    if not db_path.exists():
        return {}, 0
    connection = sqlite3.connect(db_path)
    rows = connection.execute("SELECT kind, COUNT(*) FROM documents GROUP BY kind ORDER BY kind").fetchall()
    total = connection.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    connection.close()
    return {str(kind): int(count) for kind, count in rows}, int(total)


def manifest_rows(root: Path) -> list[tuple[str, int]]:
    rows: list[tuple[str, int]] = []
    for manifest in sorted((root / "raw").rglob("manifest.json")):
        import json

        data = json.loads(manifest.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else data.get("items", [])
        rows.append((manifest.relative_to(root).as_posix(), len(items)))
    return rows


def replace_section(text: str, heading: str, replacement: str) -> str:
    pattern = rf"(## {re.escape(heading)}\n)(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, flags=re.S)
    if not match:
        raise ValueError(f"README section not found: {heading}")
    return text[: match.start()] + match.group(1) + replacement.rstrip() + "\n" + text[match.end() :]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Refresh CPA-ZH README statistics.")
    parser.add_argument("--root", default="knowledge-base/CPA-ZH", help="Knowledge base root.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Date to write into README.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    readme = root / "README.md"
    text = readme.read_text(encoding="utf-8")

    wiki_pages = sum(
        1
        for page in (root / "wiki").rglob("*.md")
        if "_trash" not in page.relative_to(root / "wiki").parts
    )
    raw_files = sum(1 for p in (root / "raw").rglob("*") if p.is_file())
    manifests = manifest_rows(root)
    case_cards = 0
    if (root / "wiki" / "cases").exists():
        for path in (root / "wiki" / "cases").rglob("*.md"):
            metadata, _body = parse_frontmatter(path.read_text(encoding="utf-8"))
            case_cards += metadata.get("page_role") == "case"
    by_kind, total = search_counts(root)

    text = re.sub(
        r"截至 \d{4}-\d{2}-\d{2}，",
        f"截至 {args.date}，",
        text,
        count=1,
    )

    status_section = f"""

| 项目 | 数量或状态 |
|---|---:|
| wiki 页面 | {wiki_pages} |
| raw 原始文件 | {raw_files} |
| manifest 批次 | {len(manifests)} |
| 本地检索索引记录 | {total} |
| 实务案例卡片 | {case_cards} |
| wiki 内链状态 | 最近检查为 0 缺失 |
| Python 运行方式 | 统一使用工作区虚拟环境 `.venv` |
"""
    text = replace_section(text, "当前状态", status_section)

    search_table = "\n| 类型 | 数量 |\n|---|---:|\n"
    for kind, count in sorted(by_kind.items()):
        search_table += f"| {kind} | {count} |\n"
    search_table += f"| total | {total} |\n"
    text = re.sub(
        r"当前索引构成：\n\n\| 类型 \| 数量 \|\n\|---\|---:\|\n(?:\| .*? \| [0-9]+ \|\n)+",
        "当前索引构成：\n" + search_table,
        text,
        flags=re.S,
    )

    manifest_table = "\n| manifest | 条目 |\n|---|---:|\n"
    for path, count in manifests:
        manifest_table += f"| `{path}` | {count} |\n"
    text = re.sub(
        r"当前 manifest：\n\n\| manifest \| 条目 \|\n\|---\|---:\|\n(?:\| `.*?` \| [0-9]+ \|\n)+",
        "当前 manifest：\n" + manifest_table,
        text,
        flags=re.S,
    )

    readme.write_text(text, encoding="utf-8")
    print(f"updated={readme}")
    print(f"wiki_pages={wiki_pages}")
    print(f"raw_files={raw_files}")
    print(f"manifests={len(manifests)}")
    print(f"search_total={total}")
    print(f"case_cards={case_cards}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
