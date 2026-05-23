---
name: handoff
description: Generate a clean restart prompt to move this conversation to a fresh Claude Code chat. Use when the current session is getting long (~20+ turns) and tokens are stacking up because Claude re-reads the entire history every turn.
---

You are about to hand off this conversation to a new Claude Code session.

Generate a single self-contained "restart prompt" that gives the new session everything it needs without making it re-derive context from a long chat history.

## Structure

Output the restart prompt inside ONE fenced code block. Inside the block, use these sections:

1. **What we're working on** — 1-2 sentences on the current task / project.
2. **State right now** — what's done, what's in progress, key files with absolute paths.
3. **Next step** — the immediate next thing the new session should do.
4. **Constraints / decisions / gotchas** — non-obvious things that won't be picked up just by reading the code (e.g., "we decided NOT to use approach X because Y", "the user is non-technical, prefers brief answers", "don't push to remote without asking").
5. **Read these first** — file paths in priority order, no more than 5.

## Rules

- Keep the restart prompt under 400 words.
- Do not include conversational filler ("we had a great chat", "as we discussed", etc.). The new session doesn't need to know how this chat went, only where things are now.
- Use absolute file paths (Windows style: `C:\Users\...\file.md`) since you is on Windows.
- If a memory file or playbook is relevant, reference its path so the new session loads it instead of repeating its contents.
- Do NOT include API keys, passwords, or credentials in the restart prompt.

## After generating

Below the fenced code block, write one short line to you:

> Paste this into a fresh Claude Code chat. You can close this one. Tokens saved.
