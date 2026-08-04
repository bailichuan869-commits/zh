---
source_type: "local-lecture"
source_role: "content"
---

# Python 第 28 课：CPAHelper Agent 的工具设计

## 今天看一个真实的 Agent 项目

前面两节课，我们已经用 AgentScope 做过一个合同助手：

```text
第 26 课：让 AI 阅读合同 Markdown，并按字段抽取内容。
第 27 课：理解 Agent tool，同时判断什么时候该用 tool，什么时候该用固定代码。
```

今天不继续写新代码。

今天看一个真实项目：

```text
CPAHelperForExcel
```

这个项目里已经有一个运行在 Excel 里的 Agent。

它不是单纯聊天。

它可以读取 Excel、预览表格、写入单元格、生成公式、筛选数据、创建工作表、生成图表，也可以在需要时调用更高风险的 VBA 工具。

这节课要看的不是“某一行代码怎么写”，而是：

```text
为什么要给 Agent 设计一组工具？
这些工具为什么要这样拆？
什么任务适合让 Agent 带着工具干活？
什么任务不适合全交给 Agent？
```

## 先把结论放在前面

合同字段抽取项目里，任务流程比较固定：

```text
上传合同
转成 Markdown
配置字段
AI 抽取 JSON
固定代码导出 Excel
```

所以它更适合：

```text
AI 负责理解和抽取
固定代码负责稳定交付
```

但是 Excel 办公助理不一样。

用户可能会说：

```text
帮我看看这个工作簿里有什么。
帮我复核这个表的合计。
帮我找出异常数据。
帮我把筛选结果放到新表。
帮我生成一个透视表。
帮我把当前选区整理成 Markdown。
```

这些任务不是固定流程。

Agent 需要自己判断：

```text
先看哪里
读哪些区域
要不要筛选
要不要写入
要不要新建工作表
要不要生成图表
要不要提醒用户确认风险操作
```

这类场景就很适合 Agent tool。

## 为什么不能让 AI 直接乱操作 Excel

Excel 是一个很危险的宿主环境。

因为它里面可能有：

```text
重要数据
公式
外部链接
隐藏表
筛选状态
财务底稿
审计痕迹
正在打开的多个工作簿
```

如果让 AI 没有边界地操作 Excel，风险会很高。

所以工具设计的第一层意义是：

```text
把 AI 的能力限制在可控动作里。
```

比如：

```text
读取当前选区
预览某个工作表
写入指定区域
创建一个新工作表
生成一个图表
把计算过程写到 AI计算草稿 表
```

这些动作都有明确输入、明确输出，也更容易记录日志和排查问题。

## 工具不是越多越好

很多人一开始会以为：

```text
工具越多，Agent 越强。
```

其实不是。

更准确的说法是：

```text
工具要覆盖任务需要，但每个工具都要边界清楚。
```

一个好的工具通常应该满足：

| 判断点 | 说明 |
|---|---|
| 名字清楚 | AI 看名字就知道什么时候用 |
| 参数明确 | 需要哪些输入，不要模糊 |
| 结果稳定 | 返回结构固定，方便 AI 继续推理 |
| 风险可控 | 写入、删除、运行 VBA 这类操作要有边界 |
| 粒度合适 | 不要一个工具包办所有事，也不要拆得太碎 |

工具的本质不是“函数列表”。

工具是给 AI 设计的一套工作方式。

## CPAHelper Agent 的工具分类

这个项目里的工具可以按用途分成几类。

### 1. 上下文工具

这类工具让 Agent 先知道自己在哪里。

```text
get_current_excel_context
get_excel_sheet_list
```

它们解决的问题是：

```text
当前工作簿是什么？
当前工作表是什么？
当前选区在哪里？
这个工作簿有哪些 Sheet？
```

这类工具很重要。

因为 Agent 在真正读写前，应该先确认上下文。

### 2. 预览工具

这类工具让 Agent 先粗看数据结构，而不是一上来就全表读取。

```text
preview_excel_sheet
preview_excel_range
```

它们适合用在：

```text
不知道表头在哪里
不知道有多少行
不知道哪些列有用
不知道当前选区是什么结构
```

这也是 Excel Agent 很重要的习惯：

```text
先预览，再精读，再行动。
```

### 3. 精确读取工具

当 Agent 确认了要读哪个区域，再用精确读取工具。

```text
get_excel_range_values_and_formulas
get_current_selection_values_and_formulas
find_excel_cells
```

这类工具适合：

```text
读取具体单元格
读取指定区域
查看公式
查找某个关键字
```

### 4. 写入工具

当 Agent 需要把结果写回 Excel，就会使用写入工具。

```text
write_excel_cell
write_excel_cells_batch
write_excel_range
fill_excel_formula_series
```

这里要特别注意：

```text
如果是长表里填同一类公式，优先用 fill_excel_formula_series。
```

因为这比让 AI 一格一格写更稳定，也更符合 Excel 的使用方式。

### 5. 计算工具

这个项目里有一个很值得讲的工具：

```text
append_calculation_scratchpad
```

它的作用是：

```text
把计算过程追加到 AI计算草稿 工作表里。
让 Excel 公式负责精确计算。
AI 负责组织计算步骤和解释结果。
```

这非常重要。

因为涉及金额、比例、差异、汇总时，不应该让大模型心算。

更稳的做法是：

```text
AI 设计计算过程
Excel 执行公式计算
用户可以在工作表里复核过程
```

### 6. 分析工具

这类工具用于更复杂的数据分析动作。

```text
manage_excel_filter
copy_visible_rows_to_sheet
create_excel_pivot_table
create_excel_chart
```

它们适合开放任务。

比如用户说：

```text
帮我找出金额大于 10 万的记录，复制到新表，并生成一个汇总图。
```

这时 Agent 可以自己组合多个工具完成任务。

### 7. 结构工具

这类工具会改变工作簿结构。

```text
create_excel_sheet
rename_excel_sheet
delete_excel_sheet
insert_excel_dimension
delete_excel_dimension
```

其中删除工作表、删除行列属于高风险动作。

工具设计里要明确标记风险，执行前要有保护机制。

### 8. 高风险工具

比如：

```text
run_vba_snippet
replace_external_links
delete_excel_sheet
```

这类工具不是不能给 Agent。

而是要有更强的限制。

比如：

```text
先验证
先生成计划
默认 dryRun
真正执行前需要确认
返回详细结果
失败时给出错误原因
```

这就是工具设计里的安全边界。

## 工具返回结果为什么要统一

工具执行以后，不能随便返回一段文字。

项目里有统一的 `ToolResult`。

它大概包含：

```text
success
status
message
data
error
```

这样做的好处是：

```text
Agent 能判断工具是否成功
Agent 能读取结构化 data
Agent 能在失败时看到 error
前端也能展示统一的结果
日志更容易排查
```

工具返回结果越稳定，Agent 后续越容易继续工作。

## 系统提示词也属于工具设计的一部分

工具不是注册进去就完了。

还要通过系统提示词告诉 Agent：

```text
什么时候应该先看上下文
什么时候应该预览表格
什么时候应该请求更多工具
什么时候应该用 Excel 公式计算
什么时候需要谨慎处理高风险工具
```

在这个项目里，系统提示词里有几个很关键的规则：

```text
面对未知工作表或大表时，先 preview。
涉及金额、税率、比例、汇总时，不要只靠心算。
复核、汇总、差异、多步推导，优先使用 AI计算草稿。
长表逐行公式，优先使用 fill_excel_formula_series。
高风险工具要先说明计划，并依赖宿主确认机制。
```

这说明：

```text
Agent 的效果不是只靠模型。
工具设计、提示词设计、宿主保护机制，都会影响最终效果。
```
