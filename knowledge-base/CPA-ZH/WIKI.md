---
project: CPA-ZH
domain: professional-knowledge
created: 2026-06-26
---

# CPA-ZH 知识库配置

## 项目信息

- **名称**：CPA-ZH
- **领域**：中国注册会计师行业法规、准则、政策、职业道德与审计实务
- **说明**：围绕中国注册会计师行业建立的可持续知识库，用于沉淀法规准则、政策文件、职业道德、独立性要求、审计实务技能、智能化工具应用与案例分析。
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
  domain_concepts:
    - accounting-standards
    - audit-standards
    - professional-ethics
    - independence
    - audit-practice
    - policy-supervision
    - intelligent-tools
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
    outlines/: outline
```

## 质量要求

```yaml
quality:
  required_metadata:
    concept: [title, type, concept_type, created, updated]
    source: [title, type, source_type, created, raw_path]
    entity: [title, type, entity_type, created, updated]
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
- 智能化工具页面应同时记录适用场景、数据输入要求、控制点、局限性和审计证据留痕要求。
```

---
*配置版本：1.0*
*最近更新：2026-06-26*
