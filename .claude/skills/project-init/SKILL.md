---
name: project-init
description: |
  Scaffold a new project with the two "non-negotiable" Claude files: CLAUDE.md (project
  behavior / voice / guardrails) + project_specs.md (what this project IS, success
  criteria, constraints). Inspired by Jono Catliff's 500-hour Claude Code playbook:
  every project gets these two files before any code is written, full stop.

  Use when: "/project-init", "start a new project", "set up [folder] as a Claude project",
  "init this folder", "scaffold the CLAUDE.md and specs for [project]".

  Output: writes CLAUDE.md, project_specs.md, .gitignore, README.md skeleton to the
  current folder (or --path target). Inherits your global CLAUDE.md voice rules so
  the project-level file doesn't repeat what's already in ~/.claude/CLAUDE.md.

  NOT for: marketing-specific brand briefs (use marketing-context instead), or
  reinitializing a folder that already has these files (will refuse — bring receipts).
argument-hint: "[--path <dir>] [--type web|app|api|marketing|misc] [--name <project>]"
allowed-tools: Read, Write, AskUserQuestion
---

# project-init — bootstrap a new Claude project

## Why this exists

From Jono Catliff (500 hours of Claude Code use): *"The next tip is having two files
inside every project you create. The CLAUDE.md file and the project_specs file.
These are non-negotiables for me."*

Most "Claude wrote bad code" complaints trace back to missing these two files. Claude
defaults to generic best-practices when there's no project context, and generic
best-practices are wrong for your project ~50% of the time.

## What gets written

### `CLAUDE.md` — project behavior rules
Folder-level instructions Claude auto-loads in every session inside this directory.
Layered on top of `~/.claude/CLAUDE.md` (global rules), so this file ONLY covers
project-specific behavior — voice, tech stack, conventions, what to never touch.

### `project_specs.md` — what this project IS
The source of truth for project identity. Answers:
- What problem does this solve?
- Who's it for?
- What does "done" look like?
- What's explicitly out of scope?
- Non-obvious constraints

### `README.md` — public-facing description (skeleton)
Quick blurb + install + usage. The user fills the real content.

### `.gitignore` — sensible defaults by project type
Avoids the "I accidentally committed `.env`" disaster.

## Trigger phrases

`/project-init`, "init this folder", "set up this project for Claude",
"create the CLAUDE.md and specs", "scaffold a new project".

## Process

### 1. Detect or ask for project type

Look at the current folder for signals:
- `package.json` → web (Node) or app (React/Next)
- `pyproject.toml` / `requirements.txt` → api or misc Python
- `Cargo.toml` → api (Rust)
- `index.html` + no package.json → static web
- empty folder → ask

If ambiguous, ask ONE question:
> "What kind of project is this — web, app, api, marketing, or misc?"

### 2. Ask for the bare essentials (4 questions max, bundled)

Use `AskUserQuestion` with all of these at once, never one-at-a-time:

1. **Project name** (short — e.g. "claude-arsenal", "ntp-mobile")
2. **One-sentence problem** ("What problem does this solve?")
3. **Primary user** ("Who's it for?")
4. **One constraint that's non-obvious** ("Anything I should know that I won't pick up from reading the code?")

If the user types short answers, run with them. Don't push for more.

### 3. Write the files

For each file, **check if it exists first**. If yes, surface to user:
> "CLAUDE.md already exists at <path>. Overwrite, append, or skip?"

Never silently overwrite. Confirmation is the default.

### 4. CLAUDE.md template

```markdown
# <Project Name>

Folder-level Claude instructions. Auto-loaded when working in this directory.
Layers on top of `~/.claude/CLAUDE.md` (global rules).

---

## What this project is

<One-sentence problem from intake.>
<One sentence on the primary user.>

See `project_specs.md` for the full spec.

## Stack

<Auto-detected stack from signals: e.g. "Next.js 15 + Tailwind + TypeScript" /
"Python 3.12 + FastAPI" / "Static HTML/CSS, no framework". Edit if wrong.>

## Conventions

<Pulled from auto-detection — e.g. "All TypeScript files in src/, tests in tests/,
two-space indentation". Default to widely-used conventions for the stack.>

## Voice (if a marketing / customer-facing project)

<If --type marketing: include voice rules. Otherwise skip this section.>

## Don't

- Don't <constraint #1 from intake — e.g. "use any framework not already in package.json">
- Don't push to main without a PR
- Don't edit files outside this folder unless explicitly asked

## When in doubt

Ask one clarifying question, not five.
```

### 5. project_specs.md template

```markdown
# Project specs — <Project Name>

## The problem

<One-sentence problem from intake.>

## Who it's for

<Primary user from intake.>

## What "done" looks like

- [ ] <Concrete milestone #1 — auto-filled placeholder if user didn't specify>
- [ ] <Concrete milestone #2>
- [ ] <Concrete milestone #3>

## Out of scope

- <Auto-fill: "Anything the spec above doesn't explicitly cover.">

## Non-obvious constraints

<Whatever the user said in question 4. If they said nothing, write: "None known yet —
add here as discovered.">

## Decisions

(Track major architectural / strategic decisions as they happen. Each entry: date,
decision, reason. This becomes the project memory across Claude sessions.)

- <YYYY-MM-DD>: Project initialized.
```

### 6. .gitignore by type

**Web / app (Node):**
```
node_modules/
.next/
dist/
build/
.env
.env.*
*.log
.DS_Store
```

**API (Python):**
```
__pycache__/
*.pyc
.venv/
venv/
.env
.env.*
*.log
.pytest_cache/
.mypy_cache/
```

**Marketing / misc:**
```
.env
.env.*
*.log
output/
.DS_Store
*.backup
```

### 7. README.md skeleton

```markdown
# <Project Name>

<One-sentence problem.>

## Quick start

<Auto-fill based on detected stack. E.g. for Node: `npm install && npm run dev`.>

## Status

In development.
```

### 8. Final output

Print to the user:
```
✓ project-init complete

Created in <path>:
  CLAUDE.md           (project behavior rules)
  project_specs.md    (what this project is)
  README.md           (public skeleton)
  .gitignore          (sensible defaults for <type>)

Next:
  - Edit project_specs.md to flesh out "What done looks like" milestones
  - Edit CLAUDE.md if any conventions are wrong
  - Then describe what you want to build — Claude has context now
```

## Cost / time

- ~30 seconds end-to-end
- ~2¢ in tokens (small templated writes)

## Common patterns

### "Init this folder for a new SaaS landing page"
```
/project-init --type web --name acme-landing
```
→ CLAUDE.md with web conventions, project_specs.md, web-flavored .gitignore.

### "Start a new agency client project"
```
mkdir clients/regal-nails && cd clients/regal-nails && /project-init --type marketing
```
→ Marketing-flavored setup with voice rules placeholder.

### "Quick init — bare minimum"
```
/project-init --name quick-test
```
→ Skips all questions, writes minimal templates the user fills later.

## Pairs well with

- `marketing-context` — run AFTER project-init on marketing projects, layers MARKETING.md
- `claude-design` — pulls project_specs.md to inform design briefs
- `handoff` — restart prompts include "read project_specs.md first"

## What this is NOT

- It's NOT a code generator. No source files, no API scaffolds, no framework setup.
- It's NOT marketing-context. That skill builds MARKETING.md with brand voice, ICP,
  competitive landscape — much heavier. project-init is just the two "non-negotiable"
  Claude files.
- It's NOT a CMS / Notion / Confluence replacement. The files are markdown the user
  edits in their editor. Source of truth is the repo.
