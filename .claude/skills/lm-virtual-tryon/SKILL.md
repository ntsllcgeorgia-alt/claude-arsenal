---
name: lm-virtual-tryon
description: |
  Generate a virtual try-on video — model wearing a clothing item, holding a product, or
  demonstrating an accessory. For your agency fashion / beauty / retail clients.

  Use when: "/lm-virtual-tryon", "virtual try-on for [client]", "model wearing [product]",
  "show someone using [product] for [client]".

  Chains: higgsfield-soul-id (model) → marketing_studio_video (virtual_try_on or ugc_virtual_try_on)
  → ffmpeg.

  Output: 8s 9:16 vertical MP4 + 16:9 horizontal crop.
---

# lm-virtual-tryon — Model-wearing-product video flow

## What this flow does

Generates a video of a model **wearing** the product (clothing, accessory, beauty product, glasses) or **using** it in a natural way. Useful for your clients in:
- Apparel / accessories
- Beauty (foundation match, lipstick, jewelry try-on)
- Eyewear / sunglasses
- Watches / wearables

Two modes:
- **`virtual_try_on`** — polished, model-driven, studio aesthetic
- **`ugc_virtual_try_on`** — organic, phone-vertical, "trying this on at home" vibe

## Trigger phrases

`/lm-virtual-tryon`, "virtual try-on for [client]", "model wearing [product]", "show someone using [product]", "try-on video for [client]".

## Inputs

Required:
- **client slug**
- **product** in one sentence (e.g. "oversized white linen shirt", "round gold-frame sunglasses", "matte burgundy lipstick")
- **model brief** in one sentence (e.g. "early 30s woman with dark hair", "20s man with beard"). Defaults from `clients/<slug>/MARKETING.md` personas if available.

Optional:
- **mode** — `virtual_try_on` (polished, default for non-UGC clients), `ugc_virtual_try_on` (organic, phone-vertical)
- **setting** — `studio` (default), `home`, `outdoor`, `cafe`
- **duration** — 8s default, 4-15s
- **aspect** — `9:16` (default for `ugc_virtual_try_on`), `16:9` for `virtual_try_on`
- **reference product image** — actual product photo path (preserves identity)
- **reuse client Soul ID** — `clients/<slug>/soul-id.txt` if exists

## Process

1. **Read context** — `clients/<slug>/DESIGN.md`, `clients/<slug>/MARKETING.md` for audience + palette.
2. **Get / generate Soul Character:**
   - If `clients/<slug>/soul-id.txt` exists, reuse.
   - Otherwise generate: `higgsfield generate create text2image_soul_v2 --prompt "<model brief>, natural skin texture, <setting> lighting"` → save reference → train via `higgsfield-soul-id` → store ID at `clients/<slug>/soul-id.txt`.
3. **Generate the still frame** with `higgsfield generate create nano_banana_2 --image <product-photo>` (if real product photo provided) or text-only:
   - Composition: model wearing/holding/using the product in the chosen setting
   - Save to `clients/<slug>/tryon-frame.jpg`
4. **Generate the try-on video** with `higgsfield generate create marketing_studio_video`:
   - `--mode <virtual_try_on | ugc_virtual_try_on>`
   - `--avatars '[{"id":"<soul-id>","type":"custom"}]'`
   - `--product_ids` if a product entity was created via `marketing-studio products fetch`
   - `--medias '[{"role":"start_image","url":"<tryon-frame.jpg>"}]'`
   - `--aspect_ratio <ratio>`
   - `--duration <seconds>`
   - `--generate_audio false` (try-on usually silent or music-bed in post)
   - Save to `clients/<slug>/tryon-<product-slug>.mp4`
5. **Generate the alternate aspect crop** with ffmpeg for cross-platform.

## Output

```
clients/<slug>/
├── soul-id.txt                 # reusable Soul ID
├── tryon-frame.jpg             # still composition reference
├── tryon-<product>.mp4         # master video (9:16 or 16:9 per mode)
└── tryon-<product>-alt.mp4     # other aspect crop
```

## Quality bar

- Product must be visible and identifiable — if the try-on video makes the product look generic, regenerate with a stronger product `--image` reference.
- Model's interaction with the product must be NATURAL — no awkward hand placement, no clipping into the body.
- Fabric drape / lipstick texture / metallic sheen must look real. Watch for AI-flatness.
- 8s minimum to show the product convincingly. 4-6s often reads as too quick.

## Hard rules

- **Always pass the real product photo via `--image` when available.** Identity preservation matters here more than anywhere.
- **Reuse the client's Soul Character** — don't burn budget retraining.
- **`ugc_virtual_try_on` for organic phone-vertical content, `virtual_try_on` for polished studio content.** Don't mix.
- Never put a face on a body in a way that looks uncanny — if the result is creepy, regenerate or switch the angle.
- Verify cost first if duration > 10s or if Soul retraining is needed.

## Connected
- [[Higgsfield Stack]] · [[Launch & Manage]] · [[reference_higgsfield_api]]
