---
title: AI 编程与自动化工具模板库
type: concept
concept_type: tool-template-library
created: 2026-07-09
updated: 2026-07-09
sources: [ai-coding-lectures-archive-2026-07-09]
tags: [ai-coding, automation, tool-template, audit-tools, python, vba, agent]
related: [[concepts/ai-coding-lectures]], [[concepts/ai-coding-audit-automation-scenario-matrix]], [[concepts/ai-coding-risk-control-checklist]], [[concepts/ai-coding-tool-registry]], [[concepts/intelligent-tools]]
domain: tools
topic: ai-coding
---

# AI 编程与自动化工具模板库

本页把第五板块讲义提炼为可复用工具模板。它不是代码仓库，而是工具设计入口：每个模板都说明适用场景、输入输出、优先技术路线、控制点和后续落地位置。

## 模板总表

| 模板 | 适用场景 | 输入 | 输出 | 优先路线 | 讲义入口 |
|---|---|---|---|---|---|
| PDF 原文归档工具 | 法规、准则、政策、底稿附件归档 | PDF、HTML、URL、本地目录 | raw 归档目录、metadata、source-url、manifest | Python | [[concepts/cpa-zh-archive-doc-helper]], [[concepts/ai-coding-python-lectures]] |
| PDF 转 Markdown 工具 | PDF 正文进入知识库检索，扫描件列入 OCR 待办 | PDF、OCR/解析配置 | Markdown、转换 manifest、OCR 待处理清单 | Python + 文档解析 API | [[_maintenance/cpa-zh-pdf-to-markdown-helper]], [[concepts/ai-coding-python-lectures]] |
| Excel 底稿清洗工具 | 明细表、抽样表、底稿索引表标准化 | Excel 工作簿、字段规则 | 清洗后工作簿、问题清单、处理日志 | Python 或 VBA | [[concepts/ai-coding-python-lectures]], [[concepts/ai-coding-vba-addin-lectures]] |
| Excel 链接与公式检查工具 | 底稿外链、公式、手输数排查 | Excel 工作簿 | 外链清单、公式异常、手输数区域 | VBA 优先，Python 辅助 | [[concepts/ai-coding-vba-addin-lectures]] |
| Word 报告批量处理工具 | 审计报告、说明、复核意见统一处理 | Word 文件、模板规则 | 标准化 Word、差异清单 | Python | [[concepts/ai-coding-python-lectures]] |
| 案例卡片生成助手 | 实务案例批量加工 | Word/PDF/Markdown 案例原文 | wiki/cases 案例卡片草稿 | Agent + Python | [[concepts/cpa-zh-case-card-helper]], [[concepts/ai-coding-agent-lectures]], [[concepts/ai-coding-python-lectures]] |
| 案例主题索引回挂助手 | 新增案例后维护主题索引 | wiki/cases 案例卡片 | 主题、准则、风险、底稿用途回挂建议 | Python + 规则建议 | [[concepts/cpa-zh-case-index-helper]], [[concepts/case-topic-index]] |
| 本地问答日志回写助手 | 把有价值问答沉淀为知识页 | 问题、回答、标签、关联页面 | wiki/questions 问答页草稿 | Agent + Python | [[concepts/cpa-zh-qa-capture-helper]], [[concepts/kb-maintenance-workflow]] |
| 知识库维护助手 | 新来源入库、索引、体检、README 刷新 | raw 新资料、manifest | wiki 来源页、概念页、健康检查结果 | Agent + 固定脚本 | [[concepts/cpa-zh-local-ingest-helper]], [[concepts/ai-coding-agent-lectures]] |
| 监管规则归档助手 | 证监会、财政部、中注协网页归档 | 官方 URL、本地下载文件 | official.html/PDF、来源说明、状态看板 | Python + Agent | [[concepts/ai-coding-agent-lectures]], [[concepts/ai-coding-python-lectures]] |
| 数据源抓取与核验工具 | 汇率、上市公司报表、公开数据核验 | API 参数、查询口径 | 结构化数据、来源记录 | Python API | [[concepts/ai-coding-python-lectures]] |
| VBA 加载项工具箱 | 高频 Excel 底稿动作按钮化 | 当前工作簿、用户参数 | 处理后的工作簿、操作结果 | VBA | [[concepts/ai-coding-vba-addin-lectures]] |

## 工具模板结构

每个工具后续落地时，建议统一按以下结构建页或建 README：

| 字段 | 要求 |
|---|---|
| 工具名称 | 用业务动作命名，不用技术名堆叠 |
| 适用场景 | 明确对应哪类审计、财务或知识库任务 |
| 输入要求 | 文件格式、字段、目录结构、参数配置 |
| 输出结果 | 文件、表格、日志、wiki 页面或异常清单 |
| 技术路线 | Python、VBA、Agent、API、GUI、Web 的选择依据 |
| 控制点 | 输入校验、人工确认、异常处理、输出复核 |
| 留痕要求 | 原始文件、处理日志、版本号、执行时间、操作者 |
| 禁止边界 | 不允许自动覆盖原文、不允许跳过人工判断、不允许直接改结论 |

## Python 模板优先场景

| 场景 | 选择 Python 的原因 |
|---|---|
| 批量文件处理 | 适合目录遍历、文件复制、哈希、manifest、批量转换 |
| PDF/Word/HTML 解析 | 生态更完整，便于接入解析库和 API |
| 数据清洗和结构化 | 适合字段映射、异常规则、批量表格输出 |
| GUI 或 Web 工具 | 适合把脚本封装为桌面或网页小工具 |
| 可测试工具 | 适合建立单元测试、命令行参数和日志 |

## VBA 模板优先场景

| 场景 | 选择 VBA 的原因 |
|---|---|
| 当前 Excel 工作簿内操作 | 审计人员直接在底稿中点击按钮完成 |
| 格式、公式、链接处理 | Excel 原生对象模型更直接 |
| 轻量分发 | 加载项可在团队内通过按钮菜单使用 |
| 人机交互简单 | 输入框、复选框、下拉框足够承载 |

## Agent 模板优先场景

| 场景 | 选择 Agent 的原因 |
|---|---|
| 多步骤知识加工 | 需要读原文、提炼结构、回写 wiki、更新索引 |
| 页面核验和人工判断辅助 | 需要浏览页面、比对标题、记录链接 |
| 工具编排 | 需要先跑脚本，再读结果，再生成说明 |
| 非固定问题 | 输入材料和输出要求每次略有变化 |

## 模板落地优先级

| 优先级 | 工具 | 理由 |
|---|---|---|
| P1 | 案例卡片生成助手 | 第四板块会持续扩展案例，复用价值高 |
| P1 | 知识库维护助手 | 与 CPA-ZH 日常维护直接相关 |
| P1 | PDF 原文归档工具 | 法规、政策、准则更新都会用到 |
| P2 | Excel 底稿清洗工具 | 审计实务使用频率高，但需要结合具体底稿字段 |
| P2 | VBA 加载项工具箱 | 适合团队分发，但需要先定按钮边界 |
| P3 | Web/桌面小工具 | 适合成熟后产品化，不宜一开始过度封装 |

## 后续动作

1. 为 P1 工具建立单独工具页或 README。
2. 将已落地工具登记到 [[concepts/ai-coding-tool-registry]]。
3. 将已成熟模板回挂到 [[concepts/ai-coding-audit-automation-scenario-matrix]]。
4. 每个工具落地前先通过 [[concepts/ai-coding-risk-control-checklist]] 做风险检查。
