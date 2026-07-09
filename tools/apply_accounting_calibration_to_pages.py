from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
WIKI = KB / "wiki"
ACCOUNTING_DIR = WIKI / "concepts" / "accounting-standards"
OTHER_RULES_DIR = ACCOUNTING_DIR / "other-rules"
CSV_PATH = KB / "raw" / "indexes" / "enterprise-accounting-standards-unmapped-review.csv"

START = "<!-- calibration-supplement:start -->"
END = "<!-- calibration-supplement:end -->"


TARGETS: dict[str, list[Path]] = {
    "CAS 22 / 金融工具确认和计量": [ACCOUNTING_DIR / "cas-22.md"],
    "CAS 33 / 合并财务报表": [ACCOUNTING_DIR / "cas-33.md"],
    "CAS 21 / 租赁": [ACCOUNTING_DIR / "cas-21.md"],
    "CAS 25 / 保险合同": [ACCOUNTING_DIR / "cas-25.md"],
    "CAS 30 / 财务报表列报": [ACCOUNTING_DIR / "cas-30.md"],
    "CAS 20 / 企业合并或 CAS 2 / 长期股权投资": [
        ACCOUNTING_DIR / "cas-20.md",
        ACCOUNTING_DIR / "cas-02.md",
    ],
    "CAS 19 / 外币折算": [ACCOUNTING_DIR / "cas-19.md"],
    "CAS 11 / 股份支付": [ACCOUNTING_DIR / "cas-11.md"],
    "CAS 13 / 或有事项": [ACCOUNTING_DIR / "cas-13.md"],
    "解释第14号 / PPP专题": [
        ACCOUNTING_DIR / "interpretations" / "interp-14.md",
        ACCOUNTING_DIR / "cas-14.md",
    ],
    "其他规定 / 增值税会计处理规定": [OTHER_RULES_DIR / "vat-accounting.md"],
    "其他规定 / 新冠肺炎疫情相关租金减让会计处理规定": [
        OTHER_RULES_DIR / "covid-rent-concessions.md",
        ACCOUNTING_DIR / "cas-21.md",
    ],
    "其他规定 / 资金集中管理": [OTHER_RULES_DIR / "cash-pooling.md"],
    "其他规定专题": [OTHER_RULES_DIR / "topic-rules.md"],
}


OTHER_RULE_PAGES: dict[Path, tuple[str, str]] = {
    OTHER_RULES_DIR / "vat-accounting.md": (
        "增值税会计处理规定",
        "汇集财政部增值税会计处理规定及相关实施问答。",
    ),
    OTHER_RULES_DIR / "covid-rent-concessions.md": (
        "新冠肺炎疫情相关租金减让会计处理规定",
        "汇集疫情相关租金减让会计处理规定及相关问答。",
    ),
    OTHER_RULES_DIR / "cash-pooling.md": (
        "资金集中管理会计处理",
        "汇集资金集中管理相关应用案例和后续核验线索。",
    ),
    OTHER_RULES_DIR / "topic-rules.md": (
        "其他专题性会计处理规定",
        "汇集暂不宜直接归入单一准则编号的专题性会计处理规定。",
    ),
}


def read_rows() -> list[dict[str, str]]:
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def wiki_link_for(path: Path) -> str:
    rel = path.relative_to(WIKI).with_suffix("").as_posix()
    return f"[[{rel}]]"


def ensure_other_rule_page(path: Path) -> None:
    if path.exists():
        return
    title, description = OTHER_RULE_PAGES[path]
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        f"title: {title}",
        "type: concept",
        "concept_type: accounting-other-rule",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [enterprise-accounting-standards-number-index-2026-06-26]",
        "tags: [accounting, standards, other-rules, calibration, p1-core]",
        "related: [[concepts/accounting-standards-system]], [[concepts/accounting-standards/calibration/index]]",
        "---",
        "",
        f"# {title}",
        "",
        "## 定位",
        "",
        description,
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def supplement_block(rows: list[dict[str, str]], bucket: str) -> str:
    lines = [
        START,
        "",
        "## 校准补充资料",
        "",
        f"以下资料来自 [[concepts/accounting-standards/unmapped-review]] 的人工校准建议，建议桶为“{bucket}”。",
        "这些条目保留原始官方链接和本地 HTML 路径，后续应结合原文继续核验后再纳入正式映射。",
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
    lines.extend(["", END, ""])
    return "\n".join(lines)


def upsert_supplement(path: Path, rows: list[dict[str, str]], bucket: str) -> None:
    if path in OTHER_RULE_PAGES:
        ensure_other_rule_page(path)
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    block = supplement_block(rows, bucket)
    pattern = re.compile(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", re.S)
    if pattern.search(text):
        text = pattern.sub("\n\n" + block, text).rstrip() + "\n"
    else:
        text = text.rstrip() + "\n\n" + block
    path.write_text(text, encoding="utf-8")


def write_other_rules_index() -> None:
    OTHER_RULES_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        "title: 企业会计准则其他规定入口",
        "type: concept",
        "concept_type: accounting-other-rules-index",
        "created: 2026-06-26",
        "updated: 2026-06-26",
        "sources: [enterprise-accounting-standards-number-index-2026-06-26]",
        "tags: [accounting, standards, other-rules, p1-core]",
        "related: [[concepts/accounting-standards-system]], [[concepts/accounting-standards/calibration/index]]",
        "---",
        "",
        "# 企业会计准则其他规定入口",
        "",
        "本入口汇集暂不宜直接归入单一准则编号、但已从校准表中形成专题入口的财政部会计处理规定。",
        "",
        "| 专题 | 页面 |",
        "|---|---|",
    ]
    for path, (title, _description) in OTHER_RULE_PAGES.items():
        lines.append(f"| {title} | {wiki_link_for(path)} |")
    (OTHER_RULES_DIR / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows_by_bucket: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_rows():
        rows_by_bucket[row["SuggestedBucket"]].append(row)

    written: set[Path] = set()
    for bucket, paths in TARGETS.items():
        rows = rows_by_bucket.get(bucket, [])
        if not rows:
            continue
        for path in paths:
            upsert_supplement(path, rows, bucket)
            written.add(path)

    for bucket, rows in rows_by_bucket.items():
        match = re.fullmatch(r"解释第(\d+)号", bucket)
        if not match:
            continue
        path = ACCOUNTING_DIR / "interpretations" / f"interp-{int(match.group(1)):02d}.md"
        upsert_supplement(path, rows, bucket)
        written.add(path)

    write_other_rules_index()
    print(f"updated_pages={len(written)}")


if __name__ == "__main__":
    main()
