from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge-base" / "CPA-ZH" / "wiki"
CONCEPTS = WIKI / "concepts"

START = "<!-- practice-framework:start -->"
END = "<!-- practice-framework:end -->"


FRAMEWORKS: dict[Path, str] = {
    CONCEPTS / "law-cpa.md": """
## 有效版本线索

- 本地文本版本线索：1993-10-31 通过，2014-08-31 修正。
- 官方核验入口：国家法律法规数据库（`https://flk.npc.gov.cn/`）检索“中华人民共和国注册会计师法”。
- 本页以本地 raw 文本和条款级页面为知识库底稿；正式引用前应以国家法律法规数据库或权威发布文本复核。

## 核心义务地图

| 主题 | 条款入口 | 实务含义 |
|---|---|---|
| 行业监管主体 | [[concepts/laws/cpa-law/cpa-law-article-005]] | 财政部门对注册会计师、会计师事务所和协会进行监督指导。 |
| 法定审计业务范围 | [[concepts/laws/cpa-law/cpa-law-article-014]] | 财务报表审计、验资、合并分立清算相关审计和其他法定审计业务，是注册会计师法定职责的起点。 |
| 获取资料和现场协助 | [[concepts/laws/cpa-law/cpa-law-article-017]] | 审计程序需要客户配合时，可与审计证据、管理层责任和受限事项判断衔接。 |
| 回避和独立性 | [[concepts/laws/cpa-law/cpa-law-article-018]] | 与 [[concepts/ethics-code]]、[[concepts/independence-standard-1]] 共同构成独立性底线。 |
| 保密义务 | [[concepts/laws/cpa-law/cpa-law-article-019]] | 底稿、客户资料、询证信息和项目沟通均应纳入保密控制。 |
| 拒绝出具不当报告 | [[concepts/laws/cpa-law/cpa-law-article-020]] | 当委托人示意不实证明或故意不提供资料时，应升级为报告意见和业务保持问题。 |
| 按执业准则出具报告 | [[concepts/laws/cpa-law/cpa-law-article-021]] | 与 [[concepts/audit-standards-system]] 直接衔接，是“程序到意见”的法定连接点。 |
| 禁止行为 | [[concepts/laws/cpa-law/cpa-law-article-022]] | 覆盖利益冲突、违反独立性、索取收受不当利益等风险场景。 |

## 审计实务连接

| 实务问题 | 连接页面 |
|---|---|
| 客户资料受限、拒绝配合、管理层诚信疑虑 | [[concepts/audit-standards/csa-1211]], [[concepts/audit-standards/csa-1503]] |
| 独立性、收费、非鉴证服务和关联关系 | [[concepts/independence-standard-1]], [[concepts/ethics-code]] |
| 出具审计报告前的程序充分性 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1501]] |
| 事务所执业许可、监督检查和诚信建设 | [[concepts/policy-firm-license-supervision]], [[concepts/policy-firm-inspection]], [[concepts/policy-integrity]] |

## 风险提示

- 法定业务范围、独立性和报告责任应同时看，不能只把注册会计师法当作资格管理文件。
- 遇到客户限制审计范围、示意不当证明、重大资料缺失时，应同步考虑业务保持、治理层沟通和报告意见影响。
- 涉及证券服务业务时，还应联动 [[concepts/law-securities]] 的证券服务机构勤勉尽责和连带赔偿责任规则。
""",
    CONCEPTS / "law-accounting.md": """
## 有效版本线索

- 本地文本版本线索：1985-01-21 通过，1999-10-31 修订，2024-06-28 第三次修正。
- 官方核验入口：国家法律法规数据库（`https://flk.npc.gov.cn/`）检索“中华人民共和国会计法”。
- 本页以本地 raw 文本和条款级页面为知识库底稿；正式引用前应以国家法律法规数据库或权威发布文本复核。

## 核心义务地图

| 主题 | 条款入口 | 实务含义 |
|---|---|---|
| 会计资料真实完整 | [[concepts/laws/accounting-law/accounting-law-article-003]], [[concepts/laws/accounting-law/accounting-law-article-004]] | 单位负责人对会计工作和会计资料真实性、完整性负责，是审计管理层责任判断的上位依据。 |
| 以实际经济业务核算 | [[concepts/laws/accounting-law/accounting-law-article-009]] | 关注虚构交易、提前确认收入、隐藏负债和资金空转等风险。 |
| 会计资料符合统一制度 | [[concepts/laws/accounting-law/accounting-law-article-013]] | 与 [[concepts/accounting-standards-system]] 连接，支持会计政策适用和列报披露判断。 |
| 财务会计报告编制 | [[concepts/laws/accounting-law/accounting-law-article-020]], [[concepts/laws/accounting-law/accounting-law-article-021]] | 报表编制、签章责任和管理层声明应形成一致证据链。 |
| 内部会计监督 | [[concepts/laws/accounting-law/accounting-law-article-025]], [[concepts/laws/accounting-law/accounting-law-article-026]] | 与内部控制了解、控制测试和舞弊风险识别直接相关。 |
| 向事务所如实提供资料 | [[concepts/laws/accounting-law/accounting-law-article-029]], [[concepts/laws/accounting-law/accounting-law-article-033]] | 支持审计资料完整性、范围受限和管理层诚信评价。 |
| 违法责任和信用记录 | [[concepts/laws/accounting-law/accounting-law-article-040]], [[concepts/laws/accounting-law/accounting-law-article-041]], [[concepts/laws/accounting-law/accounting-law-article-042]], [[concepts/laws/accounting-law/accounting-law-article-047]] | 对假账、虚假报告、隐匿销毁资料和授意违法的责任风险形成定位。 |

## 审计实务连接

| 实务问题 | 连接页面 |
|---|---|
| 会计资料真实完整和管理层责任 | [[concepts/audit-standards/csa-1151]], [[concepts/audit-standards/csa-1301]] |
| 虚假财务报告、舞弊和凌驾控制 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1211]] |
| 会计政策、会计估计和财务报表列报 | [[concepts/accounting-standards-system]], [[concepts/accounting-standards/cas-30]], [[concepts/audit-standards/csa-1321]] |
| 财会监督和审计秩序治理 | [[concepts/policy-caihui-supervision]], [[concepts/policy-audit-order]] |

## 风险提示

- 会计法更偏向单位会计责任和财会监督，不能替代具体企业会计准则判断。
- 审计中发现资料不完整、不真实或管理层限制时，应将会计法责任、审计证据充分适当性和报告意见影响放在同一张判断表里。
- 2024 年修正后的条文应在正式引用前复核官方数据库文本，尤其是法律责任和处罚金额相关条款。
""",
    CONCEPTS / "law-company.md": """
## 有效版本线索

- 本地文本版本线索：1993-12-29 通过，2023-12-29 第二次修订；新修订公司法自 2024-07-01 起施行。
- 官方核验入口：国家法律法规数据库公司法 2023 年版本 `https://flk.npc.gov.cn/detail2.html?ZmY4MDgxODE4YzkxMDhlYjAxOGNiNjkyMmY3NTBjMDc%3D=`。
- 本页以本地 raw 文本和条款级页面为知识库底稿；正式引用前应以国家法律法规数据库或权威发布文本复核。

## 核心义务地图

| 主题 | 条款入口 | 实务含义 |
|---|---|---|
| 股东查阅和财务信息权利 | [[concepts/laws/company-law/company-law-article-057]], [[concepts/laws/company-law/company-law-article-110]] | 财务报告、会议记录、股东名册和治理资料是审计了解治理结构的重要证据。 |
| 上市公司信息披露相关治理 | [[concepts/laws/company-law/company-law-article-138]], [[concepts/laws/company-law/company-law-article-140]] | 与 [[concepts/law-securities]] 的信息披露责任衔接。 |
| 财务会计制度和年度报告审计 | [[concepts/laws/company-law/company-law-article-207]], [[concepts/laws/company-law/company-law-article-208]], [[concepts/laws/company-law/company-law-article-209]] | 公司应建立财务会计制度，并在会计年度终了编制财务会计报告、依法经审计。 |
| 利润分配和公积金 | [[concepts/laws/company-law/company-law-article-210]], [[concepts/laws/company-law/company-law-article-211]], [[concepts/laws/company-law/company-law-article-212]], [[concepts/laws/company-law/company-law-article-214]] | 利润分配、弥补亏损、公积金和资本公积处理影响权益列报和合规风险。 |
| 聘用会计师事务所 | [[concepts/laws/company-law/company-law-article-215]], [[concepts/laws/company-law/company-law-article-216]] | 公司应向事务所提供真实、完整资料，不得拒绝、隐匿、谎报。 |
| 另立账簿和虚假报告责任 | [[concepts/laws/company-law/company-law-article-217]], [[concepts/laws/company-law/company-law-article-254]] | 与会计法、舞弊风险和审计范围受限判断直接相关。 |
| 验资、验证和中介责任 | [[concepts/laws/company-law/company-law-article-101]], [[concepts/laws/company-law/company-law-article-257]] | 涉及验资、验证、评估或重大遗漏报告时，应联动注册会计师法责任。 |

## 审计实务连接

| 实务问题 | 连接页面 |
|---|---|
| 公司治理、董监高责任和治理层沟通 | [[concepts/audit-standards/csa-1151]], [[concepts/audit-standards/csa-1211]] |
| 利润分配、权益交易和资本公积 | [[concepts/accounting-standards/cas-30]], [[concepts/accounting-standards/cas-37]] |
| 合并范围、股权结构和控制判断 | [[concepts/accounting-standards/cas-33]], [[concepts/audit-standards/csa-1401]] |
| 另立账簿、虚假财务报告和管理层诚信 | [[concepts/law-accounting]], [[concepts/audit-standards/csa-1141]] |

## 风险提示

- 公司法中的财务会计制度、利润分配、事务所聘用和资料提供义务，是年报审计和治理层沟通的常用上位依据。
- 对股权转让、增资减资、利润分配、回购股份、合并分立清算等事项，应同时看公司法、会计准则和审计证据。
- 2023 年修订后条文编号和内容变化较大，引用历史底稿或旧模板时要核对条号。
""",
    CONCEPTS / "law-securities.md": """
## 有效版本线索

- 本地文本版本线索：1998-12-29 通过，2019-12-28 第二次修订；修订后证券法自 2020-03-01 起施行。
- 官方核验入口：国家法律法规数据库证券法 2019 年版本 `https://flk.npc.gov.cn/detail2.html?ZmY4MDgwODE3MWU5ZTE4MTAxNzI3ZTMyYjk0ZDdkZTY%3D=`。
- 本页以本地 raw 文本和条款级页面为知识库底稿；正式引用前应以国家法律法规数据库或权威发布文本复核。

## 核心义务地图

| 主题 | 条款入口 | 实务含义 |
|---|---|---|
| 证券发行和公司法衔接 | [[concepts/laws/securities-law/securities-law-article-002]] | 发行交易中的公司治理、资本制度和信息披露需与 [[concepts/law-company]] 联动。 |
| 信息披露基本责任 | [[concepts/laws/securities-law/securities-law-article-078]], [[concepts/laws/securities-law/securities-law-article-079]], [[concepts/laws/securities-law/securities-law-article-080]] | 真实、准确、完整、及时、公平披露是上市公司审计风险评估的核心背景。 |
| 年报和临时报告事项 | [[concepts/laws/securities-law/securities-law-article-082]], [[concepts/laws/securities-law/securities-law-article-085]] | 财务报告、重大交易、重大风险和治理变化影响审计计划和关键审计事项。 |
| 证券服务机构勤勉尽责 | [[concepts/laws/securities-law/securities-law-article-160]], [[concepts/laws/securities-law/securities-law-article-163]] | 会计师事务所出具证券业务审计报告或鉴证报告时，应核查验证所依据资料。 |
| 投资者保护和民事责任 | [[concepts/laws/securities-law/securities-law-article-169]], [[concepts/laws/securities-law/securities-law-article-220]] | 虚假陈述、误导性陈述、重大遗漏可能引发行政、民事和声誉风险。 |
| 信息披露违法责任 | [[concepts/laws/securities-law/securities-law-article-197]] | 发行人、控股股东、实际控制人和责任人员均可能被追责。 |
| 证券服务机构违法责任 | [[concepts/laws/securities-law/securities-law-article-213]], [[concepts/laws/securities-law/securities-law-article-214]] | 未勤勉尽责、文件虚假记载或资料保存问题会直接触发中介机构责任。 |

## 审计实务连接

| 实务问题 | 连接页面 |
|---|---|
| 上市公司年报审计、IPO 审计和证券服务责任 | [[concepts/policy-audit-order]], [[concepts/case-analysis]] |
| 信息披露重大错报、舞弊和关键审计事项 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1504]] |
| 其他信息、年报一致性和报告后事项 | [[concepts/audit-standards/csa-1521]], [[concepts/audit-standards/csa-1501]] |
| 合并范围、收入确认、金融工具估值等高频监管风险 | [[concepts/accounting-standards/cas-33]], [[concepts/accounting-standards/cas-14]], [[concepts/accounting-standards/cas-22]] |

## 风险提示

- 证券法下的审计责任不是只看报告签字页，而是看是否勤勉尽责、是否对依据资料进行必要核查验证。
- 对公众公司项目，应把信息披露口径、财务报表审计结论、其他信息和监管问询放在同一风险闭环中。
- 证券服务机构责任常与注册会计师法、会计法、公司法和监管处罚规则叠加，应在重大项目收口阶段单独复核。
""",
}


def upsert_framework(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    full = START + "\n" + block.strip() + "\n\n" + END
    pattern = re.compile(rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?", re.S)
    if pattern.search(text):
        text = pattern.sub("\n\n" + full + "\n", text).rstrip() + "\n"
    else:
        text = text.rstrip() + "\n\n" + full + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for path, block in FRAMEWORKS.items():
        if not path.exists():
            raise FileNotFoundError(path)
        upsert_framework(path, block)
    print(f"law_practice_pages={len(FRAMEWORKS)}")


if __name__ == "__main__":
    main()
