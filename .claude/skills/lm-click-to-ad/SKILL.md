---
name: lm-click-to-ad
description: |
  Paste a product URL, get a publish-ready video ad. Higgsfield's Click-to-Ad flow,
  tuned for your clients. Fastest path from "client sent me their site" to "shippable ad."

  Use when: "/lm-click-to-ad", "make an ad from this URL", "click to ad for [URL]",
  "fast ad for [client website]".

  Chains: marketing-studio products fetch --url → marketing_studio_video with click_to_ad feature.

  Output: 8s video ad in 3 formats (9:16, 1:1, 16:9) for any social platform.
---

# lm-click-to-ad — One-URL → publish-ready ad

## What this flow does

The fastest possible path from "I have a client URL" to "I have a video ad ready to push to Meta / TikTok / YouTube." Uses Higgsfield's **Click-to-Ad** feature: paste the URL, the backend scrapes product data + photos, generates an ad video, and we render it in 3 aspect ratios.

Perfect for:
- First-call client demos ("here, watch this — I made this for your site in 3 minutes")
- Quick ad iterations for clients on Engine ($1,497) or Empire ($3,997) tiers
- A/B test variants — run this 4 times with different modes, ship the best one

## Trigger phrases

`/lm-click-to-ad`, "make an ad from this URL", "click to ad for [URL]", "fast ad for [client website]".

## Inputs

Required:
- **URL** — the client's product page or landing page

Optional:
- **client slug** — if missing, infer from URL hostname (e.g. `regalnails.com` → `regal-nails`)
- **mode** — `ugc` (default), `tv_spot`, `product_showcase`, `wild_card`
- **duration** — 8s default
- **count** — how many ad variants to generate (default 1, max 4)
- **aspects** — comma-separated list, default `9:16,1:1,16:9`

## Process

1. **Resolve client slug:**
   - If passed explicitly, use it.
   - Else parse URL hostname → kebab-case (e.g. `regalnails.com` → `regal-nails`).
   - Create `clients/<slug>/` if it doesn't exist.
2. **Fetch the product entity** from the URL:
   ```
   higgsfield marketing-studio products fetch --url <URL> --wait
   ```
   Save the returned product UUID to `clients/<slug>/product-id.txt`.
3. **(Optional) Read brand context** — `clients/<slug>/DESIGN.md` if exists. If not, default to your agency's editorial-dark.
4. **Generate the ad(s)** with `higgsfield generate create marketing_studio_video`:
   - `--feature click_to_ad`
   - `--url <URL>` (backend reuses the fetched entity)
   - `--mode <mode>`
   - `--duration <seconds>`
   - `--generate_audio true`
   - For each aspect in the aspects list: generate one variant
   - Save to `clients/<slug>/ad-<mode>-<aspect>.mp4`
5. **(Optional) Run all 4 modes** if `count=4` was passed — generates `ugc`, `tv_spot`, `product_showcase`, `wild_card` versions in the primary aspect ratio for A/B testing.
6. **Print a summary** with file paths + a one-line "use this for X platform" recommendation:
   - `9:16` → TikTok / IG Reels / YouTube Shorts
   - `1:1` → IG feed / FB feed
   - `16:9` → YouTube pre-roll / web embed

## Output

```
clients/<slug>/
├── product-id.txt                  # Higgsfield product UUID (reusable)
├── ad-<mode>-9x16.mp4              # vertical (TikTok/Reels/Shorts)
├── ad-<mode>-1x1.mp4               # square (IG/FB feed)
└── ad-<mode>-16x9.mp4              # horizontal (YouTube/web)
```

## Quality bar

- The ad must look like it was made FOR this product, not a generic template with the product slotted in. Verify against the source URL's actual product photos.
- 8s minimum — anything less reads as a placeholder.
- No on-screen text in the ad itself (text-on-video burns conversion). Save text for the platform's caption.
- If the generated ad makes claims the source URL doesn't support, regenerate. Don't fabricate features.

## Hard rules

- **Use `--feature click_to_ad`** — that's the magic. Don't manually orchestrate fetch+generate as separate steps.
- **Cache the product UUID** at `clients/<slug>/product-id.txt`. Re-fetching the same URL is wasteful.
- Never publish without  explicit go-ahead. This skill creates assets, not posts.
- Verify cost first if `count > 1` — that multiplies fast.
- Never use forbidden words in any text overlay or caption ("leverage / synergy / curated / delve").

## Connected
- [[Higgsfield Stack]] · [[Launch & Manage]] · [[reference_higgsfield_api]]
