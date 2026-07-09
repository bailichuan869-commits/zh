# Skill 检查说明

日期：2026-06-24

## 一、检查范围

本次检查覆盖当前已安装的以下 10 个非系统 skill：

1. `chen-yiwei-perspective`
2. `chenyiwei-bbs`
3. `course-generator`
4. `darwin-skill`
5. `find-skills`
6. `guizang-ppt-skill`
7. `llm-wiki`
8. `multi-search-engine`
9. `regulatory-penalty-evaluator`
10. `tianchuan-audit-perspective`

## 二、检查目标

本轮检查与修复重点不是改写 skill 的专业能力本身，而是清理以下通用问题：

1. 运行时绑定过强
2. 作者本机绝对路径硬编码
3. 不存在的工具名或伪 API 调用
4. 缺少 fallback 的强依赖说明
5. 不同 skill 之间的边界冲突或职责重叠

## 三、已完成修复

### 1. 运行时中立性修复

已将多处仅适用于特定运行时的描述改为通用表达，例如：

1. `.claude/skills/...` 改为 `<skills-root>/...`
2. “Claude Code skill” 改为更通用的 “skill” 或 “Agent skill”
3. “在 Claude Code 中使用” 改为“在当前运行时中使用”或“使用当前运行时可用能力”

涉及的主要 skill：

1. `find-skills`
2. `guizang-ppt-skill`
3. `darwin-skill`
4. `chen-yiwei-perspective`

### 2. 工具依赖与 fallback 修复

已补齐或放宽以下依赖说明：

1. `find-skills`：`npx skills` 不再被写成唯一入口，增加手工浏览 `skills.sh` 和运行时自带安装流程的 fallback。
2. `llm-wiki`：`qmd search` 改为可选优化能力，补充 `wiki/index.md + 文件检索 + 直接读取页面` 的 fallback。
3. `chen-yiwei-perspective`：去掉对特定网页读取工具名的绑定，改为当前运行时可用的网页阅读或抓取能力。
4. `multi-search-engine`：主说明中已不再把伪工具调用当成前提。

### 3. 路径硬编码修复

已清理多处作者本机路径，例如：

1. `/Users/...`
2. `~/.claude/skills/...`

涉及的主要 skill：

1. `chen-yiwei-perspective`
2. `guizang-ppt-skill`
3. `darwin-skill`

### 4. 参考文档误导性示例修复

已将部分会误导运行时判断的伪代码示例改为更中立的示例形式：

1. `multi-search-engine` 的部分参考文档由 `web_fetch(...)` 改为直接 URL 示例
2. `CHANNELLOG` 中同类示例已同步清理
3. `guizang-ppt-skill` 的参考文档中作者本地参考 deck 路径已改为项目占位路径

### 5. skill 边界与职责修复

已处理部分 skill 间职责重叠问题：

1. `tianchuan-audit-perspective` 补充了与监管处罚/问询类 skill 的协同边界
2. `regulatory-penalty-evaluator` 调整了“底稿编号/底稿要求”的默认措辞，避免无依据发明编号体系
3. `chenyiwei-bbs` 收紧触发边界，避免被误用为所有会计审计问题的默认入口

## 四、当前状态

按本轮检查结果，当前这批 skill 已基本达到可继续使用的状态：

1. 主文档层面的明显运行时绑定问题已大幅清理
2. 主要安装说明、触发说明、参考说明已更适合跨运行时使用
3. 高风险的本机路径写死问题已基本处理
4. 主要误导性依赖说明已补 fallback

## 五、剩余说明

当前扫描仍会看到少量 `.claude/skills`、`Claude Code` 等字样，主要集中在 `darwin-skill` 的以下内容中：

1. runtime-neutrality 审查规则
2. 反例说明
3. 用于扫描红灯模式的 grep 示例

这些内容属于“说明什么是不合格写法”的元文档，不是 skill 自己仍然存在运行时绑定，因此本轮未继续删除。

## 六、结论

本轮工作可以视为：

1. 完成了一次针对当前已安装 skill 的结构性检查
2. 完成了一次面向可移植性和可维护性的修复
3. 将大部分“只能在作者原环境里成立”的描述改成了更稳妥的通用表达

如后续继续扩充 skill，建议把本轮检查标准作为常规验收项：

1. 是否存在本机绝对路径
2. 是否写死某个运行时
3. 是否依赖不存在的工具名
4. 是否给出 fallback
5. 是否与现有 skill 发生职责冲突
