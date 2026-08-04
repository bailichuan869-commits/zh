---
project: CPA-ZH
domain: professional-knowledge
created: 2026-06-26
---

# CPA-ZH 知识库配置

## 项目信息

- **名称**：CPA-ZH
- **领域**：中国注册会计师行业法规、准则、政策、职业道德与审计实务
- **说明**：围绕中国注册会计师行业建立的可持续知识库，用于沉淀法规准则、政策文件、职业道德、独立性要求、审计实务技能、智能化工具应用、案例分析与 AI 编程自动化讲义。
- **创建时间**：2026-06-26
- **维护人**：zhaozhonghua

## 实体类型

```yaml
entities:
  types:
    - organization
    - regulation
    - standard
    - policy
    - event
  custom_types:
    - regulator
    - professional-body
    - accounting-firm
  required_attributes:
    organization: [role, scope]
    regulation: [issuer, effective_date, legal_level]
    standard: [issuer, topic, effective_date]
    policy: [issuer, document_no, issued_date]
    event: [date, significance]
```

## 概念分类

```yaml
concepts:
  categories:
    - framework
    - principle
    - method
    - requirement
    - competency
    - learning-section
    - lecture-track
    - tool-template-library
    - scenario-matrix
    - control-checklist
    - implementation-roadmap
    - tool-registry
    - automation-tool
  domain_concepts:
    - accounting-standards
    - audit-standards
    - professional-ethics
    - independence
    - audit-practice
    - policy-supervision
    - intelligent-tools
    - ai-coding
    - automation
```

## 工作流配置

```yaml
workflow:
  default_mode: mixed
  interactive_keywords:
    - 法规原文
    - 准则原文
    - 最新
    - 修订
    - 处罚案例
    - 重大
  batch_threshold: 5
  auto_save_queries: true
  ask_before_save: false
  confirm_new_pages: false
```

## 巡检规则

```yaml
lint:
  check_frequency: weekly
  rules:
    - check_missing_pages
    - check_incomplete_metadata
    - check_section_schema
    - check_data_gaps
    - check_stale_claims
    - check_orphans
  severity:
    stale_claim: critical
    missing_page: warning
    incomplete_metadata: warning
    data_gap: suggestion
    orphan_page: suggestion
```

## 输出偏好

```yaml
output:
  default_format: markdown
  enable_marp: true
  enable_charts: false
  include_citations: true
```

## 标签体系

```yaml
tags:
  priority:
    - p1-core
    - p2-important
    - p3-extension
  status:
    - draft
    - structured
    - reviewed
    - verified
  domain:
    - cpa
    - law
    - accounting
    - audit
    - standards
    - policy
    - ethics
    - independence
    - practice
    - tools
```

## 命名规则

```yaml
naming:
  source_files: "{date}-{slug}.{ext}"
  entity_pages: "entities/{slug}.md"
  concept_pages: "concepts/{slug}.md"
  question_pages: "questions/{slug}.md"
  source_summaries: "sources/{date}-{slug}.md"
  id_format: "{type}-{slug}"
  slug_rules:
    lowercase: true
    replace_spaces: "-"
    remove_special_chars: true
```

## 来源目录

```yaml
sources:
  directories:
    - laws/
    - standards/
    - policies/
    - ethics/
    - practice/
    - cases/
    - tools/
    - lectures/
    - outlines/
    - assets/
  default_types:
    laws/: law
    standards/: standard
    policies/: policy
    ethics/: ethics
    practice/: practice-note
    cases/: case
    tools/: tool-note
    lectures/: lecture
    outlines/: outline
```

## 质量要求

```yaml
quality:
  required_metadata:
    concept: [title, type, concept_type, created, updated]
    source: [title, type, source_type, created, raw_path]
    entity: [title, type, entity_type, created, updated]
    case: [title, type, case_type, created, updated, sources, raw_path]
    question: [title, type, question_type, created, updated, sources, status]
  claims:
    require_source: true
    require_confidence_level: false
  dates:
    use_absolute_dates: true
    verify_latest_before_answering: true
```

## 自定义说明

```text
- 本知识库优先服务注册会计师行业知识沉淀、审计实务判断与学习复盘。
- 法规、准则、政策类页面必须区分“原文依据”“核心要求”“实务影响”“常见问题”和“待核验更新点”。
- 对可能随时间变化的法律法规、政策文件、考试办法、监管要求，回答或更新前应核验最新有效版本。
- 案例分析应尽量采用“事实背景 -> 适用规则 -> 审计应对 -> 风险提示 -> 可复用经验”的结构。
- 问答回写应保留原问题、原回答、关联页面、复核状态和后续动作，不应把未经复核的回答直接升级为正式口径。
- 涉及陈老师、陈版主、陈奕蔚、论坛真实答疑或陈版主视角的问题，不在本知识库保存原文、摘录、题号、派生案例或汇总索引；应调用正式安装的 `chen-yiwei-perspective` 或 `chenyiwei-bbs` skills 处理。
- 智能化工具页面应同时记录适用场景、数据输入要求、控制点、局限性和审计证据留痕要求。
- 讲义类资料应保留原始 Markdown，并在 wiki 层提炼学习线、适用场景、可复用工具模板和审计实务落地点。
- 原文件必须抽取为 Markdown 后再加工：放入 `raw/` 的原始资料（html/htm/xml/pdf/docx/txt/csv 等）都须先经 `tools/convert_raw_to_md.py`（或 `tools/kb.py archive-doc` / `pdf-md`）抽取为 `raw/*.md` 统一 Markdown 门面，再基于该 md 进行 wiki 结构化加工；禁止跳过 md 中间产物、直接对原文件（PDF/DOCX/HTML）做人工摘录式加工而不留可检索的 md。
```

---
*配置版本：1.0*
*最近更新：2026-07-25*
