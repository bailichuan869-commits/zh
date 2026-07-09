from __future__ import annotations

import csv
import html
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
AUDIT_RAW = KB / "raw" / "standards" / "audit"
INDEX_DIR = KB / "raw" / "indexes"
WIKI_DIR = KB / "wiki" / "concepts" / "audit-standards"

DIRECT_PDFS = AUDIT_RAW / "downloaded-cicpa-professional-standards-pdfs.csv"
TOPIC_ITEMS = AUDIT_RAW / "cicpa-professional-standards-topic-items.csv"
GUIDELINES_34_HTML = AUDIT_RAW / "cicpa-guidelines-34-20230410.html"
ZIP_DIR = AUDIT_RAW / "archives" / "2023-23-audit-standards"


TYPE_LABELS = {
    "standard": "准则原文",
    "guideline": "应用指南",
    "topic_entry": "专题条目",
    "archive_pdf": "ZIP解压准则",
}


NOTICE_URLS = {
    "2022-鉴证业务基本准则等15项应用指南": "https://www.cicpa.org.cn/xxfb/tzgg/202201/t20220120_63335.html",
    "2022-鉴证业务基本准则等11项准则": "https://www.cicpa.org.cn/xxfb/tzgg/202201/t20220120_63336.html",
    "2023-重大错报风险识别和评估等准则": "https://www.cicpa.org.cn/xxfb/tzgg/202301/t20230103_63902.html",
    "2023-34项审计准则应用指南": "https://www.cicpa.org.cn/xxfb/tzgg/202304/t20230410_64066.html",
}


STANDARD_RE = re.compile(
    r"中国注册会计师(?P<family>审计准则|审阅准则|其他鉴证业务准则|相关服务准则|鉴证业务准则|质量管理准则|独立性准则|职业道德守则|可持续信息鉴证业务准则)"
    r"第\s*(?P<number>[0-9０-９Xx]+)\s*号(?:[—\-－]+(?P<name>[^》\)\]（(]*))?"
)


def fullwidth_to_ascii(text: str) -> str:
    return text.translate(str.maketrans("０１２３４５６７８９", "0123456789"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def rel(path_text: str) -> str:
    if not path_text:
        return ""
    path = Path(path_text)
    try:
        return path.relative_to(KB).as_posix()
    except ValueError:
        return path.as_posix()


def clean_text(text: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"^[0-9０-９]+[\.．、]?", "", text)
    return text.strip()


def strip_title(title: str) -> str:
    title = clean_text(title)
    title = title.replace("》《", "》 《")
    return title


def parse_standard(title: str) -> tuple[str, str, str]:
    text = fullwidth_to_ascii(strip_title(title))
    if "中国注册会计师鉴证业务基本准则" in text and "第" not in text:
        return "assurance-basic", "鉴证业务基本准则", "中国注册会计师鉴证业务基本准则"
    match = STANDARD_RE.search(text)
    if not match:
        return "", "", ""
    family = match.group("family")
    number = match.group("number").upper()
    name = (match.group("name") or "").strip()
    if "应用指南" in name:
        name = name.replace("应用指南", "")
    key_prefix = {
        "审计准则": "csa",
        "审阅准则": "crs",
        "其他鉴证业务准则": "coa",
        "相关服务准则": "crs-svc",
        "鉴证业务准则": "cabs",
        "质量管理准则": "cqms",
        "独立性准则": "independence",
        "职业道德守则": "ethics",
        "可持续信息鉴证业务准则": "sustainability-assurance",
    }.get(family, "standard")
    key = f"{key_prefix}-{number.lower()}"
    title_base = f"中国注册会计师{family}第{number}号"
    if name:
        title_base += f"——{name}"
    return key, family, title_base


def infer_source_type(title: str, group: str, local_path: str) -> str:
    text = f"{title} {group} {local_path}"
    if "应用指南" in text:
        return "guideline"
    if "ZIP" in group or "2023-23" in local_path:
        return "archive_pdf"
    return "standard"


def parse_guidelines_34_titles() -> dict[str, str]:
    if not GUIDELINES_34_HTML.exists():
        return {}
    raw = GUIDELINES_34_HTML.read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(r'<a\s+[^>]*href="\./(?P<file>W[^"]+\.pdf)"[^>]*>(?P<label>.*?)</a>', re.I | re.S)
    title_by_file: dict[str, str] = {}
    for match in pattern.finditer(raw):
        file_name = match.group("file")
        label = clean_text(match.group("label"))
        if not label:
            continue
        existing = title_by_file.get(file_name, "")
        if "准则第" in label or "鉴证业务基本准则" in label:
            title_by_file[file_name] = label
        elif not existing:
            title_by_file[file_name] = label
    return title_by_file


def pdf_article_id(url: str) -> str:
    match = re.search(r"/([^/]+\.pdf)$", url, re.I)
    return match.group(1) if match else url


def make_record(
    source_type: str,
    title: str,
    group: str,
    url: str,
    local_path: str,
    status: str = "",
    source_note: str = "",
) -> dict[str, str]:
    key, family, standard_title = parse_standard(title)
    return {
        "StandardKey": key or "unmapped",
        "StandardFamily": family,
        "StandardTitle": standard_title,
        "SourceType": source_type,
        "SourceTypeLabel": TYPE_LABELS[source_type],
        "Title": strip_title(title),
        "Group": group,
        "Url": url,
        "LocalPath": rel(local_path),
        "Status": status,
        "SourceNote": source_note,
        "MappingMethod": "title-standard-number" if key else "unmapped",
        "Confidence": "high" if key else "low",
    }


def load_direct_pdf_records() -> list[dict[str, str]]:
    rows = []
    title_by_pdf = parse_guidelines_34_titles()
    for row in read_csv(DIRECT_PDFS):
        title = row.get("Title", "")
        url = row.get("Url", "")
        pdf_name = pdf_article_id(url)
        title_is_only_seq = bool(re.fullmatch(r"\s*[0-9０-９]+[\.．]?\s*", title or ""))
        if pdf_name in title_by_pdf and (title_is_only_seq or not parse_standard(title)[0]):
            title = title_by_pdf[pdf_name]
        group = row.get("Group", "")
        local_path = row.get("LocalFile", "")
        source_type = infer_source_type(title, group, local_path)
        rows.append(
            make_record(
                source_type=source_type,
                title=title,
                group=group,
                url=url,
                local_path=local_path,
                status=row.get("Status", ""),
                source_note="direct-pdf-csv",
            )
        )
    return rows


def load_archive_pdf_records() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not ZIP_DIR.exists():
        return rows
    for path in sorted(ZIP_DIR.rglob("*.pdf")):
        title = path.stem
        if "." in title:
            title = title.split(".", 1)[1]
        title = re.sub(r"（?2022年12月22日修订）?", "", title)
        rows.append(
            make_record(
                source_type="archive_pdf",
                title=title,
                group="2023-23项审计准则ZIP解压",
                url=NOTICE_URLS["2023-重大错报风险识别和评估等准则"],
                local_path=str(path),
                status="ok",
                source_note="zip-extracted-pdf",
            )
        )
    return rows


def load_topic_records() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    if not TOPIC_ITEMS.exists():
        return records
    for row in read_csv(TOPIC_ITEMS):
        title = row.get("Title", "")
        key, _, _ = parse_standard(title)
        if not key:
            continue
        records.append(
            make_record(
                source_type="topic_entry",
                title=title,
                group="中注协执业准则专题条目",
                url=row.get("Url", ""),
                local_path="",
                status=row.get("Date", ""),
                source_note="topic-entry",
            )
        )
    return records


def row_preference(row: dict[str, str]) -> tuple[int, int]:
    type_score = {"standard": 4, "archive_pdf": 3, "guideline": 2, "topic_entry": 1}.get(row["SourceType"], 0)
    path_score = 1 if row["LocalPath"] else 0
    return type_score, path_score


def dedupe_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    best: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        if row["StandardKey"] == "unmapped":
            key = (row["SourceType"], row["StandardKey"], row["Title"] or row["LocalPath"])
        else:
            key = (row["SourceType"], row["StandardKey"], pdf_article_id(row["Url"]) or row["Title"])
        current = best.get(key)
        if current is None or row_preference(row) > row_preference(current):
            best[key] = row
    return list(best.values())


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def write_csv(path: Path, rows: Iterable[dict[str, str]]) -> None:
    rows = list(rows)
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_standard_page(key: str, rows: list[dict[str, str]]) -> None:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    page = WIKI_DIR / f"{key}.md"
    title = next((row["StandardTitle"] for row in rows if row["StandardTitle"]), key)
    family = next((row["StandardFamily"] for row in rows if row["StandardFamily"]), "")
    counts = Counter(row["SourceTypeLabel"] for row in rows)
    lines = [
        "---",
        f"title: {title}",
        "type: concept",
        "concept_type: audit-standard",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [cicpa-professional-standards-number-index-2026-06-26]",
        "tags: [audit, standards, cicpa, p1-core]",
        "related: [[concepts/audit-standards-system]], [[sources/cicpa-professional-standards-number-index-2026-06-26]]",
        "---",
        "",
        f"# {title}",
        "",
        "## 定位",
        "",
        f"- 准则类型：{family or '未识别'}",
        f"- 索引键：`{key}`",
        f"- 资料记录数：{len(rows)}",
        "",
        "## 资料分布",
        "",
        "| 类型 | 数量 |",
        "|---|---:|",
    ]
    for label, count in sorted(counts.items()):
        lines.append(f"| {label} | {count} |")
    lines.extend(["", "## 关联资料", "", "| 类型 | 标题 | 来源分组 | 官方链接 | 本地文件 |", "|---|---|---|---|---|"])
    for row in rows:
        lines.append(
            "| {type} | {title} | {group} | {url} | `{local}` |".format(
                type=md_escape(row["SourceTypeLabel"]),
                title=md_escape(row["Title"]),
                group=md_escape(row["Group"]),
                url=row["Url"],
                local=md_escape(row["LocalPath"]),
            )
        )
    page.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_unmapped_page(rows: list[dict[str, str]]) -> None:
    page = WIKI_DIR / "unmapped.md"
    lines = [
        "---",
        "title: 中国注册会计师执业准则未映射资料",
        "type: concept",
        "concept_type: audit-standard-unmapped",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [cicpa-professional-standards-number-index-2026-06-26]",
        "tags: [audit, standards, cicpa, unmapped, p1-core]",
        "related: [[concepts/audit-standards-system]], [[sources/cicpa-professional-standards-number-index-2026-06-26]]",
        "---",
        "",
        "# 中国注册会计师执业准则未映射资料",
        "",
        "下列资料暂未能稳定解析到具体准则编号，后续需要人工核验。",
        "",
        "| 类型 | 标题 | 来源分组 | 官方链接 | 本地文件 |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {type} | {title} | {group} | {url} | `{local}` |".format(
                type=md_escape(row["SourceTypeLabel"]),
                title=md_escape(row["Title"]),
                group=md_escape(row["Group"]),
                url=row["Url"],
                local=md_escape(row["LocalPath"]),
            )
        )
    page.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_markdown_index(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    unmapped: list[dict[str, str]] = []
    for row in rows:
        if row["StandardKey"] == "unmapped":
            unmapped.append(row)
        else:
            grouped[row["StandardKey"]].append(row)

    for key, group_rows in grouped.items():
        write_standard_page(key, group_rows)
    write_unmapped_page(unmapped)

    summary_rows: list[dict[str, str]] = []
    for key in sorted(grouped):
        group_rows = grouped[key]
        counts = Counter(row["SourceType"] for row in group_rows)
        title = next((row["StandardTitle"] for row in group_rows if row["StandardTitle"]), key)
        family = next((row["StandardFamily"] for row in group_rows if row["StandardFamily"]), "")
        summary_rows.append(
            {
                "StandardKey": key,
                "StandardFamily": family,
                "StandardTitle": title,
                "WikiPage": f"concepts/audit-standards/{key}",
                "StandardCount": str(counts["standard"] + counts["archive_pdf"]),
                "GuidelineCount": str(counts["guideline"]),
                "TopicEntryCount": str(counts["topic_entry"]),
                "TotalMappedRecords": str(len(group_rows)),
            }
        )

    index_lines = [
        "# 中国注册会计师执业准则编号级索引",
        "",
        "生成日期：2026-06-26",
        "",
        "## 文件",
        "",
        "- 编号汇总 CSV：`raw/indexes/cicpa-professional-standards-number-index.csv`",
        "- 映射明细 CSV：`raw/indexes/cicpa-professional-standards-number-mapping.csv`",
        "- 分准则 wiki 页：`wiki/concepts/audit-standards/`",
        "",
        "## 汇总",
        "",
        "| 准则 | 准则类型 | 准则原文/ZIP | 应用指南 | 专题条目 | 合计 | 页面 |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in summary_rows:
        index_lines.append(
            "| {title} | {family} | {standard} | {guide} | {topic} | {total} | [[{page}]] |".format(
                title=md_escape(row["StandardTitle"]),
                family=md_escape(row["StandardFamily"]),
                standard=row["StandardCount"],
                guide=row["GuidelineCount"],
                topic=row["TopicEntryCount"],
                total=row["TotalMappedRecords"],
                page=row["WikiPage"],
            )
        )
    index_lines.extend(
        [
            f"| 未映射资料 |  |  |  |  | {len(unmapped)} | [[concepts/audit-standards/unmapped]] |",
            "",
            "## 映射说明",
            "",
            "- 直接 PDF 清单优先采用 CSV 标题；如 2023 年 34 项应用指南附件标题仅为序号，则从通知 HTML 的附件链接补全标题。",
            "- ZIP 解压 PDF 依据文件名解析准则编号和标题。",
            "- 专题条目仅在标题中能稳定识别准则编号时纳入对应准则页。",
            "- 无法稳定解析准则编号的资料保留在未映射页。",
        ]
    )
    (INDEX_DIR / "cicpa-professional-standards-number-index.md").write_text(
        "\n".join(index_lines) + "\n", encoding="utf-8"
    )
    return summary_rows


def main() -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_direct_pdf_records() + load_archive_pdf_records() + load_topic_records()
    rows = dedupe_rows(rows)
    write_csv(INDEX_DIR / "cicpa-professional-standards-number-mapping.csv", rows)
    summary_rows = write_markdown_index(rows)
    write_csv(INDEX_DIR / "cicpa-professional-standards-number-index.csv", summary_rows)
    mapped = sum(1 for row in rows if row["StandardKey"] != "unmapped")
    unmapped = len(rows) - mapped
    print(f"standards={len(summary_rows)} mapped_records={mapped} unmapped={unmapped} total_rows={len(rows)}")


if __name__ == "__main__":
    main()
