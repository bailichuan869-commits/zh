---
title: CPA-ZH 知识库检索与维护工作流
type: concept
concept_type: maintenance
created: 2026-06-29
updated: 2026-07-09
sources: [kb-retrieval-upgrade-2026-06-29]
tags: [cpa, maintenance, search, archive, verified]
related: [[overview]], [[concepts/regulations-and-standards]], [[concepts/policy-documents]], [[concepts/history-ethics-independence]], [[concepts/source-status-dashboard]], [[concepts/kb-section-upgrade-dashboard]]
domain: tools
topic: kb-ops
---

# CPA-ZH 知识库检索与维护工作流

本页规定 CPA-ZH 后续检索、下载、归档和更新的固定流程。目标是减少盲搜，优先利用本地归档和官方来源注册表，再对网络来源做补漏核验。

## 工具入口

| 工具 | 作用 | 推荐命令 |
|---|---|---|
| 官方来源注册表 | 固定财政部、中注协、证监会、全国人大等可信入口 | `knowledge-base/CPA-ZH/source-registry.yml` |
| 本地全文检索 | 检索 wiki 页、manifest 元数据和 raw 正文；优先复用文本缓存 | `.\.venv\Scripts\python.exe tools\kb_search.py query "独立性 准则"` |
| raw 文本缓存 | 抽取 PDF/DOCX/HTML/文本文件正文，缓存到 `cache/text/` | `.\.venv\Scripts\python.exe tools\kb_text_cache.py build` |
| 本地索引重建 | 新增或更新资料后重建 SQLite 检索库，自动读取新鲜文本缓存 | `.\.venv\Scripts\python.exe tools\kb_search.py index` |
| manifest 审计 | 检查 raw 目录、manifest、metadata、source-url 是否一致 | `.\.venv\Scripts\python.exe tools\kb_manifest_audit.py` |
| 链接汇总/检查 | 离线汇总官方 URL；联网时可检查状态码 | `.\.venv\Scripts\python.exe tools\kb_link_check.py --include-wiki` |
| 一键体检 | 同时检查 manifest、wiki 内链、案例卡片回挂、文本缓存、搜索索引状态和 README 统计 | `.\.venv\Scripts\python.exe tools\kb_health_check.py` |
| 来源状态仪表盘 | 追踪 manifest 条目的官方链接、文本抽取、OCR 和后续维护动作 | `.\.venv\Scripts\python.exe tools\kb_source_status.py write-report` |
| 分板块技术升级仪表盘 | 按五大板块检查 wiki 元数据、来源字段、归类情况和后续升级重点 | `.\.venv\Scripts\python.exe tools\kb.py schema --write-report` |
| 本地问答日志回写 | 将有价值的问答保存为 `wiki/questions/` 页面，后续可升级为案例、专题或清单 | `.\.venv\Scripts\python.exe tools\kb.py qa-capture --question "..." --answer "..."` |
| README 统计刷新 | 自动更新 README 中的 wiki 页数、raw 文件数、manifest 数、索引记录数和案例卡片数 | `.\.venv\Scripts\python.exe tools\kb_update_readme_stats.py` |
| 完整交付验收 | 检查导航树新鲜度、API 契约、知识资产健康度、前端测试和生产构建 | `.\.venv\Scripts\python.exe tools\kb.py verify` |

## 标准维护步骤

1. 先查本地：用 `kb_search.py query` 搜索法规名称、文号、准则号、关键词。
2. 再查注册表：确认应优先访问哪个官方机构、栏目和专题页。
3. 下载或归档：每个来源都要保留 `official.*`、`metadata.json`、`source-url.txt`，批量目录要有 `manifest.json`。
4. 回写 wiki：把官方链接、本地归档路径、效力状态和版本提示写入相关概念页或来源页。
5. 跑审计：执行 `kb_manifest_audit.py` 和 wiki 内链检查，避免“文件已下载但清单未登记”。
6. 刷新文本缓存：执行 `kb_text_cache.py build`，让 PDF/DOCX/HTML 等 raw 正文形成可复用缓存。
7. 重建索引：执行 `kb_search.py index`，让新资料立即可检索。
8. 刷新 README：执行 `kb_update_readme_stats.py`，保持首页统计与真实状态一致。
9. 一键体检：执行 `kb_health_check.py`，确认 manifest、内链、文本缓存、索引和案例卡片回挂状态。
10. 更新来源状态仪表盘：执行 `kb_source_status.py write-report`，确认是否存在待 OCR、待补链接或待缓存条目。
11. 更新分板块技术升级仪表盘：执行 `tools/kb.py schema --write-report`，确认五大板块的元数据和来源结构是否需要补齐。
12. 回写问答：对有复用价值的本地问答，使用 `tools\kb.py qa-capture` 保存到 `wiki/questions/`，并保持 `status: draft` 直到人工复核。
13. 记录日志：更新 `wiki/log.md`，说明新增来源、维护范围和验证结果。

## 发布与周期维护

- 每次前后端发布前执行 `tools\kb.py verify`；该命令不会写入知识资产，但会运行前端生产构建并重建被忽略的 `frontend/dist/`。
- 法律法规按季度复核，政策文件按月复核；职业道德和独立性资料在中注协通知发布时触发复核。正式修订将旧版标记为 `superseded`，征求意见稿保持 `draft`。
- 每周执行 `tools\kb.py links --include-wiki`、`tools\kb.py sources write-report` 和 `tools\kb.py schema --write-report`，再人工处理来源状态仪表盘和板块升级仪表盘中的待办项。
- 有复用价值的问答和案例先以草稿入库，人工复核来源、结论确定性和关联页面后才可提升为正式知识页。

## 版本效力规则

| 场景 | 处理方式 |
|---|---|
| 出现正式修订通知 | 新建或更新原文归档，旧版标记为 `superseded` |
| 出现应用指南或解释 | 归档为配套解释来源，并回挂到准则页 |
| 只有征求意见稿 | 标记为 `draft` 或历史参考，不作为正式依据 |
| 官方链接失效 | 保留本地归档，记录失效日期，并重新查找官方替代链接 |
| 同一文件多入口 | 保留发文机关入口为主，转载入口作为辅助来源 |

## 检索建议

- 中文检索优先用多个关键词加空格，例如 `独立性 准则 应用指南`、`财会 2024 29`。
- 查法规有效版本时同时搜“法律名称 + 修订日期/文号/施行日期”。
- 查政策执行要求时同时搜“文件名 + 检查/监督/责任/整改”。
- 对 PDF 正文命中不稳定时，先运行 `kb_text_cache.py build`，再搜 manifest 标题、文号和本地归档路径；关键判断仍应打开原文核对。

## 后续升级方向

- 为每个板块建立定期更新任务：法律法规按季度，政策文件按月，职业道德和独立性准则按中注协通知触发。
- 对监管处罚和案例库增加“事实、规则、审计应对、处罚后果”结构化字段。
- 将 [[concepts/kb-section-upgrade-dashboard]] 作为板块治理入口，优先处理其中的 `missing-frontmatter` 和 `section-unclassified` 提示。
