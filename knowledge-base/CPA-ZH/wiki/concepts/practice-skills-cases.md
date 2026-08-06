---
title: 实务技能与案例分析
type: concept
concept_type: framework
maturity: draft
created: 2026-06-26
updated: 2026-06-26
sources: [2026-06-26-initial-structure]
tags: [cpa, audit, practice, tools, p1-core]
related: [[concepts/audit-practice-operations]], [[concepts/audit-process]], [[concepts/intelligent-tools]], [[concepts/comprehensive-competency]], [[concepts/case-analysis]]
domain: practice
topic: audit-practice
---

# 实务技能与案例分析

本板块把法规准则转化为可执行的审计实务能力，包括审计流程、底稿撰写、抽样、RPA、数据清洗、智能化财务应用和复杂场景应对。

## 子专题

- [[concepts/audit-practice-operations]] - 审计实务操作总入口。
- [[concepts/audit-process]] - 审计计划、底稿、抽样等流程能力。
- [[concepts/intelligent-tools]] - RPA、数据清洗与智能化财务应用。
- [[concepts/comprehensive-competency]] - 跨学科知识整合与复杂场景应对。
- [[concepts/case-analysis]] - 案例分析框架。

## 建议沉淀方式

案例和实务页面优先采用“场景 -> 风险 -> 规则 -> 程序 -> 证据 -> 结论 -> 复盘”的结构，便于复用到审计底稿、培训和问答。

## 案例入库标准

每张案例卡至少记录事实背景、争议问题、适用规则、判断路径、审计关注点、底稿证据和结论边界。事实不足时列出需要补证的字段，不把示例条件推广成无条件结论；来源不清时保留原始链接和本地门面，不创建无依据的正式口径。

## 主题路由

| 场景 | 优先入口 | 可复用产物 |
|---|---|---|
| 收入、合同和回购安排 | [[concepts/accounting-judgments/revenue-contract-control-transfer]] | 收入确认案例卡、合同条款核查表 |
| 金融工具、减值和权益区分 | [[concepts/accounting-judgments/financial-assets-classification-derecognition-ecl]] | 金融工具判断矩阵、估值和减值底稿 |
| 合并、长期股权投资和重组 | [[concepts/accounting-judgments/consolidation-control-loss-of-control]] | 控制判断表、合并抵销和重组证据链 |
| 研发、数据资源和证券发行 | [[concepts/securities-issuance-rd-staff-investment]] | 研发人员、投入归集和披露一致性清单 |

## 复核边界

Agent 负责从完整 raw 来源抽取事实、建立引用和发现矛盾；页面只有在来源、版本、事实边界和证据链清楚后才可进入人工复核队列。`agent-reviewed` 表示机器复核完成，不等于 `user-approved`。
