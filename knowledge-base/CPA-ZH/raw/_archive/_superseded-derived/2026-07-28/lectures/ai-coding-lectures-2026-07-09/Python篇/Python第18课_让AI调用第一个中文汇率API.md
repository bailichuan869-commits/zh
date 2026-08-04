---
source_type: "local-lecture"
source_role: "content"
---

# Python 第 18 课：让 AI 调用第一个中文汇率 API

## 今天第一次请求外部 API

前面我们做过 PDF、Excel、Word 工具。

这些工具大多数都是在处理本地文件：

```text
本地 PDF
本地 Excel
本地 Word
```

从这一节开始，我们换一种数据来源：

> 从外部系统获取数据。

比如汇率、天气、股票行情、企业信息、文档解析结果，都可能来自外部 API。

今天不急着讲复杂概念。

我们先让 AI 帮我们调用一个中文文档比较友好的汇率 API，完成一个最小工具：

```text
输入币种和金额
请求 API 获取汇率
计算折算金额
输出结果
```

## 今天要解决的问题

很多同学听到 API，会觉得它像一个程序员专属的词。

但先不用怕。

今天我们只把 API 理解成一句话：

> API 就是别人提供好的一个网址，我们按它的规则传参数，它返回一段数据。

最简单的 API 请求，可以看成：

```text
URL + 参数 → JSON 结果
```

今天的目标不是背 API 术语，而是跑通这条链路：

```text
看文档
找到接口地址
拼参数
用浏览器验证
用 Python 请求
解析 JSON
做成一个小工具
```

## 今天使用的 API

今天使用 Ratata 的公开汇率 API。

开发者文档：

```text
https://www.ratata.money/zh/developers
```

它适合课堂入门，因为：

- 文档有中文说明。
- 返回 JSON。
- 不需要 API Key。
- 支持汇率查询和金额换算。
- 参数简单，容易在浏览器里直接验证。

课堂上先不纠结它是不是财务正式数据源。

今天它的角色是：

> 帮我们理解 API 请求的完整过程。

正式做财务工具时，还是要确认数据来源、授权、更新频率和使用限制。

## API 的四个关键词

今天只记住四个词。

| 关键词 | 含义 | 今天的例子 |
|---|---|---|
| URL | 接口地址 | `https://ratata.money/api/v1/rates/convert` |
| 参数 | 传给 API 的条件 | `from=USD&to=CNY&amount=100` |
| 请求方法 | 怎么请求 | `GET` |
| 响应结果 | API 返回的数据 | JSON |

把它连起来就是：

```text
GET https://ratata.money/api/v1/rates/convert?from=USD&to=CNY&amount=100
```

这句话的意思是：

```text
把 100 美元换算成人民币。
```

## 先用浏览器打开

学 API 的第一步，不要急着写 Python。

先把接口放到浏览器里打开。

```text
https://ratata.money/api/v1/rates/convert?from=USD&to=CNY&amount=100
```

如果接口正常，会看到一段类似这样的 JSON：

```json
{
  "from": "USD",
  "to": "CNY",
  "amount": 100,
  "result": 724.56,
  "rate": 7.2456
}
```

不同时间返回的汇率可能不同。

所以课堂上不要要求学生记住某一个固定数字。

要让大家观察字段：

| 字段 | 含义 |
|---|---|
| `from` | 原币种 |
| `to` | 目标币种 |
| `amount` | 原金额 |
| `rate` | 汇率 |
| `result` | 折算结果 |

这一步的重点是：

> JSON 看起来像字典，Python 很容易读取里面的字段。

## 再让 AI 写最小 Python 代码

先安装依赖：

```powershell
python -m pip install requests
```

最小代码大概长这样：

```python
import requests

url = "https://ratata.money/api/v1/rates/convert"
params = {
    "from": "USD",
    "to": "CNY",
    "amount": 100,
}

response = requests.get(url, params=params, timeout=10)
data = response.json()

print(data)
print("汇率：", data["rate"])
print("折算结果：", data["result"])
```

这段代码里要讲清楚三件事。

第一，`url` 是接口地址。

第二，`params` 是参数。

第三，`response.json()` 把 API 返回的 JSON 转成 Python 字典。

## 为什么不要手拼 URL

初学时很容易这样写：

```python
url = "https://ratata.money/api/v1/rates/convert?from=USD&to=CNY&amount=100"
```

这当然能跑。

但更推荐写成：

```python
params = {
    "from": "USD",
    "to": "CNY",
    "amount": 100,
}

requests.get(url, params=params)
```

这样更清楚，也更不容易在参数变多时写错。

让 AI 写 API 请求时，也要提醒它：

> 参数用 `params` 字典传，不要全部手动拼到 URL 里。

## 做成第一个小工具

第一版工具先做命令行输入。

运行后让用户输入：

```text
原币种：USD
目标币种：CNY
金额：100
```

程序输出：

```text
100 USD 按汇率 7.2456 折算为 724.56 CNY
```

这一版只解决一个问题：

> 用户输入一笔金额，程序调用 API 返回折算结果。

## 再升级成批量处理

办公场景里，通常不会只算一笔。

更常见的是有一张交易表：

```text
input\foreign_transactions.csv
```

示例内容：

```csv
交易日期,摘要,原币种,目标币种,原金额
2026-05-20,境外服务费,USD,CNY,1200
2026-05-21,软件订阅费,EUR,CNY,300
2026-05-22,差旅报销,JPY,CNY,50000
```

程序逐行读取：

```text
原币种
目标币种
原金额
```

然后逐行请求 API，最后输出：

```text
output\exchange_result.csv
```

输出字段可以设计成：

| 字段 | 说明 |
|---|---|
| 交易日期 | 原始交易日期 |
| 摘要 | 原始摘要 |
| 原币种 | 比如 USD |
| 目标币种 | 比如 CNY |
| 原金额 | 原始金额 |
| 汇率 | API 返回的 rate |
| 折算金额 | API 返回的 result |
| 状态 | 成功或失败 |
| 错误信息 | 失败时记录原因 |

## 推荐项目结构

今天的项目不用做复杂。

可以这样放：

```text
exchange_api_demo/
  main.py
  requirements.txt
  README.md
  input/
    foreign_transactions.csv
  output/
```

每个文件的作用：

```text
main.py                         主程序
requirements.txt                依赖列表
input/foreign_transactions.csv   输入交易数据
output/                         输出折算结果
```

今天先不要做 GUI。

API 入门阶段，命令行更容易看清楚请求和返回。

## 代码要注意什么

让 AI 写代码时，要提醒它处理几类问题。

### 网络失败

API 请求可能失败。

比如：

- 没联网。
- 接口访问超时。
- 接口临时不可用。

所以请求时要设置：

```python
timeout=10
```

并且用 `try...except` 捕获错误。

### 返回不是预期 JSON

有时接口返回的内容不是预期结构。

所以不要直接假设一定有：

```python
data["rate"]
data["result"]
```

要先检查字段是否存在。

### 币种写错

如果用户把 `USD` 写成 `U SD`，或者写成不支持的币种，接口可能返回错误。

工具要给出中文提示。

### 不要请求太快

公开 API 通常有限速。

Ratata 文档里写了按 IP 限速。

批量处理时不要一口气发太多请求。

课堂示例只处理几行数据即可。

## 今天要讲清楚的概念

API 这节课最容易讲散。

今天只讲这些概念就够了：

```text
接口地址 URL
请求参数 params
GET 请求
JSON 响应
字段提取
网络异常
接口限速
```

暂时不讲：

- OAuth。
- Header 鉴权。
- POST 上传文件。
- 异步任务。
- Webhook。
- 自己开发 API。

这些后面再讲。

第 18 课的任务是把门打开，不是把整栋楼逛完。

## 和后面课程怎么衔接

今天我们是直接请求 API：

```text
requests → API → JSON
```

第 19 课会看到另一种方式：

```text
AkShare 函数 → AkShare 内部请求数据源 → DataFrame
```

所以第 19 课可以这样衔接：

> 上一节我们自己拼 URL、传参数、解析 JSON。今天看 AkShare，它把很多外部数据接口包装成了 Python 函数。

第 20 课再讲 MinerU 时，可以继续升级：

```text
普通同步 API → 提交任务后马上返回结果
异步 API → 先返回 task_id，后面轮询结果
```

这样 API 模块的层次就很清楚。

## 课堂实现节奏

建议今天分五步。

第一步：浏览器直接打开 API。

让学生看到：

```text
网址可以直接返回 JSON 数据。
```

第二步：解释 URL 和参数。

把这段拆开：

```text
https://ratata.money/api/v1/rates/convert
?from=USD
&to=CNY
&amount=100
```

第三步：让 AI 写最小 Python 请求。

只打印 JSON、汇率和折算结果。

第四步：封装成函数。

函数可以叫：

```python
convert_currency(from_currency, to_currency, amount)
```

第五步：读取 CSV 批量处理。

把输入和输出做成一个小工具。

## 今天不要做什么

今天先不做这些：

- 不做 GUI。
- 不做复杂配置文件。
- 不做很多 API 对比。
- 不做正式财务数据校验。
- 不批量请求几百行数据。
- 不把 API Key、Token、签名鉴权全讲完。

今天只盯住一个核心：

> 让 AI 帮我们完成第一次 API 请求，并把 JSON 结果变成可用数据。

## 今天要记住

API 入门不要先背概念。

先看清楚这条链路：

```text
文档告诉我们怎么请求
URL 决定请求哪个接口
参数决定要查什么
JSON 是接口返回的数据
Python 负责请求、解析和保存
```

以后换成天气 API、企业信息 API、股票数据 API、文档解析 API，本质都差不多。

只是参数、返回字段和稳定性要求不同。

## 做完以后你应该能

- 解释 API 是什么。
- 看懂一个简单 API 文档里的接口地址和参数。
- 用浏览器验证一个 GET API。
- 用 `requests.get()` 请求 API。
- 用 `response.json()` 解析 JSON。
- 从 JSON 里提取汇率和折算结果。
- 把多行外币交易批量折算并输出 CSV。
- 知道公开 API 可能有网络失败、字段变化和限速问题。

## 本节课提示词

把下面这段发给 AI：

```text
我想做一个 Python 汇率折算工具，用 Ratata 的公开汇率 API。

API 文档：
https://www.ratata.money/zh/developers

请先帮我讲清楚：
1. API 是什么
2. URL、参数、GET 请求、JSON 响应分别是什么意思
3. 为什么可以先把 API 地址放到浏览器里测试
4. 为什么 Python 里推荐用 requests.get(url, params=params)，而不是手动拼接完整 URL
5. 公开 API 可能遇到哪些问题，比如网络失败、返回字段变化、限速

第一步，请写一个最小 Python 示例：
- 请求 https://ratata.money/api/v1/rates/convert
- 参数 from=USD，to=CNY，amount=100
- 打印完整 JSON
- 打印 rate 和 result
- 设置 timeout=10
- 如果请求失败，输出中文错误提示

第二步，请把它封装成函数：
convert_currency(from_currency, to_currency, amount)

第三步，请扩展成批量处理工具：
- 输入文件 input/foreign_transactions.csv
- 字段包括：交易日期、摘要、原币种、目标币种、原金额
- 逐行调用汇率 API
- 输出 output/exchange_result.csv
- 输出字段包括：交易日期、摘要、原币种、目标币种、原金额、汇率、折算金额、状态、错误信息
- 如果某一行失败，不要中断整个程序，要把错误写到这一行
- 如果 input 或 output 文件夹不存在，请自动创建

项目结构：
exchange_api_demo/
  main.py
  requirements.txt
  README.md
  input/
    foreign_transactions.csv
  output/

请输出：
1. 需求理解
2. API 调用流程
3. 推荐项目结构
4. requirements.txt
5. main.py 完整代码
6. 示例 foreign_transactions.csv
7. 如何运行
8. 如何验证结果
9. 常见错误和排查方法

代码要适合零基础学员阅读，关键位置加少量中文注释。
```
