---
title: CPA-ZH 原文归档助手
type: concept
concept_type: automation-tool
created: 2026-07-09
updated: 2026-07-09
sources: [ai-coding-lectures-archive-2026-07-09]
tags: [ai-coding, automation, archive, raw-archive, official-source, manifest]
related: [[concepts/ai-coding-project-roadmap]], [[concepts/ai-coding-tool-template-library]], [[concepts/cpa-zh-local-ingest-helper]], [[concepts/kb-maintenance-workflow]], [[concepts/source-status-dashboard]]
domain: tools
topic: helpers
---

# CPA-ZH 原文归档助手

本页记录第五板块 P1 项目“PDF/HTML 原文归档工具”的首版落地。工具入口为 `tools/kb.py archive-doc`，底层脚本为 `tools/kb_archive_doc.py`。

首版处理单个本地原文文件，适合法规、政策、准则、监管规则、PDF 附件或 HTML 原文的保守归档。它不联网下载，不认定最新有效版本；默认 dry-run 预览，只有显式加 `--commit` 才写入 `raw/`。

## 功能范围

| 功能 | 状态 |
|---|---|
| 单个本地原文归档 | 已支持 |
| dry-run 预览 | 已支持，默认行为 |
| 复制为 `official.*` | 加 `--commit` 后执行 |
| 生成或追加 `manifest.json` | 加 `--commit` 后执行 |
| 生成 `metadata.json` | 加 `--commit` 后执行 |
| 生成 `source-url.txt` | 加 `--commit` 后执行 |
| 记录文号、官方 URL、附件 URL、官方来源、核验状态 | 已支持 |
| 联网下载官方原文 | 不支持 |
| 自动判断有效版本 | 不支持 |

## 典型命令

先预览：

```powershell
.\.venv\Scripts\python.exe tools\kb.py archive-doc `
  --source "D:\path\to\official.pdf" `
  --raw-subdir "policies/new-policy-batch" `
  --slug "new-policy" `
  --title "政策文件标题" `
  --document-no "文号" `
  --official-url "https://example.gov.cn/page.html" `
  --official-source "官方来源" `
  --official-page-status "verified" `
  --wiki-page "concepts/policy-example"
```

确认无误后写入：

```powershell
.\.venv\Scripts\python.exe tools\kb.py archive-doc `
  --source "D:\path\to\official.pdf" `
  --raw-subdir "policies/new-policy-batch" `
  --slug "new-policy" `
  --title "政策文件标题" `
  --document-no "文号" `
  --official-url "https://example.gov.cn/page.html" `
  --official-source "官方来源" `
  --official-page-status "verified" `
  --wiki-page "concepts/policy-example" `
  --commit
```

## 输出结构

```text
raw/<raw-subdir>/
├── manifest.json
└── <slug>/
    ├── official.pdf 或 official.html
    ├── metadata.json
    └── source-url.txt
```

## 字段说明

| 字段 | 用途 |
|---|---|
| `--raw-subdir` | `raw/` 下批次目录，例如 `policies/second-section` |
| `--slug` | 单个文件归档目录名，也作为 manifest 条目标识 |
| `--title` | 文件标题 |
| `--document-no` | 文号或规则编号 |
| `--official-url` | 官方页面 URL |
| `--attachment-url` | 官方附件 URL；当页面和附件不同地址时使用 |
| `--official-source` | 官方来源名称 |
| `--official-page-status` | `verified`、`local`、`pending` 等 |
| `--wiki-page` | 回挂的 wiki 页面 |
| `--append` | 向已有 manifest 追加条目 |
| `--commit` | 真正写入；不加时只预览 |

## 维护流程

1. 先 dry-run，核对来源文件、目标目录、标题、文号和 URL。
2. 加 `--commit` 写入。
3. 运行 `tools/kb.py manifest`。
4. 运行 `tools/kb.py sources summary`。
5. 如需检索正文，运行 `tools/kb.py cache build` 和 `tools/kb.py index`。
6. 更新或新增对应 wiki 概念页、来源页。
7. 运行 `tools/kb.py health`。

## 风险边界

- 不联网下载；联网核验仍需单独执行或人工完成。
- 不自动认定“最新有效版本”。
- 不覆盖已有条目；追加时必须显式使用 `--append`。
- 不改写原始来源文件，只复制到 `raw/`。
- PDF 文本抽取和 OCR 状态需后续通过文本缓存和来源状态仪表盘复核。

## 首版验证

已使用已归档的“监管规则适用指引——发行类第9号：研发人员及研发投入”PDF 做 dry-run 验证，确认默认模式只输出计划，不写入测试目录。
