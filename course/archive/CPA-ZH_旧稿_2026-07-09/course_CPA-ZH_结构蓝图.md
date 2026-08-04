# 【废稿】CPA-ZH 课程结构蓝图

> **废弃说明**：本稿已被推翻，不作为后续课程建设依据。问题在于把“贴合知识库结构”执行成了“学习知识库目录”，没有先抽取实质知识点并分主次。

> 目标：以 CPA-ZH 知识库中的专业知识为课程主体，不按外部通用教材重排；课程结构贴合知识库，但正文必须侧重法律、准则、政策、职业道德、独立性、审计实务和案例知识本身。
>
> 当前依据：`knowledge-base/CPA-ZH/wiki/index.md`、`overview.md`、四个一级板块入口、第一板块完成度页、专题矩阵、政策对照与执行清单、职业道德与独立性页面、实务案例入口。

---

## 一、结构原则

### 1. 课程必须贴合知识库层级

CPA-ZH 的课程体系按知识库现有四条主线展开：

| 知识库主线 | 课程中的位置 | 学习定位 |
|---|---|---|
| 行业重要法规与准则 | 第一门主课 | 执业依据、会计判断和审计程序的基础层 |
| 行业重要政策性文件 | 第二门主课 | 监管导向、事务所治理和项目合规层 |
| 行业史、职业道德与独立性 | 第三门主课 | 承接、执行、签发前的底线判断层 |
| 实务技能与案例分析 | 第四门主课 | 把规则转成底稿、程序、证据和案例复盘 |

知识库的 `sources/`、`raw/indexes/`、版本核验页、校准页和维护页只作为来源追溯和版本复核的辅助内容，不作为正文主线。

### 2. 分主次但不遗漏

| 层级 | 内容类型 | 课程处理方式 |
|---|---|---|
| P1 主干必学 | 一级板块入口、法律概览、准则体系页、职业道德、独立性、审计流程、专题矩阵 | 正文章节精讲 |
| P2 高频重点 | 14 个第一板块实务专题、7 份政策文件、高频会计准则和审计准则、5 个案例 | 专题章节精讲和案例训练 |
| P3 知识颗粒 | 589 条法律条款页、42 个会计准则编号页、20 个解释页、40 个审计准则编号页、其他规定和校准页 | 按主题吸收进正文，保留典型条款、典型准则和典型解释训练 |
| P4 溯源辅助 | `wiki/sources/`、`raw/indexes/`、官方链接、版本效力、检索工具、维护流程 | 放入附录，只服务于依据追溯和版本复核 |

### 3. 每章都要绑定知识库页面

每个课程章节必须列出：

- 对应知识库入口；
- 覆盖的下级页面范围；
- 本章主次级别；
- 需要精读、略读、作为补充知识或作为附录引用的页面；
- 学完后能做什么实务判断。

---

## 二、建议课程体系

### 总课：CPA-ZH 注册会计师执业知识总览

| 章 | 章节名称 | 对应知识库页面 | 层级 |
|---|---|---|---|
| 第0章 | 课程导引 | `wiki/overview.md`, 四个一级板块入口 | P1 |
| 第1章 | 注册会计师执业知识地图 | 四个一级板块入口 | P1 |
| 第2章 | 法律与准则：执业判断的依据层 | 第一板块入口 | P1 |
| 第3章 | 政策与监管：行业治理的方向层 | 第二板块入口 | P1 |
| 第4章 | 职业道德与独立性：能不能做的底线层 | 第三板块入口 | P1 |
| 第5章 | 审计实务与案例：把规则变成证据链 | 第四板块入口 | P1/P2 |
| 第6章 | 综合判断框架：从场景到结论 | 四大板块交叉 | P2 |
| 附录 | 资料来源、索引和版本意识 | `wiki/sources/`, `raw/indexes/` | P4 |

---

## 三、第一门主课：行业重要法规与准则

对应入口：`wiki/concepts/regulations-and-standards.md`

### 课程定位

这是 CPA-ZH 的第一主干课。它回答“注册会计师执业判断的依据在哪里”：法律确定责任边界，会计准则确定确认计量列报披露，审计准则确定程序、证据和报告动作。

### 章节结构

| 章 | 章节名称 | 覆盖范围 | 层级 |
|---|---|---|---|
| 第1章 | 第一板块总览与完成度地图 | `first-section-completion-map.md`, `first-section-master-index` | P1 |
| 第2章 | 四部核心法律的责任边界 | `law-cpa.md`, `law-accounting.md`, `law-company.md`, `law-securities.md` | P1 |
| 第3章 | 四部核心法律的关键条款主题 | 四部法律目录页、589 条条款页、`core-laws-article-index` | P3 |
| 第4章 | 法律责任与审计风险总表 | `first-section-responsibility-risk-map.md`, `core-laws-official-verification.md` | P1 |
| 第5章 | 企业会计准则体系 | `accounting-standards-system.md`, `basic.md`, 42 个 CAS 页面 | P1/P3 |
| 第6章 | 会计准则解释、应用案例、实施问答 | 20 个解释页、应用案例、实施问答、其他规定 | P2/P3 |
| 第7章 | 会计准则补充规则与特殊事项 | 解释、其他规定、校准资料、未映射资料 | P3/P4 |
| 第8章 | 中国注册会计师执业准则体系 | `audit-standards-system.md`, 40 个执业准则页 | P1/P3 |
| 第9章 | 审计准则主题导航 | `audit-standards/topics.md` | P1 |
| 第10章 | 第一板块专题矩阵 | `first-section-topic-matrix.md` 和 14 个专题页 | P1/P2 |
| 第11章 | 综合训练：从实务场景形成专业判断 | 14 个专题页交叉训练 | P2 |

### 第一板块专题矩阵必须覆盖

| 专题 | 课程处理 |
|---|---|
| 收入确认错报风险 | 精讲 |
| 金融工具估值与减值 | 精讲 |
| 合并范围与控制判断 | 精讲 |
| 持续经营与重大不确定性 | 精讲 |
| 关键审计事项 | 精讲 |
| 证券服务责任 | 精讲 |
| 关联方及资金占用 | 精讲 |
| 资产减值 | 精讲 |
| 利润分配和权益交易 | 重点讲 |
| 所得税和递延所得税 | 重点讲 |
| 政府补助和专项资金 | 重点讲 |
| 或有事项和重大诉讼 | 重点讲 |
| 职工薪酬 | 重点讲 |
| 长期股权投资 | 重点讲 |

---

## 四、第二门主课：行业重要政策性文件

对应入口：`wiki/concepts/policy-documents.md`

### 课程定位

本课不以背政策文件名称为目标，而是学习监管逻辑：政策文件说明监管为什么查、查什么、事务所和项目组如何落地。

### 章节结构

| 章 | 章节名称 | 覆盖范围 | 层级 |
|---|---|---|---|
| 第1章 | 第二板块总览：政策文件和法律准则的关系 | `policy-documents.md` | P1 |
| 第2章 | 七份政策文件横向对照 | `policy-document-comparison.md` | P1 |
| 第3章 | 财会监督和审计秩序 | `policy-caihui-supervision.md`, `policy-audit-order.md` | P1 |
| 第4章 | 考试、注册和执业资格 | `policy-cpa-exam.md`, `policy-cpa-registration.md` | P2 |
| 第5章 | 事务所许可、监督检查和诚信建设 | `policy-firm-license-supervision.md`, `policy-firm-inspection.md`, `policy-integrity.md` | P1/P2 |
| 第6章 | 政策落地地图 | `policy-implementation-map.md` | P1 |
| 第7章 | 政策执行检查清单 | `policy-execution-checklist.md` | P1 |
| 第8章 | 官方链接、版本效力和复核触发 | `policy-official-link-checklist.md`, `policy-version-validity-tracker.md` | P4 |

---

## 五、第三门主课：行业史、职业道德与独立性

对应入口：`wiki/concepts/history-ethics-independence.md`

### 课程定位

这是执业底线课，解决“能不能接、能不能做、怎样回避、怎样留痕”的问题。它应当放在审计实务课之前学习。

### 章节结构

| 章 | 章节名称 | 覆盖范围 | 层级 |
|---|---|---|---|
| 第1章 | 第三板块总览 | `history-ethics-independence.md` | P1 |
| 第2章 | 中国注册会计师行业发展基础 | `industry-history.md` | P2 |
| 第3章 | 职业道德守则体系 | `ethics-code.md` 和职业道德守则归档资料 | P1 |
| 第4章 | 职业道德概念框架：识别、评价、应对威胁 | `ethics-code.md` 判断框架 | P1 |
| 第5章 | 独立性准则第1号 | `independence-standard-1.md` | P1 |
| 第6章 | 独立性在承接、项目组、非鉴证服务、收费和签发中的检查 | `independence-standard-1.md`, `policy-execution-checklist.md` | P1 |
| 第7章 | 职业道德与政策、法律、审计流程的交叉 | `policy-integrity.md`, `law-cpa.md`, `audit-process.md` | P2 |
| 第8章 | 官方来源和版本替代关系 | `third-section-official-archive-2026-06-29.md` | P4 |

---

## 六、第四门主课：实务技能与案例分析

对应入口：`wiki/concepts/practice-skills-cases.md`

### 课程定位

本课把前三门课的规则变成实务动作：场景、风险、规则、程序、证据、结论、复盘。

### 章节结构

| 章 | 章节名称 | 覆盖范围 | 层级 |
|---|---|---|---|
| 第1章 | 第四板块总览 | `practice-skills-cases.md` | P1 |
| 第2章 | 审计实务操作总入口 | `audit-practice-operations.md` | P1 |
| 第3章 | 审计计划、底稿、抽样与流程 | `audit-process.md` | P1 |
| 第4章 | 智能化工具与数据处理 | `intelligent-tools.md` | P2 |
| 第5章 | 综合胜任能力 | `comprehensive-competency.md` | P2 |
| 第6章 | 案例分析方法 | `case-analysis.md` | P1 |
| 第7章 | 2026 年 7 月第一期案例组 | `wiki/cases/` 5 个案例页 | P2 |
| 第8章 | 案例来源、导入批次和后续扩展 | `case-batch-2026-07-first-issue.md`, raw case manifest | P4 |

### 已有案例必须覆盖

| 案例 | 课程处理 |
|---|---|
| 长期股权投资确认：同一控制下内部重组中的账面价值结转判断 | 精讲 |
| 暂估转固超过 12 个月的税会差异处理 | 精讲 |
| 免费使用设备是否属于政府补助 | 精讲 |
| 骨科手术导航设备销售的收入确认 | 精讲 |
| 海外销售定制化产品的收入确认 | 精讲 |

---

## 七、附录课：来源、索引和版本复核

对应入口：`wiki/concepts/kb-maintenance-workflow.md`

### 课程定位

这门课作为附录性课程，不教新的专业结论，只帮助学习者理解专业结论为什么需要来源、版本和索引支撑。

### 章节结构

| 章 | 章节名称 | 覆盖范围 | 层级 |
|---|---|---|---|
| 第1章 | CPA-ZH 维护工作流 | `kb-maintenance-workflow.md` | P4 |
| 第2章 | 来源与版本意识 | `wiki/sources/` 22 个来源页 | P4 |
| 第3章 | 索引与证据追溯意识 | `raw/indexes/` 下各 CSV 和 Markdown 索引 | P4 |
| 第4章 | 本地检索作为辅助复核手段 | `tools/kb_search.py`, `search/kb_search.sqlite` | P4 |
| 第5章 | 资料完整性和链接检查意识 | `tools/kb_manifest_audit.py`, `tools/kb_link_check.py` | P4 |
| 第6章 | 版本效力与最新口径复核 | 版本跟踪页、官方链接清单、来源归档页 | P4 |

---

## 八、覆盖矩阵

### 按目录覆盖

| 知识库目录或页面组 | 课程归属 | 覆盖方式 |
|---|---|---|
| `wiki/index.md`, `overview.md` | 总课 | 精讲 |
| `wiki/concepts/regulations-and-standards.md` | 第一门主课 | 精讲 |
| `wiki/concepts/law-*.md` | 第一门主课 | 精讲 |
| `wiki/concepts/laws/**` | 第一门主课 | 按法律主题吸收，典型条款精讲 |
| `wiki/concepts/accounting-standards-system.md` | 第一门主课 | 精讲 |
| `wiki/concepts/accounting-standards/*.md` | 第一门主课 | 高频准则精讲，其余按主题归入知识颗粒 |
| `wiki/concepts/accounting-standards/interpretations/**` | 第一门主课 | 解释体系作为补充规则讲解 |
| `wiki/concepts/accounting-standards/calibration/**` | 第一门附录 | 作为特殊事项和版本复核线索 |
| `wiki/concepts/audit-standards-system.md` | 第一门主课 | 精讲 |
| `wiki/concepts/audit-standards/**` | 第一门主课 | 高频准则精讲，其余按审计主题归入知识颗粒 |
| `wiki/concepts/first-section-topics/**` | 第一门主课 | 专题精讲 |
| `wiki/concepts/policy-*.md` | 第二门主课 | 精讲或重点讲 |
| `wiki/concepts/history-ethics-independence.md` | 第三门主课 | 精讲 |
| `wiki/concepts/ethics-code.md` | 第三门主课 | 精讲 |
| `wiki/concepts/independence-standard-1.md` | 第三门主课 | 精讲 |
| `wiki/concepts/practice-skills-cases.md` | 第四门主课 | 精讲 |
| `wiki/concepts/audit-process.md`, `audit-practice-operations.md` | 第四门主课 | 精讲 |
| `wiki/concepts/intelligent-tools.md`, `comprehensive-competency.md` | 第四门主课 | 重点讲 |
| `wiki/concepts/case-analysis.md` | 第四门主课 | 精讲 |
| `wiki/cases/**` | 第四门主课 | 案例精讲 |
| `wiki/sources/**` | 附录 | 来源追溯和版本意识 |
| `raw/indexes/**` | 附录 | 依据定位和覆盖核验 |
| `raw/**/manifest.json` | 工具课 | 批次归档和完整性核验 |

### 按学习主次覆盖

| 主次 | 必须掌握的能力 |
|---|---|
| P1 | 能说清四大板块结构；能从法律、会计准则、审计准则定位依据；能识别职业道德和独立性底线；能用专题矩阵解决实务问题 |
| P2 | 能处理高频专题、政策落地、实务案例和项目检查清单 |
| P3 | 能理解典型法律条款、准则编号、解释、应用案例、实施问答和审计准则编号页代表的知识颗粒 |
| P4 | 能在必要时追溯来源、核验版本和确认依据可靠性 |

---

## 九、生成正式课程时的章节模板

每个正式章节应采用以下结构：

1. 学习目标；
2. 对应知识库页面；
3. 本章主次级别；
4. 核心内容；
5. 知识来源；
6. 记忆辅助；
7. 常见混淆；
8. 实务任务；
9. 知识检测；
10. 答案与复盘。

其中“对应知识库页面”和“知识来源”是强制项，用来保证课程内容来自 CPA-ZH，而不是外部泛化教材。

---

## 十、下一步建议

建议先生成总课和第一门主课的课程骨架，并优先填充专业知识正文：

- `course/source/course_CPA-ZH_总课.md`
- `course/source/course_CPA-ZH_第一门_行业重要法规与准则.md`

第一批正文优先写：

1. 总课第1章至第6章；
2. 第一门主课第1章至第4章；
3. 第一板块专题矩阵第10章的目录和学习任务。

这样可以先建立全局学习路径，再进入最重的法规、准则和专题内容。
