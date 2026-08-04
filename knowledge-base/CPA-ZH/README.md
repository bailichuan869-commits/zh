# CPA-ZH 知识库

CPA-ZH 是围绕中国注册会计师行业建立的本地知识库，用于沉淀法规准则、政策文件、职业道德与独立性要求、审计实务技能和案例分析。

截至 2026-08-04，知识库已经具备“原文归档 + 结构化 wiki + 本地检索 + 案例卡片”的基础形态。

新手优先入口：

- `wiki/concepts/kb-user-guide.md` - CPA-ZH 使用手册，说明结构、检索、新增资料、案例使用和维护命令。
- `wiki/index.md` - 知识库总索引。
- `wiki/concepts/kb-maintenance-workflow.md` - 维护工作流。
- `wiki/concepts/source-status-dashboard.md` - 来源状态仪表盘，查看待 OCR、官方链接和文本缓存状态。
- `wiki/concepts/kb-section-upgrade-dashboard.md` - 分板块技术升级仪表盘，查看五大板块的元数据、来源结构和后续升级重点。
- `../../tools/kb.py` - 统一维护入口，封装检索、缓存、索引、分板块治理检查、体检和 README 统计刷新。

## 当前状态


| 项目 | 数量或状态 |
|---|---:|
| wiki 页面 | 886 |
| raw 原始文件 | 4562 |
| manifest 批次 | 8 |
| 本地检索索引记录 | 1538 |
| 实务案例卡片 | 24 |
| wiki 内链状态 | 最近检查为 0 缺失 |
| Python 运行方式 | 统一使用工作区虚拟环境 `.venv` |

## 最近重大更新（2026-07-23）

- **《注册会计师法》2026 修订草案已接入知识库**：依据主席令第七十八号（2026-06-26 通过、2027-01-01 施行）二十七条修改决定，手工套用 2014 修正版原文生成 8 章 60 条草案全文，归档于 `raw/laws/中华人民共和国注册会计师法-2026-草案.md`，可浏览页见 `wiki/concepts/laws/cpa-law-2026-draft.md`。草案为推演文本，正式引用以官方重新公布的重排版为准。
- **旧版（2014 修正）条款页已排除出检索**：46 个旧条款页、1 个旧条款目录页与旧法 raw 全文已从本地检索索引移除（文件物理保留，仍可经 `wiki/concepts/law-cpa.md` 的历史版本链接访问）。检索“注册会计师法”现只返回 2026 修订草案及主入口页。排除逻辑见 `tools/kb_search.py` 的 `SUPERSEDED_SEARCH_EXCLUDES`。
- 相关页面：修改决定归档 `raw/laws/注册会计师法-修改决定-2026.md`、要点对照 `wiki/concepts/laws/cpa-law/2026-amendment-highlights.md`、来源核验 `wiki/sources/cpa-law-amendment-2026.md`。

## 最近重大更新（2026-07-24）

- **陈老师/陈版主答疑已转为 skills 路由**：仓库内不再保留陈老师答疑汇总、派生案例卡片或专题索引；涉及陈版主历史答疑或陈奕蔚式准则判断时，统一走正式安装的 `chen-yiwei-perspective` 与 `chenyiwei-bbs` skills。

## 目录结构

```text
knowledge-base/CPA-ZH/
├── README.md                 # 本说明文件
├── WIKI.md                   # 知识库配置、分类、质量规则
├── source-registry.yml       # 官方来源注册表
├── raw/                      # 原始资料层，保留下载或导入文件
├── wiki/                     # 结构化知识层
│   ├── index.md              # 总索引
│   ├── overview.md           # 总览
│   ├── concepts/             # 概念、专题、规则框架
│   ├── sources/              # 来源批次和归档说明
│   ├── cases/                # 加工后的案例卡片
│   └── questions/            # 本地问答回写页
├── cache/
│   └── text/                 # raw 文件文本抽取缓存
└── search/
    └── kb_search.sqlite      # 本地检索索引
```

## 已建设板块

### 一、行业重要法规与准则

已维护四部核心法律、企业会计准则体系、中国注册会计师执业准则体系，并建立条款级、准则编号级和实务专题级入口。

核心入口：

- `wiki/concepts/regulations-and-standards.md`
- `wiki/concepts/first-section-completion-map.md`
- `wiki/concepts/accounting-standards-system.md`
- `wiki/concepts/audit-standards-system.md`
- `wiki/concepts/first-section-topic-matrix.md`

### 二、行业重要政策性文件

已完成 7 份政策性文件的原文归档、版本效力跟踪和执行检查清单。

核心入口：

- `wiki/concepts/policy-documents.md`
- `wiki/concepts/policy-version-validity-tracker.md`
- `wiki/concepts/policy-execution-checklist.md`
- `raw/policies/second-section/manifest.json`

### 三、行业史与职业道德

已归档中注协职业道德规范专题页、职业道德守则、独立性准则第1号及 2026 应用指南，并建立框架页。

核心入口：

- `wiki/concepts/history-ethics-independence.md`
- `wiki/concepts/ethics-code.md`
- `wiki/concepts/independence-standard-1.md`
- `raw/ethics/third-section/manifest.json`

### 四、实务技能与案例分析

第四板块已启动。已导入 2026 年 7 月第一期 5 个实务案例，加工为 5 张案例卡片。涉及陈老师/陈版主答疑的内容不再在知识库中沉淀，相关问题改走 skills 路由。

核心入口：

- `wiki/concepts/practice-skills-cases.md`
- `wiki/concepts/case-analysis.md`
- `wiki/concepts/case-topic-index.md`
- `wiki/concepts/case-index-suggestion-report.md`
- `wiki/sources/case-batch-2026-07-first-issue.md`
- `wiki/cases/`

已加工案例：

- `wiki/cases/2026-07-first-issue-long-term-equity-investment-confirmation.md`
- `wiki/cases/2026-07-first-issue-temporary-fixed-asset-tax-difference.md`
- `wiki/cases/2026-07-first-issue-government-grant-free-use-equipment.md`
- `wiki/cases/2026-07-first-issue-equipment-sales-revenue-recognition.md`
- `wiki/cases/2026-07-first-issue-overseas-sales-revenue-recognition.md`

已归档待拆分资料：

### 五、AI 编程与自动化

已导入 `D:\ai-coding\讲义` 下 58 份 Markdown 讲义，按 Agent、Python、VBA 插件三条学习线归档，用于支撑审计自动化、知识库维护、Excel 工具和 Agent 工作流建设。

核心入口：

- `wiki/concepts/ai-coding-lectures.md`
- `wiki/concepts/ai-coding-agent-lectures.md`
- `wiki/concepts/ai-coding-python-lectures.md`
- `wiki/concepts/ai-coding-vba-addin-lectures.md`
- `wiki/concepts/ai-coding-tool-template-library.md`
- `wiki/concepts/ai-coding-audit-automation-scenario-matrix.md`
- `wiki/concepts/ai-coding-risk-control-checklist.md`
- `wiki/concepts/ai-coding-project-roadmap.md`
- `wiki/concepts/ai-coding-tool-registry.md`
- `wiki/concepts/cpa-zh-local-ingest-helper.md`
- `wiki/concepts/cpa-zh-case-card-helper.md`
- `wiki/concepts/cpa-zh-case-index-helper.md`
- `wiki/concepts/cpa-zh-qa-capture-helper.md`
- `wiki/concepts/cpa-zh-archive-doc-helper.md`
- `wiki/concepts/cpa-zh-pdf-to-markdown-helper.md`
- `wiki/sources/ai-coding-lectures-archive-2026-07-09.md`
- `raw/lectures/ai-coding-lectures-2026-07-09/manifest.json`

## 本地检索

## 前后端浏览器

浏览器采用独立前后端结构：仓库根目录的 `backend/` 是只读 FastAPI API，`frontend/` 是 Vue 3 + Vite + Ant Design Vue 应用。后端默认绑定 `127.0.0.1:8765`，前端开发服务默认绑定 `127.0.0.1:5173`。

```powershell
# 终端一：从仓库根目录启动 API
.\.venv\Scripts\python.exe tools\start_kb_api.py

# 终端二：启动 Vue 前端
cd frontend
npm install
npm run dev
```

新版 API 统一位于 `/api/v1`，覆盖健康检查、统计、分类树、检索、知识页、反向链接和 raw 原文读取。所有写入、缓存、索引和质量检查继续经 `tools/kb.py` 执行。

旧的静态单页 UI、索引构建脚本和静态服务已删除；活跃浏览器仅使用根目录的前后端应用。

所有 Python 命令统一使用工作区虚拟环境：

```powershell
.\.venv\Scripts\python.exe
```

常用检索命令：

```powershell
.\.venv\Scripts\python.exe tools\kb.py search "独立性准则"
.\.venv\Scripts\python.exe tools\kb.py search "收入确认"
.\.venv\Scripts\python.exe tools\kb.py search "政府补助 免费使用设备"
.\.venv\Scripts\python.exe tools\kb.py search "长期股权投资 内部重组"
```

重建索引：

```powershell
.\.venv\Scripts\python.exe tools\kb.py index
```

查看索引统计：

```powershell
.\.venv\Scripts\python.exe tools\kb.py stats
```

构建或刷新 raw 文本缓存：

```powershell
.\.venv\Scripts\python.exe tools\kb.py cache build
.\.venv\Scripts\python.exe tools\kb.py cache stats
```

本地资料入库预览：

```powershell
.\.venv\Scripts\python.exe tools\kb.py ingest-local --source "D:\path\to\files" --raw-subdir "cases/new-batch" --batch-slug "new-batch"
```

案例卡片草稿预览：

```powershell
.\.venv\Scripts\python.exe tools\kb.py case-card --source "knowledge-base/CPA-ZH/raw/cases/batch/case.docx" --slug "draft-case"
```

案例主题索引建议：

```powershell
.\.venv\Scripts\python.exe tools\kb.py case-index
.\.venv\Scripts\python.exe tools\kb.py case-index --write-report
```

本地问答日志回写预览：

```powershell
.\.venv\Scripts\python.exe tools\kb.py qa-capture --question "客户有售后回购条款，能不能确认收入？" --answer "需要围绕控制权是否转移、回购条款实质和客户是否存在重大经济动因判断。"
```

单个原文归档预览：

```powershell
.\.venv\Scripts\python.exe tools\kb.py archive-doc --source "D:\path\to\official.pdf" --raw-subdir "policies/new-batch" --slug "official-doc" --title "文件标题"
```

PDF 转 Markdown 预览：

```powershell
.\.venv\Scripts\python.exe tools\kb.py pdf-md --source "knowledge-base\CPA-ZH\raw"
```

`tools/kb.py` 是统一入口；原来的 `tools/kb_search.py` 和 `tools/kb_text_cache.py` 仍可直接使用。`kb.py index` 会优先复用 `cache/text/` 中的新鲜缓存；当缓存缺失或原文件变更时，才现场抽取正文。

当前索引构成：

| 类型 | 数量 |
|---|---:|
| pdf-markdown | 97 |
| raw-file | 503 |
| raw-manifest | 101 |
| wiki | 837 |
| total | 1538 |

> 说明：wiki 有效页面 793（不含暂存区 `_trash` 与维护区 `_maintenance`）。其中 47 个旧《注册会计师法》页面与 1 个旧法 raw 全文早已排除出检索索引（见 `SUPERSEDED_SEARCH_EXCLUDES`）；历史专题拆分页及维护控制页已不再进入索引。raw-file 仍为 651。

## 归档与审计

一键体检：

```powershell
.\.venv\Scripts\python.exe tools\kb.py health
```

manifest 审计：

```powershell
.\.venv\Scripts\python.exe tools\kb.py manifest
```

分板块技术升级检查：

```powershell
.\.venv\Scripts\python.exe tools\kb.py schema
.\.venv\Scripts\python.exe tools\kb.py schema --write-report
```

当前 manifest：

| manifest | 条目 |
|---|---:|
| `raw/cases/2026-07-first-issue/manifest.json` | 5 |
| `raw/cases/2026-08-first-issue-second-seminar/manifest.json` | 4 |
| `raw/ethics/third-section/manifest.json` | 24 |
| `raw/lectures/ai-coding-lectures-2026-07-09/manifest.json` | 58 |
| `raw/outlines/practice-question-bank-2026-07-13/manifest.json` | 1 |
| `raw/policies/issuance-guidance/manifest.json` | 1 |
| `raw/policies/second-section/manifest.json` | 7 |
| `raw/sources/challenge-knowledge-source-summary-2026-07-13/manifest.json` | 1 |

官方链接汇总：

```powershell
.\.venv\Scripts\python.exe tools\kb.py links
```

联网检查链接时使用：

```powershell
.\.venv\Scripts\python.exe tools\kb.py links --include-wiki --check
```

刷新 README 统计：

```powershell
.\.venv\Scripts\python.exe tools\kb.py readme
```

## 新资料放置规则

原始资料统一放入 `raw/`，不要直接覆盖 wiki 页面。

- 原文件须先抽取为 Markdown 再加工：所有原始资料都需经抽取生成 `raw/*.md` 门面后再做 wiki 加工（规则详见 `WIKI.md` 自定义说明）；不经抽取、直接对原文件做人工加工视为违规。

建议位置：

```text
raw/laws/          法律法规原文
raw/standards/     会计准则、审计准则、应用指南、解释、问答
raw/policies/      政策性文件
raw/ethics/        职业道德、独立性准则
raw/cases/         实务案例、项目复盘、监管案例
raw/lectures/      讲义、工具课程、自动化学习资料
```

加工后的知识页放入：

```text
wiki/concepts/     规则、框架、专题
wiki/sources/      来源批次说明
wiki/cases/        案例卡片
```

## 维护流程

1. 先把原始文件放入 `raw/`，并抽取为 `raw/*.md` 门面（见 `WIKI.md` 原文件抽取规则）。
2. 为批次建立或更新 `manifest.json`。
3. 在 `wiki/sources/` 建来源批次页。
4. 在 `wiki/concepts/` 或 `wiki/cases/` 生成结构化页面。
5. 更新 `wiki/index.md` 和 `wiki/log.md`。
6. 构建或刷新 raw 文本缓存。
7. 重建本地检索索引。
8. 生成分板块技术升级仪表盘。
9. 刷新 README 统计。
10. 运行一键体检。
11. 更新来源状态仪表盘。
12. 抽查关键词检索结果。

详细流程见：

- `wiki/concepts/kb-maintenance-workflow.md`

## 质量原则

- 法规、准则、政策优先使用官方来源。
- 原文文件保留在 `raw/`，wiki 页面只做结构化加工。
- 重要页面应写明官方链接、本地归档路径、效力状态和更新时间。
- 新增或改造页面后，应运行 `tools\kb.py schema --write-report`，确认页面能归入正确板块且关键元数据完整。
- 案例卡片应包含事实背景、争议问题、适用规则、判断过程、审计关注点和底稿留痕。
- 对最新法规、政策、准则变动，应先核验后更新。

## 当前最适合继续建设的方向

1. 继续扩展第四板块，把更多实务案例加工为案例卡片。
2. 为案例卡片增加跨案例索引，例如“收入确认案例索引”“政府补助案例索引”。
3. 对第一板块核心准则增加更多审计程序模板和底稿提示。
4. 为政策文件、职业道德和独立性准则建立定期复核清单。
5. 按第五板块项目落地路线推进 P1 工具：CPA-ZH 入库助手、案例卡片生成助手、PDF 原文归档工具。
6. 取得《注册会计师法》2026 修订官方重新公布全文后，用 `tools/generate_core_law_article_pages.py` 把草案拆为 60 个正式条款页替换旧结构。
