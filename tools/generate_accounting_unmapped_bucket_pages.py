from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
CSV_PATH = KB / "raw" / "indexes" / "enterprise-accounting-standards-unmapped-review.csv"
OUT_DIR = KB / "wiki" / "concepts" / "accounting-standards" / "calibration"


BUCKET_META: dict[str, tuple[str, str, list[str]]] = {
    "CAS 22 / 金融工具确认和计量": (
        "cas-22-financial-instruments",
        "企业会计准则第22号相关未映射资料",
        ["[[concepts/accounting-standards/cas-22]]"],
    ),
    "CAS 33 / 合并财务报表": (
        "cas-33-consolidated-financial-statements",
        "企业会计准则第33号相关未映射资料",
        ["[[concepts/accounting-standards/cas-33]]"],
    ),
    "CAS 21 / 租赁": (
        "cas-21-leases",
        "企业会计准则第21号相关未映射资料",
        ["[[concepts/accounting-standards/cas-21]]"],
    ),
    "CAS 25 / 保险合同": (
        "cas-25-insurance-contracts",
        "企业会计准则第25号相关未映射资料",
        ["[[concepts/accounting-standards/cas-25]]"],
    ),
    "CAS 30 / 财务报表列报": (
        "cas-30-financial-statement-presentation",
        "企业会计准则第30号相关未映射资料",
        ["[[concepts/accounting-standards/cas-30]]"],
    ),
    "CAS 20 / 企业合并或 CAS 2 / 长期股权投资": (
        "cas-20-cas-02-investments-combinations",
        "企业合并及长期股权投资相关未映射资料",
        ["[[concepts/accounting-standards/cas-20]]", "[[concepts/accounting-standards/cas-02]]"],
    ),
    "CAS 19 / 外币折算": (
        "cas-19-foreign-currency-translation",
        "企业会计准则第19号相关未映射资料",
        ["[[concepts/accounting-standards/cas-19]]"],
    ),
    "CAS 11 / 股份支付": (
        "cas-11-share-based-payment",
        "企业会计准则第11号相关未映射资料",
        ["[[concepts/accounting-standards/cas-11]]"],
    ),
    "CAS 13 / 或有事项": (
        "cas-13-contingencies",
        "企业会计准则第13号相关未映射资料",
        ["[[concepts/accounting-standards/cas-13]]"],
    ),
    "解释第14号 / PPP专题": (
        "interp-14-ppp",
        "企业会计准则解释第14号及 PPP 专题未映射资料",
        ["[[concepts/accounting-standards/interpretations/interp-14]]"],
    ),
    "其他规定 / 增值税会计处理规定": (
        "other-vat-accounting",
        "增值税会计处理相关未映射资料",
        [],
    ),
    "其他规定 / 新冠肺炎疫情相关租金减让会计处理规定": (
        "other-covid-rent-concessions",
        "新冠肺炎疫情相关租金减让会计处理未映射资料",
        ["[[concepts/accounting-standards/cas-21]]"],
    ),
    "其他规定 / 资金集中管理": (
        "other-cash-pooling",
        "资金集中管理相关未映射资料",
        [],
    ),
    "其他规定专题": (
        "other-rules-topic",
        "其他会计处理规定专题未映射资料",
        [],
    ),
    "待人工核验": (
        "pending-manual-review",
        "待人工核验未映射资料",
        [],
    ),
}


def read_rows() -> list[dict[str, str]]:
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def bucket_meta(bucket: str) -> tuple[str, str, list[str]]:
    if bucket in BUCKET_META:
        return BUCKET_META[bucket]
    match = re.fullmatch(r"解释第(\d+)号", bucket)
    if match:
        no = int(match.group(1))
        return (
            f"interp-{no:02d}",
            f"企业会计准则解释第{no}号未映射资料",
            [f"[[concepts/accounting-standards/interpretations/interp-{no:02d}]]"],
        )
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", bucket).strip("-").lower() or "unknown"
    return slug, f"{bucket} 未映射资料", []


def write_bucket_page(bucket: str, rows: list[dict[str, str]]) -> tuple[str, str, int]:
    slug, title, related = bucket_meta(bucket)
    path = OUT_DIR / f"{slug}.md"
    related_links = ["[[concepts/accounting-standards/unmapped-review]]", "[[sources/enterprise-accounting-standards-number-index-2026-06-26]]"]
    related_links.extend(related)
    lines = [
        "---",
        f"title: {title}",
        "type: concept",
        "concept_type: accounting-standard-calibration-bucket",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [enterprise-accounting-standards-number-index-2026-06-26]",
        "tags: [accounting, standards, calibration, p1-core]",
        f"related: {', '.join(related_links)}",
        "---",
        "",
        f"# {title}",
        "",
        "## 定位",
        "",
        f"- 建议桶：{bucket}",
        f"- 资料条目数：{len(rows)}",
        "- 性质：从未稳定映射资料中整理出的人工校准入口；尚不替代正式编号索引。",
        "",
        "## 资料清单",
        "",
        "| 类型 | 标题 | 置信度 | 理由 | 官方链接 | 本地文件 |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {source_type} | {title} | {confidence} | {reason} | {url} | `{local}` |".format(
                source_type=md_escape(row["SourceType"]),
                title=md_escape(row["Title"]),
                confidence=md_escape(row["Confidence"]),
                reason=md_escape(row["Reason"]),
                url=md_escape(row["Url"]),
                local=md_escape(row["LocalPath"]),
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return slug, title, len(rows)


def write_index(page_rows: list[tuple[str, str, int]]) -> None:
    lines = [
        "---",
        "title: 企业会计准则未映射资料校准入口",
        "type: concept",
        "concept_type: accounting-standard-calibration-index",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [enterprise-accounting-standards-number-index-2026-06-26]",
        "tags: [accounting, standards, calibration, p1-core]",
        "related: [[concepts/accounting-standards-system]], [[concepts/accounting-standards/unmapped-review]]",
        "---",
        "",
        "# 企业会计准则未映射资料校准入口",
        "",
        "本入口将 `unmapped-review.md` 中的建议桶拆成独立页面，便于按准则或专题继续人工核验。",
        "",
        "| 专题 | 条目数 | 页面 |",
        "|---|---:|---|",
    ]
    for slug, title, count in sorted(page_rows, key=lambda item: (-item[2], item[1])):
        lines.append(f"| {title} | {count} | [[concepts/accounting-standards/calibration/{slug}]] |")
    (OUT_DIR / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_rows():
        grouped[row["SuggestedBucket"]].append(row)
    page_rows = [write_bucket_page(bucket, rows) for bucket, rows in grouped.items()]
    write_index(page_rows)
    print(f"bucket_pages={len(page_rows)}")


if __name__ == "__main__":
    main()
