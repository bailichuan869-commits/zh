from __future__ import annotations

import csv
import html
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
ACCOUNTING_RAW = KB / "raw" / "standards" / "accounting"
INDEX_DIR = KB / "raw" / "indexes"
WIKI_DIR = KB / "wiki" / "concepts" / "accounting-standards"


CSV_FILES = {
    "standard": ACCOUNTING_RAW / "downloaded-enterprise-accounting-standards.csv",
    "interpretation": ACCOUNTING_RAW / "downloaded-enterprise-accounting-standards-interpretations.csv",
    "application_case": ACCOUNTING_RAW / "downloaded-enterprise-accounting-standards-application-cases.csv",
    "implementation_qa": ACCOUNTING_RAW / "downloaded-enterprise-accounting-standards-implementation-qa-v2.csv",
    "other_rule": ACCOUNTING_RAW / "downloaded-enterprise-accounting-standards-other-rules.csv",
}


TYPE_LABELS = {
    "standard": "准则原文",
    "interpretation": "准则解释",
    "application_case": "应用案例",
    "implementation_qa": "实施问答",
    "other_rule": "其他规定",
}


TOPIC_TO_STANDARD = {
    "存货": 1,
    "长期股权投资": 2,
    "投资性房地产": 3,
    "固定资产": 4,
    "生物资产": 5,
    "无形资产": 6,
    "非货币性资产交换": 7,
    "资产减值": 8,
    "职工薪酬": 9,
    "企业年金基金": 10,
    "股份支付": 11,
    "债务重组": 12,
    "或有事项": 13,
    "收入": 14,
    "建造合同": 15,
    "政府补助": 16,
    "借款费用": 17,
    "所得税": 18,
    "外币折算": 19,
    "企业合并": 20,
    "租赁": 21,
    "金融工具确认和计量": 22,
    "金融资产转移": 23,
    "套期保值": 24,
    "套期会计": 24,
    "保险合同": 25,
    "原保险合同": 25,
    "再保险合同": 26,
    "石油天然气开采": 27,
    "会计政策、会计估计变更和差错更正": 28,
    "资产负债表日后事项": 29,
    "财务报表列报": 30,
    "现金流量表": 31,
    "中期财务报告": 32,
    "合并财务报表": 33,
    "每股收益": 34,
    "分部报告": 35,
    "关联方披露": 36,
    "金融工具列报": 37,
    "首次执行": 38,
    "首次执行企业会计准则": 38,
    "公允价值计量": 39,
    "合营安排": 40,
    "在其他主体中权益的披露": 41,
    "持有待售": 42,
}


CATEGORY_SLUG_TO_STANDARD = {
    "chzzsswd": 1,
    "cqgqtzzzsswd": 2,
    "cwbblbzzsswd": 30,
    "gdzczzsswd": 4,
    "gfzzsswd": 11,
    "gfzfyyal": 11,
    "hbcwbbzzsswd": 33,
    "jkwd": 17,
    "jrgjzzss": 22,
    "jrgjzzyy": 22,
    "kjzckjgjbgzzsswd": 28,
    "qyhbzzsswd": 20,
    "qyhbzzyyal": 20,
    "sczxzzsswd": 38,
    "sdszzyyal": 18,
    "srzzsswd": 14,
    "srzzyy": 14,
    "wbzs": 19,
    "wxzczzsswd": 6,
    "xbxhtsswd": 25,
    "xjllbzzsswd": 31,
    "zcjzzzsswd": 8,
    "zfbzzzsswd": 16,
    "zlzzsswd": 21,
    "zlzzyyal": 21,
    "zwcz": 12,
}


SPECIAL_TOPIC_TO_STANDARD = {
    "预期信用损失": 22,
    "金融负债与权益工具": 37,
    "合同资产": 14,
    "合同负债": 14,
    "合同履约成本": 14,
    "现金折扣": 14,
    "数据资源": 6,
}


STANDARD_RE = re.compile(r"企业会计准则第\s*([0-9０-９]+)\s*号")
INTERPRETATION_RE = re.compile(r"企业会计准则解释第\s*([0-9０-９]+)\s*号")


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


def html_text(local_file: str) -> str:
    if not local_file:
        return ""
    path = Path(local_file)
    if not path.exists():
        return ""
    raw = path.read_text(encoding="utf-8", errors="ignore")
    raw = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", raw)
    raw = re.sub(r"(?is)<[^>]+>", " ", raw)
    return html.unescape(re.sub(r"\s+", " ", raw))


def standard_key(no: int | None) -> str:
    if no is None:
        return "basic"
    return f"cas-{no:02d}"


def standard_page(no: int | None) -> str:
    return f"concepts/accounting-standards/{standard_key(no)}"


def extract_standard_numbers(text: str) -> set[int]:
    normalized = fullwidth_to_ascii(text)
    return {int(match.group(1)) for match in STANDARD_RE.finditer(normalized)}


def extract_interpretation_numbers(text: str) -> set[int]:
    normalized = fullwidth_to_ascii(text)
    return {int(match.group(1)) for match in INTERPRETATION_RE.finditer(normalized)}


def slug_matches(url: str) -> set[int]:
    found: set[int] = set()
    for slug, no in CATEGORY_SLUG_TO_STANDARD.items():
        if f"/{slug}/" in url:
            found.add(no)
    return found


def topic_matches(text: str) -> set[int]:
    found: set[int] = set()
    for topic, no in TOPIC_TO_STANDARD.items():
        if topic in text:
            found.add(no)
    for topic, no in SPECIAL_TOPIC_TO_STANDARD.items():
        if topic in text:
            found.add(no)
    return found


def choose_mapping(source_type: str, title: str, url: str, local_file: str) -> tuple[set[int], str, str]:
    title_text = fullwidth_to_ascii(title)
    direct = extract_standard_numbers(title_text)
    if direct:
        return direct, "title-standard-number", "high"

    by_slug = slug_matches(url)
    if by_slug:
        return by_slug, "url-category-slug", "high"

    if source_type == "interpretation":
        body_numbers = extract_standard_numbers(html_text(local_file))
        if body_numbers:
            return body_numbers, "html-standard-number", "medium"

    by_topic = topic_matches(title_text)
    if by_topic:
        return by_topic, "title-topic-keyword", "medium"

    return set(), "unmapped", "low"


def make_record(source_type: str, source_row: dict[str, str]) -> dict[str, str]:
    return {
        "SourceType": source_type,
        "SourceTypeLabel": TYPE_LABELS[source_type],
        "Title": source_row.get("Title", ""),
        "Url": source_row.get("Url", ""),
        "LocalPath": rel(source_row.get("LocalFile", "")),
        "Seq": source_row.get("Seq", ""),
    }


def load_standard_records() -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    all_rows: list[dict[str, str]] = []
    standards: dict[str, dict[str, str]] = {}
    seen_source_keys: set[tuple[str, str]] = set()

    for source_type, csv_path in CSV_FILES.items():
        for row in read_csv(csv_path):
            base = make_record(source_type, row)
            dedupe_key = (source_type, base["Url"] or base["Title"])
            if dedupe_key in seen_source_keys:
                continue
            seen_source_keys.add(dedupe_key)

            title = base["Title"]
            url = base["Url"]
            local_path = str(KB / base["LocalPath"]) if base["LocalPath"] else ""

            if source_type == "standard" and "基本准则" in title:
                mapped = {None}
                method = "basic-standard-title"
                confidence = "high"
            else:
                mapped, method, confidence = choose_mapping(source_type, title, url, local_path)

            interpretation_numbers = sorted(extract_interpretation_numbers(title))
            if not interpretation_numbers and source_type == "interpretation":
                interpretation_numbers = sorted(extract_interpretation_numbers(html_text(local_path)))

            if not mapped:
                all_rows.append(
                    {
                        **base,
                        "StandardNo": "",
                        "StandardKey": "unmapped",
                        "StandardPage": "",
                        "MappingMethod": method,
                        "Confidence": confidence,
                        "InterpretationNo": ";".join(str(no) for no in interpretation_numbers),
                    }
                )
                continue

            for standard_no in sorted(mapped, key=lambda value: -1 if value is None else value):
                key = standard_key(standard_no)
                record = {
                    **base,
                    "StandardNo": "" if standard_no is None else str(standard_no),
                    "StandardKey": key,
                    "StandardPage": standard_page(standard_no),
                    "MappingMethod": method,
                    "Confidence": confidence,
                    "InterpretationNo": ";".join(str(no) for no in interpretation_numbers),
                }
                all_rows.append(record)
                if source_type == "standard":
                    existing = standards.get(key)
                    if existing is None or "（财会〔2017〕" in title or "（财会〔2020〕" in title:
                        standards[key] = record

    return all_rows, standards


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


def article_id(url: str) -> str:
    match = re.search(r"/(t\d+_\d+)\.htm", url)
    if match:
        return match.group(1)
    return url


def row_preference(row: dict[str, str]) -> tuple[int, int, int]:
    method_score = {
        "url-category-slug": 4,
        "title-standard-number": 3,
        "html-standard-number": 2,
        "title-topic-keyword": 1,
        "unmapped": 0,
    }.get(row["MappingMethod"], 0)
    confidence_score = {"high": 2, "medium": 1, "low": 0}.get(row["Confidence"], 0)
    category_score = 1 if slug_matches(row["Url"]) else 0
    return method_score, confidence_score, category_score


def dedupe_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    best: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        key = (row["SourceType"], row["StandardKey"], article_id(row["Url"]) or row["Title"])
        current = best.get(key)
        if current is None or row_preference(row) > row_preference(current):
            best[key] = row
    return list(best.values())


def write_standard_page(key: str, rows: list[dict[str, str]], standard_record: dict[str, str] | None) -> None:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    title = "企业会计准则——基本准则" if key == "basic" else f"企业会计准则第{int(rows[0]['StandardNo'])}号"
    if standard_record and standard_record["Title"]:
        title = standard_record["Title"]
    page = WIKI_DIR / f"{key}.md"
    standard_no = rows[0]["StandardNo"]
    counts = Counter(row["SourceTypeLabel"] for row in rows)
    lines = [
        "---",
        f"title: {title}",
        "type: concept",
        "concept_type: accounting-standard",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [enterprise-accounting-standards-number-index-2026-06-26]",
        "tags: [accounting, standards, cas, p1-core]",
        "related: [[concepts/accounting-standards-system]], [[sources/enterprise-accounting-standards-number-index-2026-06-26]]",
        "---",
        "",
        f"# {title}",
        "",
        "## 定位",
        "",
        f"- 准则编号：{standard_no or '基本准则'}",
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

    if standard_record:
        lines.extend(
            [
                "",
                "## 准则原文",
                "",
                f"- 标题：{standard_record['Title']}",
                f"- 官方链接：{standard_record['Url']}",
                f"- 本地文件：`{standard_record['LocalPath']}`",
            ]
        )

    lines.extend(["", "## 关联资料", "", "| 类型 | 标题 | 官方链接 | 本地文件 | 映射 |", "|---|---|---|---|---|"])
    for row in rows:
        lines.append(
            "| {type} | {title} | {url} | `{local}` | {method}/{confidence} |".format(
                type=md_escape(row["SourceTypeLabel"]),
                title=md_escape(row["Title"]),
                url=row["Url"],
                local=md_escape(row["LocalPath"]),
                method=row["MappingMethod"],
                confidence=row["Confidence"],
            )
        )
    page.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_unmapped_page(rows: list[dict[str, str]]) -> None:
    page = WIKI_DIR / "unmapped.md"
    lines = [
        "---",
        "title: 企业会计准则未映射资料",
        "type: concept",
        "concept_type: accounting-standard-unmapped",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [enterprise-accounting-standards-number-index-2026-06-26]",
        "tags: [accounting, standards, unmapped, p1-core]",
        "related: [[concepts/accounting-standards-system]], [[sources/enterprise-accounting-standards-number-index-2026-06-26]]",
        "---",
        "",
        "# 企业会计准则未映射资料",
        "",
        "下列资料未能通过准则编号、专题栏目或标题关键词保守映射到具体企业会计准则编号，后续需要人工核验。",
        "",
        "| 类型 | 标题 | 官方链接 | 本地文件 |",
        "|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {md_escape(row['SourceTypeLabel'])} | {md_escape(row['Title'])} | {row['Url']} | `{md_escape(row['LocalPath'])}` |"
        )
    page.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_markdown_index(mapped_rows: list[dict[str, str]], standard_rows: dict[str, dict[str, str]]) -> None:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    unmapped: list[dict[str, str]] = []
    for row in mapped_rows:
        if row["StandardKey"] == "unmapped":
            unmapped.append(row)
        else:
            grouped[row["StandardKey"]].append(row)

    for key, rows in grouped.items():
        write_standard_page(key, rows, standard_rows.get(key))
    write_unmapped_page(unmapped)

    index_path = INDEX_DIR / "enterprise-accounting-standards-number-index.md"
    csv_path = "raw/indexes/enterprise-accounting-standards-number-index.csv"
    detail_csv_path = "raw/indexes/enterprise-accounting-standards-number-mapping.csv"

    lines = [
        "# 企业会计准则编号级索引",
        "",
        "生成日期：2026-06-26",
        "",
        "## 文件",
        "",
        f"- 编号汇总 CSV：`{csv_path}`",
        f"- 映射明细 CSV：`{detail_csv_path}`",
        "- 分准则 wiki 页：`wiki/concepts/accounting-standards/`",
        "",
        "## 汇总",
        "",
        "| 准则 | 准则页 | 准则原文 | 解释 | 应用案例 | 实施问答 | 其他规定 | 合计 |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    summary_rows: list[dict[str, str]] = []
    for key in sorted(grouped, key=lambda item: -1 if item == "basic" else int(item.split("-")[1])):
        rows = grouped[key]
        counts = Counter(row["SourceType"] for row in rows)
        standard_no = "" if key == "basic" else key.split("-")[1].lstrip("0")
        title = "企业会计准则——基本准则"
        if standard_rows.get(key):
            title = standard_rows[key]["Title"]
        page = standard_page(None if key == "basic" else int(standard_no))
        summary = {
            "StandardNo": standard_no,
            "StandardKey": key,
            "Title": title,
            "WikiPage": page,
            "StandardCount": str(counts["standard"]),
            "InterpretationCount": str(counts["interpretation"]),
            "ApplicationCaseCount": str(counts["application_case"]),
            "ImplementationQaCount": str(counts["implementation_qa"]),
            "OtherRuleCount": str(counts["other_rule"]),
            "TotalMappedRecords": str(len(rows)),
        }
        summary_rows.append(summary)
        lines.append(
            "| {title} | [[{page}]] | {standard} | {interpretation} | {case} | {qa} | {other} | {total} |".format(
                title=md_escape(title),
                page=page,
                standard=counts["standard"],
                interpretation=counts["interpretation"],
                case=counts["application_case"],
                qa=counts["implementation_qa"],
                other=counts["other_rule"],
                total=len(rows),
            )
        )
    lines.extend(
        [
            "| 未映射资料 | [[concepts/accounting-standards/unmapped]] | {standard} | {interpretation} | {case} | {qa} | {other} | {total} |".format(
                standard=sum(1 for row in unmapped if row["SourceType"] == "standard"),
                interpretation=sum(1 for row in unmapped if row["SourceType"] == "interpretation"),
                case=sum(1 for row in unmapped if row["SourceType"] == "application_case"),
                qa=sum(1 for row in unmapped if row["SourceType"] == "implementation_qa"),
                other=sum(1 for row in unmapped if row["SourceType"] == "other_rule"),
                total=len(unmapped),
            ),
            "",
            "## 映射说明",
            "",
            "- `title-standard-number`：标题中明确出现《企业会计准则第N号》。",
            "- `url-category-slug`：财政部专题栏目 URL 可直接对应准则主题。",
            "- `html-standard-number`：解释类文件正文中出现准则编号。",
            "- `title-topic-keyword`：标题关键词可保守对应准则主题。",
            "- `unmapped`：暂不强行归类，留待人工核验。",
        ]
    )
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_csv(INDEX_DIR / "enterprise-accounting-standards-number-index.csv", summary_rows)


def main() -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    mapped_rows, standards = load_standard_records()
    mapped_rows = dedupe_rows(mapped_rows)
    write_csv(INDEX_DIR / "enterprise-accounting-standards-number-mapping.csv", mapped_rows)
    write_markdown_index(mapped_rows, standards)

    total = len(mapped_rows)
    unmapped = sum(1 for row in mapped_rows if row["StandardKey"] == "unmapped")
    pages = len([path for path in WIKI_DIR.glob("*.md")])
    print(f"mapped_records={total - unmapped} unmapped={unmapped} total_rows={total} pages={pages}")


if __name__ == "__main__":
    main()
