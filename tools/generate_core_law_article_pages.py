from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
RAW_LAWS = KB / "raw" / "laws"
OUT_DIR = KB / "wiki" / "concepts" / "laws"
INDEX_DIR = KB / "raw" / "indexes"

LAW_CONFIG = {
    "中华人民共和国注册会计师法.md": {
        "slug": "cpa-law",
        "concept": "concepts/law-cpa",
        "tags": ["cpa", "law", "article", "p1-core"],
    },
    "中华人民共和国会计法.md": {
        "slug": "accounting-law",
        "concept": "concepts/law-accounting",
        "tags": ["accounting", "law", "article", "p1-core"],
    },
    "中华人民共和国公司法.md": {
        "slug": "company-law",
        "concept": "concepts/law-company",
        "tags": ["company-law", "law", "article", "p1-core"],
    },
    "中华人民共和国证券法.md": {
        "slug": "securities-law",
        "concept": "concepts/law-securities",
        "tags": ["securities-law", "law", "article", "p1-core"],
    },
}

LAW_CONFIG_BY_SLUG = {str(config["slug"]): config for config in LAW_CONFIG.values()}


CHAPTER_RE = re.compile(r"^(?:#{1,3}\s*)?第[一二三四五六七八九十百零〇]+章[ 　]*(.+?)\s*$")
SECTION_RE = re.compile(r"^(?:#{1,4}\s*)?第[一二三四五六七八九十百零〇]+节[ 　]*(.+?)\s*$")
ARTICLE_RE = re.compile(r"^第([一二三四五六七八九十百零〇]+)条[ 　]*(.*)$")


def chinese_to_int(text: str) -> int:
    text = text.replace("〇", "零")
    digits = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    units = {"十": 10, "百": 100, "千": 1000}
    total = 0
    section = 0
    number = 0
    for char in text:
        if char in digits:
            number = digits[char]
        elif char in units:
            unit = units[char]
            if number == 0:
                number = 1
            section += number * unit
            number = 0
        else:
            raise ValueError(f"unsupported numeral: {text}")
    total += section + number
    return total


def clean_heading(line: str) -> str:
    return re.sub(r"^#{1,6}\s*", "", line).strip()


def first_sentence(text: str, limit: int = 90) -> str:
    compact = re.sub(r"\s+", "", text)
    compact = re.sub(r"^第[一二三四五六七八九十百零〇]+条", "", compact)
    if not compact:
        return ""
    for marker in ("。", "；", ";"):
        pos = compact.find(marker)
        if 0 <= pos < limit:
            return compact[: pos + 1]
    return compact[:limit] + ("..." if len(compact) > limit else "")


def parse_law(path: Path) -> list[dict[str, str | int]]:
    title = path.stem
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    chapter = ""
    section = ""
    articles: list[dict[str, str | int]] = []
    current: dict[str, str | int] | None = None
    body_lines: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            if current is not None:
                body_lines.append("")
            continue

        chapter_match = CHAPTER_RE.match(line)
        if chapter_match:
            chapter = clean_heading(line)
            section = ""
            if current is not None:
                current["body"] = "\n".join(body_lines).strip()
                articles.append(current)
                current = None
                body_lines = []
            continue

        section_match = SECTION_RE.match(line)
        if section_match:
            section = clean_heading(line)
            if current is not None:
                current["body"] = "\n".join(body_lines).strip()
                articles.append(current)
                current = None
                body_lines = []
            continue

        article_match = ARTICLE_RE.match(line)
        if article_match:
            if current is not None:
                current["body"] = "\n".join(body_lines).strip()
                articles.append(current)
            article_no_cn = article_match.group(1)
            lead = article_match.group(2).strip()
            article_no = chinese_to_int(article_no_cn)
            current = {
                "law": title,
                "article_no": article_no,
                "article_no_cn": article_no_cn,
                "chapter": chapter,
                "section": section,
            }
            body_lines = [f"第{article_no_cn}条 {lead}".strip()]
            continue

        if current is not None:
            body_lines.append(line)

    if current is not None:
        current["body"] = "\n".join(body_lines).strip()
        articles.append(current)

    return articles


def md_escape_table(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def write_article_page(config: dict[str, object], row: dict[str, str | int], source_path: Path) -> str:
    slug = str(config["slug"])
    article_no = int(row["article_no"])
    duplicate_ordinal = int(row.get("duplicate_ordinal", 1))
    duplicate_suffix = "" if duplicate_ordinal == 1 else f"-{duplicate_ordinal}"
    filename = f"{slug}-article-{article_no:03d}{duplicate_suffix}.md"
    page_path = OUT_DIR / slug / filename
    page_path.parent.mkdir(parents=True, exist_ok=True)
    tags = ", ".join(str(tag) for tag in config["tags"])
    title = f"{row['law']}第{row['article_no_cn']}条"
    body = str(row["body"]).strip()
    summary = first_sentence(body)
    section_line = f"- 节：{row['section']}\n" if row["section"] else ""
    content = f"""---
title: {title}
type: concept
concept_type: law-article
created: 2026-06-26
updated: 2026-06-26
sources: [local-core-laws-2026-06-26]
tags: [{tags}]
related: [[{config["concept"]}]], [[sources/core-laws-article-index-2026-06-26]]
---

# {title}

## 定位

- 法律：{row['law']}
- 章节：{row['chapter']}
{section_line}- 条号：第{row['article_no_cn']}条
- 本地原文：`{source_path.relative_to(KB).as_posix()}`

## 条文原文

{body}

## 检索摘要

{summary}
"""
    page_path.write_text(content, encoding="utf-8")
    return f"concepts/laws/{slug}/{filename[:-3]}"


def write_law_index(slug: str, rows: list[dict[str, str | int]]) -> str:
    config = LAW_CONFIG_BY_SLUG[slug]
    law = str(rows[0]["Law"])
    index_path = OUT_DIR / slug / "index.md"
    tag_list = ", ".join(str(tag) for tag in config["tags"])
    lines = [
        "---",
        f"title: {law}条款目录",
        "type: concept",
        "concept_type: law-article-index",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [local-core-laws-2026-06-26]",
        f"tags: [{tag_list}, article-index]",
        f"related: [[{config['concept']}]], [[sources/core-laws-article-index-2026-06-26]]",
        "---",
        "",
        f"# {law}条款目录",
        "",
        "## 汇总",
        "",
        f"- 条款记录数：{len(rows)}",
        "- 条款页：本目录下按条号生成。",
        "- 说明：如原文存在重复条号，第二个及以后条款页文件名会追加序号后缀。",
        "",
        "## 条款",
        "",
        "| 条号 | 章节 | 摘要 | 页面 |",
        "|---:|---|---|---|",
    ]
    for row in rows:
        suffix = "" if int(row["DuplicateOrdinal"]) == 1 else f"（第{row['DuplicateOrdinal']}个同号条款）"
        lines.append(
            "| {no}{suffix} | {chapter} | {summary} | [[{page}]] |".format(
                no=row["ArticleNo"],
                suffix=suffix,
                chapter=md_escape_table(str(row["Chapter"])),
                summary=md_escape_table(str(row["Summary"])),
                page=row["WikiPage"],
            )
        )
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return f"concepts/laws/{slug}/index"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str | int]] = []
    for filename, config in LAW_CONFIG.items():
        source_path = RAW_LAWS / filename
        article_counts: Counter[int] = Counter()
        for article in parse_law(source_path):
            article_no = int(article["article_no"])
            article_counts[article_no] += 1
            article["duplicate_ordinal"] = article_counts[article_no]
            page_link = write_article_page(config, article, source_path)
            body = str(article["body"])
            rows.append(
                {
                    "Law": article["law"],
                    "ArticleNo": article["article_no"],
                    "ArticleNoCn": article["article_no_cn"],
                    "DuplicateOrdinal": article["duplicate_ordinal"],
                    "Chapter": article["chapter"],
                    "Section": article["section"],
                    "Summary": first_sentence(body, 120),
                    "WikiPage": page_link,
                    "RawPath": source_path.relative_to(KB).as_posix(),
                }
            )

    per_law_index_links: dict[str, str] = {}
    for slug in LAW_CONFIG_BY_SLUG:
        law_rows = [row for row in rows if str(row["WikiPage"]).startswith(f"concepts/laws/{slug}/")]
        if law_rows:
            per_law_index_links[slug] = write_law_index(slug, law_rows)

    csv_path = INDEX_DIR / "core-laws-article-index.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(str(row["Law"]) for row in rows)
    md_lines = [
        "# 四部核心法律条款级索引",
        "",
        "生成日期：2026-06-26",
        "",
        "## 汇总",
        "",
        "| 法律 | 条款数 |",
        "|---|---:|",
    ]
    for law, count in counts.items():
        md_lines.append(f"| {md_escape_table(law)} | {count} |")
    md_lines.extend(
        [
            f"| 合计 | {len(rows)} |",
            "",
            "## 文件",
            "",
            "- CSV 明细：`raw/indexes/core-laws-article-index.csv`",
            "- 条款页目录：`wiki/concepts/laws/`",
            "",
            "## 分法律条款目录",
            "",
        ]
    )
    for slug, link in per_law_index_links.items():
        law_rows = [row for row in rows if str(row["WikiPage"]).startswith(f"concepts/laws/{slug}/")]
        md_lines.append(f"- [[{link}]] - {law_rows[0]['Law']}，{len(law_rows)} 条记录")
    md_lines.extend(
        [
            "",
            "## 条款索引",
            "",
            "| 法律 | 条号 | 章节 | 摘要 | Wiki 页 |",
            "|---|---:|---|---|---|",
        ]
    )
    for row in rows:
        md_lines.append(
            "| {law} | {no} | {chapter} | {summary} | [[{page}]] |".format(
                law=md_escape_table(str(row["Law"])),
                no=row["ArticleNo"],
                chapter=md_escape_table(str(row["Chapter"])),
                summary=md_escape_table(str(row["Summary"])),
                page=row["WikiPage"],
            )
        )
    (INDEX_DIR / "core-laws-article-index.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"articles={len(rows)} csv={csv_path} md={INDEX_DIR / 'core-laws-article-index.md'}")
    for law, count in counts.items():
        print(f"{law}: {count}")


if __name__ == "__main__":
    main()
