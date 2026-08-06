---
title: CPA-ZH Agent 工具
type: concept
concept_type: automation-tool
created: 2026-08-04
updated: 2026-08-04
tags: [agent, mcp, cli, knowledge-base, review-gate]
sources: [cpa-zh-agent-architecture]
raw_path: workspace/docs/cpa-zh-agent.md
related: [[concepts/ai-coding-tool-registry]], [[concepts/kb-maintenance-workflow]], [[concepts/kb-user-guide]]
domain: tools
topic: helpers
---

# CPA-ZH Agent 工具

CPA-ZH Agent 工具把知识库搜索、阅读、资料摄入、问答沉淀、案例草稿和页面复核统一到共享 Python 服务层。CLI 与本机 stdio MCP 使用相同业务逻辑，浏览器保持只读。

## 组件

| 组件 | 入口 | 职责 |
|---|---|---|
| 共享服务 | `tools/cpa_zh_agent_service.py` | 路径安全、完整预览、哈希校验、短期令牌和提交后维护 |
| JSON CLI | `tools/cpa_zh_agent.py` | 脚本、批处理和人工终端操作 |
| stdio MCP | `tools/cpa_zh_mcp.py` | 供 Codex 或其他本机 Agent 客户端调用，不监听端口 |

## 读取能力

- `search`：关键词检索，可限定 wiki/raw、领域和数量。
- `read_page`：读取 wiki frontmatter、完整正文、关联页面和内容哈希。
- `read_raw`：读取 raw 文本；二进制原件必须存在 Markdown 门面。
- `health`：检查缓存、索引、manifest、README 统计和知识库健康状态。
- `pending_reviews` / `review_detail`：列出待复核页面并读取完整正文。

## 写入门控

`ingest_preview`、`qa_preview`、`case_preview` 和 `review_preview` 只生成计划，不写知识资产。预览返回目标路径、来源、拟变更、完整 Markdown 或文件清单、风险提示、内容哈希和 10 分钟令牌。

只有用户看完完整预览并明确批准后，Agent 才能用原令牌调用 `commit`，且必须传入 `confirmed=true`。提交前重新校验：

1. 令牌未过期且属于当前 CPA-ZH 根目录；
2. 输入文件或目录哈希未变化；
3. 目标文件状态未变化；
4. 待复核页面仍满足准入条件；
5. 令牌尚未被使用。

commit 后自动运行需要的 cache、index 和 health。令牌至多使用一次；失败时通过结构化错误说明知识内容是否已经写入。

## 风险边界

- `raw/` 只接收来源摄入，不从 `wiki/` 反向覆盖。
- 问答页和案例卡片默认是草稿，不自动成为正式专业结论。
- demo 模式不写文件，适合 Agent 接入验收。
- 旧 `kb.py --commit` 仍为人工兼容入口；Agent 不得绕过 preview/commit 门控直接调用。
- 旧维护 API 暂时保留迁移兼容，前端不再承载维护表单和 AI 配置。

## 使用说明

工作区命令、统一 JSON envelope、MCP 工具表、Codex 配置和环境变量见 `workspace/docs/cpa-zh-agent.md`。
