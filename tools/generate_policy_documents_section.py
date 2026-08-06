from __future__ import annotations

from pathlib import Path

from kb_common import normalize_core_law_article_links, update_frontmatter


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge-base" / "CPA-ZH" / "wiki"
CONCEPTS = WIKI / "concepts"


PAGES: dict[Path, str] = {
    CONCEPTS / "policy-documents.md": """---
title: 行业重要政策性文件
type: concept
concept_type: framework
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure, archived-cpa-competition-policy-pages]
tags: [cpa, policy, supervision, p2-important]
related: [[concepts/policy-caihui-supervision]], [[concepts/policy-audit-order]], [[concepts/policy-cpa-exam]], [[concepts/policy-cpa-registration]], [[concepts/policy-firm-license-supervision]], [[concepts/policy-integrity]], [[concepts/policy-firm-inspection]], [[concepts/policy-document-comparison]], [[concepts/policy-implementation-map]], [[concepts/policy-official-link-checklist]]
---

# 行业重要政策性文件

本板块维护注册会计师行业的重要政策性文件，重点不是背文件名，而是看清政策的治理目标、监管对象、事务所影响和责任边界。

## 文件入口

| 文件 | 文号 | 定位 | 入口 |
|---|---|---|---|
| 关于进一步加强财会监督工作的意见 | 中办发〔2023〕4号 | 财会监督顶层设计 | [[concepts/policy-caihui-supervision]] |
| 关于进一步规范财务审计秩序促进注册会计师行业健康发展的意见 | 国办发〔2021〕30号 | 注册会计师行业治理主线 | [[concepts/policy-audit-order]] |
| 注册会计师全国统一考试办法 | 财政部令第115号 | 考试准入制度 | [[concepts/policy-cpa-exam]] |
| 注册会计师注册办法 | 财政部令第99号 | 执业注册制度 | [[concepts/policy-cpa-registration]] |
| 会计师事务所执业许可和监督管理办法 | 财政部令第97号 | 事务所准入和日常监管 | [[concepts/policy-firm-license-supervision]] |
| 注册会计师行业诚信建设纲要 | 财会〔2023〕5号 | 行业诚信和信用监管 | [[concepts/policy-integrity]] |
| 会计师事务所监督检查办法 | 财办〔2022〕23号 | 监督检查程序和整改处理 | [[concepts/policy-firm-inspection]] |

## 综合维护入口

- [[concepts/policy-document-comparison]] - 七份政策文件横向对照。
- [[concepts/policy-implementation-map]] - 从政策要求到事务所执行的落地地图。
- [[concepts/policy-official-link-checklist]] - 官方来源和链接核验清单。

## 与第一板块的关系

- 法律确定责任边界：[[concepts/law-cpa]], [[concepts/law-accounting]], [[concepts/law-company]], [[concepts/law-securities]]。
- 准则确定执业动作：[[concepts/audit-standards-system]], [[concepts/audit-standards/topics]]。
- 政策确定监管导向：本板块解释为什么要严监管、查什么、怎么整改、如何追责。
""",
    CONCEPTS / "policy-caihui-supervision.md": """---
title: 关于进一步加强财会监督工作的意见
type: concept
concept_type: policy
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure, archived-cpa-competition-policy-pages]
tags: [policy, supervision, caihui-supervision, p2-important]
related: [[concepts/policy-documents]], [[concepts/policy-audit-order]], [[concepts/law-accounting]], [[concepts/first-section-responsibility-risk-map]]
---

# 关于进一步加强财会监督工作的意见

## 基本信息

- 文号：中办发〔2023〕4号
- 定位：财会监督顶层设计文件。
- 官方来源：待联网核验；维护入口见 [[concepts/policy-official-link-checklist]]。

## 政策定位

该意见把财会监督放入党和国家监督体系，强调内部监督、政府监督、社会监督协同。对注册会计师行业而言，会计师事务所审计属于社会监督的重要组成部分，重点承担公共信息质量把关责任。

## 核心要求

| 维度 | 要点 | 执业含义 |
|---|---|---|
| 监督体系 | 内部监督、政府监督、社会监督协同 | 审计不是孤立服务，而是财会监督链条中的社会监督。 |
| 监督重点 | 财经纪律、会计信息质量、中介机构执业质量 | 财务造假和中介失职是重点治理对象。 |
| 监督机制 | 信息共享、线索移送、联合惩戒、整改闭环 | 事务所底稿和结论可能进入跨部门监管链条。 |
| 责任导向 | 压实单位、监管部门、中介机构责任 | 项目执行需能证明勤勉尽责和职业怀疑。 |

## 事务所影响

- 质量管理要服务于“防财务造假、防审计失败、防责任外溢”。
- 项目组应关注监管协同背景下的信息共享和线索移送风险。
- 对上市公司、国有企业、金融企业等高关注主体，应提高风险评估深度。

## 与第一板块连接

| 问题 | 连接 |
|---|---|
| 会计资料真实完整 | [[concepts/law-accounting]], [[concepts/first-section-responsibility-risk-map]] |
| 证券服务机构责任 | [[concepts/law-securities]], [[concepts/first-section-topics/securities-service-liability]] |
| 审计程序和报告责任 | [[concepts/audit-standards-system]], [[concepts/audit-standards/csa-1501]] |
| 行业治理政策衔接 | [[concepts/policy-audit-order]], [[concepts/policy-integrity]] |

## 维护提示

- 本页适合作为“为什么严监管”的政策依据。
- 具体处罚和责任仍应回到法律、部门规章和准则，不宜只引用政策表述。
""",
    CONCEPTS / "policy-audit-order.md": """---
title: 关于进一步规范财务审计秩序促进注册会计师行业健康发展的意见
type: concept
concept_type: policy
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure, archived-cpa-competition-policy-pages]
tags: [policy, audit-order, accounting-firm, p2-important]
related: [[concepts/policy-documents]], [[concepts/policy-caihui-supervision]], [[concepts/policy-firm-license-supervision]], [[concepts/policy-integrity]], [[concepts/policy-firm-inspection]]
---

# 关于进一步规范财务审计秩序促进注册会计师行业健康发展的意见

## 基本信息

- 文号：国办发〔2021〕30号
- 定位：注册会计师行业秩序治理和健康发展主线文件。
- 官方来源：待联网核验；维护入口见 [[concepts/policy-official-link-checklist]]。

## 政策定位

该意见聚焦审计秩序、行业监管、诚信建设和质量提升。它是事务所许可监管、注册管理、诚信建设、监督检查等后续制度的上位政策背景。

## 核心要求

| 维度 | 要点 | 执业含义 |
|---|---|---|
| 整治乱象 | 挂名执业、低价竞争、买卖报告、程序走过场 | 事务所承接和收费不能牺牲审计质量。 |
| 强化监管 | 联合监管、信用监管、信息化监管 | 审计报告、签字注册会计师、事务所质量记录更容易被穿透。 |
| 完善制度 | 注册办法、事务所许可办法、检查办法衔接 | 准入、执业、检查、处罚形成闭环。 |
| 质量提升 | 准则执行、质量管理、人才培养 | 质量管理体系要落到项目执行证据。 |

## 事务所影响

- 客户承接、业务保持、收费安排和项目资源投入需要可解释。
- 审计报告赋码、备案、监管数据报送等信息化要求应纳入所内流程。
- 挂名执业、超胜任能力承接和低价竞争属于高风险治理对象。

## 与第一板块连接

| 问题 | 连接 |
|---|---|
| 注册会计师依法执业 | [[concepts/law-cpa]], [[concepts/audit-standards-system]] |
| 证券服务责任 | [[concepts/law-securities]], [[concepts/first-section-topics/securities-service-liability]] |
| 事务所监督检查 | [[concepts/policy-firm-inspection]], [[concepts/policy-firm-license-supervision]] |
| 行业诚信约束 | [[concepts/policy-integrity]], [[concepts/ethics-code]] |

## 维护提示

- 本页适合作为“行业治理为什么强化”的主线入口。
- 具体执法依据要与 [[concepts/policy-firm-inspection]]、[[concepts/policy-firm-license-supervision]] 和法律责任页面联合使用。
""",
    CONCEPTS / "policy-cpa-exam.md": """---
title: 注册会计师全国统一考试办法
type: concept
concept_type: policy
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure, archived-cpa-competition-policy-pages]
tags: [policy, exam, cpa, p2-important]
related: [[concepts/policy-documents]], [[concepts/policy-cpa-registration]], [[concepts/law-cpa]]
---

# 注册会计师全国统一考试办法

## 基本信息

- 文号：财政部令第115号
- 定位：注册会计师考试准入制度。
- 官方来源：待联网核验；维护入口见 [[concepts/policy-official-link-checklist]]。

## 政策定位

该办法承接 [[concepts/laws/cpa-law/cpa-law-article-009]] 的统一考试制度，解决“如何考试、谁组织、成绩如何管理、违规如何处理”的问题。考试合格并不等于执业注册，还需满足注册条件。

## 核心要求

| 维度 | 要点 | 管理含义 |
|---|---|---|
| 考试组织 | 财政部考委会、中注协、地方考办 | 明确考试组织责任。 |
| 报名条件 | 学历或相关职称条件 | 是考试准入，不是执业准入。 |
| 考试阶段 | 专业阶段和综合阶段 | 专业能力到综合职业能力递进。 |
| 成绩管理 | 专业阶段单科成绩滚动有效 | 与人才培养和备考周期相关。 |
| 违规处理 | 对考试违规作出处理 | 体现行业准入诚信要求。 |

## 与注册管理连接

- 考试办法解决“能否取得考试合格资格”。
- [[concepts/policy-cpa-registration]] 解决“能否注册成为执业注册会计师”。
- [[concepts/law-cpa]] 是上位法基础。

## 维护提示

- 本页主要服务行业准入和人才培养，不直接作为项目审计程序依据。
- 与诚信建设联动时，可关注考试违规、诚信档案和职业准入约束。
""",
    CONCEPTS / "policy-cpa-registration.md": """---
title: 注册会计师注册办法
type: concept
concept_type: policy
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure, archived-cpa-competition-policy-pages]
tags: [policy, registration, cpa, p2-important]
related: [[concepts/policy-documents]], [[concepts/law-cpa]], [[concepts/policy-cpa-exam]], [[concepts/policy-integrity]]
---

# 注册会计师注册办法

## 基本信息

- 文号：财政部令第99号
- 定位：注册会计师执业注册管理制度。
- 官方来源：待联网核验；维护入口见 [[concepts/policy-official-link-checklist]]。

## 政策定位

注册办法承接 [[concepts/law-cpa]] 中考试、注册、撤销注册等制度，解决考试合格人员如何成为执业注册会计师，以及注册后如何持续管理的问题。

## 核心要求

| 维度 | 要点 | 管理含义 |
|---|---|---|
| 注册条件 | 考试合格、审计业务经历等 | 区分考试合格和执业注册。 |
| 不予注册 | 民事能力、处罚、处分、吊销等情形 | 职业准入和诚信约束。 |
| 撤销/注销 | 注册后不符合条件或发生特定事项 | 动态管理执业资格。 |
| 协会管理 | 注册、备案、年检或持续监管 | 行业自律和财政监管衔接。 |

## 事务所影响

- 项目签字人员必须具备适当执业资格和胜任能力。
- 挂名执业、资格异常、注册信息不实会放大事务所质量管理风险。
- 人员注册状态应纳入承接、签字和质量控制流程。

## 与第一板块连接

| 问题 | 连接 |
|---|---|
| 上位法律依据 | [[concepts/law-cpa]], [[concepts/laws/cpa-law/cpa-law-article-011]] |
| 考试制度 | [[concepts/policy-cpa-exam]] |
| 诚信和职业道德 | [[concepts/policy-integrity]], [[concepts/ethics-code]] |
| 事务所质量管理 | [[concepts/policy-audit-order]], [[concepts/policy-firm-license-supervision]] |
""",
    CONCEPTS / "policy-firm-license-supervision.md": """---
title: 会计师事务所执业许可和监督管理办法
type: concept
concept_type: policy
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure, archived-cpa-competition-policy-pages]
tags: [policy, accounting-firm, license, supervision, p2-important]
related: [[concepts/policy-documents]], [[concepts/law-cpa]], [[concepts/policy-audit-order]], [[concepts/policy-firm-inspection]]
---

# 会计师事务所执业许可和监督管理办法

## 基本信息

- 文号：财政部令第97号
- 定位：会计师事务所准入、变更、备案和日常监督管理制度。
- 官方来源：待联网核验；维护入口见 [[concepts/policy-official-link-checklist]]。

## 政策定位

该办法是事务所“能不能设、怎么设、如何变更、如何监管”的基础制度。它与 [[concepts/law-cpa]] 的事务所设立规则、[[concepts/policy-firm-inspection]] 的监督检查程序、[[concepts/policy-integrity]] 的信用约束共同构成事务所监管框架。

## 核心要求

| 维度 | 要点 | 事务所影响 |
|---|---|---|
| 执业许可 | 合伙人/股东、注册会计师人数、组织形式等 | 准入条件和持续合规。 |
| 变更备案 | 名称、合伙人、股东、分所等事项 | 重大组织变化需及时办理。 |
| 日常监管 | 财政部门监管、信息报送、执业质量关注 | 质量管理和信息透明度要求提升。 |
| 处理处罚 | 不符合条件、违规执业、资料不实 | 与信用记录和监督检查衔接。 |

## 实务连接

| 问题 | 连接 |
|---|---|
| 事务所设立上位法 | [[concepts/law-cpa]], [[concepts/laws/cpa-law/cpa-law-article-027]] |
| 行业秩序治理 | [[concepts/policy-audit-order]] |
| 监督检查程序 | [[concepts/policy-firm-inspection]] |
| 诚信和信用约束 | [[concepts/policy-integrity]] |

## 维护提示

- 本页适合放入事务所治理、质量管理和监管合规的知识链。
- 具体条文引用前应核对财政部规章最新有效版本。
""",
    CONCEPTS / "policy-integrity.md": """---
title: 注册会计师行业诚信建设纲要
type: concept
concept_type: policy
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure, archived-cpa-competition-policy-pages]
tags: [policy, integrity, ethics, p2-important]
related: [[concepts/policy-documents]], [[concepts/ethics-code]], [[concepts/independence-standard-1]], [[concepts/policy-audit-order]]
---

# 注册会计师行业诚信建设纲要

## 基本信息

- 文号：财会〔2023〕5号
- 定位：注册会计师行业诚信体系和信用监管建设文件。
- 官方来源：待联网核验；维护入口见 [[concepts/policy-official-link-checklist]]。

## 政策定位

诚信建设纲要把诚信作为行业治理基础，强调诚信档案、信用约束、失信惩戒、诚信文化和数字化监管。它与职业道德守则、独立性准则和事务所质量管理共同支撑行业信任。

## 核心要求

| 维度 | 要点 | 执业含义 |
|---|---|---|
| 诚信档案 | 记录事务所和从业人员诚信信息 | 执业记录会影响职业声誉和监管评价。 |
| 信用约束 | 对失信行为实施约束和惩戒 | 处罚、检查、投诉等事项可能形成长期影响。 |
| 诚信文化 | 把诚信嵌入事务所治理和人员管理 | 不能只靠事后处罚，要前置到质量管理。 |
| 协同监管 | 与财政监管、协会自律、市场信用体系衔接 | 行业信息可能跨部门共享。 |

## 与职业道德连接

- [[concepts/ethics-code]] 解决注册会计师应当如何保持诚信、客观和专业胜任能力。
- [[concepts/independence-standard-1]] 解决审计和审阅业务的独立性要求。
- 本页更偏行业治理和信用监管。

## 与第一板块连接

| 问题 | 连接 |
|---|---|
| 禁止行为和独立性 | [[concepts/law-cpa]], [[concepts/laws/cpa-law/cpa-law-article-024]] |
| 证券服务责任 | [[concepts/law-securities]], [[concepts/first-section-topics/securities-service-liability]] |
| 审计质量和报告责任 | [[concepts/audit-standards-system]], [[concepts/audit-standards/csa-1501]] |
""",
    CONCEPTS / "policy-firm-inspection.md": """---
title: 会计师事务所监督检查办法
type: concept
concept_type: policy
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure, archived-cpa-competition-policy-pages]
tags: [policy, inspection, accounting-firm, p2-important]
related: [[concepts/policy-documents]], [[concepts/policy-firm-license-supervision]], [[concepts/policy-audit-order]], [[concepts/first-section-responsibility-risk-map]]
---

# 会计师事务所监督检查办法

## 基本信息

- 文号：财办〔2022〕23号
- 定位：会计师事务所监督检查程序、整改和处理的操作性制度。
- 官方来源：待联网核验；维护入口见 [[concepts/policy-official-link-checklist]]。

## 政策定位

监督检查办法解决“怎么查、查什么、发现问题后怎么处理”的问题。它把事务所执业质量、质量管理体系、注册会计师执业行为和整改责任纳入监督检查闭环。

## 核心要求

| 维度 | 要点 | 事务所影响 |
|---|---|---|
| 检查计划 | 财政部门组织检查 | 事务所应持续保持资料和质量管理可检查状态。 |
| 检查内容 | 执业质量、质量管理、独立性、人员管理等 | 底稿不是唯一检查对象，所级体系也会被检查。 |
| 检查程序 | 通知、进场、取证、沟通、结论 | 需要完整提供资料并配合说明。 |
| 整改处理 | 整改、约谈、处罚、移送、信用记录 | 检查发现事项会进入后续监管链条。 |

## 与第一板块连接

| 问题 | 连接 |
|---|---|
| 事务所准入和监管 | [[concepts/policy-firm-license-supervision]] |
| 注册会计师依法执业 | [[concepts/law-cpa]], [[concepts/audit-standards-system]] |
| 证券服务责任和重大错报风险 | [[concepts/law-securities]], [[concepts/first-section-responsibility-risk-map]] |
| 审计底稿和证据 | [[concepts/audit-standards/csa-1301]], [[concepts/audit-standards/csa-1501]] |

## 维护提示

- 本页适合作为监管检查和整改场景的入口。
- 对具体检查发现，后续可接入第四板块案例库或监管处罚案例页。
""",
    CONCEPTS / "policy-document-comparison.md": """---
title: 第二板块政策文件对照表
type: concept
concept_type: comparison
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure, archived-cpa-competition-policy-pages]
tags: [policy, comparison, p2-important]
related: [[concepts/policy-documents]], [[concepts/policy-implementation-map]], [[concepts/policy-official-link-checklist]]
---

# 第二板块政策文件对照表

## 总体对照

| 文件 | 层级/性质 | 主要对象 | 核心问题 | 关联页面 |
|---|---|---|---|---|
| 关于进一步加强财会监督工作的意见 | 顶层政策 | 财会监督体系、单位、监管部门、中介机构 | 财会监督协同和严监管 | [[concepts/policy-caihui-supervision]] |
| 关于进一步规范财务审计秩序促进注册会计师行业健康发展的意见 | 国办政策 | 注册会计师行业、事务所、监管部门 | 审计秩序和行业治理 | [[concepts/policy-audit-order]] |
| 注册会计师全国统一考试办法 | 部门规章 | 考生、考试组织机构 | 考试准入 | [[concepts/policy-cpa-exam]] |
| 注册会计师注册办法 | 部门规章 | 注册申请人、注册会计师、协会 | 执业注册和资格管理 | [[concepts/policy-cpa-registration]] |
| 会计师事务所执业许可和监督管理办法 | 部门规章 | 会计师事务所及分所 | 准入、变更、日常监管 | [[concepts/policy-firm-license-supervision]] |
| 注册会计师行业诚信建设纲要 | 行业治理文件 | 事务所、注册会计师、行业组织 | 诚信档案和信用监管 | [[concepts/policy-integrity]] |
| 会计师事务所监督检查办法 | 监管操作文件 | 财政部门、事务所、注册会计师 | 检查程序、整改、处理 | [[concepts/policy-firm-inspection]] |

## 高频区分

| 比较项 | 容易混淆点 | 正确区分 |
|---|---|---|
| 财会监督意见 vs 审计秩序意见 | 都谈监管 | 前者是财会监督体系顶层设计，后者聚焦注册会计师行业秩序。 |
| 考试办法 vs 注册办法 | 都与成为注册会计师有关 | 考试办法管考试合格，注册办法管执业注册。 |
| 事务所许可办法 vs 监督检查办法 | 都涉及事务所监管 | 许可办法重准入和日常监管，检查办法重检查程序和整改处理。 |
| 诚信建设纲要 vs 职业道德守则 | 都讲诚信 | 纲要偏行业信用治理，守则偏职业行为规范。 |
| 政策文件 vs 法律法规 | 都能影响执业 | 法律确定责任边界，政策体现治理重点和监管方向。 |

## 使用建议

- 做监管分析时，先用本页定位政策文件，再回到第一板块法律和准则。
- 做事务所治理时，重点串联 [[concepts/policy-audit-order]], [[concepts/policy-firm-license-supervision]], [[concepts/policy-firm-inspection]], [[concepts/policy-integrity]]。
""",
    CONCEPTS / "policy-implementation-map.md": """---
title: 第二板块政策落地地图
type: concept
concept_type: implementation-map
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure, archived-cpa-competition-policy-pages]
tags: [policy, implementation, accounting-firm, p2-important]
related: [[concepts/policy-documents]], [[concepts/policy-document-comparison]], [[concepts/first-section-responsibility-risk-map]]
---

# 第二板块政策落地地图

本页把政策要求翻译成事务所和项目层面的维护动作。

## 落地矩阵

| 政策要求 | 事务所动作 | 项目动作 | 关联页面 |
|---|---|---|---|
| 财会监督协同 | 建立监管信息、处罚案例、整改事项跟踪机制 | 重大风险事项及时升级沟通 | [[concepts/policy-caihui-supervision]] |
| 规范审计秩序 | 管控低价竞争、挂名执业、超能力承接 | 承接保持和资源配置留痕 | [[concepts/policy-audit-order]] |
| 注册和资格管理 | 定期核对注册状态、签字资格、继续教育 | 项目组胜任能力评价 | [[concepts/policy-cpa-registration]] |
| 事务所许可和变更 | 维护执业许可、分所、合伙人/股东变更合规 | 重大组织变化影响项目时及时沟通 | [[concepts/policy-firm-license-supervision]] |
| 诚信建设 | 维护诚信档案、投诉处罚和整改记录 | 识别独立性、诚信和职业道德风险 | [[concepts/policy-integrity]] |
| 监督检查 | 保持质量管理、底稿、独立性和人员资料可检查 | 项目底稿形成风险-程序-证据-结论闭环 | [[concepts/policy-firm-inspection]] |

## 与第一板块的衔接

- 责任边界：[[concepts/first-section-responsibility-risk-map]]
- 证券服务责任：[[concepts/first-section-topics/securities-service-liability]]
- 审计程序总入口：[[concepts/audit-standards/topics]]
- 法律版本核验：[[concepts/core-laws-official-verification]]

## 维护提示

- 本页适合后续接入事务所质量管理制度、监管处罚案例和整改清单。
- 若后续进入第四板块案例库，可把每类政策要求映射到处罚案例和底稿缺陷类型。
""",
    CONCEPTS / "policy-official-link-checklist.md": """---
title: 第二板块官方链接核验清单
type: concept
concept_type: verification-map
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure]
tags: [policy, official-links, verification, p2-important]
related: [[concepts/policy-documents]], [[concepts/policy-document-comparison]]
---

# 第二板块官方链接核验清单

本页记录第二板块政策文件的官方来源维护状态。当前网络访问受限时，先保留“待核验”状态，不硬写未确认链接。

## 核验清单

| 文件 | 文号 | 预期官方来源 | 状态 |
|---|---|---|---|
| [[concepts/policy-caihui-supervision]] | 中办发〔2023〕4号 | 中国政府网、财政部等权威转载 | 待核验 |
| [[concepts/policy-audit-order]] | 国办发〔2021〕30号 | 中国政府网 | 待核验 |
| [[concepts/policy-cpa-exam]] | 财政部令第115号 | 财政部官网部门规章栏目 | 待核验 |
| [[concepts/policy-cpa-registration]] | 财政部令第99号 | 财政部官网部门规章栏目 | 待核验 |
| [[concepts/policy-firm-license-supervision]] | 财政部令第97号 | 财政部官网部门规章栏目 | 待核验 |
| [[concepts/policy-integrity]] | 财会〔2023〕5号 | 财政部、中注协相关栏目 | 待核验 |
| [[concepts/policy-firm-inspection]] | 财办〔2022〕23号 | 财政部相关通知栏目 | 待核验 |

## 核验流程

1. 优先使用中国政府网、财政部官网、中国注册会计师协会官网。
2. 记录标题、文号、发布日期、施行日期或印发日期、URL 和本地保存路径。
3. 若发现文件修订或废止，更新对应政策页的“基本信息”和本清单状态。
4. 每次核验后更新 [[concepts/policy-documents]] 和 [[concepts/policy-document-comparison]]。

## 暂不处理

- 非官方转载链接不作为最终依据。
- 搜索引擎摘要不作为有效来源。
""",
}


POLICY_METADATA: dict[Path, dict[str, object]] = {
    CONCEPTS / "policy-audit-order.md": {
        "asset_id": "cpa-zh:policy:audit-order-2021-30",
        "source_id": "policy-audit-order-2021-30",
        "knowledge_type": "policy",
        "page_role": "knowledge",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "version": "国办发〔2021〕30号",
        "published_on": "2021-07-30",
        "effective_from": "unknown",
        "lifecycle_status": "unknown",
        "authority_level": "official",
        "raw_path": "raw/policies/second-section/audit-order-2021-30/official.html.md",
        "markdown_path": "wiki/concepts/policy-audit-order.md",
        "source_url": "https://www.gov.cn/zhengce/content/2021-08/23/content_5632714.htm",
        "content_sha256": "2e83953cae99b8366155c20fd52454ec47172de327c27080c4e1cf226c989409",
    },
    CONCEPTS / "policy-caihui-supervision.md": {
        "asset_id": "cpa-zh:policy:caihui-supervision-2023-4",
        "source_id": "policy-caihui-supervision-2023-4",
        "knowledge_type": "policy",
        "page_role": "knowledge",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "version": "中办发〔2023〕4号",
        "published_on": "2023-02-15",
        "effective_from": "unknown",
        "lifecycle_status": "unknown",
        "authority_level": "official",
        "raw_path": "raw/policies/second-section/caihui-supervision-2023-4/official.html.md",
        "markdown_path": "wiki/concepts/policy-caihui-supervision.md",
        "source_url": "https://www.gov.cn/zhengce/2023-02/15/content_5741628.htm",
        "content_sha256": "edba2cc9532ac41c324308e11fd9f1a6d73e4d5fa723b611317981b201557ca5",
    },
    CONCEPTS / "policy-cpa-exam.md": {
        "asset_id": "cpa-zh:policy:cpa-exam-2024-115",
        "source_id": "policy-cpa-exam-2024-115",
        "knowledge_type": "policy",
        "page_role": "knowledge",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "version": "财政部令第115号",
        "published_on": "2024-01-23",
        "effective_from": "2024-03-01",
        "lifecycle_status": "unknown",
        "authority_level": "official",
        "raw_path": "raw/policies/second-section/cpa-exam-2024-115/official.html.md",
        "markdown_path": "wiki/concepts/policy-cpa-exam.md",
        "source_url": "https://www.gov.cn/gongbao/2024/issue_11286/202404/content_6945588.html",
        "content_sha256": "23b0a578b1f15c4f2e726fc32c6b97145e34866365caab7207bd9b1a56aa5180",
        "supersedes": "财政部令第75号修改版本",
    },
    CONCEPTS / "policy-cpa-registration.md": {
        "asset_id": "cpa-zh:policy:cpa-registration-2019-99",
        "source_id": "policy-cpa-registration-2019-99",
        "knowledge_type": "policy",
        "page_role": "knowledge",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "version": "财政部令第99号修改版本",
        "published_on": "2019-03-15",
        "effective_from": "2019-03-15",
        "lifecycle_status": "unknown",
        "authority_level": "official",
        "raw_path": "raw/policies/second-section/cpa-registration-2019-99/official.html.md",
        "markdown_path": "wiki/concepts/policy-cpa-registration.md",
        "source_url": "https://www.mof.gov.cn/gkml/caizhengwengao/wg201901/wg201912/202005/t20200522_3518260.htm",
        "content_sha256": "7a3f8a6d74e5018aec4abc41a3605cc7c89324b7ea5f8b6f5b4ca90e1b88d02d",
        "supersedes": "财政部令第25号经2017年第一次修改版本",
    },
    CONCEPTS / "policy-firm-inspection.md": {
        "asset_id": "cpa-zh:policy:firm-inspection-2022-23",
        "source_id": "policy-firm-inspection-2022-23",
        "knowledge_type": "policy",
        "page_role": "knowledge",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "version": "财办〔2022〕23号",
        "published_on": "unknown",
        "effective_from": "unknown",
        "lifecycle_status": "unknown",
        "authority_level": "official",
        "raw_path": "raw/policies/second-section/firm-inspection-2022-23/official.html.md",
        "markdown_path": "wiki/concepts/policy-firm-inspection.md",
        "source_url": "https://www.gov.cn/zhengce/zhengceku/2022-05/16/content_5690682.htm",
        "content_sha256": "43bf065427d8c38b71c6a4580a7a3b8d69c952d81ec4a2f6210efe6dae0144e9",
    },
    CONCEPTS / "policy-firm-license-supervision.md": {
        "asset_id": "cpa-zh:policy:firm-license-supervision-2019-97",
        "source_id": "policy-firm-license-supervision-2019-97",
        "knowledge_type": "policy",
        "page_role": "knowledge",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "version": "财政部令第97号修改版本",
        "published_on": "2019-01-02",
        "effective_from": "2019-01-02",
        "lifecycle_status": "unknown",
        "authority_level": "official",
        "raw_path": "raw/policies/second-section/firm-license-supervision-2019-97/official.html.md",
        "markdown_path": "wiki/concepts/policy-firm-license-supervision.md",
        "source_url": "https://www.gov.cn/gongbao/content/2019/content_5392297.htm",
        "content_sha256": "e5b2056d3d8ed66b9242dd2eb7e28f319529581d65f00b28de0ddf693c818029",
        "supersedes": "财政部令第89号公布版本",
    },
    CONCEPTS / "policy-integrity.md": {
        "asset_id": "cpa-zh:policy:integrity-2023-5",
        "source_id": "policy-integrity-2023-5",
        "knowledge_type": "policy",
        "page_role": "knowledge",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
        "version": "财会〔2023〕5号",
        "published_on": "unknown",
        "effective_from": "unknown",
        "lifecycle_status": "unknown",
        "authority_level": "official",
        "raw_path": "raw/policies/second-section/integrity-2023-5/official.html.md",
        "markdown_path": "wiki/concepts/policy-integrity.md",
        "source_url": "https://www.gov.cn/zhengce/zhengceku/2023-04/02/content_5749779.htm",
        "content_sha256": "8a8529c7395d3fdb47b188a82e22abc393b7316998f85f7a459b785b2e2a2e5c",
    },
}


SUPPORTING_METADATA: dict[Path, dict[str, object]] = {
    CONCEPTS / "policy-document-comparison.md": {
        "asset_id": "cpa-zh:index:policy-document-comparison",
        "knowledge_type": "index",
        "page_role": "index",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
    },
    CONCEPTS / "policy-documents.md": {
        "asset_id": "cpa-zh:index:policy-documents",
        "knowledge_type": "index",
        "page_role": "index",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
    },
    CONCEPTS / "policy-execution-checklist.md": {
        "asset_id": "cpa-zh:index:policy-execution-checklist",
        "knowledge_type": "index",
        "page_role": "index",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
    },
    CONCEPTS / "policy-implementation-map.md": {
        "asset_id": "cpa-zh:index:policy-implementation-map",
        "knowledge_type": "index",
        "page_role": "index",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
    },
    CONCEPTS / "policy-official-link-checklist.md": {
        "asset_id": "cpa-zh:index:policy-official-link-checklist",
        "knowledge_type": "index",
        "page_role": "index",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
    },
    CONCEPTS / "policy-version-validity-tracker.md": {
        "asset_id": "cpa-zh:index:policy-version-validity-tracker",
        "knowledge_type": "index",
        "page_role": "index",
        "maturity": "reviewed",
        "answer_ready": False,
        "review_status": "agent-reviewed",
        "updated": "2026-08-06",
    },
}


def main() -> None:
    metadata_by_path = {**POLICY_METADATA, **SUPPORTING_METADATA}
    for path in sorted(set(PAGES) | set(metadata_by_path), key=lambda item: item.as_posix()):
        fallback = PAGES.get(path)
        if path.exists():
            current = path.read_text(encoding="utf-8-sig")
        elif fallback is not None:
            current = fallback
        else:
            raise FileNotFoundError(f"Missing editorial policy page: {path}")
        normalized, _ = normalize_core_law_article_links(current)
        metadata = metadata_by_path.get(path)
        if metadata:
            normalized = update_frontmatter(normalized, metadata)
        path.write_text(normalized.strip() + "\n", encoding="utf-8")
    print(f"policy_pages={len(PAGES)}")
    print(f"governed_pages={len(metadata_by_path)}")


if __name__ == "__main__":
    main()
