---
project: 注册会计师竞赛知识库
domain: 专业教育
created: 2026-06-24
---

# 知识库配置

## 项目信息

- **名称**：注册会计师行业青年知识竞赛知识库
- **领域**：专业教育
- **说明**：围绕注册会计师行业青年知识竞赛的知识清单建立的持续积累型知识库，用于沉淀法规、准则、政策、职业道德、实务技能与备赛方法。
- **创建时间**：2026-06-24
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
    - competition
    - regulator
  required_attributes:
    organization: [role, scope]
    regulation: [issuer, level]
    standard: [issuer, topic]
    policy: [issuer, date]
    event: [date, significance]
```

## 概念分类

```yaml
concepts:
  categories:
    - framework
    - method
    - principle
    - competency
    - study-plan
  domain_concepts:
    - audit-practice
    - professional-ethics
    - examination-prep
```

## 工作流配置

```yaml
workflow:
  default_mode: batch
  interactive_keywords:
    - 核心
    - 重点
    - 法规原文
    - 真题
    - 案例
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
    - check_orphans
    - check_missing_pages
    - check_incomplete_metadata
    - check_data_gaps
  severity:
    orphan_page: warning
    missing_page: warning
    incomplete_metadata: warning
    data_gap: suggestion
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
    - reviewed
    - structured
  domain:
    - cpa
    - competition
    - audit
    - standards
    - regulation
    - ethics
    - policy
    - skills
```

## 命名规则

```yaml
naming:
  source_files: "{date}-{slug}.{ext}"
  entity_pages: "entities/{slug}.md"
  concept_pages: "concepts/{slug}.md"
  source_summaries: "sources/{date}-{slug}.md"
  id_format: "{type}-{slug}"
```

## 来源目录

```yaml
sources:
  directories:
    - reports/
    - notes/
    - cases/
    - assets/
  default_types:
    reports/: report
    notes/: note
    cases/: case
```

## 质量要求

```yaml
quality:
  required_metadata:
    concept: [title, type, concept_type, created, updated]
    source: [title, type, source_type, created, raw_path]
  claims:
    require_source: true
    require_confidence_level: false
```

## 自定义说明

```text
- 优先把清单类来源转化为可学习的结构化页面，而不是简单转存。
- 后续补充法规或准则原文时，按“核心要求、适用场景、常见考点、实务连接”四段展开。
- 强调法规、职业道德与审计实务之间的交叉链接。
- 对明显会变化的政策、考试办法和监管要求补充更新时间。
- 案例、模拟题和政策动态应优先链接到已有概念页。
```

---
*配置版本：1.0*
*最近更新：2026-06-24*
