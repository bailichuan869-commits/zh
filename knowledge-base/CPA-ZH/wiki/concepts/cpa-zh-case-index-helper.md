---
title: CPA-ZH 案例主题索引回挂助手
type: concept
concept_type: automation-tool
created: 2026-07-09
updated: 2026-07-10
sources: [ai-coding-lectures-archive-2026-07-09]
tags: [ai-coding, automation, case-index, case-card, maintenance]
related: [[concepts/ai-coding-tool-registry]], [[concepts/case-topic-index]], [[concepts/case-index-suggestion-report]], [[concepts/cpa-zh-case-card-helper]], [[concepts/case-analysis]]
domain: tools
topic: helpers
---

# CPA-ZH 案例主题索引回挂助手

本页记录第五板块 P2 项目“案例主题索引自动回挂工具”的首版落地。工具入口为 `tools/kb.py case-index`，底层脚本为 `tools/kb_case_index_suggest.py`。

常规模式先扫描 `wiki/cases/` 案例卡片，生成“按会计主题、准则入口、审计风险、底稿用途”的回挂建议报告。工具只输出建议，不再维护任何批量派生答疑索引区块。

## 功能范围

| 功能 | 状态 |
|---|---|
| 扫描 `wiki/cases/` 案例卡片 | 已支持 |
| 识别案例标题、标签、related 链接和一句话结论 | 已支持 |
| 生成会计主题建议 | 已支持 |
| 生成准则入口建议 | 已支持 |
| 生成审计风险建议 | 已支持 |
| 生成底稿用途建议 | 已支持 |
| 检查案例是否已在主题索引出现 | 已支持 |
| 自动改写 `case-topic-index.md` | 不支持；仅生成建议报告，正式索引仍由人工复核后写入 |

## 典型命令

预览建议：

```powershell
.\.venv\Scripts\python.exe tools\kb.py case-index
```

写入建议报告：

```powershell
.\.venv\Scripts\python.exe tools\kb.py case-index --write-report
```

报告默认写入：

```text
wiki/concepts/case-index-suggestion-report.md
```

## 判断依据

| 依据 | 用途 |
|---|---|
| `tags` | 识别收入确认、政府补助、长期股权投资、税会差异等主题 |
| `related` | 识别 CAS、审计准则、第一板块专题和政策入口 |
| `## 一句话结论` | 提炼主题索引中的关键判断 |
| `## 审计关注点` | 提炼审计风险列 |
| `## 底稿留痕建议` | 提炼底稿用途列 |

## 维护流程

1. 新增或修改案例卡片后，先运行 `tools\kb.py case-index` 预览。
2. 检查 `missing` 数量；若大于 0，打开 [[concepts/case-index-suggestion-report]]。
3. 人工复核“建议补入”的行，把合适内容复制到 [[concepts/case-topic-index]]。
4. 若建议分类不准确，优先修正案例卡片的 `tags`、`related` 或正文小标题。
5. 运行 `tools\kb.py schema --write-report`、`tools\kb.py index` 和 `tools\kb.py health`。

## 风险边界

- 不自动认定案例专业结论，只生成索引维护建议。
- 不直接改写主题索引，避免错误分类被批量写入。
- 关键词规则不能替代人工判断，复杂案例需要人工调整主题、风险和底稿用途。
- 新增主题达到 5 个以上案例时，建议拆分独立专题索引页。

## 首版验证

已对现有正式案例卡片完成报告写入验证，结果以 `cases=`、`indexed=`、`missing=` 三行统计为准。
