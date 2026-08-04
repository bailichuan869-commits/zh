---
source_type: "local-lecture"
source_role: "content"
---

# Python 第 17 课：Word 工具箱集成

## 今天把多个 Word 工具放到一起

上一节课，我们做了一个 Word 表格/标题提取工具。

它能做的事情是：

```text
读取 Word 文档
提取标题目录
提取表格清单
输出 Excel 检查清单
```

但真实工作里，Word 需求通常不会只有一个。

同事可能还会继续问：

```text
能不能把 Word 里的表格完整导出到 Excel？
能不能批量把 Word 转成 PDF？
能不能检查文档里有没有某些关键词？
能不能把这些功能放到一个工具里？
```

所以今天我们不再做单个脚本。

今天要做的是：

> 一个 Word 工具箱。

## 今天要解决的问题

单个小工具用多了以后，会出现新问题：

- 每个工具一个脚本，文件越来越散。
- 每个工具的输入输出规则不一样。
- 同事不知道该运行哪个脚本。
- 后面新增功能时，很容易把代码写乱。

Word 工具箱要解决的是：

```text
一个入口
多个 Word 功能
统一输入输出
统一日志提示
后续还能继续扩展
```

这和前面做 Python 工具箱的思路是一致的。

## 今天工具箱先集成哪些功能

第一版 Word 工具箱先集成三个功能：

```text
1. 文档体检
2. 表格导出
3. 批量转 PDF
```

### 功能一：文档体检

文档体检就是上一节课工具的升级版。

输入：

```text
一个 Word 文件
```

输出：

```text
Excel 检查报告
```

报告里可以包含：

- 标题目录。
- 表格清单。
- 关键词命中。

其中关键词可以来自配置文件：

```text
config\word_keywords.json
```

示例：

```json
{
  "keywords": ["重大", "异常", "风险", "整改", "保留意见"]
}
```

### 功能二：表格导出

表格导出比“表格清单”更进一步。

它不是只告诉你有多少个表格，而是把 Word 里的每个表格完整导出到 Excel。

输出方式：

```text
每个 Word 表格一个 Sheet
再增加一个“表格清单”Sheet
```

这个功能适合：

- 报告附表提取。
- 合同条款表提取。
- 整改事项表提取。
- 制度对照表提取。

### 功能三：批量转 PDF

批量转 PDF 和前两个功能不一样。

前两个功能适合用：

```text
python-docx
```

但批量转 PDF 更适合用：

```text
COM 控制 Word
```

因为“另存为 PDF”是 Word 软件自己的能力。

这正好复习第 16 课的判断：

```text
读取 docx 内容结构 → python-docx
控制 Word 软件导出 PDF → COM
```

## 你会学到

- 如何把多个 Word 工具整理到一个项目里。
- 如何设计工具注册表。
- 为什么不同功能可以使用不同技术路线。
- 如何让工具箱统一管理输入、输出和日志。
- 如何把上一节课的单个工具变成工具箱里的一个功能。

## 推荐项目结构

第一版项目结构可以这样设计：

```text
word_toolbox/
  main.py
  requirements.txt
  README.md
  config/
    word_keywords.json
  data/
    input_docs/
  output/
  src/
    core/
      tool_registry.py
      paths.py
    tools/
      document_check.py
      table_export.py
      batch_to_pdf.py
```

每个目录的作用：

```text
main.py                     工具箱入口
config/                     放配置文件
data/input_docs/             放待处理 Word
output/                     放输出结果
src/core/tool_registry.py    管理工具列表
src/tools/                  放具体 Word 工具
```

今天可以先做命令行版。

不用急着做 GUI。

先把工具层结构稳定下来。

## 工具注册表是什么

工具箱不能靠一堆散乱的 `if` 硬写。

更好的方式是做一个工具注册表。

它记录：

| 字段 | 含义 |
|---|---|
| 工具编号 | 用户选择哪个功能 |
| 工具名称 | 显示给用户看的名字 |
| 工具说明 | 这个工具解决什么问题 |
| 调用函数 | 真正执行的 Python 函数 |

比如：

```text
1 文档体检      document_check.run
2 表格导出      table_export.run
3 批量转 PDF    batch_to_pdf.run
```

以后新增功能时，只要：

```text
1. 在 src/tools 新增一个工具文件
2. 在 tool_registry.py 里登记
3. main.py 自动显示出来
```

这就是工具箱可扩展的关键。

## 今天的运行方式

第一版可以做成命令行菜单。

运行：

```powershell
python main.py
```

显示：

```text
Word 工具箱

1. 文档体检：提取标题、表格清单和关键词命中
2. 表格导出：把 Word 中的所有表格导出到 Excel
3. 批量转 PDF：把 input_docs 里的 Word 批量另存为 PDF

请输入工具编号：
```

用户输入编号后，工具开始执行。

所有输出都放到：

```text
output/
```

## 文件安全规则

Word 工具箱一定要遵守几个规则：

- 不要修改原 Word 文件。
- 所有结果输出到 `output`。
- 批量处理前先打印将要处理的文件数量。
- 转 PDF 失败时要记录哪个文件失败。
- 没有找到输入文件时，要给中文提示。
- 出错时不要静默跳过。

这些规则比代码本身还重要。

办公自动化最怕的是：

> 一次批量操作，把原始文件弄坏了，还不知道哪里出错。

所以我们默认只生成新文件，不覆盖原文件。

## 三个工具的技术路线

今天要让大家看到：

| 工具 | 推荐技术路线 | 原因 |
|---|---|---|
| 文档体检 | python-docx + openpyxl | 读取 Word 结构，输出 Excel |
| 表格导出 | python-docx + openpyxl | 提取 Word 表格，整理成 Excel |
| 批量转 PDF | win32com | 调用 Word 软件导出 PDF |

这就是第 16 课的能力地图真正落地。

不是所有 Word 功能都用同一个库。

我们根据需求选择方式。

## 课堂实现节奏

建议今天分四步完成。

第一步：搭项目结构。

```text
word_toolbox/
  main.py
  src/core/
  src/tools/
```

第二步：做工具注册表。

先让 `main.py` 能显示工具菜单。

第三步：接入两个 python-docx 工具。

```text
文档体检
表格导出
```

第四步：说明批量转 PDF 的 COM 路线。

如果课堂电脑有 Word，就可以现场演示。

如果环境不稳定，可以先把 COM 工具作为代码讲解和课后练习。

## 今天不要做什么

今天先不做这些：

- 不做复杂 GUI。
- 不做拖拽上传。
- 不做 Web 页面。
- 不把所有代码写在 `main.py` 里。
- 不要求一次把所有异常处理做到完美。

今天的重点是：

> 多个 Word 工具如何组织成一个可以继续扩展的工具箱。

## 今天要记住

单个工具解决一个问题。

工具箱解决一类问题。

Word 工具箱的关键不是功能越多越好，而是结构要清楚：

```text
入口层：main.py
注册表：tool_registry.py
工具层：src/tools
输入输出：data/input_docs 和 output
```

结构清楚以后，后面新增工具就不慌。

## 做完以后你应该能

- 设计一个 Word 工具箱项目结构。
- 把多个 Word 工具登记到工具注册表。
- 解释文档体检、表格导出、批量转 PDF 分别适合什么技术路线。
- 让工具箱统一从 `data/input_docs` 读取文件。
- 让工具箱统一把结果输出到 `output`。
- 知道为什么工具箱默认不修改原文件。

## 本节课提示词

把下面这段发给 AI：

```text
我想做一个 Python Word 工具箱，把多个 Word 自动化工具集成到一个项目里。

第一版工具箱先做命令行菜单，不做 GUI。

工具箱功能：
1. 文档体检
   - 使用 python-docx 读取 Word
   - 提取标题目录
   - 提取表格清单
   - 根据 config\word_keywords.json 检查关键词命中
   - 输出 Excel 检查报告

2. 表格导出
   - 使用 python-docx 读取 Word
   - 把每个 Word 表格完整导出到 Excel 的单独 Sheet
   - 增加一个“表格清单”Sheet

3. 批量转 PDF
   - 使用 win32com 控制 Word 软件
   - 把 data\input_docs 里的 docx 批量另存为 PDF
   - 输出到 output\pdf

项目结构：
word_toolbox/
  main.py
  requirements.txt
  README.md
  config/
    word_keywords.json
  data/
    input_docs/
  output/
  src/
    core/
      tool_registry.py
      paths.py
    tools/
      document_check.py
      table_export.py
      batch_to_pdf.py

设计要求：
- main.py 显示命令行菜单，让用户选择工具编号
- tool_registry.py 管理工具编号、名称、说明和调用函数
- 每个具体工具放在 src\tools 里
- 不要修改原 Word 文件
- 所有输出写入 output 目录
- 如果没有找到输入 Word，要给中文提示
- 批量转 PDF 前先打印将要处理的文件数量
- 代码适合零基础学员阅读，有必要注释

请输出：
1. 需求理解
2. 推荐项目结构
3. requirements.txt 内容
4. tool_registry.py 代码
5. paths.py 代码
6. main.py 代码
7. document_check.py 代码
8. table_export.py 代码
9. batch_to_pdf.py 代码
10. word_keywords.json 示例
11. 如何准备测试文件
12. 如何运行和验证三个工具
13. 常见错误和排查方法
```
