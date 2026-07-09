const fs = require("fs");
const path = require("path");

const workspaceRoot = path.resolve(__dirname, "..");
const kbRoot = path.join(workspaceRoot, "archived", "cpa-competition");
const wikiRoot = path.join(kbRoot, "wiki");
const outputDir = path.join(kbRoot, "ui");
const outputFile = path.join(outputDir, "index.html");

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function readUtf8(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

function walkMarkdownFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const entryPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkMarkdownFiles(entryPath));
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      files.push(entryPath);
    }
  }
  return files.sort();
}

function parseScalar(value) {
  const trimmed = value.trim();
  if (trimmed.startsWith("[") && trimmed.endsWith("]")) {
    const inner = trimmed.slice(1, -1).trim();
    if (!inner) return [];
    return inner
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean)
      .map((item) => item.replace(/^['"]|['"]$/g, ""));
  }
  if (trimmed === "true") return true;
  if (trimmed === "false") return false;
  return trimmed.replace(/^['"]|['"]$/g, "");
}

function parseFrontmatter(raw) {
  if (!raw.startsWith("---\n")) {
    return { metadata: {}, body: raw };
  }

  const end = raw.indexOf("\n---\n", 4);
  if (end === -1) {
    return { metadata: {}, body: raw };
  }

  const fmText = raw.slice(4, end);
  const body = raw.slice(end + 5).trim();
  const metadata = {};

  for (const line of fmText.split(/\r?\n/)) {
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!match) continue;
    const [, key, value] = match;
    metadata[key] = parseScalar(value);
  }

  return { metadata, body };
}

function getFirstHeading(body) {
  const line = body.split(/\r?\n/).find((item) => item.startsWith("# "));
  return line ? line.slice(2).trim() : "";
}

function getSection(relativePath) {
  const normalized = relativePath.replace(/\\/g, "/");
  const parts = normalized.split("/");
  if (parts.length === 1) return "overview";
  return parts[0];
}

function getExcerpt(body) {
  const cleaned = body
    .replace(/^#{1,6}\s+/gm, "")
    .replace(/\[\[([^\]]+)\]\]/g, "$1")
    .replace(/\*\*/g, "")
    .replace(/`/g, "")
    .replace(/\|/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  return cleaned.slice(0, 180);
}

function collectLinks(body) {
  const links = [];
  const regex = /\[\[([^\]]+)\]\]/g;
  let match;
  while ((match = regex.exec(body))) {
    links.push(match[1]);
  }
  return Array.from(new Set(links));
}

function loadDocuments() {
  const files = walkMarkdownFiles(wikiRoot);
  const docs = files.map((filePath) => {
    const raw = readUtf8(filePath);
    const { metadata, body } = parseFrontmatter(raw);
    const relativePath = path.relative(wikiRoot, filePath).replace(/\\/g, "/");
    const id = relativePath.replace(/\.md$/, "");
    const title = metadata.title || getFirstHeading(body) || path.basename(filePath, ".md");

    return {
      id,
      title,
      section: getSection(relativePath),
      type: metadata.type || "",
      conceptType: metadata.concept_type || "",
      sourceType: metadata.source_type || "",
      created: metadata.created || "",
      updated: metadata.updated || "",
      tags: Array.isArray(metadata.tags) ? metadata.tags : [],
      sources: Array.isArray(metadata.sources) ? metadata.sources : [],
      related: Array.isArray(metadata.related) ? metadata.related : [],
      excerpt: getExcerpt(body),
      links: collectLinks(body),
      markdown: body,
      relativePath,
    };
  });

  const docMap = new Map(docs.map((doc) => [doc.id, doc]));
  for (const doc of docs) {
    doc.backlinks = docs
      .filter((candidate) => candidate.id !== doc.id && candidate.links.includes(doc.id))
      .map((candidate) => candidate.id);

    doc.relatedResolved = doc.related
      .map((item) => item.replace(/^\[\[|\]\]$/g, ""))
      .filter((id) => docMap.has(id));
  }

  return docs.sort((a, b) => a.title.localeCompare(b.title, "zh-CN"));
}

function buildHtml(docs) {
  const docJson = JSON.stringify(docs, null, 2);

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>注册会计师竞赛知识库</title>
  <style>
    :root {
      --bg: #f3efe5;
      --panel: rgba(255, 252, 246, 0.88);
      --panel-strong: #fffaf0;
      --ink: #18222f;
      --muted: #5a6775;
      --line: rgba(24, 34, 47, 0.12);
      --accent: #b84c2a;
      --accent-soft: rgba(184, 76, 42, 0.14);
      --accent-2: #1d5c63;
      --shadow: 0 20px 40px rgba(24, 34, 47, 0.12);
      --radius: 24px;
      --radius-sm: 14px;
      --serif: "Noto Serif SC", "Source Han Serif SC", "STSong", Georgia, serif;
      --sans: "Aptos", "Segoe UI", "PingFang SC", "Microsoft YaHei UI", sans-serif;
    }

    * {
      box-sizing: border-box;
    }

    html, body {
      margin: 0;
      min-height: 100%;
      background:
        radial-gradient(circle at top left, rgba(184, 76, 42, 0.18), transparent 28%),
        radial-gradient(circle at top right, rgba(29, 92, 99, 0.16), transparent 26%),
        linear-gradient(180deg, #f8f3e9 0%, #efe7d9 100%);
      color: var(--ink);
      font-family: var(--sans);
    }

    body {
      padding: 24px;
    }

    .shell {
      display: grid;
      grid-template-columns: 320px minmax(0, 1fr);
      gap: 22px;
      min-height: calc(100vh - 48px);
    }

    .sidebar,
    .content {
      background: var(--panel);
      border: 1px solid rgba(255, 255, 255, 0.7);
      backdrop-filter: blur(16px);
      box-shadow: var(--shadow);
      border-radius: var(--radius);
    }

    .sidebar {
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .brand {
      padding: 8px 4px 0;
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent);
      font-weight: 700;
    }

    .brand h1 {
      margin: 10px 0 8px;
      font-family: var(--serif);
      font-size: 30px;
      line-height: 1.1;
      letter-spacing: -0.02em;
    }

    .brand p {
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
      font-size: 14px;
    }

    .search {
      display: grid;
      gap: 10px;
    }

    .search input {
      width: 100%;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.85);
      padding: 13px 14px;
      border-radius: 16px;
      font-size: 14px;
      color: var(--ink);
      outline: none;
    }

    .search input:focus {
      border-color: rgba(184, 76, 42, 0.45);
      box-shadow: 0 0 0 4px rgba(184, 76, 42, 0.12);
    }

    .stats {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }

    .stat {
      padding: 14px;
      border-radius: 18px;
      background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,248,238,0.75));
      border: 1px solid rgba(24, 34, 47, 0.08);
    }

    .stat strong {
      display: block;
      font-size: 24px;
      font-family: var(--serif);
      margin-bottom: 4px;
    }

    .stat span {
      color: var(--muted);
      font-size: 12px;
    }

    .filters {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .chip {
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.7);
      padding: 8px 12px;
      cursor: pointer;
      color: var(--muted);
      font-size: 13px;
      transition: 180ms ease;
    }

    .chip.active,
    .chip:hover {
      background: var(--accent-soft);
      color: var(--accent);
      border-color: rgba(184, 76, 42, 0.18);
    }

    .nav-title {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--muted);
      margin: 2px 0;
    }

    .nav-list {
      display: grid;
      gap: 8px;
      overflow: auto;
      padding-right: 4px;
    }

    .nav-item {
      border: 1px solid transparent;
      border-radius: 18px;
      padding: 12px 14px;
      cursor: pointer;
      transition: 180ms ease;
      background: rgba(255, 255, 255, 0.45);
    }

    .nav-item:hover,
    .nav-item.active {
      border-color: rgba(184, 76, 42, 0.18);
      background: rgba(255, 249, 242, 0.96);
      transform: translateX(2px);
    }

    .nav-item small {
      display: block;
      color: var(--muted);
      margin-top: 4px;
      line-height: 1.5;
    }

    .nav-item .meta {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 4px;
      color: var(--accent-2);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .content {
      display: grid;
      grid-template-rows: auto auto 1fr;
      overflow: hidden;
    }

    .hero {
      padding: 28px 32px 20px;
      border-bottom: 1px solid var(--line);
      background:
        linear-gradient(135deg, rgba(184, 76, 42, 0.08), rgba(29, 92, 99, 0.08)),
        rgba(255, 252, 246, 0.72);
    }

    .hero-top {
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: flex-start;
    }

    .hero h2 {
      margin: 0 0 8px;
      font-family: var(--serif);
      font-size: clamp(30px, 4vw, 44px);
      line-height: 1.05;
      letter-spacing: -0.03em;
    }

    .hero p {
      margin: 0;
      color: var(--muted);
      line-height: 1.7;
      max-width: 760px;
    }

    .meta-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      padding: 0 32px 16px;
      border-bottom: 1px solid var(--line);
      background: rgba(255, 252, 246, 0.66);
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border-radius: 999px;
      padding: 8px 12px;
      background: rgba(24, 34, 47, 0.05);
      color: var(--muted);
      font-size: 13px;
    }

    .reader {
      overflow: auto;
      padding: 28px 32px 40px;
    }

    .article {
      max-width: 940px;
      margin: 0 auto;
      font-size: 16px;
      line-height: 1.85;
    }

    .article h1,
    .article h2,
    .article h3,
    .article h4 {
      font-family: var(--serif);
      line-height: 1.2;
      color: var(--ink);
      letter-spacing: -0.02em;
    }

    .article h1 {
      font-size: 40px;
      margin: 0 0 16px;
    }

    .article h2 {
      font-size: 26px;
      margin: 30px 0 12px;
      padding-top: 6px;
    }

    .article h3 {
      font-size: 20px;
      margin: 24px 0 10px;
    }

    .article p {
      margin: 0 0 14px;
    }

    .article ul,
    .article ol {
      margin: 0 0 16px 22px;
      padding: 0;
    }

    .article li {
      margin-bottom: 8px;
    }

    .article code {
      font-family: "Cascadia Code", "Consolas", monospace;
      background: rgba(24, 34, 47, 0.08);
      border-radius: 8px;
      padding: 2px 6px;
      font-size: 0.92em;
    }

    .article pre {
      overflow: auto;
      background: #1c2835;
      color: #f4f7fb;
      padding: 18px;
      border-radius: 18px;
    }

    .article table {
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0;
      border-radius: 18px;
      overflow: hidden;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.8);
    }

    .article th,
    .article td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
    }

    .article th {
      background: rgba(24, 34, 47, 0.05);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--muted);
    }

    .article blockquote {
      margin: 18px 0;
      padding: 16px 18px;
      border-left: 4px solid var(--accent);
      background: rgba(184, 76, 42, 0.08);
      border-radius: 0 16px 16px 0;
      color: var(--muted);
    }

    .article a {
      color: var(--accent-2);
      text-decoration: none;
      border-bottom: 1px solid rgba(29, 92, 99, 0.24);
    }

    .article a:hover {
      color: var(--accent);
      border-bottom-color: rgba(184, 76, 42, 0.45);
    }

    .support-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin-top: 28px;
    }

    .support-card {
      padding: 18px;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.82);
      border: 1px solid var(--line);
    }

    .support-card h4 {
      margin: 0 0 10px;
      font-size: 16px;
      font-family: var(--sans);
      letter-spacing: 0;
    }

    .link-list {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .doc-link {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 11px;
      border-radius: 999px;
      background: rgba(29, 92, 99, 0.08);
      color: var(--accent-2);
      border: 1px solid rgba(29, 92, 99, 0.12);
      cursor: pointer;
      font-size: 13px;
    }

    .empty {
      color: var(--muted);
      border: 1px dashed var(--line);
      border-radius: 20px;
      padding: 20px;
      text-align: center;
      background: rgba(255,255,255,0.45);
    }

    .footer-note {
      margin-top: 26px;
      color: var(--muted);
      font-size: 13px;
    }

    @media (max-width: 1080px) {
      body {
        padding: 14px;
      }

      .shell {
        grid-template-columns: 1fr;
        min-height: auto;
      }

      .sidebar {
        order: 2;
      }

      .content {
        order: 1;
      }
    }

    @media (max-width: 720px) {
      .hero,
      .meta-bar,
      .reader {
        padding-left: 18px;
        padding-right: 18px;
      }

      .stats,
      .support-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="shell">
    <aside class="sidebar">
      <section class="brand">
        <div class="eyebrow">知识库界面</div>
        <h1>注册会计师竞赛知识库</h1>
        <p>本地静态界面，直接浏览法规、专题页、来源页和交叉链接。继续补料后可重新生成，无需外部依赖。</p>
      </section>

      <section class="search">
        <input id="searchInput" type="search" placeholder="搜索标题、考点、法条、标签..." />
        <div class="stats">
          <div class="stat">
            <strong id="docCount">0</strong>
            <span>总文档数</span>
          </div>
          <div class="stat">
            <strong id="conceptCount">0</strong>
            <span>专题页</span>
          </div>
        </div>
      </section>

      <section>
        <div class="nav-title">模块筛选</div>
        <div class="filters" id="filters"></div>
      </section>

      <section style="min-height: 0; display: flex; flex-direction: column; gap: 10px;">
        <div class="nav-title">文档导航</div>
        <div class="nav-list" id="navList"></div>
      </section>
    </aside>

    <main class="content">
      <section class="hero">
        <div class="hero-top">
          <div>
            <div class="eyebrow" id="heroEyebrow">已加载</div>
            <h2 id="heroTitle">知识库已就绪</h2>
            <p id="heroDescription">左侧可以按模块筛选并搜索，中间打开任何页面后，支持继续沿着交叉链接跳转。</p>
          </div>
        </div>
      </section>

      <section class="meta-bar" id="metaBar"></section>

      <section class="reader">
        <article class="article" id="article"></article>
      </section>
    </main>
  </div>

  <script id="docsData" type="application/json">${docJson}</script>
  <script>
    const docs = JSON.parse(document.getElementById("docsData").textContent);
    const docMap = new Map(docs.map((doc) => [doc.id, doc]));
    const navList = document.getElementById("navList");
    const filtersWrap = document.getElementById("filters");
    const article = document.getElementById("article");
    const metaBar = document.getElementById("metaBar");
    const searchInput = document.getElementById("searchInput");
    const heroEyebrow = document.getElementById("heroEyebrow");
    const heroTitle = document.getElementById("heroTitle");
    const heroDescription = document.getElementById("heroDescription");
    const CODE_FENCE = "\\u0060\\u0060\\u0060";

    const sections = ["all", ...Array.from(new Set(docs.map((doc) => doc.section)))];
    let activeSection = "all";
    let activeSearch = "";
    let activeDocId = location.hash ? decodeURIComponent(location.hash.slice(1)) : "";

    if (!activeDocId || !docMap.has(activeDocId)) {
      activeDocId = docMap.has("overview") ? "overview" : docs[0].id;
    }

    document.getElementById("docCount").textContent = String(docs.length);
    document.getElementById("conceptCount").textContent = String(docs.filter((doc) => doc.section === "concepts").length);

    function normalize(value) {
      return value.toLowerCase();
    }

    function getSectionLabel(section) {
      const labels = {
        all: "全部",
        overview: "总览",
        concepts: "专题",
        sources: "来源"
      };
      return labels[section] || section;
    }

    function getSectionAccent(section) {
      const labels = {
        overview: "总览页",
        concepts: "专题页",
        sources: "来源页"
      };
      return labels[section] || "知识页";
    }

    function getTypeLabel(type) {
      const labels = {
        concept: "专题",
        source: "来源",
        index: "索引"
      };
      return labels[type] || type;
    }

    function getTagLabel(tag) {
      const labels = {
        cpa: "注册会计师",
        competition: "竞赛",
        structured: "结构化",
        framework: "框架",
        reviewed: "已整理",
        law: "法律",
        accounting: "会计",
        supervision: "监督",
        regulation: "法规",
        standards: "准则",
        policy: "政策",
        audit: "审计",
        ethics: "职业道德",
        independence: "独立性",
        skills: "技能",
        company: "公司",
        governance: "治理",
        securities: "证券",
        disclosure: "披露",
        source: "来源",
        practice: "练习",
        questions: "题库",
        update: "动态",
        case: "案例",
        comparison: "对照",
        revenue: "收入",
        evidence: "证据",
        confirmation: "函证",
        "data-analysis": "数据分析",
        "intelligent-tools": "智能工具",
        "study-plan": "备赛计划",
        "p1-core": "核心",
        "p2-important": "重点",
        "p3-extension": "扩展",
        rpa: "机器人流程自动化"
      };
      return labels[tag] || tag;
    }

    function filterDocs() {
      return docs.filter((doc) => {
        const sectionMatch = activeSection === "all" || doc.section === activeSection;
        if (!sectionMatch) return false;
        if (!activeSearch) return true;

        const haystack = normalize([
          doc.title,
          doc.excerpt,
          doc.markdown,
          doc.tags.join(" "),
          doc.id
        ].join(" "));

        return haystack.includes(normalize(activeSearch));
      });
    }

    function renderFilters() {
      filtersWrap.innerHTML = "";
      for (const section of sections) {
        const button = document.createElement("button");
        button.className = "chip" + (activeSection === section ? " active" : "");
        button.textContent = getSectionLabel(section);
        button.type = "button";
        button.addEventListener("click", () => {
          activeSection = section;
          renderFilters();
          renderNav();
        });
        filtersWrap.appendChild(button);
      }
    }

    function renderNav() {
      const items = filterDocs();
      navList.innerHTML = "";

      if (!items.length) {
        navList.innerHTML = '<div class="empty">没有匹配结果，换个关键词试试。</div>';
        return;
      }

      for (const doc of items) {
        const card = document.createElement("button");
        card.type = "button";
        card.className = "nav-item" + (doc.id === activeDocId ? " active" : "");
        card.innerHTML = \`
          <div class="meta">
            <span>\${getSectionLabel(doc.section)}</span>
            \${doc.type ? \`<span>\${getTypeLabel(doc.type)}</span>\` : ""}
          </div>
          <strong>\${escapeHtml(doc.title)}</strong>
          <small>\${escapeHtml(doc.excerpt || "打开查看详情")}</small>
        \`;
        card.addEventListener("click", () => openDoc(doc.id));
        navList.appendChild(card);
      }
    }

    function escapeHtml(value) {
      return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;");
    }

    function renderInline(text) {
      let html = escapeHtml(text);
      html = html.replace(/\\*\\*(.+?)\\*\\*/g, "<strong>$1</strong>");
      html = html.replace(/\u0060([^\u0060]+)\u0060/g, "<code>$1</code>");
      html = html.replace(/\\[\\[([^\\]]+)\\]\\]/g, (_, id) => {
        const normalizedId = id.trim();
        const doc = docMap.get(normalizedId);
        if (!doc) return "<code>" + escapeHtml(normalizedId) + "</code>";
        return '<a href="#' + encodeURIComponent(doc.id) + '" data-doc-id="' + escapeHtml(doc.id) + '">' + escapeHtml(doc.title) + "</a>";
      });
      html = html.replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, (_, label, href) => {
        return '<a href="' + href + '" target="_blank" rel="noreferrer">' + escapeHtml(label) + "</a>";
      });
      return html;
    }

    function splitTableRow(line) {
      return line
        .trim()
        .replace(/^\\|/, "")
        .replace(/\\|$/, "")
        .split("|")
        .map((cell) => cell.trim());
    }

    function isTableSeparator(line) {
      return /^\\|?\\s*:?-{3,}:?\\s*(\\|\\s*:?-{3,}:?\\s*)+\\|?$/.test(line.trim());
    }

    function markdownToHtml(markdown) {
      const lines = markdown.replace(/\\r/g, "").split("\\n");
      const html = [];

      for (let i = 0; i < lines.length; i += 1) {
        const line = lines[i];
        const trimmed = line.trim();

        if (!trimmed) continue;

        if (trimmed.startsWith(CODE_FENCE)) {
          const codeLines = [];
          i += 1;
          while (i < lines.length && !lines[i].trim().startsWith(CODE_FENCE)) {
            codeLines.push(lines[i]);
            i += 1;
          }
          html.push("<pre><code>" + escapeHtml(codeLines.join("\\n")) + "</code></pre>");
          continue;
        }

        const headingMatch = trimmed.match(/^(#{1,6})\\s+(.*)$/);
        if (headingMatch) {
          const level = headingMatch[1].length;
          html.push("<h" + level + ">" + renderInline(headingMatch[2]) + "</h" + level + ">");
          continue;
        }

        if (trimmed === "---") {
          html.push("<hr />");
          continue;
        }

        if (trimmed.startsWith(">")) {
          const quoteLines = [];
          while (i < lines.length && lines[i].trim().startsWith(">")) {
            quoteLines.push(lines[i].trim().replace(/^>\\s?/, ""));
            i += 1;
          }
          i -= 1;
          html.push("<blockquote>" + quoteLines.map(renderInline).join("<br />") + "</blockquote>");
          continue;
        }

        if (trimmed.startsWith("|") && i + 1 < lines.length && isTableSeparator(lines[i + 1])) {
          const headers = splitTableRow(lines[i]);
          const rows = [];
          i += 2;
          while (i < lines.length && lines[i].trim().startsWith("|")) {
            rows.push(splitTableRow(lines[i]));
            i += 1;
          }
          i -= 1;

          html.push("<table><thead><tr>" + headers.map((cell) => "<th>" + renderInline(cell) + "</th>").join("") + "</tr></thead><tbody>" +
            rows.map((row) => "<tr>" + row.map((cell) => "<td>" + renderInline(cell) + "</td>").join("") + "</tr>").join("") +
            "</tbody></table>");
          continue;
        }

        if (/^[-*]\\s+/.test(trimmed)) {
          const items = [];
          while (i < lines.length && /^[-*]\\s+/.test(lines[i].trim())) {
            items.push(lines[i].trim().replace(/^[-*]\\s+/, ""));
            i += 1;
          }
          i -= 1;
          html.push("<ul>" + items.map((item) => "<li>" + renderInline(item) + "</li>").join("") + "</ul>");
          continue;
        }

        if (/^\\d+\\.\\s+/.test(trimmed)) {
          const items = [];
          while (i < lines.length && /^\\d+\\.\\s+/.test(lines[i].trim())) {
            items.push(lines[i].trim().replace(/^\\d+\\.\\s+/, ""));
            i += 1;
          }
          i -= 1;
          html.push("<ol>" + items.map((item) => "<li>" + renderInline(item) + "</li>").join("") + "</ol>");
          continue;
        }

        const paragraphLines = [trimmed];
        while (
          i + 1 < lines.length &&
          lines[i + 1].trim() &&
          !/^(#{1,6})\\s+/.test(lines[i + 1].trim()) &&
          !/^[-*]\\s+/.test(lines[i + 1].trim()) &&
          !/^\\d+\\.\\s+/.test(lines[i + 1].trim()) &&
          !lines[i + 1].trim().startsWith(">") &&
          !(lines[i + 1].trim().startsWith("|") && i + 2 < lines.length && isTableSeparator(lines[i + 2])) &&
          !lines[i + 1].trim().startsWith(CODE_FENCE) &&
          lines[i + 1].trim() !== "---"
        ) {
          paragraphLines.push(lines[i + 1].trim());
          i += 1;
        }

        html.push("<p>" + renderInline(paragraphLines.join(" ")) + "</p>");
      }

      return html.join("");
    }

    function renderMeta(doc) {
      const pills = [];
      pills.push('<span class="pill">模块 · ' + getSectionLabel(doc.section) + "</span>");
      if (doc.updated) pills.push('<span class="pill">更新 · ' + escapeHtml(doc.updated) + "</span>");
      if (doc.type) pills.push('<span class="pill">类型 · ' + escapeHtml(getTypeLabel(doc.type)) + "</span>");
      for (const tag of doc.tags.slice(0, 6)) {
        pills.push('<span class="pill">#' + escapeHtml(getTagLabel(tag)) + "</span>");
      }
      metaBar.innerHTML = pills.join("");
    }

    function renderSupportCards(doc) {
      const related = doc.relatedResolved.map((id) => docMap.get(id)).filter(Boolean);
      const backlinks = doc.backlinks.map((id) => docMap.get(id)).filter(Boolean);

      return \`
        <div class="support-grid">
          <section class="support-card">
            <h4>相关页面</h4>
            \${related.length
              ? '<div class="link-list">' + related.map((item) => '<button type="button" class="doc-link" data-doc-link="' + escapeHtml(item.id) + '">' + escapeHtml(item.title) + "</button>").join("") + "</div>"
              : '<div class="empty">当前页面还没有整理出相关页面。</div>'}
          </section>
          <section class="support-card">
            <h4>反向引用</h4>
            \${backlinks.length
              ? '<div class="link-list">' + backlinks.map((item) => '<button type="button" class="doc-link" data-doc-link="' + escapeHtml(item.id) + '">' + escapeHtml(item.title) + "</button>").join("") + "</div>"
              : '<div class="empty">暂时没有其他页面引用它。</div>'}
          </section>
        </div>
      \`;
    }

    function openDoc(docId) {
      const doc = docMap.get(docId);
      if (!doc) return;

      activeDocId = doc.id;
      location.hash = encodeURIComponent(doc.id);
      renderNav();

      heroEyebrow.textContent = getSectionAccent(doc.section);
      heroTitle.textContent = doc.title;
      heroDescription.textContent = doc.excerpt || "已打开文档。";

      renderMeta(doc);
      article.innerHTML = markdownToHtml(doc.markdown) + renderSupportCards(doc) + '<p class="footer-note">文档路径：' + escapeHtml(doc.relativePath) + "</p>";

      article.querySelectorAll("[data-doc-id], [data-doc-link]").forEach((element) => {
        element.addEventListener("click", (event) => {
          event.preventDefault();
          openDoc(element.getAttribute("data-doc-id") || element.getAttribute("data-doc-link"));
        });
      });
    }

    searchInput.addEventListener("input", () => {
      activeSearch = searchInput.value.trim();
      renderNav();
    });

    window.addEventListener("hashchange", () => {
      const nextId = location.hash ? decodeURIComponent(location.hash.slice(1)) : "";
      if (nextId && docMap.has(nextId)) openDoc(nextId);
    });

    renderFilters();
    renderNav();
    openDoc(activeDocId);
  </script>
</body>
</html>`;
}

function main() {
  ensureDir(outputDir);
  const docs = loadDocuments();
  fs.writeFileSync(outputFile, buildHtml(docs), "utf8");
  console.log("Generated UI:", outputFile);
  console.log("Documents indexed:", docs.length);
}

main();
