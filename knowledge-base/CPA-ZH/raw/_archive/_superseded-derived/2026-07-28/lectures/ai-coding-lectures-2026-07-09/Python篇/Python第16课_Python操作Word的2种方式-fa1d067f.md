---
source_type: "local-lecture"
source_role: "content"
representation: "semantic-transcript"
extraction_profile: "readable"
structure_status: "verified-auto"
source_pages: 0
heading_count: 15
table_count: 3
extraction_engine: "markdown-pass-through"
extraction_status: "ok"
structure_updated_at: "2026-07-28"
---

# Python 第 16 课：Python 操作 Word 的2种方式

## 今天先不急着做工具

前面我们已经处理过 PDF 和 Excel。

从这一节开始，我们进入另一个很常见的办公文件：

> Word 文档。

很多同学一听到 Word 自动化，第一反应可能是：

```text
能不能自动改格式？
能不能自动提取表格？
能不能批量转 PDF？
能不能帮我检查报告？
```

这些都可以做。

但在真正动手之前，我们先要理解一件事：

> Python 操作 Word，不只有一种方式。

不同方式适合不同场景。

如果一开始选错方向，后面就容易让 AI 写出很复杂、很不稳定、很难维护的代码。

## 今天要解决的问题

同样是 Word 自动化，背后可能是三条不同路线：

```text
第一种：用 python-docx 直接读取和生成 docx 文件。
第二种：用 COM 控制真正的 Word 软件。
第三种：把 docx 当成压缩包，理解里面的 XML 结构。
```

这节课不追求马上做出一个复杂工具。

今天的目标是：

> 以后你再遇到 Word 需求时，能先判断应该走哪条路。

## 你会学到

- `.docx` 文件为什么不是一个普通文档文件。
- `python-docx` 适合做什么。
- COM 操作 Word 适合做什么。
- XML 路线大概是什么。
- 为什么初学阶段不要直接手改 Word 底层 XML。
- 如何根据需求选择 Word 自动化方式。

## 小例子一：把 docx 看成一个文件包

先准备一个很简单的 Word 文件：

```text
data\word_demo.docx
```

里面放几段文字：

```text
一、项目基本情况
这是第一段正文。

二、审计发现
这是第二段正文。
```

然后复制一份，把后缀改成：

```text
word_demo.zip
```

解压以后，你会看到里面不是一个神秘的 Word 黑盒，而是一堆文件。

其中比较重要的是：

```text
word/
  document.xml
  styles.xml
  numbering.xml
  media/
```

这说明：

> `.docx` 本质上也是一个压缩包，里面保存了很多 XML 文件。

这和我们前面讲 Excel 时很像：

```text
.xlsx 是压缩包 + XML
.docx 也是压缩包 + XML
```

但今天只要知道这件事，不需要大家直接去改 XML。

## 方式一：python-docx

Word 篇最常用、最适合初学者的库是：

```text
python-docx
```

它的特点是：

```text
不需要打开 Word 软件
直接读取和写入 docx 文件
适合处理段落、标题、表格和简单格式
```

它很适合做这些事情：

- 读取 Word 里的段落。
- 提取标题目录。
- 提取 Word 表格。
- 生成一份新的 Word 报告。
- 对简单段落和表格做格式设置。
- 把 Word 里的信息整理到 Excel。

比如后面我们会做的工具：

```text
Word 表格/标题提取工具
```

就适合先用 `python-docx`。

## python-docx 不适合什么

`python-docx` 很实用，但不是万能的。

它不太适合：

- 完整保留特别复杂的排版。
- 处理修订痕迹、批注等复杂 Word 功能。
- 调用 Word 自带的另存为 PDF。
- 执行 Word 宏。
- 处理必须依赖 Word 软件本身的操作。

所以遇到 Word 需求时，不要只问：

```text
Python 能不能做？
```

还要继续问：

```text
我是要处理 docx 文件里的内容结构？
还是要控制 Word 软件本身？
```

## 方式二：COM 控制 Word 软件

第二种方式是 COM。

它可以理解成：

> Python 向 Windows 发指令，让真正的 Word 软件打开文档、执行操作、保存结果。

常见库是：

```text
win32com
```

COM 适合做这些事情：

- 批量打开 Word 文件。
- 把 Word 另存为 PDF。
- 执行 Word 宏。
- 调用 Word 软件自己的排版和转换能力。
- 处理 `.doc` 转 `.docx` 这类依赖 Word 的转换。

比如：

```text
批量把一个文件夹里的 docx 转成 PDF
```

这个需求就很适合考虑 COM。

因为“导出 PDF”本来就是 Word 软件自己很擅长的事情。

## COM 的注意事项

COM 很强，但也有代价。

它通常要求：

- Windows 系统。
- 本机安装了 Microsoft Word。
- Word 软件能正常启动。

它也更容易遇到这些问题：

- 速度比直接处理文件慢。
- Word 弹窗可能打断程序。
- 文件被占用时可能失败。
- 程序结束后要注意关闭 Word 进程。
- 不太适合放到服务器上长期跑。

所以 COM 不是“更高级”，只是适合另一类场景。

## 方式三：理解 docx 里的 XML

第三种方式是直接理解 Word 文件底层的 XML。

刚才我们已经看到：

```text
word/document.xml
word/styles.xml
word/numbering.xml
```

这些文件保存了 Word 文档的正文、样式、编号等信息。

有些高级工具会直接读取或修改这些 XML。

这条路线适合：

- 分析 Word 文件的底层结构。
- 读取 `python-docx` 不方便暴露的信息。
- 做非常细的格式或结构检查。

但对初学者来说，今天只需要记住：

> XML 是底层结构。先知道它存在，不要一上来就手改它。

我们优先用稳定的库和清晰的工具流程。

## 三种方式怎么选

可以先用这张表判断：

| 需求 | 推荐方式 | 原因 |
|---|---|---|
| 提取段落、标题、表格 | python-docx | 直接读取 docx，简单稳定 |
| 生成一份简单 Word 报告 | python-docx | 不需要打开 Word 软件 |
| Word 表格导出到 Excel | python-docx | 读取结构后交给 Excel 处理 |
| 批量 docx 转 PDF | COM | 导出 PDF 是 Word 软件能力 |
| 执行已有 Word 宏 | COM | 需要控制 Word 软件 |
| 分析特别底层的样式和编号 | XML | 需要读取 docx 内部结构 |
| 初学阶段做办公工具 | python-docx 优先 | 学习成本低，容易验证 |

## 今天课堂的小演示

今天可以让 AI 帮我们做三件小事。

第一步，解释 Word 自动化方式：

```text
请用零基础能理解的方式，解释 Python 操作 Word 的三种方式：
python-docx、COM、直接理解 docx 内部 XML。
请说明它们分别适合什么场景，不要直接写复杂代码。
```

第二步，读取一个 Word 的段落和表格数量：

```text
请帮我写一个最小示例，使用 python-docx 读取 data\word_demo.docx。
只打印：
- 段落数量
- 前 5 个非空段落
- 表格数量
不要修改原 Word 文件。
```

第三步，说明如果要批量转 PDF，为什么可能需要 COM：

```text
如果我要把一个文件夹里的 Word 批量另存为 PDF，
请说明为什么 python-docx 不适合做这件事，为什么可能要用 COM 控制 Word 软件。
先解释思路，不要急着写完整工具。
```

## 今天要记住

Python 操作 Word，不是只有一个答案。

先判断需求属于哪一类：

```text
处理 docx 文件内容结构 → 优先 python-docx
控制 Word 软件本身 → 考虑 COM
理解特别底层结构 → 再看 XML
```

这节课先把地图画清楚。

后面我们再开始复刻具体的 Word 工具。

## 做完以后你应该能

- 说清 `.docx` 和 XML 的关系。
- 解释 `python-docx` 适合做什么。
- 解释 COM 操作 Word 适合做什么。
- 知道为什么批量转 PDF 通常要考虑 COM。
- 遇到 Word 需求时，先做技术路线判断。

## 本节课提示词

把下面这段发给 AI：

```text
我想学习 Python 操作 Word 的三种方式。

请用适合零基础学员理解的方式讲清楚：
1. docx 文件为什么可以理解成一个压缩包，里面有 XML
2. python-docx 是什么，适合做哪些 Word 自动化任务
3. python-docx 不适合做哪些事情
4. COM 控制 Word 是什么，适合哪些任务
5. COM 方式有什么环境要求和风险
6. 直接理解 docx 内部 XML 是什么，为什么初学阶段不建议直接手改
7. 遇到不同 Word 需求时应该怎么选择路线

请再给一个最小演示代码：
- 使用 python-docx 读取 data\word_demo.docx
- 打印非空段落数量
- 打印前 5 个非空段落
- 打印表格数量
- 不修改原 Word 文件

最后请给出一个场景判断表：
- 标题提取
- 表格导出
- 生成简单 Word
- 批量转 PDF
- 执行 Word 宏
- 分析底层样式
分别推荐 python-docx、COM 还是 XML。
```
