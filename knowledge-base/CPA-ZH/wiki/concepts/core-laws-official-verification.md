---
title: 四部核心法律官方版本核验页
type: concept
concept_type: verification-map
created: 2026-06-26
updated: 2026-06-26
sources: [local-core-laws-2026-06-26, core-laws-article-index-2026-06-26]
tags: [law, official-verification, p1-core]
related: [[concepts/law-cpa]], [[concepts/law-accounting]], [[concepts/law-company]], [[concepts/law-securities]], [[concepts/first-section-responsibility-risk-map]]
---

# 四部核心法律官方版本核验页

本页用于维护四部核心法律的版本线索、官方核验入口和知识库引用状态。由于网络访问可能受限，除已明确记录的官方链接外，其余统一标注为“以国家法律法规数据库检索核验为准”。

## 核验总表

| 法律 | 本地版本线索 | 官方核验入口 | 当前处理 |
|---|---|---|---|
| [[concepts/law-cpa]] | 1993-10-31 通过，2014-08-31 修正 | 国家法律法规数据库首页 `https://flk.npc.gov.cn/` 检索“中华人民共和国注册会计师法” | 已生成概览页和 46 个条款页；直接引用前需复核官方数据库。 |
| [[concepts/law-accounting]] | 1985-01-21 通过，1999-10-31 修订，2024-06-28 第三次修正 | 国家法律法规数据库首页 `https://flk.npc.gov.cn/` 检索“中华人民共和国会计法” | 已生成概览页和 51 条记录；本地原文附则存在两个“第四十九条”，条款页已保留。 |
| [[concepts/law-company]] | 1993-12-29 通过，2023-12-29 第二次修订；2024-07-01 施行 | `https://flk.npc.gov.cn/detail2.html?ZmY4MDgxODE4YzkxMDhlYjAxOGNiNjkyMmY3NTBjMDc%3D=` | 已生成概览页和 266 个条款页；新旧条号差异较大，引用旧模板时需核对。 |
| [[concepts/law-securities]] | 1998-12-29 通过，2019-12-28 第二次修订；2020-03-01 施行 | `https://flk.npc.gov.cn/detail2.html?ZmY4MDgwODE3MWU5ZTE4MTAxNzI3ZTMyYjk0ZDdkZTY%3D=` | 已生成概览页和 226 个条款页；证券服务责任条款已纳入专题矩阵。 |

## 核验流程

1. 从国家法律法规数据库检索法律名称，核对题名、通过/修订/修正日期、施行日期和正文。
2. 将官方文本与 `raw/laws/` 本地文本比对，重点看条号、法律责任金额、附则和施行日期。
3. 如发现本地文本与官方文本不一致，先更新 `wiki/` 页面的核验说明，不直接覆盖 `raw/`；待确认后再做 raw 层替换或新增版本文件。
4. 更新 [[concepts/first-section-completion-map]] 和 [[sources/core-laws-article-index-2026-06-26]] 的说明。

## 当前风险提示

- 《会计法》存在 2024 年修正，处罚条款和信用记录相关内容应作为正式引用前重点复核项。
- 《公司法》2023 年修订后条号变化明显，历史底稿、旧培训材料和模板中的条号不宜直接沿用。
- 《证券法》涉及证券服务机构连带赔偿、行政责任和资料保存责任，公众公司项目应优先核验。
