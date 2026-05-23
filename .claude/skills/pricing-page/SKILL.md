---
name: pricing-page
description: |
  Design a pricing page or pricing section that actually converts. Tier comparison, anchored "Most Popular" callout, one-time vs recurring, FAQ for objections, decision-supporting layout. For your tiers ($497/$1,497/$3,997 + $4,997 build), client SaaS pricing, agency packages.

  Triggers on: "/pricing-page", "design the pricing page for [project]", "redesign our pricing tiers", "build a pricing comparison".
---

# pricing-page skill

Pricing pages decide deals. This skill handles the patterns that actually convert.

**Reuses:** `/claude-design` scripts.

## When to invoke

User needs:
- A standalone pricing page
- A pricing section inside a longer page
- A tier comparison redesign
- An "anchor + middle = winner" pricing layout

## The pricing decision arc

Visitors who land on a pricing page are warm. They want to compare and pick. The page exists to:
1. **Anchor** — the highest tier sets the perceived value of everything below
2. **Highlight the winner** — "Most Popular" callout pre-decides for indecisive visitors
3. **De-risk** — no contracts / cancel anytime / money-back / proof
4. **Kill objections** — FAQ at the bottom answers the 5 questions people email after seeing the prices

Skip any of these and conversion drops.

## Workflow

### Step 1 — Inputs (one bundled question)

- **How many tiers?** 2 / 3 / 4 (3 is best for most cases — anchor + winner + entry)
- **Tier names + prices** — exact (e.g. Spark $497 / Engine $1,497 / Empire $3,997)
- **Most Popular?** — which tier gets the callout (usually middle)
- **One-time builds?** — separate row beneath recurring tiers
- **Toggle?** — monthly / annual toggle if applicable (skip if recurring-only)
- **Trust signals** — what de-risks? (no contracts, cancel anytime, money-back, X-day trial)

### Step 2 — Build the prompt

```
Build a pricing section for [PROJECT].

Audience: warm prospects deciding between tiers
Tone: confident but not pushy — clear, comparable, easy to scan

Layout (top to bottom):
1. Eyebrow + section title — "Pricing" / "Three tiers. Pick yours." or similar
2. Subhead — one sentence killing the biggest objection ("No contracts. Cancel anytime.")
3. Tier grid — 3 columns desktop, stacked on mobile. Middle tier visually elevated:
   - Tier name (small, letterspaced)
   - Price (large, prominent)
   - Cadence (/mo, /yr)
   - Description (one sentence)
   - Features list (5-7 max — the marginal feature that justifies the upsell, ordered ascending in tier value)
   - CTA button (same label across tiers, same action, same color)
4. (Optional) One-time row — for builds / setup fees, separate from monthly tiers
5. (Optional) Toggle — monthly / annual with annual savings badge ("Save 20%")
6. FAQ — 5-7 questions covering: how does cancellation work, what's not included, what if I outgrow this tier, can I switch tiers, etc.
7. Footer CTA — "Still not sure? Book a 15-min call" with contact link

Content (real):
- Each tier with exact name, price, cadence, description, 5-7 features (real, not placeholder)
- "Most Popular" callout on the middle tier
- Real FAQ (write the actual questions and answers — don't placeholder)

Constraints:
- Use brand from uploaded DESIGN.md
- Mobile-first; tier cards stack on mobile, side-by-side on desktop
- Featured tier visually emphasized (border accent + scale 1.02 + "Most Popular" badge)
- Same CTA across all tiers (avoid "Buy" on one and "Contact us" on another — confusing)
- WCAG AA contrast on all text including price numbers
- Avoid: striking out higher prices ("$2000 ~~$5000~~"), "BEST VALUE!" stickers in primary colors, more than 7 features per tier
- Include: clear cadence, real numbers, FAQ, trust signals near CTA
```

### Step 3 — Iteration coaching

- **"Tiers feel cramped"** → ask Claude Design: "Increase column padding to 32-40px and reduce features per tier to 5 max."
- **"Featured tier doesn't pop enough"** → "Use brand accent border + slight scale + soft glow on the featured tier card. Don't change colors of others."
- **"Need a 4th tier"** → push back. 4 tiers = decision paralysis. Suggest moving the 4th into the FAQ ("Need more? We do custom — book a call").

### Step 4 — Validation

```
Squint test: at 50% blur, can a visitor immediately see the 'Most Popular' tier? If not, the visual emphasis isn't strong enough.
```
```
Comparison table view: generate a feature-by-feature comparison table layout for the same tiers. Useful for visitors who scan vs read.
```
```
Generate the mobile (390px) version specifically. Tier cards must stack with the featured tier ON TOP, not in the middle, so it's seen first.
```

### Step 5 — Export

Pricing pages live as either:
- Standalone: `/pricing/` — full pricing-only page
- Section: integrated into the homepage / landing page (replace existing `<section id="pricing">`)

For your agency specifically, the pricing section already exists at homepage `#pricing` — the your agency CLAUDE.md says homepage = sacred. This skill REPLACES only the pricing section block, not the surrounding page.

## Hard rules

- **3 tiers is the sweet spot.** 2 = no anchor. 4+ = decision paralysis. Push back on requests for more.
- **Featured tier in the middle.** Anchoring works because the eye goes middle-first.
- **Same CTA label across tiers.** "Get started" / "Get started" / "Get started" — not "Try" / "Buy" / "Contact us."
- **FAQ kills objections — don't skip it.** Average pricing page without FAQ converts ~40% lower than with one.
- **Show the cadence.** "$497" alone is ambiguous. "$497/mo" is clear.
