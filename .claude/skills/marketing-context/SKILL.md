---
name: marketing-context
description: |
  Generate a MARKETING.md file for a project — a single source of truth that every other marketing skill reads BEFORE acting. Captures product overview, ICP, personas, pain points, switching forces, competitive landscape, objections, customer language (verbatim), proof points, brand voice, and goals. Foundation for /cro-audit, /switching-forces, /headline-writer, and any cold-outreach work.

  Triggers on: "/marketing-context", "build marketing context for [project]", "create MARKETING.md for [client]", "I need a marketing brief for [thing]", "study this product before writing copy".
---

# marketing-context skill

The single most-important file in any marketing workflow. Every other marketing skill loads this BEFORE writing a single word. Without it, output is generic. With it, output knows the ICP, objections, proof points, and the customer's exact words.

Codifies the `product-marketing-context.md` pattern from playbook article 16.

---

## Why this matters

> "The key word is customer language. Verbatim words from real customers — pulled from interviews, reviews, support tickets — are worth more than any polished internal description because they reflect how customers actually think and talk."

A good MARKETING.md replaces a marketing consultant's first week of discovery work. It's the foundation that lets every other skill operate at expert level.

---

## Workflow when invoked

### Step 1 — Identify the project

Ask once:
- **Which project?** (your agency, NTP, TPP, your client mobile app, a client demo, new project)
- **What's available to read?** (existing landing page URL, README, brand docs, customer reviews, interview transcripts, support tickets, social comments)
- **Is there an existing MARKETING.md?** (if yes — refresh; if no — draft from scratch)

### Step 2 — Read everything

Pull from every available source:
- README + product docs
- Landing page HTML (if URL provided)
- Brand assets folder
- Existing CLAUDE.md (project rules)
- Customer reviews (Google, IG comments, support emails)
- Competitor pages (if listed)
- Past social posts / outreach DMs (for verified voice)

If a URL is provided, scrape it via:
```
python $HOME/.claude/skills/claude-design/scripts/scrape_brand_to_design_md.py <URL> <output.json>
```

### Step 3 — Draft MARKETING.md

Use this exact structure. Fill every section. Mark gaps as `[NEEDS INPUT]` rather than inventing.

```markdown
# [Project Name] — Marketing Context

## Product Overview
[1-2 sentences. What it is, who it's for, what outcome it produces.]

## Core Value Proposition
[The one-sentence promise. Specific, measurable, customer-language.]

## Target Audience / ICP
**Primary:** [who specifically — role, company size, geo, life stage]
**Secondary:** [next-tier audience]
**NOT for:** [explicit exclusions — saves wasted spend]

## Personas
### Persona 1: [Name]
- **Role / context:** [what they do]
- **Job to be done:** [the outcome they're hiring this for]
- **Day-in-the-life:** [where this product fits in their workflow]
- **Trigger to act:** [what makes them search for a solution]

[Repeat for 1-3 personas total]

## Pain Points (verbatim where possible)
- [Quote from a real customer/review]
- [Quote]
- [Quote]

## Switching Forces (Push / Pull / Habit / Anxiety)
- **Push** (what's frustrating about current state): [specific frustrations]
- **Pull** (what's attractive about us): [our hooks]
- **Habit** (what keeps them stuck): [status quo bias forces]
- **Anxiety** (fears about switching): [cost / complexity / risk]

## Competitive Landscape
| Competitor | Their angle | Our differentiator |
|------------|------------|---------------------|
| [Comp 1] | [their pitch] | [why we're different] |
| [Comp 2] | [their pitch] | [why we're different] |

## Common Objections
- **"It's too expensive"** → [response with proof]
- **"I don't have time to switch"** → [response]
- **"I tried [competitor], didn't work"** → [response]
- [3-5 more]

## Customer Language (verbatim)
Real phrases customers use — pulled from reviews, IG comments, support tickets, sales calls. NOT internal marketing-speak.

- "[exact quote]"
- "[exact quote]"
- "[exact quote]"

## Proof Points
- **Social proof:** [reviews count, ratings, testimonials, customer logos]
- **Quantitative proof:** [hard numbers — "238 reviews", "$X processed", "Y customers"]
- **Authority proof:** [press, partnerships, certifications]

## Brand Voice
- **Tone:** [3-5 specific adjectives]
- **Forbidden words/phrases:** [no "synergy", no "leverage", no "curated"]
- **Reference voices:** [example brands or writers we model]

## Current Goals & Success Metrics
- **Primary goal this quarter:** [specific outcome]
- **Primary metric:** [what number defines success]
- **Guardrail metrics:** [what we don't want to break]
- **Decision frequency:** [how often we revisit]

## Recent Wins to Quote
- [Real shipped result + date — for use in social proof, case studies, outreach]

---

*Last updated: [date] — refresh after every customer interview, win, or major positioning shift.*
```

### Step 4 — Confirm + correct

After drafting, ask user:
> "I've drafted MARKETING.md based on [sources read]. What needs correcting? What's missing? Specifically: are the customer-language quotes real (from actual reviews/comments), or did I have to infer them?"

The user's correction pass is what makes this file worth ingesting forever. Don't skip it.

### Step 5 — Save + signal downstream skills

Save to `<project-root>/MARKETING.md`. Add a note in the project's CLAUDE.md (if exists) pointing to this file:

```markdown
## Marketing context
See `MARKETING.md` for ICP, personas, switching forces, customer language, and brand voice. Every marketing-related skill should read this file FIRST.
```

---

## Per-project storage

| Project | Save to |
|---------|---------|
| your agency | `your-agency/MARKETING.md` |
| your client | `D:/Projects/ntp-mobile-app/MARKETING.md` (mobile app) + a separate one in your client web folder if different |
| your client | `bc-builder/MARKETING.md` |
| Client demo | `your-agency/clients/<slug>/MARKETING.md` |

---

## Hard rules

- **Never invent customer-language quotes.** If we don't have real reviews to pull from, mark as `[NEEDS INPUT — collect verbatim quotes from reviews]`. Inventing quotes destroys the file's value.
- **Never skip the user-confirmation pass.** A MARKETING.md that wasn't reviewed is a MARKETING.md full of plausible-sounding hallucinations.
- **Always refresh after major positioning shifts.** Stale MARKETING.md is worse than none — it gives wrong answers with confidence.
- **Don't pad.** If a section has no real input, mark `[NEEDS INPUT]`. Better short and accurate than long and wrong.
