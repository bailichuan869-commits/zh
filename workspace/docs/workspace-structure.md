# 工作区目录说明

本工作区按“活跃知识库、工具脚本、课程产物、过程资料、历史归档”分层。顶层目录尽量保持少而稳定，具体资料在各业务目录内继续细分。

## 当前结构

| 目录 | 职责 | 说明 |
|---|---|---|
| `knowledge-base/` | 活跃知识库 | 当前核心是 `CPA-ZH`。 |
| `frontend/` | 前端应用 | Vue 3 + Vite + Ant Design Vue 浏览器。 |
| `backend/` | 后端应用 | FastAPI 只读 API。 |
| `tools/` | 自动化脚本 | 知识库维护、检索、缓存、文档转换和课程构建脚本。 |
| `course/` | 课程资料 | `source/` 放 Markdown，`dist/` 放 HTML，`slides/` 放网页 PPT。 |
| `workspace/` | 过程材料 | `docs/` 放说明和检查记录，`outputs/` 放一次性输出，`tmp/` 放临时文件，`archives/` 放过程归档。 |
| `archived/` | 历史归档 | 已完成或暂不维护的项目，默认不参与当前维护；法规资料在 `archived/regulations/`。 |

## CPA-ZH 内部分层

```text
knowledge-base/CPA-ZH/
├── raw/       # 原始资料和 manifest
├── wiki/      # 结构化知识页、索引、案例卡片
├── cache/     # 文本抽取缓存，可重建
└── search/    # 本地检索索引，可重建
```

`raw/` 是事实来源，`wiki/` 是加工后的知识表达，`cache/` 和 `search/` 是工具生成的辅助层。所有维护、分类和检查脚本统一位于仓库根 `tools/`。浏览器应用位于仓库根 `frontend/` 与 `backend/`。

## 维护建议

- 维护 CPA-ZH 时，先看 `knowledge-base/CPA-ZH/README.md`。
- 常用维护命令优先走 `tools/kb.py`，避免记忆多个脚本入口。
- 更新课程内容时，把新的 Markdown 放进 `course/source/`。
- 重新生成课程 HTML 时运行：

```powershell
node .\tools\build_course_html_organized.js
```

- 临时文件和一次性输出统一放进 `workspace/`。
- 源资产、可重建产物和发布产物边界见 `workspace/docs/generated-artifacts.md`。
- 归档内容如需重新维护，先从 `archived/` 移回对应活跃目录。

## 过程文件归位（防散落）

知识库与脚本目录只放"资产与源码"，任何运行期产物、日志、临时脚本都要归位：

| 文件类型 | 归位目录 | 示例 |
|---|---|---|
| 一次性检查/扫描报告（json/md/csv） | `workspace/outputs/` | `raw_quality_report.*`、`lint_report.md`、`version_consistency_scan.*` |
| 运行日志、临时脚本、下载残留 | `workspace/tmp/` | `connect_out.log`、`_audit_tmp.py`、`skill-creator-download.zip` |
| 有长期参考价值的清理/过程记录 | `workspace/docs/`（带日期重命名） | `reorg-delete-report-2026-07-24.md` |

规则：
- 脚本写入的产物路径要用相对仓库根的路径常量（如 `workspace/outputs/...`），不要把报告写到 `tools/` 或知识库根目录。
- `knowledge-base/CPA-ZH/` 根目录只允许：README.md / WIKI.md / log.md / source-registry.yml 以及 cache/ raw/ search/ wiki/ 子目录；应用源码、脚本、日志、csv、扫描报告、临时 .py 一律迁出。
- `workspace/outputs/` 已被 `.gitignore` 忽略，属可重建产物，不进版本库。
