# CPA-ZH Frontend

```powershell
npm install
npm run dev
```

开发服务只绑定 `127.0.0.1:5173`，并将 `/api` 请求代理到本机只读 FastAPI（8765）。构建静态文件：`npm run build`。

如果只想一键启动本地联调，直接双击仓库根目录的 `start-kb.bat` 即可，它会同时拉起后端和前端。

前端保持只读知识浏览器边界，同时提供首页、全文搜索、知识答疑、wiki 正文、raw 原文和健康状态。答疑页面只读取已构建索引，并展示检索 profile、版本、生效区间和引用锚点；AI 配置、资料入库和页面复核仍由 Agent CLI 或 stdio MCP 完成。

手动本地联调也只需要读 API（8765）和前端（5173）：

```powershell
# 终端 1：只读 API
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8765

# 终端 2：前端
cd frontend
npm run dev
```

在浏览器打开 `http://127.0.0.1:5173`。资料摄入、问答沉淀、案例草稿和页面复核由 Agent CLI 或 stdio MCP 完成，见 `workspace/docs/cpa-zh-agent.md`。旧维护 API 源码暂时保留用于迁移兼容，但前端不再依赖它。
