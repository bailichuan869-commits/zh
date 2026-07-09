---
title: 企业会计准则编号级索引
type: source
source_type: generated-index
created: 2026-06-26
updated: 2026-06-26
raw_path: raw/indexes/enterprise-accounting-standards-number-index.csv
tags: [accounting, standards, cas, generated-index, p1-core]
related: [[concepts/accounting-standards-system]], [[sources/enterprise-accounting-standards-download-2026-06-26]], [[sources/enterprise-accounting-standards-interpretations-download-2026-06-26]], [[sources/enterprise-accounting-standards-application-cases-download-2026-06-26]], [[sources/enterprise-accounting-standards-implementation-qa-download-2026-06-26]]
---

# 企业会计准则编号级索引

## 文件位置

- 编号汇总 CSV：`raw/indexes/enterprise-accounting-standards-number-index.csv`
- 映射明细 CSV：`raw/indexes/enterprise-accounting-standards-number-mapping.csv`
- Markdown 总览：`raw/indexes/enterprise-accounting-standards-number-index.md`
- 分准则 wiki 页：`wiki/concepts/accounting-standards/`
- 生成脚本：`tools/generate_accounting_standards_number_index.py`

## 汇总

本索引按企业会计准则编号整合已下载的准则原文、准则解释、应用案例、实施问答和其他规定。

| 项目 | 数量 |
|---|---:|
| 准则编号页 | 42 |
| 未映射资料页 | 1 |
| 去重后资料记录 | 296 |
| 已映射到具体准则编号 | 216 |
| 待人工核验资料 | 80 |

## 重点准则

| 准则 | 已映射资料数 | 页面 |
|---|---:|---|
| 企业会计准则第14号——收入 | 27 | [[concepts/accounting-standards/cas-14]] |
| 企业会计准则第22号——金融工具确认和计量 | 22 | [[concepts/accounting-standards/cas-22]] |
| 企业会计准则第21号——租赁 | 15 | [[concepts/accounting-standards/cas-21]] |
| 企业会计准则第25号——保险合同 | 15 | [[concepts/accounting-standards/cas-25]] |
| 企业会计准则第37号——金融工具列报 | 15 | [[concepts/accounting-standards/cas-37]] |

## 映射规则

- 标题中明确出现《企业会计准则第N号》的资料，直接映射到对应准则编号。
- 财政部专题栏目 URL 能明确对应准则主题的，按栏目映射。
- 标题关键词可保守对应准则主题的，标记为中等置信度。
- 同一类资料、同一准则、同一财政部文章 ID 重复出现时，仅保留一个规范入口。
- 无法稳定归属到具体准则编号的资料，保留在 [[concepts/accounting-standards/unmapped]]，不强行归类。

## 后续处理

1. 人工核验 80 条未映射资料，特别是企业会计准则解释、PPP 会计处理、金融工具及其他综合性问答。
2. 将重点准则页从“资料索引”扩展为“原文要点、解释、案例、审计关注点”的知识页。
3. 后续如新增财政部资料，可复跑生成脚本刷新索引。
