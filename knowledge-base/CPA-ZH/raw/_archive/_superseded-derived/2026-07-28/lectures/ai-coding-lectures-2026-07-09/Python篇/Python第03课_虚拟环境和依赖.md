---
source_type: "local-lecture"
source_role: "content"
---

# Python 第 03 课：虚拟环境和依赖

## 今天先看懂“缺依赖”

上一节我们解决了“怎么稳定运行”。

今天解决另一个问题：

> 为什么我的电脑能跑，换一台电脑就跑不了？

这节课不要一上来就记命令。

我们先从一个报错开始。

## 今天要解决的问题

PDF 合并脚本需要一个第三方库，比如：

```text
pypdf
```

如果电脑里没有这个库，脚本就会报错：

```text
ModuleNotFoundError: No module named 'pypdf'
```

这句话的意思不是“你的 PDF 合并逻辑一定写错了”。

它的意思是：

```text
代码里用到了 pypdf，但当前 Python 环境里还没有安装它。
```

所以今天我们要搞清楚三件事：

- 代码缺的这个东西是什么。
- 用什么工具把它装上。
- 应该把它装到哪里。

## 你会学到

- Python 本体和第三方库是什么关系。
- 什么是第三方库。
- 什么是依赖。
- `pip` 是做什么的。
- 什么是虚拟环境。
- `.venv` 是什么。
- `requirements.txt` 是什么。

## 我们一起动手做

### 第一步：先运行脚本，观察缺依赖

在项目目录里运行：

```powershell
python .\pdf_merger.py
```

如果看到类似报错：

```text
ModuleNotFoundError: No module named 'pypdf'
```

先不要慌。

这是非常常见的依赖问题。

### 第二步：理解依赖是什么

先把 Python 和第三方库的关系说清楚。

安装 Python 以后，电脑里就有了 Python 解释器，也有了一些 Python 自带的基础工具。

这些自带工具叫标准库。

比如：

```text
os      处理文件夹和路径
sys     读取命令行参数
json    读写 JSON 数据
pathlib 更方便地处理路径
```

这些库是 Python 自带的，一般不需要额外安装。

但是 Python 不可能把所有功能都自带进来。

比如 PDF 合并、Excel 读写、网页请求、界面开发，这些更具体的能力，通常要借助别人写好的第三方库。
```
Python311
  python.exe
  Lib
    标准库
    site-packages
      第三方库
```

可以这样理解：

```text
Python 本体 = 发动机和基础工具箱
标准库 = Python 自带的常用工具
第三方库 = 别人做好的专用工具
```

我们写 PDF 合并工具时，没有自己从零开始研究 PDF 文件格式。

我们借用了别人已经写好的工具包：

```text
pypdf
```

这种被项目借用的外部工具包，就可以理解为项目的“依赖”。

一句话：

> 依赖解决的是“代码缺工具”的问题。

第三方库本身不是 Python 本体的一部分。

它是安装到某个 Python 环境里的扩展能力。

所以同一段代码在你的电脑上能运行，在别人电脑上不能运行，很多时候就是因为：

```text
你这里装了第三方库，别人那里还没装。
```

### 第三步：理解 pip 是什么

如果 `pypdf` 是我们要用的工具包，那么 `pip` 就是安装工具包的工具。

可以查看 pip 是否可用：

```powershell
python -m pip --version
```

安装依赖的命令是：

```powershell
python -m pip install pypdf
```

这里建议写成 `python -m pip`，而不是直接写 `pip`。

因为这样更清楚：

```text
请当前这个 Python 去运行 pip，并安装 pypdf。
```

### 第四步：先问一个问题，装到哪里了

直接安装依赖虽然可以解决眼前问题，但会带来一个新问题：

```text
pypdf 被装到哪个 Python 里了？
```

如果所有项目都把依赖装到全局 Python，时间久了会越来越乱：

- 这个项目需要一个版本。
- 另一个项目需要另一个版本。
- 有些包以后用不到了，但还留在电脑里。
- 换一台电脑时，不知道到底要装哪些包。

所以我们需要给当前项目准备一个独立的小房间。

这个小房间就是虚拟环境。

### 第五步：创建虚拟环境

在项目目录里运行：

```powershell
python -m venv .venv
```

`.venv` 是当前项目自己的 Python 环境。

可以把它理解为：

```text
这个项目专用的小工具间。
```

### 第六步：激活虚拟环境

PowerShell 中运行：

```powershell
.\.venv\Scripts\Activate.ps1
```

如果你使用的是 CMD，可以运行：

```cmd
.\.venv\Scripts\activate.bat
```

激活以后，命令行前面通常会出现：

```text
(.venv)
```

这表示你现在已经进入了这个项目自己的环境。

### 第七步：在虚拟环境里安装依赖

激活 `.venv` 后，再安装 `pypdf`：

```powershell
python -m pip install pypdf
```

这一次，`pypdf` 会安装到当前项目的虚拟环境里，而不是随便污染全局 Python。

### 第八步：再次运行 PDF 合并脚本

```powershell
python .\pdf_merger.py
```

如果缺依赖的问题解决了，脚本就会继续往下运行。

如果还报错，我们就继续读报错。

AI 编程也是这样：运行、观察、修正，再运行。

### 第九步：记录项目依赖

项目能在你电脑上跑还不够。

我们还要让别人知道：

```text
这个项目到底需要安装哪些包？
```

记录依赖：

```powershell
python -m pip freeze > requirements.txt
```

以后别人拿到项目后，可以先创建并激活虚拟环境，然后运行：

```powershell
python -m pip install -r requirements.txt
```

这样就能按照清单安装依赖。

## 今天要记住

依赖解决“代码缺工具”的问题。

虚拟环境解决“工具装在哪里”的问题。

`requirements.txt` 是这个项目的“工具清单”。

不是说“我电脑上能跑”就够了，而是要让别人也能复现。

## 做完以后你应该能

- 看懂 `ModuleNotFoundError: No module named 'pypdf'`。
- 解释为什么要安装 `pypdf`。
- 解释 `pip` 是安装依赖的工具。
- 创建并激活虚拟环境。
- 在虚拟环境里安装依赖。
- 生成 `requirements.txt`。
- 知道 `.venv` 不应该提交到 Git。

## 本节课提示词

把下面这段发给 AI：

```text
我正在做一个 Python PDF 合并工具，用到了 pypdf。

请帮我生成一份适合零基础学员理解的“依赖、pip 和虚拟环境”说明。

要求说明：
- Python 本体、标准库、第三方库分别是什么
- 第三方库和 Python 是什么关系
- ModuleNotFoundError: No module named 'pypdf' 是什么意思
- 什么是第三方库
- 什么是依赖
- 为什么这个项目需要 pypdf
- pip 是做什么的
- 为什么建议使用 python -m pip install pypdf
- 如果直接安装到全局 Python，可能有什么问题
- 什么是虚拟环境 .venv
- 为什么要先创建并激活虚拟环境，再安装依赖
- requirements.txt 的作用
- 为什么不能只说“我电脑上能跑”

请给出 Windows PowerShell 命令：
1. 运行脚本并观察缺依赖报错
2. 检查 pip 是否可用
3. 创建虚拟环境
4. 激活虚拟环境
5. 在虚拟环境里安装 pypdf
6. 再次运行脚本
7. 生成 requirements.txt
8. 根据 requirements.txt 安装依赖

最后请写一段可以放进 README 的“环境准备”说明。
```
