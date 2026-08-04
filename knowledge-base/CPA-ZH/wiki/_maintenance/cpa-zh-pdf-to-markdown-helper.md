---
title: CPA-ZH PDF 转 Markdown 助手
type: concept
concept_type: automation-tool
created: 2026-07-09
updated: 2026-07-09
sources: [ai-coding-lectures-archive-2026-07-09]
tags: [ai-coding, automation, pdf, markdown, text-extraction, ocr]
related: [[concepts/ai-coding-tool-registry]], [[concepts/ai-coding-project-roadmap]], [[concepts/ai-coding-tool-template-library]], [[concepts/ai-coding-risk-control-checklist]], [[concepts/source-status-dashboard]]
---

# CPA-ZH PDF 转 Markdown 助手

本页记录第五板块 P1 项目“PDF 转 Markdown/OCR 工具”的首版落地。工具入口为 `tools/kb.py pdf-md`，底层脚本为 `tools/kb_pdf_to_markdown.py`。

当前版本目标是把可抽取文字的 PDF 转为 Markdown，并把抽取不到正文或疑似乱码的 PDF 明确标记出来。它不联网、不调用外部 OCR 服务、不覆盖原 PDF。默认是 dry-run 预览，只有显式加 `--commit` 才会写入转换结果。

## 功能范围

| 功能 | 状态 |
|---|---|
| 单个 PDF 转 Markdown | 已支持 |
| 目录内 PDF 批量转 Markdown | 已支持 |
| dry-run 预览 | 已支持，默认行为 |
| 生成转换 manifest | 加 `--commit` 后执行 |
| 生成 OCR 待处理清单 | 加 `--commit` 后执行 |
| 多引擎抽取 | 已支持：`pymupdf`、`pdfplumber`、`pdfminer`、`pypdf` |
| 文本质量标记 | 已支持：`ok`、`suspect`、`garbled`、`empty` |
| 覆盖已有输出 | 需显式加 `--overwrite` |
| OCR 识别扫描件 | 当前不支持，仅标记 `ocr_status: pending` 或 `review_required` |
| 联网文档解析 API | 首版不支持 |

## 典型命令

先预览单个 PDF：

```powershell
.\.venv\Scripts\python.exe tools\kb.py pdf-md `
  --source "knowledge-base\CPA-ZH\raw\policies\issuance-guidance\issuance-class-09-rd-staff-investment\official.pdf"
```

确认无误后写入：

```powershell
.\.venv\Scripts\python.exe tools\kb.py pdf-md `
  --source "knowledge-base\CPA-ZH\raw\policies\issuance-guidance\issuance-class-09-rd-staff-investment\official.pdf" `
  --commit
```

批量处理 raw 目录下的 PDF：

```powershell
.\.venv\Scripts\python.exe tools\kb.py pdf-md `
  --source "knowledge-base\CPA-ZH\raw" `
  --commit
```

## 输出结构

```text
cache/pdf-markdown/
├── manifest.json
├── ocr-pending.md
└── files/
    └── <pdf-name>-<path-digest>.md
```

Markdown 文件会记录来源 PDF 路径、原文件 SHA256、抽取方式、正文长度和 OCR 状态。`ocr-pending.md` 只列出当前抽取器没有取得正文的 PDF。

## 参数说明

| 参数 | 说明 |
|---|---|
| `--source` | PDF 文件或包含 PDF 的目录 |
| `--output-subdir` | 输出目录，默认 `cache/pdf-markdown/files` |
| `--engine` | 抽取引擎，默认 `auto`，可选 `pymupdf`、`pdfplumber`、`pdfminer`、`pypdf` |
| `--commit` | 真正写入 Markdown、manifest 和 OCR 待处理清单 |
| `--overwrite` | 覆盖已有 Markdown 输出并更新 manifest |

## 维护流程

1. 先 dry-run，查看 `convertible`、`ocr_pending` 和 `text_quality_*` 数量。
2. 确认输出目录无误后加 `--commit`。
3. 运行 `tools/kb.py cache build --force`，让文本缓存重新读取相关文件。
4. 运行 `tools/kb.py index`，让新 Markdown 进入检索。
5. 运行 `tools/kb.py sources write-report`，复核 OCR 待处理状态。
6. 运行 `tools/kb.py health`。

## 风险边界

- 不改写 `raw/` 中的 PDF 原文。
- 不把抽取文本直接认定为官方有效原文，引用法规准则时仍应回到原 PDF 或官方链接核验。
- 不对扫描件或乱码文本做虚假 OCR；抽取不到正文时列入待处理清单，疑似乱码时标记 `text_quality: garbled`。
- 不替代人工复核，尤其是 PDF 排版复杂、页眉页脚混入、表格错位和换行异常的情况。

## 版本验证

已使用 `raw/policies/issuance-guidance/issuance-class-09-rd-staff-investment/official.pdf` 做 dry-run 验证，可取得正文约 3742 个字符。

对疑似乱码的 PDF，应标记为 `text_quality: garbled` 后转入 OCR 或文档解析流程；测试样本不应写入已清理的专题来源名称。
