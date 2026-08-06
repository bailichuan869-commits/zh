---
title: 四部核心法律条款级索引
type: source
source_type: generated-index
created: 2026-06-26
updated: 2026-08-05
sources: [local-core-laws-2026-06-26, challenge-knowledge-source-summary-2026-07-13]
raw_path: raw/indexes/core-laws-article-index.csv
tags: [cpa, law, article-index, p1-core]
related: [[concepts/regulations-and-standards]], [[concepts/law-cpa]], [[concepts/law-accounting]], [[concepts/law-company]], [[concepts/law-securities]]
domain: sources
topic: batches
---

# 四部核心法律条款级索引

## 文件位置

- CSV 明细：`raw/indexes/core-laws-article-index.csv`
- Markdown 总览：`raw/indexes/core-laws-article-index.md`
- 法律全文与索引目录：`wiki/concepts/laws/`

## 汇总

| 法律 | 条款记录数 | 合并全文索引页 | 条款目录 |
|---|---:|---:|---|
| 中华人民共和国注册会计师法（2026 修订草案） | 60 | 1 | [[concepts/laws/cpa-law/index]]（草案·待官方核对） |
| 中华人民共和国会计法 | 51 | 1 | [[concepts/laws/accounting-law/index]] |
| 中华人民共和国公司法 | 266 | 1 | [[concepts/laws/company-law/index]] |
| 中华人民共和国证券法 | 226 | 1 | [[concepts/laws/securities-law/index]] |
| 合计 | 603 | 4 |  |

## 备注

《中华人民共和国会计法》本地原文附则部分保留两个“第四十九条”。条款级生成器按原文保留两条记录，并在第二个同号条款文件名中追加序号后缀，便于追溯和后续人工核验。

2026-08-05 更新：注册会计师法条款入口先改用 `raw/laws/中华人民共和国注册会计师法-2026-草案.md`，生成 60 条草案记录。该草案依据主席令第七十八号修改决定手工套用 2014 修正版生成，非官方重新公布全文；正式引用前应以官方重排版核对。2026 修订资料见 [[concepts/laws/cpa-law/2026-amendment-highlights]] 和 [[sources/cpa-law-amendment-2026]]。

2026-08-05 结构调整：法规页不再机械保留“一条一句话”的全部独立条文页。每部法律的 `index.md` 承载完整条文和稳定锚点；专题页、责任表和政策页统一引用 `#article-xxx` 锚点，不另建法规条文知识页。

## 生成脚本

- `tools/generate_core_law_article_pages.py`

后续如替换更权威的官方原文，可以复跑该脚本更新合并全文索引、条文锚点和 CSV 明细。
