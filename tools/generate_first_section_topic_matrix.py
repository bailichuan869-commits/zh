from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge-base" / "CPA-ZH" / "wiki"
CONCEPTS = WIKI / "concepts"
TOPICS = CONCEPTS / "first-section-topics"


PAGES: dict[Path, str] = {
    CONCEPTS / "first-section-topic-matrix.md": """---
title: 第一板块专题矩阵
type: concept
concept_type: topic-matrix
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26, core-laws-article-index-2026-06-26, enterprise-accounting-standards-number-index-2026-06-26, cicpa-professional-standards-number-index-2026-06-26]
tags: [cpa, law, standards, topic-matrix, p1-core]
related: [[concepts/regulations-and-standards]], [[concepts/first-section-completion-map]], [[concepts/accounting-standards-system]], [[concepts/audit-standards-system]]
---

# 第一板块专题矩阵

本页把第一板块的法律、企业会计准则和中国注册会计师执业准则按实务问题重组。使用时先按问题进入专题页，再回到法律条款、会计准则页和审计准则页核对原始依据。

## 专题入口

| 专题 | 适用场景 | 入口 |
|---|---|---|
| 收入确认错报风险 | 收入真实性、截止、履约义务、可变对价、合同资产负债 | [[concepts/first-section-topics/revenue-recognition-misstatement]] |
| 金融工具估值与减值 | 金融资产分类、预期信用损失、公允价值、复杂金融工具 | [[concepts/first-section-topics/financial-instruments-valuation-impairment]] |
| 合并范围与控制判断 | 集团架构、结构化主体、实控人安排、组成部分审计 | [[concepts/first-section-topics/consolidation-scope-control]] |
| 持续经营与重大不确定性 | 亏损、流动性压力、债务违约、经营停滞、报告段落 | [[concepts/first-section-topics/going-concern-uncertainty]] |
| 关键审计事项 | 上市公司审计报告、重大判断、复杂估计、治理层沟通 | [[concepts/first-section-topics/key-audit-matters]] |
| 证券服务责任 | IPO、上市公司年报、证券服务机构勤勉尽责和连带赔偿 | [[concepts/first-section-topics/securities-service-liability]] |
| 关联方及资金占用 | 关联方识别、非经营性资金占用、异常往来、利益输送 | [[concepts/first-section-topics/related-parties-fund-occupation]] |
| 资产减值 | 商誉、长期资产、金融资产、存货减值和可收回金额估计 | [[concepts/first-section-topics/asset-impairment]] |
| 利润分配和权益交易 | 利润分配、公积金、资本公积、回购股份和负债权益区分 | [[concepts/first-section-topics/profit-distribution-equity-transactions]] |
| 所得税和递延所得税 | 暂时性差异、递延所得税资产可抵扣性、税务风险 | [[concepts/first-section-topics/income-tax-deferred-tax]] |
| 政府补助和专项资金 | 与资产/收益相关补助、递延收益、专项资金使用限制 | [[concepts/first-section-topics/government-grants-special-funds]] |
| 或有事项和重大诉讼 | 未决诉讼、担保、亏损合同、预计负债和披露 | [[concepts/first-section-topics/contingencies-major-litigation]] |
| 职工薪酬 | 短期薪酬、离职后福利、辞退福利、股份支付交叉 | [[concepts/first-section-topics/employee-benefits]] |
| 长期股权投资 | 控制、共同控制、重大影响、权益法和处置 | [[concepts/first-section-topics/long-term-equity-investments]] |

## 横向使用方法

1. 先定位法律责任：从 [[concepts/law-accounting]], [[concepts/law-company]], [[concepts/law-securities]], [[concepts/law-cpa]] 判断责任主体和法定义务。
2. 再定位会计判断：从 [[concepts/accounting-standards-system]] 进入具体企业会计准则、解释、应用案例和实施问答。
3. 最后设计审计应对：从 [[concepts/audit-standards/topics]] 进入风险评估、审计证据、估计、函证、报告等程序页面。

## 后续扩展候选

- 股份支付和激励计划专题：连接 [[concepts/accounting-standards/cas-11]], [[concepts/accounting-standards/cas-37]]。
- 租赁复杂安排专题：连接 [[concepts/accounting-standards/cas-21]], [[concepts/audit-standards/csa-1321]]。
- 会计政策、估计变更和差错更正专题：连接 [[concepts/accounting-standards/cas-28]], [[concepts/audit-standards/csa-1501]]。
""",
    TOPICS / "revenue-recognition-misstatement.md": """---
title: 收入确认错报风险专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [revenue, audit-risk, accounting-standards, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/accounting-standards/cas-14]], [[concepts/audit-standards/csa-1141]], [[concepts/law-accounting]]
---

# 收入确认错报风险专题

## 问题定位

收入专题通常同时涉及会计法上的会计资料真实完整、公司法上的财务会计报告责任、证券法上的信息披露责任，以及收入准则和审计准则中的舞弊风险、截止、证据和报告判断。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 会计资料真实完整 | [[concepts/laws/accounting-law/accounting-law-article-003]], [[concepts/laws/accounting-law/accounting-law-article-004]] | 判断单位负责人和会计资料责任。 |
| 实际经济业务核算 | [[concepts/laws/accounting-law/accounting-law-article-009]] | 识别虚构交易、提前确认、循环交易和无商业实质安排。 |
| 财务报告编制责任 | [[concepts/laws/accounting-law/accounting-law-article-020]], [[concepts/laws/company-law/company-law-article-208]] | 连接财务报表编制、审计和披露责任。 |
| 向事务所提供资料 | [[concepts/laws/accounting-law/accounting-law-article-029]], [[concepts/laws/company-law/company-law-article-216]] | 处理合同、发货、验收、回款等证据不完整问题。 |
| 虚假报告和信息披露责任 | [[concepts/laws/accounting-law/accounting-law-article-041]], [[concepts/laws/securities-law/securities-law-article-197]] | 评估重大错报、虚假记载和重大遗漏的责任风险。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 五步法、履约义务、交易价格、控制权转移 | [[concepts/accounting-standards/cas-14]] |
| 报表列报、合同资产、合同负债和应收项目列示 | [[concepts/accounting-standards/cas-30]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 收入舞弊风险和管理层凌驾 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1211]] |
| 合同、发货、验收、回款和截止证据 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1313]] |
| 应收账款和合同资产函证 | [[concepts/audit-standards/csa-1312]] |
| 是否形成关键审计事项或影响意见 | [[concepts/audit-standards/csa-1504]], [[concepts/audit-standards/csa-1501]] |

## 底稿收口

- 将合同条款、履约义务判断、发货验收证据、收入分录、回款和期后退货串成同一条证据链。
- 对新业务模式、平台交易、代理人安排、售后回购、重大退货权和可变对价形成单独判断备忘。
- 对上市公司项目，同步检查收入相关信息披露与年报其他信息的一致性，连接 [[concepts/audit-standards/csa-1521]]。
""",
    TOPICS / "financial-instruments-valuation-impairment.md": """---
title: 金融工具估值与减值专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [financial-instruments, valuation, impairment, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/accounting-standards/cas-22]], [[concepts/audit-standards/csa-1321]], [[concepts/law-securities]]
---

# 金融工具估值与减值专题

## 问题定位

金融工具专题重点覆盖金融资产分类、合同现金流量特征、业务模式、公允价值估值、预期信用损失、负债权益区分和披露。高风险项目通常同时牵涉会计估计、专家工作、信息披露和证券服务责任。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 国家统一会计制度 | [[concepts/laws/accounting-law/accounting-law-article-013]] | 连接企业会计准则的分类、计量和披露要求。 |
| 财务会计报告责任 | [[concepts/laws/accounting-law/accounting-law-article-020]], [[concepts/laws/company-law/company-law-article-208]] | 评估估值和减值是否进入报表和附注。 |
| 信息披露真实准确完整 | [[concepts/laws/securities-law/securities-law-article-078]], [[concepts/laws/securities-law/securities-law-article-080]] | 处理复杂金融工具、重大估计和敏感性披露。 |
| 证券服务机构勤勉尽责 | [[concepts/laws/securities-law/securities-law-article-163]], [[concepts/laws/securities-law/securities-law-article-213]] | 评价审计报告或鉴证报告涉及复杂估值时的中介责任。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 金融工具确认计量、分类、减值和终止确认 | [[concepts/accounting-standards/cas-22]] |
| 金融工具列报、负债权益区分和披露 | [[concepts/accounting-standards/cas-37]] |
| 财务报表列报和重要披露 | [[concepts/accounting-standards/cas-30]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 会计估计、估值模型、管理层偏向 | [[concepts/audit-standards/csa-1321]] |
| 利用专家工作和评价专家胜任能力 | [[concepts/audit-standards/csa-1421]] |
| 估值输入、外部证据和模型证据 | [[concepts/audit-standards/csa-1301]] |
| 关键审计事项和报告披露 | [[concepts/audit-standards/csa-1504]], [[concepts/audit-standards/csa-1501]] |

## 底稿收口

- 建立金融工具清单，逐项勾稽合同条款、业务模式、现金流量特征、计量属性和报表列示。
- 对公允价值模型、关键参数、市场数据来源、信用风险阶段划分和前瞻性调整保留复核轨迹。
- 对管理层覆盖调整、非活跃市场报价和重大敏感性结果，单独形成项目组判断。
""",
    TOPICS / "consolidation-scope-control.md": """---
title: 合并范围与控制判断专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [consolidation, control, group-audit, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/accounting-standards/cas-33]], [[concepts/audit-standards/csa-1401]], [[concepts/law-company]]
---

# 合并范围与控制判断专题

## 问题定位

合并范围专题关注控制判断、结构化主体、委托代理、潜在表决权、实际控制人安排和集团审计责任。它通常跨越公司治理、证券信息披露、合并报表准则和集团审计准则。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 公司治理和股东资料 | [[concepts/laws/company-law/company-law-article-057]], [[concepts/laws/company-law/company-law-article-110]] | 获取章程、股东名册、会议记录和财务报告，识别控制安排。 |
| 上市公司信息披露 | [[concepts/laws/company-law/company-law-article-140]], [[concepts/laws/securities-law/securities-law-article-078]] | 核对实际控制人、重大投资、并购和处置披露。 |
| 年度报告和重大事项披露 | [[concepts/laws/securities-law/securities-law-article-082]], [[concepts/laws/securities-law/securities-law-article-085]] | 识别合并范围变化、重大交易和风险事项。 |
| 向事务所提供完整资料 | [[concepts/laws/company-law/company-law-article-216]] | 处理组成部分资料、投资协议和控制证据缺失。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 控制三要素、合并范围和结构化主体 | [[concepts/accounting-standards/cas-33]] |
| 长期股权投资、权益法和成本法衔接 | [[concepts/accounting-standards/cas-02]] |
| 财务报表列报和合并抵销结果 | [[concepts/accounting-standards/cas-30]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 识别合并范围重大错报风险 | [[concepts/audit-standards/csa-1211]] |
| 关联方、实际控制人和特殊关系识别 | [[concepts/audit-standards/csa-1323]] |
| 集团审计、组成部分重要性和复核 | [[concepts/audit-standards/csa-1401]] |
| 合并报表结论和报告影响 | [[concepts/audit-standards/csa-1501]] |

## 底稿收口

- 将集团架构图、工商信息、投资协议、章程、董事会安排、资金往来和实际决策记录交叉核对。
- 对未纳入合并范围主体列明排除理由，尤其关注结构化主体、代持、委托代理和一致行动安排。
- 将组成部分审计发现、合并调整、抵销分录和未更正错报统一汇总。
""",
    TOPICS / "going-concern-uncertainty.md": """---
title: 持续经营与重大不确定性专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [going-concern, audit-report, disclosure, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/audit-standards/csa-1324]], [[concepts/audit-standards/csa-1503]], [[concepts/accounting-standards/cas-30]]
---

# 持续经营与重大不确定性专题

## 问题定位

持续经营专题关注企业是否有能力在可预见未来持续经营，以及管理层披露和审计报告段落是否足以反映重大不确定性。常见触发因素包括连续亏损、流动性紧张、债务违约、主要业务停滞、重大诉讼和融资失败。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 财务报告编制和签章 | [[concepts/laws/accounting-law/accounting-law-article-020]], [[concepts/laws/accounting-law/accounting-law-article-021]] | 判断管理层是否在报表和附注中反映持续经营事项。 |
| 公司年度财务报告审计 | [[concepts/laws/company-law/company-law-article-208]], [[concepts/laws/company-law/company-law-article-209]] | 连接公司年度报告、股东沟通和审计要求。 |
| 重大事项和风险披露 | [[concepts/laws/securities-law/securities-law-article-080]], [[concepts/laws/securities-law/securities-law-article-082]] | 上市公司项目中核对重大风险和临时公告。 |
| 虚假记载和重大遗漏责任 | [[concepts/laws/securities-law/securities-law-article-197]] | 持续经营披露不足可能形成信息披露风险。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 财务报表列报、重要性和附注披露 | [[concepts/accounting-standards/cas-30]] |
| 或有事项、未决诉讼和重大承诺 | [[concepts/accounting-standards/cas-13]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 持续经营评价和管理层未来应对计划 | [[concepts/audit-standards/csa-1324]] |
| 审计意见类型和强调事项段 | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1503]] |
| 其他信息与财务报表一致性 | [[concepts/audit-standards/csa-1521]] |
| 舞弊风险和管理层偏向 | [[concepts/audit-standards/csa-1141]] |

## 底稿收口

- 获取现金流预测、融资协议、债务到期表、违约豁免、经营计划和期后事项证据。
- 评价管理层计划的可执行性，不只看计划文字，还要看历史兑现能力和外部约束。
- 报告收口时区分“充分披露下的重大不确定性段落”和“披露不足导致的非无保留意见”。
""",
    TOPICS / "key-audit-matters.md": """---
title: 关键审计事项专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [key-audit-matters, audit-report, listed-company, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/audit-standards/csa-1504]], [[concepts/audit-standards/csa-1151]], [[concepts/law-securities]]
---

# 关键审计事项专题

## 问题定位

关键审计事项来自与治理层沟通过的事项，并从本期审计中最为重要的事项中确定。它不是替代管理层披露，也不能掩盖无法获取充分适当审计证据的问题。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 证券信息披露责任 | [[concepts/laws/securities-law/securities-law-article-078]], [[concepts/laws/securities-law/securities-law-article-080]] | 核对关键事项与年报披露是否一致。 |
| 年度报告和重大事项 | [[concepts/laws/securities-law/securities-law-article-082]], [[concepts/laws/securities-law/securities-law-article-085]] | 定位收入、估值、并购、持续经营等高关注事项。 |
| 证券服务机构勤勉尽责 | [[concepts/laws/securities-law/securities-law-article-163]] | 关键事项文字应能追溯到审计应对和证据。 |
| 信息披露违法责任 | [[concepts/laws/securities-law/securities-law-article-197]] | 重大遗漏或误导性陈述可能放大报告风险。 |

## 常见会计事项入口

| 事项 | 入口 |
|---|---|
| 收入确认 | [[concepts/accounting-standards/cas-14]], [[concepts/first-section-topics/revenue-recognition-misstatement]] |
| 金融工具估值和减值 | [[concepts/accounting-standards/cas-22]], [[concepts/first-section-topics/financial-instruments-valuation-impairment]] |
| 合并范围和重大并购处置 | [[concepts/accounting-standards/cas-33]], [[concepts/first-section-topics/consolidation-scope-control]] |
| 持续经营重大不确定性 | [[concepts/first-section-topics/going-concern-uncertainty]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 治理层沟通事项来源 | [[concepts/audit-standards/csa-1151]] |
| 关键审计事项确定和报告描述 | [[concepts/audit-standards/csa-1504]] |
| 审计意见和报告整体收口 | [[concepts/audit-standards/csa-1501]] |
| 无法获取充分证据时的意见类型 | [[concepts/audit-standards/csa-1503]] |

## 底稿收口

- 将关键审计事项候选清单、治理层沟通记录、风险评估、审计应对和报告文字放在同一索引下。
- 描述“审计中如何应对”时，应能回到具体程序、证据和项目组结论。
- 对未列为关键审计事项的重大事项，保留排除理由，避免报告阶段只靠文字判断。
""",
    TOPICS / "securities-service-liability.md": """---
title: 证券服务责任专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [securities-service, liability, audit-report, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/law-securities]], [[concepts/law-cpa]], [[concepts/policy-audit-order]]
---

# 证券服务责任专题

## 问题定位

证券服务责任专题用于 IPO、上市公司年报、再融资、重大资产重组等公众公司项目。核心是证券服务机构是否勤勉尽责，审计报告或鉴证文件是否存在虚假记载、误导性陈述或重大遗漏，以及能否证明自己没有过错。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 注册会计师法定业务和报告证明效力 | [[concepts/laws/cpa-law/cpa-law-article-014]], [[concepts/laws/cpa-law/cpa-law-article-021]] | 连接注册会计师法下的业务范围和执业准则要求。 |
| 拒绝不当报告和禁止行为 | [[concepts/laws/cpa-law/cpa-law-article-020]], [[concepts/laws/cpa-law/cpa-law-article-022]] | 处理客户施压、资料受限、利益冲突和独立性问题。 |
| 证券服务机构勤勉尽责 | [[concepts/laws/securities-law/securities-law-article-160]], [[concepts/laws/securities-law/securities-law-article-163]] | 证券业务审计报告和鉴证报告的核心法律入口。 |
| 连带赔偿和民事责任优先 | [[concepts/laws/securities-law/securities-law-article-169]], [[concepts/laws/securities-law/securities-law-article-220]] | 评估投资者损失、赔偿责任和风险后果。 |
| 中介机构行政责任 | [[concepts/laws/securities-law/securities-law-article-213]], [[concepts/laws/securities-law/securities-law-article-214]] | 识别未勤勉尽责、文件虚假和资料保存责任。 |

## 准则和政策入口

| 问题 | 入口 |
|---|---|
| 执业准则总入口 | [[concepts/audit-standards-system]], [[concepts/audit-standards/topics]] |
| 审计证据和报告意见 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1501]] |
| 关键审计事项和其他信息 | [[concepts/audit-standards/csa-1504]], [[concepts/audit-standards/csa-1521]] |
| 规范财务审计秩序和行业诚信 | [[concepts/policy-audit-order]], [[concepts/policy-integrity]] |

## 高频项目入口

| 项目风险 | 入口 |
|---|---|
| 收入确认重大错报 | [[concepts/first-section-topics/revenue-recognition-misstatement]] |
| 金融工具估值和减值 | [[concepts/first-section-topics/financial-instruments-valuation-impairment]] |
| 合并范围和控制判断 | [[concepts/first-section-topics/consolidation-scope-control]] |
| 持续经营重大不确定性 | [[concepts/first-section-topics/going-concern-uncertainty]] |

## 底稿收口

- 证券服务项目应保留“重大风险-程序-证据-结论-报告披露”的闭环索引。
- 对监管问询、年报其他信息、公告披露和财务报表之间的不一致，应记录识别、追问和处理过程。
- 重大判断事项应同步留痕项目质量复核、治理层沟通和合伙人最终判断。
""",
    TOPICS / "related-parties-fund-occupation.md": """---
title: 关联方及资金占用专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [related-parties, fund-occupation, audit-risk, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/accounting-standards/cas-36]], [[concepts/audit-standards/csa-1323]], [[concepts/law-company]], [[concepts/law-securities]]
---

# 关联方及资金占用专题

## 问题定位

关联方及资金占用专题用于识别控股股东、实际控制人、董监高、集团内主体和其他特殊关系方之间的异常交易、非经营性资金占用、代垫费用、违规担保、利益输送和披露不完整问题。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 会计资料真实完整 | [[concepts/laws/accounting-law/accounting-law-article-003]], [[concepts/laws/accounting-law/accounting-law-article-004]] | 判断往来、担保、资金拆借和交易背景是否完整入账。 |
| 公司治理和股东查阅 | [[concepts/laws/company-law/company-law-article-057]], [[concepts/laws/company-law/company-law-article-110]] | 获取股东名册、会议记录、财务报告和治理资料。 |
| 上市公司实际控制人信息 | [[concepts/laws/company-law/company-law-article-140]] | 核对实际控制人、共同控制、重大影响和一致行动关系。 |
| 信息披露真实准确完整 | [[concepts/laws/securities-law/securities-law-article-078]], [[concepts/laws/securities-law/securities-law-article-080]] | 判断关联交易、资金占用和担保披露是否充分。 |
| 信息披露违法责任 | [[concepts/laws/securities-law/securities-law-article-197]] | 评估隐瞒关联方、重大遗漏或误导性陈述风险。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 关联方关系识别和披露 | [[concepts/accounting-standards/cas-36]] |
| 合并范围、结构化主体和控制判断 | [[concepts/accounting-standards/cas-33]], [[concepts/first-section-topics/consolidation-scope-control]] |
| 金融工具、往来款和信用风险 | [[concepts/accounting-standards/cas-22]], [[concepts/first-section-topics/financial-instruments-valuation-impairment]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 关联方识别、披露和交易真实性 | [[concepts/audit-standards/csa-1323]] |
| 舞弊风险、管理层凌驾和异常交易 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1211]] |
| 往来款函证、银行流水和外部证据 | [[concepts/audit-standards/csa-1312]], [[concepts/audit-standards/csa-1301]] |
| 关键审计事项和其他信息一致性 | [[concepts/audit-standards/csa-1504]], [[concepts/audit-standards/csa-1521]] |

## 底稿收口

- 将股权结构、董监高名单、工商信息、银行流水、往来明细、合同和担保资料放在同一索引下交叉核验。
- 对大额往来、长期挂账、无商业实质交易、期末集中回款或期后反向流出事项单独形成判断。
- 对上市公司项目，应将关联方清单与公告、年报其他信息、监管问询和函证结果进行一致性检查。
""",
    TOPICS / "asset-impairment.md": """---
title: 资产减值专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [asset-impairment, accounting-estimates, valuation, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/accounting-standards/cas-08]], [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1421]]
---

# 资产减值专题

## 问题定位

资产减值专题覆盖商誉、长期股权投资、固定资产、无形资产、在建工程、使用权资产、存货和金融资产减值。核心问题通常是减值迹象是否完整识别、资产组划分是否合理、可收回金额或可变现净值估计是否可靠。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 实际经济业务核算 | [[concepts/laws/accounting-law/accounting-law-article-009]] | 识别停产、闲置、亏损合同、技术淘汰等真实经营事实。 |
| 会计制度和财务报告 | [[concepts/laws/accounting-law/accounting-law-article-013]], [[concepts/laws/accounting-law/accounting-law-article-020]] | 连接减值准则、估计披露和报表列报。 |
| 公司年度财务报告审计 | [[concepts/laws/company-law/company-law-article-208]] | 判断资产减值对年度报告和审计意见的影响。 |
| 重大风险和信息披露 | [[concepts/laws/securities-law/securities-law-article-080]], [[concepts/laws/securities-law/securities-law-article-082]] | 上市公司减值事项通常需要与经营风险、业绩预告和年报披露一致。 |
| 虚假记载和重大遗漏责任 | [[concepts/laws/securities-law/securities-law-article-197]] | 大额减值计提不足或不当转回可能形成信息披露风险。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 长期资产和商誉减值 | [[concepts/accounting-standards/cas-08]] |
| 存货跌价准备 | [[concepts/accounting-standards/cas-01]] |
| 金融资产预期信用损失 | [[concepts/accounting-standards/cas-22]], [[concepts/first-section-topics/financial-instruments-valuation-impairment]] |
| 列报、重大估计和附注披露 | [[concepts/accounting-standards/cas-30]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 会计估计、模型和管理层偏向 | [[concepts/audit-standards/csa-1321]] |
| 估值专家和关键假设评价 | [[concepts/audit-standards/csa-1421]] |
| 经营证据、外部证据和模型输入 | [[concepts/audit-standards/csa-1301]] |
| 舞弊风险、业绩压力和减值转回 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1211]] |
| 报告意见和关键审计事项 | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1504]] |

## 底稿收口

- 将减值迹象、资产组划分、预测期现金流、折现率、增长率、可比市场数据和敏感性分析串成闭环。
- 对商誉和重大长期资产减值，应保留管理层预算批准、历史预测偏差分析和专家复核记录。
- 对存货和应收款项减值，应同时核对库龄、周转、期后销售或回款、客户信用风险和外部市场信息。
""",
    TOPICS / "profit-distribution-equity-transactions.md": """---
title: 利润分配和权益交易专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [profit-distribution, equity-transactions, presentation, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/law-company]], [[concepts/accounting-standards/cas-30]], [[concepts/accounting-standards/cas-37]]
---

# 利润分配和权益交易专题

## 问题定位

利润分配和权益交易专题覆盖弥补亏损、提取法定公积金、股利分配、资本公积、回购股份、增资减资、可转债和永续债等事项。关键是区分权益交易、损益交易和金融负债，避免把公司法合规问题和会计列报问题割裂。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 公司财务会计制度 | [[concepts/laws/company-law/company-law-article-207]], [[concepts/laws/company-law/company-law-article-208]] | 判断财务报告和利润分配基础。 |
| 利润分配和法定公积金 | [[concepts/laws/company-law/company-law-article-210]], [[concepts/laws/company-law/company-law-article-211]], [[concepts/laws/company-law/company-law-article-212]] | 检查弥补亏损、提取公积、股东会决议和违法分配责任。 |
| 资本公积和公积金用途 | [[concepts/laws/company-law/company-law-article-213]], [[concepts/laws/company-law/company-law-article-214]] | 连接资本公积、转增资本和弥补亏损限制。 |
| 财务资料真实完整 | [[concepts/laws/company-law/company-law-article-216]], [[concepts/laws/accounting-law/accounting-law-article-020]] | 获取股东会决议、分配方案、权益变动和支付证据。 |
| 上市公司信息披露 | [[concepts/laws/securities-law/securities-law-article-080]], [[concepts/laws/securities-law/securities-law-article-197]] | 核对分红、回购、权益工具和重大资本交易披露。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 财务报表列报、所有者权益变动表和附注 | [[concepts/accounting-standards/cas-30]] |
| 金融负债与权益工具区分 | [[concepts/accounting-standards/cas-37]], [[concepts/accounting-standards/cas-22]] |
| 长期股权投资和权益法影响 | [[concepts/accounting-standards/cas-02]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 重大交易、治理程序和权利义务证据 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1151]] |
| 管理层凌驾和不当利润调节 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1211]] |
| 负债权益区分涉及估计或专家判断 | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1421]] |
| 报表列报和其他信息一致性 | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1521]] |

## 底稿收口

- 将董事会或股东会决议、利润分配方案、未分配利润、公积金、支付流水和权益变动表勾稽一致。
- 对违法分配、超额分配、以资本公积弥补亏损、回购股份和特殊权益工具，应单独形成法律和会计双重判断。
- 对可转债、永续债、优先股等工具，应从合同条款出发判断金融负债与权益工具区分，并检查列报披露。
""",
    TOPICS / "income-tax-deferred-tax.md": """---
title: 所得税和递延所得税专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [income-tax, deferred-tax, estimates, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/accounting-standards/cas-18]], [[concepts/audit-standards/csa-1321]]
---

# 所得税和递延所得税专题

## 问题定位

所得税专题关注当期所得税、递延所得税资产和负债、可抵扣亏损、税会差异、税收优惠和不确定税务事项。高风险点通常是递延所得税资产确认是否有足够未来应纳税所得额支撑，以及税务处理是否和经营事实一致。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 会计资料和实际业务 | [[concepts/laws/accounting-law/accounting-law-article-009]], [[concepts/laws/accounting-law/accounting-law-article-013]] | 判断所得税计算基础是否来自真实业务和统一会计制度。 |
| 财务报告编制责任 | [[concepts/laws/accounting-law/accounting-law-article-020]], [[concepts/laws/company-law/company-law-article-208]] | 检查所得税费用、递延所得税和附注披露。 |
| 信息披露责任 | [[concepts/laws/securities-law/securities-law-article-080]], [[concepts/laws/securities-law/securities-law-article-197]] | 上市公司税收优惠、重大税务争议和递延所得税资产确认不足或过度确认的披露风险。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 所得税费用、暂时性差异和递延所得税 | [[concepts/accounting-standards/cas-18]] |
| 财务报表列报和重要估计披露 | [[concepts/accounting-standards/cas-30]] |
| 或有税务事项和税务争议 | [[concepts/accounting-standards/cas-13]], [[concepts/first-section-topics/contingencies-major-litigation]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 递延所得税资产可实现性估计 | [[concepts/audit-standards/csa-1321]] |
| 税务计算证据和外部文件 | [[concepts/audit-standards/csa-1301]] |
| 持续经营、盈利预测和未来应纳税所得额 | [[concepts/first-section-topics/going-concern-uncertainty]], [[concepts/audit-standards/csa-1324]] |
| 关键审计事项和披露充分性 | [[concepts/audit-standards/csa-1504]], [[concepts/audit-standards/csa-1501]] |

## 底稿收口

- 将纳税申报表、税务优惠文件、可抵扣亏损到期表、盈利预测、暂时性差异明细和所得税分录勾稽一致。
- 对递延所得税资产确认，应评价未来盈利预测、历史盈利能力、可执行经营计划和税法限制。
- 对重大税务争议或稽查事项，应同步评价预计负债、或有负债和附注披露。
""",
    TOPICS / "government-grants-special-funds.md": """---
title: 政府补助和专项资金专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [government-grants, special-funds, revenue, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/accounting-standards/cas-16]], [[concepts/audit-standards/csa-1301]]
---

# 政府补助和专项资金专题

## 问题定位

政府补助专题关注补助是否来自政府、是否附带条件、与资产还是收益相关、递延收益摊销是否匹配、专项资金是否按规定使用，以及补助是否具备可收取和合规使用证据。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 实际经济业务核算 | [[concepts/laws/accounting-law/accounting-law-article-009]] | 判断补助入账是否基于真实拨款、批文和履约条件。 |
| 会计资料符合统一制度 | [[concepts/laws/accounting-law/accounting-law-article-013]] | 连接政府补助准则和列报规则。 |
| 财务报告编制和披露 | [[concepts/laws/accounting-law/accounting-law-article-020]], [[concepts/laws/securities-law/securities-law-article-080]] | 检查补助收益、递延收益和附注披露是否完整。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 政府补助确认、计量和列报 | [[concepts/accounting-standards/cas-16]] |
| 收入、其他收益和列报呈现 | [[concepts/accounting-standards/cas-14]], [[concepts/accounting-standards/cas-30]] |
| 或有退回义务和承诺事项 | [[concepts/accounting-standards/cas-13]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 批文、拨款、验收和资金使用证据 | [[concepts/audit-standards/csa-1301]] |
| 管理层舞弊和业绩压力 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1211]] |
| 递延收益摊销和条件满足判断 | [[concepts/audit-standards/csa-1321]] |
| 披露和其他信息一致性 | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1521]] |

## 底稿收口

- 将政府批文、项目申报材料、拨款流水、验收文件、资金使用台账和会计处理勾稽一致。
- 对附条件补助，单独评价条件是否已满足、是否存在退回风险和递延收益摊销基础。
- 对期末集中确认的大额补助，应关注是否存在业绩调节动机和披露不充分风险。
""",
    TOPICS / "contingencies-major-litigation.md": """---
title: 或有事项和重大诉讼专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [contingencies, litigation, provisions, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/accounting-standards/cas-13]], [[concepts/audit-standards/csa-1321]]
---

# 或有事项和重大诉讼专题

## 问题定位

或有事项专题关注未决诉讼、担保、产品质量保证、亏损合同、环境义务、赔偿事项和重大承诺。核心是区分预计负债、或有负债、或有资产和披露事项，并判断金额估计和披露是否充分。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 或有事项财务报告说明 | [[concepts/laws/accounting-law/accounting-law-article-019]], [[concepts/laws/accounting-law/accounting-law-article-020]] | 会计法明确担保、未决诉讼等或有事项应按统一制度在财务报告中说明。 |
| 公司治理和重大事项 | [[concepts/laws/company-law/company-law-article-208]], [[concepts/laws/company-law/company-law-article-216]] | 获取诉讼、担保、承诺和资料提供证据。 |
| 证券重大事项披露 | [[concepts/laws/securities-law/securities-law-article-080]], [[concepts/laws/securities-law/securities-law-article-085]] | 上市公司重大诉讼、担保和风险事项披露。 |
| 虚假记载和重大遗漏责任 | [[concepts/laws/securities-law/securities-law-article-197]] | 重大诉讼或担保披露遗漏的责任风险。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 预计负债、或有负债、或有资产和披露 | [[concepts/accounting-standards/cas-13]] |
| 财务报表列报和附注 | [[concepts/accounting-standards/cas-30]] |
| 持续经营重大不确定性 | [[concepts/first-section-topics/going-concern-uncertainty]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 管理层估计和律师意见评价 | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1301]] |
| 期后事项和报告影响 | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1503]] |
| 其他信息和公告一致性 | [[concepts/audit-standards/csa-1521]] |
| 舞弊风险和隐瞒负债 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1211]] |

## 底稿收口

- 获取诉讼清单、律师函、法院文书、担保合同、董事会决议、期后进展和管理层评估。
- 对预计负债确认，应评价现时义务、经济利益流出可能性和金额可靠估计。
- 对未确认但披露的重大或有事项，应保留不确认理由和披露充分性评价。
""",
    TOPICS / "employee-benefits.md": """---
title: 职工薪酬专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [employee-benefits, payroll, provisions, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/accounting-standards/cas-09]], [[concepts/audit-standards/csa-1301]]
---

# 职工薪酬专题

## 问题定位

职工薪酬专题覆盖短期薪酬、离职后福利、辞退福利、其他长期职工福利、奖金绩效、社保公积金、股份支付交叉事项和人员成本资本化。常见风险是完整性、截止、计提依据和分类列报。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 实际业务和会计资料 | [[concepts/laws/accounting-law/accounting-law-article-009]], [[concepts/laws/accounting-law/accounting-law-article-013]] | 判断薪酬计提、支付和分配是否符合真实用工和统一制度。 |
| 财务报告编制 | [[concepts/laws/accounting-law/accounting-law-article-020]], [[concepts/laws/company-law/company-law-article-208]] | 检查应付职工薪酬、成本费用和附注披露。 |
| 信息披露和重大事项 | [[concepts/laws/securities-law/securities-law-article-080]] | 上市公司高管薪酬、股权激励和重大裁员事项。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 职工薪酬确认、计量和列报 | [[concepts/accounting-standards/cas-09]] |
| 财务报表列报 | [[concepts/accounting-standards/cas-30]] |
| 或有义务、辞退福利和重组计划 | [[concepts/accounting-standards/cas-13]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 薪酬完整性、截止和分配证据 | [[concepts/audit-standards/csa-1301]] |
| 控制测试、审批和信息系统 | [[concepts/audit-standards/csa-1231]] |
| 管理层奖金和舞弊诱因 | [[concepts/audit-standards/csa-1141]], [[concepts/audit-standards/csa-1211]] |
| 披露和其他信息一致性 | [[concepts/audit-standards/csa-1501]], [[concepts/audit-standards/csa-1521]] |

## 底稿收口

- 将人员花名册、劳动合同、薪酬政策、考勤、工资表、社保公积金、银行流水和费用分配表勾稽一致。
- 对奖金、年终奖、辞退福利和长期激励，评价计提依据、批准程序、支付条件和截止。
- 对研发、在建工程、存货等资本化人员成本，应检查分配基础和受益对象。
""",
    TOPICS / "long-term-equity-investments.md": """---
title: 长期股权投资专题
type: concept
concept_type: first-section-topic
created: 2026-06-26
updated: 2026-06-26
sources: [first-section-master-index-2026-06-26]
tags: [long-term-equity-investments, consolidation, equity-method, p1-core]
related: [[concepts/first-section-topic-matrix]], [[concepts/accounting-standards/cas-02]], [[concepts/accounting-standards/cas-33]], [[concepts/audit-standards/csa-1401]]
---

# 长期股权投资专题

## 问题定位

长期股权投资专题关注控制、共同控制、重大影响、成本法、权益法、投资处置、减值和合并报表衔接。它是合并范围、关联方、资产减值和权益交易的交叉口。

## 法律责任入口

| 维度 | 入口 | 用途 |
|---|---|---|
| 公司治理和股东资料 | [[concepts/laws/company-law/company-law-article-057]], [[concepts/laws/company-law/company-law-article-110]] | 获取章程、股东名册、会议记录和投资决策资料。 |
| 年度财务报告审计 | [[concepts/laws/company-law/company-law-article-208]], [[concepts/laws/company-law/company-law-article-216]] | 获取被投资单位财务资料和投资证据。 |
| 上市公司重大投资披露 | [[concepts/laws/securities-law/securities-law-article-080]], [[concepts/laws/securities-law/securities-law-article-085]] | 核对重大投资、并购处置、控制权变化和信息披露。 |

## 会计准则入口

| 判断点 | 入口 |
|---|---|
| 长期股权投资确认、计量、权益法和处置 | [[concepts/accounting-standards/cas-02]] |
| 合并范围和控制判断 | [[concepts/accounting-standards/cas-33]], [[concepts/first-section-topics/consolidation-scope-control]] |
| 长期资产减值 | [[concepts/accounting-standards/cas-08]], [[concepts/first-section-topics/asset-impairment]] |
| 列报和披露 | [[concepts/accounting-standards/cas-30]] |

## 审计程序入口

| 程序问题 | 入口 |
|---|---|
| 控制、共同控制和重大影响证据 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1211]] |
| 集团审计和组成部分工作 | [[concepts/audit-standards/csa-1401]] |
| 关联方关系和特殊安排 | [[concepts/audit-standards/csa-1323]] |
| 投资减值和估值 | [[concepts/audit-standards/csa-1321]], [[concepts/audit-standards/csa-1421]] |

## 底稿收口

- 将投资协议、章程、董事会席位、表决权安排、实际决策记录、被投资单位报表和工商信息交叉核验。
- 对权益法核算，检查被投资单位净利润调整、其他综合收益、利润分配和未实现内部交易抵销。
- 对处置和丧失控制权事项，应同步评价个别报表、合并报表和披露影响。
""",
}


def main() -> None:
    TOPICS.mkdir(parents=True, exist_ok=True)
    for path, text in PAGES.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"topic_pages={len(PAGES)}")


if __name__ == "__main__":
    main()
