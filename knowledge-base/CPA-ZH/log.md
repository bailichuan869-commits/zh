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

## [2026-07-09 17:30] ingest | 导入 AI 编程与自动化

- 从 `D:\ai-coding\讲义` 导入 Agent、Python、VBA 插件三类 Markdown 讲义 58 份。
- 原文归档至 `raw/lectures/ai-coding-lectures-2026-07-09/`。
- 新增来源：[[sources/ai-coding-lectures-archive-2026-07-09]]
- 新增板块入口：[[concepts/ai-coding-lectures]]
- 新增分入口：[[concepts/ai-coding-agent-lectures]]、[[concepts/ai-coding-python-lectures]]、[[concepts/ai-coding-vba-addin-lectures]]
- 维护说明：该板块用于支撑审计自动化、知识库维护、Excel 工具和 Agent 工作流建设。

## [2026-07-09 18:20] maintenance | 一次性清理可验证升级项

- 补齐 6 个来源页的 `sources` 或 `raw_path` 元数据，覆盖第二板块、第三板块和维护批次来源页。
- 重新生成 [[concepts/kb-section-upgrade-dashboard]]，分板块 schema 检查结果为 `flagged=0`、`unclassified=0`。
- 复核来源状态：manifest 条目 95 项，来源状态提示 `flagged=0`。
- 复核 manifest：5 个 manifest、95 个条目，审计通过。
- 后续维护重点从“结构补缺”转为内容深化：第三板块情景库、第四板块案例扩展、第五板块工具模板提炼。

## [2026-07-09 18:45] maintenance | 第五板块 2.0 工具化升级

- 新增 [[concepts/ai-coding-tool-template-library]]，将讲义能力提炼为 PDF、Excel、Word、知识库维护、案例加工、Agent 和 VBA 加载项工具模板。
- 新增 [[concepts/ai-coding-audit-automation-scenario-matrix]]，按审计流程、知识库维护和实务场景映射自动化工具路线。
- 新增 [[concepts/ai-coding-risk-control-checklist]]，沉淀自动化工具的输入、处理、输出、日志、复核和 Agent 使用边界。
- 新增 [[concepts/ai-coding-project-roadmap]]，规划 CPA-ZH 入库助手、案例卡片生成助手、PDF 原文归档工具等优先项目。
- 更新第五板块总入口、智能化工具页、总索引、README 和 WIKI 配置，形成从讲义到工具模板、场景矩阵、风险控制和项目落地的闭环。

## [2026-07-09 19:05] maintenance | 落地 CPA-ZH 本地入库助手

- 新增 `tools/kb_ingest_local.py`，支持本地文件或目录 dry-run 入库预览，显式 `--commit` 后复制到 raw 并生成 manifest、metadata、source-url。
- 将工具接入统一入口：`tools/kb.py ingest-local`。
- 新增 [[concepts/cpa-zh-local-ingest-helper]]，记录功能范围、典型命令、参数说明、输出结构、维护流程和风险边界。
- 使用 `README.md` 完成 dry-run 验证，确认默认模式只输出计划，不写入测试目录。

## [2026-07-09 19:25] maintenance | 落地 CPA-ZH 案例卡片生成助手

- 新增 `tools/kb_case_card.py`，支持从本地 Word/PDF/Markdown/TXT/HTML 等原文生成 `wiki/cases/` 案例卡片草稿。
- 将工具接入统一入口：`tools/kb.py case-card`。
- 新增 [[concepts/cpa-zh-case-card-helper]]，记录功能范围、典型命令、生成结构、风险边界和验证方式。
- 使用已有长期股权投资案例原文完成 dry-run 验证，确认默认模式只输出草稿预览，不写入 `wiki/cases/`。

## [2026-07-09 19:45] maintenance | 落地 CPA-ZH 原文归档助手

- 新增 `tools/kb_archive_doc.py`，支持单个 PDF/HTML/DOCX 等原文 dry-run 归档预览，显式 `--commit` 后复制为 `official.*` 并生成 manifest、metadata、source-url。
- 将工具接入统一入口：`tools/kb.py archive-doc`。
- 新增 [[concepts/cpa-zh-archive-doc-helper]]，记录功能范围、典型命令、输出结构、字段说明、维护流程和风险边界。
- 使用已归档的发行类第9号 PDF 完成 dry-run 验证，确认默认模式只输出计划，不写入测试目录。

## [2026-07-09 20:10] maintenance | 建立第五板块工具注册表

- 新增 [[concepts/ai-coding-tool-registry]]，汇总 `tools/kb.py` 已落地命令、dry-run 与 commit 边界、写入风险等级、验证命令和后续工具规划。
- 回挂第五板块总入口、工具模板库、审计自动化场景矩阵、风险控制清单、项目落地路线、总索引和 README。
- 更新 `tools/README.md`，补充工具注册表入口和统一命令写入模式。

## [2026-07-09 20:35] maintenance | 落地 CPA-ZH PDF 转 Markdown 助手

- 新增 `tools/kb_pdf_to_markdown.py`，支持单个 PDF 或目录批量 dry-run 预览，显式 `--commit` 后写入 Markdown、转换 manifest 和 OCR 待处理清单。
- 将工具接入统一入口：`tools/kb.py pdf-md`。
- 新增 [[concepts/cpa-zh-pdf-to-markdown-helper]]，记录功能范围、典型命令、输出结构、维护流程和风险边界。
- 使用发行类第9号 PDF 完成 dry-run 验证，当前 `pypdf` 可抽取正文约 3742 个字符。

## [2026-07-09 20:55] maintenance | 落地 CPA-ZH 案例主题索引回挂助手

- 新增 `tools/kb_case_index_suggest.py`，扫描 `wiki/cases/` 案例卡片并生成按会计主题、准则入口、审计风险和底稿用途组织的回挂建议。
- 将工具接入统一入口：`tools/kb.py case-index`。
- 新增 [[concepts/cpa-zh-case-index-helper]] 和 [[concepts/case-index-suggestion-report]]。
- 使用现有 5 张案例卡片完成 dry-run 和报告写入验证，结果为 `cases=5`、`indexed=5`、`missing=0`。

## [2026-07-09 21:15] maintenance | 落地 CPA-ZH 本地问答日志回写助手

- 新增 `tools/kb_qa_capture.py`，支持直接传入问题/回答或读取 UTF-8 文本文件，默认 dry-run，显式 `--commit` 后写入 `wiki/questions/`。
- 将工具接入统一入口：`tools/kb.py qa-capture`。
- 新增 [[concepts/cpa-zh-qa-capture-helper]]，记录功能范围、典型命令、输出结构、维护流程和风险边界。
- 升级 schema 检查，支持 `type: question` 和 `wiki/questions/` 目录归类。

## [2026-07-13 17:20] verification | 核实考察知识清单文件来源汇总

- 归档用户提供的《考察知识清单_文件来源汇总.html》至 `raw/sources/challenge-knowledge-source-summary-2026-07-13/file-source-summary/official.html`。
- 新增 [[sources/challenge-knowledge-source-summary-verification-2026-07-13]]，逐项核实前三板块来源覆盖情况。
- 标记高优先级差异：《中华人民共和国注册会计师法》来源汇总提示 2026-06-26 修订、2027-01-01 施行，现有 CPA-ZH 本地文本仍为 2014 修正版线索，后续需归档新版并重建条款页。
- 为第二板块政策文件和第三板块职业道德/独立性来源页补充备选官方链接和核验入口。

## [2026-07-14 10:20] maintenance | 按最新来源纠偏注册会计师法版本状态

- 尝试联网访问全国人大网《注册会计师法》2026 修改决定链接，沙箱内外均未能连接远程服务器；未伪造新版全文。
- 按 [[sources/challenge-knowledge-source-summary-verification-2026-07-13]] 的最新来源线索，更新 [[concepts/law-cpa]]、[[concepts/laws/cpa-law/index]]、[[sources/core-laws-article-index-2026-06-26]]、[[concepts/first-section-completion-map]]、[[concepts/regulations-and-standards]]、[[sources/first-section-master-index-2026-06-26]] 和 [[concepts/first-section-responsibility-risk-map]]。
- 为 `concepts/laws/cpa-law/` 下 46 个条款页统一加入版本提示：当前条款基于 2014 修正版，仅作修订前历史索引和差异复核参考。
- 后续仍需取得 2026 修订后官方全文，再重建 raw 文本、条款页和核心法律条款索引。

## [2026-07-13 17:25] ingest | 归档练习题库（试卷一）答案解析

- 从用户桌面导入 `练习题库 （试卷一）-答案解析.pdf`，归档至 `raw/outlines/practice-question-bank-2026-07-13/practice-question-bank-paper-1-answer-explanations/official.pdf`。
- 新增 raw manifest：`raw/outlines/practice-question-bank-2026-07-13/manifest.json`。
- 使用 `tools/kb.py pdf-md --engine auto` 转为 Markdown 派生文本，实际引擎为 `pymupdf`，文本质量 `ok`，抽取正文约 9,314 字符。
- 新增来源页：[[sources/practice-question-bank-paper-1-answer-explanations-2026-07-13]]。
- 新增问答校准页：[[questions/practice-question-bank-paper-1-answer-key]]，保存试卷一标准答案表，并记录三道错题校准：不定项第 1 题、不定项第 10 题、判断第 14 题。

## [2026-07-23 11:38] ingest | 归档注册会计师法2026修订决定并推进版本更新

- 联网核验确认《注册会计师法》2026 修订真实存在：主席令第七十八号，2026-06-26 第十四届全国人大常委会第二十三次会议通过，2027-01-01 施行（多家权威媒体交叉确认；本环境 WebFetch 不可达外网，事实经 WebSearch 摘要 + 人民网/人民日报全文确认）。
- 归档修改决定全文：`raw/laws/注册会计师法-修改决定-2026.md`（转录自人民网/人民日报/新华社 2026-06-27 02 版全文，二十七条完整）。
- 新增来源页：[[sources/cpa-law-amendment-2026]]，记录主席令、官方核验入口与本地归档关系。
- 新增要点对照页：[[concepts/laws/cpa-law/2026-amendment-highlights]]，二十七条逐项对照 + 五条修订主线 + 高频考点速记。
- 更新 [[concepts/law-cpa]] 版本状态（由“待补充”改为“2026 修订已确认并归档”）、frontmatter sources/tags/updated。
- 更新 [[sources/core-laws-article-index-2026-06-26]] 注会法备注与汇总行（46 → 修订前，待重建约 59 条）。
- 更新 [[concepts/laws/cpa-law/index]] 版本提示、汇总与 related。
- 待办：取得官方重新公布文本后，重建 raw 文本、约 59 条条款页与核心法律条款索引（任务 #4 仍 pending）。

## [2026-07-23 11:51] update | 生成《注册会计师法》2026 修订草案（手工套用）

- 依据 `raw/laws/注册会计师法-修改决定-2026.md`（二十七条修改决定）手工套用 2014 修正版原文，生成 2026 修订草案全文。
- 新增 raw 草案：`raw/laws/中华人民共和国注册会计师法-2026-草案.md`（8 章 60 条，含草案声明与修订说明）。
- 新增 wiki 草案条款页：`wiki/concepts/laws/cpa-law-2026-draft.md`（合并单页，8 章 60 条全文，标注"草案·待官方核对"）。
- 更新 [[concepts/law-cpa]] 版本状态表（新增"2026 修订草案（手工套用）"行）、条款目录与待补充，加入草案链接。
  - 更新 [[concepts/laws/cpa-law/index]] 版本提示（指向草案）、汇总（46 → 草案推演 60 条）、frontmatter。
  - 说明：草案非官方文本；序号重排（新增党的领导第2条、诚信建设第7条、准入管理第33条、第六章监督管理第42-46条、删原第43条等）与罚则倍数（五倍→十倍）均依修改决定推演。60 条离散条款页待官方重排版核对后再生成。

## [2026-07-23 13:51] maintenance | 重建搜索索引与文本缓存（草案接入检索）

- 新增文件致索引过期：wiki 页面 985→988（新增 cpa-law-amendment-2026、2026-amendment-highlights、cpa-law-2026-draft）、raw 文件 795→797（新增 修改决定-2026、2026-草案）。
- 运行 `tools/kb_search.py index` 重建搜索索引：indexed=1836（原 1831，+5），写入 `search/kb_search.sqlite`。
- 运行 `tools/kb_text_cache.py build` 重建文本缓存：files_seen=719、cached=718、empty=0（原空记录 1 条已修复）、errors=0。
- 实测检索"注册会计师法 2026 草案"已命中新草案 raw 与 wiki 页，新注册会计师法（2026 修订草案）现已可直接检索。

## [2026-07-23 13:54] maintenance | 从检索索引排除旧法（2014版），只保留新法（2026草案）

- 用户需求：搜"注册会计师法"只返回新法（2026修订草案），不要旧法（2014修正版）干扰。实测确认旧法 46 个条款页霸榜检索结果、新法被淹没。
- 修改 `tools/kb_search.py`：新增 `SUPERSEDED_SEARCH_EXCLUDES` 常量与 `is_search_excluded()` 辅助函数，在 `iter_documents` 的 wiki 遍历与 raw-file 遍历两处跳过被取代的旧法文件。
- 排除范围：`wiki/concepts/laws/cpa-law/cpa-law-article-*.md`（46 个旧条款页）+ `raw/laws/中华人民共和国注册会计师法.md`（旧法 raw 全文）。新法草案（raw + wiki 单页）、修改决定、要点对照、主入口 law-cpa.md、条款目录 cpa-law/index.md 均保留。
- 旧法文件物理保留，仍可通过 [[concepts/law-cpa]] 的历史版本链接访问；2027-01-01 前如需"现行有效旧条文"可走此路径。
- 运行 `tools/kb_search.py index` 重建：indexed=1789（原 1836，-47）。
- 验证：搜"注册会计师法"前 10 条均为新法相关（草案 raw/wiki、修改决定、要点对照、主入口、条款目录），旧条款页与旧 raw 已彻底消失；其他政策文件因正文引用注会法而出现，属正常关联。

## [2026-07-23 14:01] maintenance | 同步 CPA-ZH README 统计与版本说明

- 推动背景：旧法排除出检索后，README 仍显示旧统计（wiki 985 / raw 795 / 索引 1831），health 报 "README stat stale" 三处告警。
- 同步数字（经 `kb.py health` 核对）：wiki 页面 985→988、raw 原始文件 795→797、本地检索索引记录 1831→1789；索引构成表 pdf-markdown 98 / raw-file 650→651 / raw-manifest 98 / wiki 985→942 / total 1831→1789；日期 2026-07-14→2026-07-23。
- 新增"最近重大更新（2026-07-23）"小节：说明《注册会计师法》2026 修订草案接入、旧版（2014修正）条款页已排除出检索（排除逻辑见 `tools/kb_search.py` 的 `SUPERSEDED_SEARCH_EXCLUDES`）、相关页面链接。
- 索引构成表下补充说明：wiki 实际文件 988，其中 46 个旧法条款页 + 1 个旧 raw 已排除出索引，故索引内 wiki 942 / raw-file 651。
- 在"当前最适合继续建设的方向"新增第 6 项：取得官方重公布全文后用 `tools/generate_core_law_article_pages.py` 拆 60 个正式条款页替换旧结构。
- 复跑 `kb.py health`：Issues=none、Warnings=none（含 README 告警已清除）。注意 `wiki 页面` 状态行须为纯数字，health 解析器不识别带括号说明，故说明移至"最近重大更新"与索引表注释。

## [2026-07-23 14:05] maintenance | 补全旧法排除：移除旧条款目录页 cpa-law/index.md

- 用户反馈检索仍出现旧法。排查确认：上一轮只排除了 46 个离散旧条款页（cpa-law-article-*.md）与旧 raw 全文，但漏掉唯一的旧法目录页 `wiki/concepts/laws/cpa-law/index.md`（其正文即 2014 版 46 条条款目录，含旧法条文摘要），该页仍在索引中，搜"注册会计师法"排第 5 条。
- 其他非旧法本身的引用：练习题题库 PDF（试卷一）作为考题引用注会法旧条款（学习资料，未排除）；law-cpa.md 主入口仅在"历史版本"语境提及旧法、无旧法条文正文（保留正确）；公司法/证券法/会计法的"违反本法规定"属其他法律（无关）。
- 修复：在 `tools/kb_search.py` 的 `SUPERSEDED_SEARCH_EXCLUDES` 增加 `"wiki/concepts/laws/cpa-law/index.md"`。重建索引 indexed=1789→1788（-1）。
- 验证：搜"注册会计师法"前 7 条均为新法（修改决定、要点对照、主入口、草案 raw/wiki、监督检查办法），旧目录页消失；搜"第四十五条"仅余公司法/会计法/证券法（其他法律）。
- 同步 README：索引总记录 1789→1788、wiki 942→941；"最近重大更新"与索引表注释将排除数由 46 更正为 47（含目录页）。复跑 health：Issues=none、Warnings=none。

## [2026-07-23 14:13] maintenance | 修复文本缓存空记录（根因：归档文件被误纳入缓存）

- 健康检查一直显示 `text_cache empty=1`（719 项中 1 条空）。定位：空条目源文件为 `raw/standards/audit/archives/2023-23-audit-standards.zip`，缓存文件 `cache/text/files/06/068b5a....txt` 大小 0 字节。
- 根因：`tools/kb_text_cache.py` 的 `iter_raw_files` 把 `raw/` 下所有文件都送进抽取器，但 `.zip` 是二进制归档、没有可抽取的单一文本，故恒为空。重抽也无效。
- 修复：在 `kb_text_cache.py` 新增 `SKIP_SUFFIXES`（zip/rar/7z/tar/gz/bz2/xz/jar/iso + 位图 png/jpg/jpeg/gif/bmp/tif/tiff/webp），`iter_raw_files` 跳过这些无可抽取文本的文件。
- 连带修复误报：`kb_health_check.py` 的 `text_cache_stats` 用独立的 `TEXT_CACHE_SKIP_NAMES` 枚举"应缓存文件"，未含 zip，导致构建器跳过 zip 后 health 误报 `text cache is stale`。已在 `kb_health_check.py` 增加同名 `TEXT_CACHE_SKIP_SUFFIXES` 并让枚举同时按后缀过滤，两边一致。
- 重建缓存：`kb_text_cache.py build` → files_seen=718、cached=718、empty=0、errors=0（zip 已不再纳入）。复跑 health：text_cache items=718 cached=718 empty=0 stale=False；search_index total=1788 stale=False；Issues=none、Warnings=none。
- 清理：删除临时输出文件；磁盘上那个 0 字节孤儿缓存文件（manifest 已不再引用）暂留，无害。

## [2026-07-23 14:23] lint | 知识库体检（llm-wiki Lint 框架：断链 / 孤立页）

- 用 llm-wiki 的 Lint 操作对 CPA-ZH 做体检，自写 `tools/wiki_lint.py`（检测断链 broken links 与孤立页 orphan pages；链接约定 `[[concepts/foo/bar]]` 为 wiki/ 根相对路径，frontmatter 的 `related:` 一并计入）。
- 结果：wiki 页 988 个，**断链 0 条**（所有 `[[链接]]` 均指向真实存在的页面，无缺失页——干净信号）；**孤立页 29 个**（无任何入链）。
- 孤立页分类：
  - 合理孤立（非问题）：`wiki/log.md`（活动日志页，天然无入链）。
  - 疑似测试残留：`questions/revenue-repurchase-qa-demo`（示例 QA 页）。
  - 值得接入：17 个 CAS 会计准则页（cas-03/05/10/12/23/24/26/27/29/32/34/35/38/39/40/41/42）+ 9 个准则解释页（interp-04/05/06/07/08/11/19）+ 3 个 CSA 审计准则页（csa-1152/1241/1331）。这些页既无正文入链、也不在 `wiki/index.md` 收录，存在但几乎不可达，建议补索引或入链。
- 实测 `wiki/index.md` 完全未收录上述 CAS/CSA 孤立页，确认其为"未接入"而非"仅索引未正文关联"。
- 产出：报告 `lint_report.md`；脚本 `tools/wiki_lint.py` 可复用为定期 lint 工具。
- 运行注意：本环境 `.venv` 在 `/d/ai-audit/.venv`，须在 `/d/ai-audit` 下用绝对路径 `python` 调用脚本，且需 `PYTHONFAULTHANDLER=1` 规避段错误；Bash 内 `grep` 偶发段错误，判断结果以 Read 工具读输出文件为准。

## [2026-07-23 14:31] lint-fix | 批量接入 27 个孤立准则页

- 用户要求把体检发现的 27 个孤立准则页补接入索引。自写 `tools/connect_orphan_standards.py`：读取每页 frontmatter `title:`（回退首行 `# ` 标题），生成 `- [[链接]] - <标题>。` 行，插入到对应体系页的"重点入口"区（`## 待补充` 之前）。
- 接入分布：17 个 CAS（cas-03/05/10/12/23/24/26/27/29/32/34/35/38/39/40/41/42）+ 7 个解释（interp-04/05/06/07/08/11/19）→ `wiki/concepts/accounting-standards-system.md`（+25 行，含注释行）；3 个 CSA（csa-1152/1241/1331）→ `wiki/concepts/audit-standards-system.md`（+4 行，含注释行）。
- 两个体系页本身已在 `wiki/index.md`（第 43、54 行）链接，导航链完整：index → 体系页 → 27 个准则页。
- 复跑 `tools/wiki_lint.py` 验证：孤立页 29 → **2**（仅剩 `wiki/log.md` 日志页与 `questions/revenue-repurchase-qa-demo` 示例页，均属合理/可清理孤立）。断链仍 0。
- 复用工具：`connect_orphan_standards.py`、`wiki_lint.py` 均可留存为定期 lint/接入维护脚本。

## [2026-07-23 14:38] script-review | 核对并加固新建脚本

- 用户要求核对本次新建的两个脚本（wiki_lint.py / connect_orphan_standards.py）。
- 加固①：wiki_lint.py 输出 `lint_report.md` 由相对路径改为基于 `__file__` 的绝对路径（CPA-ZH/lint_report.md），不再依赖运行时 cwd；其 `WIKI` 读取路径本就基于 `__file__`（CPA-ZH/wiki）稳健。
- 加固②：connect_orphan_standards.py 的 `BASE` 由 `Path("wiki")`（相对、强依赖 cwd）改为基于 `__file__` 绝对路径；初次加固误写成 `parent.parent`（=CPA-ZH，缺 wiki 层），导致找不到 cas-03.md，已修正为 `parent.parent / "wiki"`（=CPA-ZH/wiki）。并新增幂等保护：检测到 `<!-- 补充接入` 注释则 SKIP，避免误跑重复插入 27 条。
- 验证：从项目根 `/d/ai-audit` 直接调用脚本绝对路径（venv python `D:/ai-audit/.venv/Scripts/python.exe`，符合"全部 venv 运行"约定）。wiki_lint 输出 `DONE pages=988 broken=0 orphans=2`（cwd 独立生效）；connect 重跑输出 `SKIP ×2 + DONE`（路径正确且幂等生效、未重复插入）。
- 环境坑：Git Bash 下 `PY=/d/ai-audit/.venv/...` 变量赋值 + cd 组合会解析异常（connect 测试曾回退系统 Python、路径变 `D:\d\ai-audit`）；改用 `D:/ai-audit/.venv/Scripts/python.exe` 绝对路径直写、不 cd、不变量后稳定。
## [2026-07-30] ingest | 2026年8月第一期（第二期研讨会）案例
- 归档 4 份内部研讨 DOCX，并生成保持 Word 文档顺序的 Markdown 语义派生件。
- 新增来源页：[[sources/case-batch-2026-08-first-issue-second-seminar]]。
- 新增 4 张已复核案例卡片：[[cases/2026-08-first-issue-consolidation-structured-platform]]、[[cases/2026-08-first-issue-lease-asset-not-ready]]、[[cases/2026-08-first-issue-medical-distributor-revenue]]、[[cases/2026-08-first-issue-space-test-bench-capitalization]]。
- 更新 [[concepts/case-analysis]] 和 [[concepts/case-topic-index]]，回挂准则、相关案例、审计风险和底稿用途。
