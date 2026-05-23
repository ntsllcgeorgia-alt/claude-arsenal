---
name: claude-design
description: |
  End-to-end Claude Design workflow automation. Runs the full play from "I have an idea" to "shippable design + code handoff" — generates DESIGN.md from existing brand assets, copies the perfect 4-input prompt to clipboard, opens claude.ai/design with project pre-named, walks through inline iteration, runs the 3 validation prompts before export, and routes handoff bundle to Claude Code in the right project folder.

  Triggers on: "/claude-design", "let's design [a thing]", "use claude design for [project]", "design a [landing page / pitch deck / app screen / one-pager / prototype]".
---

# Claude Design Skill

Codifies articles 06, 08, 09 from the playbook into a single executable workflow.

**Source articles (read on demand if user references "the articles"):**
- `claude-playbook/articles/06-claude-design.md` — workflow basics + DESIGN.md hack
- `claude-playbook/articles/08-claude-design-masterclass.md` — handoff bundles + iteration patterns + limitations
- `claude-playbook/articles/09-claude-design-advanced.md` — getdesign.md + 4-input formula + validation prompts
- `claude-playbook/articles/10-claude-design-burn-rate.md` — token economics + 3 editing surfaces + Opus/Sonnet switching

---

## What this skill does (vs doesn't)

**Automates:**
- DESIGN.md generation from a URL, a folder of assets, or getdesign.md
- 4-input prompt construction (goal · layout · content · constraints)
- Opening claude.ai/design in browser with prompt pre-copied to clipboard
- Validation prompt set (WCAG / responsive / A/B variations)
- Handoff bundle → Claude Code routing
- **Image generation via Higgsfield Nano Banana 2** (for assets that should NOT come from Claude Design — branded product photos, hero stills with reference images, character-consistent series)

**Cannot automate (user does in browser, skill walks them through):**
- Pasting prompt and hitting Generate at claude.ai/design
- Inline edits / comments on the canvas
- Clicking Export

The friction around the manual steps is reduced to seconds.

## Image generation backends — pick the right one

| Backend | When to use | Script |
|---------|------------|--------|
| **Claude Design** (claude.ai/design, Opus 4.7 vision) | Layouts, screens, slide decks, full UI mockups | (manual via browser) |
| **Higgsfield Nano Banana 2** ( account, hardcoded keys) | Branded product photography (truck parts, stills with reference images), character-consistent series, photorealistic mockups | `scripts/generate_higgsfield_image.py` |
| **Imagen 4** (Gemini API) | Editorial / lifestyle stills (client demo work — Example Client, etc.) | use existing `portal-scraper/generate_*.py` |
| **Veo 3.1** (Gemini API) | Cinematic videos, hero loops, splashes (16:9 + 9:16) | use existing `portal-scraper/generate_hero_video*.py` |

**Rule of thumb:**
- "Design a screen" → Claude Design
- "Generate a product photo with these references" → Higgsfield Nano Banana 2
- "Generate a hero video" → Veo 3.1
- "Generate a brand-style still" → Imagen 4

Higgsfield's superpower is **reference images** — pass up to 3 URLs of real product photos, and Nano Banana 2 generates a new image that respects them. Critical for your clients product photography where the part has to look like THE part, not "a generic part."

---

## Quota / token economics (read this BEFORE running the workflow)

Claude Design has a **separate weekly quota** from regular Claude/Code. Author of article 10 burned 30% of Max 20x quota in ONE day. Treat it like money.

Cost-saving rules baked into this skill:

1. **Brainstorm phase happens in regular Claude, NOT in Claude Design.** Claude Design is for executing a known brief, not for figuring out what the brief should be. If the user opens this skill in "thinking out loud" mode, route them back to a normal Claude chat first to lock the spec, THEN come here.

2. **Switch models mid-session.** Opus 4.7 for the first generation (the heavy lift). Sonnet 4.6 for tweaks (no quality drop, half the cost).

3. **Reference real designs by name.** "Linear 2023 with higher density" beats "make it clean." "Modern fintech, light bone background" beats "make it minimal." Specific = one-shot. Vague = re-runs.

4. **ONE major change per prompt.** Mega-prompts only land 1-2 of the asks. Pick the highest-leverage change, ship it, then next.

5. **Watch the build live.** Claude Design has a verifier agent. If the user says "it's heading wrong" at minute 2 — STOP IT. Don't let a 10-minute wrong-path build complete.

6. **Edit in canvas, not chat, where possible.** Three surfaces:
   - **Edit tool** — click element, change text/color/sizing (cheapest, no prompt needed)
   - **Draw tool** — circle a region + comment for non-element changes
   - **Tweaks panel** — pre-built variation toggles for cover style, accents, chrome
   - Rule: if you can change it without prompting, change it without prompting.

7. **File upload cap is 30-40MB.** Don't upload long videos. Compress or extract.

8. **If the thread sprawls past ~30 turns,** export the project and reopen in a fresh session. Don't trust /clear to reset context.

9. **At ~30% weekly burn, warn the user.** Suggest finishing in fewer prompts or pausing for the weekly reset.

---

## Workflow when invoked

### Step 1 — Ask the user what they're designing

Ask ONCE, not five times:
1. **What's being designed?** (landing page / pitch deck / app screen / one-pager / prototype / social graphic)
2. **For which project?** (your agency, your client mobile app, TPP, a client demo, something new — controls where files land + which CLAUDE.md applies)
3. **Brand source?** (existing folder of assets / scrape a URL / borrow via getdesign.md / from scratch)

If user gave most of this in their initial trigger ("design the your client login screen"), don't re-ask — infer and confirm in one line.

### Step 2 — Generate or locate DESIGN.md

Branch on brand source:

**A) "Existing folder of assets"** — analyze locally
Read every brand-relevant file in the target folder (logos, past slides, landing pages, brand PDFs, screenshots). Produce DESIGN.md following the structure in `templates/design-md-template.md`. Save to project folder root as `DESIGN.md`.

**B) "Scrape a URL"** — run the scraper
```
python $HOME\.claude\skills\claude-design\scripts\scrape_brand_to_design_md.py <URL> <OUTPUT_PATH>
```
The script uses Playwright + visual analysis to pull logo, colors, fonts, tone. Outputs raw scrape data; Claude then post-processes into DESIGN.md format using the template.

**C) "From getdesign.md"** — pull a brand
```
python $HOME\.claude\skills\claude-design\scripts\pull_getdesign_md.py <BRAND_NAME> <OUTPUT_PATH>
```
Names like "mastercard", "airbnb", "ferrari", "caterpillar", "patagonia". Falls back to manual instructions if the brand isn't on getdesign.md.

**D) "From scratch"** — Claude defines it conversationally
Ask 6 questions (audience, voice, mood, palette direction, typography mood, do-not-use list). Output to `DESIGN.md` in target folder.

### Step 3 — Build the 4-input prompt

Use `templates/4-input-prompt.md` as the formula. ONE prompt, locked inputs:

1. **Goal** — what's being built and why
2. **Layout** — explicit section structure
3. **Content** — actual headlines, copy, CTAs (real, not placeholder)
4. **Constraints** — tone, audience, what to avoid, format/aspect

Construct the prompt in code-fence so user can one-click copy. Also auto-copy to clipboard via `clip` (Windows).

### Step 4 — Open claude.ai/design with project pre-named

Open https://claude.ai/design in browser (PowerShell `Start-Process`). Surface a tight checklist for user:

```
Your move at claude.ai/design:
1. New Project → name it "<inferred name>"
2. Upload DESIGN.md (full path is on your clipboard)
3. Paste the 4-input prompt (already on your clipboard, just Ctrl+V)
4. Hit Generate
5. Tell me when first draft is back — say "first draft" or describe what you see
```

### Step 5 — Iteration coaching (cost-aware)

When user reports the first draft, route them to the **CHEAPEST iteration channel** that can deliver:

| User says | Use | Why cheapest |
|-----------|-----|--------------|
| "make this taller / smaller / different color" on a specific element | **Edit tool** in canvas | No prompt = nearly free |
| "this gradient feels heavy" / "this section is too busy" (region, not element) | **Draw tool** in canvas | One screenshot, one comment |
| "let me see this with a different cover style / accent / chrome" | **Tweaks panel** | Pre-built variations, cheap |
| "simplify the whole hero" / "more premium feel overall" | **Chat** (structural) | Worth the cost |
| "save this, then try a completely different approach" | **Chat with branch save** | Don't lose the good draft |

**Hard rules:**
- ONE major change per prompt. If user wants 4 things changed, ship them in 4 separate prompts.
- Always recommend the canvas tool first when applicable. Chat is the fallback, not the default.
- If user is iterating heavily, suggest switching the Claude Design model from Opus 4.7 to Sonnet 4.6 — same quality on tweaks, half the cost.

Don't iterate FOR the user. Translate their feedback into the right channel + suggested phrasing.

### Step 6 — Validate before export

Before user clicks Export, run all 3 validation prompts from `templates/validation-prompts.md`:

```
Review this for contrast and accessibility. List any WCAG 2.1 AA violations with exact fixes.
```
```
Generate desktop, tablet, and mobile versions.
```
```
Suggest 2 A/B test variations of the hero section, each with a different angle.
```

User pastes each into Claude Design chat, surfaces the response back. We fix issues in the canvas before exporting.

### Step 7 — Export + handoff

User clicks Export → choose path:
- **PDF / PPTX** — done, file saved locally
- **Standalone HTML** — drop into project folder, link from README
- **Handoff bundle** — drop in target project folder, then Claude Code takes over (see Step 8)

Skip "Send to Canva" — confirmed broken (article 09).

### Step 8 — Build with Claude Code (if handoff bundle)

Switch to a fresh Claude Code session in the target project folder (the per-folder CLAUDE.md auto-loads). Hand it the bundle:

```
Build this React Native screen / web component from the handoff bundle in <bundle-path>.
Stack constraints in CLAUDE.md (use existing library choices, no new deps).
Match the design pixel-for-pixel where it makes sense; use taste to override if dealer/audience expectation differs.
```

For your client mobile app specifically: Expo SDK 54, RN 0.81, TypeScript, React Navigation v7, Apollo Client, Zustand, React Hook Form, Montserrat. **Do not** add a new UI library mid-project.

---

## Outputs the skill always produces

- A `DESIGN.md` in the target project folder
- A 4-input prompt (in code fence, also clipboard)
- A validation checklist surfaced before export
- (When applicable) a handoff bundle imported into the right project

## Style for skill responses

- Match  preferred voice (terse, action-led, no preamble)
- Numbered checklists for every browser step
- Don't lecture about what Claude Design IS — assume he's read articles 06+08+09
- If something's broken or untestable from this side (e.g. claude.ai/design rendering), say so honestly
- Never iterate on the design FOR him — he has the taste, surface the right channel + phrasing for him to do it

## Failure modes to surface honestly

- **Browser auto-open didn't work** → give him the URL, he clicks
- **Clipboard copy failed** → drop the prompt in a code fence so he can copy
- **getdesign.md doesn't have the brand** → fall back to scrape OR build from scratch
- **claude.ai/design refuses to load** → "research preview, gradual rollout. Try in a few hours."
- **Handoff bundle has unsupported animations** → flag the limitation, suggest hand-coding that section after the rest is built
