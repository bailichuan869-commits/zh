---
source_type: "local-lecture"
source_role: "content"
representation: "semantic-transcript"
extraction_profile: "readable"
structure_status: "verified-auto"
source_pages: 0
heading_count: 13
table_count: 0
extraction_engine: "markdown-pass-through"
extraction_status: "ok"
structure_updated_at: "2026-07-28"
---

# Python 第 12 课：从临时脚本到双击运行 EXE

## 今天解决一个最常见的小问题

真实工作里，很多自动化需求一开始都很小。

可能是同事问你：

> 我这里有几个 Excel，能不能帮我合一下、清一下、生成一个结果？

你用 Python 很快写了一个脚本。

在你的电脑上能跑。

但发给同事以后，他的电脑可能没有 Python、没有依赖库、不会打开命令行，也不知道脚本应该放在哪里。

所以今天这节课要解决的是：

> 把一个临时 Python 脚本打包成 EXE，让别人把文件按约定放好，双击一下就能运行。

这不是大型软件开发。

这是非常实用的“小工具交付”能力。

## 今天要解决的问题

临时脚本经常卡在这些地方：

- 只能在自己的电脑上运行。
- 同事电脑没有 Python。
- 同事不会安装依赖。
- 输入文件路径写死在代码里。
- 同事不知道文件应该放哪里。
- 运行完不知道结果在哪里。

所以今天不追求复杂界面，只追求一件事：

```text
同事按说明摆文件
双击 EXE
在 output 里拿结果
```

## 这一节的交付物

最终交付给同事的不是源码，而是一个文件夹：

```text
小工具交付包/
  run_tool.exe
  README.txt
  input/
    把要处理的文件放这里.txt
  output/
```

你只需要告诉同事三句话：

```text
1. 把要处理的 Excel 放到 input 文件夹。
2. 双击 run_tool.exe。
3. 处理结果在 output 文件夹。
```

这就是本节课的核心。

## 你会学到

- 临时脚本为什么不能直接发给别人。
- 如何把写死路径改成相对路径。
- 如何设计 `input`、`output`、`README` 交付结构。
- 如何让 EXE 双击运行，而不是要求别人输入命令。
- 如何在运行完成后暂停窗口，让同事看清成功或失败。
- 如何用 PyInstaller 打包一个单文件 EXE。
- 如何在另一台电脑或新文件夹里做交付测试。

## 案例：双击运行的 Excel 小工具

今天案例可以很小：

> 把 `input` 文件夹里的 Excel/CSV 文件合并成一个结果表。

工具规则：

- 读取 `input` 文件夹。
- 自动查找 `.xlsx` 和 `.csv` 文件。
- 合并所有数据。
- 增加“来源文件名”列。
- 输出到 `output\合并结果.xlsx`。
- 如果没有找到文件，要提示用户。
- 运行结束后停住窗口，显示“按回车键退出”。

这个案例的重点不是 Excel 汇总本身，而是：

> 文件夹约定清楚，别人不用改代码，也不用输入参数。

## 推荐项目结构

开发时项目可以这样放：

```text
one_click_tool/
  main.py
  requirements.txt
  README.txt
  input/
  output/
  src/
    excel_merge_tool.py
```

打包交付时可以这样放：

```text
交付包/
  run_tool.exe
  README.txt
  input/
  output/
```

课堂上要特别强调：

- `input` 和 `output` 使用相对路径。
- EXE 放在哪里，就以 EXE 所在目录作为工作目录。
- 不要让同事去改 Python 代码。
- 不要让同事去安装 Python。

## 脚本要做的小改造

临时脚本常常是这样：

```text
input_dir = "D:\我的项目\data"
output_file = "D:\我的项目\result.xlsx"
```

要改成：

```text
当前工具所在目录
  input
  output
```

也就是：

```text
input_dir = 工具目录 / "input"
output_file = 工具目录 / "output" / "合并结果.xlsx"
```

这样打包成 EXE 后，不管同事把交付包放到桌面、D 盘还是共享文件夹，都能按同样规则运行。

## 双击运行要注意什么

如果 EXE 一闪而过，同事会以为没运行。

所以脚本最后要有类似这样的行为：

```text
处理完成。
结果文件：output\合并结果.xlsx
按回车键退出...
```

如果报错，也要停住：

```text
处理失败：input 文件夹里没有找到 Excel 或 CSV 文件。
请把文件放到 input 文件夹后重新运行。
按回车键退出...
```

这比“程序崩了、一闪而过”好太多。

## 打包和测试

打包命令示例：

```powershell
pyinstaller --onefile --name run_tool main.py
```

打包后不要只在源码目录里测。

要新建一个测试交付包：

```text
测试交付包/
  run_tool.exe
  README.txt
  input/
    测试数据.xlsx
  output/
```

然后双击 `run_tool.exe`。

如果这里能跑，才说明真的可以发给别人。

## 今天要记住

这节课的关键词不是“高级”，而是“交付”。

```text
别人不需要懂 Python
别人不需要装环境
别人不需要输入命令
别人只需要按约定摆文件，然后双击
```

这就是很多日常小工具最实用的形态。

## 做完以后你应该能

- 把一个临时 Python 脚本改造成可交付的小工具。
- 设计清楚 `input` 和 `output` 文件夹约定。
- 打包一个双击运行的 EXE。
- 写一份同事能看懂的 `README.txt`。
- 在新文件夹里测试交付包是否真的可用。

## 本节课提示词

把下面这段发给 AI：

```text
我有一个临时 Python 脚本，想把它整理成可以发给同事使用的双击运行 EXE。

真实使用方式：
- 同事不安装 Python
- 同事不打开命令行
- 同事只需要把要处理的文件放进 input 文件夹
- 然后双击 run_tool.exe
- 处理结果输出到 output 文件夹

案例功能：
合并 input 文件夹里的 Excel/CSV 文件。

功能要求：
- 自动读取 EXE 所在目录下的 input 文件夹
- 自动创建 output 文件夹
- 读取 input 中的 .xlsx 和 .csv 文件
- 合并所有数据
- 增加“来源文件名”列
- 输出到 output\合并结果.xlsx
- 如果 input 文件夹不存在，自动创建并提示用户把文件放进去
- 如果 input 里没有 Excel/CSV 文件，给出中文提示
- 运行成功或失败后都不要让窗口一闪而过，要显示“按回车键退出”
- 代码适合零基础学员阅读

项目结构：
one_click_tool/
  main.py
  requirements.txt
  README.txt
  input/
  output/
  src/
    excel_merge_tool.py

请输出：
1. 需求理解
2. 推荐项目结构
3. main.py 代码
4. src\excel_merge_tool.py 代码
5. requirements.txt 内容
6. README.txt 示例
7. PyInstaller 打包命令
8. 打包后的交付包应该怎么摆
9. 如何在新文件夹里测试
10. 常见错误和排查方法
```
