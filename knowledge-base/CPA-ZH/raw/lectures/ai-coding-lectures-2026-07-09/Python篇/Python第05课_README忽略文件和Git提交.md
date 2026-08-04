---
source_type: "local-lecture"
source_role: "index-page"
---

# Python 第 05 课：README、忽略文件和 Git 提交

## 今天把第一个工具保存成版本

前面我们已经有了一个能跑、也能点按钮使用的 PDF 合并工具。

今天要把它从“临时脚本”整理成“第一个正式小项目”。

## 今天要解决的问题

一个项目如果没有整理，很快就会变乱：

- 下次忘了怎么运行。
- 不知道输入文件放哪里。
- 不知道输出在哪里。
- 不知道命令行和 GUI 分别怎么启动。
- `.venv`、输出文件、临时文件可能被一起提交。
- 改坏以后回不到之前版本。

## 你会学到

- README 应该写什么。
- `.gitignore` 是什么。
- 哪些文件不应该提交。
- Git 第一次提交是什么意思。

## 我们一起动手做

把项目整理成：

```text
pdf_tools_demo/
  input_pdfs/
  output/
  src/
    tools/
      pdf_merger.py
    ui/
      app.py
  README.md
  requirements.txt
  .gitignore
```

`.gitignore` 至少忽略：

```gitignore
.venv/
__pycache__/
*.pyc
output/
*.tmp
```

第一次提交：

```powershell
git init
git add .
git commit -m "Add PDF merger tool"
```

## 今天要记住

Git 的第一作用不是炫技，而是让项目有可回退的历史。

README 的第一作用不是形式，而是让下次的自己知道怎么用。

## 做完以后你应该能

- 给小工具写 README。
- 知道 `.gitignore` 要忽略哪些文件。
- 完成第一次 Git 提交。
- 提交前检查有没有不该提交的东西。

## 本节课提示词

把下面这段发给 AI：

```text
我已经有一个能运行的 Python PDF 合并工具，现在想把它整理成第一个正式小项目。

请帮我生成：
1. README.md
2. .gitignore
3. Git 第一次提交前检查清单

项目信息：
- 工具用途：合并 input_pdfs 文件夹里的多个 PDF
- 输出文件：output\merged.pdf
- 依赖：pypdf、PySide6
- 命令行运行：python src\tools\pdf_merger.py
- GUI 运行：python src\ui\app.py

README 要包括：
- 工具用途
- 目录结构
- 环境准备
- 安装依赖
- 如何放入 PDF
- 如何用命令行运行
- 如何打开 GUI 界面
- 输出文件在哪里
- 常见错误

.gitignore 要忽略：
- .venv
- __pycache__
- pyc 文件
- output
- 临时文件

请再给出第一次 Git 提交建议命令。
```
