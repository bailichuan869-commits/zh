const fs = require("fs");
const path = require("path");

const mdPath = path.join(process.cwd(), "course_发行类第9号_零基础课程.md");
const templatePath = "C:/Users/zhaozhonghua/.codex/skills/course-generator/assets/html-template.html";
const outPath = path.join(process.cwd(), "course_发行类第9号_零基础课程.html");

const md = fs.readFileSync(mdPath, "utf8");
const template = fs.readFileSync(templatePath, "utf8");

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function inlineFormat(text) {
  let s = escapeHtml(text);
  s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
  s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  return s;
}

function parseSections(full) {
  const lines = full.replace(/\r\n/g, "\n").split("\n");
  const courseTitle = lines[0].replace(/^#\s+/, "").trim();
  const subtitle = "基于《监管规则适用指引——发行类第9号》的零基础自学课程";
  const estimatedHours = (full.match(/\*\*预计学习时长\*\*：([^\n]+)/)?.[1] || "8 小时").replace(" 小时", "");
  const lastUpdated = (full.match(/\*\*最后更新\*\*：([^\n]+)/)?.[1] || "2026-06-23").trim();

  const parts = full.split(/\n## /);
  const chunks = [];
  for (let i = 1; i < parts.length; i++) {
    chunks.push("## " + parts[i]);
  }

  const chapters = [];
  let globalReview = "";
  let glossary = "";
  let progress = "";

  for (const chunk of chunks) {
    if (chunk.startsWith("## 第")) {
      chapters.push(chunk);
    } else if (chunk.startsWith("## 课程总复习")) {
      globalReview = chunk;
    } else if (chunk.startsWith("## 术语表")) {
      glossary = chunk;
    } else if (chunk.startsWith("## 学习进度检查表")) {
      progress = chunk;
    }
  }

  return { courseTitle, subtitle, estimatedHours, lastUpdated, chapters, globalReview, glossary, progress };
}

function getChapterTitle(chunk) {
  const first = chunk.split("\n")[0].trim();
  return first.replace(/^##\s+/, "");
}

function slugChapter(id) {
  return `ch${id}`;
}

function parseBullets(lines, startIndex) {
  const items = [];
  let i = startIndex;
  while (i < lines.length) {
    const line = lines[i];
    if (/^\s*-\s+/.test(line)) {
      items.push(line.replace(/^\s*-\s+/, "").trim());
      i++;
      continue;
    }
    if (/^\s*\d+\.\s+/.test(line)) break;
    if (/^### |^#### |^## /.test(line)) break;
    if (line.trim() === "") { i++; continue; }
    break;
  }
  return { items, next: i };
}

function parseTable(lines, startIndex) {
  const rows = [];
  let i = startIndex;
  while (i < lines.length && /^\|/.test(lines[i].trim())) {
    const line = lines[i].trim();
    if (!/^\|\-/.test(line.replace(/\s/g, ""))) rows.push(line);
    i++;
  }
  if (rows.length < 2) return { html: "", next: i };
  const header = rows[0].split("|").slice(1, -1).map(s => s.trim());
  const body = rows.slice(1).map(r => r.split("|").slice(1, -1).map(s => s.trim()));
  let html = '<table class="comparison-table"><thead><tr>';
  header.forEach(h => html += `<th>${inlineFormat(h)}</th>`);
  html += "</tr></thead><tbody>";
  body.forEach(row => {
    html += "<tr>";
    row.forEach(cell => html += `<td>${inlineFormat(cell)}</td>`);
    html += "</tr>";
  });
  html += "</tbody></table>";
  return { html, next: i };
}

function parseDetails(block) {
  const match = block.match(/<details>\s*<summary>(.*?)<\/summary>\s*([\s\S]*?)<\/details>/);
  if (!match) return "";
  return `<div class="tip"><strong>${inlineFormat(match[1])}</strong><br>${match[2].trim().split("\n").map(l => inlineFormat(l)).join("<br>")}</div>`;
}

function extractSection(chunk, title) {
  const re = new RegExp(`### ${title}\\n([\\s\\S]*?)(?=\\n### |\\n## |$)`);
  return chunk.match(re)?.[1]?.trim() || "";
}

function buildObjectivesHtml(text) {
  const items = text.split("\n").map(l => l.trim()).filter(l => l.startsWith("- [ ]"));
  return `<div class="section"><h4>学习目标</h4><ul>${items.map(i => `<li>${inlineFormat(i.replace(/^- \[ \]\s*/, ""))}</li>`).join("")}</ul></div>`;
}

function buildGenericContentHtml(text) {
  const lines = text.split("\n");
  let html = '<div class="section"><h4>核心内容</h4>';
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }
    if (/^#### /.test(line)) {
      html += `<h4>${inlineFormat(line.replace(/^####\s+/, ""))}</h4>`;
      i++;
      continue;
    }
    if (/^\s*-\s+/.test(line)) {
      const { items, next } = parseBullets(lines, i);
      html += `<ul>${items.map(item => `<li>${inlineFormat(item)}</li>`).join("")}</ul>`;
      i = next;
      continue;
    }
    if (/^\|/.test(line.trim())) {
      const { html: tableHtml, next } = parseTable(lines, i);
      html += tableHtml;
      i = next;
      continue;
    }
    if (/^```/.test(line)) {
      let j = i + 1;
      const buf = [];
      while (j < lines.length && !/^```/.test(lines[j])) { buf.push(lines[j]); j++; }
      html += `<div class="mind-map">${escapeHtml(buf.join("\n"))}</div>`;
      i = j + 1;
      continue;
    }
    if (/^> /.test(line)) {
      const buf = [];
      let j = i;
      while (j < lines.length && /^> /.test(lines[j])) { buf.push(lines[j].replace(/^> /, "")); j++; }
      html += `<div class="tip">${buf.map(l => inlineFormat(l)).join("<br>")}</div>`;
      i = j;
      continue;
    }
    html += `<p>${inlineFormat(line)}</p>`;
    i++;
  }
  html += "</div>";
  return html;
}

function buildMemoryHtml(text) {
  const lines = text.split("\n");
  let html = '<div class="section memory-aids"><h4>记忆辅助</h4>';
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }
    if (/^#### 对比表格/.test(line)) {
      html += `<h4>对比表格</h4>`;
      i++;
      const { html: tableHtml, next } = parseTable(lines, i);
      html += tableHtml;
      i = next;
      continue;
    }
    if (/^#### 比喻地图/.test(line)) {
      html += `<h4>比喻地图</h4>`;
      i++;
      const buf = [];
      while (i < lines.length && !/^#### /.test(lines[i])) { if (lines[i].trim()) buf.push(lines[i]); i++; }
      html += `<div class="analogy-map">${buf.map(l => `<div>${inlineFormat(l.replace(/^>\s?/, ""))}</div>`).join("")}</div>`;
      continue;
    }
    if (/^#### 思维导图概要/.test(line) || /^#### 思维导图/.test(line)) {
      html += `<h4>思维导图概要</h4>`;
      i++;
      while (i < lines.length && lines[i].trim() === "") i++;
      if (/^```/.test(lines[i] || "")) {
        i++;
        const buf = [];
        while (i < lines.length && !/^```/.test(lines[i])) { buf.push(lines[i]); i++; }
        if (i < lines.length) i++;
        html += `<div class="mind-map">${escapeHtml(buf.join("\n"))}</div>`;
      }
      continue;
    }
    if (/^#### 一句话总结/.test(line)) {
      html += `<h4>一句话总结</h4>`;
      i++;
      const { html: tableHtml, next } = parseTable(lines, i);
      if (tableHtml) {
        html += tableHtml;
      } else {
        const { items, next: n2 } = parseBullets(lines, i);
        html += `<div class="one-liner-grid">${items.map(x => `<div class="one-liner-card">${inlineFormat(x)}</div>`).join("")}</div>`;
        i = n2;
        continue;
      }
      i = next;
      continue;
    }
    if (/^#### 易错警示卡/.test(line)) {
      html += `<h4>易错警示卡</h4>`;
      i++;
      const buf = [];
      while (i < lines.length && !/^#### /.test(lines[i])) { if (lines[i].trim()) buf.push(lines[i]); i++; }
      html += `<div class="mistake-card">${buf.map(l => `<div>${inlineFormat(l.replace(/^>\s?/, ""))}</div>`).join("")}</div>`;
      continue;
    }
    i++;
  }
  html += "</div>";
  return html;
}

function buildSummaryHtml(text) {
  const lines = text.split("\n").filter(Boolean);
  return `<div class="summary-box"><h4>本章小结</h4>${lines.map(line => /^\d+\./.test(line.trim()) ? `<div>${inlineFormat(line.trim())}</div>` : `<p>${inlineFormat(line.trim())}</p>`).join("")}</div>`;
}

function parseQuizAnswerMeta(text) {
  const detailMatch = text.match(/<details>\s*<summary>本章答案<\/summary>\s*([\s\S]*?)<\/details>/);
  const answerBlock = detailMatch ? detailMatch[1].trim() : "";
  const questionBlock = detailMatch ? text.replace(detailMatch[0], "").trim() : text.trim();

  const judgmentAnswers = new Map();
  for (const match of answerBlock.matchAll(/(?:^|\n)\s*(\d+)\.\s*(正确|错误)/g)) {
    judgmentAnswers.set(match[1], match[2]);
  }

  const singleChoiceAnswers = new Map();
  const singleChoiceBlock = answerBlock.match(/单选题答案：\s*([\s\S]*?)(?=\n(?:概念辨析参考：|综合题参考：)|$)/);
  if (singleChoiceBlock) {
    for (const match of singleChoiceBlock[1].matchAll(/(?:^|\n)\s*(\d+)\.\s*([A-D])/g)) {
      singleChoiceAnswers.set(match[1], match[2]);
    }
  }

  const referenceBlock = answerBlock.match(/(?:概念辨析参考：|综合题参考：)\s*([\s\S]*?)$/);
  const referenceAnswer = referenceBlock
    ? referenceBlock[1]
        .split("\n")
        .map(line => line.trim())
        .filter(Boolean)
        .map(line => line.replace(/^-+\s*/, ""))
        .join(" ")
    : "";

  return { questionBlock, judgmentAnswers, singleChoiceAnswers, referenceAnswer };
}

function parseQuizBlocks(text, chapterIndex) {
  const { questionBlock, judgmentAnswers, singleChoiceAnswers, referenceAnswer } = parseQuizAnswerMeta(text);
  const lines = questionBlock.split("\n");
  let i = 0;
  let html = '<div class="section quiz-section"><h4>知识检测</h4>';
  let qCounter = 1;
  let currentSection = "";

  function makeId() {
    const id = `q-${chapterIndex}-${qCounter}`;
    qCounter++;
    return id;
  }

  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) { i++; continue; }
    if (/^#### /.test(line)) {
      const heading = line.replace(/^####\s+/, "").trim();
      if (heading.includes("判断题")) currentSection = "judgment";
      else if (heading.includes("单选题")) currentSection = "single";
      else if (heading.includes("概念辨析") || heading.includes("综合题")) currentSection = "text";
      else currentSection = "";
      html += `<h4>${inlineFormat(heading)}</h4>`;
      i++;
      continue;
    }

    if (/^\d+\.\s+\[ \]/.test(line.trim())) {
      const id = makeId();
      const questionNo = (line.trim().match(/^(\d+)\./) || [])[1];
      const q = line.trim().replace(/^\d+\.\s+\[ \]\s*/, "");
      const correctAnswer = judgmentAnswers.get(questionNo) || "正确";
      html += `
<div class="quiz-item" id="${id}" data-type="radio" data-correct="${escapeHtml(correctAnswer)}" data-explain="请结合本章规则判断，并对照章节答案核对原因。">
  <div class="q">${inlineFormat(q)} <span class="type-badge">判断题</span></div>
  <div class="options">
    <label class="option"><input type="radio" name="${id}" value="正确"> 正确</label>
    <label class="option"><input type="radio" name="${id}" value="错误"> 错误</label>
  </div>
  <button class="quiz-check-btn" onclick="checkAnswer('${id}')">检查答案</button>
  <div class="feedback"></div>
</div>`;
      i++;
      continue;
    }

    if (/^\d+\.\s+/.test(line.trim()) && currentSection === "single") {
      const id = makeId();
      const questionNo = (line.trim().match(/^(\d+)\./) || [])[1];
      const q = line.trim().replace(/^\d+\.\s+/, "");
      const opts = [];
      let j = i + 1;
      while (j < lines.length && /^[A-D]\./.test(lines[j].trim())) {
        opts.push(lines[j].trim());
        j++;
      }
      if (opts.length === 0) {
        const explainText = referenceAnswer || "请先独立作答，再对照本章答案或章节内容复盘。";
        html += `<div class="quiz-item" id="${id}" data-type="text" data-explain="${escapeHtml(explainText)}"><div class="q">${inlineFormat(q)} <span class="type-badge">分析题</span></div><button class="quiz-check-btn" onclick="checkAnswer('${id}')">显示参考答案</button><div class="feedback"></div></div>`;
        i++;
        continue;
      }
      const correctAnswer = singleChoiceAnswers.get(questionNo) || "";
      html += `<div class="quiz-item" id="${id}" data-type="radio" data-correct="${escapeHtml(correctAnswer)}" data-explain="请结合章节内容和参考答案判断。"><div class="q">${inlineFormat(q)} <span class="type-badge">单选题</span></div><div class="options">`;
      opts.forEach(opt => {
        const value = opt.charAt(0);
        html += `<label class="option"><input type="radio" name="${id}" value="${value}"> ${inlineFormat(opt)}</label>`;
      });
      html += `</div><button class="quiz-check-btn" onclick="checkAnswer('${id}')">检查答案</button><div class="feedback"></div></div>`;
      i = j;
      continue;
    }

    if (/^\d+\.\s+/.test(line.trim())) {
      const id = makeId();
      const q = line.trim().replace(/^\d+\.\s+/, "");
      const explainText = referenceAnswer || "请先独立作答，再对照本章答案或章节内容复盘。";
      html += `<div class="quiz-item" id="${id}" data-type="text" data-explain="${escapeHtml(explainText)}"><div class="q">${inlineFormat(q)} <span class="type-badge">分析题</span></div><button class="quiz-check-btn" onclick="checkAnswer('${id}')">显示参考答案</button><div class="feedback"></div></div>`;
      i++;
      continue;
    }

    i++;
  }

  html += "</div>";
  return html;
}

function splitChapter(chunk) {
  const title = getChapterTitle(chunk);
  const objectives = extractSection(chunk, "学习目标");
  const core = extractSection(chunk, "核心内容");
  const memory = extractSection(chunk, "记忆辅助");
  const summary = extractSection(chunk, "本章小结");
  const quiz = extractSection(chunk, "知识检测");
  return { title, objectives, core, memory, summary, quiz };
}

function buildChapterHtml(chunk, idx, total) {
  const { title, objectives, core, memory, summary, quiz } = splitChapter(chunk);
  const id = slugChapter(idx);
  const prev = idx > 0 ? slugChapter(idx - 1) : null;
  const next = idx < total - 1 ? slugChapter(idx + 1) : null;
  return `
<div class="chapter ${idx === 0 ? "open" : ""}" id="${id}">
  <div class="chapter-header" onclick="toggleChapter('${id}')">
    <span class="arrow">▶</span>
    <h3>${escapeHtml(title)}</h3>
    <input type="checkbox" class="chapter-checkbox" onchange="updateProgress()" onclick="event.stopPropagation()" title="标记本章完成">
  </div>
  <div class="chapter-body">
    ${objectives ? buildObjectivesHtml(objectives) : ""}
    ${core ? buildGenericContentHtml(core) : ""}
    ${memory ? buildMemoryHtml(memory) : ""}
    ${summary ? buildSummaryHtml(summary) : ""}
    ${quiz ? parseQuizBlocks(quiz, idx) : ""}
    <div class="chapter-nav">
      <button onclick="${prev ? `goToChapter('${prev}')` : ""}" ${prev ? "" : "disabled"}>◀ 上一章</button>
      <span>${escapeHtml(title)}</span>
      <button onclick="${next ? `goToChapter('${next}')` : ""}" ${next ? "" : "disabled"}>下一章 ▶</button>
    </div>
  </div>
</div>`;
}

function buildGlobalReviewHtml(text) {
  return `<section class="global-review" id="globalReview">${buildGenericContentHtml(text.replace(/^##\s+课程总复习/, "").trim()).replace('<div class="section"><h4>核心内容</h4>', '<h2>课程总复习</h2>')}</section>`;
}

function buildGlossaryHtml(text) {
  const lines = text.split("\n");
  const start = lines.findIndex(line => /^\|/.test(line.trim()));
  const { html: tableHtml } = parseTable(lines, start);
  return `<section class="glossary" id="glossary"><h2>术语表</h2>${tableHtml}</section>`;
}

function buildProgressItems(chapters) {
  return chapters.map((ch, idx) => `<li><label><input type="checkbox" onchange="this.checked = this.checked">${escapeHtml(getChapterTitle(ch))}</label></li>`).join("\n");
}

const parsed = parseSections(md);
const sidebarNavItems = parsed.chapters.map((ch, i) => `<a href="#ch${i}" class="toc-chapter">${escapeHtml(getChapterTitle(ch))}</a>`).join("\n")
  + `\n<a href="#globalReview" class="toc-chapter">课程总复习</a>\n<a href="#glossary" class="toc-chapter">术语表</a>\n<a href="#progressSection" class="toc-chapter">学习进度</a>`;

const chaptersHtml = parsed.chapters.map((ch, i) => buildChapterHtml(ch, i, parsed.chapters.length)).join("\n");
const globalReviewHtml = buildGlobalReviewHtml(parsed.globalReview);
const glossaryHtml = buildGlossaryHtml(parsed.glossary);
const progressItemsHtml = buildProgressItems(parsed.chapters);
const mobileLayoutFix = `
.sidebar-toc-header {
  display: none;
}

.top-bar .sidebar-toggle {
  position: relative;
  left: auto;
  top: auto;
  z-index: auto;
  flex: 0 0 auto;
  width: 36px;
  height: 36px;
  margin-right: 8px;
}

.top-bar .sidebar-toggle.shifted {
  left: auto;
}

@media (max-width: 900px) {
  .sidebar-toggle {
    width: 34px;
    height: 34px;
    font-size: 16px;
  }
  .top-bar {
    display: flex;
    position: sticky;
    top: 0;
    padding: 6px 10px;
    min-height: 48px;
    gap: 6px;
    align-items: center;
  }
  .top-bar input[type="search"] {
    display: block;
    flex: 1 1 auto;
    min-width: 0;
    width: auto;
    max-width: none;
    margin: 0;
    padding: 7px 12px;
    font-size: 13px;
  }
  .top-bar button:not(.sidebar-toggle),
  .top-bar select,
  .top-bar .progress-bar-wrap,
  .top-bar .progress-text {
    display: none;
  }
  .sidebar-toc {
    width: min(84vw, 320px);
    padding: 0;
  }
  .sidebar-toc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px 10px;
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    background: var(--sidebar-bg);
    z-index: 2;
  }
  .sidebar-toc-header h3 {
    margin: 0;
    font-size: 15px;
    letter-spacing: 0;
    text-transform: none;
  }
  .sidebar-close {
    width: 32px;
    height: 32px;
    border: 1px solid var(--border);
    border-radius: 50%;
    background: var(--bg-secondary);
    color: var(--text);
    cursor: pointer;
    font-size: 18px;
    line-height: 1;
  }
  .sidebar-toc nav {
    padding: 8px 12px 16px;
  }
}
`;

let output = template
  .replace(/__COURSE_TITLE__/g, parsed.courseTitle)
  .replace(/__COURSE_SUBTITLE__/g, parsed.subtitle)
  .replace(/__ESTIMATED_HOURS__/g, parsed.estimatedHours)
  .replace(/__LAST_UPDATED__/g, parsed.lastUpdated)
  .replace("<!-- __COURSE_CONTENT__ -->", chaptersHtml)
  .replace("<!-- __GLOBAL_REVIEW_CONTENT__ -->", globalReviewHtml)
  .replace("<!-- __GLOSSARY_CONTENT__ -->", glossaryHtml)
  .replace("<!-- __PROGRESS_ITEMS__ -->", progressItemsHtml)
  .replace("<!-- __SIDEBAR_NAV_ITEMS__ -->", sidebarNavItems)
  .replace('placeholder="🔍 搜索课程内容..."', 'placeholder="搜索课程内容..."')
  .replace(/<button class="sidebar-toggle" id="sidebarToggle" onclick="toggleSidebar\(\)" title="显示\/隐藏目录">☰<\/button>\s*/g, '')
  .replace(
    '<aside class="sidebar-toc" id="sidebarToc">',
    `<aside class="sidebar-toc" id="sidebarToc">
  <div class="sidebar-toc-header">
    <h3>课程目录</h3>
    <button class="sidebar-close" onclick="toggleSidebar()" title="收起目录">×</button>
  </div>`
  )
  .replace('<div class="top-bar">', `<div class="top-bar">
  <button class="sidebar-toggle" id="sidebarToggle" onclick="toggleSidebar()" title="显示/隐藏目录">☰</button>`)
  .replace("</style>", `${mobileLayoutFix}\n</style>`);

fs.writeFileSync(outPath, output, "utf8");
console.log(outPath);
