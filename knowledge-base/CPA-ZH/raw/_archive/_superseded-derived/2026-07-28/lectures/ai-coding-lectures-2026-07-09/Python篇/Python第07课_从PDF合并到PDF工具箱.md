---
source_type: "local-lecture"
source_role: "content"
---

# Python 第 07 课：从 PDF 合并到 PDF 工具箱

## 今天从一个工具升级到工具箱

前面我们一直围绕 PDF 合并。

今天要把思路往前推一步：

> 如果以后还要加 PDF 拆分、提取页面、加水印、旋转页面，项目应该怎么组织？

## 今天要解决的问题

如果所有功能都继续塞到一个文件里，很快会乱：

- GUI 代码和处理逻辑混在一起。
- 配置读取到处复制。
- 新增工具时不知道改哪里。
- 后面很难做成审计工具箱。

## 你会学到

- 什么是模块化。
- `tools`、`core`、`ui` 分别做什么。
- 什么是工具注册表。
- 为什么从第一个小工具开始就要控制结构。

## 我们一起动手做

把项目整理成工具箱雏形：

```text
pdf_tools_demo/
  config/
    pdf_merge_config.json
  data/
    input_pdfs/
  output/
  src/
    main.py
    core/
      config_manager.py
      logger.py
      tool_registry.py
    tools/
      pdf_merger.py
    ui/
      app.py
  README.md
  requirements.txt
  .gitignore
```

工具注册表示意：

```text
pdf_merge -> PDF 合并
```

后面可以继续扩展：

- PDF 拆分。
- 提取指定页。
- 加水印。
- 页面旋转。
- 批量重命名。

## 今天要记住

我们不是为了 PDF 合并而拆模块。

我们是为了让项目以后还能长大。

## 做完以后你应该能

- 解释为什么不能把所有代码放一个文件。
- 说清 `core`、`tools`、`ui` 的分工。
- 设计一个简单工具注册表。
- 看出 PDF 工具箱和后续审计工具箱之间的关系。

## 本节课提示词

把下面这段发给 AI：

```text
我现在有一个 Python PDF 合并工具，想把它整理成 PDF 工具箱雏形。

目标结构：
src/
  main.py
  core/
    config_manager.py
    logger.py
    tool_registry.py
  tools/
    pdf_merger.py
  ui/
    app.py
config/
  pdf_merge_config.json

改造要求：
- main.py 只负责启动程序
- tools 存放具体 PDF 工具逻辑
- ui 存放界面代码
- core 存放配置读取、日志、工具注册表
- tool_registry.py 先注册 pdf_merge 工具
- 后续要方便新增 PDF 拆分、提取页面、加水印等工具
- 不要改坏已有 PDF 合并功能

请输出：
1. 推荐项目结构
2. 每个文件的职责
3. tool_registry.py 示例
4. main.py 示例
5. 改造步骤
6. 改造后如何验证 PDF 合并仍然能运行
```
