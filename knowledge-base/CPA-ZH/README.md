# CPA-ZH 知识库

CPA-ZH 是围绕中国注册会计师行业建立的本地知识库，用于沉淀法规准则、政策文件、职业道德与独立性要求、审计实务技能和案例分析。

截至 2026-07-09，知识库已经具备“原文归档 + 结构化 wiki + 本地检索 + 案例卡片”的基础形态。

新手优先入口：

- `wiki/concepts/kb-user-guide.md` - CPA-ZH 使用手册，说明结构、检索、新增资料、案例使用和维护命令。
- `wiki/index.md` - 知识库总索引。
- `wiki/concepts/kb-maintenance-workflow.md` - 维护工作流。
- `wiki/concepts/source-status-dashboard.md` - 来源状态仪表盘，查看待 OCR、官方链接和文本缓存状态。

## 当前状态


| 项目 | 数量或状态 |
|---|---:|
| wiki 页面 | 815 |
| raw 原始文件 | 722 |
| manifest 批次 | 4 |
| 本地检索索引记录 | 1500 |
| 实务案例卡片 | 5 |
| wiki 内链状态 | 最近检查为 0 缺失 |
| Python 运行方式 | 统一使用工作区虚拟环境 `.venv` |

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
│   └── cases/                # 加工后的案例卡片
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

第四板块已启动。已导入 2026 年 7 月第一期 5 个实务案例，并加工为 5 张案例卡片。

核心入口：

- `wiki/concepts/practice-skills-cases.md`
- `wiki/concepts/case-analysis.md`
- `wiki/sources/case-batch-2026-07-first-issue.md`
- `wiki/cases/`

已加工案例：

- `wiki/cases/2026-07-first-issue-long-term-equity-investment-confirmation.md`
- `wiki/cases/2026-07-first-issue-temporary-fixed-asset-tax-difference.md`
- `wiki/cases/2026-07-first-issue-government-grant-free-use-equipment.md`
- `wiki/cases/2026-07-first-issue-equipment-sales-revenue-recognition.md`
- `wiki/cases/2026-07-first-issue-overseas-sales-revenue-recognition.md`

## 本地检索

所有 Python 命令统一使用工作区虚拟环境：

```powershell
.\.venv\Scripts\python.exe
```

常用检索命令：

```powershell
.\.venv\Scripts\python.exe tools\kb_search.py query "独立性准则"
.\.venv\Scripts\python.exe tools\kb_search.py query "收入确认"
.\.venv\Scripts\python.exe tools\kb_search.py query "政府补助 免费使用设备"
.\.venv\Scripts\python.exe tools\kb_search.py query "长期股权投资 内部重组"
```

重建索引：

```powershell
.\.venv\Scripts\python.exe tools\kb_search.py index
```

查看索引统计：

```powershell
.\.venv\Scripts\python.exe tools\kb_search.py stats
```

构建或刷新 raw 文本缓存：

```powershell
.\.venv\Scripts\python.exe tools\kb_text_cache.py build
.\.venv\Scripts\python.exe tools\kb_text_cache.py stats
```

`kb_search.py index` 会优先复用 `cache/text/` 中的新鲜缓存；当缓存缺失或原文件变更时，才现场抽取正文。

当前索引构成：

| 类型 | 数量 |
|---|---:|
| raw-file | 648 |
| raw-manifest | 37 |
| wiki | 815 |
| total | 1500 |

## 归档与审计

一键体检：

```powershell
.\.venv\Scripts\python.exe tools\kb_health_check.py
```

manifest 审计：

```powershell
.\.venv\Scripts\python.exe tools\kb_manifest_audit.py
```

当前 manifest：

| manifest | 条目 |
|---|---:|
| `raw/cases/2026-07-first-issue/manifest.json` | 5 |
| `raw/ethics/third-section/manifest.json` | 24 |
| `raw/policies/issuance-guidance/manifest.json` | 1 |
| `raw/policies/second-section/manifest.json` | 7 |

官方链接汇总：

```powershell
.\.venv\Scripts\python.exe tools\kb_link_check.py
```

联网检查链接时使用：

```powershell
.\.venv\Scripts\python.exe tools\kb_link_check.py --include-wiki --check
```

刷新 README 统计：

```powershell
.\.venv\Scripts\python.exe tools\kb_update_readme_stats.py
```

## 新资料放置规则

原始资料统一放入 `raw/`，不要直接覆盖 wiki 页面。

建议位置：

```text
raw/laws/          法律法规原文
raw/standards/     会计准则、审计准则、应用指南、解释、问答
raw/policies/      政策性文件
raw/ethics/        职业道德、独立性准则
raw/cases/         实务案例、项目复盘、监管案例
```

加工后的知识页放入：

```text
wiki/concepts/     规则、框架、专题
wiki/sources/      来源批次说明
wiki/cases/        案例卡片
```

## 维护流程

1. 先把原始文件放入 `raw/`。
2. 为批次建立或更新 `manifest.json`。
3. 在 `wiki/sources/` 建来源批次页。
4. 在 `wiki/concepts/` 或 `wiki/cases/` 生成结构化页面。
5. 更新 `wiki/index.md` 和 `wiki/log.md`。
6. 构建或刷新 raw 文本缓存。
7. 重建本地检索索引。
8. 刷新 README 统计。
9. 运行一键体检。
10. 更新来源状态仪表盘。
11. 抽查关键词检索结果。

详细流程见：

- `wiki/concepts/kb-maintenance-workflow.md`

## 质量原则

- 法规、准则、政策优先使用官方来源。
- 原文文件保留在 `raw/`，wiki 页面只做结构化加工。
- 重要页面应写明官方链接、本地归档路径、效力状态和更新时间。
- 案例卡片应包含事实背景、争议问题、适用规则、判断过程、审计关注点和底稿留痕。
- 对最新法规、政策、准则变动，应先核验后更新。

## 当前最适合继续建设的方向

1. 继续扩展第四板块，把更多实务案例加工为案例卡片。
2. 为案例卡片增加跨案例索引，例如“收入确认案例索引”“政府补助案例索引”。
3. 对第一板块核心准则增加更多审计程序模板和底稿提示。
4. 为政策文件、职业道德和独立性准则建立定期复核清单。
