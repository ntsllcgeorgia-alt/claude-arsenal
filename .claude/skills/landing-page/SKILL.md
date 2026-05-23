---
name: landing-page
description: |
  Design a single-goal conversion-focused landing page (waitlist, lead-gen, product launch, ad-driven, sales). One CTA, one promise, one decision. NOT a multi-section client demo (use /website-design for those).

  Triggers on: "/landing-page", "build a landing page for [thing]", "design a waitlist page", "design a sales page for [product]", "build a lead-gen page".
---

# landing-page skill

Specialized child of `/website-design`. Pre-loads conversion-focused single-page templates.

**Reuses:** all `/claude-design` scripts + `/website-design` patterns.

## When to invoke (vs /website-design)

| Need | Use |
|------|-----|
| Single-goal page with ONE CTA (waitlist, lead-gen, product launch, ad LP) | **/landing-page** |
| Multi-section client demo (Example Client-style with reviews + gallery + about + visit) | `/website-design` |
| Just a hero section to A/B test | `/hero-section` |

## The single-goal rule

Every landing page must answer ONE question for ONE audience with ONE next step. If the user describes "and we also want to show the team and a blog and...", redirect: "That's a website. Use `/website-design`. Landing pages convert because they don't compete with themselves."

## Workflow

### Step 1 — Lock the goal (one bundled question)

- **Single goal?** Waitlist signup / book a call / buy now / download / ad LP for paid traffic
- **Audience?** (Same depth as `/claude-design`)
- **One promise?** What outcome does the user get if they take the CTA?
- **One CTA?** Exact button label
- **Brand source?** Existing DESIGN.md / scrape URL / from scratch

### Step 2 — Generate / locate DESIGN.md

Same as `/claude-design`.

### Step 3 — Build the prompt — landing-page-specific structure

```
Build a single-goal landing page for [PROJECT].

Goal: [one specific conversion action — e.g. "join waitlist", "book a 15-min call"]
Audience: [who]
Promise: [what they get]

Sections (every section must support the goal — cut anything that doesn't):
1. Hero — [headline = the promise, subhead = the proof, primary CTA = the goal]
2. Three proof points — [why this is real / safe / better]
3. Social proof — [logo bar, count, testimonial, screenshot — pick one, not all]
4. How it works — [3 steps max]
5. FAQ — [3-5 objection-killers]
6. CTA repeat — [same CTA, sticky on scroll]
7. Footer — [legal only, minimal]

Content (real, not placeholder):
- Headline: "[exact text]"
- Subhead: "[exact text]"
- Primary CTA: "[exact label]"
- Three proof points: "[bullet 1]", "[bullet 2]", "[bullet 3]"
- FAQ: "[Q + A x3-5]"

Constraints:
- Use brand from uploaded DESIGN.md
- Mobile-first, single column
- Primary CTA must be visible at every scroll position (sticky or repeated)
- NO secondary navigation. NO links to "About" or "Blog" or anything else.
- Page weight under 1.5MB
- Avoid: lorem ipsum, multiple competing CTAs, stock-photo-people, "premier/professional/trusted" cliché
- Include: Open Graph meta tags, favicon, viewport meta
```

### Step 4 — Iteration coaching

Same as `/website-design`, plus:
- **"Is the goal clear in 5 seconds?"** — squint test the hero. If a first-time visitor can't tell what action to take, the headline or CTA is wrong.
- **"What if I removed this section?"** — for every section, ask if removing it would hurt conversion. If no, cut it.

### Step 5 — Validation

```
Squint test: at 50% blur, can a first-time visitor identify the single action they should take? If not, name the fix.
```
```
Generate desktop + mobile + above-the-fold-only versions. Surface what's visible without scrolling.
```
```
Suggest 2 hero variations: outcome-led vs proof-led vs fear-led. Same single CTA each time.
```

### Step 6 — Export & deploy

Default deploy: `_repos/launch-and-manage/lp/<slug>/` → live at `your-agency.com/lp/<slug>/`

For paid-traffic landing pages, append `?utm_source=...` tracking template.

## Hard rules

- **One CTA only.** Multiple CTAs = no CTA. If user insists on two, ask which is more important. The other becomes a tertiary text link.
- **No primary navigation.** Landing pages don't have nav menus. Only logo (back to root) + the single CTA.
- **Page weight under 1.5MB.** Run a weight check before deploy.
- **Open Graph tags required.** Every LP gets shared. Make the share preview not embarrassing.
