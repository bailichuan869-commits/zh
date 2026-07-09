# CPA-ZH 活动日志

## [2026-06-26 00:00] init | 创建 CPA-ZH 初始知识库

- 新建知识库配置：[[WIKI]]
- 新建总览页：[[wiki/overview]]
- 新建索引页：[[wiki/index]]
- 新增来源摘要：[[wiki/sources/2026-06-26-initial-structure]]
- 根据用户提供的初始目录创建四大板块与关键子专题页面。
- 备注：后续应逐份摄入法规、准则、政策文件原文，并记录官方来源、版本日期和核验日期。

## [2026-06-26 10:58] ingest | 完善第一板块来源链接

- 复制四部本地法律文本到 `raw/laws/`。
- 新增来源：[[sources/local-core-laws-2026-06-26]]
- 新增来源：[[sources/accounting-standards-official-links]]
- 新增来源：[[sources/audit-standards-official-links]]
- 更新概念页：[[concepts/accounting-standards-system]]、[[concepts/audit-standards-system]]
- 说明：终端直连官方下载受限，本次先记录官方有效链接和部分直接 PDF 附件链接。

## [2026-06-26 11:20] ingest | 下载企业会计准则专题

- 下载财政部会计司“企业会计准则”专题真实栏目及分页索引。
- 批量下载企业会计准则条目 HTML 原文页：47 个成功，0 个失败。
- 新增来源：[[sources/enterprise-accounting-standards-download-2026-06-26]]
- 下载清单：`raw/standards/accounting/downloaded-enterprise-accounting-standards.csv`

## [2026-06-26 12:25] ingest | 下载企业会计准则解释

- 下载财政部会计司“企业会计准则解释”栏目及分页索引。
- 批量下载企业会计准则解释条目 HTML 原文页：20 个成功，0 个失败。
- 新增来源：[[sources/enterprise-accounting-standards-interpretations-download-2026-06-26]]
- 下载清单：`raw/standards/accounting/downloaded-enterprise-accounting-standards-interpretations.csv`

## [2026-06-26 13:55] ingest | 下载企业会计准则应用案例和实施问答

- 下载财政部会计司“应用案例”栏目、7个子栏目及相关分页索引。
- 批量下载应用案例条目 HTML 原文页：63 个成功，0 个失败。
- 新增来源：[[sources/enterprise-accounting-standards-application-cases-download-2026-06-26]]
- 下载财政部会计司“实施问答”栏目、24个子栏目及相关分页索引。
- 批量下载实施问答条目 HTML 原文页：163 个成功，0 个失败。
- 新增来源：[[sources/enterprise-accounting-standards-implementation-qa-download-2026-06-26]]
- 说明：实施问答标题较长，最终采用短编号文件名目录 `implementation-qa-pages-v2/` 保存完整条目。

## [2026-06-26 14:05] ingest | 下载企业会计准则其他规定

- 下载财政部会计司“其他规定”栏目及分页索引。
- 批量下载其他规定条目 HTML 原文页：22 个成功，0 个失败。
- 新增来源：[[sources/enterprise-accounting-standards-other-rules-download-2026-06-26]]
- 下载清单：`raw/standards/accounting/downloaded-enterprise-accounting-standards-other-rules.csv`

## [2026-06-26 14:25] ingest | 下载中国注册会计师执业准则专题

- 下载中注协“注册会计师执业准则”专题入口和3个分页。
- 提取专题条目清单：72 条。
- 下载4个已核验通知页。
- 下载直接 PDF 附件：62 个成功，0 个失败。
- 下载并解压2023年准则通知中的 ZIP 附件：23 项审计准则 PDF。
- 新增来源：[[sources/cicpa-professional-standards-download-2026-06-26]]

## [2026-06-26 14:45] ingest | 生成第一板块资料总表

- 生成第一板块资料总表：[[sources/first-section-master-index-2026-06-26]]
- 汇总记录：476 条。
- CSV 明细：`raw/indexes/first-section-master-index.csv`
- Markdown 总览：`raw/indexes/first-section-master-index.md`
- 更新概念页：[[concepts/regulations-and-standards]]

## [2026-06-26 15:20] ingest | 生成四部核心法律条款级索引

- 新增来源：[[sources/core-laws-article-index-2026-06-26]]
- 生成条款页记录：589 条。
- 分法律目录：[[concepts/laws/cpa-law/index]]、[[concepts/laws/accounting-law/index]]、[[concepts/laws/company-law/index]]、[[concepts/laws/securities-law/index]]
- CSV 明细：`raw/indexes/core-laws-article-index.csv`
- Markdown 总览：`raw/indexes/core-laws-article-index.md`
- 生成脚本：`tools/generate_core_law_article_pages.py`
- 备注：《中华人民共和国会计法》本地原文附则部分保留两个“第四十九条”，本次按原文生成两条记录。

## [2026-06-26 16:10] ingest | 生成企业会计准则编号级索引

- 新增来源：[[sources/enterprise-accounting-standards-number-index-2026-06-26]]
- 生成 42 个准则编号页和 1 个未映射资料页。
- 去重后资料记录：296 条；已映射到具体准则编号：216 条；待人工核验：80 条。
- 编号汇总：`raw/indexes/enterprise-accounting-standards-number-index.csv`
- 映射明细：`raw/indexes/enterprise-accounting-standards-number-mapping.csv`
- Markdown 总览：`raw/indexes/enterprise-accounting-standards-number-index.md`
- 分准则目录：`wiki/concepts/accounting-standards/`
- 生成脚本：`tools/generate_accounting_standards_number_index.py`

## [2026-06-26 16:45] ingest | 生成中国注册会计师执业准则编号级索引

- 新增来源：[[sources/cicpa-professional-standards-number-index-2026-06-26]]
- 生成 40 个准则编号页和 1 个未映射资料页。
- 资料记录：100 条；全部映射到具体准则编号。
- 编号汇总：`raw/indexes/cicpa-professional-standards-number-index.csv`
- 映射明细：`raw/indexes/cicpa-professional-standards-number-mapping.csv`
- Markdown 总览：`raw/indexes/cicpa-professional-standards-number-index.md`
- 分准则目录：`wiki/concepts/audit-standards/`
- 生成脚本：`tools/generate_cicpa_professional_standards_number_index.py`
