---
title: AI 编程与自动化项目落地路线
type: concept
concept_type: implementation-roadmap
created: 2026-07-09
updated: 2026-07-09
sources: [ai-coding-lectures-archive-2026-07-09]
tags: [ai-coding, automation, roadmap, project, audit-tools]
related: [[concepts/ai-coding-lectures]], [[concepts/ai-coding-tool-template-library]], [[concepts/ai-coding-audit-automation-scenario-matrix]], [[concepts/ai-coding-risk-control-checklist]], [[concepts/ai-coding-tool-registry]], [[concepts/cpa-zh-local-ingest-helper]], [[concepts/cpa-zh-case-card-helper]], [[concepts/cpa-zh-archive-doc-helper]]
domain: tools
topic: ai-coding
---

# AI 编程与自动化项目落地路线

本页把第五板块从“学习资料”推进到“项目落地”。路线遵循小步快跑：先做命令行脚本，再做可复用工具，最后才考虑 GUI、Web 或加载项分发。

已落地工具和统一命令见 [[concepts/ai-coding-tool-registry]]。路线图负责规划“接下来做什么”，注册表负责记录“当前能直接用什么”。

## 分阶段路线

| 阶段 | 目标 | 产物 | 验收标准 |
|---|---|---|---|
| 0. 需求澄清 | 找到重复劳动和风险点 | 场景说明、输入输出、人工复核点 | 能说清不用工具时如何做 |
| 1. 临时脚本 | 跑通最小可用流程 | 单脚本、样例输入、样例输出 | 小样本结果可人工核对 |
| 2. 稳定工具 | 参数化、日志化、异常处理 | CLI 工具、README、日志 | 可重复运行，失败可追踪 |
| 3. 工作流集成 | 接入知识库或底稿流程 | manifest、wiki 页、索引、体检 | 输出能被 CPA-ZH 检索和复核 |
| 4. 团队分发 | 降低使用门槛 | GUI、Web、EXE、VBA 加载项 | 非开发人员能按说明使用 |
| 5. 质量维护 | 版本、测试、变更记录 | 测试样例、版本日志、风险清单 | 改动后可验证不破坏原流程 |

## 推荐项目池

| 项目 | 优先级 | 目标用户 | 技术路线 | 对应模板 |
|---|---|---|---|---|
| CPA-ZH 入库助手 | P1 | 知识库维护者 | Python + Agent | [[concepts/ai-coding-tool-template-library]] |
| 案例卡片生成助手 | P1 | 审计复盘和培训 | Agent + Markdown 模板 | [[concepts/cpa-zh-case-card-helper]], [[concepts/case-analysis]] |
| 案例主题索引回挂助手 | P2 | 案例库维护者 | Python + 规则建议 | [[concepts/cpa-zh-case-index-helper]], [[concepts/case-topic-index]] |
| 本地问答日志回写助手 | P2 | 知识库使用者 | Python + Markdown 模板 | [[concepts/cpa-zh-qa-capture-helper]], [[concepts/kb-maintenance-workflow]] |
| PDF 原文归档工具 | P1 | 法规政策维护 | Python | [[concepts/cpa-zh-archive-doc-helper]], [[concepts/ai-coding-tool-template-library]] |
| PDF 转 Markdown/OCR 工具 | P1 | 法规政策和准则维护 | Python + 文本抽取 | [[_maintenance/cpa-zh-pdf-to-markdown-helper]], [[concepts/source-status-dashboard]] |
| 研发费用底稿检查工具 | P2 | IPO/年报项目组 | Python + Excel | [[concepts/securities-issuance-rd-staff-investment]] |
| Excel 底稿整理加载项 | P2 | 审计人员 | VBA | [[concepts/ai-coding-vba-addin-lectures]] |
| 函证状态跟踪工具 | P2 | 审计项目组 | Python/Excel | [[concepts/audit-process]] |
| Word 报告批量检查工具 | P3 | 报告复核人员 | Python | [[concepts/ai-coding-python-lectures]] |

## P1 项目拆解

### CPA-ZH 入库助手

| 项目 | 内容 |
|---|---|
| 输入 | 本地文件夹、官方 URL、板块类型、来源说明 |
| 输出 | raw 归档目录、manifest 条目、wiki/sources 来源页草稿、索引更新 |
| 控制点 | 官方链接核验、raw 不覆盖、schema 检查、health 检查 |
| 首版边界 | 已落地为 [[concepts/cpa-zh-local-ingest-helper]]；先支持本地文件入库，不自动联网下载 |

### 案例卡片生成助手

| 项目 | 内容 |
|---|---|
| 输入 | Word/PDF/Markdown 案例原文、案例批次、主题标签 |
| 输出 | wiki/cases 案例卡片草稿、case-topic-index 回挂建议 |
| 控制点 | 不杜撰事实；结论和依据必须人工复核 |
| 首版边界 | 已落地为 [[concepts/cpa-zh-case-card-helper]]；先处理结构清晰的 Word 或 Markdown 案例，生成草稿不生成最终结论 |

### 案例主题索引回挂助手

| 项目 | 内容 |
|---|---|
| 输入 | `wiki/cases/` 案例卡片 |
| 输出 | [[concepts/case-index-suggestion-report]] |
| 控制点 | 只生成建议，不直接改写主题索引；主题、风险和底稿用途需人工复核 |
| 首版边界 | 已落地为 [[concepts/cpa-zh-case-index-helper]]；根据 tags、related 和正文结构生成回挂建议 |

### 本地问答日志回写助手

| 项目 | 内容 |
|---|---|
| 输入 | 本地问答文本，或问题/回答两个 UTF-8 文本文件 |
| 输出 | `wiki/questions/` 问答草稿页 |
| 控制点 | 保留原问题和原回答；默认 `status: draft`；未经复核不得当作正式专业口径 |
| 首版边界 | 已落地为 [[concepts/cpa-zh-qa-capture-helper]]；自动 related 仅为关键词建议 |

### PDF 原文归档工具

| 项目 | 内容 |
|---|---|
| 输入 | PDF/HTML 文件、来源 URL、文件标题、板块 |
| 输出 | official 文件、source-url.txt、metadata.json、manifest 更新建议 |
| 控制点 | 哈希、字节数、来源路径、重复文件提示 |
| 首版边界 | 已落地为 [[concepts/cpa-zh-archive-doc-helper]]；先处理本地原文文件，不联网下载，不自动认定最新有效版本 |

### PDF 转 Markdown/OCR 工具

| 项目 | 内容 |
|---|---|
| 输入 | PDF 文件或包含 PDF 的目录 |
| 输出 | `cache/pdf-markdown/` 下的 Markdown、manifest、OCR 待处理清单 |
| 控制点 | 不覆盖 PDF 原文；抽取结果需人工抽查；扫描件不得伪造 OCR 文本 |
| 首版边界 | 已落地为 [[_maintenance/cpa-zh-pdf-to-markdown-helper]]；先支持可抽取文字 PDF，扫描件只登记待 OCR |

## 技术选型规则

| 需求 | 首选 |
|---|---|
| 批量文件、解析、归档 | Python |
| 当前 Excel 工作簿内一键处理 | VBA |
| 需要读资料、写说明、更新 wiki | Agent |
| 需要团队非技术人员使用 | GUI、EXE 或 VBA 加载项 |
| 需要多人同时访问 | Web 服务 |

## 项目文档模板

每个落地项目应包含：

1. `README.md`：用途、安装、使用、输入输出；
2. `CHANGELOG.md`：版本和变更；
3. `examples/`：样例输入输出；
4. `tests/` 或人工验收清单；
5. 风险控制清单链接：[[concepts/ai-coding-risk-control-checklist]]；
6. 工具注册表登记：[[concepts/ai-coding-tool-registry]]；
7. CPA-ZH 回挂页面。

## 近期路线建议

1. 先做不联网的 CPA-ZH 入库助手。
2. 再做案例卡片生成助手，服务第四板块扩展。
3. 再做 PDF 原文归档工具和 PDF 转 Markdown/OCR 工具，服务第一、二、三板块更新。
4. 最后根据真实底稿样式做 Excel/VBA 工具。
