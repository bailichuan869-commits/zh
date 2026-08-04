---
source_type: "local-lecture"
source_role: "content"
---

﻿# Python 第 21 课：MinerU 文档解析 API 请求

## 今天请求一个真实文档解析 API

前面我们已经知道了 API 的基本概念，也用 AkShare 获取了 A 股报表数据。

上一节又补了 Markdown，所以今天看到文档解析结果里的标题、列表、表格和代码块时，就不会把它们当成乱码。

今天换一个更接近 AI 文档处理的接口：

> MinerU 文档解析 API。

它可以把 PDF、图片、Word、PPT 等文档解析成结构化结果，比如 Markdown。

官方文档：

```text
https://mineru.net/apiManage/docs
```

## 今天要解决的问题

很多时候我们手里不是结构化 Excel，而是 PDF 或扫描件：

- 审计报告。
- 合同。
- 发票附件。
- 底稿说明。
- 制度文件。

如果能把 PDF 解析成 Markdown，后面就可以继续让 AI 做摘要、提取字段、生成底稿说明。

## 你会学到

- 文档解析 API 和普通查询 API 有什么不同。
- 什么是异步任务。
- 什么是 `task_id`。
- 为什么需要轮询结果。
- 什么是签名上传 URL。
- 为什么课堂上要先用小文件和模拟结果。

## MinerU 有两种 API

官方文档里有两类：

| 类型             | 特点                                 | 适合课堂吗   |
| -------------- | ---------------------------------- | ------- |
| 精准解析 API       | 需要 Token，支持单文件/批量、多格式输出，限制更高       | 适合正式项目  |
| Agent 轻量解析 API | 不需要 Token，IP 限频，单文件，输出 Markdown 链接 | 更适合课堂入门 |

今天优先讲 Agent 轻量解析 API。

## 这类 API 的流程

它不是“一请求马上返回结果”。

而是：

```text
提交解析任务
→ 得到 task_id
→ 等一会儿
→ 根据 task_id 查询任务状态
→ 任务完成后得到 Markdown 结果链接
```

如果是本地文件上传，还多一步：

```text
申请上传 URL
→ PUT 上传文件
→ 轮询解析结果
```

## 我们一起动手做

先做 URL 解析版本：

```text
POST https://mineru.net/api/v1/agent/parse/url
```

请求体里包含：

- 文件 URL。
- 语言。
- 页码范围。
- 是否识别表格。
- 是否 OCR。
- 是否识别公式。

然后查询结果：

```text
GET https://mineru.net/api/v1/agent/parse/{task_id}
```

如果课堂网络不稳定，就用本地模拟 JSON 练流程。

## 今天要记住

有些 API 是同步的，请求后马上返回结果。

有些 API 是异步的，请求后只返回任务 ID，需要后续轮询。

文档解析、OCR、视频处理这类耗时任务，经常是异步 API。

## 做完以后你应该能

- 解释 MinerU API 的基本用途。
- 说清 `task_id` 的作用。
- 看懂提交任务和查询结果两个接口。
- 区分 URL 解析和本地文件上传。
- 用模拟响应写出完整的轮询逻辑。

## 本节课提示词

把下面这段发给 AI：

```text
我想学习如何用 Python 请求 MinerU 文档解析 API。

官方文档：
https://mineru.net/apiManage/docs

请优先使用 Agent 轻量解析 API 设计课堂示例，因为它不需要 Token，适合入门演示。

请帮我讲清楚：
- MinerU 文档解析 API 是做什么的
- 精准解析 API 和 Agent 轻量解析 API 有什么区别
- 什么是异步任务
- task_id 是什么
- 为什么需要轮询查询结果
- URL 解析和本地文件上传有什么区别

请生成一个 Python 示例：
1. 提交 URL 解析任务
2. 获取 task_id
3. 每隔几秒查询一次任务状态
4. 如果 state=done，打印 markdown_url
5. 如果 state=failed，打印失败原因
6. 如果网络不可用，提供本地模拟 JSON 的写法

接口信息：
- 提交 URL 解析任务：POST https://mineru.net/api/v1/agent/parse/url
- 查询解析结果：GET https://mineru.net/api/v1/agent/parse/{task_id}

请求参数建议包含：
- url
- language: ch
- page_range: 1-3
- enable_table: true
- is_ocr: false
- enable_formula: true

请输出：
1. 需求理解
2. API 调用流程图
3. Python 代码
4. 模拟响应示例
5. 常见错误和排查方法
6. 课堂验证方法
```
