---
source_type: "local-lecture"
source_role: "content"
---

# Python 第 22 课：本地桌面路线 React + pywebview

## 这一课要解决的问题

前面我们已经做出了一套 Python 工具箱：

- `core/`、`excel/`、`pdf/`、`word/` 负责真正处理文件和数据。
- `gui/` 和 `main.py` 是 PySide6 桌面入口。
- 工具层已经能被不同入口调用。

PySide6 能做桌面软件，前面的版本也已经够我们使用。

但它有一个现实问题：

> 如果想让 AI 帮我们修改和美化界面，网页界面通常比 PySide6 界面更好改。

现在 AI 对 HTML、CSS、React 和网页组件的训练材料更多。你让 AI 做一个网页工具界面，它更容易给出结构清楚、视觉更现代、交互更完整的结果。

所以这一课我们学习一条新路线：

```text
先让 AI 做网页界面
再用 pywebview 把网页装进桌面窗口
最后仍然调用本机 Python 工具层
```

完整调用链是：

```text
React 前端 -> pywebview 桥接 -> Python 工具层
```

这条路线适合做“装在自己电脑上的办公自动化软件”。

## pywebview 是什么

pywebview 不是 FastAPI，也不是一个后端服务器。

你可以把它理解成两件事：

- 打开一个桌面窗口，窗口里显示 HTML/React 页面。
- 把 Python 对象暴露给前端，让 JavaScript 可以调用本机 Python 方法。

所以前端调用 Python 的方式不是：

```text
fetch("/api/xxx")
```

而是类似：

```text
window.pywebview.api.xxx()
```

这就是 pywebview 的核心：

```text
桌面壳 + JS-Python 桥接
```

## 为什么这条路线适合办公工具箱

很多办公自动化工具不是给一群人访问服务器，而是给自己或同事在本机处理文件。

这类需求有几个特点：

- 文件在本机磁盘上。
- 经常要选择文件夹、选择输出路径。
- 可能要调用本机 Excel、Word、COM。
- 用户希望双击打开，像普通软件一样使用。
- 不希望文件上传到服务器。

这时 pywebview 就很自然。

它让我们同时得到两边的好处：

- 用网页技术做界面，AI 更擅长生成和调整。
- 用 Python 继续处理 Excel、PDF、Word 和本机文件。
- 用 pywebview 把网页界面包装成桌面软件。

所以这一课不是为了追新技术，而是为了解决一个实际问题：

> 桌面工具需要更好看的界面，而网页界面更适合交给 AI 开发。

## 这条路线的项目结构

可以让 AI 按下面的结构整理项目：

```text
excel_tools/
  core/
    rename.py
    round.py
    financial_reports.py
  excel/
    com.py
    xml.py
  pdf/
    core.py
  word/
    extract.py

  web/
    src/
      App.jsx
      styles.css
    package.json
    vite.config.js

  webview_api.py
  webview_main.py
  main.py
```

各层职责：

- `core/`、`excel/`、`pdf/`、`word/`：业务工具层，只负责干活。
- `web/src/App.jsx`：React 页面，只负责展示、点击、状态和参数。
- `webview_api.py`：桥接层，把 Python 方法暴露给前端。
- `webview_main.py`：桌面入口，打开 pywebview 窗口。
- `main.py`：保留原来的 PySide6 入口，方便对比和过渡。

## 这一课你要看懂什么

这一课不要求你逐行掌握 React。

重点是看懂四个判断：

1. PySide6 能用，但网页界面更适合让 AI 开发。
2. pywebview 适合本地文件工具箱。
3. 业务逻辑不能写进 `App.jsx`。
4. `webview_api.py` 是桥接层，不是业务层。

代码可以交给 AI 生成和调整，但你要能检查边界有没有乱：

```text
前端只管交互
桥接层只管连接
工具层只管业务
入口层只管启动
```

只要这几个边界清楚，项目后面就不容易越改越乱。

## 这条路线的优点

- 更像普通桌面软件，容易做出成品感。
- 文件默认留在本机，适合审计、财务、办公自动化。
- 能调用本机 Excel、Word 和文件选择框。
- 网页界面比传统桌面 GUI 更适合让 AI 生成、调整和美化。
- 打包后可以发给同事使用。

## 这条路线的缺点

- 主要适合单机使用。
- 不适合天然多人同时访问。
- 前端依赖 pywebview 环境，直接用浏览器打开时能力不完整。
- 如果未来要部署到服务器，还需要改成 API 服务路线。

## 学习时可以怎么观察

建议你先对比两个版本：

1. 打开现有 PySide6 版本，看传统桌面入口是什么样。
2. 再打开 React + pywebview 版本，看同一批工具如何换成网页界面。

观察时不要陷入 UI 细节，重点看懂调用链：

```text
webview_main.py
  创建窗口，加载 React 页面，注入 Python API

webview_api.py
  暴露 choose_folder、start_job、get_job 等方法

web/src/App.jsx
  通过 window.pywebview.api 调用 Python
```

你真正要带走的是：同一套 Python 工具层，可以换不同的界面入口。

## 本节课提示词

把下面这段发给 AI：

```text
我有一个 Python 办公自动化工具箱项目，业务能力已经分散在 core、excel、pdf、word 等模块中。

现在 PySide6 版本已经能用，但我希望界面更现代，也希望利用 AI 更擅长开发网页界面的特点。

现在我想走本地桌面应用路线：
React 前端 -> pywebview 桥接 -> Python 工具层。

请帮我设计并实现一个最小可运行版本。

目标：
- 不重写业务工具函数
- React 页面只负责界面、按钮、参数和状态展示
- webview_api.py 负责把 Python 方法暴露给前端
- webview_main.py 负责启动 pywebview 桌面窗口
- 前端通过 window.pywebview.api 调用 Python
- 保留原来的 PySide6 入口，方便对比

请输出：
1. 推荐项目结构
2. 为什么从 PySide6 过渡到 React + pywebview
3. 需要安装的 Python 和前端依赖
4. webview_main.py 示例
5. webview_api.py 示例
6. React 前端如何调用 Python 方法
7. 如何启动开发模式和构建桌面版本
8. 常见错误：把业务逻辑写进前端或桥接层

请用适合零基础同学理解的方式解释。
```

## 今天要记住

pywebview 解决的是：

> 把网页界面变成本地桌面软件。

它适合本机文件处理、本机 Excel/Word 自动化、单机办公工具箱。

真正稳定的资产不是 pywebview，也不是 React 页面，而是后面的业务工具层。
