---
source_type: "local-lecture"
source_role: "content"
representation: "semantic-transcript"
extraction_profile: "readable"
structure_status: "verified-auto"
source_pages: 0
heading_count: 8
table_count: 0
extraction_engine: "markdown-pass-through"
extraction_status: "ok"
structure_updated_at: "2026-07-28"
---

# Python 第 09 课：Claude Code 安装

## 今天安装一个命令行 AI 编程工具

前面我们已经做出了 PDF 工具箱，并完成了打包。

从这一节开始，我们补充一个更偏工程实践的 AI 编程工具：

> Claude Code。

它可以在命令行里读取项目、修改文件、运行命令，也更容易让学员理解 AI 编程工具是怎么和项目目录交互的。

## 安装命令

npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com


## 常用启动方式

最高权限：

claude --permission-mode bypassPermissions

## 常用操作

1. 对话框中直接输命令：! xx
2. ctr + B 后台运行，继续对话
3. ctr + O 打开细节
4. @具体文件
5. ctr+回车换行

## 注意

1. 不能鼠标选择对应位置编辑
2. 图片：得看模型是否支持多模态

## 斜杠命令

/help
/model  切换模型
/btw  临时会话，不打断当前对话 esc退出
/compact 主动压缩
/clear 清空上下文
/resume 继续上次对话
/init 初始化claude.md
/simplify 从质量、效率、复用性来review
/memory 打开记忆


## 回滚

两下esc或者/rewind  回滚    无法回滚中间执行过的命令，比如安装了新的依赖，最终还是靠git
