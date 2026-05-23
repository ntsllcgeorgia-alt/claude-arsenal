# DESIGN.md template

This is the structure every DESIGN.md should follow.  your agency template at `your-agency/templates/DESIGN.md` is a good real-world example to emulate.

When generating, fill every section. Flag anything genuinely missing as `[NEEDS INPUT]` rather than inventing.

---

```markdown
# [Project Name] — Design System

## Brand Promise (the feeling every output should produce)
One sentence. The specific reaction the target user should have.
Example: "A 47-year-old salon owner sees this and thinks 'wait — that's MY business. How much does this cost?'"

## Audience Profile
- Who specifically (age, role, location, income/scale band)
- What they currently use / are tired of
- Their buying motivator (pain or vanity?)

## Voice & Copy
### Headlines
- Word count rule
- 2-3 GOOD examples
- 2-3 BAD examples (real anti-patterns to avoid)

### Subheads / Body
- Tone, voice, reading level
- Active vs passive
- Real-numbers vs generic-claims rule

### CTAs
- Verbs only
- Specific actions, not "Learn more"
- 3 examples

## Typography
- Display font (with weight and use case)
- Body font (with weight and use case)
- Letter-spacing / leading rules
- Italic usage (if any)

## Color
### Primary palette
- Background: hex + name
- Foreground: hex + name
- 1-2 accent colors with hex + named role

### Allowed gradients / overlays
List explicitly. If none, say none.

### Forbidden colors
Common colors that violate the brand (e.g. "no pure black, no neon green").

## Layout & Spacing
- Section padding rule (desktop and mobile)
- Max content width
- Grid system (12-col, 8-col, asymmetric, etc.)
- Vertical rhythm

## Imagery
- Photography style (editorial / lifestyle / product / abstract)
- Illustration style (if any)
- Image treatment (color grading, vignettes, overlays)
- Forbidden imagery (stock photo aesthetics, etc.)

## Components / Patterns
Common UI elements with exact specs:
- Buttons (primary, secondary, ghost) — radius, padding, hover
- Cards — radius, border, hover behavior
- Forms — input style, label position, validation states
- Navigation — fixed/sticky, blur, behavior

## Motion
- Animation philosophy (subtle vs expressive)
- Transition durations and easing curves
- Hover effects (allowed)
- Loading states

## Do-Not-Use List
Hard rules. Words, colors, patterns, photography styles, copy clichés that should never appear in output.
- "Synergy / leverage / ecosystem / curated / unleash"
- Stock photos with people in suits high-fiving
- Lorem ipsum (use real-feeling placeholder copy)
- Etc.

## Reference Examples
Links or filenames of past work / competitors / aspirational sites that match this brand.
```

---

## Generation rules (when Claude is producing this from assets)

1. **Read every file** in the source folder before writing — don't sample.
2. **Pull literal hex values** from logos and graphics. Don't approximate.
3. **Quote real copy** from existing materials (with light cleanup) — don't invent voice.
4. **Flag missing fields** explicitly with `[NEEDS INPUT — got nothing for this]`. Don't pad.
5. **Keep it under 400 lines.** If it's longer, you're hallucinating detail.
