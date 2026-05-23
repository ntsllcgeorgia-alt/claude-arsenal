---
name: token-check
description: |
  Count Claude tokens for any text, file, or prompt — and estimate the API cost
  across Sonnet 4.6, Opus 4.7, and Haiku 4.5. Built on Anthropic's count_tokens
  API (free, accurate, no message generation).

  Use when: you asks "how many tokens in this", "how much would this cost",
  "is this prompt too long", "what's the token cost of [file/folder]", or wants
  to compare a prompt's cost across Claude models before sending.

  Triggers on: "/token-check", "token count for [...]", "how much does this cost
  in Claude", "count tokens", "is this too long for Sonnet".

  NOT for: live message generation (just use Claude normally), GPT/OpenAI
  tokenization (use tiktoken directly), context-window-warning while in a
  conversation (that's automatic).
---

# token-check — Claude token counter + cost estimator

## What this does

Wraps Anthropic's `messages.count_tokens` API into a one-shot CLI. Pass text or a file path, get:

- Token count using the actual Claude tokenizer (not an estimate)
- Side-by-side cost across Sonnet 4.6, Opus 4.7, Haiku 4.5
- Cost estimate for input + a configurable expected output length

## How to invoke

```bash
# Inline text
python $HOME/.claude/skills/token-check/token_check.py --text "your text here"

# A file
python $HOME/.claude/skills/token-check/token_check.py --file path/to/prompt.md

# Piped from stdin
cat path/to/prompt.md | python $HOME/.claude/skills/token-check/token_check.py

# With expected output size (default 500 tokens)
python $HOME/.claude/skills/token-check/token_check.py --file prompt.md --output-tokens 2000
```

## Output format

```
=== Token check ===
Input:  prompt.md (4,127 chars)

Model            Input tokens   Input cost     Est. output cost (2000 tok)   Total
Opus 4.7         982            $0.01473       $0.15000                       $0.16473
Sonnet 4.6       982            $0.00295       $0.03000                       $0.03295
Haiku 4.5        982            $0.00098       $0.01000                       $0.01098

Source tokenizer: Claude (via Anthropic count_tokens API)
```

## When you should reach for this

- Before shipping a new SKILL.md — check its prompt template isn't bloated
- Before kicking off a big agent task — estimate the bill
- When comparing Sonnet vs Opus for the same prompt — see cost delta
- When debugging "why is my context filling so fast" — measure real input weight
- Before posting a big system prompt to a new project's CLAUDE.md

## Prerequisites

- Python 3.10+ (you has 3.12 at C:\Python312)
- `anthropic` Python package — script auto-installs if missing
- `ANTHROPIC_API_KEY` set in env (you already has this via Claude Code)

## What it doesn't do (v1)

- Bloat analysis (repeated phrases, whitespace runs) — possible v2
- Folder/project-wide token totals — possible v2
- GPT-4 / Gemini token counts — out of scope, use tiktoken directly
- Cost projections across a full conversation — too many variables

## Cost of running this skill

Anthropic's `count_tokens` endpoint is **FREE**. The skill makes ~3 calls (one per model) per invocation. No tokens consumed.

## Related

- [[wiki/method_tokenization_karpathy]] — the underlying theory
- [[wiki/method_steinberger_agentic_coding]] — #6 on MCP token tax
- Karpathy's full lecture — "Let's build the GPT Tokenizer" on YouTube
