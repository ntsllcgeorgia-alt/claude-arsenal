---
name: lm-product-showcase
description: |
  Generate a clean product-focused video — less presenter, more product. For your clients
  selling physical products (retail, food, beauty, fashion). The product is the hero.

  Use when: "/lm-product-showcase", "product showcase video for [client]", "show the product
  itself for [project]", "clean product highlight for [thing]".

  Chains: higgsfield-product-photoshoot (still) → marketing_studio_video (product_showcase mode) → ffmpeg.

  Output: 8s 16:9 MP4 + 9:16 vertical crop.
---

# lm-product-showcase — Clean product-focused video flow

## What this flow does

Generates a video where the PRODUCT is the hero — no on-screen presenter, no testimonial voiceover. Just the product in motion: rotating, being held, used, plated, modeled.

For your clients selling tangible things:
- Restaurant: dish being plated, steam rising, hand placing garnish
- Salon: nail polish bottle, gel being applied, finished hand reveal
- Apparel: fabric draping, button-pull, garment turning on hanger
- Contractor: finished install, before-after wipe
- Bakery: dough being shaped, oven open, finished pastry close-up

## Trigger phrases

`/lm-product-showcase`, "product showcase for [client]", "show the product itself for [project]", "clean product highlight", "no-presenter product video".

## Inputs

Required:
- **client slug**
- **product description** in one sentence (e.g. "matte black nail polish bottle with chrome cap", "wood-fired Margherita pizza with fresh basil")
- **action** in one sentence (e.g. "slowly rotating against dark backdrop", "steam rising as the lid lifts off", "hands placing the bottle on a marble surface")

Optional:
- **brand mode** — `editorial` (default), `industrial`, `glamour`, `lifestyle`
- **duration** — 8s default, 4-12s
- **aspect** — `16:9` (default), `9:16`, `1:1`
- **reference image** — actual product photo path (preserves identity)

## Process

1. **Read brand context** — `clients/<slug>/DESIGN.md` for palette + mood.
2. **Generate the product still** — TWO paths:
   - **Path A (preferred): real product photo available.** Use `higgsfield generate create nano_banana_2 --image <real-photo>` for identity-preserving render in the brand-mode aesthetic.
   - **Path B: text-only.** Use `higgsfield generate create nano_banana_2 --prompt "<product>, <brand mode> aesthetic, studio lighting, <aspect>"`.
   - Save to `clients/<slug>/showcase-frame.jpg`.
3. **Generate the showcase video** with `higgsfield generate create marketing_studio_video`:
   - `--mode product_showcase` (no presenter, polished)
   - `--medias '[{"role":"image","url":"<showcase-frame.jpg>"}]'`
   - `--aspect_ratio <ratio>`
   - `--duration <seconds>`
   - `--generate_audio false` (showcase typically uses music bed in post)
   - Save to `clients/<slug>/showcase.mp4`
4. **Generate the vertical crop** with ffmpeg center-safe crop to 9:16 → `clients/<slug>/showcase-9x16.mp4`.
5. **Optional: add subtle music bed** if `clients/<slug>/score.mp3` exists — ffmpeg mix at -18dB so it sits under any future voiceover.

## Output

```
clients/<slug>/
├── showcase-frame.jpg         # the still product reference
├── showcase.mp4               # 16:9 master
└── showcase-9x16.mp4          # vertical crop for social
```

## Quality bar

- Product identity must be preserved — if the client provided a real product photo and the output doesn't match, regenerate with `--image` reference enabled.
- Lighting must look intentional — studio lighting, not flat.
- Background subtle, brand-mode-consistent. Never a busy or distracting backdrop.
- No "AI tells" — count details (e.g. number of buttons on a shirt, number of slices on a pizza). Re-generate if anomalies.
- Action must be one continuous motion. No cuts within the showcase clip.

## Hard rules

- **Always pass a real product photo via `--image` when available.** your clients hate when the AI-generated product looks "close-ish but wrong" — preserve identity.
- **Use `generate create marketing_studio_video --mode product_showcase`** — this is the cleanest path. Not `--mode ugc`.
- Never invent product features that aren't in the brief or the photo (e.g. don't add fake text labels, fake size variants, fake "NEW" badges).
- Verify cost first if duration > 8s.

## Connected
- [[Higgsfield Stack]] · [[Launch & Manage]] · [[reference_higgsfield_api]]
