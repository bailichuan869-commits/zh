---
source_type: "local-lecture"
source_role: "content"
---

# Python 第 08 课：打包 PDF 工具箱为 EXE

## 今天把工具箱交给别人用

前面我们已经把 PDF 合并工具做成了一个小工具箱：

- 有工具函数。
- 有 JSON 配置。
- 有 PySide6 GUI。
- 有模块化结构。

今天做第一模块的收尾：

> 把 PDF 工具箱打包成一个可以双击运行的 EXE。

## 今天要解决的问题

如果别人想用我们的工具，不能要求他每次都：

- 打开命令行。
- 激活虚拟环境。
- 安装依赖。
- 运行 Python 文件。

更友好的方式是：

```text
双击 EXE → 打开工具箱
```

## 你会学到

- 为什么要打包。
- 什么是入口文件。
- 什么是 PyInstaller。
- 什么是 `dist` 输出目录。
- 为什么打包后还要重新测试。
- 为什么配置文件、图标、模板可能要一起带上。

## 我们一起动手做

安装打包工具：

```powershell
python -m pip install pyinstaller
```

假设入口文件是：

```text
src\main.py
```

打包命令：

```powershell
pyinstaller --onefile --windowed src\main.py
```

打包后查看：

```text
dist/
  main.exe
```

## PySide6 打包要注意

桌面 GUI 项目打包后，常见问题包括：

- 找不到配置文件。
- 找不到图标或资源。
- 路径从开发目录变成了 EXE 所在目录。
- 打包文件比较大。
- 杀毒软件可能误报。

所以打包不是结束，打包后一定要重新测试。

## 今天要记住

打包不是开发结束，而是交付开始。

能在开发环境运行，不代表打包后一定能运行。

## 做完以后你应该能

- 解释为什么要打包 EXE。
- 使用 PyInstaller 打包一个 PySide6 工具箱。
- 找到 `dist` 里的 EXE。
- 知道打包后要测试配置、输出和核心功能。
- 知道用户使用 EXE 时不需要理解 Python 环境。

## 本节课提示词

把下面这段发给 AI：

```text
我已经有一个 Python PDF 工具箱项目，使用 PySide6 做了桌面 GUI。

现在我想把它打包成 Windows EXE，方便不会 Python 的同事双击使用。

项目情况：
- 入口文件：src\main.py
- 工具逻辑在 src\tools
- GUI 在 src\ui
- 配置文件在 config
- 输出目录是 output

请帮我生成打包方案。

要求说明：
- 为什么要打包 EXE
- PyInstaller 是什么
- 如何安装 PyInstaller
- 最简单的打包命令
- --onefile 和 --windowed 分别是什么意思
- 打包后 dist 目录里会有什么
- PySide6 项目打包常见问题
- config 配置文件如何处理
- 打包后如何测试

请输出：
1. 打包前检查清单
2. 安装和打包命令
3. 如果需要带 config 目录，应该怎么处理
4. 打包后测试清单
5. 常见错误和排查方法
6. 给用户的简短使用说明
```
