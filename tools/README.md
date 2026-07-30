# tools 脚本说明

`tools/` 保存项目自动化脚本。CPA-ZH 维护优先使用统一入口 `kb.py`；公共 CLI 转发逻辑放在 `kb_cli_support.py`，具体脚本保留为兼容入口，也方便单独调试。

知识库内的工具注册表见 `knowledge-base/CPA-ZH/wiki/concepts/ai-coding-tool-registry.md`。新增工具时，应同步维护该注册表、本文件和对应 wiki 工具页。

## 统一入口

### 分离式浏览器运行

`start_kb_api.py` 启动根目录 `backend/` 的只读 FastAPI 服务，默认监听 `127.0.0.1:8765`；Vue 前端在根目录 `frontend/` 通过 `npm run dev` 单独启动。

根目录的 `start-kb.bat` 和 `stop-kb.bat` 是面向本机用户的双击入口；对应实现为 `tools/start_kb_api.py` 和 `tools/stop_kb.py`，两者均按其自身位置推导项目根目录。

```powershell
.\.venv\Scripts\python.exe tools\kb.py health
.\.venv\Scripts\python.exe tools\kb.py verify
.\.venv\Scripts\python.exe tools\kb.py search "收入确认"
.\.venv\Scripts\python.exe tools\kb.py cache build
.\.venv\Scripts\python.exe tools\kb.py index
.\.venv\Scripts\python.exe tools\kb.py readme
.\.venv\Scripts\python.exe tools\kb.py ingest-local --source "D:\path\to\files" --raw-subdir "cases/new-batch" --batch-slug "new-batch"
.\.venv\Scripts\python.exe tools\kb.py case-card --source "knowledge-base/CPA-ZH/raw/cases/batch/case.docx" --slug "draft-case"
.\.venv\Scripts\python.exe tools\kb.py case-index --write-report
.\.venv\Scripts\python.exe tools\kb.py qa-capture --question "客户有售后回购条款，能不能确认收入？" --answer "需要围绕控制权是否转移、回购条款实质和客户是否存在重大经济动因判断。"
.\.venv\Scripts\python.exe tools\kb.py qa-summary-index --source "knowledge-base/CPA-ZH/cache/pdf-markdown/files/official-a5f41e751162.md" --commit
.\.venv\Scripts\python.exe tools\kb.py qa-batch-process --source "knowledge-base/CPA-ZH/cache/pdf-markdown/files/official-a5f41e751162.md" --max-cards 999 --commit
.\.venv\Scripts\python.exe tools\kb.py qa-feature-cases --commit
.\.venv\Scripts\python.exe tools\kb.py archive-doc --source "D:\path\to\official.pdf" --raw-subdir "policies/new-batch" --slug "official-doc" --title "文件标题"
.\.venv\Scripts\python.exe tools\kb.py pdf-md --source "knowledge-base\CPA-ZH\raw" --engine auto
```

## 写入模式

| 类型 | 命令 | 说明 |
|---|---|---|
| 只读 | `health`、`verify`、`manifest`、`search`、`stats`、`sources summary`、`case-index` | 查询、检查当前状态或打印建议 |
| 重建报告 | `index`、`cache build`、`schema --write-report`、`sources write-report`、`case-index --write-report`、`readme` | 可重复生成索引、缓存、建议报告或仪表盘 |
| 显式写入 | `ingest-local --commit`、`case-card --commit`、`qa-capture --commit`、`qa-summary-index --commit`、`qa-batch-process --commit`、`qa-feature-cases --commit`、`archive-doc --commit`、`pdf-md --commit` | 新增 raw、wiki 或转换缓存文件，执行前先 dry-run |

## CPA-ZH 维护脚本

| 脚本 | 职责 |
|---|---|
| `kb.py` | 统一维护入口，路由到下列脚本。 |
| `kb_cli_support.py` | 统一入口共享辅助：脚本转发、可选参数和 flag 组装。 |
| `kb_health_check.py` | 一键体检：manifest、wiki 内链、检索索引、文本缓存、README 统计。 |
| `verify_cpa_zh_delivery.py` | 完整交付门禁：导航树新鲜度、Python/API 契约测试、知识库体检、前端测试和生产构建；`kb.py verify --skip-frontend` 可用于不含前端的快速检查。 |
| `kb_search.py` | 构建和查询本地 SQLite 检索索引。 |
| `kb_text_cache.py` | 抽取 raw 文件正文并缓存，供检索复用。 |
| `kb_manifest_audit.py` | 检查 raw manifest 与本地文件、metadata 的一致性。 |
| `kb_link_check.py` | 汇总或联网检查官方链接。 |
| `kb_source_status.py` | 生成来源状态统计和 wiki 仪表盘。 |
| `kb_update_readme_stats.py` | 刷新 CPA-ZH README 中的统计数字。 |
| `kb_ingest_local.py` | 本地入库助手：dry-run 预览或复制本地文件到 raw，并生成 manifest、metadata、source-url。 |
| `kb_case_card.py` | 案例卡片生成助手：从本地原文生成 `wiki/cases/` 案例卡片草稿。 |
| `kb_case_index_suggest.py` | 案例主题索引回挂助手：扫描案例卡片并生成主题、准则、风险和底稿用途回挂建议。 |
| `kb_qa_capture.py` | 本地问答日志回写助手：把有价值的问答保存到 `wiki/questions/`，并建议 related 链接。 |
| `kb_qa_summary_index.py` | 长篇答疑汇总拆分工作台助手：从已抽取 Markdown 中识别问答标题，生成候选问题池、主题分类和优先拆分队列。 |
| `kb_qa_batch_process.py` | 长篇答疑汇总批量案例加工助手：将问答条目分流为草稿案例卡片、问答沉淀候选和主题素材，并生成分类总览。 |
| `kb_feature_qa_cases.py` | 主题精选案例生成助手：从陈老师答疑草稿案例中按每个主题生成 1 张精选代表案例卡片。 |
| `kb_archive_doc.py` | 原文归档助手：归档单个 PDF/HTML/DOCX 原文为 `official.*`，并生成 manifest、metadata、source-url。 |
| `kb_pdf_to_markdown.py` | PDF 转 Markdown助手：用 PyMuPDF、pdfplumber、pdfminer、pypdf 多引擎抽取 PDF，转成 Markdown 并标记文本质量。 |
| `kb_schema_check.py` | 检查 wiki 概念页 frontmatter schema 一致性，生成升级仪表盘 `wiki/concepts/kb-section-upgrade-dashboard.md`。 |
| `import_local_case_batch.py` | 导入本地案例批次。 |

## 知识页生成脚本

| 脚本 | 职责 |
|---|---|
| `generate_core_law_article_pages.py` | 生成核心法律条款页。 |
| `generate_accounting_standards_number_index.py` | 生成企业会计准则编号索引。 |
| `generate_accounting_interpretation_pages.py` | 生成会计准则解释页。 |
| `generate_cicpa_professional_standards_number_index.py` | 生成注册会计师执业准则编号索引。 |
| `generate_policy_documents_section.py` | 生成政策文件板块。 |
| `generate_first_section_topic_matrix.py` | 生成第一板块专题矩阵。 |
| `generate_first_section_law_maintenance_pages.py` | 生成法律维护页。 |
| `generate_accounting_standards_calibration.py` | 生成会计准则校准资料。 |
| `generate_accounting_unmapped_bucket_pages.py` | 生成未映射准则资料页。 |

## 内容加工脚本

| 脚本 | 职责 |
|---|---|
| `apply_accounting_calibration_to_pages.py` | 将会计准则校准结果写入页面。 |
| `apply_core_law_practice_frameworks.py` | 给核心法律页补实践框架。 |
| `apply_first_section_judgment_frameworks.py` | 给第一板块页面补判断框架。 |
| `archive_policy_documents.py` | 归档政策文件原文。 |
| `archive_third_section_documents.py` | 归档第三板块资料。 |
| `docx_to_markdown.py` | 将 docx 转为 Markdown。 |
| `polish_audit_doc.py` | 审计文档润色辅助。 |
| `format_legal_md.py` | 把 `raw/` 下已转换 `.md` 重排成「参考法规版式」语义化结构（`--apply` 写入，`--from-archive` 从 `_archive` 重抽），幂等。 |

## 课程构建

| 脚本 | 职责 |
|---|---|
| `build_course_html.js` | 构建课程 HTML。 |
| `build_course_html_organized.js` | 按整理后的课程结构构建 HTML。 |

## 知识库分类与质量工具

知识库的分类、质量评估和交付辅助工具统一位于仓库根 `tools/`，不在 `knowledge-base/CPA-ZH/` 下保留脚本。优先通过 `kb.py` 执行有对应子命令的维护动作。

| 脚本 | 职责 |
|---|---|
| `kb_common.py` | 分类、内容成熟度和检索评估共享的元数据、Markdown 和路径辅助。 |
| `build_golden_content.py` | 生成可复核的会计判断专题与黄金案例集。 |
| `classify_wiki.py` | 语义分类回填：按路径规则为 wiki/raw 推断 domain/topic 并写回 frontmatter，生成 `search/navigation-tree.json`。子命令 `report`/`apply`/`build`。 |
| `kb_eval.py` | 评估黄金问题集的本地检索效果。 |
| `kb_maturity.py` | 生成内容成熟度仪表盘，或回填成熟度元数据。 |
| `wiki_lint.py` | wiki 断链/孤立页检查：扫描所有 `[[…]]` 链接与未被引用的页面。 |
| `version_consistency_scan.py` | 按关键字（如「注册会计师法」）扫描全 wiki，输出语义版本一致性报告。 |
| `connect_orphan_standards.py` | 将指定的历史孤儿准则页接入主题树；仅用于对应的 2026-07 修复。 |

分类树构建：

```powershell
.\.venv\Scripts\python.exe tools\kb.py classify build
```

> **已归档（一次性 / 旧版）**：`build_kb_ui.js`、`serve_kb_ui.py` 及 2026-07 的 `reorg_*` 清理脚本仅保留历史参考；活跃浏览器使用根目录 `frontend/` 和 `backend/`。

## 抽取与质量维护（tools/ 根目录）

| 脚本 | 职责 |
|---|---|
| `convert_raw_to_md.py` | 把 raw/ 下原文件（html/htm/xml/pdf/docx/txt/csv）抽取为统一 Markdown 门面并归档原文。新增 `--clean` 模式：对已转换的 `raw/*.md` 原地后处理清洗（剥离财政部网站导航/页脚模板垃圾；长行仅剥离子串以保留被融合的正文）+ 补缺失 `source_type`，幂等，不动 `_archive` 原文。 |
| `raw_quality.py` | 抽取质量扫描：`scan` 遍历 `raw/*.md`（跳 `_archive/_trash/_maintenance`），判定 `EMPTY`/`ERROR_PAGE`/`LOW_CONTENT`/`MISSING_SOURCE_TYPE`，并联网实检 `source_url`（`--no-check-urls` 关闭），产出 `workspace/outputs/raw_quality_report.json` 与 `.md` 维护清单。 |

## 外部来源搜索

| 脚本 | 职责 |
|---|---|
| `search_policy_official_links.py` | 搜索政策文件官方链接。 |
| `search_third_section_official_links.py` | 搜索第三板块官方链接。 |
| `search_third_section_bing_rss.py` | 通过 Bing RSS 辅助搜索第三板块资料。 |
