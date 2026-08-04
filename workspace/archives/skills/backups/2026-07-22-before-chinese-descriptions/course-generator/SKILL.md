---
name: course-generator
description: >
  Generate a complete self-study course from any learning material file for absolute beginners.
  The course must progress from easy to hard, cover every knowledge point in the source without
  omission, include strong memory aids such as comparison tables, mnemonics, analogy maps, and
  summaries, and provide knowledge-check exercises instead of calculation-heavy drills. Output as
  Markdown or self-contained interactive HTML. Use this skill when the user provides a file and asks
  to "make a course", "generate a curriculum", "create a tutorial", "制作课程", "生成教程",
  "整理学习资料", "零基础课程", "做成课件", "做成自学课程", "出习题", or any similar request
  to turn learning material into structured lessons for beginners.
---

# Course Generator

Turn any learning material into a beginner-friendly self-study course.

## Goal

Produce a course that:
- assumes zero prior knowledge
- covers the source completely
- teaches in dependency order
- adds memory aids on purpose
- checks understanding with exercises

## Core Principles

1. **Zero assumptions**: define every term on first use.
2. **No knowledge left behind**: every concept, rule, fact, process, relationship, exception, and example from the source must appear somewhere in the course.
3. **Progressive disclosure**: each chapter must rely only on concepts already introduced.
4. **Memory-first design**: every chapter needs explicit memory aids.
5. **Understanding over calculation**: exercises should verify comprehension, not rote computation.

## Output Modes

- **Markdown**: best for notes, printing, and quick review.
- **HTML**: best for interactive self-study with collapsible chapters, progress tracking, and instant quiz feedback.

If the user does not specify a format, ask during the planning checkpoint and default to `Markdown` only if they do not answer.

## Workflow

### Phase 0: Input Sanity Check

Before analysis, confirm the source can actually be used.

1. Identify the source file and its type.
2. Confirm the file is readable.
3. Estimate whether it is small, medium, large, or very large.
4. Confirm which output path or filename you will write.

Failure handling:
- If the source file cannot be found, stop and ask the user for the correct file.
- If the file exists but cannot be read, explain the read error and ask the user whether to retry with another file or another format.
- If the file is too large for one-pass analysis, switch to chunked analysis and tell the user that delivery will happen in batches.

### Phase 1: Deep Analysis

Read the source thoroughly. Then do three explicit passes.

#### Pass 1: Extract all knowledge points

List every:
- concept
- term
- definition
- rule
- principle
- fact
- formula with explanation
- process
- relationship
- exception
- example

If unsure whether something counts, include it.

#### Pass 2: Map dependencies

For each knowledge point, identify prerequisites and group them into:
- foundational concepts
- intermediate concepts
- advanced concepts

#### Pass 3: Identify confusable concepts

Find concepts learners are likely to mix up. These must later become:
- comparison tables
- contrast prompts
- concept-differentiation exercises

### CHECKPOINT 1: Plan Confirmation

After the three passes and before writing any course content, show the user this planning summary:

```text
📋 分析结果确认

一、知识点清单（共 N 个）
[按基础 / 中级 / 高级分组列出]

二、课程章节规划（共 M 章）
第0章：课程导引
第1章：...
第2章：...

三、主要易混淆概念对
- 概念A vs 概念B
- 概念C vs 概念D

四、输出格式
1. Markdown
2. HTML

请确认规划是否符合预期，并选择输出格式。如需调整章节、顺序或范围，请直接说明。
```

Rules:
- Do not start drafting chapter content before the user confirms.
- If the user requests changes, update the plan and re-confirm.
- If the user already chose the format earlier, keep that choice in the confirmation summary instead of asking again.

### Phase 2: Course Architecture

After confirmation, build the course architecture.

#### Mandatory chapter order

- `第0章` or `课前准备`: course introduction only
- `第1章` onward: content chapters in prerequisite order
- final sections: global review, glossary, progress checklist, answer key

#### Mandatory content for 第0章

Include:
- how to use the course
- study method suggestions
- course structure explanation
- optional tool recommendations

#### Mandatory structure for every content chapter

Every chapter must contain:
1. `学习目标`
2. `核心内容`
3. `记忆辅助`
4. `本章小结`
5. `知识检测`

#### Mandatory end matter

Include:
- a complete glossary of all defined terms
- a course-wide review section
- a progress checklist
- an answer key or answer blocks for chapter exercises

### Phase 3: Content Writing Rules

For each concept:
- start with a concrete analogy before the abstract definition when helpful
- define terms immediately
- explain in plain language
- provide at least one example
- use the pattern `what -> why -> how`

### Memory Aid Requirements

Every content chapter must contain:
- at least one **comparison table**
- at least one additional memory aid type

Available memory aid types:
1. comparison table
2. mnemonic rhyme
3. analogy map
4. mind-map summary
5. common-mistake cards
6. one-line summaries

### Exercise Rules

Exercises must test understanding, not calculation.

Use at least three exercise types per chapter. Valid types include:
- 判断题
- 单选题
- 多选题
- 填空题
- 配对题
- 概念辨析
- 情景判断
- 排序题
- 归类题

Exercise volume guideline:
- short chapter: 5-8
- medium chapter: 10-15
- long chapter: 15-25

## Incremental Output Workflow

Never try to print the whole course in one assistant response.

Use the runtime's available file creation and file editing capability to assemble the course incrementally.

### Step 1: Create the skeleton file

Create the full course file first with:
- title and metadata
- table of contents
- chapter placeholders
- ending-section placeholders

### Step 2: Fill chapters in order

Replace placeholders one chapter at a time, starting from `第0章`.

If a chapter is too large:
- split it into multiple edits
- keep the file valid after every write

### Step 3: Fill ending sections

After all chapters are inserted, replace:
- global review placeholder
- glossary placeholder
- progress placeholder
- answer key placeholder

### Markdown Route

Read `references/markdown-template.md` before generating Markdown output.

Use that file for:
- the skeleton format
- placeholder names
- chapter section order
- ending section order

### HTML Route

Read `assets/html-template.html` in full before generating HTML output.

Rules:
1. keep its CSS and JS infrastructure intact
2. keep the file self-contained
3. use the template placeholders exactly as documented in the HTML template
4. avoid injecting unescaped AI-generated text into unsafe HTML contexts

Failure handling:
- If `references/markdown-template.md` is missing, create a Markdown skeleton using the placeholder contract documented in this skill and tell the user you are using the fallback template.
- If `assets/html-template.html` is missing, fall back to Markdown unless the user explicitly requires HTML.
- If a placeholder replacement fails because the marker is missing, stop, inspect the output file, repair the placeholder structure, and continue only after the file is valid again.
- If file writing fails mid-course, report which chapter was last completed and resume from the next placeholder after the write path is fixed.

## Large File Strategy

If the source is very large:

1. Analyze in logical chunks.
2. Estimate the number of chapters.
3. Offer:
   - full generation in one end-to-end run
   - phased delivery in chapter batches
4. Do not omit source content just to stay short.

### Recommended Size Tiers

Use extracted text size as the primary signal, not just the raw file size on disk.

- **Small: <= 20KB extracted text**
  - Usually safe for one-pass analysis.
  - Full end-to-end generation is often feasible, but chapter-by-chapter writing is still preferred.

- **Medium: 20KB - 50KB extracted text**
  - One-pass analysis is acceptable when the structure is simple.
  - If the source is dense or highly technical, switch to chunked analysis.
  - Prefer chapter-by-chapter output assembly.

- **Large: 50KB - 200KB extracted text**
  - Always use chunked analysis.
  - Always estimate chapter count before drafting.
  - Always offer phased delivery in chapter batches.
  - Do not attempt to draft the whole course body in one uninterrupted generation pass.

- **Very large: > 200KB extracted text**
  - Treat it as a multi-stage project.
  - Build a master knowledge-point inventory first.
  - Confirm the chapter plan before drafting content.
  - Deliver in batches by chapter range or topic group.
  - Finish with a consolidation pass for glossary, review, and answer sections if needed.

### Density Override

Even below 50KB, treat the file like a larger tier when any of these are true:
- the source is unusually dense, such as legal, technical, or research-heavy writing
- a short file contains many distinct terms, rules, or exceptions
- the material mixes multiple domains or multiple languages
- the user explicitly wants exhaustive coverage with many exercises and memory aids

When these conditions appear, prefer chunked analysis and phased delivery earlier.

## Quality Checklist

Before presenting the finished course, verify:

- every source concept appears somewhere in the course
- the user confirmed the analysis plan
- `第0章` is present
- glossary is present
- chapter order respects prerequisites
- every chapter has all five required sections
- every chapter includes a comparison table
- every chapter includes at least one additional memory aid
- exercise types are mixed
- no placeholder markers remain
- the final file is complete and readable

## Blacklist: Do Not Do These

- Do not skip "obvious" concepts because they seem basic.
- Do not introduce terms before defining them.
- Do not collapse the whole course into one response.
- Do not replace comparison tables with generic prose.
- Do not use exercise sections for calculation-heavy drills unless the source itself is explicitly about calculation practice.
- Do not silently drop chapters, glossary entries, or answer sections because of token pressure.
- Do not continue writing after a failed file edit without first checking what was actually written.

## Runtime-Neutral File Editing Guidance

This skill must work across different skill-compatible runtimes.

Use whichever local file tools the current runtime provides to:
- create the output file
- insert chapter content
- inspect partially written output
- resume after interruption

Do not hardcode one product's tool names as if they are universally available.

## Different Source Types

- **Textbooks / PDFs**: preserve coverage, but reorganize for progressive learning when needed.
- **Lecture notes / slides**: expand terse bullets into explanations and examples.
- **Reference manuals / docs**: group related features and add scenario-based teaching.
- **Research papers**: teach background first, then method, then implications.
- **Code or technical docs**: teach concept -> syntax -> example -> practice.
- **Mixed sources**: identify the primary domain and organize around its natural learning path.

## Language Rules

- By default, match the main language of the source.
- If the user requests another language, follow the user's request.
- For mixed-language material, use the dominant language and translate key foreign terms on first use.
- Mnemonics and analogies should match the course output language.
- The glossary should include original terms plus translations when needed.
