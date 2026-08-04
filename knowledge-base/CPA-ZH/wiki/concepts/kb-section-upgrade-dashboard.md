---
title: CPA-ZH 分板块技术升级仪表盘
type: concept
concept_type: maintenance-dashboard
created: 2026-08-04
updated: 2026-08-04
sources: [kb-schema-check]
tags: [maintenance, schema, section-upgrade, quality-control, cpa]
related: [[concepts/kb-maintenance-workflow]], [[concepts/kb-user-guide]], [[concepts/source-status-dashboard]]
domain: tools
topic: kb-ops
---

# CPA-ZH 分板块技术升级仪表盘

本页由 `tools/kb.py schema --write-report` 生成，用于按五个业务板块检查 wiki 页面元数据、来源结构和后续升级重点。它是治理看板，不替代具体法规、准则和案例页面的专业判断。

## 总览

| 指标 | 数量 |
|---|---:|
| wiki 页面 | 886 |
| 需关注页面 | 0 |
| 警告类型 | 0 |

## 分板块现状

| 板块 | 页面数 | 主要治理目标 | 当前提示 |
|---|---:|---|---|
| 一、行业重要法规与准则 | 800 | 官方来源、原文归档、本地索引三者一致；核心法律、会计准则、审计准则页面保留效力状态和更新时间；将高频准则继续沉淀为实务专题、审计程序和底稿提示 | 无 |
| 二、行业重要政策性文件 | 14 | 政策原文、版本效力、执行检查清单持续联动；按月或遇监管新规时复核官方链接和有效状态；把政策要求拆成事务所治理、项目执行、人员管理和监督检查动作 | 无 |
| 三、行业史与职业道德 | 5 | 职业道德守则、独立性准则和应用指南保持官方原文可追溯；补充独立性情景、威胁类型和防范措施矩阵；将职业道德要求连接到审计项目承接、人员轮换和非鉴证服务判断 | 无 |
| 四、实务技能与案例分析 | 32 | 案例卡片统一保留事实、规则、判断、审计关注点和底稿留痕；按会计主题、审计风险和准则入口建立跨案例索引；把成熟案例沉淀为程序模板、复核清单和问答口径 | 无 |
| 五、AI 编程与自动化 | 16 | 讲义保留原始 Markdown，wiki 层提炼学习线和工具模板；按 Agent、Python、VBA、审计自动化场景维护索引；记录自动化工具的数据边界、控制点、证据留痕和适用风险 | 无 |
| 维护、索引与来源页 | 19 | 保持元数据、来源和索引可追溯 | 无 |
| 未分类页面 | 0 | 保持元数据、来源和索引可追溯 | 无 |

## 升级路线

| 板块 | 下一步维护动作 | 推荐命令或入口 |
|---|---|---|
| 一、行业重要法规与准则 | 继续补齐核心准则专题页的有效版本、原文路径、实务影响、审计程序和底稿提示 | `tools/kb.py search "收入确认 审计程序"`；[[concepts/first-section-topic-matrix]] |
| 二、行业重要政策性文件 | 每次政策变动后更新原文归档、版本效力跟踪和执行检查清单 | [[concepts/policy-version-validity-tracker]]；[[concepts/policy-execution-checklist]] |
| 三、行业史与职业道德 | 将职业道德、独立性准则加工为情景库、威胁类型和防范措施矩阵 | [[concepts/ethics-code]]；[[concepts/independence-standard-1]] |
| 四、实务技能与案例分析 | 新增案例统一加工为案例卡片，并回挂到主题索引和相关准则专题 | [[concepts/case-analysis]]；[[concepts/case-topic-index]] |
| 五、AI 编程与自动化 | 将讲义沉淀为审计自动化工具模板、脚本边界、数据要求和证据留痕清单 | [[concepts/ai-coding-lectures]]；[[concepts/intelligent-tools]] |

## 技术治理命令

```powershell
.\.venv\Scripts\python.exe tools\kb.py schema
.\.venv\Scripts\python.exe tools\kb.py schema --write-report
.\.venv\Scripts\python.exe tools\kb.py sources write-report
.\.venv\Scripts\python.exe tools\kb.py index
.\.venv\Scripts\python.exe tools\kb.py readme
.\.venv\Scripts\python.exe tools\kb.py health
```

## 警告类型说明

| 类型 | 含义 | 处理方式 |
|---|---|---|
| `missing-frontmatter:*` | 页面缺少统一元数据字段 | 补充对应字段，优先补 `title`、`type`、`updated`、`tags`、来源字段 |
| `section-unclassified` | 工具无法判断页面属于哪个板块 | 补充更明确的 tags、concept_type、source_type 或 related 链接 |
| `missing-frontmatter` | 页面没有 YAML frontmatter | 按 WIKI.md 规范补齐页面头部 |

## 需关注页面

| 页面 | 板块 | 类型 | 提示 |
|---|---|---|---|
| 无 |  |  |  |

## 使用边界

- 本检查只覆盖 wiki 页面的结构化元数据和板块归类，不判断法规准则内容是否最新。
- 涉及最新效力、官方链接和原文变动时，仍需结合 [[concepts/source-status-dashboard]] 和官方来源复核。
- 批量新增资料后，应先刷新文本缓存和检索索引，再运行本检查和健康检查。

_生成路径：`wiki/concepts/kb-section-upgrade-dashboard.md`_
