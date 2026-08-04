# 本地 Skill 评分报告

评分日期：2026-07-22  
评分范围：`%USERPROFILE%\.codex\skills` 下保留用于本报告的 9 个本地 Skill；不含 `.system`、插件目录及已改走外部路由的历史条目。  
评分方式：Darwin Skill 2.0 的 9 维 rubric。第 8 维需要独立子 Agent 做对照测试；当前环境没有可用子 Agent，因此采用典型场景干跑评估，标记为 `dry_run`，不等同于真实效果测试。

## 总分

| 排名 | Skill | 总分 | 结论 |
|---:|---|---:|---|
| 1 | `darwin-skill` | 86.9 | 评分与优化流程最完整，但篇幅较长 |
| 2 | `course-generator` | 86.5 | 结构完整，检查点和输出约束较强 |
| 3 | `guizang-ppt-skill` | 85.6 | 资源和视觉检查充分，流程较重 |
| 4 | `regulatory-penalty-evaluator` | 84.2 | 专业框架完整，适合复杂监管风险任务 |
| 5 | `llm-wiki` | 81.6 | Wiki 结构完整，失败分支仍可加强 |
| 6 | `multi-search-engine` | 81.0 | 使用示例充分，异常恢复和确认点偏少 |
| 7 | `tianchuan-audit-perspective` | 80.8 | 专业方法强，流程控制和反例清单偏少 |
| 8 | `skill-creator` | 79.9 | 内容全面，存在运行时措辞和依赖说明问题 |
| 9 | `find-skills` | 71.0 | 定位清晰，但可执行细节和边界较少 |

## 维度分数

分数顺序：`D1 前置元数据`、`D2 工作流`、`D3 失败模式`、`D4 检查点`、`D5 可执行性`、`D6 资源整合`、`D7 整体结构`、`D8 实测表现`、`D9 反例黑名单`。各维度为 1-10 分，总分按 Darwin 权重归一化为 100 分。

| Skill | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8* | D9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| course-generator | 9 | 9 | 8 | 9 | 9 | 9 | 9 | 8 | 9 |
| darwin-skill | 8 | 10 | 10 | 10 | 8 | 7 | 8 | 8 | 10 |
| find-skills | 8 | 8 | 6 | 4 | 8 | 8 | 7 | 7 | 7 |
| guizang-ppt-skill | 9 | 9 | 8 | 5 | 9 | 10 | 8 | 9 | 9 |
| llm-wiki | 9 | 9 | 7 | 4 | 9 | 9 | 9 | 8 | 8 |
| multi-search-engine | 9 | 8 | 8 | 4 | 9 | 9 | 8 | 8 | 9 |
| regulatory-penalty-evaluator | 9 | 9 | 8 | 6 | 9 | 8 | 9 | 8 | 9 |
| skill-creator | 8 | 9 | 8 | 4 | 9 | 8 | 8 | 8 | 7 |
| tianchuan-audit-perspective | 9 | 9 | 7 | 4 | 9 | 7 | 9 | 8 | 8 |

\* D8 为 `dry_run`，没有执行独立 Agent 的 with-skill/baseline 对照。

## 优先改进项

1. `find-skills`：补充搜索失败、没有结果、安装失败和用户未确认时的明确分支；增加标准输出模板。
2. `tianchuan-audit-perspective`、`llm-wiki`、`multi-search-engine`：把当前原则性说明改成更多 `如果 X 失败 -> Y` 的恢复路径，并加入显式 `CHECKPOINT`。
3. `skill-creator`：将 frontmatter 中的 `extends Claude's capabilities` 改为 runtime-neutral 的 `extends an agent's capabilities`；同时补充 Python/YAML 依赖不可用时的校验 fallback。
4. 全部 Skill：下一轮应为每个目录增加 2-3 个 `test-prompts.json`，再做真实对照测试；当前分数适合作为结构基线，不适合作为最终效果结论。

## 结论

9 个本地 Skill 均具备可发现的 `SKILL.md` 和有效的基本结构。`course-generator`、`darwin-skill`、`regulatory-penalty-evaluator` 和 `guizang-ppt-skill` 已达到较成熟水平；优先修复 `find-skills` 以及若干 Skill 的失败分支和检查点，可以最快提升整体稳定性。

## 2026-07-22 优化结果

本轮实际优化 6 个 Skill，未修改其核心业务能力；主要补充失败恢复、显式检查点、反例清单、输出格式和运行时中立性。优化前后的分数仍采用 `dry_run`，因此只代表结构与流程基线变化。

| Skill | 优化前 | 优化后 | 变化 |
|---|---:|---:|---:|
| `find-skills` | 71.0 | 85.5 | +14.5 |
| `skill-creator` | 79.9 | 87.4 | +7.5 |
| `tianchuan-audit-perspective` | 80.8 | 86.3 | +5.5 |
| `llm-wiki` | 81.6 | 87.1 | +5.5 |
| `multi-search-engine` | 81.0 | 87.8 | +6.8 |

已为这 6 个 Skill 各加入 2 个典型测试 Prompt，位置为各自 Skill 目录下的 `test-prompts.json`。优化前原文件备份位于：

`workspace/skill-backups/2026-07-22-pre-optimize`

本机 `quick_validate.py` 仍因 Python 缺少 `PyYAML` 无法运行；本轮已完成手动 frontmatter、命名、JSON、体积、资源路径和 runtime 红灯检查。下一轮可在补齐 PyYAML 后执行正式 validator，并用独立 Agent 做 with-skill/baseline 对照测试。
