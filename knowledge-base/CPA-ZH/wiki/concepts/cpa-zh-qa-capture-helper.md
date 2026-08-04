---
title: CPA-ZH 本地问答日志回写助手
type: concept
concept_type: automation-tool
created: 2026-07-09
updated: 2026-07-09
sources: [ai-coding-lectures-archive-2026-07-09]
tags: [ai-coding, automation, qa-log, writeback, maintenance]
related: [[concepts/ai-coding-tool-registry]], [[concepts/kb-maintenance-workflow]], [[concepts/kb-user-guide]]
domain: tools
topic: helpers
---

# CPA-ZH 本地问答日志回写助手

本页记录“本地问答日志回写 1.0”的工具设计。工具入口为 `tools/kb.py qa-capture`，底层脚本为 `tools/kb_qa_capture.py`。

它用于把有价值的本地问答沉淀为 `wiki/questions/` 页面，保留原问题、原回答、关联知识库页面、复核状态和后续动作。首版不自动改写回答、不自动升级为正式案例或专题页，避免把未经复核的对话内容变成正式口径。

## 功能范围

| 功能 | 状态 |
|---|---|
| 直接传入问题和回答 | 已支持 |
| 从 UTF-8 文本文件读取问题和回答 | 已支持 |
| 自动生成 `wiki/questions/` 页面 | 加 `--commit` 后执行 |
| 根据关键词建议 related 链接 | 已支持 |
| 默认 dry-run 预览 | 已支持 |
| 覆盖已有问答页 | 需显式加 `--overwrite` |
| 自动总结、改写、判断结论 | 首版不支持 |
| 自动升级为案例卡片或专题页 | 首版不支持 |

## 典型命令

预览：

```powershell
.\.venv\Scripts\python.exe tools\kb.py qa-capture `
  --question "客户有售后回购条款，能不能确认收入？" `
  --answer "需要围绕控制权是否转移、回购条款实质和客户是否存在重大经济动因判断。"
```

写入：

```powershell
.\.venv\Scripts\python.exe tools\kb.py qa-capture `
  --question "客户有售后回购条款，能不能确认收入？" `
  --answer "需要围绕控制权是否转移、回购条款实质和客户是否存在重大经济动因判断。" `
  --slug "revenue-repurchase-qa" `
  --tags "revenue-recognition,case-reuse" `
  --commit
```

从文件读取：

```powershell
.\.venv\Scripts\python.exe tools\kb.py qa-capture `
  --question-file "D:\path\question.txt" `
  --answer-file "D:\path\answer.txt" `
  --commit
```

## 输出结构

```text
wiki/questions/
└── <slug>.md
```

问答页使用 `type: question`，关键元数据包括：

| 字段 | 用途 |
|---|---|
| `question_type` | 固定为 `local-qa-writeback` |
| `sources` | 默认 `local-qa-log` |
| `status` | 默认 `draft`，人工复核后可改为 `reviewed` 或 `structured` |
| `related` | 关联准则、政策、案例、维护页 |
| `tags` | 用于后续检索和统计 |

## 维护流程

1. 对有复用价值的回答先运行 dry-run。
2. 检查标题、related 链接和 tags 是否合理。
3. 加 `--commit` 写入 `wiki/questions/`。
4. 运行 `tools\kb.py index`，让问答页可检索。
5. 若问答具有案例价值，再升级为案例卡片或专题页。
6. 运行 `tools\kb.py schema --write-report` 和 `tools\kb.py health`。

## 风险边界

- 问答页默认是草稿，不等同于正式专业结论。
- 涉及法规、准则、政策最新效力时，应回到官方原文和本地归档核验。
- 自动 related 只是关键词建议，不替代人工判断。
- 不应把聊天中的推测、未核验事实或临时想法直接升级为正式案例。

## 首版验证

已使用收入确认售后回购问题完成 dry-run 验证，可自动建议 CAS 14、收入确认专题和案例索引等关联页面。
