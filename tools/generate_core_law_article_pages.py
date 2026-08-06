from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

from kb_common import normalize_core_law_article_links


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
RAW_LAWS = KB / "raw" / "laws"
OUT_DIR = KB / "wiki" / "concepts" / "laws"
INDEX_DIR = KB / "raw" / "indexes"

LAW_CONFIG = {
    "中华人民共和国注册会计师法-2026-草案.md": {
        "slug": "cpa-law",
        "title": "中华人民共和国注册会计师法（2026 修订草案）",
        "concept": "concepts/law-cpa",
        "tags": ["cpa", "law", "p1-core"],
        "version_note": "本页基于 2026 修订草案手工套用文本，非官方重新公布全文；正式引用前应以官方重排版核对。",
    },
    "中华人民共和国会计法.md": {
        "slug": "accounting-law",
        "concept": "concepts/law-accounting",
        "tags": ["accounting", "law", "p1-core"],
    },
    "中华人民共和国公司法.md": {
        "slug": "company-law",
        "concept": "concepts/law-company",
        "tags": ["company-law", "law", "p1-core"],
    },
    "中华人民共和国证券法.md": {
        "slug": "securities-law",
        "concept": "concepts/law-securities",
        "tags": ["securities-law", "law", "p1-core"],
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
    return total + section + number


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

    def finish() -> None:
        nonlocal current, body_lines
        if current is not None:
            current["body"] = "\n".join(body_lines).strip()
            articles.append(current)
            current = None
            body_lines = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            if current is not None:
                body_lines.append("")
            continue
        if CHAPTER_RE.match(line):
            finish()
            chapter = clean_heading(line)
            section = ""
            continue
        if SECTION_RE.match(line):
            finish()
            section = clean_heading(line)
            continue
        article_match = ARTICLE_RE.match(line)
        if article_match:
            finish()
            article_no_cn = article_match.group(1)
            current = {
                "law": title,
                "article_no": chinese_to_int(article_no_cn),
                "article_no_cn": article_no_cn,
                "chapter": chapter,
                "section": section,
            }
            body_lines = [f"第{article_no_cn}条 {article_match.group(2).strip()}".strip()]
            continue
        if current is not None:
            body_lines.append(line)
    finish()
    return articles


def md_escape_table(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def article_anchor(article_no: int, duplicate_ordinal: int = 1) -> str:
    suffix = "" if duplicate_ordinal == 1 else f"-{duplicate_ordinal}"
    return f"article-{article_no:03d}{suffix}"


def article_heading(article_no_cn: str, anchor: str) -> str:
    return f"### 第{article_no_cn}条 {{#{anchor}}}"


def write_law_index(
    slug: str,
    rows: list[dict[str, str | int]],
    source_path: Path,
    *,
    apply: bool,
) -> str:
    config = LAW_CONFIG_BY_SLUG[slug]
    law = str(rows[0]["law"])
    index_path = OUT_DIR / slug / "index.md"
    tag_list = ", ".join(str(tag) for tag in config["tags"])
    lines = [
        "---",
        f"title: {law}条款全文与索引",
        "type: concept",
        "concept_type: law-article-index",
        "created: 2026-06-26",
        "updated: 2026-08-05",
        "sources: [local-core-laws-2026-06-26]",
        f"tags: [{tag_list}, article-index]",
        f"related: [[{config['concept']}]], [[sources/core-laws-article-index-2026-06-26]]",
        "---",
        "",
        f"# {law}条款全文与索引",
        "",
        "## 使用说明",
        "",
        f"- 本页按本地原文 `{source_path.relative_to(KB).as_posix()}` 编排，保留全部 {len(rows)} 条条文。",
        "- 条文标题带有稳定锚点，可从专题页和搜索结果直接定位；专业解释、实务判断或版本差异应沉淀到主题页，不再按条文生成独立知识页。",
    ]
    version_note = config.get("version_note")
    if version_note:
        lines.append(f"- 版本提示：{version_note}")
    if slug == "cpa-law":
        lines.append("- 2026 修订资料：[[concepts/laws/cpa-law/2026-amendment-highlights]]、[[sources/cpa-law-amendment-2026]]。")
    lines.extend(
        [
            "",
            "## 条款索引",
            "",
            "| 条号 | 章节 | 摘要 | 页面 |",
            "|---:|---|---|---|",
        ]
    )
    for row in rows:
        anchor = article_anchor(int(row["article_no"]), int(row["duplicate_ordinal"]))
        page = f"concepts/laws/{slug}/index#{anchor}"
        label = "全文索引锚点"
        suffix = "" if int(row["duplicate_ordinal"]) == 1 else f"（第{row['duplicate_ordinal']}个同号条款）"
        lines.append(
            f"| {row['article_no']}{suffix} | {md_escape_table(str(row['chapter']))} | "
            f"{md_escape_table(first_sentence(str(row['body']), 120))} | [[{page}|{label}]] |"
        )
    lines.extend(["", "## 条文全文", ""])
    for row in rows:
        anchor = article_anchor(int(row["article_no"]), int(row["duplicate_ordinal"]))
        lines.extend(
            [
                article_heading(str(row["article_no_cn"]), anchor),
                "",
                str(row["body"]).strip(),
                "",
            ]
        )
    if apply:
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return f"concepts/laws/{slug}/index"


def rewrite_article_links(*, apply: bool) -> tuple[int, list[str]]:
    changed = 0
    paths: list[str] = []
    for page in sorted((KB / "wiki").rglob("*.md")):
        rel = page.relative_to(KB / "wiki").as_posix()
        if re.match(r"^concepts/laws/(accounting-law|company-law|cpa-law|securities-law)/.+-article-\d{3}(?:-\d+)?\.md$", rel):
            continue
        text = page.read_text(encoding="utf-8-sig", errors="ignore")
        updated, count = normalize_core_law_article_links(text)
        if count:
            changed += count
            paths.append(rel)
            if apply:
                page.write_text(updated, encoding="utf-8", newline="\n")
    return changed, paths


def remove_article_pages(*, apply: bool) -> list[Path]:
    removed: list[Path] = []
    for slug in LAW_CONFIG_BY_SLUG:
        directory = OUT_DIR / slug
        if not directory.exists():
            continue
        for path in directory.glob(f"{slug}-article-*.md"):
            removed.append(path)
            if apply:
                path.unlink()
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(description="Build consolidated core-law full-text indexes.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write consolidated indexes, rewrite legacy links, and remove legacy article pages.",
    )
    args = parser.parse_args()
    apply = bool(args.apply)
    if apply:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
    link_count, link_paths = rewrite_article_links(apply=apply)
    rows: list[dict[str, str | int]] = []
    per_law_index_links: dict[str, str] = {}

    for filename, config in LAW_CONFIG.items():
        source_path = RAW_LAWS / filename
        article_counts: Counter[int] = Counter()
        parsed = parse_law(source_path)
        for article in parsed:
            article["law"] = str(config.get("title") or article["law"])
            article_no = int(article["article_no"])
            article_counts[article_no] += 1
            article["duplicate_ordinal"] = article_counts[article_no]
            wiki_page = f"concepts/laws/{config['slug']}/index#{article_anchor(article_no, article_counts[article_no])}"
            rows.append(
                {
                    "Law": article["law"],
                    "ArticleNo": article_no,
                    "ArticleNoCn": article["article_no_cn"],
                    "DuplicateOrdinal": article["duplicate_ordinal"],
                    "Chapter": article["chapter"],
                    "Section": article["section"],
                    "Summary": first_sentence(str(article["body"]), 120),
                    "WikiPage": wiki_page,
                    "Standalone": "no",
                    "RawPath": source_path.relative_to(KB).as_posix(),
                }
            )
        per_law_index_links[str(config["slug"])] = write_law_index(
            str(config["slug"]),
            parsed,
            source_path,
            apply=apply,
        )

    removed = remove_article_pages(apply=apply)

    csv_path = INDEX_DIR / "core-laws-article-index.csv"
    if apply:
        with csv_path.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    counts = Counter(str(row["Law"]) for row in rows)
    md_lines = [
        "# 四部核心法律条款级索引",
        "",
        "生成日期：2026-08-05",
        "",
        "## 汇总",
        "",
        "| 法律 | 条款数 | 合并全文索引页 |",
        "|---|---:|---:|",
    ]
    for law, count in counts.items():
        md_lines.append(f"| {md_escape_table(law)} | {count} | 1 |")
    md_lines.extend(
        [
            f"| 合计 | {len(rows)} | {len(per_law_index_links)} |",
            "",
            "## 文件",
            "",
            "- CSV 明细：`raw/indexes/core-laws-article-index.csv`",
            "- 法律全文与索引：`wiki/concepts/laws/`",
            "",
            "## 分法律入口",
            "",
        ]
    )
    for slug, link in per_law_index_links.items():
        source_name = next(name for name, config in LAW_CONFIG.items() if config["slug"] == slug)
        raw_path = (RAW_LAWS / source_name).relative_to(KB).as_posix()
        law_rows = [row for row in rows if row["RawPath"] == raw_path]
        law_name = str(law_rows[0]["Law"])
        md_lines.append(f"- [[{link}]] - {law_name}，{len(law_rows)} 条记录")
    md_lines.extend(
        [
            "",
            "## 条款索引",
            "",
            "| 法律 | 条号 | 章节 | 摘要 | Wiki 目标 |",
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
    if apply:
        (INDEX_DIR / "core-laws-article-index.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8", newline="\n")

    print(f"apply={str(apply).lower()}")
    print(f"articles={len(rows)} consolidated_indexes={len(per_law_index_links)} standalone=0")
    print(f"article_links_rewritten={link_count} files={len(link_paths)}")
    print(f"article_pages_to_remove={len(removed)} removed={len(removed) if apply else 0}")
    for path in removed[:20]:
        print(f"article_page: {path.relative_to(KB).as_posix()}")
    if len(removed) > 20:
        print(f"article_page_more={len(removed) - 20}")
    for law, count in counts.items():
        print(f"{law}: {count}")


if __name__ == "__main__":
    main()
