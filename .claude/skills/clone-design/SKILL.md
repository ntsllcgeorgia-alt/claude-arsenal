---
name: clone-design
description: |
  Rebuild a website's visual design from a URL, screenshot, or image reference.
  Captures the source page via Playwright (full-page screenshot + relevant HTML/CSS),
  feeds it to Claude with vision, and produces a working static clone in the user's
  current project folder. Use for design inspiration, competitor teardown, FSBO
  landing-page rebuilds, "make my site look like [this great site]", or pattern study.

  Use when: "/clone-design", "clone this website", "build me a version of [URL]",
  "rebuild this design", "I want my site to look like [URL]", "pixel-match this Dribbble".

  Output: a self-contained folder with index.html + styles.css (or React component
  if --stack react) saved to ./clones/<slug>/ — never overwrites existing files.

  NOT for: stealing trademarked brand assets, ripping someone's actual content
  verbatim, or cloning an entire SaaS app's logic. This is for VISUAL pattern study —
  layout, color palette, typography, composition. Replace all copy + branding with
  the user's own before shipping.
argument-hint: "<URL or image-path> [--stack html|react] [--out <dir>]"
allowed-tools: Bash, Read, Write, Edit, Glob
---

# clone-design — rebuild a website's visual pattern

Inspired by Jono Catliff's Dribbble-clone workflow (500-hour Claude Code video):
*"Head over to Dribbble, take a screenshot of any design you love, paste it into
Claude Code, and it'll clone it pixel-for-pixel. This is how you get websites
that don't look like AI slop."*

This skill formalizes that pattern with two improvements:
1. Works from a **live URL** (not just a screenshot) so you also get the real
   HTML/CSS hints to feed Claude — cleaner code, fewer "guess from pixels" mistakes
2. Outputs to a **clean folder** so you can iterate without polluting your project

## Trigger phrases

`/clone-design`, "clone this website", "rebuild [URL] in my project",
"build a version of [URL]", "match this Dribbble design", "I want my hero to look like [URL]'s hero".

## Inputs

**Required (one of):**
- A **URL** (`https://stripe.com`, `https://dribbble.com/shots/...`) — Playwright captures it
- A **local image path** (`./inspo/landing.png`) — used directly (no Playwright run)
- A **pasted screenshot** in chat — use Claude's native image vision

**Optional flags:**
- `--stack html` (default) — vanilla HTML + CSS, no framework
- `--stack react` — single React functional component using Tailwind
- `--out <dir>` — output folder (default: `./clones/<auto-slug>/`)
- `--full-page` — capture full scroll (default: viewport only)
- `--mobile` — also capture mobile viewport (375px wide)

## Process

### 1. Capture the source

**If URL:**
```bash
# Install playwright if missing (one-time)
pip install playwright >/dev/null 2>&1 && python -m playwright install chromium >/dev/null 2>&1

# Screenshot + HTML dump (single script call)
python -c "
from playwright.sync_api import sync_playwright
import sys, json
url, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 1440, 'height': 900})
    page.goto(url, wait_until='networkidle', timeout=30000)
    page.screenshot(path=f'{out}/source-desktop.png', full_page=True)
    page.set_viewport_size({'width': 375, 'height': 812})
    page.screenshot(path=f'{out}/source-mobile.png', full_page=True)
    html = page.content()
    with open(f'{out}/source.html', 'w', encoding='utf-8') as f: f.write(html)
    b.close()
" "$URL" "$OUT_DIR"
```

**If local image:** copy it into `<out>/source.png` and skip the URL step.

### 2. Extract design DNA

Read the source HTML + screenshot. Note in `<out>/_design-notes.md`:
- **Palette** — primary, secondary, accent colors (hex)
- **Typography** — font family (or closest free Google Font), heading scale, body size
- **Layout** — nav style, hero composition, section rhythm
- **Spacing** — section padding, element gaps
- **Interactive elements** — buttons (style, radius, shadow), forms, hover states
- **Visual hooks** — gradients, illustrations, 3D elements, animation cues

### 3. Generate the clone

For `--stack html`:
- Create `<out>/index.html` — semantic HTML5, no inline styles, no JavaScript unless animation requires it
- Create `<out>/styles.css` — CSS custom properties for colors + spacing, mobile-first responsive
- Match the source layout to **~90% fidelity** — don't pixel-chase the last 10% (waste of tokens)

For `--stack react`:
- Create `<out>/Page.jsx` — single functional component, Tailwind CSS classes
- Include responsive breakpoints (`sm:`, `md:`, `lg:`)
- Replace any third-party imagery URL with placeholders (`/api/placeholder/600/400`)

### 4. Replace content (CRITICAL)

The output is a **structural clone**, not a content clone. Replace:
- All copy with `[YOUR HEADLINE HERE]` placeholders
- All logos with `[Your Logo]` text
- All brand-specific colors with neutral defaults (the user picks brand colors next)
- All product/team photos with placeholder URLs

Tell the user: "I've cloned the **structure**. Run `/marketing-context` first to set your brand, then I'll fill the copy."

### 5. Output summary

Print:
```
Clone created: ./clones/<slug>/
  ├── source-desktop.png      (1440px reference screenshot)
  ├── source-mobile.png       (375px reference screenshot)
  ├── source.html             (original HTML for code hints)
  ├── _design-notes.md        (palette / typo / spacing extracted)
  ├── index.html              (your clone)
  └── styles.css              (your clone's stylesheet)

Next steps:
  1. Open ./clones/<slug>/index.html in a browser to verify
  2. Replace placeholder copy with your brand voice
  3. Swap color CSS vars in styles.css for your brand palette
```

## Cost / time

- Playwright capture: free, local, ~10-20s per URL
- Claude vision + code generation: ~1-3 cents in tokens for a typical landing page

## Common patterns

### "Clone Stripe's pricing page for my agency"
```
/clone-design https://stripe.com/pricing --stack html
```
→ Then `/pricing-page` skill replaces the placeholder tiers with your actual pricing.

### "I saw a great Dribbble design — clone the hero"
```
/clone-design ./Downloads/dribbble-hero.png --stack react
```
→ Pure visual rebuild, no HTML hints needed.

### "Make my client's site look like Linear"
```
/clone-design https://linear.app --out ./clients/acme/redesign/
```
→ Drops a clean redesign baseline into the client's folder.

## Failure modes

- **URL needs login** — Playwright won't sign in. Tell user the page is gated, ask for a screenshot instead.
- **Heavy JS-rendered page** — bump `wait_until='networkidle'` timeout to 60s; some sites take a while.
- **Source uses paid fonts** — pick the closest free Google Font and note the substitution.
- **3D / WebGL elements (Spline)** — can't replicate exactly. Use a CSS gradient placeholder + comment `<!-- TODO: add Spline scene -->`.
- **Output looks wrong** — re-run with `--full-page` if you only got viewport, or paste a specific section as image for targeted re-clone.

## Pairs well with

- `marketing-context` (run first → clone uses your brand voice)
- `hero-section` (clone has a weak hero → regenerate it with 4 variations)
- `cro-audit` (audit the cloned page for conversion before shipping)
- `claude-design` (escalate to claude.ai/design for tricky animations)

## Boundaries (read this)

This skill clones **visual patterns and layout structure** — composition, hierarchy,
spacing, color systems, typography. It does **not**:
- Copy brand-specific imagery, logos, or trademarked assets
- Reproduce copyrighted copy verbatim
- Replicate proprietary functionality (only static markup + styles)

Use it the way a designer uses Dribbble for inspiration — study the pattern, build
your own thing with it. Don't ship a pixel-clone of a competitor's actual marketing
page with the brand swapped; that's a lawsuit, not a launch.
