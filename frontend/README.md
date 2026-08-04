# CPA-ZH Frontend

```powershell
npm install
npm run dev
```

开发服务只绑定 `127.0.0.1:5173`，并将 `/api` 请求代理到本机 FastAPI（8765）。构建静态文件：`npm run build`。

完整本地联调需要同时运行读 API（8765）、维护 API（8766）和前端（5173）。没有真实模型密钥或维护令牌时，在两个 Python 服务进程中设置 `CPA_ZH_DEMO_MODE=1`；维护页使用令牌 `demo`：

```powershell
# 终端 1：读 API
$env:CPA_ZH_DEMO_MODE = "1"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8765

# 终端 2：维护 API
$env:CPA_ZH_DEMO_MODE = "1"
.\.venv\Scripts\python.exe tools\start_kb_maintenance.py

# 终端 3：前端
cd frontend
npm run dev
```

在浏览器打开 `http://127.0.0.1:5173`。模拟模式仅用于本机联调，不写入知识库，也不会把凭据写入前端环境文件。

“知识库维护 > 资料导入”支持一次选择 1 至 20 个 Markdown、TXT、CSV、HTML/XML、DOCX 或 PDF 文件。文件选择后会立即抽取 Markdown、按正文生成批次名称并展示复核列表；用户只需调整批次名称并确认批量入库，无需填写本机路径、raw 目录或 Slug。
