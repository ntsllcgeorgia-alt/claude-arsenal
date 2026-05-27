---
name: quality-gate
description: |
  Score-and-critique any deliverable BEFORE you ship it. Picks a rubric based on
  what you're shipping (landing page, cold email, social post, code, design brief,
  proposal), scores each axis 1-10, surfaces what's dragging the score down, and
  returns a prioritized fix list. Designed to be the last step before you hit send.

  Inspired by Jono Catliff's "quality gates" rule in his Claude Code workflow:
  Claude scores its OWN output 1-10 against a defined rubric before saying "done."

  Use when: "/quality-gate", "score this before I send", "review this for me",
  "rate this 1-10 and tell me what's wrong", "would you ship this?", "QA this".

  Output: a structured report — score per axis, top 3 issues with exact fixes,
  one-line ship/don't-ship verdict. No fluff, no "this is great overall!" hedging.

  NOT for: code security review (use security-review), conversion-rate optimization
  on a live page (use cro-audit), or stress-testing a strategic decision (use
  counterargument).
argument-hint: "<deliverable-path-or-paste> [--type landing|email|social|code|copy|proposal|design]"
allowed-tools: Read, Glob, Grep, WebFetch
---

# quality-gate — last critical pass before you ship

## Why this exists

Most "Claude wrote okay output" failures happen because Claude marks its own
homework as "good enough." Without a rubric and a score, "good enough" drifts
toward "doesn't suck" — which is the floor, not the ceiling.

This skill forces Claude to (a) pick a rubric, (b) score, (c) name what's
dragging the score, (d) give exact fixes. Brutal honesty is the whole point —
"7/10, looks fine" is a failed quality gate. Either the score is real or the
gate didn't run.

## Trigger phrases

`/quality-gate`, "score this", "rate this 1-10", "review before I send",
"QA this", "would you ship this?", "what's wrong with this".

## Process

### 1. Detect deliverable type (or accept --type override)

Auto-detect from input:
- File extension `.html` / `.jsx` / `.tsx` / URL → **landing page**
- File extension `.py` / `.ts` / `.js` / `.go` / `.rs` → **code**
- Plain text starting with "Hi <name>," / "Hey <name>," → **email**
- 80-300 chars of casual text with hashtag or link → **social post**
- 500+ words pitching something → **proposal**
- Image / Figma URL → **design**
- Anything else → ask: `What kind of deliverable is this — landing / email / social / code / copy / proposal / design?`

### 2. Pick the rubric (5 axes per type)

**Landing page (rubric):**
1. **Hook clarity** — Does the headline answer "what is this?" in <3 seconds?
2. **Promise specificity** — Concrete outcome, or vague "transform your business"?
3. **Proof** — Specific names/numbers/results, or generic testimonials?
4. **CTA strength** — Single primary action, friction-free, above the fold?
5. **Visual hierarchy** — Eye lands on hero → benefit → CTA without scanning?

**Cold email (rubric):**
1. **Subject specificity** — Would they recognize you mean THEM, not a list?
2. **Opener relevance** — First line about them, not you?
3. **Value claim** — Concrete number / proof, or "we help companies grow"?
4. **Ask size** — 15 min / quick reply, or "let's get on a call"?
5. **Length** — Under 90 words for cold; under 150 for warm?

**Social post (rubric):**
1. **Hook** — Stops scroll? Specific number, contrarian take, or stat-shock?
2. **Voice** — Sounds like a human, not a brand account?
3. **Payoff** — Reader learns/feels/laughs by the end, or just promo?
4. **Length** — Right for platform (LinkedIn 1200ch, X 280, IG long-form ok)?
5. **CTA / next step** — Comment, share, save, click — pick ONE?

**Code (rubric):**
1. **Correctness** — Does it actually do what the spec says?
2. **Edge cases** — Handles empty input, null, network failure, malformed data?
3. **Readability** — Would a junior eng understand it without comments?
4. **Cohesion** — Single responsibility, no random helpers stuffed in?
5. **No dead weight** — No unused imports, no defensive code that can't trigger?

**Marketing copy (rubric):**
1. **Audience-first** — Reads as "you" not "we"?
2. **Specificity** — Names a real outcome, not "drive growth"?
3. **Voice** — Sounds like a person who'd say this out loud?
4. **Pain-aware** — Names a tension the reader recognizes?
5. **No corporate filler** — No "leverage", "synergy", "ecosystem", em-dash filler?

**Proposal / pitch (rubric):**
1. **Problem framing** — Reader nods at the first paragraph?
2. **Solution clarity** — Could the reader explain it back in 1 sentence?
3. **Proof** — Past results that match this prospect's situation?
4. **Pricing transparency** — Number is visible, not "let's discuss"?
5. **Decision-ready** — Reader knows the next step + when to commit?

**Design (rubric):**
1. **Hierarchy** — Eye knows where to land first, second, third?
2. **Whitespace** — Breathes, or every pixel screams?
3. **Contrast / accessibility** — Text passes WCAG AA at minimum?
4. **Consistency** — Same spacing scale, same font sizes, same radius?
5. **Distinctiveness** — Wouldn't pass as generic AI output / generic template?

### 3. Score honestly

For each axis, output:
- Score 1-10
- One sentence on WHY that score
- If <7, specific fix (not "improve X" — give the actual rewrite or change)

**Don't fudge.** If the average is below 6, say so clearly. The user explicitly
asked for honest critique. Giving a fake 8 is a failed gate.

### 4. Output format

```
QUALITY GATE — <type>

Overall: <avg>/10  →  <SHIP / DON'T SHIP / SHIP AFTER FIXES>

Axis scores:
  <Axis 1>           : <score>/10  — <one-line reason>
  <Axis 2>           : <score>/10  — <one-line reason>
  <Axis 3>           : <score>/10  — <one-line reason>
  <Axis 4>           : <score>/10  — <one-line reason>
  <Axis 5>           : <score>/10  — <one-line reason>

Top 3 issues to fix before ship:

1. <Specific issue> — <exact fix or rewrite>
2. <Specific issue> — <exact fix or rewrite>
3. <Specific issue> — <exact fix or rewrite>

Verdict: <one sentence — ship, fix-then-ship, or back-to-drawing-board>
```

### 5. Verdict thresholds

- **Average ≥ 8.0** → SHIP. Mention any axis below 7 as "consider if time."
- **Average 6.5 – 7.9** → SHIP AFTER FIXES. List the top 3 fixes; the user
  decides whether to apply them all or ship now.
- **Average < 6.5** → DON'T SHIP. The piece needs a rework, not a polish.

## Hard rules — never violate

1. **Never score 10/10.** Real work always has something to improve. 10 means
   you didn't look hard enough.
2. **Never average above 9.5 unless every axis is genuinely 9+.** No "rounding up
   to look polite."
3. **"Looks fine" / "Good overall" is a failed gate.** Pick a score, defend it.
4. **If you score something high, name what specifically is good** — same
   evidence standard you'd use for low scores.
5. **No hedging.** "Maybe consider…" / "might want to…" → just say "change X to Y."

## Common patterns

### Pre-send check on a cold email
```
/quality-gate ./drafts/cold-email-to-acme.md --type email
```

### Last pass on a landing page before deploy
```
/quality-gate https://your-site.com/landing --type landing
```

### Code review before PR
```
/quality-gate ./src/checkout.ts --type code
```

### "Would you ship this?" on a proposal
```
/quality-gate ./proposals/regal-nails-q3.md --type proposal
```

## Pairs well with

- `counterargument` — quality-gate scores the artifact; counterargument stress-tests
  the strategy behind it. Use both before a high-stakes ship.
- `cro-audit` — for landing pages, run quality-gate first (fix obvious gaps),
  then cro-audit (conversion-specific deeper dive).
- `marketing-context` — quality-gate reads MARKETING.md to know what "on-brand"
  means for the user's voice rubric.

## What this is NOT

- **Not a thumbs-up generator.** If the user wants validation, they should ask
  someone else. This is the cynical friend.
- **Not a security review.** Use `security-review` for that.
- **Not a typo checker.** That's any spellchecker. quality-gate is about substance.
- **Not opinionated about taste alone.** It scores against measurable axes; pure
  "I don't like the color" goes through `claude-design`, not here.
