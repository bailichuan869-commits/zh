# CPA-ZH Agent 工具

CPA-ZH 采用 Agent-first 工作方式：`raw/` 保存事实来源，`wiki/` 保存结构化知识，`cache/` 和 `search/` 是可重建产物。浏览器只负责搜索、阅读和原文追溯；资料摄入、问答沉淀、案例草稿和页面复核统一经过共享 Python 服务。页面复核默认支持人工 preview/commit，也支持用户明确授权的批量 Agent 复核；两者的状态分别记录为 `user-approved` 和 `agent-reviewed`。

## 入口

安装依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

JSON CLI：

```powershell
.\.venv\Scripts\python.exe tools\cpa_zh_agent.py search --query "收入确认" --limit 5
.\.venv\Scripts\python.exe tools\cpa_zh_agent.py read-page "wiki/concepts/accounting-standards/cas-14.md"
.\.venv\Scripts\python.exe tools\cpa_zh_agent.py health
```

本机 stdio MCP：

```powershell
.\.venv\Scripts\python.exe tools\cpa_zh_mcp.py
```

MCP 通过标准输入输出通信，不监听端口，也不需要常驻服务。

## 两阶段写入

所有知识资产写入都必须分开调用：

1. 调用 `ingest-preview`、`qa-preview`、`case-preview` 或 `review-preview`。
2. 向用户展示返回的完整 `data`，包括目标路径、变更清单、完整 Markdown、来源和风险提示。
3. 用户明确确认后，用原 `preview_token` 调用 `commit --confirmed`。
4. 服务重新校验令牌有效期、知识库根目录、输入哈希和目标状态，再执行写入及 cache/index/health 维护。

批量 Agent 复核使用独立入口。默认只生成完整检查报告和短期预览，不写入；明确授权 Agent 直接复核时使用 `--commit`。该模式会检查完整正文、raw 门面、来源 URL、原文哈希、原文链接和必要章节，并将通过项标记为 `agent-reviewed`，不会伪造 `user-approved`：

```powershell
.\.venv\Scripts\python.exe tools\cpa_zh_agent.py agent-review --scope golden
.\.venv\Scripts\python.exe tools\cpa_zh_agent.py agent-review --scope golden --commit
```

示例：

```powershell
$preview = .\.venv\Scripts\python.exe tools\cpa_zh_agent.py qa-preview `
  --question "售后回购安排能否确认收入？" `
  --answer "需要结合控制权转移、回购价格和客户重大经济动因判断。" `
  --slug "revenue-repurchase-review"

# 人工查看 $preview 中的 data 和 preview_token，并明确确认后再执行：
.\.venv\Scripts\python.exe tools\cpa_zh_agent.py commit "<preview_token>" --confirmed
```

令牌默认 10 分钟有效且只能使用一次。提交失败后令牌也会被消耗，应先检查结构化错误中的 `written`，再重新生成预览；`written=true` 表示知识内容已写入，但后续缓存、索引或健康检查失败，需要先修复维护状态。

设置 `CPA_ZH_DEMO_MODE=1` 时，commit 只返回模拟结果，不写知识库。

## JSON 契约

CLI 和 MCP 返回同一 envelope：

```json
{
  "ok": true,
  "operation": "search",
  "data": {},
  "preview_token": "",
  "expires_at": null,
  "warnings": [],
  "error_code": "",
  "message": ""
}
```

参数错误、路径越界、内容冲突、令牌过期和底层维护失败都通过 `ok=false` 与稳定 `error_code` 返回。`diagnostics` 仅用于人工排错，Agent 不应解析其中的命令行文本来判断协议状态。

## MCP 工具

| 工具 | 用途 |
|---|---|
| `cpa_search` | 按关键词、类型、领域和数量检索 |
| `cpa_read_page` | 读取 wiki frontmatter、正文、链接和哈希 |
| `cpa_read_raw` | 读取 raw 文本或二进制文件的 Markdown 门面 |
| `cpa_health` | 运行知识库健康检查 |
| `cpa_pending_reviews` | 列出满足准入条件的待复核页面 |
| `cpa_review_detail` | 读取待复核页面完整正文 |
| `cpa_agent_review` | 执行黄金内容或全部待复核内容的 Agent 检查；`commit=true` 时提交通过项 |
| `cpa_ingest_preview` | 预览 raw 资料摄入 |
| `cpa_qa_preview` | 预览问答草稿 |
| `cpa_case_preview` | 预览案例卡片草稿 |
| `cpa_review_preview` | 预览复核状态变更 |
| `cpa_commit` | 在明确确认后提交原预览令牌 |

## Codex 本机配置

以下配置遵循当前 Codex `config.toml` 的 stdio MCP 结构。把它加入用户配置后，重新启动 Codex 使工具注册生效：

```toml
[mcp_servers.cpa_zh]
command = 'D:\ai-audit\.venv\Scripts\python.exe'
args = ['D:\ai-audit\tools\cpa_zh_mcp.py']
startup_timeout_sec = 120

[mcp_servers.cpa_zh.env]
CPA_ZH_ROOT = 'D:\ai-audit\knowledge-base\CPA-ZH'
CPA_ZH_AGENT_PREVIEW_ROOT = 'D:\ai-audit\workspace\tmp\cpa-zh-agent-previews'
CPA_ZH_DEMO_MODE = '0'
```

先用 `CPA_ZH_DEMO_MODE='1'` 完成平行验证；确认预览、人工批准和提交行为均符合预期后，再切换为 `'0'`。

## 环境变量

| 变量 | 默认值 | 用途 |
|---|---|---|
| `CPA_ZH_ROOT` | `knowledge-base/CPA-ZH` | 知识库根目录 |
| `CPA_ZH_AGENT_PREVIEW_ROOT` | `workspace/tmp/cpa-zh-agent-previews` | 短期预览记录目录 |
| `CPA_ZH_DEMO_MODE` | `0` | `1` 时禁止真实写入 |

## 兼容边界

- `backend/` 仍是只读 API。
- 旧维护 API 和 `/answers` 暂时保留用于迁移兼容，但不再出现在前端导航。
- 旧 `kb.py` 写命令仍可用；Agent 场景必须通过共享服务的 preview/commit 门控，不应直接调用 `--commit`。
