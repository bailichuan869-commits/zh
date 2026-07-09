---
title: CPA-ZH 使用手册
type: concept
concept_type: user-guide
created: 2026-07-09
updated: 2026-07-09
sources: [kb-retrieval-upgrade-2026-06-29]
tags: [cpa, user-guide, workflow, search, maintenance]
related: [[overview]], [[concepts/kb-maintenance-workflow]], [[concepts/source-status-dashboard]], [[concepts/case-analysis]], [[concepts/case-topic-index]]
---

# CPA-ZH 使用手册

这页是 CPA-ZH 的新手入口。日常使用时先记住一句话：

> `raw/` 放原文，`wiki/` 放加工后的知识，`tools/` 用来检索和维护。

## 先从哪里开始

| 你要做什么 | 先看哪里 |
|---|---|
| 看知识库整体有什么 | [[index]] |
| 查法规、准则、政策和案例 | 本页“怎么检索” |
| 看四大板块入口 | [[index]] 的“一级板块” |
| 看案例 | [[concepts/case-analysis]] 和 [[concepts/case-topic-index]] |
| 新增资料或更新资料 | 本页“新增资料怎么放”和 [[concepts/kb-maintenance-workflow]] |
| 检查知识库有没有坏 | 本页“维护命令” |
| 查看哪些来源待 OCR 或补链接 | [[concepts/source-status-dashboard]] |

## 三层结构

| 层级 | 位置 | 用法 |
|---|---|---|
| 原文层 | `raw/` | 保存法规原文、政策原文、准则附件、案例原始文件；原则上不改写 |
| 知识层 | `wiki/` | 放整理后的专题页、来源页、案例卡片和索引页；日常主要阅读这里 |
| 工具层 | `tools/`, `search/`, `cache/` | 用于检索、抽取文本、重建索引、健康检查和统计刷新 |

不要把判断结论直接写进 `raw/`。`raw/` 是证据箱，`wiki/` 才是工作台。

## 四大板块入口

| 板块 | 入口 | 适合解决的问题 |
|---|---|---|
| 行业重要法规与准则 | [[concepts/regulations-and-standards]] | 查法律、会计准则、审计准则、准则专题和实务判断框架 |
| 行业重要政策性文件 | [[concepts/policy-documents]] | 查财会监督、审计秩序、注册、执业许可、诚信和监督检查政策 |
| 行业史与职业道德 | [[concepts/history-ethics-independence]] | 查行业史、职业道德守则、独立性准则和应用指南 |
| 实务技能与案例分析 | [[concepts/practice-skills-cases]] | 查审计流程、智能化工具、综合能力和实务案例 |

## 怎么检索

在工作区根目录 `D:\ai-audit` 运行：

```powershell
.\.venv\Scripts\python.exe tools\kb_search.py query "关键词"
```

常用检索例子：

```powershell
.\.venv\Scripts\python.exe tools\kb_search.py query "收入确认"
.\.venv\Scripts\python.exe tools\kb_search.py query "独立性 准则 应用指南"
.\.venv\Scripts\python.exe tools\kb_search.py query "政府补助 免费使用设备"
.\.venv\Scripts\python.exe tools\kb_search.py query "长期股权投资 内部重组"
.\.venv\Scripts\python.exe tools\kb_search.py query "中办发 2023 4号 财会监督"
```

检索技巧：

1. 中文检索优先用多个短词，用空格隔开。
2. 查法规政策时同时搜“名称 + 文号 + 关键词”。
3. 查案例时同时搜“准则主题 + 业务事实”，例如 `收入确认 售后回购`。
4. 查不到时先看 [[index]]，再从板块入口进入。
5. 关键结论不要只看搜索摘要，应打开对应 `wiki/` 页面和 `raw/` 原文核对。

## 怎么提问更容易用上知识库

可以直接这样问：

| 场景 | 推荐问法 |
|---|---|
| 查规则 | “用 CPA-ZH 查一下收入确认售后回购怎么判断。” |
| 查案例 | “在知识库里找政府补助相关案例，并总结审计关注点。” |
| 做会计判断 | “结合 CPA-ZH，分析这个长期股权投资重组是否确认投资收益。” |
| 做底稿 | “根据知识库，给我列一份收入确认控制权转移底稿清单。” |
| 更新资料 | “把这批新案例放进 CPA-ZH，并加工成案例卡片。” |

如果是新问题，最好同时给出：

1. 业务事实；
2. 争议点；
3. 你希望输出的形式，例如“结论 + 依据 + 审计程序 + 底稿留痕”。

## 新增资料怎么放

| 资料类型 | 原文放置位置 | 加工后位置 |
|---|---|---|
| 法律法规 | `raw/laws/` | `wiki/concepts/` 或条款页 |
| 会计准则、审计准则、解释、应用指南 | `raw/standards/` | `wiki/concepts/accounting-standards/` 或 `wiki/concepts/audit-standards/` |
| 政策文件 | `raw/policies/` | `wiki/concepts/policy-*.md` |
| 职业道德、独立性准则 | `raw/ethics/` | `wiki/concepts/ethics-*.md` 或 `wiki/concepts/independence-*.md` |
| 实务案例 | `raw/cases/批次名/` | `wiki/sources/批次说明.md` 和 `wiki/cases/案例卡片.md` |

新增一批资料时，建议同时做四件事：

1. 原始文件放入 `raw/` 对应目录；
2. 建立或更新 `manifest.json`；
3. 在 `wiki/sources/` 写来源批次说明；
4. 在 `wiki/concepts/` 或 `wiki/cases/` 生成可复用页面。

## 案例怎么用

案例优先从两个入口进入：

| 入口 | 用途 |
|---|---|
| [[concepts/case-analysis]] | 看案例库整体结构、已导入批次和案例卡片清单 |
| [[concepts/case-topic-index]] | 按收入确认、政府补助、长期股权投资、税会差异等主题找案例 |

每张案例卡片通常按这个结构阅读：

1. 一句话结论；
2. 事实背景；
3. 争议问题；
4. 准则入口；
5. 判断过程；
6. 会计处理建议；
7. 审计关注点；
8. 底稿留痕建议；
9. 易错点或可复用经验。

## 维护命令

新增或修改资料后，按这个顺序运行：

```powershell
.\.venv\Scripts\python.exe tools\kb_text_cache.py build
.\.venv\Scripts\python.exe tools\kb_search.py index
.\.venv\Scripts\python.exe tools\kb_update_readme_stats.py
.\.venv\Scripts\python.exe tools\kb_health_check.py
```

各命令作用：

| 命令 | 作用 |
|---|---|
| `kb_text_cache.py build` | 抽取 raw 文件正文，形成可复用文本缓存 |
| `kb_search.py index` | 重建本地搜索索引 |
| `kb_update_readme_stats.py` | 刷新 README 的统计数字 |
| `kb_health_check.py` | 检查 manifest、内链、案例回挂、搜索索引和缓存状态 |
| `kb_source_status.py write-report` | 生成来源状态仪表盘，追踪 OCR、官方链接和文本缓存待办 |

健康检查结果里最重要的是：

```text
Issues: none
Warnings: none
```

如果出现 warning，优先按提示重建缓存或索引；如果出现 issue，先不要继续扩展，先修复断链、manifest 或案例回挂问题。

## 常见任务速查

| 任务 | 推荐路径 |
|---|---|
| 查一个准则 | `kb_search.py query "准则名称 准则号 关键词"`，再打开对应 `wiki/concepts/accounting-standards/` 页面 |
| 查一个政策是否已归档 | 搜政策名称或文号，再看 `raw/policies/` 和 `wiki/concepts/policy-*.md` |
| 判断一个实务问题 | 先搜关键词，再读准则页、专题页和案例页，最后形成判断备忘录 |
| 导入一批案例 | 原文进 `raw/cases/批次/`，来源页进 `wiki/sources/`，卡片进 `wiki/cases/` |
| 更新法规政策 | 先核验官方来源，再归档新版本，旧版本标记效力状态，最后重建索引和体检 |
| 给别人说明知识库 | 先发本页，再发 [[index]] 和 [[concepts/kb-maintenance-workflow]] |

## 使用边界

CPA-ZH 可以帮助你快速定位规则、复用案例判断、形成审计程序和底稿清单，但不能替代最终职业判断。涉及最新法规、政策、准则或重大项目结论时，应同时核对官方原文、项目事实和事务所内部复核意见。
