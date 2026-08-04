---
source_type: "local-lecture"
source_role: "content"
representation: "semantic-transcript"
extraction_profile: "readable"
structure_status: "verified-auto"
source_pages: 0
heading_count: 17
table_count: 3
extraction_engine: "markdown-pass-through"
extraction_status: "ok"
structure_updated_at: "2026-07-28"
---

# Python 第 25 课：Web 小案例：PDF 转 Markdown 网站

## 这一课要做什么

上一课我们把前面的知识点做了一次总复习。

这一课用一个很小的网站案例，把前面的链路再顺一遍：

> 用户在网页上传 PDF，Python 后端接收文件，调用已有解析能力，把 PDF 转成 Markdown，再把结果返回给前端下载或预览。

这个案例不追求功能复杂。

重点是把下面这条链路看清楚：

```text
浏览器页面 -> 上传 PDF -> FastAPI 后端 -> Python 工具层 -> Markdown 结果 -> 页面展示/下载
```

## 为什么选 PDF 转 Markdown

前面我们已经学过：

- PDF 工具。
- Markdown 结构化写作。
- MinerU 文档解析 API。
- FastAPI + 前端 Web 服务路线。
- 工具层和入口层分离。

PDF 转 Markdown 正好能把这些点串起来。

它不是一个全新的大项目，而是把前面学过的能力重新组合：

```text
PDF 文件输入
解析工具处理
Markdown 文本输出
Web 页面作为入口
```

## 需求说明

这个小网站的最小需求：

1. 浏览器打开一个页面。
2. 页面上可以选择一个 PDF 文件。
3. 点击按钮后，把 PDF 上传到后端。
4. 后端保存到临时目录。
5. 后端调用已有 PDF 转 Markdown 能力。
6. 转换成功后，返回 Markdown 内容或下载地址。
7. 前端展示转换状态，并提供预览或下载。
8. 转换失败时，页面显示清楚的中文错误信息。

先不要做太多功能。

第一版只要跑通：

```text
上传一个 PDF -> 得到一个 Markdown
```

## 推荐项目结构

可以让 AI 按下面结构生成：

```text
pdf_to_md_web/
  app/
    main.py
    pdf_to_md.py
  web/
    index.html
  uploads/
  outputs/
  requirements.txt
  README.md
```

各层职责：

- `web/index.html`：前端页面，只负责选择文件、上传、展示状态、显示结果。
- `app/main.py`：FastAPI 入口，只负责接收请求、保存文件、调用工具层、返回结果。
- `app/pdf_to_md.py`：工具层，只负责把 PDF 转成 Markdown。
- `uploads/`：临时保存上传的 PDF。
- `outputs/`：保存转换后的 Markdown。

最重要的是这条边界：

```text
PDF 转 Markdown 的核心逻辑，不要写进 index.html，也不要全塞进 main.py。
```

## 后端接口设计

最小接口可以只有一个：

```text
POST /api/pdf-to-md
```

请求：

```text
上传一个 PDF 文件
```

返回：

```json
{
  "success": true,
  "filename": "sample.pdf",
  "markdown_preview": "# 标题...",
  "download_url": "/outputs/sample.md"
}
```

失败时返回：

```json
{
  "success": false,
  "message": "请上传 PDF 文件"
}
```

如果暂时还没接入真实 MinerU 或 PDF 解析工具，也可以先写一个假的 `pdf_to_md.py`：

```text
收到 PDF -> 生成一个示例 Markdown -> 跑通前后端链路
```

等链路跑通后，再把假的函数替换成真实解析函数。

这就是前面反复讲的：

```text
先做最小可运行版本，再替换真实能力。
```

## 前端页面需求

前端不用复杂。

有这些元素就够：

- 文件选择框。
- “开始转换”按钮。
- 转换中状态。
- 错误提示。
- Markdown 预览区域。
- 下载按钮或下载链接。

前端只负责交互，不负责解析 PDF。

前端调用后端时，用：

```text
fetch("/api/pdf-to-md")
```

不要在前端写死本机路径，比如：

```text
D:\某个文件夹\sample.pdf
```

浏览器不能直接操作用户电脑上的任意路径。

## 这一课要复习的点

这个小案例主要复习这些内容：

| 知识点 | 在案例里的位置 |
|---|---|
| 项目结构 | `app/`、`web/`、`uploads/`、`outputs/` |
| 虚拟环境和依赖 | `requirements.txt` |
| FastAPI | 接收上传文件、返回 JSON |
| 文件路径 | 上传目录、输出目录、文件名处理 |
| Markdown | 转换后的结果格式 |
| MinerU / PDF 解析 | 工具层里的真实转换能力 |
| 前端 fetch | 上传 PDF、接收结果 |
| 工具层分离 | `pdf_to_md.py` 不依赖页面 |

## 要注意什么

### 1. 文件上传不是本地路径

网页里选择文件后，浏览器上传的是文件内容。

后端不能假设自己能直接读取用户电脑上的路径。

正确流程是：

```text
前端选择文件 -> 上传文件内容 -> 后端保存临时文件 -> 后端处理
```

### 2. 临时文件要管理

上传的 PDF 和生成的 Markdown 要放到固定目录。

比如：

```text
uploads/
outputs/
```

后面可以再考虑：

- 文件名冲突。
- 转换失败后的清理。
- 旧文件定期删除。

第一版先把目录分清楚。

### 3. 接口返回要清楚

不要只返回一大段字符串。

建议返回结构化 JSON：

```text
是否成功
原始文件名
预览内容
下载地址
错误信息
```

这样前端才知道怎么展示。

### 4. 工具层不要依赖网页

`pdf_to_md.py` 只应该关心：

```text
输入 PDF 路径
输出 Markdown 路径
```

它不应该关心按钮、页面、HTTP 请求。

这样以后这个转换能力还可以接到：

- 命令行。
- pywebview 桌面软件。
- AI 文档助手。
- 批量处理脚本。

### 5. 真实解析能力可以后接

如果课堂上真实 PDF 解析太慢或依赖复杂，可以先用假函数跑通链路。

比如先生成：

```markdown
# 转换结果

文件 sample.pdf 已上传。

这里后续替换为真实 PDF 解析结果。
```

跑通以后，再接 MinerU 或其他 PDF 转 Markdown 工具。

这不是偷懒，而是正确的开发顺序。

## 今天要记住

这个案例要记住的不是某一段代码，而是完整链路：

```text
前端负责上传和展示
后端负责接收和返回
工具层负责真正转换
文件目录负责保存输入输出
```

只要这个结构清楚，后面把“小网站”升级成更完整的文档助手就很自然。

## 本节课提示词

把下面这段发给 AI：

```text
我想做一个 Python Web 小案例，用来复习 FastAPI、文件上传、前端 fetch、Markdown 输出和工具层分离。

案例名称：PDF 转 Markdown 网站。

最小需求：
- 浏览器打开一个页面
- 用户上传一个 PDF 文件
- FastAPI 后端接收 PDF
- 后端把 PDF 保存到 uploads/
- 后端调用 app/pdf_to_md.py 里的工具函数
- 工具函数把 PDF 转成 Markdown，并保存到 outputs/
- 后端返回 JSON，包括 success、filename、markdown_preview、download_url 或错误信息
- 前端展示转换状态、Markdown 预览和下载链接

项目结构：
pdf_to_md_web/
  app/
    main.py
    pdf_to_md.py
  web/
    index.html
  uploads/
  outputs/
  requirements.txt
  README.md

要求：
1. 第一版可以先用假转换函数跑通链路
2. pdf_to_md.py 只写转换逻辑，不写 FastAPI 和页面代码
3. main.py 只写接口、文件保存和结果返回
4. index.html 用原生 HTML/CSS/JS 即可
5. 说明如何启动、如何测试、如何替换成真实 MinerU 或 PDF 解析能力
6. 代码适合零基础同学阅读，关键位置加少量中文注释
```
