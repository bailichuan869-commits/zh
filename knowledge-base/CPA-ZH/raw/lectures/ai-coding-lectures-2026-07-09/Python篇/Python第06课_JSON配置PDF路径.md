---
source_type: "local-lecture"
source_role: "content"
representation: "semantic-transcript"
extraction_profile: "readable"
structure_status: "verified-auto"
source_pages: 0
heading_count: 8
table_count: 0
extraction_engine: "markdown-pass-through"
extraction_status: "ok"
structure_updated_at: "2026-07-28"
---

# Python 第 06 课：JSON 配置 

## 今天让规则不要写死在代码里

前面的 PDF 合并工具已经能跑，但很多规则可能写死在代码里。

比如：

- 输入目录。
- 输出文件名。
- 是否覆盖旧文件。
- 按什么顺序合并。

今天我们用 JSON 把这些规则拿出来。

## 今天要解决的问题

如果每次改输出文件名都要改 Python 代码，项目会越来越难维护。

更好的方式是：

```text
容易变化的规则放配置文件。
稳定的处理逻辑放代码。
```

## 你会学到

- JSON 是什么。
- 配置文件是什么。
- 什么叫配置和代码分离。
- 为什么规则变化时不要总改代码。

## 我们一起动手做

新增配置文件：

```text
config/pdf_merge_config.json
```

示例：

```json
{
  "input_dir": "input_pdfs",
  "output_file": "output/merged.pdf",
  "sort_by": "filename",
  "overwrite": false
}
```

程序读取配置后再合并 PDF。

## 今天要记住

JSON 可以理解成给程序看的“设置表”。

设置表变了，代码不一定要变。

## 做完以后你应该能

- 看懂简单 JSON。
- 让 Python 读取 JSON 配置。
- 解释哪些规则适合放进配置文件。
- 处理 JSON 写错时的报错。

## 本节课提示词

把下面这段发给 AI：

```text
我想把 Python PDF 合并工具改造成读取 JSON 配置的版本。

请新增配置文件：
config\pdf_merge_config.json

配置内容包括：
- input_dir：输入 PDF 文件夹
- output_file：输出 PDF 文件路径
- sort_by：排序方式，先支持 filename
- overwrite：如果输出文件已存在，是否覆盖

改造要求：
- Python 程序启动时读取 JSON 配置
- 如果配置文件不存在，要给出中文提示
- 如果 JSON 格式错误，要给出中文提示
- 如果 overwrite 为 false 且输出文件已存在，要提醒用户，不直接覆盖
- 合并成功后提示处理文件数和输出路径

请输出：
1. JSON 配置示例
2. 改造后的 Python 代码
3. 配置字段解释
4. 常见配置错误
5. 如何验证改配置后不改代码也能改变输出
```
