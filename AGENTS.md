# Repository Rules

This file defines the default instructions for agents working in `ai-audit`. It is an internal development guide, not end-user documentation.

## Start-of-Task Protocol

Before changing a file:

1. Read this file in full and inspect `git status --short`.
2. Identify the exact target files and the smallest practical scope.
3. Read the applicable local documentation and existing implementation before selecting an approach.
4. Check for a nearer `AGENTS.md` below the target directory. A nearer file takes precedence unless it conflicts with this file or an explicit user request.

Re-read this file when work expands into another area, introduces a dependency, moves files, performs a batch rewrite, or deletes content. Preserve all unrelated working-tree changes.

Read these documents when applicable:

- `README.md`: workspace entry points and repository boundaries.
- `knowledge-base/CPA-ZH/README.md`: knowledge-base workflow and operating model.
- `knowledge-base/CPA-ZH/WIKI.md`: content model, frontmatter, and source requirements.
- `tools/README.md`: maintenance commands, write modes, and script responsibilities.
- `workspace/docs/generated-artifacts.md`: source assets versus rebuildable artifacts.
- `frontend/README.md` or `backend/README.md`: application-specific build and run details.

## Non-Negotiable Editing Rules

1. Treat all project text files as UTF-8. Do not introduce BOMs, mojibake, or incorrectly encoded Chinese text.
2. Any file containing Chinese text must use UTF-8 without BOM.
3. Before editing a Chinese-text file, confirm its content renders correctly. Afterward, reopen the changed lines and verify the text again.
4. Prefer small, targeted patches. Do not use `Set-Content`, `Out-File`, pipeline rewrites, blind bulk replacement, or unsafe whole-file rewrites on files containing Chinese text.
5. Do not change unrelated Chinese comments, UI copy, prompts, or Markdown simply while touching a file.
6. If a target file appears garbled, stop and restore or confirm its encoding before continuing.
7. Do not add secrets, access tokens, machine-specific paths, or downloaded third-party assets to the repository.
8. Do not reset, reformat, delete, or overwrite changes outside the requested scope.

## Project Boundaries

`ai-audit` is a local knowledge workbench for the Chinese CPA profession. Its primary asset is `knowledge-base/CPA-ZH`, which covers laws, standards, policy, ethics, audit practice, cases, and learning materials.

| Path | Role | Editing rule |
| --- | --- | --- |
| `knowledge-base/CPA-ZH/raw/` | Original materials, Markdown facades, manifests | The factual source layer; do not derive facts only from binary originals. |
| `knowledge-base/CPA-ZH/wiki/` | Structured knowledge, sources, cases, Q&A, indexes | Never overwrite `raw/` from this derived layer. |
| `knowledge-base/CPA-ZH/source-registry.yml` | Official-source registry | Keep status, source URL, local raw path, and date evidence consistent. |
| `knowledge-base/CPA-ZH/cache/`, `search/` | Text cache and local indexes | Rebuild; do not hand-edit. |
| `tools/` | Python maintenance, conversion, classification, and delivery tooling | Prefer `tools/kb.py`; keep shared CLI routing in `tools/kb_cli_support.py`. |
| `backend/` | Read-only FastAPI API | It reads knowledge assets and rebuildable indexes; do not make it a write path. |
| `frontend/` | Vue 3 + Vite knowledge-base browser | `frontend/dist/` is a rebuildable static release artifact. |
| `course/source/` | Course Markdown sources | `course/dist/` and `course/slides/` are release artifacts. |
| `workspace/outputs/`, `workspace/tmp/` | One-off outputs and temporary files | Never treat as factual sources. |
| `archived/` | Historical projects and retired tools | Read-only by default; do not develop new features here. |

Keep the repository root limited to configuration, short entry documentation, dependency manifests, and the existing user-facing launchers. Put new implementation scripts in `tools/` unless an existing area has a more specific home.

## Technology Rules

- Use Python for backend and maintenance scripts. The API remains FastAPI. Do not introduce another backend runtime without explicit user approval.
- The active UI stack is Vue 3, Vite, TypeScript, and Ant Design Vue. New or substantially rebuilt UI must use it; do not introduce React or another UI library.
- Vue components use `<script setup lang="ts">`; do not add `.js`, JSX, or TSX components.
- Use Ant Design Vue components and tokens for forms, tables, navigation, dialogs, feedback, date controls, and layout. Use standard CSS only for layout, hierarchy, brand expression, and necessary visual tuning; do not add CSS-in-JS.
- Keep `App.vue` thin. Organize UI by feature, with bounded components, composables, services, and styles. Promote code to shared directories only when it is actually cross-feature.
- Before adding frontend dependencies or build tooling, inspect `frontend/package.json`, delivery commands, and API/static-hosting impact; update dependency manifests and relevant documentation together.

## Knowledge-Base Content Rules

1. Put new source materials in `raw/`, create or update the batch `manifest.json`, then derive structured pages in `wiki/`.
2. Convert PDF, DOCX, HTML, and similar originals into a searchable `raw/*.md` facade before editorial processing. Use `tools/kb.py archive-doc`, `tools/kb.py pdf-md`, or `tools/convert_raw_to_md.py` as appropriate.
3. Prefer official sources for laws, standards, and policies. Record the source URL, local raw path, legal/effectiveness status, and update date. Verify the effective version before claiming "latest", "revised", or "in force".
4. Follow the `WIKI.md` frontmatter schema for new or materially changed wiki pages. Source factual claims. Keep unverified answers as candidates or drafts, not formal conclusions.
5. Case cards must cover facts, issue, applicable rules, reasoning, audit focus, and working-paper evidence.
6. For write-capable `kb.py` commands, first run the dry run without `--commit`; review the target and diff before committing.
7. Do not store Chen Yiwei / Chen moderator forum Q&A originals, excerpts, question numbers, derived cards, or summary indexes in this repository. When a user asks for Chen Yiwei's perspective, Chen moderator forum answers, or real historical forum Q&A, route the work to the installed `chen-yiwei-perspective` and/or `chenyiwei-bbs` skills instead of creating CPA-ZH local knowledge pages from that material.

## Development and Validation

Use the workspace virtual environment for Python commands:

```powershell
.\.venv\Scripts\python.exe
```

Use the existing maintenance entry point whenever it supports the operation:

```powershell
.\.venv\Scripts\python.exe tools\kb.py health
.\.venv\Scripts\python.exe tools\kb.py cache build
.\.venv\Scripts\python.exe tools\kb.py index
.\.venv\Scripts\python.exe tools\kb.py schema --write-report
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

Apply verification in proportion to the change:

- Python scripts: run focused tests; run the full unittest suite for shared tooling, CLI routing, or validation changes.
- Raw, wiki, manifests, or source registry: run the relevant `cache build`, `index`, `schema --write-report`, and `health` commands. Do not leave stale generated indexes or README statistics.
- FastAPI API: start the local API only when the task requires runtime verification, then check the affected endpoint. The standard command is `.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8765`.
- Vue UI: run the relevant frontend checks from `frontend/` (`npm run test` and/or `npm run build`). Start `npm run dev` only when runtime UI verification is required; it proxies `/api` to the local API on port `8765`.
- Dependencies: update the relevant dependency manifest and verify the affected entry point in the workspace environment.

Do not restart the API or frontend merely because files changed. Start or stop them only when the user asks or when runtime validation is necessary for the requested work.
