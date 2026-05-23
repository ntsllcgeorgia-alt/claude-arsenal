---
name: lm-cinematic-spot
description: |
  Generate a 10-15s cinematic brand spot — broadcast-quality, no presenter, premium production
  feel. For Empire-tier your clients or hero pieces.

  Use when: "/lm-cinematic-spot", "cinematic spot for [client]", "broadcast-style video for [project]",
  "premium brand film for [client]".

  Chains: higgsfield-generate (multiple still references) → cinematic_studio_2_5 / soul_cinematic → ffmpeg cuts.

  Output: 10-15s 16:9 MP4 at 1920x1080, suitable for TV / YouTube pre-roll / website hero / OOH.
---

# lm-cinematic-spot — Premium brand film flow

## What this flow does

Generates a **10-15 second cinematic spot** — multi-shot, no on-screen presenter, dramatic lighting, premium production aesthetic. Suitable for:
- The "hero film" on a high-tier client demo
- Pre-roll YouTube ads for $1,497+ clients
- Trade-show / event displays
- Empire-tier package deliverable

This is the FLAGSHIP creative output of your agency.

## Trigger phrases

`/lm-cinematic-spot`, "cinematic spot for [client]", "broadcast-style video for [project]", "premium brand film for [client]", "TV spot for [client]".

## Inputs

Required:
- **client slug**
- **brand story in one sentence** (e.g. "Example Client turns the most boring 30 minutes of your week into the part you look forward to")
- **scene count** — 2 or 3 (default 3)

Optional:
- **palette** — read from `clients/<slug>/DESIGN.md`, else dark cinematic
- **score mood** — `triumphant`, `quiet`, `mysterious`, `playful` (default `quiet`)
- **aspect** — `16:9` (default), `21:9` (cinematic letterbox)

## Process

1. **Read brand context** — `clients/<slug>/DESIGN.md`, `clients/<slug>/MARKETING.md`. Synthesize a 3-shot storyboard from the one-sentence story.
2. **Write the storyboard** to `clients/<slug>/spot-storyboard.md`:
   - Shot 1: opening visual + emotional beat
   - Shot 2: product / service in action
   - Shot 3: closing visual + brand mark
3. **Generate 1 still reference per shot** with `higgsfield generate create soul_cinematic`:
   - For each shot, generate a 16:9 still that captures the intended composition
   - Save as `clients/<slug>/shot-{N}-ref.jpg`
4. **Generate 1 video clip per shot** with `higgsfield generate create cinematic_studio_2_5`:
   - Use the corresponding still as the start frame
   - Duration: 4-5s per shot (allow for ffmpeg trim down to 3-4s per cut)
   - Save as `clients/<slug>/shot-{N}.mp4`
5. **Cut the final spot** with ffmpeg:
   - Trim each clip to its strongest 3-4s
   - Crossfade between shots (200ms)
   - Add a closing title card with the brand mark (use a still generated with text via `gpt_image_2`)
   - Optional: add royalty-free music bed if `clients/<slug>/score.mp3` exists
   - Final output: `clients/<slug>/spot.mp4` (10-15s, 1920x1080)
6. **Generate alt cuts:**
   - 6s variant for social ads
   - 30s variant for full TV spot (only if Empire tier — read `clients/<slug>/tier.txt`)

## Output

```
clients/<slug>/
├── spot-storyboard.md           # 3-shot plan with frame descriptions
├── shot-{1,2,3}-ref.jpg         # still references
├── shot-{1,2,3}.mp4             # raw shot clips
├── spot.mp4                     # master 10-15s cinematic spot
├── spot-6s.mp4                  # social ad cut
└── spot-30s.mp4                 # (Empire tier only) full TV spot
```

## Quality bar

- Each shot must look like an actual cinematographer composed it — rule of thirds, leading lines, intentional negative space.
- No on-screen text in any shot until the final title card.
- No people unless the brand absolutely requires them — focus on product, environment, mood.
- Final spot MUST have a discernible beginning, middle, end. If the 3-shot sequence doesn't tell a 3-beat story, redo the storyboard.
- Cinema, not TikTok. No quick cuts. Long takes. Held shots.

## Hard rules

- **Use `generate create cinematic_studio_2_5` and `generate create soul_cinematic`** — these are the cinematic models. Don't fall back to `nano_banana_2` or `marketing_studio_video` for this flow.
- **Pre-check costs** before each generation — cinematic videos can be expensive. Surface total cost to you if > $5 estimated.
- Never publish to your-agency.com without  explicit go-ahead — these are flagship pieces.
- Never recycle a spot from one client to another. Each client deserves its own.

## Connected
- [[Higgsfield Stack]] · [[Launch & Manage]] · [[reference_higgsfield_api]]
