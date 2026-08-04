---
source_type: "local-lecture"
source_role: "content"
representation: "semantic-transcript"
extraction_profile: "readable"
structure_status: "verified-auto"
source_pages: 0
heading_count: 14
table_count: 0
extraction_engine: "markdown-pass-through"
extraction_status: "ok"
structure_updated_at: "2026-07-28"
---

# Python 第 02 课：命令行、路径和稳定运行

## 今天亲手敲几条命令

上一节我们已经让 AI 写出了第一个 PDF 合并脚本。

今天先不急着继续加功能。

我们要做一件很基础、但非常重要的事：

> 亲手在命令行里输入命令，理解 AI 编程工具到底是在电脑里做什么。

AI 帮我们编程时，不是凭空把项目变出来。它也需要看目录、读文件、运行命令、观察报错，然后再继续修改。

你看懂命令行，就开始看懂 AI 是怎么工作的。

## 今天要解决的问题

初学者经常会遇到这些情况：

- 明明文件存在，程序却说找不到。
- 同一段代码，有时候能跑，有时候不能跑。
- AI 让你运行一条命令，但你不知道这条命令在干什么。
- 看到 `python pdf_merger.py`，感觉像一串咒语。

今天我们要把这件事拆开。

命令行不是魔法。

命令行就是你用文字告诉电脑：

```text
我要让哪个程序，在什么位置，对哪个文件，做什么事情。
```

## 你会学到

- 什么是命令行。
- 什么是当前目录。
- 如何查看文件夹里有什么。
- 什么是相对路径和绝对路径。
- 为什么路径里有空格要加引号。
- `python` 命令到底是在叫谁干活。
- AI 运行代码时，为什么也需要看命令输出和报错。

## 案例一：我现在在哪里

先打开命令行，进入我们的项目目录。

然后输入：

```powershell
pwd
```

这条命令是在问电脑：

```text
我现在站在哪个文件夹里？
```

再输入：

```powershell
ls
```

这条命令是在问电脑：

```text
这个文件夹里有什么？
```

接着试一下切换目录：

```powershell
cd .\课程附件
ls
cd ..
```

这里要记住一句话：

> 命令不是飘在空中执行的，它一定是在某个文件夹里执行的。

很多“找不到文件”的问题，本质上不是代码错了，而是你或者 AI 站错了文件夹。

## 案例二：同一个文件，路径有不同写法

假设我们有一个测试文件夹：

```text
课程附件\PDF测试文件
```

可以用相对路径查看它：

```powershell
ls .\课程附件\PDF测试文件
```

也可以用绝对路径查看它：

```powershell
ls "D:\xxx\ai-coding-study\课程附件\PDF测试文件"
```

相对路径，是从当前目录出发。

绝对路径，是从盘符出发。

程序不是“知道你想找哪个文件”，它只认识你给它的路径。

## 案例三：路径里有空格为什么要加引号

如果文件夹名字里有空格，比如：

```text
课程附件\PDF 测试文件
```

这条命令可能会出问题：

```powershell
ls .\课程附件\PDF 测试文件
```

因为命令行会把空格当成参数分隔。

所以应该写成：

```powershell
ls ".\课程附件\PDF 测试文件"
```

这就是为什么 AI 生成命令时，经常会给路径加引号。

引号不是装饰，它是在告诉命令行：

```text
这一整段是一个路径。
```

## 案例四：python 命令到底是在叫谁

现在我们来看这条命令：

```powershell
python .\pdf_merger.py
```

这句话可以拆成三层：

```text
python           叫谁来干活
.\pdf_merger.py  让它运行哪个脚本
后面的参数       告诉脚本具体怎么做
```

所以：

```text
python = 执行程序
pdf_merger.py = 任务说明书
input/output = 任务参数
```

`python` 不是代码。

`python` 是安装在电脑里的一个程序。我们在命令行输入 `python`，就是请 Python 解释器读取 `.py` 文件，并按照里面的代码一步一步执行。

## 案例五：先运行一个最小脚本

为了理解 `python` 命令，我们先不要直接跑 PDF 合并工具。

在项目目录中新建一个文件：

```text
hello.py
```

写入：

```python
print("你好，我是 Python 脚本")
```

然后在命令行运行：

```powershell
python .\hello.py
```

这条命令的意思是：

```text
请 Python 运行 hello.py 这个脚本。
```

如果命令行里打印出了文字，就说明 Python 已经开始替我们执行脚本了。

## 案例六：脚本也可以接收参数

再新建一个文件：

```text
say_hello.py
```

写入：

```python
import sys

name = sys.argv[1]
print("你好，" + name)
```

运行：

```powershell
python .\say_hello.py 小王
python .\say_hello.py 小李
```

现在这条命令就可以拆开看：

```text
python          启动 Python
say_hello.py    运行这个脚本
小王             传给脚本的参数
```

理解了这个，我们再看 PDF 工具就不陌生了。

例如：

```powershell
python .\pdf_merger.py --input ".\input_pdfs" --output ".\output\merged.pdf"
```

它的意思是：

```text
请 Python 运行 pdf_merger.py。
输入文件夹是 input_pdfs。
输出文件是 output\merged.pdf。
```

## 案例七：故意制造一次找不到文件

现在我们故意把输入文件夹名字写错：

```powershell
python .\pdf_merger.py --input ".\wrong_folder" --output ".\output\merged.pdf"
```

观察报错。

看到红字不要慌，先找关键词：

```text
No such file or directory
找不到指定的路径
```

报错不是敌人。

报错是线索。

AI 编程工具也是这样工作的：先运行命令，看到报错，再根据报错继续修改。

## 今天要记住

命令行做的事情可以拆成四个问题：

- 我现在站在哪个目录？
- 我要调用哪个程序？
- 我要让它处理哪个文件？
- 我要给它什么参数？

`python .\pdf_merger.py` 不是咒语。

它的意思是：

```text
请 Python 解释器运行这个 Python 脚本。
```

当你看懂这句话，后面学习虚拟环境、依赖安装、打包 EXE，都会顺很多。

## 做完以后你应该能

- 用 `pwd` 判断当前目录。
- 用 `ls` 查看文件夹内容。
- 用 `cd` 切换目录。
- 解释相对路径和绝对路径。
- 解释为什么路径有空格时要加引号。
- 说清楚 `python .\xxx.py` 这条命令的含义。
- 把“找不到文件”的问题说清楚发给 AI。

## 本节课提示词

把下面这段发给 AI：

```text
我正在学习如何在命令行运行 Python PDF 合并工具。

请你用适合零基础学员的方式，帮我解释这些内容：
- 命令行是什么
- pwd、ls、cd 分别在做什么
- 什么是当前目录
- 什么是相对路径
- 什么是绝对路径
- 路径里有空格为什么要加引号
- python .\pdf_merger.py 这条命令到底是什么意思
- python、脚本文件、命令参数之间是什么关系

请再帮我设计一个课堂练习：
1. 先用 pwd、ls、cd 观察项目目录
2. 再创建 hello.py 并用 python .\hello.py 运行
3. 再创建 say_hello.py，让脚本接收一个名字参数
4. 最后回到 pdf_merger.py，用 --input 和 --output 参数运行 PDF 合并工具
5. 故意写错一次路径，观察报错并解释原因

如果需要改进 pdf_merger.py，请帮我加上：
- 运行时打印当前工作目录
- 检查输入文件夹是否存在
- 检查输出目录是否存在，不存在就创建
- 出错时给出适合零基础学员理解的中文提示

请输出：
1. 概念解释
2. 课堂命令清单
3. hello.py 示例
4. say_hello.py 示例
5. PDF 合并工具运行示例
6. 常见报错和排查方法
```
