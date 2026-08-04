# 项目架构说明

这个仓库的核心不是单个应用，而是一个资料驱动的知识工作台。架构重点是把“原始资料、结构化知识、生成产物、维护工具、历史材料”分清楚。

## 分层模型

```text
外部资料
  ↓
raw 原始资料层
  ↓ manifest / 来源说明
wiki 结构化知识层
  ↓
cache / search 可重建辅助层
  ↓
课程、UI、检索和问答使用
```

## 顶层边界

| 层 | 目录 | 边界 |
|---|---|---|
| 主知识库 | `knowledge-base/CPA-ZH/` | 当前核心业务资产。 |
| 前端应用 | `frontend/` | Vue 3 + Vite 知识库浏览器。 |
| 后端应用 | `backend/` | FastAPI 只读 API，读取知识库资产。 |
| 课程产物 | `course/` | 面向学习的 Markdown、HTML、网页 PPT。 |
| 工具层 | `tools/` | 生成、检查、检索、转换脚本，不沉淀知识正文。 |
| 启停入口 | 根目录 `start-kb.bat`、`stop-kb.bat`；`tools/start_kb_api.py`、`tools/stop_kb.py` | 批处理文件是面向本机用户的入口，Python 实现在工具层。 |
| 依赖清单 | `requirements.txt` | Python 运行依赖，用于重建环境。 |
| 工作过程 | `workspace/` | 说明、检查记录、临时输出。 |
| 历史归档 | `archived/` | 只读优先，默认不继续演进；`archived/regulations/` 保存已归档法规资料。 |

## CPA-ZH 内部边界

- `raw/`：来源层。保存下载、导入或手工归档的原文资料，以及批次 `manifest.json`。
- `wiki/`：知识层。保存概念页、专题页、案例卡片、来源批次页和总索引。
- `cache/`：性能层。保存 raw 文本抽取缓存，可通过工具重建。
- `search/`：检索层。保存 SQLite 检索索引，可通过工具重建。

## 命令入口

本机浏览入口是 `start-kb.bat` 和 `stop-kb.bat`。维护入口是 `tools/kb.py`：

```powershell
.\.venv\Scripts\python.exe tools\kb.py health
.\.venv\Scripts\python.exe tools\kb.py search "收入确认"
.\.venv\Scripts\python.exe tools\kb.py cache build
.\.venv\Scripts\python.exe tools\kb.py index
.\.venv\Scripts\python.exe tools\kb.py readme
```

具体脚本仍保留，适合调试和单点维护。统一入口只做路由，不改变已有脚本行为。公共转发逻辑放在 `tools/kb_cli_support.py`，避免 `kb.py` 继续膨胀。

## 生成物边界

源资产、可重建产物和随仓库保存的发布产物见 `workspace/docs/generated-artifacts.md`。

## 演进规则

1. 新资料先进入 `raw/`，再登记 manifest。
2. 结构化加工结果进入 `wiki/`，不要直接覆盖原始资料。
3. `cache/` 和 `search/` 视为可重建产物，不作为事实来源。
4. 新脚本放入 `tools/` 并补充 `tools/README.md`；共享 CLI 逻辑优先放入 `tools/kb_cli_support.py`。
5. 一次性产物放入 `workspace/outputs/`，稳定内容再迁入对应业务目录。
6. 归档项目默认不维护；重新启用前先迁回活跃目录。
7. 法规资料库已归档到 `archived/regulations/`，后续默认不维护。
8. 新增 Python 依赖时同步更新 `requirements.txt`。
