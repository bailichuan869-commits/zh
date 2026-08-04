---
source_type: "local-lecture"
source_role: "content"
representation: "semantic-transcript"
extraction_profile: "readable"
structure_status: "verified-auto"
source_pages: 0
heading_count: 17
table_count: 0
extraction_engine: "markdown-pass-through"
extraction_status: "ok"
structure_updated_at: "2026-07-28"
---

# Python 第 00 课：课前环境准备

## 这一节不是编程课

这一节只做工具准备。

目标很简单：

> 让后面的课程能顺利运行，不要第一节课就卡在安装环境上。

## 今天要准备什么

我们需要准备：

- Python
- Node.js
- Git
- 一个 AI 编程工具（workbuddy、codex、claudecode、opencode）
- 一个代码编辑器（vscode、cursor、trea、kiro）
- 一个课程工作目录

## Python：必须安装

Python 是后面所有 Python 工具的运行基础。

安装时注意：

- 建议安装 Python 3.11 或 3.12。
- Windows 安装时勾选 `Add Python to PATH`。
- 安装后重新打开 PowerShell。

检查命令：

```powershell
python --version
pip --version
```

如果能看到版本号，就说明基本可用。

## Git：建议安装

Git 用来保存项目版本。

后面我们会用它记录：

- 第一个 PDF 工具版本。
- GUI 版本。
- 打包前版本。
- 后续工具箱版本。

检查命令：

```powershell
git --version
```

## Node.js：建议提前安装

前面 PDF、Excel、Word 工具主要用 Python，不一定马上用 Node。

但后面如果扩展 Web 页面、前端工具或更完整的网页项目，Node 会很有用。

检查命令：

```powershell
node --version
npm --version
```

如果暂时没装，也不会影响前几节 Python 工具课。

## AI 编程工具

你可以使用：

- Codex
- Cursor
- VS Code + AI 插件
- 其他能读写项目文件、运行命令的 AI 编程工具

关键不是工具名字，而是它要能做到：

- 打开一个项目文件夹。
- 创建和修改文件。
- 运行终端命令。
- 读取报错并帮你分析。

## 准备课程工作目录

建议单独准备一个课程目录，例如：

```text
D:\ai-coding-course
```

后面的项目都放在这个目录下。

第一模块会创建：

```text
pdf_tools_demo
```

## 准备测试文件

第 1 课会做 PDF 合并工具。

请提前准备：

- 2-3 个小 PDF。
- 文件名最好能看出顺序，例如 `01.pdf`、`02.pdf`、`03.pdf`。

后面还会用到 Excel 和 Word 示例文件，课堂上再逐步准备。

## 版本检查清单

课前至少检查：

```powershell
python --version
pip --version
git --version
```

建议也检查：

```powershell
node --version
npm --version
```

## 常见问题

### 命令提示无法识别 python

通常是安装时没有加入 PATH，或者安装后没有重新打开 PowerShell。

### pip 无法使用

先确认 Python 是否安装正确，再检查：

```powershell
python -m pip --version
```

### Node 一定要现在装吗

不是必须。

前几节 Python 工具课不依赖 Node。Web 扩展阶段会更需要它。

### 要不要现在创建虚拟环境

不用。

虚拟环境会在第 3 课结合 PDF 工具一起讲。

## 今天要记住

这一节只要求“能检查版本”。

安装细节不用背，后面真正用到时再理解。

## 本节课提示词

把下面这段发给 AI：

```text
我准备学习 AI 辅助 Python 编程课程。

请帮我检查本机环境是否准备好。

我会在 PowerShell 中依次运行：
python --version
pip --version
git --version
node --version
npm --version

请你根据我粘贴的命令输出，帮我判断：
1. Python 是否可用
2. pip 是否可用
3. Git 是否可用
4. Node 和 npm 是否可用
5. 哪些问题会影响前几节 Python 工具课
6. 哪些问题可以等到 Web 扩展阶段再处理

请用适合零基础学员理解的语言回答，不要一次给太多复杂命令。
```
