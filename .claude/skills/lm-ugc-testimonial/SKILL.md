---
name: lm-ugc-testimonial
description: |
  Generate a UGC-style talking-head testimonial video for an your client.
  Looks like a real person filmed on their phone — perfect for ads, social, or "testimonial" section
  of a client demo.

  Use when: "/lm-ugc-testimonial", "make a UGC video for [client]", "testimonial video about [product]",
  "I need a phone-style review for [project]".

  Chains: higgsfield-soul-id (character) → marketing_studio_video (UGC mode) → optional script gen.

  Output: 8-second vertical (9:16) MP4 + horizontal (16:9) crop for web.
---

# lm-ugc-testimonial — UGC talking-head video for your clients

## What this flow does

Generates a UGC testimonial video featuring a synthetic-but-believable character giving an opinion about the client's product or service. Phone-vertical (9:16) by default. Suitable for social ads, IG Reels, TikTok, or embedded as a "What our customers say" section on a client demo.

## Trigger phrases

`/lm-ugc-testimonial`, "make a UGC video for [client]", "testimonial video about [product]", "phone-style review of [thing]".

## Inputs

Required:
- **client slug** (e.g. `regal-nails`)
- **product or service** (e.g. "gel manicure", "Sarsour catering"), in one sentence
- **angle** (e.g. "skeptical-then-converted", "obsessed-customer", "first-time-trying")

Optional:
- **character persona** (e.g. "early-30s mom in DFW", "20s salon regular") — defaults inferred from client audience
- **duration** — 8s default, 4-15s
- **mode** — `ugc` (default), `ugc_unboxing`, `product_review`, `ugc_how_to`
- **aspect ratio** — `9:16` (default), `16:9`, `1:1`

## Process

1. **Read client context** — `clients/<slug>/DESIGN.md` + `clients/<slug>/MARKETING.md` if present. Pull audience details from your agency's customer personas.
2. **Generate or reuse Soul Character:**
   - If `clients/<slug>/soul-id.txt` exists, reuse that Soul ID.
   - Otherwise train a new one: `higgsfield generate create text2image_soul_v2 --prompt "<persona detailed description>"` → save reference image → run `higgsfield-soul-id` to train → write the new ID to `clients/<slug>/soul-id.txt`.
3. **Draft the testimonial script** (≤ 25 words, no agency jargon):
   - Hook (3-4 words) — open the loop
   - Body (1-2 sentences) — the specific reason it worked
   - Closer (3-5 words) — implicit CTA
   - Use the your agency voice rules: short sentences, real specifics, no "leverage / synergy / curated / delve".
4. **Generate the video** with `higgsfield generate create marketing_studio_video`:
   - `--mode <mode>` (default `ugc`)
   - `--aspect_ratio 9:16`
   - `--duration <seconds>`
   - `--avatars '[{"id":"<soul-id>","type":"custom"}]'`
   - `--product_ids '[<product-uuid>]'` (if a product was fetched via `marketing-studio products fetch --url`)
   - `--generate_audio true` — talking head needs voice
   - Save to `clients/<slug>/ugc-<angle>.mp4`
5. **Generate a 16:9 horizontal crop** with ffmpeg (center-safe crop) for the client demo's "what our customers say" section.

## Output

```
clients/<slug>/
├── soul-id.txt                  # Reusable Soul Character ID (don't regenerate)
├── ugc-<angle>.mp4              # 9:16 vertical, phone-style
├── ugc-<angle>-16x9.mp4         # 16:9 horizontal crop for web embed
└── ugc-<angle>-script.md        # The script, for reference + future variants
```

## Quality bar

- Character must look like a REAL person, not a model. Skin should have texture. Lighting natural (window light > studio).
- Script must be in your agency's voice — short, specific, no jargon. If the testimonial sounds AI-written, regenerate the script first.
- No visible "AI tells" — count fingers in the frame, check the product doesn't morph mid-video.
- 9:16 is the master format. The 16:9 is a crop, not a regenerate.

## Hard rules

- **Reuse Soul Character per client** — never re-train if `soul-id.txt` exists. Burns budget for no gain.
- **Use `generate create`, never `marketing-studio create`** if the CLI exposes both — same `feedback_higgsfield_use_generate_create` rule.
- Never put a UGC testimonial on your-agency.com homepage — only on individual client demos or paid ads.
- Never use real customer names in the script unless explicitly provided by you. Use first-name-only fakes ("Sarah", "Marco") as placeholders.
- Verify cost first if the duration > 10s.

## Connected
- [[Higgsfield Stack]] · [[Launch & Manage]] · [[reference_higgsfield_api]]
