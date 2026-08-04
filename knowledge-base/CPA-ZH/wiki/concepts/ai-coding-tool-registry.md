---
title: AI 编程与自动化工具注册表
type: concept
concept_type: tool-registry
created: 2026-07-09
updated: 2026-07-09
sources: [ai-coding-lectures-archive-2026-07-09]
tags: [ai-coding, automation, tool-registry, commands, maintenance]
related: [[concepts/ai-coding-lectures]], [[concepts/ai-coding-project-roadmap]], [[concepts/ai-coding-tool-template-library]], [[concepts/ai-coding-risk-control-checklist]], [[concepts/cpa-zh-local-ingest-helper]], [[concepts/cpa-zh-case-card-helper]], [[concepts/cpa-zh-archive-doc-helper]], [[_maintenance/cpa-zh-pdf-to-markdown-helper]], [[concepts/cpa-zh-case-index-helper]], [[concepts/cpa-zh-qa-capture-helper]]
domain: tools
topic: ai-coding
---

# AI 编程与自动化工具注册表

本页是第五板块的命令总表。以后新增、修改或废弃 CPA-ZH 自动化工具时，先更新本页，再同步更新对应工具页和 `tools/README.md`。

所有 Python 命令默认使用工作区虚拟环境：

```powershell
.\.venv\Scripts\python.exe
```

## 工具总表

| 工具 | 命令入口 | 主要用途 | 默认写入行为 | 工具页 |
|---|---|---|---|---|
| 本地入库助手 | `tools\kb.py ingest-local` | 将本地文件或目录归档到 `raw/`，生成 manifest、metadata、source-url | dry-run，不写入；加 `--commit` 后写入 | [[concepts/cpa-zh-local-ingest-helper]] |
| 案例卡片生成助手 | `tools\kb.py case-card` | 从本地案例原文生成 `wiki/cases/` 案例卡片草稿 | dry-run，不写入；加 `--commit` 后写入 | [[concepts/cpa-zh-case-card-helper]] |
| 案例主题索引回挂助手 | `tools\kb.py case-index` | 扫描案例卡片并生成主题索引回挂建议报告 | dry-run 打印报告；加 `--write-report` 后写入报告 | [[concepts/cpa-zh-case-index-helper]] |
| 本地问答日志回写助手 | `tools\kb.py qa-capture` | 将有价值的本地问答沉淀到 `wiki/questions/` | dry-run 预览；加 `--commit` 后写入 | [[concepts/cpa-zh-qa-capture-helper]] |
| 原文归档助手 | `tools\kb.py archive-doc` | 将单个 PDF/HTML/DOCX 等原文归档为 `official.*` 并生成来源文件 | dry-run，不写入；加 `--commit` 后写入 | [[concepts/cpa-zh-archive-doc-helper]] |
| PDF 转 Markdown 助手 | `tools\kb.py pdf-md` | 将可抽取文字的 PDF 转为 Markdown，并列出待 OCR PDF | dry-run，不写入；加 `--commit` 后写入 | [[_maintenance/cpa-zh-pdf-to-markdown-helper]] |
| 分板块治理检查 | `tools\kb.py schema` | 检查 wiki frontmatter、板块归类和关键元数据 | 只读；加 `--write-report` 写入仪表盘 | [[concepts/kb-section-upgrade-dashboard]] |
| 来源状态仪表盘 | `tools\kb.py sources` | 汇总 manifest、官方链接、文本抽取和 OCR 状态 | `summary` 只读；`write-report` 写入仪表盘 | [[concepts/source-status-dashboard]] |
| manifest 审计 | `tools\kb.py manifest` | 检查 raw manifest 与本地文件、metadata 是否一致 | 只读 | [[concepts/kb-maintenance-workflow]] |
| 一键体检 | `tools\kb.py health` | 联合检查 manifest、内链、索引、文本缓存和 README 统计 | 只读 | [[concepts/kb-maintenance-workflow]] |
| 检索索引 | `tools\kb.py index` | 重建本地 SQLite 检索索引 | 写入 `search/kb_search.sqlite` | [[concepts/kb-maintenance-workflow]] |
| README 统计刷新 | `tools\kb.py readme` | 刷新 CPA-ZH README 中的页面、raw、manifest、索引统计 | 写入 `README.md` | [[concepts/kb-maintenance-workflow]] |
| 本地检索 | `tools\kb.py search` | 查询 wiki、raw 文本缓存和 manifest 信息 | 只读 | [[concepts/kb-user-guide]] |

## 命令速查

### 日常查询

```powershell
.\.venv\Scripts\python.exe tools\kb.py search "收入确认"
.\.venv\Scripts\python.exe tools\kb.py search "独立性准则"
.\.venv\Scripts\python.exe tools\kb.py search "研发人员 研发投入"
```

### 本地资料入库

```powershell
.\.venv\Scripts\python.exe tools\kb.py ingest-local `
  --source "D:\path\to\files" `
  --raw-subdir "cases/new-batch" `
  --batch-slug "new-batch"
```

确认预览结果后写入：

```powershell
.\.venv\Scripts\python.exe tools\kb.py ingest-local `
  --source "D:\path\to\files" `
  --raw-subdir "cases/new-batch" `
  --batch-slug "new-batch" `
  --commit
```

### 案例卡片草稿

```powershell
.\.venv\Scripts\python.exe tools\kb.py case-card `
  --source "knowledge-base\CPA-ZH\raw\cases\batch\case.docx" `
  --slug "draft-case"
```

确认预览结果后写入：

```powershell
.\.venv\Scripts\python.exe tools\kb.py case-card `
  --source "knowledge-base\CPA-ZH\raw\cases\batch\case.docx" `
  --slug "draft-case" `
  --commit
```

### 案例主题索引建议

```powershell
.\.venv\Scripts\python.exe tools\kb.py case-index
.\.venv\Scripts\python.exe tools\kb.py case-index --write-report
```

### 本地问答日志回写

```powershell
.\.venv\Scripts\python.exe tools\kb.py qa-capture `
  --question "客户有售后回购条款，能不能确认收入？" `
  --answer "需要围绕控制权是否转移、回购条款实质和客户是否存在重大经济动因判断。"
```

确认预览结果后写入：

```powershell
.\.venv\Scripts\python.exe tools\kb.py qa-capture `
  --question "客户有售后回购条款，能不能确认收入？" `
  --answer "需要围绕控制权是否转移、回购条款实质和客户是否存在重大经济动因判断。" `
  --slug "revenue-repurchase-qa" `
  --commit
```

### 单个原文归档

```powershell
.\.venv\Scripts\python.exe tools\kb.py archive-doc `
  --source "D:\path\to\official.pdf" `
  --raw-subdir "policies/new-batch" `
  --slug "official-doc" `
  --title "文件标题"
```

确认预览结果后写入：

```powershell
.\.venv\Scripts\python.exe tools\kb.py archive-doc `
  --source "D:\path\to\official.pdf" `
  --raw-subdir "policies/new-batch" `
  --slug "official-doc" `
  --title "文件标题" `
  --commit
```

### PDF 转 Markdown

```powershell
.\.venv\Scripts\python.exe tools\kb.py pdf-md `
  --source "knowledge-base\CPA-ZH\raw\policies\issuance-guidance\issuance-class-09-rd-staff-investment\official.pdf"
```

确认预览结果后写入：

```powershell
.\.venv\Scripts\python.exe tools\kb.py pdf-md `
  --source "knowledge-base\CPA-ZH\raw" `
  --commit
```

## dry-run 与 commit

| 模式 | 含义 | 适用命令 |
|---|---|---|
| dry-run | 只打印计划或草稿，不写入文件 | `ingest-local`、`case-card`、`qa-capture`、`archive-doc`、`pdf-md` 的默认模式 |
| commit | 真正复制文件、写 manifest、写 wiki 草稿、问答页或转换结果 | `ingest-local --commit`、`case-card --commit`、`qa-capture --commit`、`archive-doc --commit`、`pdf-md --commit` |
| report write | 重写治理仪表盘或状态报告 | `schema --write-report`、`sources write-report`、`case-index --write-report`、`readme`、`index` |
| read-only | 只读取并检查当前状态 | `health`、`manifest`、`search`、`sources summary`、`stats` |

## 写入风险等级

| 风险等级 | 命令 | 说明 |
|---|---|---|
| 低 | `search`、`stats`、`manifest`、`health`、`sources summary` | 只读检查或查询，不改文件 |
| 中 | `index`、`cache build`、`schema --write-report`、`sources write-report`、`case-index --write-report`、`readme`、`pdf-md --commit` | 重建缓存、索引、仪表盘、建议报告或 PDF 转换结果，可重复生成 |
| 高 | `ingest-local --commit`、`case-card --commit`、`qa-capture --commit`、`archive-doc --commit` | 新增 raw 或 wiki 文件，应先 dry-run 并核对路径 |

## 每次写入后的验证命令

```powershell
.\.venv\Scripts\python.exe tools\kb.py schema --write-report
.\.venv\Scripts\python.exe tools\kb.py sources write-report
.\.venv\Scripts\python.exe tools\kb.py index
.\.venv\Scripts\python.exe tools\kb.py readme
.\.venv\Scripts\python.exe tools\kb.py health
```

当只新增或修改工具脚本时，先增加编译检查：

```powershell
.\.venv\Scripts\python.exe -m py_compile tools\kb.py tools\kb_ingest_local.py tools\kb_case_card.py tools\kb_case_index_suggest.py tools\kb_qa_capture.py tools\kb_archive_doc.py tools\kb_pdf_to_markdown.py tools\kb_schema_check.py
```

## 工具到知识库场景映射

| 场景 | 首选工具 | 后续加工 |
|---|---|---|
| 新增本地案例资料 | `ingest-local` | 再用 `case-card` 生成案例卡片草稿，回挂 [[concepts/case-topic-index]] |
| 新增案例卡片后维护主题索引 | `case-index` | 生成 [[concepts/case-index-suggestion-report]]，人工复核后更新 [[concepts/case-topic-index]] |
| 有价值问答沉淀 | `qa-capture` | 写入 `wiki/questions/`，后续可升级为案例、专题或检查清单 |
| 新增官方 PDF 或网页下载件 | `archive-doc` | 建来源页，回挂相关法规、政策或准则专题 |
| PDF 已归档但需要可检索正文 | `pdf-md` | 转出 Markdown 后重建文本缓存和检索索引 |
| 新增讲义或课程材料 | `ingest-local` | 建学习线、模板页和场景矩阵 |
| 检查知识库是否健康 | `schema --write-report`、`sources write-report`、`health` | 修复 flagged 页面、失效来源或文本抽取问题 |
| 回答实务问题前检索依据 | `search` | 读取相关规则页、案例页和来源页后再形成判断 |

## 新工具登记规则

新增工具时至少维护以下位置：

1. 本页工具总表和命令速查；
2. 对应工具页，`concept_type` 建议使用 `automation-tool`；
3. `tools/README.md` 的脚本职责表；
4. [[concepts/ai-coding-project-roadmap]] 的项目池或后续规划；
5. 必要时回挂 [[concepts/ai-coding-tool-template-library]]、[[concepts/ai-coding-audit-automation-scenario-matrix]] 和 [[concepts/ai-coding-risk-control-checklist]]；
6. 写入 `log.md` 和 `wiki/log.md`。

## 后续工具规划

| 工具 | 优先级 | 当前状态 | 说明 |
|---|---|---|---|
| PDF 转 Markdown/OCR 工具 | P1 | 已落地首版 | 已支持可抽取文字 PDF 转 Markdown；扫描件列入 OCR 待处理清单 |
| 案例主题索引自动回挂工具 | P2 | 已落地首版 | 根据案例卡片 tags、related 和正文结构生成主题索引回挂建议报告 |
| 本地问答日志回写工具 | P2 | 已落地首版 | 将本地问答沉淀为 `wiki/questions/` 草稿页，保留 related、status 和后续动作 |
| Excel 底稿清洗工具 | P2 | 待结合真实底稿字段 | 先从研发费用、收入、函证等高频底稿切入 |
| 链接有效性复核批处理 | P2 | 已有 `links --check` 基础 | 网络稳定后可扩展为定期复核报告 |
| Web/桌面维护界面 | P3 | 待评估 | 等 CLI 流程稳定后再封装给非技术人员使用 |
