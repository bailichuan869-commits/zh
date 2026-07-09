# 工作区说明

这个工作区按“活跃内容在顶层、过程材料进 workspace、历史材料进 archived”的逻辑整理。

## 顶层入口

- `knowledge-base/`
  - 当前主知识库，核心内容是 `CPA-ZH`。
  - 相关脚本默认仍以 `knowledge-base/CPA-ZH` 为工作根目录。
- `regulations/`
  - 法规原文与整理稿。
  - `markdown/` 存放整理后的 Markdown 文本。
  - `source_docs/` 存放原始法规文档。
- `course/`
  - 课程材料与生成结果。
  - `source/` 存放课程 Markdown。
  - `dist/` 存放生成后的 HTML。
  - `slides/` 存放演示页或网页 PPT。
- `tools/`
  - 脚本与自动化工具。
- `workspace/`
  - 工作过程材料、说明文档、临时产物和一次性输出。
- `archived/`
  - 已归档项目与历史材料，默认不作为当前活跃工作内容处理。

## 约定

- 新增知识库内容优先进入 `knowledge-base/`。
- 新增法规资料优先进入 `regulations/`。
- 新增脚本放入 `tools/`。
- 临时文件、过程说明、一次性输出放入 `workspace/`。
- 已完成且短期不再维护的项目放入 `archived/`。
- `.codex/`、`.agents/`、`.git/`、`.venv/`、`.workbuddy/` 是工具或环境目录，通常不手动整理。
