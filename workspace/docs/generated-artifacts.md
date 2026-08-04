# 生成物边界说明

本项目同时保存事实来源、结构化知识和若干可重建产物。维护时先判断文件属于哪一层，再决定是否手工编辑。

## 源资产

| 路径 | 说明 |
|---|---|
| `knowledge-base/CPA-ZH/raw/` | 原始资料和 manifest，是事实来源。 |
| `knowledge-base/CPA-ZH/wiki/` | 结构化知识页、案例卡片、来源页和索引。 |
| `knowledge-base/CPA-ZH/source-registry.yml` | 官方来源注册表。 |
| `course/source/` | 课程 Markdown 源文件。 |
| `tools/` | 维护脚本和统一入口。 |
| `backend/`、`frontend/` | 分离式应用源码。 |

## 可重建产物

| 路径 | 重建方式 | 说明 |
|---|---|---|
| `knowledge-base/CPA-ZH/cache/text/` | `tools/kb.py cache build` | raw 文本抽取缓存。 |
| `knowledge-base/CPA-ZH/search/kb_search.sqlite*` | `tools/kb.py index` | 本地检索索引。 |
| `workspace/outputs/` | 由具体任务生成 | 一次性输出，不作为事实来源。 |
| `workspace/tmp/` | 本地运行与一次性任务使用 | PID、日志和临时文件。 |
| `knowledge-base/CPA-ZH/search/navigation-tree.json` | `tools/kb.py classify build` | API 浏览导航树。 |

## 随仓库保存的发布产物

| 路径 | 说明 |
|---|---|
| `frontend/dist/` | Vue 构建后的静态站点，由独立静态 Web 服务托管。 |
| `course/dist/`、`course/slides/` | 面向阅读或演示的课程发布产物。 |

## 前后端分离后的浏览器

- 根目录 `backend/` 是只读 FastAPI 源码；它只读取 `knowledge-base/CPA-ZH/` 的知识资产和检索产物。
- 根目录 `frontend/` 是 Vue 3 + Vite 源码；`frontend/dist/` 是可重建的静态发布产物，不作为事实来源。
- 旧静态 UI、其构建脚本和静态服务已删除。活跃 API 不再挂载 `ui/`、`wiki/` 或 `raw/` 静态目录。

## 维护规则

1. 不直接手工编辑 `cache/`、`search/`、`workspace/tmp/`。
2. 更新 raw 或 wiki 后，运行 `tools/kb.py cache build`、`tools/kb.py index` 和 `tools/kb.py health`。
3. 重建导航树后，应确认 `backend/` 可读取 `knowledge-base/CPA-ZH/search/navigation-tree.json`。
4. 废弃但有参考价值的脚本移入 `archived/kb-tools-legacy/`，不要留在活跃工具入口里。
5. 历史资料默认放入 `archived/`，重新启用前先迁回活跃目录并更新文档。
