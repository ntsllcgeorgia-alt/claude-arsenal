---
name: lm-carousel
description: |
  Generate a multi-slide Instagram / LinkedIn carousel for any your client (or your clients catalog). 5-10 slides
  with consistent visual style across the whole set. Uses reference-image-anchored generation so slides
  match a brand look instead of drifting between models' default aesthetics.

  Use when: "/lm-carousel", "carousel for [client]", "5-slide post on [topic] for [client]",
  "Instagram carousel about [topic]", "TPP product feature carousel", "client catalog highlight carousel".

  Chains: higgsfield-generate (cover slide, 4 variations) → user picks one → that cover becomes the
  style reference for slides 2-N → optional Late scheduling via late-social-media skill.

  Output: N numbered JPG slides + captions.txt + optional Late-scheduled queue.

  NOT for: single hero image (use higgsfield-generate), product detail / marketplace cards
  (use higgsfield-marketplace-cards), short video content (use lm-cinematic-spot / lm-product-showcase).
argument-hint: "<client-slug> [topic] [--slides N] [--ref <path>]"
allowed-tools: Bash, Read, Write, Edit, Glob
---

# lm-carousel — Multi-slide consistent-style carousel flow

## What this flow does

Generates an **Instagram / LinkedIn carousel** (5-10 slides) where every slide shares a unified visual style. The first slide is generated in 4 variations; the user picks the winner, and that winner is then used as the **style reference** for every subsequent slide so the set looks like one designer made the whole thing.

This is the pattern Chase AI demoed for "GitHub trending → Top 5 carousel" — adapted to your client niches (salons, restaurants, contractors) and your clients product features.

## Trigger phrases

`/lm-carousel`, "carousel for [client]", "5-slide post on [topic] for [client]", "Instagram carousel about [topic]", "TPP feature carousel for [SKU]", "client catalog highlight for [category]".

## Inputs

Required:
- **client slug** (e.g. `regal-nails`, `acme-roofing`, `tpp`, `ntp`) — used for brand voice + output path.
- **topic** — what the carousel is about, one sentence. Examples:
  - `"5 reasons to switch to gel manicures"` (Example Client)
  - `"top 5 brake-system upgrades for Peterbilt 389"` (NTP)
  - `"weekend roofing checklist"` (Acme Roofing)

Optional:
- **`--slides N`** — slide count, default 5, range 3-10.
- **`--ref <path>`** — explicit style reference image (e.g. an existing slide the user loves). If omitted, the cover-slide variation flow handles style.
- **`--aspect <ratio>`** — `1:1` (IG feed, default), `4:5` (IG portrait, max engagement), `9:16` (Stories / Reels cover).
- **`--brand-mode`** — overrides what's in DESIGN.md. Values: `editorial` (default), `industrial` (NTP), `chrome-glamour` (TPP), `salon-warm` (Example Client), `clean-corporate`.

## Process

### 1. Read brand context
- If `clients/<slug>/DESIGN.md` exists, read it for: palette, typography, voice rules, do/don't list.
- Else fall back to defaults (hot pink + cyan, Playfair italic, editorial dark, no agency jargon).
- your clients have their own brand modes — see [[Higgsfield Stack]] for the rules.

### 2. Plan the slides (no generation yet)
- Outline `N` slides as a numbered list: `1. Cover (hook)`, `2-N. Supporting points`, `N. CTA`.
- Write each slide's headline + 1-line body BEFORE generating any image. Show the plan to the user and wait for go-ahead. This is the "lets talk about it before sending it off for content creation" pattern from the Chase AI video — cheaper than re-generating after the fact.

### 3. Generate cover slide — 4 VARIATIONS
- Model: `gpt_image_2` (high-fidelity, on-image text, design / typography work).
- Run **4 separate `higgsfield generate create` calls** with the same prompt but no fixed seed, OR use `--count 4` if the model supports it.
- Prompt template:
  ```
  Instagram carousel cover, [aspect], [brand mode] aesthetic.
  Headline: "<slide-1-headline>"
  Subline: "<slide-1-body>"
  Style: <palette + typography rules from DESIGN.md>
  Composition: bold center-aligned typography, [supporting visual element], shallow depth of field.
  No watermarks, no logos, no stock-photo people.
  ```
- Cost-check first: `higgsfield generate cost gpt_image_2 --prompt "..."`. If 4 variations × cost > $0.50, surface to you.
- Save the 4 candidates to `clients/<slug>/carousel/cover-v1.jpg` … `cover-v4.jpg`.
- Open all 4 in default viewer or print URLs.

### 4. User picks the winner
- Ask: "Which cover variation? (1, 2, 3, or 4)"
- Copy the picked file to `clients/<slug>/carousel/01.jpg`.
- Delete the 3 losers. (Optional — keep for A/B later if `--keep-losers`.)

### 5. Generate slides 2 through N — ANCHORED to the winning cover
- For each slide `i` in 2..N:
  - Model: same `gpt_image_2`.
  - **Pass `--image clients/<slug>/carousel/01.jpg`** as a style reference (the winning cover) — this is the key trick for visual consistency.
  - Prompt template:
    ```
    Instagram carousel slide [i] of [N], matching the reference image's visual style exactly.
    Headline: "<slide-i-headline>"
    Body: "<slide-i-body>"
    Same palette, same typography, same composition rules as reference.
    Subject: <new visual element specific to this slide's content>.
    ```
  - Save to `clients/<slug>/carousel/<i:02d>.jpg`.

### 6. Write captions
- Generate `clients/<slug>/carousel/captions.txt`:
  - One IG-ready caption per slide, sequenced for swipe-reading.
  - Hashtag set tailored to the client's niche (max 8 hashtags, no banned/shadowbanned ones).
  - End the set with one CTA matching the client's brand voice (book now / DM us / link in bio / call XXX).
  - Voice rules per your agency: NO `leverage`, `synergy`, `curated`, `delve`, em-dashes. Short sentences. Direct DM-style.

### 7. Optional — queue to Late
- If the user says "queue it" / "schedule it" / "ship it", chain into `late-social-media` skill:
  - Account: client's IG account ID (look up in `clients/<slug>/MARKETING.md` or ask).
  - Slide order: `01.jpg` through `<N>.jpg`.
  - Caption: contents of `captions.txt`.
  - Default schedule: next available 8 AM CT slot.

## Output

```
clients/<slug>/carousel/
├── cover-v1.jpg ... cover-v4.jpg  # the 4 cover candidates (auto-cleaned after pick unless --keep-losers)
├── 01.jpg                          # the chosen cover (= winning variation)
├── 02.jpg ... <N>.jpg             # supporting slides, all style-anchored to 01.jpg
└── captions.txt                    # one caption per slide + hashtag set + CTA
```

If the demo deploys, mirror the slides to `_repos/launch-and-manage/preview/<slug>-<city>/carousel/`.

## Quality bar

- All N slides MUST share the same palette, typography, and composition logic (eyeball test — if you can't tell slide 4 was made by the same designer as slide 1, regenerate slide 4 with stronger reference weight).
- Slide 1 (cover) must be the strongest standalone — most people swipe based on slide 1 only.
- No AI tells: no extra fingers, no melting objects, no garbled text on signs / packaging in the background.
- File size per slide under 500 KB after web compression. JPEG quality 85.
- Aspect ratio matches the platform target: `1:1` for IG feed, `4:5` for IG portrait, `9:16` for Stories.

## Hard rules

- **Use `generate create`, never `product-photoshoot create`** (per `feedback_higgsfield_use_generate_create`).
- Never write to `04-PUBLISHED/`.
- Never modify `your-agency.com` homepage.
- Never auto-post to a client IG without explicit "ship it" confirmation (per your agency CLAUDE.md).
- Always run the slide-plan past the user BEFORE generating images. Don't burn credits on a misread brief.
- Voice rules from your agency CLAUDE.md apply to every caption.

## The Higgsfield MCP path (alternative to CLI)

As of 2026-05-17, the official Higgsfield MCP is wired up at user scope (`https://mcp.higgsfield.ai/mcp`). When invoked from a Claude Code session that has accepted the OAuth, you can call `mcp__higgsfield__generate_image` as a native tool instead of spawning `higgsfield generate create` via Bash. Same model catalog, same parameters, lower latency. Either path works for this skill — Bash is the documented default for portability; MCP is faster once authed.

## Connected
- [[Higgsfield Stack]] — the underlying primitives + 7 sibling flow skills + MCP path
- [[Launch & Manage]] — agency voice rules + client list
- [[your client]] / [[Truck Parts Plus]] — for your clients carousel work
- [[late-social-media]] — scheduling step at the end
