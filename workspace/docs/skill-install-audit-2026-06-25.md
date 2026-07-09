# Skill 安装审计报告

**日期**：2026-06-25
**操作**：将 `materials/skill_archives/` 中全部 10 个 skill 压缩包解包、安全审计后安装到用户级目录 `~/.workbuddy/skills/`
**当前归档位置**：上述 skill 压缩包和解包检查材料现已归档至 `archived/skill-assets/`。
**审计方法**：因 `skills-security-check` skill 不在当前环境，采用手动审计——解压全部包，用 Grep 搜索高危模式（`rm -rf`/`os.system`/`subprocess`/`eval`/`child_process`/`curl`/网络外传等），逐个审查 SKILL.md frontmatter 与附带脚本。

---

## 一、审计结论

**全部 10 个 skill 风险等级为 P2（安全），可正常安装。**

未发现恶意代码、任意命令执行、文件删除或敏感数据外传。检测到的网络访问均为声明用途内的正当行为：

| Skill | 网络访问 | 用途 | 风险 |
|-------|----------|------|------|
| chen-yiwei-perspective | curl 抓取 docs.maoyanqing.com | 同步会计准则原文（毛燕庆老师维护） | P2 |
| chenyiwei-bbs | 调用 bbs.auditdog.cn / bbs.esnai.com 公开 API | 检索陈版主论坛答疑（公开匿名，无需 token） | P2 |
| multi-search-engine | 搜索引擎 URL 模板 | 16 引擎检索（无 API key） | P2 |
| 其余 7 个 | 无网络访问 | 知识型/工具型 | P2 |

附带脚本审查：

| Skill | 脚本 | 内容 | 安全性 |
|-------|------|------|--------|
| chen-yiwei-perspective | scripts/sync-standards.sh、fetch_standards.py | curl 抓取准则 HTML 转 Markdown | 安全（正当抓取） |
| llm-wiki | scripts/wiki-init.py | 创建目录结构和初始 Markdown 文件 | 安全（无网络、无系统命令） |
| guizang-ppt-skill | scripts/validate-swiss-deck.mjs | 读取 HTML 验证布局合法性 | 安全（只读本地文件） |
| darwin-skill | scripts/ 为空 | 仅 templates 静态资源 | 安全 |

---

## 二、已安装 Skill 清单

安装位置：`C:\Users\zhaozhonghua\.workbuddy\skills\`

| 序号 | Skill 名称 | 来源压缩包 | 用途 |
|------|------------|------------|------|
| 1 | chen-yiwei-perspective | chen_yiwei_perspective_2f6a917f50.zip | 陈奕蔚会计准则实务视角 |
| 2 | chenyiwei-bbs | chenyiwei_bbs_43ff32e7c1.zip | 陈版主论坛答疑检索 |
| 3 | course-generator | course_generator_75e023cd50.zip | 零基础课程生成 |
| 4 | darwin-skill | darwin_skill_3dfbee3ea1.zip | Skill 质量评估与优化 |
| 5 | find-skills | find_skills_0_1_0_9a49ce6b49.zip | 发现并安装新 skill |
| 6 | guizang-ppt-skill | guizang_ppt_skill_235d3f3e54.zip | 网页 PPT 生成 |
| 7 | llm-wiki | llm_wiki_1_0_1_259c6dd94f.zip | 个人知识库管理 |
| 8 | multi-search-engine | multi_search_engine_2_1_3_b32487e0d2.zip | 多搜索引擎集成 |
| 9 | regulatory-penalty-evaluator | regulatory_penalty_evaluator_55d678cff6.zip | 监管处罚风险评估 |
| 10 | tianchuan-audit-perspective | tianchuan_audit_perspective_36243a14a9.zip | 田川审计底稿视角 |

---

## 三、安装处理说明

- **darwin-skill**：安装时排除了 `.git` 目录（属版本控制元数据，无需安装，可减小体积）
- **chenyiwei-bbs**：清理了 `__MACOSX`（macOS 压缩残留）
- **regulatory-penalty-evaluator**：源文件 `skill.md` 为小写，安装时重命名为标准 `SKILL.md`
- 其余 skill 按原结构安装

---

## 四、验证结果

10 个 skill 的 `SKILL.md` 全部存在性验证通过 `[OK]`。连同原有的 `qcc-company`、`travel-cn`，用户级 skill 目录现有 12 个非系统 skill。

---

## 五、使用说明

各 skill 的适用场景、提问方式与不适合场景，详见 `workspace/docs/installed-skills-guide-2026-06-24.md`（内容仍准确适用）。

> 注：新安装的 skill 需重启 WorkBuddy 会话后才会被加载到可用 skill 列表中，当前会话内仍以系统提示中列出的可用 skill 为准。
