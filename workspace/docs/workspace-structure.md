# 工作区目录说明

## 当前结构

- `knowledge-base/`
  - 当前活跃知识库，核心目录是 `CPA-ZH`。
- `regulations/`
  - 法规资料库。
  - `markdown/`：整理后的法规 Markdown 文本。
  - `source_docs/`：法规原始文档。
- `course/`
  - 课程与课件。
  - `source/`：课程 Markdown 源文件。
  - `dist/`：生成后的 HTML 成品。
  - `slides/`：章节演示页或网页 PPT。
- `tools/`
  - 构建脚本、知识库维护脚本、文档处理脚本。
- `workspace/`
  - 工作过程材料。
  - `docs/`：说明与检查记录。
  - `outputs/`：一次性输出。
  - `tmp/`：临时文件。
- `archived/`
  - 已归档项目和历史材料。
  - `cpa-competition/`：旧竞赛知识库。
  - `skill-assets/`：Skill 压缩包和解包检查材料。

## 使用建议

- 维护 CPA 知识库时，优先进入 `knowledge-base/CPA-ZH`。
- 更新课程内容时，把新的 Markdown 放进 `course/source/`。
- 重新生成课程 HTML 时，运行：
```powershell
node .\tools\build_course_html_organized.js
```
- 新增法规资料优先放进 `regulations/`。
- 临时文件和一次性输出统一放进 `workspace/`。
- 已完成且不再活跃维护的项目移入 `archived/`。
