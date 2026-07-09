from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
ACCOUNTING_RAW = KB / "raw" / "standards" / "accounting"
WIKI_DIR = KB / "wiki" / "concepts" / "accounting-standards" / "interpretations"
INDEX_DIR = KB / "raw" / "indexes"

CSV_PATH = ACCOUNTING_RAW / "downloaded-enterprise-accounting-standards-interpretations.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rel(path_text: str) -> str:
    if not path_text:
        return ""
    path = Path(path_text)
    try:
        return path.relative_to(KB).as_posix()
    except ValueError:
        return path.as_posix()


def normalize(title: str) -> str:
    return re.sub(r"\s+", "", title).replace("《", "").replace("》", "")


def parse_number(title: str) -> str:
    match = re.search(r"解释第([0-9０-９]+)号", title)
    if not match:
        return ""
    return match.group(1).translate(str.maketrans("０１２３４５６７８９", "0123456789"))


def short_topic(title: str, number: str) -> str:
    if "——" in title:
        return title.split("——", 1)[1].rstrip("》")
    if "关于印发" in title:
        return f"企业会计准则解释第{number}号"
    return title


def page_key(number: str) -> str:
    return f"interp-{int(number):02d}"


def write_page(row: dict[str, str], number: str) -> str:
    key = page_key(number)
    page = WIKI_DIR / f"{key}.md"
    title = short_topic(row["Title"], number)
    local_path = rel(row.get("LocalFile", ""))
    lines = [
        "---",
        f"title: 企业会计准则解释第{number}号",
        "type: concept",
        "concept_type: accounting-interpretation",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [enterprise-accounting-standards-interpretations-download-2026-06-26]",
        "tags: [accounting, standards, interpretation, p1-core]",
        "related: [[concepts/accounting-standards-system]], [[sources/enterprise-accounting-standards-interpretations-download-2026-06-26]]",
        "---",
        "",
        f"# 企业会计准则解释第{number}号",
        "",
        "## 定位",
        "",
        f"- 解释编号：{number}",
        f"- 标题：{title}",
        f"- 本地文件：`{local_path}`",
        f"- 官方链接：{row['Url']}",
        "",
        "## 原文入口",
        "",
        f"- 通知/原文页面：{row['Url']}",
        f"- 本地 HTML：`{local_path}`",
        "",
        "## 备注",
        "",
        "该页先作为解释编号级索引入口，后续可继续补充逐条适用事项、关键会计处理和相关准则连接。",
    ]
    page.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return f"concepts/accounting-standards/interpretations/{key}"


def main() -> None:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_csv(CSV_PATH)
    page_rows: list[dict[str, str]] = []
    for row in rows:
        number = parse_number(normalize(row["Title"]))
        if not number:
            continue
        page_link = write_page(row, number)
        page_rows.append(
            {
                "InterpretationNo": number,
                "Title": row["Title"],
                "Url": row["Url"],
                "LocalPath": rel(row.get("LocalFile", "")),
                "WikiPage": page_link,
            }
        )

    write_csv(INDEX_DIR / "accounting-interpretations-index.csv", page_rows)

    index_lines = [
        "# 企业会计准则解释编号索引",
        "",
        "生成日期：2026-06-26",
        "",
        "## 文件",
        "",
        "- 索引 CSV：`raw/indexes/accounting-interpretations-index.csv`",
        "- 解释页目录：`wiki/concepts/accounting-standards/interpretations/`",
        "",
        "## 列表",
        "",
        "| 编号 | 标题 | 页面 |",
        "|---:|---|---|",
    ]
    for row in sorted(page_rows, key=lambda r: int(r["InterpretationNo"])):
        index_lines.append(f"| {row['InterpretationNo']} | {row['Title']} | [[{row['WikiPage']}]] |")
    (INDEX_DIR / "accounting-interpretations-index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(f"interpretations={len(page_rows)}")


if __name__ == "__main__":
    main()
