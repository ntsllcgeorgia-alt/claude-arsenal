---
name: lm-hero-video
description: |
  Generate a striking hero VIDEO for any your client landing page or demo.
  5-8s loopable, optimized for the top of a landing page. Replaces static hero images.

  Use when: "hero video for [client]", "/lm-hero-video", "generate a hero loop for [project]",
  "I need a hero video for the website".

  Chains: higgsfield-generate (image reference) → seedance/kling (video) → optional Soul character.

  Output: MP4 + WebM at 1920x1080, 6 seconds, loopable.
---

# lm-hero-video — your agency landing page hero video flow

## What this flow does

Generates a 5-8s **hero video** suitable for the top of a your-agency.com client demo. The video is loopable, web-optimized, and matches the client's brand mode (industrial / glamour / editorial / clean).

## Trigger phrases

`/lm-hero-video`, "hero video for [client]", "generate a hero loop for [project]", "I need a hero video for [client]'s site".

## Inputs

Required:
- **client slug** (e.g. `regal-nails`, `acme-roofing`) — used for output path
- **subject** in one sentence (e.g. "shiny chrome wheel rim with reflections", "nail technician's hand finishing a manicure", "open kitchen with steam rising from a pizza oven")

Optional:
- **brand mode** — `editorial` (default for your agency demos), `industrial`, `glamour`, `clean-corporate`
- **aspect ratio** — `16:9` (default), `21:9` (cinematic letterbox), `9:16` (mobile-first)
- **duration** — 6s default, range 4-15s
- **palette** — read from `clients/<slug>/DESIGN.md` if present, else inferred from subject

## Process

1. **Read brand context** — if `clients/<slug>/DESIGN.md` exists, read it; else fall back to your-agency.com brand defaults (hot pink + cyan accent, editorial dark, Playfair italic, no agency jargon).
2. **Generate a still reference frame** with `higgsfield generate create nano_banana_2`:
   - Prompt: `"<subject>, <brand mode> aesthetic, cinematic <aspect_ratio>, shallow depth of field, premium production"`
   - Aspect: `16:9` (or whatever was requested)
   - Save to `clients/<slug>/hero-frame.jpg`
3. **Generate the video** with `higgsfield generate create seedance_v5_pro_25`:
   - Use the still as the start frame (`--image clients/<slug>/hero-frame.jpg`)
   - Prompt extension: `"camera slowly drifts, subject reveals detail, no cuts, loopable, ambient natural motion"`
   - Duration: requested duration (default 6s)
   - Save to `clients/<slug>/hero.mp4`
4. **Compress for web** — run ffmpeg to produce a 1920x1080 H.264 mp4 + WebM fallback under 4 MB total. Strip audio (hero videos are silent).
5. **Update the client demo HTML** — if `clients/<slug>/index.html` exists, swap the existing hero `<img>` for a `<video autoplay muted loop playsinline>` tag pointing at the new MP4. Otherwise leave the files in `clients/<slug>/` for manual placement.

## Output

```
clients/<slug>/
├── hero-frame.jpg     # the still reference (also usable as fallback poster)
├── hero.mp4           # H.264, web-optimized, < 4 MB
└── hero.webm          # WebM fallback
```

If the demo lives in `_repos/launch-and-manage/preview/<slug>-<city>/`, mirror the files there too.

## Quality bar

- Hero MUST be loopable (no visible cut at the loop boundary). Use `kling_omni_image` or `seedance_v5_pro_25` with the loopable hint.
- No people doing anything cringey, no "AI tells" (extra fingers, melting objects, duplicated subjects). Re-generate if needed.
- File size under 4 MB or it kills the LCP score on your-agency.com.
- Frame matches the brand mode of the client's DESIGN.md, NOT the your-agency.com chrome.

## Hard rules

- **Use `generate create`, never `product-photoshoot create`** (per `feedback_higgsfield_use_generate_create` — generations must appear in account history).
- Never write to `04-PUBLISHED/`.
- Never modify `your-agency.com` homepage. Heroes go in `clients/<slug>/` or `preview/<slug>/`.
- Never use forbidden words in any caption / fallback alt text generated.
- Verify cost first: `higgsfield generate cost seedance_v5_pro_25 --prompt "..."`. If > $0.50, surface to you before generating.

## Connected
- [[Higgsfield Stack]] — the underlying CLI + 5 primitive skills
- [[Launch & Manage]] — agency operations + voice rules
- [[reference_higgsfield_api]] — credentials
