---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## What is the Skills CLI?

The Skills CLI (`npx skills`) is one common package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

- `npx skills find [query]` - Search for skills interactively or by keyword
- `npx skills add <package>` - Install a skill from GitHub or other sources
- `npx skills check` - Check for skill updates
- `npx skills update` - Update all installed skills

**Browse skills at:** https://skills.sh/

If the current runtime does not provide `npx skills`, use the same discovery flow with whichever local skill installer is available, or browse `skills.sh` manually and present matching packages to the user.

## How to Help Users Find Skills

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

If the request is ambiguous enough that different interpretations would produce different skill categories, present at most three concrete interpretations and ask the user to choose one.

**CHECKPOINT:** Do not install anything during discovery. First show the source, package name, purpose, and installation impact. Install only after the user explicitly confirms the exact package.

### Step 2: Search for Skills

Run the find command with a relevant query:

```bash
npx skills find [query]
```

If that CLI is unavailable, search the catalog manually on `skills.sh` or use the runtime's built-in skill discovery workflow.

For example:

- User asks "how do I make my React app faster?" → `npx skills find react performance`
- User asks "can you help me with PR reviews?" → `npx skills find pr review`
- User asks "I need to create a changelog" → `npx skills find changelog`

The command will return results like:

```

### Search Failure Recovery

| Trigger | First response | If it still fails |
|---|---|---|
| `npx skills` is unavailable | Search `skills.sh` or use the runtime's built-in discovery capability | Explain that live catalog access is unavailable and provide precise manual search terms |
| The catalog returns no results | Retry once with one broader synonym and one domain-specific synonym | Stop searching and offer direct help or creation of a focused custom skill |
| Network access is denied | Request network permission only when live search is necessary | Continue with locally installed skills and clearly label results as local-only |
| A result has unclear ownership or contents | Inspect its source and `SKILL.md` before recommending it | Exclude it from the recommendation and explain why |
Install with npx skills add <owner/repo@skill>

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### Step 3: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. The install command they can run in the current runtime
3. A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "vercel-react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.

To install it:
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

If the runtime uses a different installation flow, keep the same package reference and adapt the install instruction instead of forcing `npx skills`.

### Step 4: Offer to Install

If the user wants to proceed, you can install the skill for them:

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.
If this command is unavailable, use the runtime's supported install flow or clone/install the skill into that runtime's skills directory.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or similar public skill collections

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init` or the runtime's equivalent skill scaffolding command

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```

## Do Not Do These

- Do not invent package names, owners, download links, popularity, or compatibility claims.
- Do not recommend a skill based only on its title; inspect its description and source when available.
- Do not install a package before the user confirms the exact package and destination.
- Do not overwrite an existing skill directory silently. Report the conflict and preserve the installed copy.
- Do not treat discovery as proof of safety. Verify that the package contains `SKILL.md` and review unexpected scripts before installation.
