---
source_type: "local-lecture"
source_role: "content"
representation: "semantic-transcript"
extraction_profile: "readable"
structure_status: "verified-auto"
source_pages: 0
heading_count: 12
table_count: 0
extraction_engine: "markdown-pass-through"
extraction_status: "ok"
structure_updated_at: "2026-07-28"
---

# Python 第 13 课：打造带 GUI 的 Excel 工具箱

## 今天从小工具进入工具箱

上一节我们解决的是一个很具体的小需求：

> 同事把文件放到 input，双击 EXE，结果出现在 output。

这种方式适合一次性小问题。

但如果你手上已经有很多小工具，比如：

- Excel 合并。
- Excel 清洗。
- PDF 合并。
- Word 表格导出。
- 批量改文件名。
- 审计检查小脚本。

继续每个工具都单独打一个 EXE，会变得很散。

今天这节课要解决的是第二类需求：

> 给自己或别人做一个带 GUI 的 Python 工具箱，把很多功能集成到一个界面里。

## 今天要解决的问题

单个 EXE 小工具适合解决小问题。

工具越来越多以后，会出现新问题：

- 工具太散，不知道该点哪个。
- 每个工具都有一套输入输出规则。
- 新增功能时没有统一入口。
- 给别人使用时，解释成本越来越高。

GUI 工具箱要解决的是：

```text
一个入口
多个功能
统一选择文件
统一输出目录
统一运行日志
```

## 你会学到

- 小工具和工具箱的区别。
- 为什么工具箱要分成“入口层”和“工具层”。
- 如何设计一个能持续加功能的 GUI。
- 如何用 PySide6 做功能列表、参数区域、运行按钮和日志窗口。
- 如何把多个已有脚本挂到同一个界面里。
- 为什么不要把业务逻辑写进按钮点击事件。

## 工具箱第一版长什么样

第一版不用追求漂亮。

先把结构做对：

```text
Python 工具箱

左侧：功能列表
  - Excel 合并
  - Excel 清洗
  - PDF 合并
  - Word 表格导出

右侧：当前功能参数
  输入文件/文件夹
  输出目录
  开始运行

底部：运行日志
```

这已经是一个很实用的工具箱雏形。

## 推荐项目结构

```text
python_toolbox/
  main.py
  requirements.txt
  README.md
  data/
  output/
  src/
    tools/
      excel_merge.py
      excel_clean.py
      pdf_merge.py
      word_table_export.py
    core/
      tool_registry.py
    ui/
      app.py
```

分工要讲清楚：

- `src\tools`：每个具体功能放这里。
- `src\core\tool_registry.py`：登记工具名称、说明和调用函数。
- `src\ui\app.py`：负责界面、按钮、日志、文件选择。
- `main.py`：启动工具箱。

今天最重要的一句话：

> GUI 只负责让人操作，真正干活的是 `src\tools`。

## 和第 12 课的关系

第 12 课是：

```text
一个小问题
一个小脚本
一个双击 EXE
```

第 13 课是：

```text
很多小功能
一个统一入口
一个 GUI 工具箱
```

两者不是谁替代谁。

实际工作里都需要：

- 临时、小、单一、给同事快速用：用第 12 课的方法。
- 长期、多个功能、反复使用：用第 13 课的方法。

## 工具注册表的作用

工具箱不能靠一堆按钮硬堆。

更好的方式是做一个工具注册表：

```text
工具名称：Excel 合并
工具说明：合并多个 Excel/CSV 文件
调用函数：run_excel_merge
输入类型：文件夹
```

以后新增工具时，只要：

```text
1. 在 src\tools 新增一个工具函数。
2. 在 tool_registry.py 里登记。
3. GUI 自动显示这个工具。
```

这样工具箱才能越做越多，而不至于越来越乱。

## GUI 工具箱打包

GUI 工具箱也可以打包成 EXE。

示例命令：

```powershell
pyinstaller --noconsole --onefile --name python_toolbox main.py
```

打包后同样要做交付测试：

```text
工具箱交付包/
  python_toolbox.exe
  README.md
  data/
  output/
```

第 13 课要提醒学员：

- GUI 工具箱可以比单个小工具复杂。
- 但复杂度必须被项目结构管理住。
- 每新增一个功能，优先放进 `src\tools`，再挂到界面。

## 今天要记住

工具箱不是把一堆脚本胡乱塞进一个窗口。

真正重要的是结构：

```text
工具层：负责处理业务
注册表：负责管理工具
界面层：负责让人选择和运行
```

结构对了，功能越多越有秩序。

## 做完以后你应该能

- 解释单个双击 EXE 和 GUI 工具箱的区别。
- 用 PySide6 搭出一个工具箱界面。
- 把多个已有 Python 工具挂到一个 GUI 中。
- 用工具注册表管理功能列表。
- 打包一个带 GUI 的 Python 工具箱。

## 本节课提示词

把下面这段发给 AI：

```text
我想做一个带 GUI 的 Python 工具箱，用来集成很多日常小工具。

工具箱目标：
- 给自己或同事使用
- 一个界面里集成多个功能
- 每个功能可以选择输入文件或文件夹
- 可以选择输出目录
- 有运行按钮
- 有运行日志
- 后续可以持续新增工具

第一版先集成这些功能：
1. Excel 合并
2. Excel 清洗
3. PDF 合并
4. Word 表格导出到 Excel

项目结构要求：
python_toolbox/
  main.py
  requirements.txt
  README.md
  data/
  output/
  src/
    tools/
      excel_merge.py
      excel_clean.py
      pdf_merge.py
      word_table_export.py
    core/
      tool_registry.py
    ui/
      app.py

设计要求：
- 使用 PySide6
- 左侧是功能列表
- 右侧是当前功能的输入路径、输出目录、运行按钮
- 底部是日志窗口
- GUI 不直接写业务逻辑，只调用 src\tools 里的函数
- 使用 tool_registry.py 管理工具名称、说明、输入类型和调用函数
- 代码适合零基础学员阅读

请输出：
1. 小工具 EXE 和 GUI 工具箱的区别
2. 推荐项目结构
3. tool_registry.py 设计
4. main.py 代码
5. src\ui\app.py 代码
6. 一个示例工具函数代码
7. 如何新增一个工具
8. requirements.txt 内容
9. PyInstaller 打包命令
10. 打包后的交付结构和测试方法
```
