from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
INDEX_DIR = KB / "raw" / "indexes"
WIKI_DIR = KB / "wiki" / "concepts" / "accounting-standards"
MAPPING_CSV = INDEX_DIR / "enterprise-accounting-standards-number-mapping.csv"


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


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def suggest_bucket(row: dict[str, str]) -> tuple[str, str, str]:
    title = row["Title"]
    url = row["Url"]
    source_type = row["SourceTypeLabel"]

    def result(bucket: str, reason: str, confidence: str = "medium") -> tuple[str, str, str]:
        return bucket, reason, confidence

    if source_type == "准则解释":
        m = re.search(r"解释第\s*([0-9０-９]+)号", title)
        if m:
            no = m.group(1).translate(str.maketrans("０１２３４５６７８９", "0123456789"))
            return result(f"解释第{no}号", "标题中明确给出解释编号", "high")
        if "PPP" in title or "PPP" in url:
            return result("解释第14号 / PPP专题", "标题包含 PPP，通常归入收入准则相关专题", "medium")
        return result("待人工核验", "仅有通知标题，未直接给出主题", "low")

    if source_type == "应用案例":
        if "PPP" in title:
            return result("解释第14号 / PPP专题", "PPP 会计处理专题", "medium")
        if "资金集中管理" in title:
            return result("其他规定 / 资金集中管理", "更接近专题性会计处理规定", "medium")
        return result("待人工核验", "标题不够明确", "low")

    if source_type == "实施问答":
        if "增值税" in title:
            return result("其他规定 / 增值税会计处理规定", "明显属于增值税会计处理专题", "high")
        if "租金减让" in title or "欠付租金" in title or "租赁" in title:
            return result("CAS 21 / 租赁", "与租赁准则直接相关", "high")
        if "外币" in title:
            return result("CAS 19 / 外币折算", "与外币折算相关", "high")
        if any(k in title for k in ["金融资产", "金融工具", "贷款", "利率", "结构性存款", "证券化", "永续债", "信用损失"]):
            return result("CAS 22 / 金融工具确认和计量", "金融资产或金融负债专题", "medium")
        if "股份支付" in title or "股权激励" in title:
            return result("CAS 11 / 股份支付", "股权激励类问题", "high")
        if any(k in title for k in ["联营", "合营", "投资方", "合并范围", "子公司", "控制"]):
            if "联营" in title or "合营" in title:
                return result("CAS 20 / 企业合并或 CAS 2 / 长期股权投资", "涉及联营/合营判断", "medium")
            return result("CAS 33 / 合并财务报表", "涉及子公司、控制或合并范围", "medium")
        if "保险" in title:
            return result("CAS 25 / 保险合同", "保险公司或保险合同专题", "high")
        if "现金流量表" in title:
            return result("CAS 31 / 现金流量表", "现金流量表列报问题", "high")
        if "预计负债" in title or "质量保证" in title:
            return result("CAS 13 / 或有事项", "预计负债专题", "medium")
        if "结构化主体" in title:
            return result("CAS 33 / 合并财务报表", "结构化主体控制判断", "medium")
        return result("待人工核验", "标题不够明确", "low")

    if source_type == "其他规定":
        if "增值税" in title:
            return result("其他规定 / 增值税会计处理规定", "增值税专题规定", "high")
        if "租金减让" in title:
            return result("其他规定 / 新冠肺炎疫情相关租金减让会计处理规定", "疫情租金减让专题", "high")
        if "财务报表格式" in title:
            return result("CAS 30 / 财务报表列报", "财务报表列报专题", "medium")
        if "永续债" in title or "新金融工具" in title or "碳排放权" in title or "资产证券化" in title:
            return result("CAS 22 / 金融工具确认和计量", "金融工具或金融资产专题", "medium")
        if "成本核算制度" in title or "专项债券" in title or "破产清算" in title:
            return result("其他规定专题", "更接近财政部专题处理规定", "medium")
        return result("待人工核验", "标题不够明确", "low")

    return result("待人工核验", "未知来源类型", "low")


def build_rows() -> list[dict[str, str]]:
    unmapped = [row for row in read_csv(MAPPING_CSV) if row["StandardKey"] == "unmapped"]
    rows: list[dict[str, str]] = []
    for row in unmapped:
        bucket, reason, confidence = suggest_bucket(row)
        rows.append(
            {
                "SourceType": row["SourceTypeLabel"],
                "Title": row["Title"],
                "Url": row["Url"],
                "LocalPath": row["LocalPath"],
                "SuggestedBucket": bucket,
                "Reason": reason,
                "Confidence": confidence,
            }
        )
    return rows


def write_markdown(rows: list[dict[str, str]]) -> None:
    page = WIKI_DIR / "unmapped-review.md"
    by_type: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_type[row["SourceType"]].append(row)
    counts = Counter(row["SuggestedBucket"] for row in rows)
    lines = [
        "---",
        "title: 企业会计准则未映射资料校准表",
        "type: concept",
        "concept_type: accounting-standard-calibration",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [enterprise-accounting-standards-number-index-2026-06-26]",
        "tags: [accounting, standards, calibration, p1-core]",
        "related: [[concepts/accounting-standards-system]], [[sources/enterprise-accounting-standards-number-index-2026-06-26]]",
        "---",
        "",
        "# 企业会计准则未映射资料校准表",
        "",
        "以下条目是编号索引里暂时没有稳定归位的资料，先按最可能的准则或专题做人工校准建议。",
        "",
        "## 总览",
        "",
        "| 建议桶 | 数量 |",
        "|---|---:|",
    ]
    for bucket, count in counts.most_common():
        lines.append(f"| {bucket} | {count} |")
    for stype in ["准则解释", "应用案例", "实施问答", "其他规定"]:
        group = by_type.get(stype, [])
        if not group:
            continue
        lines.extend(["", f"## {stype}", "", "| 标题 | 建议桶 | 置信度 | 理由 |", "|---|---|---|---|"])
        for row in group:
            lines.append(
                "| {title} | {bucket} | {conf} | {reason} |".format(
                    title=md_escape(row["Title"] or "(空标题)"),
                    bucket=md_escape(row["SuggestedBucket"]),
                    conf=row["Confidence"],
                    reason=md_escape(row["Reason"]),
                )
            )
    page.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = build_rows()
    write_csv(INDEX_DIR / "enterprise-accounting-standards-unmapped-review.csv", rows)
    write_markdown(rows)
    print(f"review_rows={len(rows)}")


if __name__ == "__main__":
    main()
