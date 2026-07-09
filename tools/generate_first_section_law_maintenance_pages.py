from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONCEPTS = ROOT / "knowledge-base" / "CPA-ZH" / "wiki" / "concepts"


PAGES: dict[Path, str] = {
    CONCEPTS / "core-laws-official-verification.md": """---
title: 四部核心法律官方版本核验页
type: concept
concept_type: verification-map
created: 2026-06-26
updated: 2026-06-26
sources: [local-core-laws-2026-06-26, core-laws-article-index-2026-06-26]
tags: [law, official-verification, p1-core]
related: [[concepts/law-cpa]], [[concepts/law-accounting]], [[concepts/law-company]], [[concepts/law-securities]], [[concepts/first-section-responsibility-risk-map]]
---

# 四部核心法律官方版本核验页

本页用于维护四部核心法律的版本线索、官方核验入口和知识库引用状态。由于网络访问可能受限，除已明确记录的官方链接外，其余统一标注为“以国家法律法规数据库检索核验为准”。

## 核验总表

| 法律 | 本地版本线索 | 官方核验入口 | 当前处理 |
|---|---|---|---|
| [[concepts/law-cpa]] | 1993-10-31 通过，2014-08-31 修正 | 国家法律法规数据库首页 `https://flk.npc.gov.cn/` 检索“中华人民共和国注册会计师法” | 已生成概览页和 46 个条款页；直接引用前需复核官方数据库。 |
| [[concepts/law-accounting]] | 1985-01-21 通过，1999-10-31 修订，2024-06-28 第三次修正 | 国家法律法规数据库首页 `https://flk.npc.gov.cn/` 检索“中华人民共和国会计法” | 已生成概览页和 51 条记录；本地原文附则存在两个“第四十九条”，条款页已保留。 |
| [[concepts/law-company]] | 1993-12-29 通过，2023-12-29 第二次修订；2024-07-01 施行 | `https://flk.npc.gov.cn/detail2.html?ZmY4MDgxODE4YzkxMDhlYjAxOGNiNjkyMmY3NTBjMDc%3D=` | 已生成概览页和 266 个条款页；新旧条号差异较大，引用旧模板时需核对。 |
| [[concepts/law-securities]] | 1998-12-29 通过，2019-12-28 第二次修订；2020-03-01 施行 | `https://flk.npc.gov.cn/detail2.html?ZmY4MDgwODE3MWU5ZTE4MTAxNzI3ZTMyYjk0ZDdkZTY%3D=` | 已生成概览页和 226 个条款页；证券服务责任条款已纳入专题矩阵。 |

## 核验流程

1. 从国家法律法规数据库检索法律名称，核对题名、通过/修订/修正日期、施行日期和正文。
2. 将官方文本与 `raw/laws/` 本地文本比对，重点看条号、法律责任金额、附则和施行日期。
3. 如发现本地文本与官方文本不一致，先更新 `wiki/` 页面的核验说明，不直接覆盖 `raw/`；待确认后再做 raw 层替换或新增版本文件。
4. 更新 [[concepts/first-section-completion-map]] 和 [[sources/core-laws-article-index-2026-06-26]] 的说明。

## 当前风险提示

- 《会计法》存在 2024 年修正，处罚条款和信用记录相关内容应作为正式引用前重点复核项。
- 《公司法》2023 年修订后条号变化明显，历史底稿、旧培训材料和模板中的条号不宜直接沿用。
- 《证券法》涉及证券服务机构连带赔偿、行政责任和资料保存责任，公众公司项目应优先核验。
""",
    CONCEPTS / "first-section-responsibility-risk-map.md": """---
title: 第一板块责任风险总表
type: concept
concept_type: responsibility-map
created: 2026-06-26
updated: 2026-06-26
sources: [core-laws-article-index-2026-06-26, first-section-master-index-2026-06-26]
tags: [law, audit-risk, responsibility, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/core-laws-official-verification]], [[concepts/law-cpa]], [[concepts/law-accounting]], [[concepts/law-company]], [[concepts/law-securities]]
---

# 第一板块责任风险总表

本表把第一板块中常见责任风险按“责任主体-法律入口-准则入口-审计收口”组织，便于从实务问题快速回到法规和准则依据。

## 责任风险矩阵

| 风险主题 | 责任主体 | 法律入口 | 准则/专题入口 | 审计收口 |
|---|---|---|---|---|
| 会计资料不真实、不完整 | 单位负责人、公司、信息披露义务人 | [[concepts/laws/accounting-law/accounting-law-article-003]], [[concepts/laws/accounting-law/accounting-law-article-004]], [[concepts/laws/accounting-law/accounting-law-article-041]] | [[concepts/accounting-standards-system]], [[concepts/audit-standards/csa-1301]] | 管理层责任、证据充分适当性、报告意见。 |
| 虚假财务报告或重大遗漏 | 公司、发行人、控股股东、实际控制人 | [[concepts/laws/company-law/company-law-article-254]], [[concepts/laws/securities-law/securities-law-article-197]] | [[concepts/first-section-topic-matrix]], [[concepts/audit-standards/csa-1141]] | 舞弊风险、关键审计事项、非无保留意见。 |
| 客户拒绝、隐匿、谎报资料 | 被审计单位、公司、管理层 | [[concepts/laws/accounting-law/accounting-law-article-029]], [[concepts/laws/company-law/company-law-article-216]], [[concepts/laws/cpa-law/cpa-law-article-020]] | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1503]] | 范围受限、管理层诚信、业务保持。 |
| 注册会计师未按准则执业 | 注册会计师、会计师事务所 | [[concepts/laws/cpa-law/cpa-law-article-021]], [[concepts/laws/cpa-law/cpa-law-article-022]] | [[concepts/audit-standards-system]], [[concepts/policy-audit-order]] | 项目质量复核、底稿闭环、报告签发。 |
| 证券服务机构未勤勉尽责 | 会计师事务所、签字注册会计师、证券服务机构 | [[concepts/laws/securities-law/securities-law-article-163]], [[concepts/laws/securities-law/securities-law-article-213]], [[concepts/laws/securities-law/securities-law-article-214]] | [[concepts/first-section-topics/securities-service-liability]], [[concepts/audit-standards/csa-1501]] | 证券业务证据链、信息披露一致性、资料保存。 |
| 关联方及资金占用披露不完整 | 公司、控股股东、实际控制人、管理层 | [[concepts/laws/company-law/company-law-article-140]], [[concepts/laws/securities-law/securities-law-article-078]], [[concepts/laws/securities-law/securities-law-article-197]] | [[concepts/first-section-topics/related-parties-fund-occupation]], [[concepts/audit-standards/csa-1323]] | 关联方识别、函证、资金流水、披露评价。 |
| 重大估计不当 | 管理层、治理层、注册会计师 | [[concepts/laws/accounting-law/accounting-law-article-020]], [[concepts/laws/securities-law/securities-law-article-080]] | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1421]] | 模型、假设、数据、专家工作、敏感性分析。 |
| 审计报告不当 | 注册会计师、会计师事务所 | [[concepts/laws/cpa-law/cpa-law-article-014]], [[concepts/laws/cpa-law/cpa-law-article-021]], [[concepts/laws/securities-law/securities-law-article-163]] | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1504]] | 意见类型、关键审计事项、其他信息、治理层沟通。 |

## 使用建议

- 先用本页定位责任主体和法律入口，再进入 [[concepts/first-section-topic-matrix]] 查实务专题。
- 对公众公司项目，优先联动 [[concepts/law-securities]]、[[concepts/first-section-topics/securities-service-liability]] 和 [[concepts/audit-standards/csa-1521]]。
- 对非公众公司项目，优先联动 [[concepts/law-accounting]]、[[concepts/law-company]] 和 [[concepts/audit-standards/topics]]。
""",
}


def main() -> None:
    for path, text in PAGES.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"law_maintenance_pages={len(PAGES)}")


if __name__ == "__main__":
    main()
