---
source_type: "local-lecture"
source_role: "content"
---

# Python 第 15 课：AGENTS.md 项目说明文件

## 本节课要解决的问题

第 14 课已经讲过 Skill。

Skill 解决的是：

> 把一套稳定方法沉淀下来，以后跨项目反复使用。

但在真实项目里，还会遇到另一个问题：

> 每次让 AI 进到一个项目里，它都不知道这个项目的规矩。

比如前面做过的 `excel_tools` 工具箱项目，里面已经有这些结构：

```text
excel_tools/
  main.py
  cli.py
  core/
  excel/
  pdf/
  gui/
    app.py
    style.py
    widgets.py
    tabs/
```

如果不提前告诉 AI 项目规则，它可能会：

- 把所有逻辑都写进 `gui/app.py`。
- 把 GUI 和 CLI 混在一起。
- 直接覆盖用户原始 Excel 或 PDF 文件。
- 新增功能时不知道应该放到 `core/`、`excel/`、`pdf/` 还是 `gui/tabs/`。
- 改界面时不管现有侧边栏、日志面板、图标和间距规则。

所以本节课要解决的是：

> 如何用 `AGENTS.md` 给 AI 写一份项目说明书。

## AGENTS.md 是什么

`AGENTS.md` 可以理解成：

> 给 AI Coding Agent 看的项目 README。

它不是代码，也不是配置文件。

它是一份项目约定。

里面可以写：

- 这个项目是做什么的。
- 项目目录怎么分工。
- 如何运行。
- 如何测试。
- 新增功能应该放在哪里。
- 哪些文件不要乱改。
- 哪些业务规则必须遵守。
- UI 风格和交互习惯是什么。

## AGENTS.md 和 Skill 的区别

第 14 课讲 Skill，第 15 课讲 AGENTS.md。

这两个很容易混，但它们不是一回事。

| 名称        | 解决什么问题                | 作用范围      |
| --------- | --------------------- | --------- |
| Prompt    | 当前这一次任务怎么做            | 一次对话      |
| README.md | 给人看的项目说明，也可以给 AI 参考   | 当前项目      |
| AGENTS.md | 给 AI 看的项目规则           | 当前项目      |
| CLAUDE.md | Claude Code 常用的项目记忆文件 | 当前项目或用户环境 |
| Skill     | 一套可复用的方法、流程、模板        | 跨项目复用     |

可以这样记：

```text
Prompt 解决这一次。
AGENTS.md 管住这个项目。
Skill 沉淀下一次。
```


## 结合 excel_tools 项目看目录约定

以 `excel_tools` 项目为例。

这个项目有两个入口：

```text
main.py    # GUI 入口
cli.py     # 命令行入口
```

还有几个核心目录：

```text
core/      # 通用业务逻辑
excel/     # Excel 相关能力
pdf/       # PDF 相关能力
gui/       # PySide6 界面
gui/tabs/  # 每个功能页
```

这就非常适合写进 `AGENTS.md`。

因为以后你让 AI 新增功能时，它就能先知道：

- 不要把业务逻辑直接写在按钮事件里。
- GUI 只是入口，真正的处理逻辑应该放在核心模块。
- 如果功能也要支持命令行，就要补 `cli.py`。
- 如果是界面功能，就要在 `gui/tabs/` 里加页面。

## 一个 AGENTS.md 示例

在 `excel_tools` 项目根目录下，新建：

```text
AGENTS.md
```

内容可以这样写：

```md
# AGENTS.md

## Project

这是一个 Python 桌面工具箱项目，用来处理日常办公中的 Excel、PDF 和批量文件任务。

项目同时提供两个入口：

- GUI 入口：`main.py`
- CLI 入口：`cli.py`

不要随意合并 GUI 和 CLI 代码。
GUI 负责交互，CLI 负责命令行调用，核心处理逻辑应放在 `core/`、`excel/`、`pdf/` 等模块中。

## Directory Rules

- `main.py`：PySide6 GUI 启动入口。
- `cli.py`：命令行入口，保留给脚本调用或打包 EXE。
- `core/`：通用业务逻辑，例如 ROUND 包裹、字符提取、目录生成、批量重命名。
- `excel/`：Excel 读写、COM、openpyxl/xml 后端。
- `pdf/`：PDF 合并、拆分、旋转、水印等逻辑。
- `gui/`：界面代码。
- `gui/tabs/`：每个功能页单独放一个 tab。

## Development Rules

新增一个工具功能时，优先按这个顺序开发：

1. 先在 `core/`、`excel/` 或 `pdf/` 中写可复用处理函数。
2. 再按需要在 `cli.py` 中补命令行调用。
3. 最后在 `gui/tabs/` 中补界面入口。

不要把核心处理逻辑直接写死在按钮点击事件里。

## Run Commands

- 启动 GUI：`python main.py`
- 查看 CLI 参数：`python cli.py -h`
- 安装依赖：`pip install -r requirements.txt`

## Excel Rules

- 使用 `xlwings` 的功能通常需要用户提前打开 Excel。
- 修改当前选区的功能，要基于 Excel 当前 selection。
- 读取和写入独立 xlsx 文件时，优先使用 `openpyxl` 相关后端。
- 不要默认覆盖用户原始 Excel 文件。
- 批量输出结果时，应输出到用户选择的目录，或者明确的 `output/` 目录。

## GUI Rules

- GUI 使用 PySide6。
- 图标优先使用 `qtawesome`。
- 左侧侧边栏负责功能导航。
- 中间区域只放当前功能的主要操作。
- 日志输出统一使用底部 `LogPanel`。
- 长时间任务不要卡住界面，应使用 worker 或后台线程。
- 按钮、图标、输入框要对齐，间距保持一致。

## File Safety Rules

- 不要删除用户文件。
- 不要覆盖用户原始 Excel、Word、PDF 文件。
- 批量重命名前必须生成预览或清单。
- 执行批量重命名前要有确认步骤。
- PDF 合并、拆分、旋转、水印等操作默认生成新文件。
- 出错时要把错误写入日志，不要静默失败。
```

## 这份 AGENTS.md 解决了什么

第一，它让 AI 知道项目结构。

以后你说：

> 帮我给工具箱增加一个 PDF 加水印功能。

AI 就不应该只改 `gui/app.py`。

它应该想到：

```text
pdf/       写 PDF 处理逻辑
cli.py     如果需要命令行入口，就补命令
gui/tabs/  增加或修改 PDF 页面
```

第二，它让 AI 知道安全边界。

办公自动化工具最怕的是：

> 一次批量操作，把原始文件改坏了。

所以 `AGENTS.md` 里要明确写：

```text
不要覆盖用户原始文件。
默认输出新文件。
批量操作前要有预览或确认。
```

第三，它让 AI 知道界面风格。

比如这个项目已经有：

- 可折叠侧边栏。
- `qtawesome` 图标。
- 底部日志面板。
- `gui/theme.py` 和 `gui/style.py` 里的统一样式。

那以后 AI 改界面时，就不应该每次重新发明一套 UI。

## CLAUDE.md

`AGENTS.md` 是更通用的项目说明文件。

`CLAUDE.md` 是 Claude Code 专用的项目说明文件。

刚开始不需要纠结文件名本身，先理解背后的思想：

> 给 AI 写清楚这个项目的规矩。

如果一个项目主要用 Claude Code，也可以写：

```text
CLAUDE.md
```

并把核心内容和 `AGENTS.md` 保持一致。

如果两个文件都维护，建议不要写两份完全重复的内容。

## 本节课要记住

`AGENTS.md` 不是写给用户看的。

它是写给 AI 看的。

它的目标不是介绍项目多厉害，而是让 AI 少猜、少乱改、少破坏。

好的 `AGENTS.md` 应该具体。

不要写：

```text
请写高质量代码。
请保持项目整洁。
```

要写：

```text
新增 GUI 功能时，把页面放在 gui/tabs/。
核心处理逻辑不要写在按钮点击事件里。
批量处理文件时，不要覆盖原文件。
```

## 做完以后你应该能

- 解释 `AGENTS.md` 和 Skill 的区别。
- 给一个 Python 项目写项目级约定。
- 知道哪些内容适合放进 `AGENTS.md`。
- 知道哪些内容不应该放进 `AGENTS.md`。
- 能结合工具箱项目，写出目录、运行、UI 和文件安全规则。

## 本节课提示词

把下面这段发给 AI：

```text
我有一个 Python 工具箱项目，请你帮我写一份 AGENTS.md。

项目结构：
- main.py 是 PySide6 GUI 启动入口
- cli.py 是命令行入口
- core/ 放通用业务逻辑
- excel/ 放 Excel 处理能力
- pdf/ 放 PDF 处理能力
- gui/ 放界面代码
- gui/tabs/ 放每个功能页面

项目规则：
- 不要把核心业务逻辑直接写在按钮点击事件里
- 新功能优先写业务函数，再接 CLI，最后接 GUI
- 不要覆盖用户原始 Excel、Word、PDF 文件
- 批量处理要输出新文件，并在日志里提示结果
- GUI 使用 PySide6 和 qtawesome
- 左侧侧边栏负责导航，底部日志面板负责输出运行信息
- 图标、文字、按钮、输入框要对齐

请输出：
1. 一份完整的 AGENTS.md
2. 哪些规则是项目结构规则
3. 哪些规则是文件安全规则
4. 哪些规则是 GUI 设计规则
5. 以后新增功能时，AI 应该如何根据这份 AGENTS.md 决定改哪些文件
```
