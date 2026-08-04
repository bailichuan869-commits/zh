---
title: CPA-ZH 检索能力升级批次
type: source
source_type: maintenance-batch
created: 2026-06-29
updated: 2026-06-29
sources: [local-maintenance-tools]
tags: [search, maintenance, manifest, link-check, registry]
related: [[concepts/kb-maintenance-workflow]]
domain: sources
topic: batches
---

# CPA-ZH 检索能力升级批次

本批次为 CPA-ZH 增加统一的本地检索和来源审计工具，目的是减少后续维护时的盲搜和漏归档。

## 新增资产

| 资产 | 路径 | 作用 |
|---|---|---|
| 官方来源注册表 | `source-registry.yml` | 固定财政部、中注协、证监会、全国人大等优先来源入口 |
| 本地全文检索 | `tools/kb_search.py` | 构建 SQLite 索引并检索 wiki、raw 文件和 manifest 元数据 |
| manifest 审计 | `tools/kb_manifest_audit.py` | 检查 manifest、metadata、source-url 和本地文件一致性 |
| 链接汇总/检查 | `tools/kb_link_check.py` | 汇总官方 URL，联网时可执行状态检查 |
| 维护流程页 | `wiki/concepts/kb-maintenance-workflow.md` | 固化后续更新、复核和检索流程 |

## 初始验证

| 项目 | 结果 |
|---|---|
| manifest 审计 | 2 个 manifest，31 个归档条目，0 个问题 |
| 本地索引 | 1385 条记录 |
| 索引构成 | wiki 803 条；raw manifest 31 条；raw file 551 条 |
| 离线 URL 汇总 | manifest 和来源注册表合计 33 个唯一 URL |

## 使用约定

后续 Python 命令统一使用工作区虚拟环境：

```powershell
.\.venv\Scripts\python.exe tools\kb_search.py index
.\.venv\Scripts\python.exe tools\kb_search.py query "独立性 准则 应用指南"
.\.venv\Scripts\python.exe tools\kb_manifest_audit.py
.\.venv\Scripts\python.exe tools\kb_link_check.py
```

需要联网核验链接时，再显式执行：

```powershell
.\.venv\Scripts\python.exe tools\kb_link_check.py --include-wiki --check
```
