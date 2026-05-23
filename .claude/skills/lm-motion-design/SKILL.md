---
name: lm-motion-design
description: |
  Generate animated motion-graphic clips for your client landing pages — section dividers, logo
  reveals, data visualizations, accent loops. NOT photorealistic video — graphic / motion-design
  aesthetic.

  Use when: "/lm-motion-design", "motion graphic for [client]", "logo reveal for [project]",
  "animated divider for [section]", "data viz animation for [client]".

  Chains: higgsfield-generate (style frame via flux_2 or gpt_image_2) → kling_omni_image (motion) → ffmpeg loop.

  Output: 3-5s loopable MP4 + transparent WebM with alpha channel where possible.
---

# lm-motion-design — Animated graphics for your agency landing pages

## What this flow does

Generates a **short motion-design clip** — animated graphic, not photorealistic video — for use as:
- A section divider on a landing page
- A logo reveal / brand mark animation
- An animated data visualization (e.g. "We've served 10K customers" with the number counting up via image swap)
- An accent loop in a hero or CTA section

Different from `/lm-hero-video` (photorealistic) — this is intentionally GRAPHIC.

## Trigger phrases

`/lm-motion-design`, "motion graphic for [client]", "logo reveal for [project]", "animated divider for [section]", "data viz for [client]".

## Inputs

Required:
- **client slug**
- **purpose** — `divider`, `logo-reveal`, `data-viz`, `accent-loop`, `section-intro`
- **concept** in one sentence (e.g. "abstract gradient waves matching brand palette", "logo materializing from particle dust", "number 47 counting up to 200 with sparkle effect")

Optional:
- **palette** — read from `clients/<slug>/DESIGN.md`
- **duration** — 3s default, 2-8s range
- **aspect** — `16:9` (default), `21:9`, `1:1` (social), `9:16` (mobile)
- **needs alpha channel** — true/false (defaults true for `logo-reveal` and `accent-loop`)

## Process

1. **Read brand context** — `clients/<slug>/DESIGN.md` for palette, typography, mood.
2. **Generate the style frame** with `higgsfield generate create flux_2` or `gpt_image_2`:
   - Prompt: graphic-design language ("flat vector", "minimalist gradient", "geometric shapes", "neon outline", "particle dust") — NOT photorealistic
   - Aspect ratio per input
   - Save to `clients/<slug>/motion-<purpose>-frame.jpg`
3. **Animate it** with `higgsfield generate create kling_omni_image`:
   - Use the frame as the start
   - Motion prompt: describe the specific animation (slow zoom, particles dispersing, gradient rotation, count-up)
   - Loopable: true (set hint in prompt)
   - Duration per input
   - Save to `clients/<slug>/motion-<purpose>.mp4`
4. **Post-process with ffmpeg:**
   - Trim to clean loop boundaries
   - If `needs_alpha=true`, attempt a chroma key on solid-color background (only works for compatible motion). Save as `clients/<slug>/motion-<purpose>.webm` with alpha.
   - Compress to under 1 MB if possible (these go in landing pages, LCP matters).
5. **Drop into the client demo HTML** — if `clients/<slug>/index.html` exists, locate the appropriate section by `id` (e.g. `#hero-divider`, `#stats-section`) and insert the `<video autoplay muted loop playsinline>` tag.

## Output

```
clients/<slug>/
├── motion-<purpose>-frame.jpg   # style reference (also poster fallback)
├── motion-<purpose>.mp4         # the animated clip
└── motion-<purpose>.webm        # alpha-channel variant where applicable
```

## Quality bar

- This is GRAPHIC DESIGN, not photo-realism. If the output looks like a still photo with subtle camera move, regenerate with a more graphic prompt.
- Loopable at the boundary — no jump cut visible.
- Under 1 MB file size where possible.
- Matches client palette from DESIGN.md exactly (not "close enough").
- For `logo-reveal`: the final frame must show the logo clearly and statically — animation enters, then settles.

## Hard rules

- **Use `flux_2` or `gpt_image_2` for style frames** — these excel at graphic-design aesthetics. `nano_banana_2` is for photorealistic and will look wrong here.
- **Use `kling_omni_image` for motion** — best for stylized / non-photoreal animation.
- Never use `marketing_studio_video` for motion design — it's tuned for UGC, will fight you.
- Verify cost first. Motion design loops are usually cheap (< $0.20) but check.
- Don't generate animations that conflict with prefers-reduced-motion accessibility — provide a static poster fallback.

## Connected
- [[Higgsfield Stack]] · [[Launch & Manage]] · [[reference_higgsfield_api]]
