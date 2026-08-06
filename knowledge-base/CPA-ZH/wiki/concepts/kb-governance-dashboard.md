---
title: CPA-ZH 知识资产治理仪表盘
type: concept
concept_type: maintenance-dashboard
created: 2026-08-06
updated: 2026-08-06
page_role: index
maturity: reviewed
answer_ready: false
sources: [kb-governance]
tags: [maintenance, governance, metadata, lifecycle, admission]
related: [[concepts/kb-content-maturity-dashboard]], [[concepts/source-status-dashboard]], [[concepts/kb-content-completeness-report]]
domain: tools
topic: kb-ops
---

# CPA-ZH 知识资产治理仪表盘

本页检查知识资产元数据、版本生命周期、来源注册表和答疑准入状态。字段未显式记录时只统计为缺口，不把系统推导的默认值写成已核验事实。

## 总览

| 指标 | 数量 |
|---|---:|
| Wiki 页面 | 270 |
| 高风险法规/准则/政策页 | 32 |
| 当前推导为 answer_ready | 44 |
| Agent 复核页 | 127 |
| 人工已批准页 | 4 |
| 已登记官方核验文档 | 13 |
| 来源注册表错误 | 0 |

## 显式元数据覆盖率

覆盖率按原始 frontmatter 统计；`asset_id`、内容哈希和默认生命周期可以由索引构建，但仍应在后续治理批次中决定哪些字段需要写回源页面。

| 字段 | 已显式记录 | 页面总数 |
|---|---:|---:|
| `asset_id` | 66 | 270 |
| `source_id` | 253 | 270 |
| `knowledge_type` | 270 | 270 |
| `domain` | 268 | 270 |
| `topic` | 268 | 270 |
| `tags` | 270 | 270 |
| `authority_level` | 78 | 270 |
| `version` | 78 | 270 |
| `published_on` | 55 | 270 |
| `effective_from` | 60 | 270 |
| `effective_to` | 41 | 270 |
| `lifecycle_status` | 78 | 270 |
| `raw_path` | 144 | 270 |
| `markdown_path` | 48 | 270 |
| `source_url` | 109 | 270 |
| `content_sha256` | 48 | 270 |
| `review_status` | 131 | 270 |
| `supersedes` | 3 | 270 |
| `superseded_by` | 0 | 270 |

## 需要治理的页面

| 页面 | 标题 | 问答状态 | 治理问题 |
|---|---|---|---|
| 无 |  |  |  |

## 官方注册表

`source-registry.yml` 当前只对明确登记的文档执行完整字段和本地路径检查；未登记的来源不会被自动视为已核验。

| 文档 ID | 状态 | 本地原文 | 官方 URL |
|---|---|---|---|
| `cpa-law-amendment-2026` | `enacted-not-effective` | `raw/laws/注册会计师法-修改决定-2026.md` | http://www.npc.gov.cn/npc/c2/c30834/202606/t20260626_455830.html |
| `accounting-interpretation-20` | `valid` | `raw/standards/accounting/interpretations-pages/关于印发-企业会计准则解释第20号-的通知.html.md` | https://kjs.mof.gov.cn/zhengcefabu/202606/t20260615_3991686.htm |
| `cicpa-audit-guidelines-2022-15` | `unknown` | `raw/standards/audit/cicpa-guidelines-15-20220120.html.md` | https://www.cicpa.org.cn/xxfb/tzgg/202201/t20220120_63335.html |
| `mof-audit-standards-2022-11` | `unknown` | `raw/standards/audit/cicpa-standards-20220120.html.md` | https://www.cicpa.org.cn/xxfb/tzgg/202201/t20220120_63336.html |
| `mof-audit-standards-2023-revision` | `unknown` | `raw/standards/audit/cicpa-standards-20230103.html.md` | https://www.cicpa.org.cn/xxfb/tzgg/202301/t20230103_63902.html |
| `cicpa-audit-guidelines-2023-34` | `unknown` | `raw/standards/audit/cicpa-guidelines-34-20230410.html.md` | https://www.cicpa.org.cn/xxfb/tzgg/202304/t20230410_64066.html |
| `policy-audit-order-2021-30` | `unknown` | `raw/policies/second-section/audit-order-2021-30/official.html.md` | https://www.gov.cn/zhengce/content/2021-08/23/content_5632714.htm |
| `policy-caihui-supervision-2023-4` | `unknown` | `raw/policies/second-section/caihui-supervision-2023-4/official.html.md` | https://www.gov.cn/zhengce/2023-02/15/content_5741628.htm |
| `policy-cpa-exam-2024-115` | `unknown` | `raw/policies/second-section/cpa-exam-2024-115/official.html.md` | https://www.gov.cn/gongbao/2024/issue_11286/202404/content_6945588.html |
| `policy-cpa-registration-2019-99` | `unknown` | `raw/policies/second-section/cpa-registration-2019-99/official.html.md` | https://www.mof.gov.cn/gkml/caizhengwengao/wg201901/wg201912/202005/t20200522_3518260.htm |
| `policy-firm-inspection-2022-23` | `unknown` | `raw/policies/second-section/firm-inspection-2022-23/official.html.md` | https://www.gov.cn/zhengce/zhengceku/2022-05/16/content_5690682.htm |
| `policy-firm-license-supervision-2019-97` | `unknown` | `raw/policies/second-section/firm-license-supervision-2019-97/official.html.md` | https://www.gov.cn/gongbao/content/2019/content_5392297.htm |
| `policy-integrity-2023-5` | `unknown` | `raw/policies/second-section/integrity-2023-5/official.html.md` | https://www.gov.cn/zhengce/zhengceku/2023-04/02/content_5749779.htm |

## 下一步

1. 先为高风险法规、会计准则、审计准则和政策页补入有证据支撑的版本、生效日期、生命周期和来源 ID。
2. 再为 Agent 已复核内容生成稳定 `asset_id`、内容哈希和来源映射；不补写无法从来源确认的日期或效力。
3. `agent-reviewed` 只表示 Agent 完成结构、引用和边界复核；正式高风险答疑仍保留人工批准底线。
4. 新版本采用新资产并记录 `supersedes`/`superseded_by`，历史查询通过 `as_of` 显式指定日期。

_JSON 明细：`workspace/outputs/kb_governance.json`；生成日期：2026-08-06。_
