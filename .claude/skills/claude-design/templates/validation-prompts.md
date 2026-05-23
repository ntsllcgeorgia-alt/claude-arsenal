# Validation prompts (run BEFORE Export)

Three commands to paste into the claude.ai/design chat after the design is "almost done." Catches the issues that cost a redesign later.

From article 09.

---

## 1. Accessibility / WCAG audit
```
Review this design for contrast and accessibility. List any WCAG 2.1 AA violations with exact fixes — name the element, the current contrast ratio, and the corrected color hex that brings it into compliance. Also flag missing focus states, missing alt text, and tap targets under 44x44px.
```

**Why this matters:** Claude Design's default palette work usually produces gorgeous-but-illegal contrast on pale text over saturated backgrounds. Catch before stakeholders see it.

---

## 2. Responsive variants
```
Generate desktop (1440px), tablet (768px), and mobile (390px) versions of this design. Surface any layout breaks where content overlaps, text wraps unfortunately, or touch targets become too small. Adjust each version to look intentional at that size, not just shrunk.
```

**Why this matters:** A design that only looks great at desktop ships broken. Force the responsiveness pass NOW, while context is fresh, not after handoff.

---

## 3. A/B test variations of the hero
```
Suggest 2 A/B test variations of the hero section, each with a clearly different angle. For each variation: (1) name the angle in 4 words or fewer, (2) propose alternative headline + subhead + CTA copy, (3) describe what visual treatment is different, (4) name the audience segment it targets best.
```

**Why this matters:** Even when shipping v1, having 2 ready alternates means you can split-test from day one without re-engaging the workflow.

---

## When to skip these

If the asset is throwaway / internal-only / will never be seen by an external user — skip 1 and 2. Run 3 anyway; it's quick.

For pitch decks: replace prompt 2 with "Generate a print-friendly PDF version where every slide reads cleanly when printed in grayscale on a single page."

For mobile app screens: replace prompt 2 with "Generate iPhone SE (smallest), iPhone 15 Pro Max, and Pixel 7 versions. Surface any layout that breaks at the smallest size."
