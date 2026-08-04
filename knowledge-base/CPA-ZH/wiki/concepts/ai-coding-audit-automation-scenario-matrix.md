---
title: AI 编程与审计自动化场景矩阵
type: concept
concept_type: scenario-matrix
created: 2026-07-09
updated: 2026-07-09
sources: [ai-coding-lectures-archive-2026-07-09]
tags: [ai-coding, automation, audit-practice, scenario-matrix, tools]
related: [[concepts/ai-coding-lectures]], [[concepts/ai-coding-tool-template-library]], [[concepts/ai-coding-risk-control-checklist]], [[concepts/ai-coding-tool-registry]], [[concepts/audit-process]], [[concepts/intelligent-tools]]
domain: tools
topic: ai-coding
---

# AI 编程与审计自动化场景矩阵

本页把第五板块讲义连接到审计、财务和知识库维护场景。使用时先定位业务场景，再选择工具路线，最后回到风险控制清单确认边界。

当前可直接运行的工具和命令见 [[concepts/ai-coding-tool-registry]]。

## 场景总表

| 场景 | 典型任务 | 可用工具模板 | 技术路线 | 人工复核点 |
|---|---|---|---|---|
| 法规准则原文归档 | 下载、复制、留 URL、建 manifest | PDF 原文归档工具、监管规则归档助手 | Python + Agent | 官方来源、版本日期、效力状态 |
| 知识库页面维护 | 来源页、概念页、索引、日志 | 知识库维护助手 | Agent + 固定脚本 | 页面链接、frontmatter、健康检查 |
| 案例加工 | Word/PDF 案例转卡片 | 案例卡片生成助手 | Agent + Python | 事实完整性、准则依据、结论边界 |
| 收入审计 | 明细清洗、异常识别、截止测试 | Excel 底稿清洗工具、数据源核验工具 | Python + Excel | 样本口径、异常规则、凭证追查 |
| 研发费用审计 | 人员、项目、投入明细匹配 | Excel 底稿清洗工具 | Python | 字段映射、资本化/费用化判断、支持性证据 |
| 函证管理 | 发函清单、回函状态、差异跟踪 | Excel 底稿清洗工具、VBA 加载项工具箱 | Python 或 VBA | 回函真实性、替代程序、差异处理 |
| 存货监盘 | 盘点表整理、差异汇总 | Excel 底稿清洗工具 | Python/VBA | 监盘记录、抽盘范围、差异原因 |
| 报告和说明处理 | Word 批量替换、格式统一、清单核对 | Word 报告批量处理工具 | Python | 报告版本、关键段落、签发流程 |
| 底稿格式整理 | ROUND、目录、断链、拆分工作簿 | VBA 加载项工具箱 | VBA | 操作前备份、处理范围、输出复核 |
| 公开数据核验 | 汇率、上市公司财报、外部数据 | 数据源抓取与核验工具 | Python API | 数据来源、日期口径、截图或文件留痕 |

## 审计流程映射

| 审计阶段 | 可自动化事项 | 不宜自动化替代的事项 |
|---|---|---|
| 项目承接 | 资料清单生成、公开信息初筛、客户目录归档 | 独立性判断、承接风险结论 |
| 风险评估 | 明细数据画像、异常波动初筛、访谈纪要整理 | 重大错报风险识别结论 |
| 控制测试 | 样本抽取、测试表生成、例外事项汇总 | 控制设计有效性和运行有效性结论 |
| 实质性程序 | 明细清洗、抽样、函证跟踪、重新计算 | 会计估计合理性、复杂交易判断 |
| 完成阶段 | 调整分录汇总、报告格式检查、底稿索引 | 审计意见类型、关键审计事项判断 |
| 归档阶段 | 文件命名、目录生成、缺失清单 | 归档质量最终复核 |

## 板块联动

| 业务主题 | 应联动页面 |
|---|---|
| 法规准则依据 | [[concepts/regulations-and-standards]], [[concepts/first-section-topic-matrix]] |
| 政策执行和监管要求 | [[concepts/policy-documents]], [[concepts/policy-execution-checklist]] |
| 独立性和职业道德 | [[concepts/history-ethics-independence]], [[concepts/independence-standard-1]] |
| 审计流程和底稿 | [[concepts/audit-process]], [[concepts/audit-practice-operations]] |
| 案例复用 | [[concepts/case-analysis]], [[concepts/case-topic-index]] |

## 场景落地格式

新增自动化场景时，建议按以下格式记录：

1. 业务目标：要减少哪类重复劳动。
2. 输入材料：文件格式、字段、目录、数据来源。
3. 处理逻辑：规则、脚本、模型或人工交互步骤。
4. 输出物：表格、报告、清单、日志或 wiki 页面。
5. 风险边界：哪些步骤必须人工复核。
6. 留痕证据：原始文件、处理日志、结果文件、复核记录。

## 优先落地场景

| 优先级 | 场景 | 原因 |
|---|---|---|
| P1 | 知识库维护和案例加工 | CPA-ZH 当前持续使用，工具收益最直接 |
| P1 | PDF 原文归档和文本抽取 | 法规、政策、准则维护都需要 |
| P2 | Excel 底稿清洗和链接检查 | 审计实务高频，但需结合具体底稿样式 |
| P2 | 研发费用底稿检查 | 已有监管规则和项目底稿场景，可继续沉淀 |
| P3 | Web/桌面产品化 | 等流程稳定后再封装 |
