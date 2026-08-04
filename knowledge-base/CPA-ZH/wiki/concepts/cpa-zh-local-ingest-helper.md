---
title: CPA-ZH 本地入库助手
type: concept
concept_type: automation-tool
created: 2026-07-09
updated: 2026-07-09
sources: [ai-coding-lectures-archive-2026-07-09]
tags: [ai-coding, automation, ingest, raw-archive, manifest, local-tool]
related: [[concepts/ai-coding-project-roadmap]], [[concepts/ai-coding-tool-template-library]], [[concepts/ai-coding-risk-control-checklist]], [[concepts/kb-maintenance-workflow]]
domain: tools
topic: helpers
---

# CPA-ZH 本地入库助手

本页记录第五板块 P1 项目“CPA-ZH 入库助手”的首版落地。工具入口为 `tools/kb.py ingest-local`，底层脚本为 `tools/kb_ingest_local.py`。

首版只处理本地文件或本地目录，不联网下载，不移动原文件。默认是 dry-run 预览，只有显式加 `--commit` 才会复制文件并写入 raw 归档。

## 功能范围

| 功能 | 状态 |
|---|---|
| 本地文件入库 | 已支持 |
| 本地目录递归入库 | 已支持 |
| dry-run 预览 | 已支持，默认行为 |
| 复制到 raw 批次目录 | 加 `--commit` 后执行 |
| 生成 `manifest.json` | 加 `--commit` 后执行 |
| 生成每个文件的 `metadata.json` | 加 `--commit` 后执行 |
| 生成每个文件的 `source-url.txt` | 加 `--commit` 后执行 |
| 可选生成 `wiki/sources` 批次页 | 加 `--source-page` 和 `--commit` 后执行 |
| 联网下载 | 不支持 |
| 自动生成案例卡片或概念页 | 不支持，后续由加工步骤完成 |

## 典型命令

先预览：

```powershell
.\.venv\Scripts\python.exe tools\kb.py ingest-local `
  --source "D:\path\to\files" `
  --raw-subdir "cases/new-case-batch" `
  --batch-slug "new-case-batch" `
  --title "新案例批次" `
  --source-type "local-case" `
  --official-source "本地案例资料" `
  --tags "case,audit-practice"
```

确认无误后写入：

```powershell
.\.venv\Scripts\python.exe tools\kb.py ingest-local `
  --source "D:\path\to\files" `
  --raw-subdir "cases/new-case-batch" `
  --batch-slug "new-case-batch" `
  --title "新案例批次" `
  --source-type "local-case" `
  --official-source "本地案例资料" `
  --tags "case,audit-practice" `
  --source-page "new-case-batch" `
  --commit
```

## 参数说明

| 参数 | 说明 |
|---|---|
| `--source` | 本地文件或目录 |
| `--raw-subdir` | `raw/` 下的目标批次目录，如 `cases/2026-08-batch` |
| `--batch-slug` | 批次标识，写入 manifest |
| `--title` | 批次标题 |
| `--source-type` | 来源类型，如 `local-case`、`local-source`、`local-lecture` |
| `--official-source` | 来源标签，如“本地案例资料”“客户提供资料”“官方 PDF” |
| `--official-url` | 有官方链接时填写；没有则留空 |
| `--wiki-page` | manifest 条目要回挂的 wiki 页面 |
| `--tags` | 逗号分隔标签 |
| `--source-page` | 可选，生成 `wiki/sources/{slug}.md` |
| `--append` | 追加到已有批次 |
| `--commit` | 真正写入；不加时只预览 |

## 输出结构

```text
raw/<raw-subdir>/
├── manifest.json
├── <item-slug>/
│   ├── 原始文件副本
│   ├── metadata.json
│   └── source-url.txt
└── ...
```

## 维护流程

1. 先 dry-run，核对目标目录、文件数量和归档路径。
2. 加 `--commit` 写入。
3. 运行 `tools/kb.py manifest`。
4. 运行 `tools/kb.py sources summary`。
5. 如需全文检索，运行 `tools/kb.py cache build` 和 `tools/kb.py index`。
6. 按资料性质加工 wiki 页面，例如来源页、概念页或案例卡片。
7. 运行 `tools/kb.py health`。

## 风险边界

- 不直接覆盖已有批次目录；需要追加时显式使用 `--append`。
- 不改写原始来源文件，只复制到 `raw/`。
- 不自动认定官方有效版本，官方链接和效力状态仍需人工核验。
- 不自动生成专业判断结论，案例卡片和概念页仍需人工复核。

## 首版验证

已使用 `README.md` 做 dry-run 验证，确认默认模式只输出计划，不写入测试目录。
