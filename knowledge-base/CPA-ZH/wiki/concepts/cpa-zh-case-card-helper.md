---
title: CPA-ZH 案例卡片生成助手
type: concept
concept_type: automation-tool
created: 2026-07-09
updated: 2026-07-09
sources: [ai-coding-lectures-archive-2026-07-09]
tags: [ai-coding, automation, case-card, audit-practice, draft]
related: [[concepts/ai-coding-project-roadmap]], [[concepts/case-analysis]], [[concepts/case-topic-index]], [[concepts/ai-coding-risk-control-checklist]]
domain: tools
topic: helpers
---

# CPA-ZH 案例卡片生成助手

本页记录第五板块 P1 项目“案例卡片生成助手”的首版落地。工具入口为 `tools/kb.py case-card`，底层脚本为 `tools/kb_case_card.py`。

首版定位是生成案例卡片草稿，不自动形成最终会计或审计结论。生成页会显式标注“待人工复核”，并保留原文摘要、事实背景、争议问题、准则入口、判断过程、审计关注点和底稿留痕框架。

## 功能范围

| 功能 | 状态 |
|---|---|
| 从本地文件生成案例卡片草稿 | 已支持 |
| 支持 Markdown、TXT、HTML、DOCX、PDF 文本抽取 | 复用 `kb_search.py` 抽取能力 |
| dry-run 预览 | 已支持，默认行为 |
| 写入 `wiki/cases/` | 加 `--commit` 后执行 |
| 自定义标题、slug、source、tags、related | 已支持 |
| 自动回写 `case-topic-index` | 不支持 |
| 自动形成专业结论 | 不支持 |

## 典型命令

先预览：

```powershell
.\.venv\Scripts\python.exe tools\kb.py case-card `
  --source "knowledge-base/CPA-ZH/raw/cases/2026-07-first-issue/案例.docx" `
  --slug "draft-case-card" `
  --title "案例卡片草稿" `
  --source-id "case-batch-2026-07-first-issue" `
  --tags "revenue-recognition,audit-practice"
```

确认无误后写入：

```powershell
.\.venv\Scripts\python.exe tools\kb.py case-card `
  --source "knowledge-base/CPA-ZH/raw/cases/2026-07-first-issue/案例.docx" `
  --slug "draft-case-card" `
  --title "案例卡片草稿" `
  --source-id "case-batch-2026-07-first-issue" `
  --tags "revenue-recognition,audit-practice" `
  --commit
```

## 生成卡片结构

| 模块 | 用途 |
|---|---|
| 一句话结论 | 默认留空，要求人工复核后填写 |
| 案例来源 | 记录来源批次、原始文件、生成方式和日期 |
| 原文摘要 | 从原文抽取前段文本，辅助人工识别主题 |
| 事实背景 | 提醒人工补充交易主体、期间、金额、合同安排等 |
| 争议问题 | 尝试识别问题表述，识别不到则留待人工提炼 |
| 准则入口 | 预留准则、政策、专题页回挂表 |
| 判断过程 | 预留经济实质、适用规则和关键条件分析 |
| 审计关注点 | 提供可复用审计动作框架 |
| 底稿留痕建议 | 提供来源、复核、备忘录和索引更新要求 |
| 待人工复核清单 | 防止草稿被误当正式结论 |

## 风险边界

- 生成结果只是草稿，不是最终专业判断。
- 原文抽取可能不完整，尤其是扫描 PDF 或复杂 Word。
- 准则入口和结论必须人工补充和复核。
- 写入后应更新 [[concepts/case-topic-index]] 和相关专题页。
- 正式使用前应运行 `tools/kb.py schema --write-report` 和 `tools/kb.py health`。

## 首版验证

已使用现有长期股权投资案例原文 dry-run 验证，确认默认模式只输出预览，不写入 `wiki/cases/`。
