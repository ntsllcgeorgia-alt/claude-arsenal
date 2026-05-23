---
name: cro-audit
description: |
  Run a 7-question conversion-rate audit on any landing page, client demo, or marketing site. Returns prioritized fixes (quick wins → high-impact changes → test ideas), copy alternatives, and a friction map. Use before shipping any client demo, before launching any landing page, or to diagnose underperforming pages.

  Triggers on: "/cro-audit", "audit this page for conversion", "review [URL] for CRO", "why isn't this page converting", "check the conversion rate of [page]".
---

# cro-audit skill

Codifies the CRO 7-question framework from playbook article 16.

> A page is a sequence of arguments not a collection of blocks. Audit in this exact order of impact: value proposition → headline → CTA → visual hierarchy → trust signals → objection handling → friction.

---

## When to invoke

- Before shipping any client demo (Example Client-style)
- Before launching any /landing-page output
- Before deploying any update to your-agency.com
- When a live page is underperforming and we don't know why
- After a /website-design build, before final export

---

## Workflow

### Step 1 — Identify scope

Ask once:
- **Page URL or local file path?**
- **Page type?** (homepage / landing page / client demo / pricing / about / case study)
- **Primary conversion goal?** (book call / signup / purchase / DM / download)
- **Traffic source assumption?** (cold ad / warm referral / organic / direct)
- **MARKETING.md available?** (if yes, load it for ICP + objections context)

### Step 2 — Load the page

For URLs: scrape via Playwright (use `claude-design/scripts/scrape_brand_to_design_md.py` pattern, or simpler — just fetch with WebFetch).

For local files: read the HTML/JSX directly.

For client demos in our repos: read the source file (e.g. `your-agency/clients/<slug>/index.html`).

### Step 3 — Run the 7 questions

Audit IN ORDER (each question's failure cascades to the next):

#### Q1: Value proposition — clear in 5 seconds?
> A first-time visitor should be able to answer: "What is this? Who is it for? What outcome will I get?" — in 5 seconds, without reading.

- Find the hero
- Squint test: at 50% blur, what's the message?
- Specific or vague? "Save time" = vague. "Cut weekly reporting from 4 hours to 15 minutes" = specific.

**Score:** 1-10
**Verdict:** [pass / fix needed / critical]

#### Q2: Headline — specific outcome or vague claim?
> Headlines that work follow these formulas:
> - {Achieve outcome} without {pain point}
> - Turn {input} into {outcome}
> - Never {unpleasant event} again
> - The {category} for {audience}
> - {Number} {people} use {product} to {outcome}

- Quote the existing headline
- Identify the formula (or note "none — generic")
- Suggest 2-3 alternatives in the right formula

**Score:** 1-10

#### Q3: CTA — one primary action, right copy, right placement?
> Formula: [Action Verb] + [What They Get] + [Qualifier if needed]
> ✅ "Get the Complete Checklist"
> ✅ "See Pricing for My Team"
> ❌ "Submit", "Click Here", "Learn More"

- Count CTAs (>1 primary = problem)
- Verb-led? Specific?
- Placement (above fold + repeated mid-scroll + footer)?
- Tap-friendly on mobile (≥44x44px)?

**Score:** 1-10

#### Q4: Visual hierarchy — scannable without reading?
- Are the 3 most-important things visible without reading every word?
- Eyebrow + headline + subhead + CTA pattern present?
- Section breaks clear?
- Mobile rendering reasonable?

**Score:** 1-10

#### Q5: Trust signals — present near the CTA?
- Reviews / ratings / count?
- Logos of known customers / press?
- Guarantees / money-back / no-contract language?
- Real photos > stock photos?
- Are these NEAR the CTA (not buried in footer)?

**Score:** 1-10

#### Q6: Objections — addressed before they block conversion?
> Load `MARKETING.md` objections list. For each objection, ask: is it addressed on this page?

Common objections to check:
- Too expensive → pricing transparency, ROI math, comparison
- Too complex → screenshots, video walkthrough, "no skills needed"
- Won't work for me → industry-specific examples, persona callouts
- I tried before → "here's what changed", new-format positioning

**Score:** 1-10

#### Q7: Friction — what's slowing the conversion?
- Form fields: how many? Each one is a drop-off point.
- Steps to convert: 1-step? 3-step? Each step = 30-50% drop.
- Mobile usability: does the CTA work on touch?
- Page weight / load time (>3s = problem)
- JavaScript-only critical content (AI agents + slow networks fail)

**Score:** 1-10

### Step 4 — Output the prioritized report

Use this exact structure:

```markdown
# CRO Audit — [Page Name / URL]

**Audit date:** [date]
**Page type:** [type]
**Primary goal:** [conversion action]
**Overall score:** [average of 7 questions] / 10

## Quick Wins (do in next 30 minutes)
- [Specific change + why + impact estimate]
- [Specific change]
- [Specific change]

## High-Impact Changes (do this week)
- [Change + before/after copy + impact estimate]
- [Change]
- [Change]

## Test Ideas (A/B test next sprint)
- [Hypothesis + variant + metric to track]
- [Hypothesis]

## Copy Alternatives
### Headline
- Current: "[exact text]"
- Variant A (outcome-led): "[text]"
- Variant B (proof-led): "[text]"
- Variant C (fear-led): "[text]"

### Primary CTA
- Current: "[text]"
- Variant A: "[verb-led, specific]"
- Variant B: "[different angle]"

## Friction Map
- [Specific friction point + fix]
- [Friction point + fix]

## Dependencies
- [Anything that needs to be true before fixes can ship — e.g. "needs new hero photo from /truck-product-image"]
```

### Step 5 — Save + apply

Save to `<page-folder>/_CRO_audit_YYYY-MM-DD.md` for historical tracking.

If the user wants to apply the fixes, hand off to `/website-design` or `/hero-section` skill with the audit findings as input.

---

## Worked example — your-agency.com homepage

If invoked on your-agency.com:
- Q1: pass (PROOF-led tagline + hero is clear)
- Q2: 8/10 — "We build it. We run it." is good Pull, could add Push/specificity
- Q3: 9/10 — single primary CTA "DM @yourhandle" is strong
- Q4: 9/10 — hero has eyebrow + tagline + subhead + 2 CTAs cleanly
- Q5: 7/10 — Example Client embedded as proof, could add review count, founder photo
- Q6: 6/10 — pricing addresses cost objection well, but missing "is this for me" objection (city-by-city, industry-by-industry persona callouts)
- Q7: 8/10 — fast load, mobile responsive, splash plays once

Quick wins:
- Add "238 reviews · 12 years · 0 websites" headline above the Example Client iframe (hammers Push)
- Add "Made in Weatherford. By a guy in Weatherford." as eyebrow on About section (geographic specificity)

---

## Hard rules

- **Always audit in the 7-question order.** A pass on Q3 means nothing if Q1 fails — visitors leave before they see the CTA.
- **Score honestly.** Don't grade on a curve. 7/10 isn't "good" — it's "needs work."
- **Quick wins must be doable in <30 min.** If it requires a redesign, it goes in High-Impact, not Quick Wins.
- **Always quote the existing copy before suggesting alternatives.** Don't paraphrase — exact text only.
- **Run a Playwright smoke test if recommending mobile fixes.** Don't claim mobile is broken without seeing it on a 390px viewport.
