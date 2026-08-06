---
title: CPA-ZH 知识页完整性报告
type: concept
concept_type: maintenance-dashboard
created: 2026-08-06
updated: 2026-08-06
page_role: index
maturity: reviewed
answer_ready: false
sources: [kb-completeness]
tags: [maintenance, completeness, quality-control, cpa]
related: [[concepts/kb-content-maturity-dashboard]], [[concepts/kb-section-upgrade-dashboard]], [[concepts/kb-user-guide]]
domain: tools
topic: kb-ops
---

# CPA-ZH 知识页完整性报告

本页由 `tools/kb.py completeness --write-report` 生成，用于发现知识页的显式待补内容、骨架页、来源缺口和 Wiki 断链。它只检查结构与维护信号，不替代法规、准则和政策的官方效力核验。

## 粒度口径

法规不按“一条一个知识页”拆分。四部核心法律保留原文和四个合并全文索引页，条文通过 `#article-xxx` 锚点检索和引用；原文页、来源页、目录页及全文索引页属于有意保留的 reference/index，不因正文较短被列为骨架缺口。

## 总览

| 指标 | 数量 |
|---|---:|
| Wiki 页面 | 270 |
| 存在待处理问题的页面 | 0 |
| 显式待补/待完善 | 0 |
| 待官方或待确认 | 0 |
| 骨架页 | 0 |
| 缺少来源元数据 | 0 |
| Wiki 断链页面 | 0 |
| 有意保留原文/来源页 | 35 |
| 有意保留目录/全文索引页 | 105 |

## 显式待补内容

先补正文、来源链或实际案例链接；完成后重新运行本报告。

| 页面 | 标题 | 检测结果 |
|---|---|---|
| 无 |  |  |

## 骨架页

补齐定位、规则/流程、实务影响、证据或交叉引用；原文和全文索引页不在此列。

| 页面 | 标题 | 检测结果 |
|---|---|---|
| 无 |  |  |

## 来源缺口

补充 sources、raw_path 或 source_url；专业结论不能只靠无来源的摘要。

| 页面 | 标题 | 检测结果 |
|---|---|---|
| 无 |  |  |

## 效力或来源待核验

保留为风险提示，不把本地草案、镜像或未核验版本写成现行官方口径。

| 页面 | 标题 | 检测结果 |
|---|---|---|
| 无 |  |  |

## Wiki 断链

修复目标路径、文件名或锚点前缀；raw/ 链接由原文层单独维护。

| 页面 | 标题 | 检测结果 |
|---|---|---|
| 无 |  |  |

## 有意保留页面

这些页面承担原文追溯、目录导航或合并全文索引职责，不作为知识正文缺口统计：

- `wiki/cases/golden-cases-index.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-judgments/index.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/basic.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-01.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-02.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-03.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-04.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-05.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-06.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-07.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-08.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-09.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-10.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-11.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-12.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-13.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-14.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-16.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-17.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-18.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-19.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-20.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-21.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-22.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-23.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-24.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-25.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-26.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-27.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-28.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-29.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-30.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-31.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-32.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-33.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-34.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-35.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-36.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-37.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-38.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-39.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-40.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-41.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/cas-42.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-01.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-02.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-03.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-04.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-05.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-06.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-07.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-08.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-09.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-12.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-13.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-14.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-15.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-16.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-17.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-18.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-19.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/interpretations/interp-20.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/other-rules/index.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/other-rules/topic-rules.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/unmapped-review.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards/unmapped.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/accounting-standards-system.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1101.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1111.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1121.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1131.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1141.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1151.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1152.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1201.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1211.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1231.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1321.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1324.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1341.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1411.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1421.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1501.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1504.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1521.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1601.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1631.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/csa-1633.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/topics.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards/unmapped.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/audit-standards-system.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/case-index-suggestion-report.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/first-batch-answer-readiness.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/kb-content-maturity-dashboard.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/kb-governance-dashboard.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/kb-section-upgrade-dashboard.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/laws/accounting-law/index.md`：原文或来源页，短正文不代表知识缺口
- `wiki/concepts/laws/company-law/index.md`：原文或来源页，短正文不代表知识缺口
- `wiki/concepts/laws/cpa-law/index.md`：原文或来源页，短正文不代表知识缺口
- `wiki/concepts/laws/cpa-law-2026-draft.md`：原文或来源页，短正文不代表知识缺口
- `wiki/concepts/laws/securities-law/index.md`：原文或来源页，短正文不代表知识缺口
- `wiki/concepts/policy-document-comparison.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/policy-documents.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/policy-execution-checklist.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/policy-implementation-map.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/policy-official-link-checklist.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/policy-version-validity-tracker.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/regulations-and-standards.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/concepts/source-status-dashboard.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/index.md`：目录或全文索引页，职责是导航和稳定锚点
- `wiki/log.md`：原文或来源页，短正文不代表知识缺口
- `wiki/questions/practice-question-bank-paper-1-answer-key.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/2026-06-26-initial-structure.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/accounting-interpretations-index-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/accounting-standards-official-links.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/ai-coding-lectures-archive-2026-07-09.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/archived-cpa-competition-policy-pages.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/audit-standards-official-links.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/case-batch-2026-07-first-issue.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/case-batch-2026-08-first-issue-second-seminar.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/challenge-knowledge-source-summary-verification-2026-07-13.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/cicpa-professional-standards-download-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/cicpa-professional-standards-number-index-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/core-laws-article-index-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/cpa-law-amendment-2026.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/enterprise-accounting-standards-application-cases-download-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/enterprise-accounting-standards-download-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/enterprise-accounting-standards-implementation-qa-download-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/enterprise-accounting-standards-interpretations-download-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/enterprise-accounting-standards-number-index-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/enterprise-accounting-standards-other-rules-download-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/first-section-master-index-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/issuance-guidance-rd-staff-investment-archive-2026-07-09.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/kb-retrieval-upgrade-2026-06-29.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/local-core-laws-2026-06-26.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/local-regulations-inventory.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/policy-documents-official-links-2026-06-29.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/policy-documents-raw-archive-2026-06-29.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/practice-question-bank-paper-1-answer-explanations-2026-07-13.md`：原文或来源页，短正文不代表知识缺口
- `wiki/sources/third-section-official-archive-2026-06-29.md`：原文或来源页，短正文不代表知识缺口

## 建议处理顺序

1. 先修复 broken-wiki-link 和 missing-source，避免内容补好后无法追溯。
2. 再处理 pending-content 和 skeleton，优先法规/准则/政策入口、流程页和高频专题。
3. 对 pending-verification 保留版本边界；只有获得官方依据后才升级为现行有效结论。
4. Agent 可执行结构、来源和引用复核；人工复核底线仍保留，`agent-reviewed` 不等于 `user-approved`。

_JSON 明细：`workspace/outputs/kb_completeness.json`；生成日期：2026-08-06。_
