---
name: website-design
description: |
  Specialized Claude Design workflow for full-page WEBSITES (landing pages, client demos, marketing sites, portfolio pages, agency work). Optimized for client demo builds, your-agency.com itself, and any web-output project. Layers on top of /claude-design with web-specific prompt templates, full-page hero patterns, conversion-focused layouts, GitHub Pages deploy hooks.

  Use when: building a full website, redesigning a client's site, creating a landing page, designing a portfolio card, doing marketing-site work. NOT for app screens — use /app-design for those.

  Triggers on: "/website-design", "design a website for [client]", "build a landing page for [project]", "let's design [client]'s site", "client demo for [type] business".
---

# website-design skill

Specialized layer on top of `/claude-design`. Pre-loads web-specific patterns and routes output to web-deploy targets.

**ALWAYS READ FIRST:** `~/.claude/skills/_shared/viktor-patterns.md` — the Viktor playbook (editorial-bold typography, reverse-loop video, magnetic CTAs, preloader pattern, Higgsfield CLI prompts). This skill applies Viktor patterns BY DEFAULT for creative-class clients. The shared file's "When to apply" decision rule is authoritative.

**Reuses:**
- `~/.claude/skills/_shared/viktor-patterns.md` — Viktor prompts + 4 code patterns + Higgsfield commands + decision tree
- `~/.claude/skills/claude-design/scripts/scrape_brand_to_design_md.py` — for client brand DESIGN.md
- `~/.claude/skills/claude-design/scripts/pull_getdesign_md.py` — for borrowed brand systems
- `~/.claude/skills/claude-design/scripts/open_claude_design.py` — for browser launch + clipboard
- **Higgsfield native skills:** `/higgsfield:generate`, `/higgsfield:product-photoshoot`, `/higgsfield:soul-id`, `/higgsfield:marketplace-cards` — preferred over the deprecated `generate_higgsfield_image.py` proxy

**Adds:**
- Web-specific 4-input prompt templates (hero, full landing, portfolio card, services grid, pricing page, about, contact)
- GitHub Pages deploy routing
- Mobile-first responsive enforcement
- Sacred-file awareness per project (e.g. your-agency.com homepage is locked)
- **Viktor-mode application** — auto-ON for creative-class clients (designers, photographers, tattoo, premium spa, agency, restaurants with destination angle, tech/SaaS/D2C). Auto-OFF for service trades (plumbers, contractors, family restaurants). Override with `viktor mode` (force on) / `simple mode` (force off).

---

## When to invoke (vs /app-design vs /claude-design)

| Need | Use |
|------|-----|
| Full client demo site (Example Client-style) | **/website-design** |
| New section on your-agency.com `/work/` | **/website-design** |
| Marketing landing page for a new product | **/website-design** |
| Pitch deck / one-pager / PDF | `/claude-design` (generic) |
| Mobile app screen | `/app-design` |
| Single component handoff to RN | `/app-design` |

## Workflow when invoked

### Step 1 — Scope & route

Ask once:
- **What kind of site?** Full client demo / Single landing page / Section update / Marketing site / Portfolio card
- **Which project?** your client (`your-agency/clients/<slug>/`) / your-agency.com itself / your client / new project
- **Brand source?** Scrape client URL / Existing folder / `templates/DESIGN.md` (your agency master template) / from scratch
- **Industry/audience?** (Use this with the Viktor decision tree to set Viktor mode default.)

If user says "client demo" — use the master `your-agency/templates/DESIGN.md` as the brand base unless we have client-specific assets to scrape.

### Step 1.5 — Determine Viktor mode (automatic)

Apply the decision rule from `~/.claude/skills/_shared/viktor-patterns.md`:

- **Viktor ON (default for):** designer, photographer, tattoo artist, premium spa, agency, video producer, musician, influencer portfolio, tech/SaaS/D2C, restaurant with destination angle, premium service business, your agency's own site
- **Viktor OFF (default for):** plumber, electrician, HVAC, locksmith, contractor, family restaurant, casual eatery, auto repair, lawn/pest/cleaning service, daycare, eldercare, conservative healthcare, funeral home, anything where customer wants "simple, clean, easy"
- **Override:** user can say `viktor mode` (force on) / `simple mode` (force off) / `motion-light` (typography only) / `motion-heavy` (every section animated)

Surface the choice to the user one-line: *"Viktor mode ON — editorial typography + reverse-loop hero video + magnetic CTAs + preloader. Say 'simple mode' to skip."*

### Step 2 — Generate / locate DESIGN.md

Same as `/claude-design` Step 2. For client demos specifically, START with `your-agency/templates/DESIGN.md` and LAYER client-specific assets on top.

### Step 3 — Build the 4-input prompt — WEB-SPECIFIC

Web prompts have additional structure beyond the generic 4-input formula. **If Viktor mode ON, use the Viktor-augmented version below; otherwise use the standard version.**

#### 3a. Standard prompt (Viktor OFF)

```
Build a [SITE TYPE: client demo landing page / marketing page / portfolio card] for [CLIENT/PROJECT].

Audience: [who specifically — same depth as /claude-design]
Tone: [3-5 specific adjectives]

Sections (in order, each with content):
1. Hero — [headline, subhead, CTA, visual treatment]
2. Social proof — [reviews, count, trust signals]
3. Services / Features — [3-6 cards or rows, each with icon + headline + 1-line desc]
4. Reviews / Testimonials — [3 real reviews if available, otherwise placeholder marker]
5. About — [story, location, year established, founder if relevant]
6. Visit / Contact — [address, phone, hours, map embed if local biz]
7. Footer — [hours grid, social, legal]

Constraints:
- Use brand from uploaded DESIGN.md
- Mobile-first responsive — design 390px first, scale up to 1440px
- All CTAs must be tap-friendly (min 44x44px)
- WCAG AA contrast minimum
- Page weight target under 3MB total
- Hero video (if any) must autoplay muted+playsinline+webkit-playsinline
- Splash logic: JS-based source select for portrait/landscape video (NOT <source media>)
- Avoid: lorem ipsum, "premier/professional/trusted" cliché copy, stock photos with people in suits, drop shadows that feel 2014
```

#### 3b. Viktor-augmented prompt (Viktor ON — DEFAULT for creative class)

Same as 3a PLUS append these constraints:

```
VIKTOR MODE — apply these patterns:

Hero treatment:
- Editorial-bold typography hero — massive sans-serif (clamp 4rem-14vw-14rem), uppercase, weight 900, line-height 0.9, letter-spacing -0.04em
- Italic serif tagline below (Playfair-style)
- Plain pure-black background (#000)
- 16:9 aspect ratio
- Generated via Higgsfield CLI: `hf generate create gpt_image_2 --prompt "..." --aspect-ratio 16:9` (Turbo quality preset, model gpt_image_2)
- Hero looping video (Kling 3.0, 12s, 1080p, "for website perfect loop") — placed AS the hero visual, plays forward then reverse-loops seamlessly (throttled-seek pattern, see _shared/viktor-patterns.md §1)

Motion patterns (apply to every page):
- Reverse-loop video pattern (no jump-cut at loop point) — see _shared/viktor-patterns.md §1
- Magnetic mouse-follow on all primary CTAs and hero focal elements — see _shared/viktor-patterns.md §2
- Preloader: short Higgsfield-generated video (scatter→reassemble or reveal motion) → fade out → main content fades in — see _shared/viktor-patterns.md §3

Stack expectations (when handing to Claude Code):
- React + Vite + TypeScript + Tailwind CSS + framer-motion (+ GSAP or Three.js if needed)
- Helvetica Neue or chosen display font, downloaded from font.download and dropped into Claude Code chat
- Performance budget: total ≤ 4MB, hero video ≤ 1.5MB, preloader ≤ 1.5MB, Lighthouse Performance ≥ 80, LCP < 2.5s

Pre-build the assets BEFORE the design pass:
1. Hero typography image: `/higgsfield:generate use gpt_image_2 4k quality 1t` with editorial prompt (see _shared/viktor-patterns.md prompts section)
2. Hero looping video: `/higgsfield:generate use kling_3_0 12 seconds 1080p "for website perfect loop"`
3. Preloader video: same model, 6 seconds, scatter/reveal motion
4. Section imagery: `/higgsfield:product-photoshoot` for any product shots

Avoid: same as standard PLUS — square heroes, generic stock typography, "vibrant gradient" backgrounds, every section animated (motion is strategic not constant).
```

When Viktor mode is ON, surface the asset list to the user BEFORE running Claude Design — they need to know which Higgsfield generations will fire and the credit cost (typical demo: ~200-350 credits per `_shared/viktor-patterns.md`).

### Step 4 — Open claude.ai/design with prompt

Same as `/claude-design` Step 4.

### Step 5 — Iteration coaching (web-specific)

In addition to the canvas/chat routing from `/claude-design`:

- **"It looks too basic / generic"** → ask Claude Design: "Add 2 motion details (hover state on cards, marquee section, parallax hero) without adding clutter."
- **"Mobile looks broken"** → "Generate the 390px and 1440px versions side-by-side. Surface every layout that breaks at small."
- **"Hero is weak"** → use `/website-design hero` sub-routine: generates 3 hero variations with different angles (proof-led, outcome-led, fear-led) for A/B picking.

### Step 6 — Web-specific validation

Run THESE prompts (overrides the generic validation set):

```
Review this design for contrast and accessibility. List any WCAG 2.1 AA violations with exact fixes.
```
```
Generate the 390px (iPhone), 768px (iPad), 1024px (laptop), and 1440px (desktop) versions. Surface every layout that breaks.
```
```
Render the page weight breakdown — total HTML/CSS/JS/images/fonts. Flag anything that pushes the page over 3MB total.
```
```
Suggest 2 hero variations with different conversion angles (proof-led vs outcome-led).
```

### Step 7 — Export → deploy routing

Web export targets:
- **client demo** → `your-agency/clients/<slug>/` (source) AND `_repos/launch-and-manage/preview/<slug>-<city>/` (deploy)
- **your-agency.com /work/ card** → add to existing `work/index.html` as new `<article>` block, push to `_repos/launch-and-manage/`
- **Standalone landing page** → ask user where; default to `_repos/launch-and-manage/landing/<slug>/`

After save:
1. Run a Playwright smoke test (Mobile + Desktop screenshot) using `portal-scraper/record_regal_nails_reel.py` pattern
2. Push to GitHub → GitHub Pages auto-deploys in ~30-60s
3. Surface the live URL to the user

## Project-specific defaults

### client demo
- Master DESIGN.md: `your-agency/templates/DESIGN.md`
- Editorial dark + Playfair italic + champagne/rose-gold accents
- 5-image hero slideshow + 12-image gallery + reviews + map + book-CTA banner
- Mobile splash uses 9:16 portrait video (Veo 3.1)

### your-agency.com itself (SACRED — confirm with user before any edit)
- Cyan #00f0ff + hot pink #ff2e93 dual accent
- Syne display + DM Sans body
- Custom cursor (desktop), magnetic CTAs
- Splash plays once per session (sessionStorage)

### your client retail
- Chrome glamour palette
- Aspirational copy
- Homepage = SACRED, never modify without confirm

## Don't

- Don't redesign the your-agency.com homepage. New work goes in `/work/` or `/preview/`. Per the your agency CLAUDE.md.
- Don't use `<source media>` on `<video>` for splash logic. Use JS-based source select. (See `clients/regal-nails/index.html` lines 695-705 + 933-970 for the working pattern.)
- Don't use lorem ipsum in client demos. Generate real-feeling placeholder copy from the brand promise + audience profile.
- Don't ship without running the page weight + responsive validation prompts. Fix issues before deploy.
