---
name: hero-section
description: |
  Design or redesign just the HERO section of a website. Generates 4 distinct hero variations (outcome-led, proof-led, fear-led, editorial-bold-animated) for A/B picking. Hero is the most-iterated section — this skill exists to focus iteration cost on the section that matters most.

  Triggers on: "/hero-section", "redesign the hero for [project]", "give me 3 hero variations", "give me 4 hero variations", "the hero is weak — fix it".
---

# hero-section skill

Surgical skill for the highest-leverage section of any page.

**ALWAYS READ FIRST:** `~/.claude/skills/_shared/viktor-patterns.md` — for the editorial-bold-animated variant template, exact prompts, and code patterns (reverse-loop video, magnetic mouse-follow, preloader).

**Reuses:** `/claude-design` scripts + `_shared/viktor-patterns.md`. **Adds:** 4-variation generation discipline (3 angles + 1 visual style).

## Why this is its own skill

Per article 09 + 10, A/B variations of the hero is one of the 3 validation prompts. Per article 10's burn-rate analysis, hero iteration is where most quota gets burned. Isolating hero work avoids touching the rest of the page mid-iteration.

## The 4 variations

Every hero takes one of these. The skill generates one variation per type so user can pick:

1. **Outcome-led** — promise the after-state. *"Your dealer portal, finally modern."*
2. **Proof-led** — show the receipt up front. *"238 reviews. Zero website. Now this."*
3. **Fear-led** — name what they're losing. *"Your competitor's site looks like 2014. Yours doesn't have to."*
4. **Editorial-bold-animated (Viktor style)** — massive uppercase typography over a dark canvas with a reverse-looping hero video, magnetic CTA. *Auto-included whenever Viktor mode is ON for the project (see `_shared/viktor-patterns.md` for the decision rule).*

The first three vary the *angle*. The fourth varies the *visual style* — pair it with whichever angle the user picked. So the user effectively chooses BOTH an angle (1/2/3) AND optionally the editorial-bold visual treatment (4 layered on top).

If Viktor mode is OFF for the project (service trades, family-mass-market), skip variation 4.

## Workflow

### Step 1 — Inputs (one bundled question)

- **Which project / page?** (controls brand DESIGN.md + audience)
- **What's the page goal?** (so the hero supports it)
- **Existing hero to redesign?** (paste URL or screenshot) OR **fresh build?**
- **Aspect ratio?** Desktop full-bleed (16:9) / mobile portrait (9:19.5) / both

### Step 2 — Generate 3 or 4 variations in ONE Claude Design session

**If Viktor mode is OFF for this project (service trades, family-mass-market):** generate 3 angle variations only.

**If Viktor mode is ON (creative class, premium, tech, your agency's own — see `_shared/viktor-patterns.md`):** generate all 4. The 4th is the editorial-bold-animated visual style applied on top of whichever angle the user picks.

```
Generate [3 or 4] hero section variations for [PAGE/PROJECT]. Same brand (uploaded DESIGN.md), same primary CTA, same audience.

Variations 1-3 differ only by ANGLE:
1. **Outcome-led** — headline promises the after-state. Visual: aspirational future.
2. **Proof-led** — headline names a specific real number / receipt. Visual: the receipt.
3. **Fear-led** — headline names what user is losing right now. Visual: the cost of inaction.

[ONLY IF VIKTOR MODE ON, include this:]
4. **Editorial-bold-animated (Viktor style)** — same brand, but the visual treatment shifts:
   - Massive uppercase sans-serif headline (clamp 4rem-14vw-14rem, weight 900, letter-spacing -0.04em, line-height 0.9)
   - Italic serif tagline below (Playfair-style, ~25% size of headline)
   - Plain pure black canvas (#000)
   - 16:9 hero rectangle with a looping video focal element (Higgsfield Kling 3.0, 12s, 1080p, "for website perfect loop")
   - Reverse-loop pattern (no jump-cut at loop point — see `_shared/viktor-patterns.md` §1)
   - Magnetic mouse-follow on the primary CTA
   - Pre-generate the looping video via `/higgsfield:generate use kling_3_0 12 seconds 1080p` BEFORE designing — paste the video URL into the design

For each variation:
- Eyebrow (optional — 6-12 char letterspaced micro-tag)
- Headline (6-12 words max)
- Subhead (one sentence, the explainer)
- Primary CTA (same exact label across all variations)
- Hero visual treatment (specific — photo / video / illustration / typography-only / screenshot)

Lay them out side-by-side. Same brand throughout. Use Tweaks panel — don't re-prompt for each.
```

### Step 3 — User picks one

Surface the variations. User says "go with proof-led" / "outcome-led" / "fear-led" / "editorial-bold" or specifies a hybrid like "proof-led with editorial-bold visual treatment."

If user can't decide → recommend:
- **Proof-led** when there's a real number to use
- **Fear-led** for cold traffic
- **Outcome-led** for warm traffic / aspirational brand
- **Editorial-bold-animated (Viktor)** when the brand is creative-class and the wow-factor is more important than fast conversion (portfolio, agency demo, premium service launch)

### Step 4 — Polish the chosen variation

Tell Claude Design: "Save the 3 variations as a branch. Now polish variation [N] to final quality. Add motion on the CTA, refine type hierarchy, and generate the 390px / 768px / 1440px versions."

### Step 5 — Export → drop into existing page

Hero section export goes to:
- client demo: replace existing `<section class="hero">` block in `clients/<slug>/index.html`
- your-agency.com homepage: REQUIRES EXPLICIT CONFIRM (sacred file)
- Standalone landing page: integrate into `/lp/<slug>/`

Always run a Playwright smoke test on mobile + desktop after replacement.

## Anti-patterns to refuse

- **"Generate 10 hero variations"** — push back. 3 angles cover the strategic space; 10 is just decoration.
- **"Make the hero pop"** — vague, ignored. Ask what specifically isn't working — typography? imagery? hierarchy? CTA visibility? answer THAT.
- **"Try a totally different vibe"** — that's a brand change, not a hero change. Route to `/website-design` if so.

## Hard rules

- Same CTA across all 3 variations. The CTA isn't the variable — the angle is.
- Same brand colors / typography. Variations test ANGLE, not BRAND.
- Each variation must be a complete hero (headline + subhead + CTA + visual). No half-finished alternatives.
