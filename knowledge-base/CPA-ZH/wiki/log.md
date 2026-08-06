---
title: CPA-ZH 知识库日志
type: source
source_type: activity-log
created: 2026-06-26
updated: 2026-08-06
sources: [kb-activity-log]
tags: [cpa, log, structured]
domain: meta
topic: root
---

# CPA-ZH 知识库日志

## 2026-08-06 | content-completeness-and-agent-review

- 修正完整性扫描对“后续可继续补充”词形的漏检；18 个企业会计准则解释占位页已改为财政部原文驱动的编号级事项索引，统一记录官方 URL、raw 门面、版本、生命周期和 Agent 复核边界。行业发展报告全文尚未取得的 1 个真实缺口继续保留。
- 新增 `tools/kb_completeness.py` 并接入 `tools/kb.py completeness --write-report`，统一扫描显式待补内容、骨架页、来源缺口、待官方核验和 Wiki 断链；初始词形口径曾报告显式待补 0，扩展检测后已按上一条完成纠偏。来源缺口、骨架页和断链保持 0，仍保留 3 个待官方核验提示。
- 核心法规继续采用四个合并全文索引页和 `#article-xxx` 条文锚点：当前 603 条法规记录、独立条文页 0，不按“一条一个知识页”拆分；原文层和索引层继续承担完整检索与追溯职责。
- 黄金专题及 21 个案例共 41 项已由 Agent 完成结构、来源和引用复核，状态标记为 `agent-reviewed`；该状态不等于 `user-approved`，人工复核和责任人准入仍是高风险正式结论的底线。
- 重新生成中国注册会计师执业准则编号页，当前识别 27 个准则页、45 条已映射记录和 17 条暂未稳定映射记录；补齐审计准则实务入口、综合执业能力交付检查，并修复审计准则体系页的失效链接。

## 2026-08-04 | agent-first

- 新增 [[concepts/cpa-zh-agent-tools]]：共享 Python 服务、JSON CLI 和本机 stdio MCP。
- Agent 写入统一采用完整预览、人工确认、短期令牌提交和内容哈希复核。
- 前端收缩为只读搜索、正文阅读、原文追溯和健康状态；旧维护接口暂时保留兼容。
- 更新 [[concepts/ai-coding-tool-registry]] 与 [[concepts/ai-coding-project-roadmap]]。

## 2026-06-26 | bootstrap

- 建立知识库根目录与三层结构。
- 补齐四部核心法律条款级索引。
- 生成企业会计准则编号索引与 42 个准则页。
- 生成中国注册会计师执业准则编号索引与 40 个准则页。
- 生成企业会计准则解释页 20 个，并记录官方有效链接。
- 将企业会计准则未映射资料统一收敛到 [[concepts/accounting-standards/unmapped-review]] 待复核清单，不再生成分桶页。
- 将校准补充资料回挂到正式准则页、解释页和其他规定专题页；新增 [[concepts/accounting-standards/other-rules/index]]。
- 新增 [[concepts/audit-standards/topics]]，按审计流程和高频实务问题组织中注协执业准则入口。
- 新增 [[concepts/first-section-completion-map]]，汇总第一板块完成度、关键索引文件和后续完善清单。
- 升级第一板块 14 个高频准则页：为 6 个企业会计准则页补充判断框架，为 8 个审计准则页补充程序设计框架、审计关注点和底稿提示。
- 升级四部核心法律概览页：为 [[concepts/law-cpa]], [[concepts/law-accounting]], [[concepts/law-company]], [[concepts/law-securities]] 补充有效版本线索、核心义务地图、审计实务连接和风险提示。
- 新增 [[concepts/first-section-topic-matrix]] 和 6 个第一板块实务专题页：收入确认错报风险、金融工具估值与减值、合并范围与控制判断、持续经营、关键审计事项、证券服务责任。
- 扩展第一板块专题矩阵：新增 [[concepts/first-section-topics/related-parties-fund-occupation]], [[concepts/first-section-topics/asset-impairment]], [[concepts/first-section-topics/profit-distribution-equity-transactions]]，专题页总数增至 9 个。
- 一次性维护第一板块剩余项目：专题矩阵扩展至 14 个实务专题；高频判断/程序框架页增至 28 个；新增 [[concepts/core-laws-official-verification]] 和 [[concepts/first-section-responsibility-risk-map]]。
- 维护第二板块行业重要政策性文件：升级 7 份政策文件页，新增 [[concepts/policy-document-comparison]], [[concepts/policy-implementation-map]], [[concepts/policy-official-link-checklist]]，用于政策对照、执行落地和官方链接核验。
- 核验第二板块 7 份政策文件官方链接，更新 [[concepts/policy-official-link-checklist]] 和各政策页“官方来源”，新增 [[sources/policy-documents-official-links-2026-06-29]]。
- 执行第二板块 2.0：归档 7 份官方原文至 `raw/policies/second-section/`，新增 [[sources/policy-documents-raw-archive-2026-06-29]], [[concepts/policy-version-validity-tracker]], [[concepts/policy-execution-checklist]]，并将本地归档路径回写至各政策页。
- 执行第三板块 1.0：以中注协“职业道德规范”专题页为主入口，归档行业史、职业道德守则（2020）、独立性准则第1号、2026 应用指南等 24 个官方来源/附件及历史补充归档；升级 [[concepts/history-ethics-independence]], [[concepts/industry-history]], [[concepts/ethics-code]], [[concepts/independence-standard-1]]；新增 [[sources/third-section-official-archive-2026-06-29]]。
- 升级知识库检索与维护能力：新增官方来源注册表 `source-registry.yml`，新增本地检索、manifest 审计和链接汇总工具；建立 [[concepts/kb-maintenance-workflow]] 和 [[sources/kb-retrieval-upgrade-2026-06-29]]；初始索引 1385 条记录，manifest 审计通过。
- 导入 2026年7月第一期实务案例 5 个 Word 文件至 `raw/cases/2026-07-first-issue/`；新增 [[sources/case-batch-2026-07-first-issue]]，升级 [[concepts/case-analysis]] 的案例库维护结构。
- 加工首张实务案例卡片：[[cases/2026-07-first-issue-long-term-equity-investment-confirmation]]，沉淀 A 公司持有 D 公司长期股权投资转换为 C 公司投资的确认判断，并回挂 [[concepts/first-section-topics/long-term-equity-investments]] 和 [[sources/case-batch-2026-07-first-issue]]。
- 继续加工 4 张实务案例卡片：[[cases/2026-07-first-issue-temporary-fixed-asset-tax-difference]]、[[cases/2026-07-first-issue-government-grant-free-use-equipment]]、[[cases/2026-07-first-issue-equipment-sales-revenue-recognition]]、[[cases/2026-07-first-issue-overseas-sales-revenue-recognition]]，分别覆盖暂估转固税会差异、免费使用设备政府补助判断、设备销售售后回购收入确认和海外销售履约义务拆分。
- 增加技术维护工具：新增 `tools/kb_health_check.py` 一键体检和 `tools/kb_update_readme_stats.py` README 统计刷新；更新 `README.md` 和 [[concepts/kb-maintenance-workflow]] 的维护命令。
- 升级 raw 正文处理能力：新增 `tools/kb_text_cache.py` 文本抽取缓存，`kb_search.py` 重建索引时优先复用 `cache/text/`，`kb_health_check.py` 增加文本缓存状态检查；同步更新 `README.md` 和 [[concepts/kb-maintenance-workflow]]。
- 增强案例库可用性：新增 [[concepts/case-topic-index]]，将 5 张案例卡片按会计主题、准则入口、审计风险和底稿用途重新组织，并回挂 [[concepts/case-analysis]] 与总索引。
- 增加新手使用入口：新增 [[concepts/kb-user-guide]]，用操作手册形式说明 CPA-ZH 的三层结构、四大板块、检索方法、新增资料规则、案例使用方式和维护命令；并回挂 README 与总索引。
- 归档发行监管规则：从用户提供的本地底稿目录归档 `发行类第9号.pdf` 至 `raw/policies/issuance-guidance/issuance-class-09-rd-staff-investment/official.pdf.md`；按用户提供的证监会官方链接 `https://www.csrc.gov.cn/csrc/c101802/c7445462/content.shtml` 更新来源信息；新增 [[sources/issuance-guidance-rd-staff-investment-archive-2026-07-09]] 和 [[concepts/securities-issuance-rd-staff-investment]]，并回挂政策入口、证券服务责任专题和总索引。该 PDF 常规文本抽取为空，已标注为待 OCR。
- 增加来源状态仪表盘：新增 `tools/kb_source_status.py` 和 [[concepts/source-status-dashboard]]，按 manifest 条目追踪官方链接、文本缓存和 OCR 状态；当前 37 个 manifest 条目均已进入文本缓存，其中 12 个 PDF 待 OCR。
- 新增第五板块“AI 编程与自动化”：从 `D:\ai-coding\讲义` 导入 58 份 Markdown 讲义至 `raw/lectures/ai-coding-lectures-2026-07-09/`；新增 [[sources/ai-coding-lectures-archive-2026-07-09]], [[concepts/ai-coding-lectures]], [[concepts/ai-coding-agent-lectures]], [[concepts/ai-coding-python-lectures]], [[concepts/ai-coding-vba-addin-lectures]]，并回挂总索引、总览、使用手册和智能化工具页。
- 一次性清理可验证升级项：补齐 6 个来源页的 `sources` 或 `raw_path` 元数据；重新生成 [[concepts/kb-section-upgrade-dashboard]] 后 schema 检查为 `flagged=0`、`unclassified=0`；来源状态为 `flagged=0`；5 个 manifest、95 个条目审计通过。
- 执行第五板块 2.0 工具化升级：新增 [[concepts/ai-coding-tool-template-library]], [[concepts/ai-coding-audit-automation-scenario-matrix]], [[concepts/ai-coding-risk-control-checklist]], [[concepts/ai-coding-project-roadmap]]；将 58 份讲义进一步连接到审计自动化场景、工具模板、风险控制和项目落地路线。
- 落地第五板块 P1 工具首版：新增 `tools/kb_ingest_local.py` 并接入 `tools/kb.py ingest-local`；新增 [[concepts/cpa-zh-local-ingest-helper]]；工具默认 dry-run，仅在显式 `--commit` 后复制本地文件并生成 raw manifest、metadata 和 source-url。
- 落地第五板块 P1 工具第二项：新增 `tools/kb_case_card.py` 并接入 `tools/kb.py case-card`；新增 [[concepts/cpa-zh-case-card-helper]]；工具默认 dry-run，从本地案例原文生成待人工复核的 `wiki/cases/` 案例卡片草稿。
- 落地第五板块 P1 工具第三项：新增 `tools/kb_archive_doc.py` 并接入 `tools/kb.py archive-doc`；新增 [[concepts/cpa-zh-archive-doc-helper]]；工具默认 dry-run，用于单个 PDF/HTML/DOCX 原文归档为 `official.*` 并生成 manifest、metadata、source-url。
- 建立第五板块工具注册表：新增 [[concepts/ai-coding-tool-registry]]，统一登记已落地工具、命令入口、dry-run/commit 边界、写入风险等级、验证命令和后续工具规划；并回挂第五板块总入口、路线图、模板库、风险控制清单、总索引、README 与 `tools/README.md`。
- 落地第五板块 P1 工具第四项：新增 `tools/kb_pdf_to_markdown.py` 并接入 `tools/kb.py pdf-md`；新增 [[_maintenance/cpa-zh-pdf-to-markdown-helper]]；工具默认 dry-run，把可抽取文字的 PDF 转为 Markdown，并把抽取不到正文的 PDF 登记为 OCR 待处理。
- 落地第五板块 P2 工具首版：新增 `tools/kb_case_index_suggest.py` 并接入 `tools/kb.py case-index`；新增 [[concepts/cpa-zh-case-index-helper]] 和 [[concepts/case-index-suggestion-report]]；工具扫描案例卡片并生成主题、准则、风险和底稿用途回挂建议，现有 5 张案例均已在主题索引出现。
- 落地第五板块 P2 工具第二项：新增 `tools/kb_qa_capture.py` 并接入 `tools/kb.py qa-capture`；新增 [[concepts/cpa-zh-qa-capture-helper]]；工具把本地问答回写到 `wiki/questions/`，保留原问题、原回答、related、status 和后续动作。
- 归档练习题库（试卷一）答案解析：新增 [[sources/practice-question-bank-paper-1-answer-explanations-2026-07-13]]，PDF 原文进入 `raw/outlines/practice-question-bank-2026-07-13/`，并使用 `pymupdf` 生成可检索 Markdown 派生文本；新增 [[questions/practice-question-bank-paper-1-answer-key]]，沉淀标准答案和 3 道错题校准记录。
- 核实考察知识清单文件来源汇总：归档用户提供的 HTML 至 `raw/sources/challenge-knowledge-source-summary-2026-07-13/file-source-summary/official.html.md`；新增 [[sources/challenge-knowledge-source-summary-verification-2026-07-13]]；将《注册会计师法》2026 修订线索标记为高优先级待维护事项，并为第二、第三板块补充备选官方链接。
- 重做核心法规页结构：四部法律改为“合并全文索引 + 稳定条文锚点 + 高价值独立页”，共 603 条条文记录、57 个独立条文页；《注册会计师法》当前先使用 2026 修订草案，草案·待官方核对。

## 2026-07-24 | ui-reconstruction

- 重构知识库 UI 与信息架构，目标是落地一个“实用、成逻辑、可检索”的审计执业/培训知识库（核心场景：日常审计执业查询 + 培训与知识沉淀）。
- 新增 `knowledge-base/CPA-ZH/tools/classify_wiki.py`：按路径规则为全部 840 个活跃 wiki 页推断语义化一级 domain / 二级 topic，并把 domain/topic 写回各页 frontmatter；覆盖率 840/840（0 兜底、0 未分类），已排除 `_trash`/`_maintenance` 工作区目录。
- 生成 `knowledge-base/CPA-ZH/ui/categories.json`：11 个 domain（会计准则、审计准则、法律法规、职业道德与独立性、监管政策、实务专题、案例库、知识来源、工具与自动化、问答沉淀、知识库导航）两级语义树 + 页面清单，供前端导航与分面检索。
- 升级 `tools/kb_search.py`：检索索引 documents 表增加 `domain`/`topic` 两列；`documents_fts` 改用 FTS5 `trigram` 分词器，根治中文 3 字子串无法高亮的问题；新增 `clean_title()` 剥离来源文档标题前缀编号（如 `058-`）。重建索引 1640 条，未分类清零。
- 新增 `knowledge-base/CPA-ZH/tools/kb_server.py`：FastAPI 服务，提供 `/api/search`（FTS5 + 分面 + snippet 高亮）、`/api/tree`（categories.json）、`/api/doc`（frontmatter + 正文 + 反链）、`/api/backlinks`、`/api/raw`（路径穿越防护 + CSP 沙箱）等端点，并静态托管 `/ui`、`/wiki`、`/raw`；单实例锁防止重复启动。
- 重写 `knowledge-base/CPA-ZH/ui/index.html`：轻量原生 JS 单页应用，含顶栏搜索（Ctrl K）、语义两级侧边树、首页策展（统计卡/常用入口/专题卡片/最近更新）、专题浏览、搜索结果（分面 + 高亮）、文档详情（TOC + 反链 + 原文直达）和 raw 查看（pdf/html/md 沙箱预览）。旧文件备份为 `ui/index_legacy_backup.html`。
- 启动命令：`.venv/Scripts/python.exe knowledge-base/CPA-ZH/tools/kb_server.py`，默认监听 http://127.0.0.1:8765/（根路径重定向至 /ui/index.html）。

## 2026-07-24 | extract-quality-rule

- 根因修复 `tools/convert_raw_to_md.py` 抽取导航垃圾问题（"财政部微信/返回主站"等）：新增 `decompose_nav()`（按 CSS class/id 提示词删 nav/header/footer/aside 等容器）+ `strip_boilerplate()`（行级样板过滤：整行精确匹配删除；≤30 字含垃圾串整行删；长行仅剥离垃圾子串以保护与页脚粘连的正文；巨型菜单行仅在"已污染"文件中删除，防误删正文）。
- 新增 `--clean` 幂等后处理模式：对既有 `raw/**/*.md` 原地清洗（跳过 `_archive/_trash/_maintenance`，不动 `_archive` 原件），并为缺 `source_type` 的转换页按 `original_file` 后缀回填。本次实清 86 个文件，清洗后全库 Grep 导航垃圾模式 0 残留。
- 新增 `tools/raw_quality.py`：raw 质量扫描器，分类 EMPTY / ERROR_PAGE（文本短语 + 正文<300 字门槛，规避 404 编号/金额误判）/ LOW_CONTENT(<80 字) / MISSING_SOURCE_TYPE，联网实检 source_url（HEAD→GET）。本次结果：718 文件，EMPTY 0、ERROR_PAGE 0、LOW_CONTENT 120（多为合法短问答，仅告警）、MISSING_SOURCE_TYPE 74（均为手工撰写页无 original_file，属正常）、OK 524。
- URL 实检增加出网预检规则：基准站点（baidu/qq）均不可达则判定沙箱拦截出网，全部 URL 标 UNVERIFIED 而非误判 ERROR。本机 32 条含 source_url 文件无法实检；经内置网络通道抽查 4 域名（cicpa/gov.cn/mof/csrc）样本均存活，暂无真实死链证据。报告：`workspace/outputs/raw_quality_report.{json,md}`。
- 重建检索索引：`python tools/kb_search.py index` → indexed=1648。`tools/README.md` 补充"抽取与质量维护"章节。

## 2026-07-25 | quality-rescan
- 出网恢复后复检 raw_quality.py：32 条含 source_url 文件全部 ALIVE，0 DEAD/ERROR/BLOCKED。
- 增强 `check_url()`：遇 401/403/429 自动用完整浏览器 UA 复检一次，复检 2xx 即判存活，消除反爬 403 误判（mof.gov.cn 两条 403 复检 200 确认为反爬拦截）。新增 BROWSER_UA / _do_request 辅助。
- 最终质量结论：718 文件 EMPTY 0、ERROR_PAGE 0、LOW_CONTENT 120（合法短问答仅告警）、MISSING_SOURCE_TYPE 74（手工页正常）、OK 524；URL 实检全部存活。无空页/错误页/失效 URL。报告 workspace/outputs/raw_quality_report.{json,md}。

## 2026-07-25 | architecture-cleanup
- 服务去重：`serve_kb_ui.py`（旧版静态 UI 服务，前端依赖 `kb_server.py` 的 `/api`，单独运行 UI 不可用）归档至 `archived/kb-tools-legacy/`；现仅 `kb_server.py` 占 8765 端口，消除双服务端口争用。同步将 `build_kb_ui.py` 的完成提示改为运行 `kb_server.py`。
- 归档一次性迁移脚本：将 5 个 2026-07 内容清理脚本移入 `archived/kb-tools-legacy/`（经核查无活跃脚本 import 它们）。
- 维护基线可持久化：`workspace/outputs/` 原被 gitignore，现对最新 `raw_quality_report.{json,md}` 执行 `git add -f` 强制跟踪，避免克隆即丢（用户「识别并维护」基线）。其余产物仍可经 `python tools/raw_quality.py scan` 重生。
- 文档同步：`tools/README.md` 的「知识库检索与界面」表移除已归档脚本并新增归档说明段，并修正 `kb_server.py` 锁路径描述为 `workspace/tmp/.kb_serve.lock`（此前表述滞后于实际改动）。

## 2026-07-25 | ingestion-rule
- 新增加工规则（权威落点 `WIKI.md` 自定义说明；并在 `README.md` 新资料放置规则 + 维护流程 step1 做可见性强化）：所有放入 `raw/` 的原始资料（html/htm/xml/pdf/docx/txt/csv 等）都必须先经 `tools/convert_raw_to_md.py`（或 `tools/kb.py archive-doc` / `pdf-md`）抽取为 `raw/*.md` 统一 Markdown 门面，再基于该 md 进行 wiki 结构化加工；禁止跳过 md 中间产物、直接对原文件做人工摘录式加工。固化"原文件 → md → wiki"标准管线。

## 2026-07-25 | ui-enhance
- 知识库 Web UI（`ui/index.html`）三项增强：
  1. 搜索体验：搜索框输入即时下拉建议（debounce 180ms，高亮匹配词、↑↓ 选择、Enter 打开、Esc 收起）；结果分页（每页 20，上一页/下一页 + 页码信息，后端 `/api/search` 新增 `offset` 参数并放宽为真实总数）；无结果时给更换关键词/放宽筛选的友好提示。
  2. 阅读体验：文档详情页 TOC 大纲随滚动高亮当前章节（IntersectionObserver）；顶部阅读进度条；右下返回顶部按钮；打印/导出 Markdown 按钮；原文「新标签打开」链接。
  3. 视觉交互：加载骨架屏（搜索中）；统计卡/入口卡 hover 上浮动效；`?` 唤起快捷键帮助弹层（Esc 关闭）；整体样式打磨。
- 后端 `kb_server.py` 的 `/api/search` 改造：`limit` 上限 100、新增 `offset: int = Query(0, ge=0)`、去掉内部 `LIMIT 200` 硬截断、`results` 改用 `rows[offset:offset+limit]`、`total` 返回真实命中数（向前兼容，offset 默认 0）。
- 验证：本环境命令执行工具（Bash/PowerShell）异常不可用，未能启动服务做运行验证；已对 `index.html` 与 `kb_server.py` 做人工静态复查，函数定义/调用衔接一致、无语法断层。请本地 `python knowledge-base/CPA-ZH/tools/kb_server.py` 后访问 http://127.0.0.1:8765/ 确认。

## 2026-07-25 | raw-nav-strip
- 问题：用户在「原文.准则文本」下打开 `企业会计准则-基本准则.html` 时，UI 原文查看页（iframe）原样渲染了 mof.gov.cn 模板的整块导航（顶部 logo + 部门名 + 站内搜索 + 当前位置面包屑 + 返回主站 + 右侧二维码悬浮栏）。`strip_boilerplate` 文本规则虽能把已抽好的 `raw/*.md` 剥干净，但**原始 HTML 直接进 iframe** 时导航依然在场。
- 修复（两处联动，让"抽取 / 原文查看"都只剩正文）：
  1. `tools/convert_raw_to_md.py` 的 `NAV_CLASS_HINTS` 补 8 个 mof 模板类：`popfr / logodiv / zzname / zz_serach / searchinput / buttoninput / returnmain / dangqian`，覆盖 logo / 部门名 / 搜索框 / 当前位置 / 返回主站 / 右侧二维码栏；顺便修了一个潜伏 bug——`decompose_nav` 在 `el.attrs` 为 `None` 的元素上 `el.get("class", [])` 会 AttributeError，改成显式判 `if not am: continue`。
  2. `knowledge-base/CPA-ZH/tools/kb_server.py` 的 `/api/raw`：HTML 文件先经 `decompose_nav` 剥离再返回（HTMLResponse），与抽取器共用同一套规则；非 HTML 走原 `FileResponse`；`decompose_nav` 通过 `sys.path` 注入仓库根 `tools/` 后从 `convert_raw_to_md` 导入，导入失败则降级原样返回，不影响可用性。
- 验证（用本环境实操，因内联 `-c` 规避了沙箱 `/d/` 改写）：
  - 离线：`decompose_nav` 处理基本准则 HTML 后，8 个目标类计数 1→0，`title_con`/`TRS_Editor` 保留 1；正文文本中「返回主站/财政部微信/当前位置/请输入关键字/条法司」全部 False；HTML 体积 18633→11633。
  - 端到端：杀掉旧 8765 服务（PID 3904）→ `start_kb.main()` 用新代码拉起 → `GET /api/raw?path=raw/_archive/.../企业会计准则-基本准则.html`：返回 11633 字节，导航关键词全部 False，`title_con`/`TRS_Editor`/`中华人民共和国财政部令第76号` 保留 True，`/api/search` 同时验证仍返回 424 字节正常结果。注：响应 HTML 中仍含 `popfr` 字符串，是 `<style>` 里残留的 `.popfr{...}` CSS 规则（指向已被移除的元素，渲染无副作用），未做清理避免误伤共享样式。
- 范围：活跃 `raw/**/*.md` 经 `grep` 扫描「返回主站 / 财政部微信 / 网站标识码 / 当前位置 / 条法司」残留为 0 条，故无需对存量 .md 做回填重抽；新规则主要保护后续新增的 mof 模板类抓取 + UI 原文查看体验。

## 2026-07-25 | heading-demote（规则+回填）

- 问题：`tools/format_legal_md.py` 的 `format_general()` 旧规则把 "1.xxx"/"1、xxx"开头的行无差别升级为 `## 二级标题`，但法规问答里的"处理方式条款"刚好以这种形式出现且长达数百字（如「企业会计准则解释第7号」5 条"母公司将子公司改为分公司的会计处理"），造成正文被错误放大加粗。
- 修复（两步）：
  1. `tools/format_legal_md.py` 抽出 `is_title_candidate()`（≤40字、无句末问号感叹号分号、逗号顿号总数 ≤1），并在 `format_general()` 中加"降级"分支：扫描已存在的 `## 1.xxx` 行，不满足标题候选特征的，去掉 `## ` 前缀回归正文。
  2. 新增 `tools/demote_bad_h2.py`（一次性回滚脚本）：复用 `is_title_candidate` 精准降级，不动升级规则，避免对其他内容的反向改动。
- 验证（用本环境实跑，DRY + 抽样 + APPLY）：
  - DRY 扫描 718 个 md，命中 58 个、降级 1353 处，0 反向改动。
  - 抽样：审计准则 1141/1211/1421/1521 应用指南、增值税会计处理规定等 Top 10 文件的 KEEP/DEMOTE 判断全部正确（短 Q&A 标题保留、长条款/问句/多逗号段降级）。
  - APPLY 后复检截图文件「关于印发-企业会计准则解释第7号-的通知.html.md」：`## N.xxx` 计数 8→0；正文行 `1．原为非同一控制下...` 存在并保持原文连续。
- 范围：58 个 md，分布在 `standards/audit/pdfs/`（审计准则应用指南 21 份占大头）、`standards/accounting/interpretations-pages/`（4 份准则解释）、`standards/accounting/other-rules-pages/`（增值税会计处理规定 26 处）、`outlines/practice-question-bank-*`（习题答案解析 21 处）。
- 知识库 UI 无需重启（kb_server 直接读 md 静态托管），浏览器刷新即可看到截图里那段「1、原为非同一控制下企业合并取得...」恢复为正文样式。

## 2026-07-25 | inline-paren-merge（规则+回填）

- 问题：`tools/format_legal_md.py` 的 `format_legal()` 第 4 条规则（"（X）转 bullet"）在正文中间也会触发，把法律/会计准则里"按本条（一）至（二）项规定"这种**行中引用片段**切成独立 bullet，导致正文被切碎（如「持有待售」第42号准则 7 个 inline 引用段被切到独立行）。
- 修复（两步）：
  1. `tools/format_legal_md.py` 的 `format_legal()` 第 4 条规则改为**仅匹配行首/段首**（`(^|\n)[ \t\u3000]*（X）`）才升级为 bullet；行中的 "（X）" 保持内联，防新内容继续错。
  2. 新增 `tools/merge_inline_parens.py`（一次性回滚脚本）：识别"被错误升级的 inline 引用片段"（特征：bullet body ≤ 60 字 + 以"（中文数字）"开头 + 命中三种模式之一——末尾连词"和/或/，/、/至"、"（X）项/条款/规定"上下文、"（X）至（Y）"范围），合并到上一段尾部，多轮扫描直到稳定。
- 验证：
  - DRY 扫描 718 个 md，命中 41 个、合并 225 处 inline 引用片段、0 误伤独立项（"履行/最终确定/消除..." 等以动词开头的独立项保留为 bullet）。
  - 抽样：「持有待售」第42号 11 处合并到位，"并按照本条（一）至（三）的规定进行披露" 连续行生成；伦理独立性应用指南 36 处合并，"第（一）项指出..." "第（二）款..." 型连续行出现。
  - APPLY 后复检截图文件 `remaining inline_refs (line-only)= 0`。
- 范围：伦理独立性 3 份（96 处）+ 审计准则 1141/1211/1321 等 4 份（28 处）+ 会计准则 25/37/42 等 4 份（37 处）+ 其它 30 份。
- 刷新浏览器即可看到截图红框里那段「（十）归属于母公司...并按照本条（一）至（三）的规定进行披露。企业专为转售而取得的持有待售的子公司，应当按照本条（二）至（五）和（十）的规定进行披露。」恢复为正常连续正文。

## 2026-07-26 | heading-swallow 回滚（规则守卫）

- 问题：昨日 `merge_inline_parens.py` 把 `**第二十五条**（六）、（七）、（九）、（十）的规定披露可比会计期间的信息。` 误判为 inline 引用片段，合并到 `**第二十七条**` 末尾，吃掉了行 100 和 106 的 `**第二十五条**`（同时第二十七/二十九条被切碎成两行：`并按照本准则` 单独成行 + `**第二十五条**（六）...` 单独成行）。
- 根因：`looks_like_inline_ref` 无守卫，把 `**第X条**` 粗体文章标题伪 bullet 也认作 inline 引用。
- 修复（三处）：
  1. 精准回滚截图文件（`企业会计准则第42号-持有待售的非流动资产-处置组和终止经营.html.md`）：剥掉两处 `**第二十五条**` 残片并把"按照本准则\n\n（六）..."两行合并回 27/29 条单段。
  2. `tools/merge_inline_parens.py` 的 `looks_like_inline_ref` 加守卫：body 以 `**第X条**` 开头则不算 inline 引用。
  3. `tools/format_legal_md.py` 的 `format_legal()` 第 4 条规则加同等守卫：升级 bullet 时窥探后 30 字，含 `**第X条**` 跳过升级，防新内容继续错。
- 验证：全量扫描 718 个 md 中同模式（"（X）...**第Y条**"）= 0 处残留；新规则对截图文件 merged=0（不再误合并）；所有真标题 `**第二十五条**` 等保留；27/29 条恢复成单段完整句子（"按照本准则（六）、（七）、（九）、（十）的规定披露可比会计期间的信息。" 和 "按照本准则（六）至（十）的规定进行披露。"）。
- 范围：仅 1 个文件（42 号准则）受影响，无其它文件需要回填。

## 2026-07-26 | no-cache 头 + 重启（修浏览器缓存坑）

- 问题：用户反馈"已修的 27/29 条未生效"，实测文件已是修好的（行 98/102 完整单段），`/api/raw` 也返回修好的内容，但浏览器看到的是旧版——根因是 `/api/raw` 和 `/api/doc` 没加 `Cache-Control`，浏览器（或中间层）缓存了旧响应。
- 修复：
  1. `kb_server.py` 的 `/api/raw` 和 `/api/doc` 端点统一加 `Cache-Control: no-store, must-revalidate` + `Pragma: no-cache`。
  2. 旧 8765 进程（PID 35324）taskkill，新进程已起，验证 `Cache-Control` 头生效。
- 验证：`/api/raw?path=raw/standards/accounting/standards-pages/企业会计准则第42号-...md` 返回 status=200、`Cache-Control: no-store, must-revalidate`、第二十七/二十九段已为单段完整句。
- 后续：用户需在浏览器硬刷（Ctrl+Shift+R）一次以丢弃旧缓存；之后任何 md 改动不会被缓存。

## 2026-07-26 | 全局 no-store 中间件（彻底修浏览器缓存）

- 问题：磁盘文件已修好、`/api/raw` 也返回修好的，但用户浏览器仍显示旧版（25/27 条切碎）。
- 根因深挖：`kb_server.py` 把 `/raw` `/wiki` `/ui` 用 `StaticFiles` 直接挂载（行 320-322），"新标签看原文"按钮（index.html:659 `<a href="/raw/...">`）和 HTML 快照（行 729 `staticUrl=/raw/...`）都走 `/raw/...` 静态路由。**该路由此前没有任何缓存头**，浏览器按启发式缓存了旧版原文响应；而 showRaw 的 markdown 渲染走 `/api/raw`（之前加过 no-store），但 user 实际点开的可能正是静态路由的旧缓存。
- 修复：在 `kb_server.py` 加全局 ASGI 中间件 `_no_store`，对所有响应（含 StaticFiles 挂载与 `/api/*`）统一加 `Cache-Control: no-store, must-revalidate` + `Pragma: no-cache`；仅 `/api/docs` 与 `/api/openapi.json` 放行。
- 验证：重启后 /api/raw、/raw/static、/ui/index.html 三者均返回 status=200 + `Cache-Control: no-store, must-revalidate`；第二十七条完整单段、`第二十七条→第二十八条` 连续均 True。
- 后续建议：用户请**开无痕窗口**（最确定的无缓存验证）或硬刷（Ctrl+Shift+R）一次。若无痕窗口仍显示旧的，说明浏览器连的不是本机 8765（需排查 URL/端口）。

## 2026-07-26 | 一键入口修复（启动器保证拿最新版）

- 问题：用户反馈「一键入口（start-kb.bat）进去还是旧版」。
- 根因：`start_kb.py` 原逻辑是「端口在跑就直接复用」，但若后台是改 no-store 之前启动的旧进程，它不会重启，浏览器命中无防缓存头的旧服务；且 `webbrowser.open(URL)` 复用已打开的旧标签页、不重新请求，导致旧 DOM 一直显示。
- 修复（重写 `start_kb.py`）：
  1. 复用前先探测运行中的服务是否最新——`GET /` 看响应头是否含 `Cache-Control: no-store`（`_probe_fresh()`）；是最新才复用。
  2. 端口被占用但服务不是最新（旧进程/旧代码）→ `_kill_existing()` 杀掉旧实例（优先用记录的 PID，再用 netstat 按端口兜底），再拉起最新 `kb_server.py`。
  3. 打开浏览器时强制带缓存破坏参数 `?_=<毫秒时间戳>`，避免浏览器复用旧标签页的陈旧 DOM。
  4. `start-kb.bat` 末行加 `if errorlevel 1 pause`，异常时保留窗口便于排错。
- 验证：
  - 复用分支（8765 已是最新）：`main()` 走「知识库已在运行（已是最新）」、不杀服务、端口保持 alive、no-store=True。
  - 重启分支（隔离端口 8799，强制 `_probe_fresh=False` 模拟旧实例）：`main()` 走到杀掉重拉、alive=True、fresh(no-store)=True，清理后端口释放。
  - 空端口拉起（8765 当前未运行）：`main()` 直接拉起、alive=True、fresh(no-store)=True。
- 结论：现在无论后台是旧进程还是空端口，双击 start-kb.bat 都保证打开的是最新版（最新代码 + 强制重新导航）。
