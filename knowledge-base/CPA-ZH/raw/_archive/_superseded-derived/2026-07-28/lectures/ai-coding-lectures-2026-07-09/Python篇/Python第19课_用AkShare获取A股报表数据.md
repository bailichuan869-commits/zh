---
source_type: "local-lecture"
source_role: "content"
---

﻿# Python 第 19 课：用 AkShare 获取 A 股报表数据

## 今天换一种方式获取外部数据

上一节我们知道了 API 是什么：通过 URL、参数和响应结果，从外部系统获取数据。

今天再看一种更适合财经数据的方式：

> 不自己拼 API 请求，而是使用 AkShare 这种第三方库获取 A 股报表数据。

AkShare 已经把很多财经数据接口封装成了 Python 函数。

我们只需要安装它、查文档、调用函数，就可以拿到 DataFrame。

## 今天要解决的问题

做财务分析或审计辅助时，经常要看上市公司的三大报表：

- 资产负债表。
- 利润表。
- 现金流量表。

如果手工打开网页、复制数据、整理 Excel，会很慢。

今天我们让 Python 自动获取一只 A 股公司的报表数据，并保存成 Excel。

## 你会学到

- AkShare 是什么。
- 第三方库也可以封装外部数据接口。
- 如何用 AkShare 获取 A 股财务报表。
- 股票代码为什么要区分 `sh600519`、`sz000001` 这种格式。
- 为什么外部数据工具要保留原始数据。
- 如何把三张报表保存到一个 Excel 的多个 Sheet。

## AkShare 和 API 是什么关系

上一节我们直接理解 API 请求：

```text
URL + 参数 → 响应结果
```

AkShare 做的事情，可以理解为：

```text
Python 函数 → AkShare 帮我们请求数据源 → 返回 DataFrame
```

也就是说，AkShare 不是 Python 自带的功能。

它是第三方库，也是外部数据接口的封装层。

课堂上我们不需要先研究每个网页接口怎么请求，而是先学会：

- 找到 AkShare 文档。
- 选择合适的函数。
- 看懂函数参数。
- 观察返回数据。
- 保存和校验结果。

## 我们一起动手做

先安装依赖：

```powershell
python -m pip install akshare openpyxl
```

检查 AkShare 是否安装成功：

```powershell
python -c "import akshare as ak; print(ak.__version__)"
```

先用一个最小示例获取资产负债表：

```python
import akshare as ak

df = ak.stock_financial_report_sina(stock="sh600519", symbol="资产负债表")
print(df.head())
print(df.columns)
```

这里有两个重要参数：

```text
stock   股票代码，示例：sh600519
symbol  报表类型，可选：资产负债表、利润表、现金流量表
```

然后再扩展成一个小工具：

- 输入股票代码，比如 `600519`。
- 自动转换为 AkShare 需要的格式，比如 `sh600519`。
- 分别获取三张报表。
- 保存到 `output\a_stock_financial_reports.xlsx`。
- 每张报表保存到一个 Sheet。
- 如果获取失败，给出中文提示。

## 课堂建议

这节课先用沪深 A 股中比较常见的代码做演示，比如：

```text
600519  贵州茅台
000001  平安银行
```

先不要一上来做很多股票的批量抓取。

外部数据源可能会变化，也可能因为网络或访问频率出现失败。

所以我们要养成两个习惯：

- 先少量测试。
- 先保存原始返回结果。

## 今天要记住

AkShare 的重点不是“背函数名”。

重点是理解这条链路：

```text
查文档 → 选函数 → 传参数 → 得到 DataFrame → 检查字段 → 保存 Excel
```

外部数据不一定稳定。

所以工具要能提示错误，也要保留原始数据，方便后续核对。

## 做完以后你应该能

- 解释 AkShare 是什么。
- 说明 AkShare 和自己写 API 请求的区别。
- 用 AkShare 获取一只 A 股公司的三大报表。
- 把三张报表输出到一个 Excel 文件。
- 说清楚为什么要先检查 `df.columns`。
- 说明外部财经数据工具的稳定性风险。

## 本节课提示词

把下面这段发给 AI：

```text
我想做一个 Python 工具，用 AkShare 获取 A 股上市公司的财务报表数据。

业务场景：
我希望输入一个 A 股股票代码，比如 600519 或 000001，程序自动获取这家公司的三大报表：
- 资产负债表
- 利润表
- 现金流量表

请使用 AkShare 的财务报表接口：
ak.stock_financial_report_sina(stock="sh600519", symbol="资产负债表")

请帮我讲清楚：
- AkShare 是什么
- AkShare 和直接写 requests 请求 API 有什么区别
- 为什么 AkShare 属于第三方库
- stock 参数为什么要写成 sh600519 或 sz000001
- symbol 参数有哪些可选值
- 为什么外部数据源可能不稳定
- 为什么要先 print(df.head()) 和 print(df.columns())

工具要求：
- 如果用户输入 600519，自动转换成 sh600519
- 如果用户输入 000001，自动转换成 sz000001
- 分别获取资产负债表、利润表、现金流量表
- 每张报表保存到一个 Excel Sheet
- 输出文件保存到 output\a_stock_financial_reports.xlsx
- 如果 output 文件夹不存在，自动创建
- 如果某张报表获取失败，要记录失败原因并继续处理其他报表
- 不要一开始就批量抓很多股票，先做好单只股票

请输出：
1. 需求理解
2. AkShare 接口说明
3. 股票代码转换函数
4. Python 实现代码
5. 输出 Excel 的 Sheet 设计
6. 常见错误和排查方法
7. 课堂验证步骤
```
