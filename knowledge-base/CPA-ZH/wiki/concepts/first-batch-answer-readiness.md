---
title: 首批答疑主题复核与准入清单
type: concept
concept_type: maintenance-dashboard
created: 2026-08-03
updated: 2026-08-03
page_role: index
maturity: reviewed
answer_ready: false
sources: [case-batch-2026-08-first-issue-second-seminar, cas-22-23, cas-31]
tags: [maintenance, answer-readiness, reviewed, pending-review]
related: [[concepts/kb-content-maturity-dashboard]], [[concepts/case-topic-index]], [[concepts/accounting-judgments/index]]
domain: practice
topic: audit-practice
---

# 首批答疑主题复核与准入清单

本清单管理首批五个高频主题的答疑准入。`answer_ready: true` 仅授予已具备可定位来源、明确适用边界、人工复核结论和复核状态的知识页或案例卡；目录页和待复核草稿不进入答疑主检索集。

| 主题 | 当前可答疑资产 | 待人工复核资产 | 准则与来源入口 |
|---|---|---|---|
| 收入确认 | [[cases/2026-08-first-issue-medical-distributor-revenue]] | [[concepts/accounting-judgments/revenue-contract-control-transfer]] | [[concepts/accounting-standards/cas-14]] |
| 租赁 | [[cases/2026-08-first-issue-lease-asset-not-ready]] | [[concepts/accounting-judgments/lease-term-modification-sale-leaseback]] | [[concepts/accounting-standards/cas-21]] |
| 合并范围与控制 | [[cases/2026-08-first-issue-consolidation-structured-platform]] | [[concepts/accounting-judgments/consolidation-control-loss-of-control]] | [[concepts/accounting-standards/cas-33]] |
| 金融工具 | 无；证据不足时应拒答 | [[concepts/accounting-judgments/financial-assets-classification-derecognition-ecl]]、[[cases/golden-expected-credit-loss-simplified]] | [[concepts/accounting-standards/cas-22]] |
| 现金流量表与列报 | 无；证据不足时应拒答 | [[concepts/cash-flow-classification-and-presentation]] | [[concepts/accounting-standards/cas-31]] |

## 人工复核准入清单

1. 核对原始事实、适用会计准则版本和报告期。
2. 保留条件分支、反向证据及不适用边界，不将示例泛化为无条件结论。
3. 核对审计程序、底稿证据与结论之间的对应关系。
4. 通过维护端生成预览并确认后，系统才会把页面更新为 `maturity: reviewed`、`answer_ready: true` 和 `review_status: user-approved`。

## 闭环记录

新增高价值问题先使用问答回写工具保存为 `wiki/questions/` 草稿，再由本清单决定进入哪个主题复核队列。每次完成一批复核后，重建缓存和检索索引，并运行 schema 与健康检查。
