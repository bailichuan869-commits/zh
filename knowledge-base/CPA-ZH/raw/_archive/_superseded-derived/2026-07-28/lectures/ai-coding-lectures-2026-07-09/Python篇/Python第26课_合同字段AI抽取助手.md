---
source_type: "local-lecture"
source_role: "content"
---

# Python 第 26 课：搭建合同抽取 Harness：用 AgentScope 启动合同助手

## 今天不是只调用一次大模型

前面我们已经做过两种产品形态：

```text
本地桌面路线：React + pywebview
Web 服务路线：FastAPI + 前端
```

也做过一个 Web 小案例：PDF 转 Markdown 网站。

从这一节开始，我们进入一个新的项目：

>AI合同助手。

最终目标是：

```text
上传一份合同
-> 转成 Markdown
-> 配置需要抽取的字段
-> 让 AI 按字段配置去合同里找内容
-> 输出 Excel 抽取结果
-> 保留每一步运行日志
```

如果只是让 AI 总结一段合同文本，直接复制到聊天窗口也能做。

但我们现在要做的是一个可以反复运行、可以调试、可以接回工具箱的项目。

所以今天先引入一个重要概念：

> Harness。

## 什么是 Harness

Harness 可以理解成：

> 给 AI 搭一个固定的运行工作台。

它不是只包含大模型。

它还包含：

```text
任务说明
系统提示词
输入文件
字段配置
可用工具
输出格式
日志记录
错误处理
人工复核入口
```

如果把大模型看成发动机，那么 harness 就是把发动机装进一辆能跑、能刹车、能看仪表盘的车里。

在我们的合同助手里，harness 不是一句提示词，而是一整个小项目。

它要明确：

```text
从哪里读合同
按什么规则分析
要抽取哪些字段
能调用哪些工具
结果写到哪里
每一步日志在哪里
```

这就是 harness 的价值。

## Harness 和框架是什么关系

这几个词容易混在一起。

可以这样区分：

| 层级         | 作用                          | 本项目里的例子                |
| ---------- | --------------------------- | ---------------------- |
| 大模型        | 理解文本、生成结果                   | Qwen / GPT             |
| Agent 框架   | 组织 Agent、消息、工具和事件           | AgentScope             |
| 工具         | 执行确定性动作                     | 读合同、读字段配置、写 Excel      |
| 业务 Harness | 把输入、提示词、工具、输出、日志组织成可重复运行的项目 | `contract_agent/`      |
| 产品入口       | 给用户操作                       | pywebview / FastAPI 前端 |

一句话：

```text
框架解决 Agent 怎么运行。
业务 Harness 解决这个 AI 能力在合同抽取场景里怎么稳定运行、测试和复用。
```

AgentScope 本身已经提供了很多通用 harness 能力：

```text
Agent 运行
模型调用
消息管理
工具注册
工具调用
事件流
日志观察
状态管理
```

所以 AgentScope 不是一个简单的“大模型 API 调用库”。

它更像一个：

> 通用 Agent harness 框架。

我们在它上面再搭一个业务 harness：

```text
合同目录
字段配置
系统提示词
合同抽取规则
Excel 输出
日志保存位置
```

也就是说：

```text
AgentScope 解决“Agent 如何稳定运行”。
contract_agent 解决“合同抽取这个业务如何稳定运行”。
```

如果不使用 AgentScope 或 Microsoft Agent Framework 这类框架，我们就要自己写很多底层逻辑：

```text
自己维护 messages
自己拼系统提示词和用户消息
自己解析模型返回的 tool call
自己决定什么时候调用哪个工具
自己把工具结果塞回对话
自己记录每一步事件日志
自己处理模型重试和异常
自己管理多轮状态
```

这些事情当然可以自己写。

但对业务项目来说，重点不是重复造 Agent 底座。

我们的重点是：

```text
设计合同字段
设计合同抽取提示词
设计读取合同和写 Excel 的工具
把能力接回工具箱
让用户能稳定使用
```

所以选择 AgentScope / Microsoft Agent Framework 这类框架，本质上是为了：

> 少写底层 Agent 运行逻辑，把精力放在业务 harness 上。

## 为什么选择 AgentScope

本模块使用 AgentScope。

不是因为它是唯一选择，而是因为它适合我们这个项目。

你可以先这样理解：

| 框架                        | 适合什么                          |
| ------------------------- | ----------------------------- |
| 普通 Python API 调用          | 简单问答、单次总结                     |
| LangChain / LangGraph     | 通用 LLM 应用、链式流程、RAG、复杂图流程      |
| Microsoft Agent Framework | 微软生态里的 Agent / Workflow 生产化方向 |
| AgentScope                | Agent、工具调用、事件流、日志观察           |

Microsoft Agent Framework 和 AgentScope 属于类似层级：

```text
它们都在帮我们封装 Agent harness 的底层能力。
```

区别在于：

```text
Microsoft Agent Framework 更偏微软生态、企业级 Agent、Workflow、多 Agent 生产化方向。
AgentScope 更适合本模块这种 Agent-first、工具调用、事件流观察的教学项目。
```

我们的合同助手重点是：

```text
让 AI 读取合同
让 AI 理解字段配置
让 AI 调用工具
观察每一步事件和日志
最后接回工具箱
```

所以 AgentScope 很合适。
文档地址：[AgentScope](https://doc.agentscope.io/zh_CN/index.html)
## 为什么合同抽取适合大模型

合同字段抽取不是普通的表格读取。

同一个字段，在不同合同里的写法可能完全不同：

```text
合同金额
合同总价
服务费用
项目总金额
本合同价款
```

付款条款也可能写成：

```text
首付款、验收款、质保金
分阶段付款
按月结算
验收后一次性支付
```

这种任务很适合大模型：

- 能理解不同说法背后的含义。
- 能从长文本里找关键信息。
- 能把自然语言整理成结构化结果。
- 能在找不到字段时说明缺失原因。

但是大模型不适合直接做所有事情。

更合理的分工是：

```text
Python 负责读取文件、保存文件、写 Excel。
AI 负责理解合同、判断字段含义、抽取内容。
AgentScope 负责组织 Agent、消息、工具和事件日志。
业务 harness 负责把这一切固定成可重复运行的项目。
```

## 今天要让 AI 帮我们做什么

今天不手写具体代码。

我们要让 AI 帮我们生成一个：

> 合同抽取 harness 第一版项目。

这个项目暂时不做字段配置，也不做工具调用。

它只需要跑通第一条链路：

```text
合同 Markdown
-> 系统提示词
-> AgentScope Agent
-> 合同摘要和关键条款
-> 事件日志
-> summary.md
```

也就是说，今天要让 AI 交付这些东西：

```text
1. 一个 contract_agent 项目结构
2. 一份示例合同 Markdown
3. 一份系统提示词
4. 一个能运行的主程序
5. 一个 .env.example 配置示例
6. 一个 requirements.txt
7. 一个 output/logs 日志目录
8. 一份 summary.md 分析结果
9. 一份运行说明 README
```

你不需要先看懂每一行代码。

这一节重点是看懂：

```text
AI 生成的项目是不是符合 harness 思路
输入在哪里
提示词在哪里
输出在哪里
日志在哪里
运行入口在哪里
出了问题怎么排查
```

## 产物应该长什么样

让 AI 生成的项目结构应该类似：

```text
contract_agent/
  README.md
  main.py
  config.py
  requirements.txt
  .env.example

  prompts/
    system_prompt.md

  input/
    contracts/
      sample_contract.md

  output/
    logs/
    summary.md
```

每个文件的作用：

| 文件 | 作用 |
|---|---|
| `README.md` | 说明项目怎么运行、怎么检查结果 |
| `main.py` | 运行入口 |
| `config.py` | 读取模型配置 |
| `requirements.txt` | 依赖列表 |
| `.env.example` | API Key 和模型配置示例 |
| `prompts/system_prompt.md` | 系统提示词 |
| `input/contracts/sample_contract.md` | 示例合同 Markdown |
| `output/logs/` | 保存 AgentScope 事件日志 |
| `output/summary.md` | 保存合同分析结果 |

这个结构本身就是 harness 的第一版。

## 今天要检查 AI 生成的项目

AI 生成项目后，不要只看“有没有代码”。

要按下面这张清单检查：

| 检查项 | 要求 |
|---|---|
| 项目结构 | 是否有 `prompts`、`input`、`output/logs` |
| 输入文件 | 是否有一份可测试的合同 Markdown |
| 系统提示词 | 是否明确要求基于合同原文，不要编造 |
| 运行入口 | 是否说明运行哪个文件 |
| 日志 | 是否保存 AgentScope 事件日志 |
| 输出 | 是否生成 `summary.md` |
| 配置 | 是否把 API Key 放在 `.env`，没有写死在代码里 |
| 说明文档 | 是否告诉你怎么安装、怎么运行、怎么检查结果 |

如果这些没有做到，就继续让 AI 修改。

## 运行以后重点看什么

运行以后，不要只看最终回答。

重点看终端和日志里的事件：

```text
REPLY_START
MODEL_CALL_START
TEXT_BLOCK_DELTA
MODEL_CALL_END
REPLY_END
```

这些事件告诉你：

```text
Agent 什么时候开始回复
什么时候调用模型
模型输出了哪些文本
什么时候结束回复
```

后面讲工具调用时，还会看到：

```text
TOOL_CALL_START
TOOL_CALL_DELTA
TOOL_RESULT_TEXT_DELTA
TOOL_RESULT_END
```

这就是 AgentScope 很适合这个项目的地方：

> 它能让你看到 Agent 中间到底做了什么。

## 今天要记住

今天不是为了看懂所有代码。

今天是在搭合同抽取 harness 的第一版：

```text
固定输入：input/contracts/sample_contract.md
固定规则：prompts/system_prompt.md
固定执行：AgentScope Agent
固定输出：output/summary.md
固定日志：output/logs/*.jsonl
```

有了 harness，后面才好继续加：

```text
字段配置
工具调用
Excel 输出
上传合同
接回工具箱
```

下一节会继续升级：

> 不把字段写死在提示词里，而是让用户配置要抽取的字段，再让 AI 按配置抽取。

## 做完以后你应该能

- 解释什么是 harness。
- 说明 harness 和大模型、Agent 框架、工具、产品入口之间的关系。
- 解释为什么选 AgentScope / MAF 这类框架，而不是自己手写底层 Agent 逻辑。
- 解释为什么合同字段抽取适合大模型。
- 看懂一个合同抽取 harness 的项目结构。
- 知道系统提示词、输入合同、输出结果、事件日志分别放在哪里。
- 能让 AI 生成一个 `contract_agent` 项目第一版。
- 能按检查清单判断 AI 生成的项目是否合格。

## 本节课提示词

把下面这段发给 AI：

```text
我想新建一个 Python 项目 contract_agent，用 AgentScope 做合同字段抽取助手。

这节课先不要求我手写代码，请你直接帮我生成“合同抽取 harness 第一版项目”。

项目目标：
- 读取 input/contracts/sample_contract.md
- 使用 prompts/system_prompt.md 作为系统提示词
- 创建 AgentScope Agent
- 让 Agent 阅读合同 Markdown
- 输出合同摘要、合同双方、合同金额、付款安排、验收条款、风险提示、下一步建议
- 使用 reply_stream 打印每个 Agent 事件
- 把事件日志保存到 output/logs/run_时间.jsonl
- 把最终回答保存到 output/summary.md

请先解释：
1. 什么是 harness
2. AgentScope 为什么可以看成通用 Agent harness 框架
3. contract_agent 为什么是合同抽取业务 harness
4. 为什么不用自己手写 messages、tool call、事件日志这些底层逻辑

请生成：
1. 项目结构
2. requirements.txt
3. .env.example
4. prompts/system_prompt.md
5. input/contracts/sample_contract.md
6. main.py
7. config.py
8. README.md

要求：
- 不要把 API Key 写死在代码里
- 事件日志必须保存到 output/logs/
- 最终分析结果保存到 output/summary.md
- README 要说明如何安装依赖、配置 API Key、运行项目、检查日志和结果
- 代码中关键位置加少量中文注释
- 项目要适合零基础学员运行和观察
```
