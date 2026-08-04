---
source_type: "local-lecture"
source_role: "content"
representation: "semantic-transcript"
extraction_profile: "readable"
structure_status: "verified-auto"
source_pages: 0
heading_count: 25
table_count: 1
extraction_engine: "markdown-pass-through"
extraction_status: "ok"
structure_updated_at: "2026-07-28"
---

# VBA第06课：AI 完成功能区按钮的实现

## 这一节要做什么

前面几节我们已经手动理解了 VBA、按钮、回调和真正业务函数之间的关系。

这一节开始，让 AI 接管整个 VBA 工程。

你要做的是：

```text
在设计器里配置按钮和需求
  ↓
让 AI 读取项目说明
  ↓
AI 写 VBA 代码
  ↓
AI 注入 final.xlsm
  ↓
自动验证
  ↓
手动打开 Excel 再确认
```

## 本节你会学到

- 怎么在项目根目录打开 VS Code。
- `CLAUDE.md` 和 `AGENTS.md` 是什么。
- `src/AI_Generated.bas` 是做什么的。
- `export/` 目录是做什么的。
- `workbooks/source.xlsm`、`workbooks/final.xlsm`、`workbooks/backups/` 分别是什么。
- 怎么在设计器里给按钮写“给 AI 的功能说明”。
- 怎么让 AI 实现按钮功能并注入工作簿。
- 为什么让 AI 操作前要先关闭 `final.xlsm`。

## 先打开项目根目录

找到功能区设计器创建的项目文件夹。

在这个文件夹上右键：

```text
使用 VS Code 打开
```

注意，一定要在项目根目录打开。

如果打开错了目录，AI 可能看不到项目说明，也就不知道该怎样操作这个 VBA 工程。

## 认识项目里的关键文件

### CLAUDE.md 和 AGENTS.md

导出设计时，设计器会生成：

```text
CLAUDE.md
AGENTS.md
```

它们可以理解为写给 AI 的项目手册。

区别是：

- `CLAUDE.md`：给 Claude Code 读取。
- `AGENTS.md`：给其他 Agent 终端读取。

里面会告诉 AI：

- 当前项目是什么；
- 有哪些按钮；
- 每个按钮的回调过程是什么；
- 每个按钮的核心过程是什么；
- 应该在哪里写 VBA；
- 应该怎样把代码注入到工作簿；
- 应该怎样验证结果。

你不需要每天手写这些内容，但要知道它们很重要。

如果 AI 没读到这些手册，它就很难正确操作项目。

### project.json

`project.json` 是设计器的项目配置文件。

它保存：

- 选项卡；
- 分组；
- 控件；
- 图标；
- 按钮名称；
- 回调；
- 给 AI 的需求说明。

设计器重新打开项目时，会读取这个文件恢复界面。

### src 目录

重点看：

```text
src/AI_Generated.bas
```

这是 AI 写本次 VBA 代码的地方。

以后你想看 AI 这次到底写了哪些核心过程，通常就看这个文件。

### export 目录

`export/` 主要给 AI 读取旧代码用。

如果 AI 需要了解工作簿里已有 VBA，它可以把旧代码抽出来，放到这里分析。

### workbooks 目录

这个目录里通常有：

```text
workbooks/source.xlsm
workbooks/final.xlsm
workbooks/backups/
```

含义如下：

| 文件或目录 | 作用 |
| --- | --- |
| `source.xlsm` | 模板源文件，不要手动乱改 |
| `final.xlsm` | 最终产物，后面真正使用和测试它 |
| `backups/` | 每次修改前的备份，方便出问题后恢复 |

特别注意：

> 让 AI 注入代码前，一定要先关闭 `final.xlsm`。  
> 如果它还在 Excel 里打开，AI 很可能无法写入文件。

## 第一步：给按钮补充 AI 功能说明

回到功能区设计器，打开项目。

选中按钮，在属性里填写“给 AI 的功能说明”。

### 自动排序

可以写：

```text
自动排序当前选中的单元格。
如果是空单元格，则跳过。
只对数字排序。
不要影响未选中的区域。
```

### 添加 ROUND

可以写：

```text
对选中区域添加 ROUND 公式，保留两位小数。
跳过空单元格。
如果单元格已经是公式，要谨慎处理。
```

写完以后保存项目，并点击：

```text
导出设计
```

导出后，`CLAUDE.md` 和 `AGENTS.md` 里会带上这些按钮需求。

也就是说，AI 后面能直接看到每个按钮要做什么。

## 第二步：让 AI 实现自动排序

确认两件事：

- `final.xlsm` 已经关闭；
- VS Code 打开的是项目根目录。

然后启动 Claude Code 或 WorkBuddy。

可以这样说：

```text
帮我实现自动排序的功能。
先用 plan 模式确认你的实现计划，不要直接乱改。
```

你需要重点看 AI 的计划里有没有这些内容：

- 它知道项目里已经有按钮；
- 它知道回调模块由设计器生成；
- 它知道业务代码应该写到 `src/AI_Generated.bas`；
- 它知道需要注入到 `workbooks/final.xlsm`；
- 它知道注入后要做运行验证和结构检查。

确认没问题后，再让 AI 执行。

## 第三步：检查 AI 做了什么

AI 执行完成后，重点看几个结果：

- 是否写入了自动排序核心过程；
- 是否更新了 `src/AI_Generated.bas`；
- 是否注入了 `workbooks/final.xlsm`；
- 是否做了运行验证；
- 是否做了结构检查；
- 是否生成了备份。

如果这些都完成，说明工程流程基本跑通。

## 第四步：手动验证自动排序

打开：

```text
workbooks/final.xlsm
```

随便输入几个数字，例如：

```text
6
7
5
1
2
```

选中区域，点击：

```text
智能工具 → 数据处理组 → 自动排序
```

检查数字是否被正确排序。

再按：

```text
Alt + F11
```

看一下代码结构：

- 回调模块通常是设计器生成的；
- 真正实现通常在 `AI_Generated` 模块里；
- 回调过程会调用 AI 实现的核心函数。

## 第五步：继续实现添加 ROUND

先关闭 `final.xlsm`。

然后继续让 AI 做第二个按钮：

```text
将“添加 ROUND”功能实现。
先给出计划，确认后再写代码并注入。
```

AI 的计划里应该包含：

- 获取当前 `Selection`；
- 判断是否选中单元格区域；
- 遍历每个单元格；
- 空单元格跳过；
- 对数值或可计算公式添加 `ROUND(..., 2)`；
- 避免影响未选中区域；
- 注入后验证。

确认计划后，再让 AI 执行。

## 第六步：手动验证添加 ROUND

打开 `final.xlsm`。

准备几类测试数据：

- 普通小数；
- 公式结果；
- 空单元格；
- 已经有 `ROUND` 的单元格。

选中区域，点击：

```text
添加 ROUND
```

检查：

- 是否保留两位小数；
- 是否跳过空单元格；
- 是否没有影响未选中的区域；
- 公式是否符合你的预期。

## 完整工作流

以后做新的按钮，可以按这个流程走：

```text
设计器配置按钮和 AI 功能说明
  ↓
保存项目并导出设计
  ↓
关闭 final.xlsm
  ↓
在项目根目录启动 AI
  ↓
AI 读取 CLAUDE.md / AGENTS.md
  ↓
AI 写 src/AI_Generated.bas
  ↓
AI 注入 workbooks/final.xlsm
  ↓
AI 自动验证
  ↓
人工打开 final.xlsm 做最终确认
```

## 常见问题

### AI 提示无法写入文件

大概率是 `final.xlsm` 还在 Excel 里打开。

处理方法：

```text
关闭 final.xlsm → 再让 AI 重新注入
```

### 按钮能点，但没有效果

可能是真正业务函数只是占位过程，里面还没有写代码。

检查：

- 回调函数调用了哪个核心过程；
- `AI_Generated` 模块里这个过程是否有具体代码。

### 按钮报“子过程或函数未定义”

说明回调指向的核心过程不存在，或者名字不一致。

检查：

- 设计器中的核心过程名；
- 回调模块里的 `Call ...`；
- `AI_Generated` 模块里的 `Sub ...` 名称。

## 本节记住这五点

1. 设计器负责生成界面和回调。
2. `CLAUDE.md` / `AGENTS.md` 负责告诉 AI 项目规则。
3. AI 负责写核心业务函数并注入。
4. `final.xlsm` 是最终产物，AI 操作前要关闭。
5. 自动验证很有用，但最后仍然要自己打开 Excel 再试一次。

## 课后练习

在同一个项目中新增第 3 个按钮：

```text
清理空行
```

给 AI 的功能说明可以写：

```text
删除当前选中区域中整行内容为空的行。
只处理选中区域所在的行。
运行前弹窗确认。
运行后提示删除了多少行。
```

完成标准：

1. 在设计器里新增按钮并填写提示。
2. 导出设计。
3. 关闭 `final.xlsm`。
4. 让 AI 用 plan 模式实现。
5. 打开 `final.xlsm` 手动验证。
