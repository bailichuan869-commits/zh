# ai-audit 工作区

这个仓库是一个面向审计、会计准则和监管资料的本地知识工作台。当前主线是 `CPA-ZH` 知识库，同时保留课程产物、维护脚本和历史归档。

## 快速入口

| 入口 | 用途 |
|---|---|
| `knowledge-base/CPA-ZH/README.md` | 主知识库说明、检索命令、维护流程 |
| `knowledge-base/CPA-ZH/wiki/index.md` | CPA-ZH wiki 总索引 |
| `start-kb.bat` | 双击启动 CPA-ZH 前后端联动 Web 界面 |
| `stop-kb.bat` | 停止本机 CPA-ZH 知识库 Web 服务 |
| `tools/kb.py` | CPA-ZH 统一维护入口 |
| `course/` | 课程 Markdown、HTML 和网页 PPT |
| `archived/regulations/` | 已归档法规原文与整理稿，后续默认不维护 |
| `workspace/docs/` | 工作区说明、检查记录和架构说明 |
| `workspace/docs/generated-artifacts.md` | 源资产、可重建产物和发布产物边界 |
| `workspace/docs/cpa-zh-agent.md` | Agent CLI、stdio MCP 与两阶段写入说明 |
| `requirements.txt` | Python 运行依赖清单 |

## 目录分层

```text
ai-audit/
├── frontend/                # Vue 3 + Vite 知识库浏览器
├── backend/                 # FastAPI 只读 API
├── knowledge-base/          # 当前活跃知识库
│   └── CPA-ZH/              # CPA 行业知识库主线
├── tools/                   # 自动化脚本和维护入口
├── requirements.txt         # Python 运行依赖
├── start-kb.bat             # 知识库前后端联动启动入口
├── stop-kb.bat              # 知识库 UI 停止入口
├── course/                  # 课程资料与生成结果
├── workspace/               # 过程资料、临时输出和说明文档
└── archived/                # 已完成或暂不维护的历史项目
    └── regulations/         # 已归档法规资料
```

## 常用命令

所有 Python 命令建议使用工作区虚拟环境：

```powershell
.\.venv\Scripts\python.exe
```

启动或停止知识库 Web 界面：

```powershell
.\start-kb.bat
.\stop-kb.bat
```

## CPA-ZH 前后端运行

知识库浏览器已拆分为独立的 Vue 前端和 FastAPI 后端。`start-kb.bat` 会同时启动本机 API（`http://127.0.0.1:8765/api/docs`）和前端（`http://127.0.0.1:5173`）：

```powershell
.\start-kb.bat
```

如需手动分别启动，前端开发服务地址为 `http://127.0.0.1:5173`，通过 Vite 代理调用后端。生产部署时先执行 `npm run build`，再由独立静态 Web 服务托管 `frontend/dist/`。

CPA-ZH 维护建议优先使用统一入口：

```powershell
.\.venv\Scripts\python.exe tools\kb.py health
.\.venv\Scripts\python.exe tools\kb.py search "收入确认"
.\.venv\Scripts\python.exe tools\kb.py cache build
.\.venv\Scripts\python.exe tools\kb.py index
.\.venv\Scripts\python.exe tools\kb.py readme
.\.venv\Scripts\python.exe tools\kb.py verify
```

Agent 是知识库维护的主要交互入口。浏览器保持只读；Agent 通过共享服务先生成完整预览，在用户明确确认后再使用短期令牌提交：

```powershell
.\.venv\Scripts\python.exe tools\cpa_zh_agent.py search --query "收入确认"
.\.venv\Scripts\python.exe tools\cpa_zh_agent.py pending-reviews
.\.venv\Scripts\python.exe tools\cpa_zh_mcp.py
```

完整配置和两阶段确认流程见 `workspace/docs/cpa-zh-agent.md`。

旧脚本入口仍然保留，例如 `tools/kb_search.py`、`tools/kb_health_check.py`、`tools/kb_text_cache.py`。

## 放置规则

- 新增知识库内容：优先放入 `knowledge-base/CPA-ZH/raw/`，再加工到 `wiki/`。
- 法规资料库已归档到 `archived/regulations/`，后续默认不新增、不维护。
- 新增课程资料：Markdown 放入 `course/source/`，生成品放入 `course/dist/` 或 `course/slides/`。
- 新增脚本：放入 `tools/`，并在 `tools/README.md` 归类。
- 新增 Python 依赖：同步更新 `requirements.txt`。
- 临时文件、一次性输出、过程说明：放入 `workspace/`。
- 已完成且短期不维护的项目：移入 `archived/`。

## 架构原则

- `raw/` 保存原始资料，`wiki/` 保存结构化知识，`cache/` 和 `search/` 是可重建产物；具体规则见 `workspace/docs/generated-artifacts.md`。
- 顶层目录按业务域分层，脚本只做维护和生成，不混入知识正文。
- 能复用 `tools/kb.py` 的维护动作，优先通过统一入口执行。
- 不在历史归档里继续建设新功能；需要复活时先迁回活跃目录。
