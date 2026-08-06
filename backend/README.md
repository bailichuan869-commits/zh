# CPA-ZH Backend

只读 FastAPI 服务。启动：

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8765
```

也可以直接双击仓库根目录的 `start-kb.bat`，它会同时拉起后端和前端。

接口文档：`http://127.0.0.1:8765/api/docs`。

## 知识答疑

`POST /api/v1/answers` 只读取本地检索索引。它优先使用已复核的知识页和案例卡，并以权威原文补充证据；证据不足时不生成专业结论。

搜索支持 `general-search`、`answer-current`、`case-review` 和 `learning` 四个 profile，并可通过 `as_of`、`status`、`source_type`、`tag` 限制资产范围。答疑响应会返回 `citations`、`retrieval_trace`、`risk_flags` 和 `insufficient_evidence`；profile 配置位于 `knowledge-base/CPA-ZH/retrieval-profiles.json`。

在启动读 API 前设置以下环境变量：

```powershell
$env:OPENAI_API_KEY = "..."
$env:CPA_ZH_ANSWER_MODEL = "gpt-4.1-mini"
```

没有模型密钥时，可启用仅限本机的开发模拟模式。它只返回本地证据驱动的固定答复，不调用外部模型：

```powershell
$env:CPA_ZH_DEMO_MODE = "1"
```

密钥不得写入仓库、前端变量或知识库文件。

## AI 配置页

前端的“AI 配置”页通过维护服务管理 OpenAI Responses API 兼容服务的地址、模型、启用状态和 API 密钥。保存后的密钥只写入当前 Windows 用户的本机配置目录，读接口永不返回密钥；未启用该配置时，答疑继续使用 `OPENAI_API_KEY` 和 `CPA_ZH_ANSWER_MODEL` 环境变量。

配置页要求维护令牌。可选地用 `CPA_ZH_AI_CONFIG_PATH` 指定本机配置文件位置；不要将该文件放入仓库或共享目录。

## 维护服务

维护写入与本服务分离，始终仅监听本机回环地址。设置维护令牌后启动：

```powershell
$env:CPA_ZH_MAINTENANCE_TOKEN = "..."
.\.venv\Scripts\python.exe tools\start_kb_maintenance.py
```

维护端默认监听 `127.0.0.1:8766`，提供问答沉淀和本地来源入库。资料导入使用短期上传会话，自动完成多文件解析、Markdown 抽取和批次命名；会话文件暂存于 `workspace/tmp/`，确认或过期后清理。所有写入均须先预览复核，再确认提交；提交后自动重建缓存、检索索引并执行健康检查。

开发模拟模式下，维护端使用令牌 `demo`，预览和确认只返回模拟结果，不修改知识库、不执行维护命令：

```powershell
$env:CPA_ZH_DEMO_MODE = "1"
$env:CPA_ZH_MAINTENANCE_TOKEN = ""
.\.venv\Scripts\python.exe tools\start_kb_maintenance.py
```
