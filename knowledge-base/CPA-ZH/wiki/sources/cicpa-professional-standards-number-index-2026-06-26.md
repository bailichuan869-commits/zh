---
title: 中国注册会计师执业准则编号级索引
type: source
source_type: generated-index
created: 2026-06-26
updated: 2026-06-26
raw_path: raw/indexes/cicpa-professional-standards-number-index.csv
tags: [audit, standards, cicpa, generated-index, p1-core]
related: [[concepts/audit-standards-system]], [[sources/cicpa-professional-standards-download-2026-06-26]]
---

# 中国注册会计师执业准则编号级索引

## 文件位置

- 编号汇总 CSV：`raw/indexes/cicpa-professional-standards-number-index.csv`
- 映射明细 CSV：`raw/indexes/cicpa-professional-standards-number-mapping.csv`
- Markdown 总览：`raw/indexes/cicpa-professional-standards-number-index.md`
- 分准则 wiki 页：`wiki/concepts/audit-standards/`
- 生成脚本：`tools/generate_cicpa_professional_standards_number_index.py`

## 汇总

本索引整合中注协执业准则专题下载批次中的直接 PDF、2023 年 23 项审计准则 ZIP 解压 PDF，以及可稳定识别准则编号的专题条目。

| 项目 | 数量 |
|---|---:|
| 准则编号页 | 40 |
| 未映射资料页 | 1 |
| 映射资料记录 | 100 |
| 未映射资料记录 | 0 |
| 直接准则原文 PDF | 13 |
| ZIP 解压准则 PDF | 23 |
| 应用指南 PDF | 49 |
| 专题条目 | 15 |

## 重点准则入口

| 准则 | 页面 |
|---|---|
| 中国注册会计师鉴证业务基本准则 | [[concepts/audit-standards/assurance-basic]] |
| 中国注册会计师审计准则第1101号——注册会计师的总体目标和审计工作的基本要求 | [[concepts/audit-standards/csa-1101]] |
| 中国注册会计师审计准则第1211号——通过了解被审计单位及其环境识别和评估重大错报风险 | [[concepts/audit-standards/csa-1211]] |
| 中国注册会计师审计准则第1301号——审计证据 | [[concepts/audit-standards/csa-1301]] |
| 中国注册会计师审计准则第1501号——对财务报表形成审计意见和出具审计报告 | [[concepts/audit-standards/csa-1501]] |

## 映射规则

- 直接 PDF 清单优先采用 CSV 标题。
- 2023 年 34 项应用指南中标题仅为序号的 PDF，从通知 HTML 的附件链接补全标题。
- ZIP 解压 PDF 依据文件名解析准则编号和标题。
- 专题条目仅在标题中能稳定识别准则编号时纳入对应准则页。
- 无法稳定解析准则编号的资料保留在 [[concepts/audit-standards/unmapped]]。

## 后续处理

1. 对重点审计准则页补充“目标、关键要求、审计程序、底稿关注点、监管处罚连接”。
2. 提取 PDF 正文文本，建立条款级或章节级索引。
3. 将审计准则与四部法律、企业会计准则重点章节建立交叉引用。
