from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

from kb_common import update_frontmatter


ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge-base" / "CPA-ZH"
WIKI = KB / "wiki"
ACCOUNTING_DIR = WIKI / "concepts" / "accounting-standards"
OTHER_RULES_DIR = ACCOUNTING_DIR / "other-rules"
CSV_PATH = KB / "raw" / "indexes" / "enterprise-accounting-standards-unmapped-review.csv"

START = "<!-- calibration-supplement:start -->"
END = "<!-- calibration-supplement:end -->"
COVID_BOUNDARY_START = "<!-- covid-rent-concessions-boundary:start -->"
COVID_BOUNDARY_END = "<!-- covid-rent-concessions-boundary:end -->"


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
        "汇集疫情相关租金减让会计处理规定及相关问答，仅用于历史期间追溯。",
    ),
    OTHER_RULES_DIR / "cash-pooling.md": (
        "资金集中管理会计处理",
        "依据财政部资金集中管理会计处理应用案例，整理业务结构、账务连接、减值和列报核查入口。",
    ),
    OTHER_RULES_DIR / "topic-rules.md": (
        "其他专题性会计处理规定",
        "汇集暂不宜直接归入单一准则编号的专题性会计处理规定。",
    ),
}

OTHER_RULE_GOVERNANCE: dict[Path, dict[str, object]] = {
    OTHER_RULES_DIR / "cash-pooling.md": {
        "page_role": "knowledge",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "asset_id": "cpa-zh:accounting-other-rule:cash-pooling",
        "source_id": "enterprise-accounting-standards-application-cases-download-2026-06-26",
        "knowledge_type": "accounting-application-case",
        "source_type": "official-application-case",
        "version": "application-case-2022-01-24",
        "published_on": "2022-01-24",
        "effective_from": "unknown",
        "lifecycle_status": "unknown",
        "authority_level": "official",
        "raw_path": "raw/standards/accounting/application-cases-pages/023-资金集中管理会计处理应用案例.html.md",
        "source_url": "https://kjs.mof.gov.cn/zt/kjzzss/srzzzq/jrgjzzyy/202201/t20220124_3784577.htm",
    },
    OTHER_RULES_DIR / "covid-rent-concessions.md": {
        "page_role": "knowledge",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "asset_id": "cpa-zh:accounting-other-rule:covid-rent-concessions",
        "source_id": "enterprise-accounting-standards-other-rules-download-2026-06-26",
        "knowledge_type": "accounting-other-rule",
        "source_type": "official-rule",
        "version": "caihui-2020-10",
        "published_on": "2020-06-19",
        "effective_from": "2020-06-19",
        "lifecycle_status": "historical",
        "authority_level": "official",
        "raw_path": "raw/standards/accounting/other-rules-pages/018-关于印发-新冠肺炎疫情相关租金减让会计处理规定-的通知.html.md",
        "source_url": "https://kjs.mof.gov.cn/zhengcefabu/202006/t20200624_3538070.htm",
    },
    OTHER_RULES_DIR / "vat-accounting.md": {
        "page_role": "knowledge",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "asset_id": "cpa-zh:accounting-other-rule:vat-accounting",
        "source_id": "enterprise-accounting-standards-other-rules-download-2026-06-26",
        "knowledge_type": "accounting-other-rule",
        "source_type": "official-rule",
        "version": "caihui-2016-22",
        "published_on": "2016-12-03",
        "effective_from": "2016-12-03",
        "lifecycle_status": "unknown",
        "authority_level": "official",
        "raw_path": "raw/standards/accounting/other-rules-pages/009-关于印发-增值税会计处理规定-的通知.html.md",
        "source_url": "https://kjs.mof.gov.cn/zhengcefabu/201612/t20161212_2479869.htm",
    },
    OTHER_RULES_DIR / "topic-rules.md": {
        "page_role": "index",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "asset_id": "cpa-zh:index:accounting-other-rules-topics",
        "source_id": "enterprise-accounting-standards-other-rules-download-2026-06-26",
        "knowledge_type": "accounting-other-rules-index",
        "source_type": "index",
        "version": "collection-2026-08-06",
        "effective_from": "unknown",
        "lifecycle_status": "unknown",
        "authority_level": "curated",
    },
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
        "related: [[concepts/accounting-standards-system]], [[concepts/accounting-standards/unmapped-review]]",
        "---",
        "",
        f"# {title}",
        "",
        "## 定位",
        "",
        description,
        "",
    ]
    if path == OTHER_RULES_DIR / "cash-pooling.md":
        lines.extend(
            [
                "## 来源与适用范围",
                "",
                "- 官方案例页：[[raw/standards/accounting/application-cases-pages/023-资金集中管理会计处理应用案例.html.md|资金集中管理会计处理应用案例]]。",
                "- 实质性附件：[[raw/standards/accounting/application-case-attachments/023-P020220124608610279549.pdf.md|财政部 PDF 文本门面]]。",
                "- 官方链接：https://kjs.mof.gov.cn/zt/kjzzss/srzzzq/jrgjzzyy/202201/t20220124_3784577.htm",
                "- 本页整理案例中的三种组织结构和账务连接，不替代对集团资金协议、账户控制权和报告期适用规则的判断。",
                "",
                "## 三种业务结构",
                "",
                "| 情形 | 资金管理主体 | 关键会计连接 |",
                "|---|---|---|",
                "| 一 | 母公司内设资金结算中心，资金归集到母公司银行账户 | 子公司形成对母公司的其他应收款；母公司对应其他应付款，超出归集余额的拨付形成拆借关系 |",
                "| 二 | 母公司内设资金结算中心，资金归集到母公司在财务公司的账户 | 母公司、财务公司和子公司分别确认存款、吸收存款或内部往来，需区分主体层级 |",
                "| 三 | 财务公司直接负责集团内资金集中管理 | 子公司在财务公司开立账户，额外资金需求可能体现为财务公司贷款和子公司短期借款 |",
                "",
                "## 判断与核查重点",
                "",
                "- 先识别账户开立主体、资金实际控制人、归集授权、可支取条件和资金池协议，再确定是内部往来、银行存款还是借款。",
                "- 将归集余额、拨付金额和额外拆借分开核算；同一主体既有归集资金又有额外融资时，不能只按资金净额判断。",
                "- 检查金融机构属性、资金利率、期限、减值迹象、关联方披露和合并报表抵销范围。",
                "- 重大性允许时可使用“应收资金集中管理款”等更能反映业务实质的科目，但应保持会计政策一致并充分披露。",
                "",
                "## 审计证据",
                "",
                "获取资金池协议、银行或财务公司对账单、账户授权、归集及拨付流水、内部审批、借款合同、利率和期限资料，编制母子公司往来及合并抵销勾稽表；对期末大额归集和期后回拨实施截止性检查。",
                "",
                "## 结论边界",
                "",
                "本页仅总结一个财政部应用案例。具体项目还需结合集团控制关系、资金可支配性、金融机构监管属性、减值和披露事实进行人工复核；案例分录不能直接替代项目会计政策。",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def supplement_block(groups: list[tuple[str, list[dict[str, str]]]]) -> str:
    lines = [
        START,
        "",
        "## 校准补充资料",
        "",
        "以下资料来自 [[concepts/accounting-standards/unmapped-review]] 的 Agent 复核候选。条目保留原始官方链接和本地 HTML 路径；正式引用前仍应结合原文核验适用范围和有效状态。",
    ]
    for bucket, rows in groups:
        lines.extend(
            [
                "",
                f"### Agent 候选桶：{bucket}",
                "",
                "| 类型 | 标题 | 置信度 | 证据依据 | 官方链接 | 本地文件 |",
                "|---|---|---|---|---|---|",
            ]
        )
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


def upsert_covid_boundary(text: str) -> str:
    block = "\n".join(
        [
            COVID_BOUNDARY_START,
            "",
            "## 当前适用边界",
            "",
            "> 本页已归入历史资料，不作为当前期间会计答疑的默认依据。仅在追溯疫情期间交易时使用，并须核对租金减让是否由疫情直接引发、合同其他条款是否发生重大变化，以及企业是否属于境外上市等排除范围。",
            "",
            "财政部 2022 年实施问答说明，财会〔2022〕13号曾允许符合条件的企业对 2022 年 6 月 30 日之后应付租赁付款额的疫情相关减让继续采用简化方法，但未在本地材料中给出统一废止日。因此本页不编造 `effective_to`，以 `historical` 管理并从当前有效答疑范围排除。",
            "",
            "- 规定原文：[[raw/standards/accounting/other-rules-pages/018-关于印发-新冠肺炎疫情相关租金减让会计处理规定-的通知.html.md|财会〔2020〕10号]]",
            "- 适用问答：[[raw/standards/accounting/implementation-qa-pages-v2/qa-059.html.md|2022 年简化处理方法适用问答]]",
            "",
            COVID_BOUNDARY_END,
        ]
    )
    pattern = re.compile(
        rf"(?:\r?\n)*{re.escape(COVID_BOUNDARY_START)}.*?{re.escape(COVID_BOUNDARY_END)}(?:\r?\n)*",
        re.S,
    )
    if pattern.search(text):
        return pattern.sub("\n\n" + block + "\n\n", text).rstrip() + "\n"
    marker = re.compile(rf"(?:\r?\n)*{re.escape(START)}")
    if marker.search(text):
        return marker.sub("\n\n" + block + "\n\n" + START, text, count=1)
    return text.rstrip() + "\n\n" + block + "\n"


def upsert_supplement(path: Path, groups: list[tuple[str, list[dict[str, str]]]]) -> None:
    if path in OTHER_RULE_PAGES:
        ensure_other_rule_page(path)
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    block = supplement_block(groups)
    pattern = re.compile(
        rf"(?:\r?\n)*{re.escape(START)}.*?{re.escape(END)}(?:\r?\n)*",
        re.S,
    )
    if pattern.search(text):
        text = pattern.sub("\n\n" + block, text).rstrip() + "\n"
    else:
        text = text.rstrip() + "\n\n" + block
    if path == OTHER_RULES_DIR / "covid-rent-concessions.md":
        text = upsert_covid_boundary(text)
    if path in OTHER_RULE_GOVERNANCE:
        text = update_frontmatter(text, OTHER_RULE_GOVERNANCE[path])
    path.write_text(text, encoding="utf-8")


def remove_supplement(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", re.S)
    cleaned = pattern.sub("\n", text).rstrip() + "\n"
    if cleaned == text:
        return False
    path.write_text(cleaned, encoding="utf-8")
    return True


def apply_page_governance(path: Path, fields: dict[str, object] | None = None) -> bool:
    if not path.exists():
        return False
    governance = fields if fields is not None else OTHER_RULE_GOVERNANCE.get(path)
    if not governance:
        return False
    text = path.read_text(encoding="utf-8")
    if path == OTHER_RULES_DIR / "covid-rent-concessions.md":
        text = upsert_covid_boundary(text)
    updated = update_frontmatter(text, governance)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


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
        "related: [[concepts/accounting-standards-system]], [[concepts/accounting-standards/unmapped-review]]",
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

    page_groups: dict[Path, list[tuple[str, list[dict[str, str]]]]] = defaultdict(list)
    for bucket, paths in TARGETS.items():
        rows = rows_by_bucket.get(bucket, [])
        if not rows:
            continue
        for path in paths:
            page_groups[path].append((bucket, rows))

    for bucket, rows in rows_by_bucket.items():
        match = re.fullmatch(r"解释第(\d+)号", bucket)
        if not match:
            continue
        path = ACCOUNTING_DIR / "interpretations" / f"interp-{int(match.group(1)):02d}.md"
        page_groups[path].append((bucket, rows))

    known_paths = set(OTHER_RULE_PAGES) | {path for paths in TARGETS.values() for path in paths}
    known_paths.update((ACCOUNTING_DIR / "interpretations").glob("interp-*.md"))
    for path in sorted(known_paths):
        groups = page_groups.get(path, [])
        if groups:
            upsert_supplement(path, groups)
        else:
            remove_supplement(path)

    for path in OTHER_RULE_GOVERNANCE:
        apply_page_governance(path)

    write_other_rules_index()
    print(f"updated_pages={len(page_groups)}")


if __name__ == "__main__":
    main()
