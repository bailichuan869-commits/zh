# 知识库界面

## 入口

- 打开 `index.html` 即可浏览本地知识库界面。

## 重新生成

当 `wiki/` 下的 Markdown 内容更新后，在工作区根目录执行：

```powershell
node D:\ai-audit\tools\build_kb_ui.js
```

生成器会重新扫描：

- `D:\ai-audit\archived\cpa-competition\wiki\concepts`
- `D:\ai-audit\archived\cpa-competition\wiki\sources`
- `D:\ai-audit\archived\cpa-competition\wiki\overview.md`
- `D:\ai-audit\archived\cpa-competition\wiki\index.md`

并覆盖输出：

- `D:\ai-audit\archived\cpa-competition\ui\index.html`
