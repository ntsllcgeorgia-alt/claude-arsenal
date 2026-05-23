# token-check

Count Claude tokens for any text or file. Estimate the API cost across Sonnet, Opus, and Haiku before you send.

Built 2026-05-18, sourced from Karpathy's "Let's build the GPT Tokenizer" lecture (the 15-min clip you watched via @rohit4verse on X). The lecture's core insight — "tokens are the atom of LLMs" — means that every cost, every context-window warning, every "why does Claude do that weird thing" question traces back to tokenization. This skill makes token counting one command away.

## Why this exists

Three pains it solves:

1. **"Is this prompt too expensive?"** — you have a 4K-character system prompt for a new skill. Will it cost $0.01 or $1 per invocation? You can't eyeball this.
2. **"Should I use Sonnet or Opus?"** — same input, 5x cost difference. For routine tasks, Haiku is 15x cheaper than Opus.
3. **"Why is my context filling so fast?"** — measure the actual weight of your inputs instead of guessing.

## Quick start

```bash
# Inline
python $HOME/.claude/skills/token-check/token_check.py --text "your prompt here"

# A file
python $HOME/.claude/skills/token-check/token_check.py --file C:/Projects/your-project/vault/Higgsfield Stack.md

# Pipe from anything
type prompt.md | python $HOME/.claude/skills/token-check/token_check.py

# With a custom expected output size
python $HOME/.claude/skills/token-check/token_check.py --file prompt.md --output-tokens 5000
```

## Example output

```
=== Token check ===
Input:  Higgsfield Stack.md (8,219 chars)
Output projection: 500 tokens

Model         In tokens     In cost      Est out cost         Total
-----------------------------------------------------------------------
Opus 4.7         1,847    $0.02771       $0.03750             $0.06521
Sonnet 4.6       1,847    $0.00554       $0.00750             $0.01304
Haiku 4.5        1,847    $0.00185       $0.00250             $0.00435

Source tokenizer: Claude (via Anthropic count_tokens API — free)
```

## How it works

Wraps Anthropic's `messages.count_tokens()` endpoint, which:

- Uses the **actual** Claude tokenizer (not an approximation)
- Returns the exact token count that the priced API would use
- Costs nothing — Anthropic offers `count_tokens` as a free endpoint
- Runs in milliseconds (no generation, just a parse)

The skill calls this endpoint once per model (Opus/Sonnet/Haiku) and tabulates the result.

## When to reach for this

- **Before shipping a new skill** — check that the prompt template inside it isn't bloated
- **Before kicking off an expensive agent task** — estimate the bill before pulling the trigger
- **When comparing Sonnet vs Opus** — see the cost delta on a real prompt, not an average
- **When auditing existing skills** — point it at every SKILL.md and find the heaviest one
- **When building MCPs** — every tool definition costs tokens on every message; measure them

## What it doesn't do

- Bloat warnings (repeated phrases, whitespace runs) — possible v2
- Folder-wide totals (sum tokens across a whole project) — possible v2
- GPT-4 / Gemini tokens — use `tiktoken` for OpenAI; Gemini has its own API
- Real-time monitoring of an in-flight conversation — that's the Claude Code UI's job

## The Karpathy insight, applied

Karpathy's lecture surfaces five tokenization weirdnesses you'll see in your daily Claude use:

| Behavior | Tokenization cause |
|---|---|
| "Count the r's in strawberry" → wrong | Word is one token; letters aren't visible |
| 3-digit math errors | "127" is one token, "677" is two — digit chunking is arbitrary |
| Non-English prompts cost 2-4x more | Tokenizer trained mostly on English |
| Python with deep indentation balloons | (Older models) each space was its own token |
| MCPs feel "heavy" | Every tool's schema loads as tokens on every message |

`/token-check` lets you measure all of these directly.

## Maintenance

- Pricing in [token_check.py](token_check.py) is hardcoded per the model row. Update when Anthropic changes prices.
- If a new model is released, add it to the `MODELS` list at the top of [token_check.py](token_check.py).

## Related notes

- [vault/wiki/method_tokenization_karpathy.md](C:/Projects/your-project/vault/wiki/method_tokenization_karpathy.md) — the underlying theory
- [vault/wiki/method_steinberger_agentic_coding.md](C:/Projects/your-project/vault/wiki/method_steinberger_agentic_coding.md) — lesson #6 (CLI over MCP for token reasons)
- [tiktokenizer.vercel.app](https://tiktokenizer.vercel.app) — visual tokenizer playground
