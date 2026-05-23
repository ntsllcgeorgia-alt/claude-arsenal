# Viktor Prompts Library — your agency Production Templates

A growing library of Viktor-style build prompts, sourced from you 2026-05-11+. Each template is a complete, paste-ready spec for a Viktor-tier cinematic build.

**Use these for CLIENT builds.** Do NOT use this aesthetic for the your agency-self homepage (which uses the tools-company aesthetic per V2-BRAND-STRATEGY.md v3 pivot).

## When to use Viktor templates

| Client type | Template fit |
|---|---|
| Tattoo studios | ✅ Template 01 (cinematic two-section) |
| Premium salons / spas / med-spas | ✅ Template 01 + variations |
| Photographers / videographers | ✅ Template 01 |
| Indie restaurants (destination angle) | ✅ Template 01 |
| Boutique fitness studios | ✅ Template 01 |
| Premium-local creative-class | ✅ Template 01 |
| Plumbers / casual / mass-market | ❌ Use traditional templates instead |
| Tools / SaaS / dev-focused | ❌ Use your agency-self aesthetic (tools company) |

## How to adapt a Viktor template for a specific client

1. **Read the template structure** (tech stack, CSS utilities, component specs)
2. **Swap content** — headlines, copy, video URLs, brand names, icons, stats
3. **Adapt color** — Viktor templates default to all-white text; swap accent based on client brand
4. **Generate new videos** via Higgsfield image-to-video (per the locked workflow — image first, then animate)
5. **Keep the structure intact** — the liquid-glass utilities, FadingVideo component, BlurText animation are house-locked patterns

---

## Template 01 — Cinematic Two-Section Landing Page (Space-Travel reference)

**Origin:** you paste 2026-05-11. Original example was for a space-travel concept; pattern is universal for premium client demos.

**Structure overview:**
- Single-page landing
- Two full-height sections (Hero + Capabilities)
- Both use looping background videos with custom JS crossfade
- Shared liquid-glass design system
- Framer Motion entrance animations
- All-white text, black bg, no overlays

**Tech stack (pinned, CDN-only):**

```html
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
<script src="https://unpkg.com/framer-motion@11.11.17/dist/framer-motion.js"></script>
<script>window.Motion = window.FramerMotion;</script>
```

- Body: `bg: #000`
- Page is React app mounted on `#root`
- All components: `<script type="text/babel">` exporting via `window.X = X`

**Fonts:**
Google Fonts: `family=Instrument+Serif:ital@0;1&family=Barlow:wght@300;400;500;600`

Tailwind config additions:
- `font-heading` → `'Instrument Serif', serif` (ALWAYS italic in use)
- `font-body` → `'Barlow', sans-serif`
- Default border radius override: `DEFAULT: "9999px"` (so bare `rounded` → pill)

**Liquid-glass utilities (exact CSS, in `<style>` block):**

Two variants:
- `.liquid-glass` — subtle, for nav/chips/cards
- `.liquid-glass-strong` — heavier blur, for primary CTA

```css
.liquid-glass {
  background: rgba(255,255,255,0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: "";
  position: absolute; inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%,
    rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%,
    rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%,
    rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
.liquid-glass-strong { /* same but: */
  backdrop-filter: blur(50px);
  box-shadow: 4px 4px 4px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.15);
}
.liquid-glass-strong::before { /* same but 0.5 / 0.2 / 0 / 0 / 0.2 / 0.5 stops */ }
```

**FadingVideo component (rAF-driven crossfade, no CSS transitions):**

Wraps `<video autoPlay muted playsInline preload="auto">` starting at `opacity: 0`.

Constants:
- `FADE_MS = 500`
- `FADE_OUT_LEAD = 0.55` seconds

Behavior:
- `fadeTo(target, duration)` uses `requestAnimationFrame`
- Reads current opacity from `video.style.opacity` — each new fade resumes from wherever the last left off
- Each call calls `cancelAnimationFrame` on the previous rAF id before starting
- On `loadeddata`: set opacity 0, `play()`, `fadeTo(1)`
- On `timeupdate`: if `fadingOutRef` not set AND `duration - currentTime <= 0.55 && > 0`, flip the ref and `fadeTo(0)`
- On `ended`: set opacity 0 → after `setTimeout(100ms)` reset `currentTime = 0`, `play()`, clear `fadingOutRef`, `fadeTo(1)`
- `loop` attribute is OFF (looping handled manually via `ended`)
- Cleanup on unmount: cancel rAF, remove listeners

**Section 1 — Hero (full viewport, black bg):**

Background video (120% width/height, top-aligned, centered horizontally — focal point is top of frame):
- src: `<HERO_VIDEO_URL>` (originally space-travel reference)
- class: `absolute left-1/2 top-0 -translate-x-1/2 object-cover object-top z-0`
- style: `{ width: "120%", height: "120%" }`
- NO overlay

z-10 layer holds: Navbar → Hero content (flex-1, centered) → Partners row

**Navbar (fixed top-4, px-8 / lg:px-16, z-50):**
- Left: 48×48 liquid-glass circle with italic serif lowercase brand letter (Instrument Serif)
- Center (desktop only): liquid-glass pill, `px-1.5 py-1.5`, holding 5 text links — Home, Voyages, Worlds, Innovation, Plan Launch — each `px-3 py-2 text-sm font-medium text-white/90 font-body`. Followed by white pill button "Claim a Spot" + ArrowUpRight (bg-white text-black, whitespace-nowrap)
- Right: 48×48 invisible spacer to balance logo

**Hero content (centered, pt-24 px-4):**
All Framer Motion: `initial: {filter: blur(10px), opacity: 0, y: 20}`, easeOut

1. **Badge (delay 0.4s):** liquid-glass rounded-full pill. Contains white pill chip "New" (`bg-white text-black px-3 py-1 text-xs font-semibold`) + text label (`text-sm text-white/90, pr-3`)
2. **Headline — BlurText component** (word-by-word). Classes: `text-6xl md:text-7xl lg:text-[5.5rem] font-heading italic text-white leading-[0.8] max-w-2xl justify-center tracking-[-4px]`
3. **Subheading (delay 0.8s):** `mt-4 text-sm md:text-base text-white max-w-2xl font-body font-light leading-tight`
4. **CTAs (delay 1.1s, flex items-center gap-6 mt-6):**
   - Primary: `liquid-glass-strong rounded-full px-5 py-2.5 text-sm font-medium text-white` with label + ArrowUpRight (h-5 w-5)
   - Secondary: bare text link, label + Play icon (h-4 w-4, filled)
5. **Stats row (delay 1.3s, flex items-stretch gap-4 mt-8):** Two liquid-glass cards, `p-5 w-[220px] rounded-[1.25rem]`, each:
   - Top: white 28×28 outline SVG icon
   - Bottom: large number in Instrument Serif italic white (`text-4xl tracking-[-1px] leading-none`)
   - Label below (`text-xs text-white font-body font-light mt-2`)

**Partners (bottom of hero, delay 1.4s):**
`flex flex-col items-center gap-4 pb-8`:
- liquid-glass rounded-full chip (`px-3.5 py-1 text-xs font-medium text-white`): partnership tagline
- Row of 5 names in Instrument Serif italic white, `text-2xl md:text-3xl tracking-tight, gap-12/md:gap-16`

**BlurText component (word-by-word blur-in):**
- IntersectionObserver triggers on 10% visibility
- Splits text by spaces
- Each word is a `motion.span` with:
  - `initial: {filter: 'blur(10px)', opacity: 0, y: 50}`
  - 3-step keyframes to `{filter: 'blur(5px)', opacity: 0.5, y: -5}` → `{filter: 'blur(0px)', opacity: 1, y: 0}`
  - `duration: 0.7` (stepDuration 0.35 × 2), `times: [0, 0.5, 1]`, `ease: easeOut`
- Stagger: `delay = (i * 100) / 1000` seconds
- `display: inline-block`, `marginRight: 0.28em` (not non-breaking-space — letter-spacing -4px eats nbsp)
- Parent `<p>`: `display: flex; flexWrap: wrap; justifyContent: center; rowGap: 0.1em`

**Section 2 — Capabilities (min-h-screen, black bg):**

Background video (full-bleed, no 120% scale):
- src: `<CAPABILITIES_VIDEO_URL>`
- class: `absolute inset-0 w-full h-full object-cover z-0`
- Same FadingVideo treatment
- No overlay

Content: `relative z-10 px-8 md:px-16 lg:px-20 pt-24 pb-10 flex flex-col min-h-screen`

**Header (mb-auto):**
- Kicker: `text-sm font-body text-white/80 mb-6` → `// Capabilities`
- Heading: `font-heading italic text-white text-6xl md:text-7xl lg:text-[6rem] leading-[0.9] tracking-[-3px]`:
  - Line 1 + `<br/>` + Line 2

**Three cards (`grid grid-cols-1 md:grid-cols-3 gap-6 mt-16`):**
Each is liquid-glass `rounded-[1.25rem] p-6 min-h-[360px] flex flex-col`.

Top row of each card (`flex items-start justify-between gap-4`):
- Left: 44×44 nested liquid-glass square (`rounded-[0.75rem]`) with white Material Icons SVG (`fill currentColor, h-6 w-6 text-white`)
- Right: `flex flex-wrap justify-end gap-1.5 max-w-[70%]` — 4 small liquid-glass pill tags (`rounded-full px-3 py-1 text-[11px] text-white/90 font-body whitespace-nowrap`)

Material icons used in original (swap per client):
- Image icon: `M5 21q-.825 0-1.412-.587T3 19V5q0-.825.588-1.412T5 3h14q.825 0 1.413.588T21 5v14q0 .825-.587 1.413T19 21H5Zm1-4h12l-3.75-5-3 4L9 13l-3 4Z`
- Movie icon: `M4 6.47 5.76 10H20v8H4V6.47M22 4h-4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4c-1.1 0-1.99.89-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4Z`
- Lightbulb icon: `M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1Zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7Z`

Middle: `flex-1` spacer

Bottom of each card (mt-6):
- Title `h3`: `font-heading italic text-white text-3xl md:text-4xl tracking-[-1px] leading-none`
- Body `p`: `mt-3 text-sm text-white/90 font-body font-light leading-snug max-w-[32ch]`

**Inline lucide-style SVG icons (currentColor stroke):**
- ArrowUpRight: 24×24, `M7 17L17 7` + `M7 7h10v10`, strokeWidth 2, round caps
- Play: 24×24 filled polygon `6 4 20 12 6 20 6 4`

**Hard rules (do not violate):**
- All text white; NO green, NO gradient backgrounds
- NO CSS transitions on videos — fades must be rAF-driven per FadingVideo spec
- Videos are full-bleed with no dark overlay; contrast comes from liquid-glass chrome
- Framer Motion dev warnings about list keys: suppress with console.error filter wrapper — they're benign

---

## Reusable patterns extracted from Template 01

These are the your agency-house-standard patterns. Use across ALL Viktor-style client builds:

1. **CDN-only React + Tailwind + Framer Motion stack** — no build step, drop-in
2. **Liquid-glass utility (2 variants)** — universal chrome for any premium feel
3. **FadingVideo component (rAF crossfade)** — replaces janky CSS transitions on loops
4. **BlurText component (word-by-word animation)** — premium typographic reveal
5. **Two-section (Hero + Body) structure** — works for any premium-local single-page demo
6. **All-white text on black, no overlays** — chrome carries the contrast
7. **Instrument Serif italic + Barlow body** — Viktor's go-to type stack (free Google Fonts, fine to use as-is OR swap for your agency's locked Archivo Black + Inter for your agency-branded client work)
8. **Stats row pattern (2 liquid-glass cards with icon + big number + label)** — universal social proof block
9. **3-card capability grid (icon + tags + title + body)** — universal services block
10. **Inline Material Icons via SVG path data** — no icon font dependency

---

---

## Template 02 — Velorah Glassmorphic Hero (minimal premium service)

**Origin:** you paste 2026-05-11. Single-page hero with fullscreen video, glassmorphic nav, cinematic typography. Deep-navy theme.

**Best for:** Premium SaaS landing, high-end service brands, "tools for thinkers" positioning, minimalist luxury

**Tech:** React + Vite + Tailwind + TypeScript + shadcn/ui

**Video:** Fullscreen `<video>` (autoPlay, loop, muted, playsInline), `absolute inset-0 w-full h-full object-cover z-0`. Reference URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260314_131748_f2ca2a28-fed7-44c8-b9a9-bd9acdd5ec31.mp4`

**Fonts:** Instrument Serif (display, always italic) + Inter 400/500 (body). CSS vars: `--font-display`, `--font-body`. Body uses `var(--font-body)`. Headings: inline `fontFamily: "'Instrument Serif', serif"`

**Color theme (dark, HSL CSS vars):**
- `--background: 201 100% 13%` (deep navy)
- `--foreground: 0 0% 100%` (white)
- `--muted-foreground: 240 4% 66%` (muted gray)
- `--primary: 0 0% 100%`, `--primary-foreground: 0 0% 4%`
- `--secondary, --muted, --accent: 0 0% 10%`
- `--border, --input: 0 0% 18%`

**Nav (relative z-10, flex justify-between, px-8 py-6, max-w-7xl):**
- Logo: brand name + `<sup className="text-xs">®</sup>`, `text-3xl tracking-tight`, Instrument Serif, text-foreground
- Nav links (hidden mobile, md:flex): 5 links, `text-sm text-muted-foreground hover:text-foreground transition-colors`
- CTA: liquid-glass rounded-full px-6 py-2.5, hover:scale-[1.03]

**Hero (relative z-10, flex-col centered, px-6 pt-32 pb-40 py-[90px]):**
- H1: `text-5xl sm:text-7xl md:text-8xl, leading-[0.95], tracking-[-2.46px], max-w-7xl, font-normal`, Instrument Serif. Specific words wrapped in `<em className="not-italic text-muted-foreground">` for color contrast
- Subtext: `text-muted-foreground text-base sm:text-lg max-w-2xl mt-8 leading-relaxed`
- CTA: liquid-glass rounded-full px-14 py-5 text-base mt-12, hover:scale-[1.03] cursor-pointer

**Liquid-glass utility:** Same as Template 01

**Animations (CSS keyframes):**
```css
@keyframes fade-rise {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-rise { animation: fade-rise 0.8s ease-out both; }
.animate-fade-rise-delay { animation: fade-rise 0.8s ease-out 0.2s both; }
.animate-fade-rise-delay-2 { animation: fade-rise 0.8s ease-out 0.4s both; }
```
- H1 → `animate-fade-rise`
- Subtext → `animate-fade-rise-delay`
- Hero CTA → `animate-fade-rise-delay-2`

**Hard rules:** No decorative blobs, no radial gradients, no overlays. Minimalist cinematic vertically-centered hero. Video provides ALL visual depth.

---

## Template 03 — Jack 3D Creator Portfolio (full multi-section portfolio)

**Origin:** you paste 2026-05-11. Multi-section creator portfolio with scroll-driven animations.

**Best for:** Designers, photographers, videographers, 3D artists, creative-class solopreneurs (the persona we locked at 25% of your agency pipeline). Whoever needs to show range + identity.

**Tech:** React + TypeScript + Tailwind + Framer Motion + Lucide React. Page title: `Jack -- 3D Creator` (swap per client).

**Global styles:**
- Background `#0C0C0C` on html, body, #root, main wrapper
- Font family: `'Kanit', sans-serif` (Google Fonts, weights 300-900)
- `.hero-heading` class: gradient text `background: linear-gradient(180deg, #646973 0%, #BBCCD7 100%)` with `-webkit-background-clip: text; -webkit-text-fill-color: transparent`
- Main wrapper: `overflowX: 'clip'`

**Section order:** Hero → Marquee → About → Services → Projects

### Section 1 — Hero (h-screen, flex-col, overflowX clip)

**Navbar:** 4 links (About, Price, Projects, Contact), `justify-between`, color `#D7E2EA`, font-medium, uppercase, tracking-wider. Sizes: `text-sm md:text-lg lg:text-[1.4rem]`. Padding: `px-6 md:px-10 pt-6 md:pt-8`. Hover: opacity 70% / 200ms.

**Hero heading h1:** `Hi, i'm jack` (lowercase i, curly apostrophe). `.hero-heading` gradient class. Font-black, uppercase, tracking-tight, leading-none, whitespace-nowrap, w-full. `text-[14vw] sm:text-[15vw] md:text-[16vw] lg:text-[17.5vw]`. Margin top `mt-6 sm:mt-4 md:-mt-5`. Wrapped in `overflow-hidden`.

**Bottom bar (flex justify-between items-end, pb-7 sm:pb-8 md:pb-10):**
- Left: paragraph "a 3d creator driven by crafting striking and unforgettable projects", color `#D7E2EA`, font-light, uppercase, tracking-wide, leading-snug. Font: `clamp(0.75rem, 1.4vw, 1.5rem)`. Max-w: `max-w-[160px] sm:max-w-[220px] md:max-w-[260px]`
- Right: ContactButton component (see below)

**Hero Portrait:** Centered absolute. Wrapped in Magnet component (mouse-following).
- Image: `https://shrug-person-78902957.figma.site/_components/v2/d24c01ad3a56fc65e942a1f501eb73db42d7cf9a/Rectangle_40443.81459862.png`
- Magnet: padding 150, strength 3, activeTransition "transform 0.3s ease-out", inactiveTransition "transform 0.6s ease-in-out"
- Positioning: `absolute left-1/2 -translate-x-1/2 z-10`
- Width: `w-[280px] sm:w-[360px] md:w-[440px] lg:w-[520px]`
- Mobile: `top-1/2 -translate-y-1/2`. Sm+: `sm:top-auto sm:translate-y-0 sm:bottom-0`

**FadeIn delays:** Navbar 0 / y-20, Heading 0.15 / y40, Left text 0.35 / y20, Contact button 0.5 / y20, Portrait 0.6 / y30

### Section 2 — Marquee (two horizontal-scroll rows of motionsites.ai GIFs)

Background `#0C0C0C`. Padding: `pt-24 sm:pt-32 md:pt-40 pb-10`.

21 GIF URLs from motionsites.ai (preserved here for reference — these are NOT for production use without re-hosting):
- `hero-space-voyage-preview-eECLH3Yc.gif`
- `hero-codenest-preview-Cgppc2qV.gif`
- ... (full list of 21 reels for use as inspiration / reference imagery — re-host or substitute on production)

Row 1: first 11, tripled for seamless scroll, moves RIGHT on page scroll (`translateX(offset - 200)`)
Row 2: remaining 10, tripled, moves LEFT (`translateX(-(offset - 200))`)
Scroll offset: `(window.scrollY - sectionTop + window.innerHeight) * 0.3`
Tile size: 420×270, `rounded-2xl`, `object-cover`, lazy-loaded, `gap-3`. willChange: 'transform'. Passive scroll listener.

### Section 3 — About (min-h-screen centered)

Padding: `px-5 sm:px-8 md:px-10 py-20`.

**4 decorative 3D images** positioned absolutely in corners (moon icon top-left, 3D object bottom-left, lego icon top-right, 3D group bottom-right). Each fades in with x-translate.

**Heading:** "About me" using `.hero-heading` gradient, font-black, uppercase, leading-none, tracking-tight, centered. Font: `clamp(3rem, 12vw, 160px)`. FadeIn: delay 0, y 40.

**Animated paragraph:** Character-by-character scroll-driven opacity. Each char: opacity 0.2 → 1 based on scroll progress. Framer Motion `useScroll` targeting the paragraph, offset `['start 0.8', 'end 0.2']`. Each char uses invisible placeholder + absolute positioned animated span.

Contact button below text. Gaps: heading→text `gap-10 sm:gap-14 md:gap-16`, text→button `gap-16 sm:gap-20 md:gap-24`.

### Section 4 — Services (light theme)

White background `#FFFFFF`, rounded top corners `rounded-t-[40px] sm:rounded-t-[50px] md:rounded-t-[60px]`. Padding: `px-5 sm:px-8 md:px-10 py-20 sm:py-24 md:py-32`.

**Heading:** "Services" color `#0C0C0C`, font-black uppercase, font: `clamp(3rem, 12vw, 160px)`. Margin: `mb-16 sm:mb-20 md:mb-28`.

**5 service items, vertical list, max-w-5xl, centered:**
1. 3D Modeling
2. Rendering
3. Motion Design
4. Branding
5. Web Design

Each: horizontal layout. Number left (font-black, `clamp(3rem, 10vw, 140px)`, `#0C0C0C`). Name + description stacked right. Name font-medium uppercase `clamp(1rem, 2.2vw, 2.1rem)`. Description font-light leading-relaxed max-w-2xl `clamp(0.85rem, 1.6vw, 1.25rem)` opacity 0.6. Items separated by 1px borders `rgba(12, 12, 12, 0.15)`. Padding: `py-8 sm:py-10 md:py-12`. Staggered FadeIn each item delays by `i * 0.1`.

### Section 5 — Projects (sticky stacking cards)

Dark `#0C0C0C`, rounded top corners, pulled up with `-mt-10 sm:-mt-12 md:-mt-14, z-10`.

**Heading:** "Project" using `.hero-heading` gradient (note: singular intentional).

**3 sticky-stacking project cards** that scale down as you scroll past them. Card stacking via Framer Motion `useScroll` and `useTransform`. Each card: `sticky top-24 md:top-32` inside `h-[85vh]` container.

**Scale calc:** `targetScale = 1 - (totalCards - 1 - index) * 0.03`. Offset: `top: ${index * 28}px`.

**Card design:** `rounded-[40px] sm:rounded-[50px] md:rounded-[60px]`, `border-2 border-[#D7E2EA]`, background `#0C0C0C`, padding `p-4 sm:p-6 md:p-8`.

**Card layout:**
- Top row: huge number, category label, project name, ghost button "Live Project"
- Bottom row: 2-column image grid (40%/60%). Left has 2 stacked images. Right has 1 tall image. All `rounded-[40px]+`. Heights: left top `clamp(130px, 16vw, 230px)`, left bottom `clamp(160px, 22vw, 340px)`.

**3 projects in original:** Nextlevel Studio (Client), Aura Brand Identity (Personal), Solaris Digital (Client). All images CloudFront URLs preserved in the user's original paste for reference.

### Reusable components from Template 03

**ContactButton:** Rounded-full pill, gradient bg `linear-gradient(123deg, #18011F 7%, #B600A8 37%, #7621B0 72%, #BE4C00 100%)`. Inner shadow `0px 4px 4px rgba(181, 1, 167, 0.25), 4px 4px 12px #7721B1 inset`. White 2px outline with -3px offset. White text font-medium uppercase tracking-widest. Sizes: `px-8 py-3 sm:px-10 sm:py-3.5 md:px-12 md:py-4`. Label: "Contact Me".

**LiveProjectButton:** Ghost outline pill. Rounded-full, `border-2 border-[#D7E2EA]`, text `#D7E2EA`, font-medium uppercase tracking-widest. `px-8 py-3 sm:px-10 sm:py-3.5`. Hover `bg-[#D7E2EA]/10`.

**FadeIn:** Framer Motion wrapper with `whileInView`, `viewport={{ once: true, margin: "50px", amount: 0 }}`. Accepts delay, duration (0.7), x (0), y (30). Easing: `[0.25, 0.1, 0.25, 1]`. Uses `motion.create()` for dynamic element types.

**Magnet:** Mouse-following magnetic hover. Tracks mouse position relative to element center, applies `translate3d` transform divided by strength factor. Activates within padding distance of edge. Smooth: 0.3s ease-out in, 0.6s ease-in-out out. `willChange: 'transform'`.

**AnimatedText:** Char-by-char scroll-reveal. Each char opacity 0.2 → 1 based on position in text relative to scroll progress. `useScroll` on the paragraph, offset `['start 0.8', 'end 0.2']`. Each char: invisible placeholder + absolute-positioned animated span.

### Dependencies for Template 03
- `react`, `react-dom` (^18.3.1)
- `framer-motion` (^12.38.0)
- `lucide-react` (^0.344.0)
- `tailwindcss` (^3.4.1)
- `vite`, `typescript`

---

## Template 04 — SkyElite Private Jet Landing (clean luxury, light theme)

**Origin:** you paste 2026-05-11. Premium light-theme landing with overlapping typography.

**Best for:** Travel/hospitality, premium service businesses that need APPROACHABLE luxury (not dark cinematic). When the client wants "premium but warm" not "premium but mysterious."

**Tech:** React + TypeScript + Tailwind + Lucide React. `useState` for mobile menu toggle.

**Video:** Fullscreen `<video>` (autoplay, muted, loop, playsInline), `object-cover`, full viewport `h-screen`. Reference URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_091828_e240eb17-6edc-4129-ad9d-98678e3fd238.mp4`

**Typography:** Inter (Google Fonts, weights 400/500/600/700). Applied to entire body via CSS.

**Container:** Outer `min-h-screen, bg-gray-50`. Hero `relative h-screen overflow-hidden`. Content wrapper `relative h-full flex-col`. Main area `flex-1 flex items-center justify-center`.

**Nav:**
- Brand "SkyElite" left (`text-2xl font-semibold text-gray-900`)
- Desktop menu (hidden mobile, `md:flex`): Start, Story, Rates, Benefits, FAQ
- Links: `gray-900 hover:text-gray-700 transition`
- Mobile: hamburger Menu/X (Lucide React)
- Mobile menu: dropdown `white/95 opacity, backdrop blur, rounded, shadow`
- Container: `max-w-7xl mx-auto px-8 py-6`

**Hero (centered, -mt-80 to pull up):**
- Label: "PRIVATE JETS" — `text-sm font-semibold gray-600 tracking-wider mb-4`, uppercase
- Heading (overlapping two-line effect):
  - Line 1: "Premium." — `text-6xl md:text-7xl lg:text-8xl font-normal text-gray-500 leading-none tracking-tighter`
  - Line 2: "Accessible." — same size, color `#202A36`, `margin-top: -12px` for overlap
- Subtitle: "Your dedication deserves recognition." — `text-lg md:text-xl gray-600 mb-6 max-w-2xl`
- CTAs (gap-4, centered):
  - "Discover": `px-4 py-2 rounded-full bg-gray-300 text-gray-800 font-medium hover:bg-gray-400`
  - "Book Now": `px-4 py-2 rounded-full white bg-color #202A36 hover #1a2229 transition-colors`

**Hard rules:**
- Clean, modern, premium-looking
- Smooth interactions throughout
- Mobile-first responsive (sm/md/lg breakpoints)
- All transitions via `transition-colors` class

---

## Use-case matrix — updated with Templates 02, 03, 04

| Client type | Template fit | Why |
|---|---|---|
| Tattoo studios | 01 or 02 | Dark cinematic suits the aesthetic |
| Premium salons | 01 or 02 | Editorial/glassmorphic both work |
| Photographers / 3D artists / designers | **03** | Portfolio structure with sticky cards |
| Indie restaurants (destination) | 01 | Hero video + capabilities cards |
| Boutique fitness | 02 | Minimal/glass works |
| Travel / hospitality / spas | **04** | Light luxury, approachable |
| Premium service (lawyers, consultants) | 04 | Clean professional |
| Med-spas | 02 or 04 | Depending on brand voice |
| Plumbers / casual mass-market | None | Traditional templates only |
| Tools / SaaS / dev-focused | None | Use your agency-self aesthetic (tools company) |

---

---

## Template 05 — Aethera Cinematic Hero (LIGHT theme variant)

**Origin:** you paste 2026-05-11. Cinematic hero with looping video background, white/black/gray palette. Aethera reference brand.

**Best for:** Premium service brands wanting CLEAN/MINIMAL/LIGHT (not dark cinematic). Think: high-end consultancies, premium hospitality, luxury wellness, fashion-adjacent brands. Approachable luxury.

**Tech:** React + Vite + Tailwind + TypeScript

**Fonts:**
- Display (headings, logo): Instrument Serif
- Body (nav, descriptions): Inter
- Import in `/src/styles/fonts.css`

**Video background:**
- URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_083109_283f3553-e28f-428b-a723-d639c617eb2b.mp4`
- Position: `top: '300px', inset: 'auto 0 0 0'`
- Custom fade loop via `useEffect` + `useRef`:
  - `requestAnimationFrame` continuously monitors `currentTime` and `duration`
  - Fade in 0.5s at start (opacity 0→1)
  - Fade out 0.5s before end (opacity 1→0)
  - On `ended`: opacity to 0, wait 100ms, reset `currentTime = 0`, `play()` again
  - Manual seamless loop
- Gradient overlays: `absolute inset-0 bg-gradient-to-b from-background via-transparent to-background`

**Nav:**
- Logo: "Aethera®" (registered as superscript), `text-3xl tracking-tight`, Instrument Serif, color `#000000`
- Menu: Home (`#000000`), Studio/About/Journal/Reach Us (all `#6F6F6F`), `text-sm transition-colors`
- CTA: "Begin Journey", `rounded-full px-6 py-2.5 text-sm`, black bg, white text, hover scale 1.03
- Layout: `flex justify-between, px-8 py-6, max-w-7xl mx-auto`

**Hero (paddingTop: 'calc(8rem - 75px)', pb-40):**
- Centered: `flex flex-col items-center justify-center text-center, px-6`
- Headline: "Beyond silence, we build the eternal."
  - `text-5xl sm:text-7xl md:text-8xl, max-w-7xl, font-normal`, Instrument Serif
  - `line-height: 0.95, letter-spacing: -2.46px`
  - Main color `#000000`, italic emphasized words ("silence," and "the eternal.") `#6F6F6F`
  - Animation: `animate-fade-rise`
- Description: `text-base sm:text-lg, max-w-2xl, mt-8, leading-relaxed, color #6F6F6F`. Animation: `animate-fade-rise-delay`
- CTA: "Begin Journey", `rounded-full px-14 py-5 text-base mt-12, black bg, white text`, hover scale 1.03. Animation: `animate-fade-rise-delay-2`

**Colors (locked):**
- Background: `#FFFFFF`
- Headlines/logos/buttons: `#000000`
- Descriptions/menu items: `#6F6F6F`
- Button text: `#FFFFFF`

**Animations (`/src/styles/theme.css`):**
```css
@keyframes fade-rise { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
.animate-fade-rise { animation: fade-rise 0.8s ease-out both; }
.animate-fade-rise-delay { animation: fade-rise 0.8s ease-out 0.2s both; }
.animate-fade-rise-delay-2 { animation: fade-rise 0.8s ease-out 0.4s both; }
```

**Layout:**
- Container: `relative min-h-screen w-full overflow-hidden`
- Background video layer (z-0)
- Gradient overlay
- Navbar (z-10)
- Hero (z-10)

---

## Template 06 — Asme Liquid Glass Single Hero (dark cinematic, signup-focused)

**Origin:** you paste 2026-05-11. Single-page hero. Dark theme with liquid-glass. Built around email-capture intent.

**Best for:** Waitlist / coming-soon / launch landing pages where the ONE goal is email signup. Pre-launch products. Newsletter-driven creators.

**Tech:** Vite + React 18 + TypeScript + Tailwind CSS 3 + lucide-react

**Video background:**
- URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260328_115001_bcdaa3b4-03de-47e7-ad63-ae3e392c32d4.mp4`
- Full-screen muted autoplay, `object-cover`
- Shifted down 17% (`translate-y-[17%]`) — top cropped, interesting content in lower frame
- Custom JS fade system (no CSS transitions, identical pattern to Template 01)
- Outer container: `min-h-screen bg-black overflow-hidden`

**Font:** Google "Instrument Serif" (regular + italic). Import: `@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap')`. Heading uses inline `fontFamily: "'Instrument Serif', serif"`

**Liquid-glass CSS:** Identical to Template 01

**Layout (single flex column):**

**Navbar (relative z-20, pl-6 pr-6 py-6):**
- Inner: `rounded-full px-6 py-3 flex items-center justify-between max-w-5xl mx-auto`
- Left: Globe icon (24px) + "Asme" white `font-semibold text-lg`, `gap-2`
- Next to logo (`gap-8`): nav links "Features", "Pricing", "About" — hidden mobile (`md:`), `text-white/80 hover:text-white text-sm font-medium`
- Right (`gap-4`): "Sign Up" plain white text button, "Login" liquid-glass `rounded-full px-6 py-2` button

**Hero content (relative z-10 flex-1 flex flex-col items-center justify-center px-6 py-12 text-center -translate-y-[20%]):**
- Heading: "Built for the curious" — `text-5xl md:text-6xl lg:text-7xl text-white mb-8 tracking-tight whitespace-nowrap`, Instrument Serif
- Below in `max-w-xl w-full space-y-4`:
  - Email input: liquid-glass `rounded-full pl-6 pr-2 py-2 flex items-center gap-3`. Transparent email input (`placeholder "Enter your email" text-white placeholder:text-white/40 text-base`). White circular submit button (`bg-white rounded-full p-3 text-black`) with ArrowRight icon (20px)
  - Subtitle: `text-white text-sm leading-relaxed px-4` — "Stay updated..."
- Manifesto button: centered, liquid-glass `rounded-full px-8 py-3 text-white text-sm font-medium hover:bg-white/5 transition-colors`

**Social icons footer (relative z-10 flex justify-center gap-4 pb-12):**
- 3 circular icon buttons, each liquid-glass `rounded-full p-4 text-white/80 hover:text-white hover:bg-white/5 transition-all`
- Icons (lucide-react, 20px): Instagram, Twitter, Globe
- Each has aria-label

---

## Template 07 — Asme Full Multi-Section Build (5-section premium build)

**Origin:** you paste 2026-05-11. Same brand as Template 06, but EXPANDED to full multi-section landing. Use this when client needs more than just a hero (waitlist) — needs a full story.

**Best for:** Full brand-launch sites, premium creator brands, agencies, products that need depth (5 sections: Hero → About → Featured Video → Philosophy → Services).

**Tech:** React + TypeScript + Vite + Tailwind + framer-motion + lucide-react. Page bg-black. Font: Google "Instrument Serif" italic + regular.

**Liquid-glass CSS:** Same as Template 01

### Section 1 — Hero (full viewport)
- Container: `min-h-screen overflow-hidden relative flex flex-col`
- Background video: `absolute inset-0 w-full h-full object-cover object-bottom`. URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260405_074625_a81f018a-956b-43fb-9aee-4d1508e30e6a.mp4`
- Muted, autoPlay, playsInline, preload="auto"
- Vanilla JS fade logic via refs (same pattern as T01/T06)

**Navbar:** liquid-glass rounded-full pill, `max-w-5xl mx-auto, px-6 py-3, flex between`. Left: Globe + "Asme". Right: "Sign Up" + "Login".

**Hero content (relative z-10, flex-1 flex-col centered, px-6 py-12 text-center, -translate-y-[20%]):**
- Heading: `text-7xl md:text-8xl lg:text-9xl text-white tracking-tight whitespace-nowrap` Instrument Serif. Text: "Know it then <em italic>all</em>."
- Email input pill (same as Template 06)
- Subtitle (same as Template 06)
- Manifesto button (same as Template 06)

**Social icons footer (same as Template 06)**

### Section 2 — About (framer-motion useInView)
- `bg-black pt-32 md:pt-44 pb-10 md:pb-14 px-6 overflow-hidden`
- Subtle radial gradient overlay: `bg-[radial-gradient(ellipse_at_top,_rgba(255,255,255,0.03)_0%,_transparent_70%)]`
- Label "About Us": `text-white/40 text-sm tracking-widest uppercase`. Animates opacity 0→1 + y 20→0, duration 0.6
- Heading: `text-4xl md:text-6xl lg:text-7xl text-white leading-[1.1] tracking-tight`. Animates opacity 0→1 + y 40→0, duration 0.8, delay 0.1
- Text structure:
  - "Pioneering" then "ideas" (Instrument Serif italic, `text-white/60`) "for"
  - `<br/>` (hidden mobile)
  - "minds that" then "create, build, and inspire." (all Instrument Serif italic `text-white/60`)

### Section 3 — Featured Video
- `bg-black pt-6 md:pt-10 pb-20 md:pb-32 px-6 overflow-hidden, max-w-6xl`
- Container: `rounded-3xl overflow-hidden aspect-video`. Animates opacity 0→1 + y 60→0, duration 0.9
- Video: `w-full h-full object-cover`, muted/autoPlay/loop/playsInline/preload="auto". URL: `hf_20260402_054547_9875cfc5-155a-4229-8ec8-b7ba7125cbf8.mp4`
- Gradient overlay: `bg-gradient-to-t from-black/60 via-transparent to-transparent`
- Bottom overlay (`absolute bottom-0 left-0 right-0 p-6 md:p-10`):
  - Flex row desktop, column mobile
  - Left: liquid-glass `rounded-2xl p-6 md:p-8 max-w-md`. Label "Our Approach" (`text-white/50 text-xs tracking-widest uppercase mb-3`). Body (`text-white text-sm md:text-base leading-relaxed`).
  - Right: "Explore more" button (liquid-glass `rounded-full px-8 py-3 white text-sm font-medium`) with `whileHover={{scale: 1.05}}`, `whileTap={{scale: 0.95}}`

### Section 4 — Philosophy / Innovation × Vision
- `bg-black py-28 md:py-40 px-6 overflow-hidden, max-w-6xl`
- Heading: `text-5xl md:text-7xl lg:text-8xl text-white tracking-tight mb-16 md:mb-24`. Text: "Innovation" + italic "x" (Instrument Serif `text-white/40`) + "Vision". Animates opacity 0→1 + y 40→0, duration 0.8
- Two-column grid (`grid-cols-1 md:grid-cols-2 gap-8 md:gap-12`):
  - Left video: `rounded-3xl overflow-hidden aspect-[4/3]`. Animates opacity 0→1 + x -40→0. URL: `hf_20260307_083826_e938b29f-a43a-41ec-a153-3d4730578ab8.mp4`
  - Right text block: Animates opacity 0→1 + x 40→0. Two sub-blocks separated by `w-full h-px bg-white/10` divider.
    - Block 1: Label "Choose your space" + body
    - Block 2: Label "Shape the future" + body

### Section 5 — Services / What We Do
- `bg-black py-28 md:py-40 px-6 overflow-hidden, max-w-6xl`
- Radial gradient: `bg-[radial-gradient(ellipse_at_center,_rgba(255,255,255,0.02)_0%,_transparent_60%)]`
- Header row: flex between "What we do" (`text-3xl md:text-5xl text-white tracking-tight`) and "Our services" (`text-white/40 text-sm`, hidden mobile). Animates opacity 0→1 + y 30→0, duration 0.7
- Two-card grid (`grid-cols-1 md:grid-cols-2 gap-6 md:gap-8`):
  - Each card: liquid-glass `rounded-3xl overflow-hidden` group class. Animates opacity 0→1 + y 50→0, duration 0.8, staggered by 0.15s
  - Card video: `aspect-video, object-cover, transition-transform duration-700 group-hover:scale-105`. Gradient overlay: `from-black/40 to-transparent`
  - Card body (`p-6 md:p-8`): tag label (uppercase tracking-widest `text-white/40 text-xs`), ArrowUpRight in liquid-glass `rounded-full p-2`, title (`text-white text-xl md:text-2xl mb-3 tracking-tight`), description (`text-white/50 text-sm leading-relaxed`)

**Card 1 video URL:** `hf_20260314_131748_f2ca2a28-fed7-44c8-b9a9-bd9acdd5ec31.mp4`. Tag "Strategy". Title "Research & Insight".
**Card 2 video URL:** `hf_20260324_151826_c7218672-6e92-402c-9e45-f1e0f454bdc4.mp4`. Tag "Craft". Title "Design & Execution".

---

## Updated use-case matrix — Templates 01-07

| Client type | Best template | Why |
|---|---|---|
| Tattoo studios | **01** or **02** | Dark cinematic / glassmorphic |
| Premium salons / med-spas | **01** or **02** | Editorial / minimal premium |
| Photographers / 3D artists / designers | **03** | Full portfolio with sticky cards |
| Indie restaurants (destination) | **01** | Hero video + capabilities |
| Boutique fitness | **02** | Minimal liquid-glass |
| Travel / hospitality / luxury wellness | **04** or **05** | Light approachable luxury |
| Premium consultants / lawyers | **04** or **05** | Clean professional |
| Waitlist / pre-launch / newsletter brand | **06** | Single-goal email capture |
| Full agency / creator brand launch | **07** | 5-section depth |
| Premium service with story | **07** | Hero + About + Featured + Philosophy + Services |
| your agency-self homepage | **none of these** | Use tools-company aesthetic instead |
| Plumbers / mass-market | **none** | Traditional templates only |

---

## Common patterns across ALL Viktor templates (the house DNA)

These appear in 5+ of the 7 templates. They are your agency's locked Viktor production patterns:

1. **Liquid-glass utility** (T01, T02, T06, T07) — universal glass chrome
2. **Instrument Serif italic display** (T01, T02, T05, T06, T07) — premium type signature
3. **Fullscreen background video with custom rAF fade loop** (T01, T05, T06, T07) — no CSS transitions, manual seamless loop
4. **Italic-for-emphasis pattern** (T02, T05, T07) — words within heading rendered italic for color/style contrast
5. **Animate-fade-rise variants** (T02, T05) — staggered entrance animations
6. **CDN-only or Vite tech stack** — drop-in, no heavy build
7. **All-white text on dark video** (T01, T02, T06, T07) — chrome carries contrast
8. **Lucide-react icons** (T02, T03, T04, T06, T07) — universal icon system
9. **Framer Motion for entrance + scroll reveals** (T01, T03, T07) — premium motion language
10. **Hot pink or single-accent strategy** — your agency's signature pink (#FF1493) is the swap-in for any "accent color" mentioned in Viktor templates

---

---

## Template 08 — Michael Smith Dark Portfolio (GSAP + HLS, multi-section, Bento + Parallax)

**Origin:** you paste 2026-05-11. Sophisticated multi-section dark portfolio with HLS video, loading screen counter, GSAP scroll animations, Bento grid, parallax gallery.

**Best for:** High-end personal portfolios (designers, directors, creative leads), agencies wanting maximum sophistication. The most complex template in the library — use for clients who need to demonstrate sophistication beyond what T01-T07 deliver.

**Tech:** React + Vite + Tailwind + TypeScript + GSAP + Framer Motion + hls.js + react-router-dom + tailwindcss-animate

**Fonts:** Inter (300-700) + Instrument Serif (italic 400). CSS vars `--font-body`, `--font-display`. Tailwind: `font-body`, `font-display`.

**CSS custom properties (HSL, no `hsl()` wrapper — Tailwind adds it):**
```css
--bg: 0 0% 4%;
--surface: 0 0% 8%;
--text: 0 0% 96%;
--muted: 0 0% 53%;
--stroke: 0 0% 12%;
--accent: 0 0% 96%;
```

**Tailwind custom colors:** `bg`, `surface`, `text-primary`, `muted`, `stroke` — all `hsl(var(--*))`.

**Accent gradient (used on logo ring, hover borders, progress bars):**
`linear-gradient(90deg, #89AACC 0%, #4E85BF 100%)` — utility class `.accent-gradient`

**Custom animations (index.css):**
- `@keyframes scroll-down` — `translateY(-100%)` → `translateY(200%)`, 1.5s ease-in-out infinite
- `@keyframes role-fade-in` — `opacity 0 + translateY(8px)` → `opacity 1 + translateY(0)`, 0.4s ease-out
- `@keyframes gradient-shift` — `background-position 0% 50% → 100% 50% → 0% 50%`, 6s ease infinite (for animated gradient borders)

Forced dark theme — no light mode toggle. Body: `bg-bg text-text-primary`.

### Section 1 — Loading Screen
Full-screen overlay (`fixed inset-0 z-[9999] bg-bg`). Uses `requestAnimationFrame` counter 000→100 over 2700ms.
- Top-left: "Portfolio" label (`text-xs text-muted uppercase tracking-[0.3em]`). Animates y:-20→0, opacity 0→1
- Center: Rotating words `["Design", "Create", "Inspire"]` cycle every 900ms. `AnimatePresence mode="wait"` with y:20→0→-20 transitions. `text-4xl md:text-6xl lg:text-7xl font-display italic text-text-primary/80`
- Bottom-right: Counter display `text-6xl md:text-8xl lg:text-9xl font-display text-text-primary tabular-nums`. Shows `String(count).padStart(3, "0")`
- Bottom progress bar: `h-[3px] bg-stroke/50`, inner div with `.accent-gradient`, `scaleX(count/100)`, `box-shadow: 0 0 8px rgba(137, 170, 204, 0.35)`
- On complete (count=100): 400ms delay → `onComplete()`

### Section 2 — Hero
Full-viewport with HLS background video.
- **HLS source:** `https://stream.mux.com/Aa02T7oM1wH5Mk5EEVDYhbZ1ChcdhRsS2m1NYyx4Ua1g.m3u8`
- Uses `hls.js` — if `Hls.isSupported()`, create HLS instance; else native HLS via `video.src`
- Video: `autoPlay muted loop playsInline`, centered with `-translate-x-1/2 -translate-y-1/2`
- Dark overlay `bg-black/20`
- Bottom fade `h-48 bg-gradient-to-t from-bg to-transparent`

**Navbar (fixed top center, `z-50 flex justify-center pt-4 md:pt-6 px-4`):**
- Pill: `inline-flex items-center rounded-full backdrop-blur-md border border-white/10 bg-surface px-2 py-2`. Adds `shadow-md shadow-black/10` when scrollY > 100
- Logo: 9×9 circle with accent gradient border (reverses on hover). Inner `bg-bg` circle with "JA" font-display italic
- Divider: `w-px h-5 bg-stroke mx-1`
- Nav links: ["Home", "Work", "Resume"] — `text-xs sm:text-sm rounded-full px-3 sm:px-4 py-1.5 sm:py-2`. Active: `text-text-primary bg-stroke/50`. Inactive: `text-muted hover:text-text-primary hover:bg-stroke/50`
- "Say hi" button: gradient hover border (using absolute span `inset: -2px`)

**Hero content (centered, z-10):**
- Eyebrow: "COLLECTION '26" — `text-xs text-muted uppercase tracking-[0.3em] mb-8`. Class `blur-in`
- Name: "Michael Smith" — `text-6xl md:text-8xl lg:text-9xl font-display italic leading-[0.9] tracking-tight text-text-primary mb-6`. Class `name-reveal`
- Role line: "A {role} lives in Chicago." — roles cycle every 2s through `["Creative", "Fullstack", "Founder", "Scholar"]`. Role word: `font-display italic text-text-primary animate-role-fade-in inline-block with key={roleIndex}`
- Description: `text-sm md:text-base text-muted max-w-md mb-12`
- CTA Buttons (inline-flex gap-4):
  - "See Works" solid: `bg-text-primary text-bg`. Hover: `bg-bg text-text-primary` with accent gradient border ring
  - "Reach out..." outlined: `border-2 border-stroke bg-bg text-text-primary`. Hover: `border-transparent` with accent gradient border ring
  - Both: `rounded-full text-sm px-7 py-3.5 hover:scale-105`

**GSAP entrance timeline (`ease: "power3.out"`):**
- `.name-reveal`: opacity 0→1, y 50→0, 1.2s, delay 0.1s
- `.blur-in`: opacity 0→1, filter blur(10px)→blur(0px), y 20→0, 1s, stagger 0.1, delay 0.3s

**Scroll indicator (bottom-center):** `text-xs text-muted uppercase tracking-[0.2em]` "SCROLL" + `w-px h-10 bg-stroke` line with `.animate-scroll-down` highlight

### Section 3 — Selected Works (Bento Grid)
`bg-bg py-12 md:py-16`. Inner: `max-w-[1200px] mx-auto px-6 md:px-10 lg:px-16`

Header (Framer Motion `whileInView`): eyebrow line + heading "Featured *projects*" (italic word) + subtext + "View all work" button.

Bento grid: `grid grid-cols-1 md:grid-cols-12 gap-5 md:gap-6`. Column spans alternate 7/5/5/7. 4 project cards: Automotive Motion, Urban Architecture, Human Perspective, Brand Identity.

Each card: `bg-surface border border-stroke rounded-3xl` with aspect ratios. Contains background image with `object-cover group-hover:scale-105`, halftone overlay `radial-gradient(circle, #000 1px, transparent 1px) at 4×4px opacity-20 mix-blend-multiply`, hover overlay `bg-bg/70 opacity-0→1 + backdrop-blur-lg`, hover label pill with animated gradient border.

### Section 4 — Journal
`bg-bg py-16 md:py-24`. Same header pattern (eyebrow + "Recent *thoughts*" + subtext + "View all").

4 journal entries as horizontal pills (`rounded-[40px] sm:rounded-full`) with titles, images, read times, dates. Each: `flex items-center gap-6 p-4 bg-surface/30 hover:bg-surface border border-stroke`.

### Section 5 — Explorations (Parallax Gallery)
`min-h-[300vh]` for scroll-driven parallax.

- **Layer 1 — Pinned Center (z-10):** `h-screen` pinned via `GSAP.ScrollTrigger.create({ pin: contentRef, pinSpacing: false })`. Eyebrow "Explorations" + heading "Visual *playground*" + subtext + Dribbble button
- **Layer 2 — Parallax Columns (z-20, absolute):** `grid grid-cols-2 gap-12 md:gap-40` in `max-w-[1400px]`. 6 items in 2 cols with GSAP scroll-driven parallax movement. Cards: `aspect-square max-w-[320px]` with rotation, lightbox on click.

### Section 6 — Stats
`bg-bg py-16 md:py-24`. 3-column grid: 20+ Years Experience, 95+ Projects Done, 200% Satisfied Clients.

### Section 7 — Contact / Footer
`bg-bg pt-16 md:pt-20 pb-8 md:pb-12 overflow-hidden`.

- Same HLS source as hero, flipped vertically (`scale-y-[-1]`). Heavier overlay `bg-black/60`
- GSAP marquee: "BUILDING THE FUTURE • " ×10. `xPercent: -50, duration 40, ease "none", repeat -1`
- CTA: Email button `mailto:hello@michaelsmith.com` with gradient hover border ring
- Footer: Social links (Twitter, LinkedIn, Dribbble, GitHub) + green pulsing dot + "Available for projects"

---

## Template 09 — Cinematic Streaming Hero (single-section, bottom-blur, blur-fade-up)

**Origin:** you paste 2026-05-11. Full-viewport cinematic hero with bottom-blur overlay (no dark gradient — pure blur). For streaming/movie/cinema-themed brands.

**Best for:** Premium video-first brands (filmmakers, video production, streaming services, entertainment studios). When the brand vibe is "cinema."

**Tech:** React + Tailwind + lucide-react. Google Font: Inter (300-700).

**Background video:** Full-screen muted autoplay loop, `object-cover`, `fixed positioned z-0`. URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260406_094145_4a271a6c-3869-4f1c-8aa7-aeb0cb227994.mp4`

**Bottom blur overlay (KEY — no gradient darkening):** Single fixed full-screen div with `backdrop-blur-xl`. Uses CSS mask so blur only appears at bottom, fading to transparent toward middle.
- Mask: `mask-image: linear-gradient(to top, black 0%, transparent 45%)` (with `-webkit-` prefix too)
- NO dark gradient overlay — only blur
- `pointer-events-none`, `z-index 1`

**Liquid-glass:** Identical to Template 01

**Blur-fade-up animation (key effect):**
```css
@keyframes blurFadeUp {
  from { opacity: 0; filter: blur(20px); transform: translateY(40px); }
  to { opacity: 1; filter: blur(0); transform: translateY(0); }
}
.animate-blur-fade-up {
  animation: blurFadeUp 1s ease-out forwards;
  opacity: 0;
}
```
Each element gets staggered `animationDelay` via inline style.

**Navbar (z-50, relative, px-4 sm:px-6 md:px-12 py-4 md:py-6 flex justify-between):**
- Left: Text logo `h-8 md:h-10` — blur-fade delay 0ms
- Center (desktop only, hidden < lg): 5 links — "Movies", "TV Series", "Editor's Pick", "Interviews", "User Reviews" — `text-sm hover:text-gray-300`. Staggered delays 100-300ms (50ms increments)
- Right: 
  - "Search" liquid-glass pill with Search icon (18px), `px-4 md:px-6 py-2`, delay 350ms
  - User profile circle: `w-10 h-10 rounded-full liquid-glass` with User icon (18px), delay 400ms
  - Hamburger (mobile only, < lg): liquid-glass circle with animated Menu/X icons (rotate-180 + opacity + scale-50, duration-500), delay 350ms

**Mobile menu (< lg breakpoint):** Absolute dropdown below navbar (`top-[72px], z-40`). Slides via `translate-y-0 opacity-100` ↔ `-translate-y-4 opacity-0 pointer-events-none`, `duration-500 ease-out`. Bg: `gray-900/95 backdrop-blur-lg + border-t border-b border-gray-800 shadow-2xl`. 5 nav links as column with `py-3 px-3 rounded-lg, hover:bg-gray-800/50`, staggered slide-in (translate-x, 50ms delays).

**Hero content (bottom of viewport, `flex-1 flex flex-col justify-end, px-4 sm:px-6 md:px-12 pb-8 md:pb-16, z-10`):**

Inside `flex-col md:flex-row items-end gap-8`:

**Left (flex-1):**
- Metadata row (`gap-3 sm:gap-6 mb-6 md:mb-8 text-xs sm:text-sm`, delay 300ms): Star icon + "8.7/10 IMDB", Clock + "132 min", Calendar + "April, 2025"
- Title: `text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-normal, letter-spacing -0.04em, mb-4 md:mb-6`, delay 400ms
- Description: `text-base sm:text-lg md:text-xl text-gray-400 mb-6 md:mb-12 max-w-2xl`, delay 500ms
- CTAs:
  - "Watch Now": `bg-white text-black rounded-full font-medium px-6 sm:px-8 py-2.5 sm:py-3` with Play icon (18px, fill-black), `hover:bg-gray-200`, delay 600ms
  - "Learn More": `rounded-full font-medium liquid-glass`, same padding, delay 700ms

**Right (navigation arrows):**
- "Previous" liquid-glass pill `px-4 sm:px-6 py-2.5 sm:py-3` with ChevronLeft, delay 800ms
- "Next" same with ChevronRight, delay 900ms

**Color palette:**
- Background: `bg-black`
- Text: white, with `text-gray-400` for subtitle
- All interactive glass: `.liquid-glass`
- Only solid color: "Watch Now" (white bg, black text)

---

## Template 10 — Minimal Video Background Snippet (utility, not a full template)

**Origin:** you paste 2026-05-11. A minimal background video setup. Use this as a SNIPPET to embed video backgrounds in any custom build.

```jsx
<video autoPlay loop muted playsInline className="absolute inset-0 w-full h-full object-cover z-0">
  <source src="https://res.cloudinary.com/dfonotyfb/video/upload/v1775585556/dds3_1_rqhg7x.mp4" type="video/mp4" />
</video>
```

Notes:
- Standard video tag pattern — works as a drop-in background layer
- Cloudinary CDN URL (vs Higgsfield CloudFront) — interchangeable, both work
- For text-heavy hero overlays, layer a dark overlay or backdrop-blur above (see Template 09's bottom-blur mask trick)

---

## Template 11 — Viktor Oddy's OWN Site (Vortex Studio — the master agency reference)

**Origin:** you paste 2026-05-11. **This is Viktor Oddy's actual portfolio/agency site.** Reverse-engineered prompt covering the entire structure. The master reference for a high-end agency landing page that converts.

**Best for:** your agency itself (if we ever drop the tools-company aesthetic and go premium-agency), or any client whose business model is "creative studio with founder personality + $5K/mo pricing." Premium-agency archetype.

**Tech:** React + TypeScript + Vite + Tailwind + lucide-react

**Fonts (custom, premium):**
- Body: "PP Neue Montreal" (loaded from Webflow CDN, weights 400 + 500)
- Serif accent: "PP Mondwest" (loaded from local `/PPMondwest-Regular.woff2`)
- Body default: PP Neue Montreal with system fallbacks

```css
@font-face {
  font-family: 'PP Neue Montreal';
  src: url('https://assets.website-files.com/6009ec8cda7f305645c9d91b/60176f9bb43e36419997ecfe_PPNeueMontreal-Book.otf') format('opentype');
  font-weight: 400;
}
@font-face {
  font-family: 'PP Neue Montreal';
  src: url('https://assets.website-files.com/6009ec8cda7f305645c9d91b/60176f9b39c5673e51a86f5a_PPNeueMontreal-Medium.otf') format('opentype');
  font-weight: 500;
}
@font-face {
  font-family: 'PP Mondwest';
  src: url('/PPMondwest-Regular.woff2') format('woff2');
  font-weight: 400;
}
```

**Color palette:**
- Primary dark: `#051A24`
- Secondary dark: `#0D212C`
- Light text on dark: `#F6FCFF`, `#E0EBF0`
- Body text: `#051A24`
- Muted: `#273C46`
- Background: white throughout

**Critical button shadows (the design signature):**
- Primary: `0_1px_2px_0_rgba(5,26,36,0.1), 0_4px_4px_0_rgba(5,26,36,0.09), 0_9px_6px_0_rgba(5,26,36,0.05), 0_17px_7px_0_rgba(5,26,36,0.01), 0_26px_7px_0_rgba(5,26,36,0), inset_0_2px_8px_0_rgba(255,255,255,0.5)`
- Secondary: `0_0_0_0.5px_rgba(0,0,0,0.05), 0_4px_30px_rgba(0,0,0,0.08)`

**Animations (all sections use `useInViewAnimation` hook with `IntersectionObserver threshold 0.1`, triggers once):**
```css
@keyframes fadeInUp {
  0% { opacity: 0; transform: translateY(30px); }
  100% { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
  opacity: 0;
}
```
Elements within each section have staggered `animationDelay` (0.1s, 0.2s, 0.3s, etc.).

### Section structure (10 sections in order)

1. **Hero** — `max-w-[440px] centered`, logo "Viktor Oddy" (PP Mondwest serif), tagline (font-mono), main heading "Build the next wave, the bold way." (with serif emphasis on "next wave" and "bold way."), 3-paragraph description, 2 buttons ("Start a chat" primary, "View projects" secondary)
2. **Infinite Marquee** — 8 motionsites.ai GIF images duplicated (16 total), `h-[280px] md:h-[500px] object-cover rounded-2xl shadow-lg`, animate-marquee 30s desktop / 10s mobile
3. **Testimonial Quote** — Quote icon + large quote "I left Apple to build the studio I always wanted to work with" (serif emphasis on "Apple") + author name + 3 company logos (Apple, IDEO, Polygon) + parallax image
4. **Pricing** — 2 cards (Monthly Partnership $5,000 dark, Custom Project $5,000 minimum light), each with title + description + price + buttons
5. **Testimonial Carousel** — Auto-scrolling (3s interval, pause on hover), 5 testimonials, prev/next chevron buttons. Heading "What builders say" + "Clutch 5/5" with 5 stars
6. **Projects** — 3 project items (evr, Automation Machines, xPortfolio), text offset left + full-width image below
7. **Partner Section** — Large white container with mouse-trail GIF spawning. Heading "Partner with us" (PP Mondwest serif, huge) + dark pill CTA with Viktor's avatar + "Start chat with Viktor"
8. **Footer** — "Start a chat" + ArrowUpRight + 2 columns of links (Services/Work/About + x.com/LinkedIn)
9. **Copyright Bar** — "Vortex Studio Limited" + "Austin, USA"
10. **Fixed Bottom Nav** — Floating pill at `bottom-6` centered. "V" letter (PP Mondwest serif) + "Start a chat" button

### Key reusable components

- **Button (3 variants):** Primary (dark bg + multi-layer shadow), Secondary (white + subtle shadow), Tertiary (white + combined shadow)
- **TestimonialSection:** Quote + parallax image (IntersectionObserver + scroll listener + `requestAnimationFrame`, max offset 200px)
- **PricingSection:** Two-card grid with dark/light variants
- **TestimonialCarousel:** Auto-scrolling with cubic-bezier(0.4, 0, 0.2, 1) 0.8s transition
- **ProjectsSection:** Vertical stack of project showcases
- **PartnerSection:** Interactive mouse-trail with random rotation (-10 to +10 deg), 1000ms fade-out, spawning every 80ms minimum
- **BottomNav:** Fixed floating pill at bottom, complex layered shadow
- **useInViewAnimation hook:** IntersectionObserver scroll-trigger

### File structure

```
src/App.tsx
src/components/Button.tsx
src/components/TestimonialSection.tsx
src/components/PricingSection.tsx
src/components/TestimonialCarousel.tsx
src/components/ProjectsSection.tsx
src/components/PartnerSection.tsx
src/components/Footer.tsx
src/components/CopyrightBar.tsx
src/components/BottomNav.tsx
src/hooks/useInViewAnimation.ts
src/index.css
```

**Key insight from Template 11:** Viktor's own site uses WHITE background (not dark). All his client demos are dark/cinematic, but his AGENCY site is bright/clean. This is a deliberate brand-vs-client-work split — same pattern we're applying to your agency (tools-company aesthetic for self vs Viktor patterns for clients).

---

---

## Template 12 — Aura AI Email Client (full premium SaaS product page)

**Origin:** you paste 2026-05-11. Full SaaS landing for an AI-native email client. Dark cinematic with shiny gradient headline, glassy cards, realistic macOS-style inbox mockup, pricing toggle.

**Best for:** SaaS / AI tools / product-led launches. The most complete product page in the library — full sections (Navbar → Hero → macOS strip → Inbox mockup → Features → Logos → Testimonials → Pricing → Final CTA).

**Tech:** React 18 + TypeScript + Vite + Tailwind + `motion/react` (framer-motion v12+) + lucide-react. Optional Supabase.

**Brand:** `#3D81E3` (brand blue), `#0c0c0c` (bg). Font: Inter (Google Fonts, 400-900).

**Liquid-glass:** Identical to Template 01

**Global background video (fixed, behind everything):**
- URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260508_064122_c4750c0e-7476-4b44-94a2-a85a65c63bf2.mp4`
- `fixed inset-0 z-0 pointer-events-none`, `w-full h-full object-cover`
- Two vertical guide lines at 36rem container edges (hidden mobile): `inset-y-0 left-1/2 -translate-x-[calc(50%+36rem)] w-px bg-white/10 z-[5]` (and inverse)

**Global SVG noise filters (two, both id `c3-noise`):**
- Root level (subtle grain, multiply blend) for shiny headline
- Inside pricing section (fractal noise, overlay blend) for giant watermark
- Both use `<feTurbulence>` and `<feBlend>` with different parameters

**Shared primitives:**
- **AppleLogo** — inline SVG, `viewBox="0 0 384 512"`, fill currentColor, default `w-4 h-4`
- **LogoMark** — abstract 4-quadrant curve, `viewBox="0 0 256 256"`, white fill
- **AppleButton** — rounded-full white pill, Apple logo + "Download Aura" + ChevronRight, hover scale chevron `+1px`
- **SectionEyebrow** — `w-1.5 h-1.5 rounded-full bg-white` dot + label + optional tag pill

**Shiny gradient on headline word "Revitalized":**
```css
backgroundImage: 'linear-gradient(to right, #091020 0%, #0B2551 12.5%, #A4F4FD 32.5%, #00d2ff 50%, #0B2551 67.5%, #091020 87.5%, #091020 100%)'
backgroundSize: '200% auto'
WebkitBackgroundClip: 'text'
color: 'transparent'
filter: 'url(#c3-noise)'
```
Animation `.animate-shiny`: 6s linear infinite, `background-position: -200% center → 200% center`

### Section structure (9 sections)

1. **Navbar** — `max-w-6xl mx-auto px-6`. LogoMark left, 5 nav links center (hidden mobile), AppleButton right
2. **Hero** — centered, `pt-16 md:pt-28 pb-20`. H1 two lines: "Your email." (white) + "Revitalized" (shiny gradient + animate-shiny). Paragraph + AppleButton + "Download for Intel / Apple Silicon" subtext
3. **macOS menu bar strip** — Full-width `h-10 bg-black/40 backdrop-blur-md border-t border-b border-white/10`. Apple logo + "Aura" + menu items + Search + date/time on right
4. **Inbox mockup** — Realistic email client UI with 3 columns (Sidebar + Message list + Reader). 6 messages with realistic content (Linear, Sophia Chen, Figma, Stripe, Vercel, GitHub)
5. **FeatureTriage** — Two-column grid. Left: heading + chips. Right: liquid-glass card with 4 sub-cards showing AI triage categories (Priority, Follow-up, Updates, Archived)
6. **LogoCloud** — Trusted-by logos in grid (Linear, Vercel, Figma, Stripe, Ramp, Notion, Loom, Arc)
7. **Testimonials** — 3-col grid of liquid-glass figures. Real names + companies (Mercury, Cohere, Lunar)
8. **Pricing** — Giant watermark headline + 3 tier cards (Free/Standard/Pro) + monthly/yearly toggle. Uses custom CSS (not Tailwind) for cinematic typography
9. **FinalCTA** — Large liquid-glass card with radial glow, two-line headline "Close the tabs. Open your day." + AppleButton + "Talk to sales" outlined button

**Key patterns from T12:**
- **Shiny gradient headline word** — premium product page signature
- **macOS menu strip** — adds "this is a real product" UI feel
- **Realistic inbox mockup** — shows product as if already exists (sells the idea)
- **Big watermark text behind pricing** — Apple-style hero text repurposed as backdrop
- **Custom CSS pricing cards** — `.c3-card` class hierarchy with hover lift, brand-aware shadows
- **AI triage card visualization** — shows AI categorizing things visually, not just claiming it

---

## Template 13 — Max Reed Personal Features Grid (3-column dark portfolio section)

**Origin:** you paste 2026-05-11. Full-viewport features section for a personal portfolio. Compact dark bento grid showing background, client voice, stats, daily software, contact.

**Best for:** Personal portfolios as a "secondary" section (not full landing), OR as a complete one-page portfolio for solo creators (designers, photographers). Bento-style information density.

**Tech:** React + TypeScript + Tailwind + lucide-react. Font: Inter (system fallback).

**Layout:** `lg:h-screen` full viewport. Dark `#0a0a0a` bg, white text, antialiased.

**Header row:**
- Left: "Hi, I'm Max Reed!" heading (`text-[28px] sm:text-3xl md:text-4xl lg:text-[44px]`, leading 1.15, font-normal, tracking-tight) + paragraph (text-sm md:text-[15px], leading-[1.6], text-white/60, max-w-3xl)
- Right: liquid-glass rounded-full button "Let's Team Up Today" (px-5 sm:px-6, py-2.5 sm:py-3)

**Grid: 3 columns on lg, 2 on md, 1 mobile, gap-4 md:gap-5:**

**Column 1 — Background card (rounded-2xl bg-black):**
- Background video: `hf_20260507_150203_44a5bd32-516a-47ce-a077-8acbf9aa8991.mp4`
- Top: "BACKGROUND" label with Sparkle icons (h-3 w-3, strokeWidth 1.5)
- Bottom: career timeline as `[auto_auto_1fr_auto]` 4-col grid (2023-Now · Freelance Creative · Solo Studio, etc.) with Sparkle separators

**Column 2 (stacked):**
- Top: Client Voice card (`bg-#324444 p-5 md:p-6 noise-overlay`). "CLIENT VOICE" eyebrow + quote (`text-[13px] sm:text-[13.5px], leading-[1.6], text-white/85`) + attribution (Elena Brooks, Creative Director — Halcyon)
- Bottom: 10M+ card (`bg-black`) with video `hf_20260507_154543_d5b83fc1-9cea-44f3-b5e8-8f325935211a.mp4`. Centered huge "10M+" (`text-5xl sm:text-6xl md:text-7xl lg:text-[88px], font-light, tracking-tight, drop-shadow`) + caption "Raised for startups"

**Column 3 (stacked):**
- Top: Daily Software card with video `hf_20260507_153148_d7a3e1dd-e5d0-4ce6-8306-00d7522ecc44.mp4`. "DAILY SOFTWARE" label + two scrolling marquee rows of liquid-glass icon tiles (h-14 w-14 md:h-16 md:w-16, rounded-xl). Row 1 left, Row 2 right, with edge mask fades
- Bottom: Reach Me card (`bg-#324444 p-5 md:p-6 noise-overlay`). "REACH ME" label + email + phone + ArrowUpRight icon button (h-9 w-9 rounded-full)

**Custom CSS additions:**
- `.liquid-glass` (same as T01)
- `@keyframes marquee-left` / `marquee-right` for icon scrolling
- `.noise-overlay::after` with SVG turbulence noise pattern (`baseFrequency='0.85' numOctaves='3'`, soft-light blend, opacity 0.55)

**Icons (all strokeWidth 1.5):** Sparkle (separator + section labels), ArrowUpRight, Figma, Framer, Palette, PenTool, Layers, Type, Aperture, Chrome, Camera, Brush, Box, Wand2

---

## Template 14 — Prosthetics Minimal Light Hero (clean editorial light theme)

**Origin:** you paste 2026-05-11. Minimal light hero. Lean, content-led, accessible-feeling. Pill-nav, badge link, single CTA. Beige background `#f0f0ee`.

**Best for:** Healthcare / medical devices / human-impact brands. When dark/cinematic is WRONG (e.g., the brand is about warmth, trust, accessibility). Approachable + premium without being luxurious.

**Tech:** React + TypeScript + Vite + Tailwind + lucide-react. NO custom font — uses default system sans-serif stack.

**Layout:**
- Root: `relative min-h-screen overflow-hidden bg-[#f0f0ee]`
- Foreground: `relative z-10 flex flex-col min-h-screen`

**Background video (fullscreen, behind everything):**
- URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260508_215831_c6a8989c-d716-4d8d-8745-e972a2eec711.mp4`
- `absolute inset-0 w-full h-full object-cover`
- autoplay muted loop playsInline

**Logo (inline SVG):**
- `viewBox="0 0 256 256"`, `width="18" height="18"`, `fill="none"`
- Single path with fill `rgb(84, 84, 84)`
- Abstract 4-quadrant geometric mark (looks like a thick angular L+R curve)

**Navbar (centered, TWO SEPARATE pills):**
- Container: `flex items-center justify-center pt-4 sm:pt-6 px-4 sm:px-8 gap-2 sm:gap-3`
- Left: circular logo container `flex items-center justify-center rounded-full w-10 h-10 sm:w-11 sm:h-11 shrink-0`, `backgroundColor: '#EDEDED'`, contains Logo SVG
- Right: pill `flex items-center gap-4 sm:gap-10 rounded-xl px-4 sm:px-8 py-2.5 sm:py-3`, `backgroundColor: '#EDEDED'`
- Nav links: ['Story', 'Products', 'Help', 'Support']. Each `text-[12px] sm:text-[14px] font-medium text-gray-700 hover:text-gray-900 transition-colors duration-200`

**Hero content (bottom-LEFT aligned, not centered):**
- Outer: `flex-1 flex items-end pb-10 sm:pb-16 lg:pb-20 px-6 sm:px-12 md:px-20 lg:px-28`
- Inner: `max-w-xs` (narrow!)
- 4 stacked elements with mb-3:
  1. **Badge link** (blue accent): `inline-flex gap-1.5 text-[11.5px] font-medium text-blue-500 hover:text-blue-600 group`. Text: "Seen on Shark Tank in India →" with arrow translating right on group hover
  2. **Headline h1**: `text-[1.5rem] sm:text-[1.75rem] leading-[1.15] font-medium text-gray-900 tracking-tight mb-3`. Text: "Simple, smart prosthetics made for people who keep fighting."
  3. **Subtext p**: `text-[13px] text-gray-400 font-normal mb-3`. Text: "Reclaim your movement now."
  4. **CTA anchor**: `inline-flex gap-2 text-[13px] font-medium text-blue-500 border border-blue-400 rounded-full px-5 py-2.5 hover:bg-blue-500 hover:text-white hover:border-blue-500 transition-all duration-200 group`. Text: "Try a free fitting →" with arrow translate on hover

**Colors:**
- Page bg: `#f0f0ee` (warm beige)
- Pill bg: `#EDEDED` (lighter gray)
- Accent: blue-500/600/400 (Tailwind blue)
- Text: gray-900 (heading) / gray-700 (nav) / gray-400 (subtext)

**Key insight from T14:** Sometimes the right answer is NOT dark cinematic. For brands that need to feel warm, approachable, human-first (medical, social-impact, education), a minimal light theme with a single accent color outperforms Viktor's signature dark cinematic. Use this template when "premium" needs to read as "accessible" not "luxurious."

---

## Updated use-case matrix — Templates 01-14

| Client type | Best template | Notes |
|---|---|---|
| Tattoo studios | **01** or **02** | Dark cinematic / glassmorphic |
| Premium salons / med-spas | **01**, **02**, or **04** | Dark or light approachable |
| Photographers / 3D artists | **03** or **13** | Full portfolio or bento section |
| High-end personal portfolio | **08** | GSAP + HLS = max sophistication |
| Indie restaurants (destination) | **01** | Hero + capabilities |
| Boutique fitness | **02** | Minimal glass |
| Travel / hospitality | **04** or **05** | Light luxury |
| Premium consultants / lawyers | **04** or **05** | Clean professional |
| Waitlist / pre-launch | **06** | Single email capture |
| Full agency / creator launch | **07** or **11** | 5-section depth |
| SaaS / AI product launch | **12** | Full product page with mockup |
| Streaming / cinema / video brand | **09** | Bottom-blur cinematic |
| Healthcare / medical / social-impact | **14** | Light minimal accessible |
| Personal creator brand portfolio | **03** or **08** | Multi-section creative |
| your agency-self homepage | NONE | Use tools-company aesthetic |
| Plumbers / mass-market | NONE | Traditional templates only |

---

## Master pattern library (extracted from all 14 templates)

The MOST repeated patterns across the library (in order of frequency):

1. **Liquid-glass utility** — appears in 9 of 14 (T01, T02, T06, T07, T09, T11, T12, T13) — UNIVERSAL chrome
2. **Background video full-bleed** — appears in 12 of 14 — universal hero treatment
3. **rAF-driven crossfade fade loops** — appears in 4 of 14 (T01, T05, T06, T07) — premium loop quality
4. **Instrument Serif italic** — appears in 7 of 14 (T01, T02, T05, T06, T07, T08, T09 implicit) — premium serif signature
5. **Inter body font** — appears in 8 of 14 — standard premium sans
6. **Italic-for-emphasis in headlines** — appears in 6 of 14 (T02, T05, T07, T08, T11 with serif) — premium typographic tension
7. **Single-accent strategy** — appears in 14 of 14 — never more than 1-2 accent colors
8. **CDN-only or Vite tech stack** — appears in all 14
9. **Framer Motion or GSAP entrance animations** — appears in 11 of 14
10. **Lucide-react icons** — appears in 9 of 14

**Strategic implication for your agency:** When delivering ANY client demo using Viktor patterns, the BASE setup is:
- Liquid-glass utility
- Background video with rAF fade
- Instrument Serif italic emphasis OR Archivo Black bold (the user's locked v3 type)
- Inter body
- Single brand-accent color
- Vite + React + Tailwind + Framer Motion + lucide-react

Everything else is variation on these foundations.

---

---

## Template 15 — Wanderful Travel Cinematic Hero (GSAP mouse parallax + playbackRate trick)

**Origin:** you paste 2026-05-11. Full-viewport cinematic travel brand hero with GSAP-driven mouse parallax on the video, slight playback speed boost, custom display font.

**Best for:** Travel brands, adventure/wanderlust brands, lifestyle/experience brands. When the hero needs to FEEL like motion + place + invitation. Travel-specific Viktor variant.

**Tech:** React + TypeScript + Vite + Tailwind + GSAP + lucide-react

**Fonts:**
- Body: Barlow (Google Fonts, 300/400/500/600)
- Hero headings: Inter (Google Fonts, 300/400/500/600/700)
- Display accent: "Dirtyline" custom font (from cdnfonts.com via @font-face)
- Also load Instrument Serif (regular + italic) for cross-template consistency

```css
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Barlow:wght@300;400;500;600&family=Inter:wght@300;400;500;600;700&display=swap');
@font-face {
  font-family: 'Dirtyline';
  src: url('https://fonts.cdnfonts.com/s/15011/Dirtyline36DaysofType.woff') format('woff');
  font-weight: normal; font-style: normal; font-display: swap;
}
```

**Body bg:** `#000`. Root container: `min-h-screen bg-black text-white overflow-x-hidden`.

**Background video (fixed, full screen, z-0):**
- URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260510_060007_60275ce7-030c-4668-a160-8f364ec537d3.mp4`
- Attributes: `autoPlay muted loop playsInline`, `object-cover`
- Wrapper scaled `scale-[1.08]` with `origin-center` (gives parallax room)
- On `onLoadedMetadata`: `playbackRate = 1.25` (subtle speed boost — more cinematic)

**GSAP mouse parallax (KEY UNIQUE FEATURE):**
```js
// Listen to mousemove
// Compute: targetX/Y = ((clientX - cx)/cx) * 20
// Lerp: currentX/Y += (target - current) * 0.06 in requestAnimationFrame
// Apply via: gsap.set(videoBg, { x, y })
```
Result: video subtly tracks the cursor, adds depth without parallax framework

**Liquid-glass utility:** Same as Template 01

**Header (fixed top, z-50, px-10 py-8, flex justify-between items-center):**
- Left: wordmark "Wanderful" + `<sup>TM</sup>`, `text-[17px] font-semibold tracking-tight`
- Center: `<nav>` liquid-glass `rounded-full px-2 py-2 flex items-center gap-1`. Links: JOURNEY, BENEFITS, JOURNAL, GUIDEBOOK. Each: `text-[11px] font-medium tracking-[0.12em] text-white/90 hover:text-white px-4 py-1.5 rounded-full transition-colors duration-200`
- Right: "GET ROAMING" anchor with same liquid-glass `rounded-full px-5 py-2.5 text-[11px] font-medium tracking-[0.12em] text-white/90 hover:text-white`

**Hero headline (fixed, `top: 120px`, centered, z-20):**
Two lines, centered, Inter 400, `font-size: clamp(40px, 5.4vw, 72px)`, `line-height: 1.1`, `letter-spacing: -0.02em`:
- Line 1 (white): "Venture without edges."
- Line 2 (`rgba(255,255,255,0.55)`): "Uncover with keen instinct."

Fade-in on mount: `opacity 0 → 100` + `translate-y-6 → 0` with `transition-all duration-1000`

**Bottom block (fixed bottom-14, z-20, flex-col items-center gap-6, fade-in delay-300):**
1. Paragraph `max-w-[620px] text-[15px] leading-relaxed` centered:
   - White: "Our smart itineraries shape around you — your rhythm, your vibe, your hunger for adventure."
   - `text-white/55`: " Each getaway is tailored, seamless, and wholly yours."
2. Primary button: white bg, black text, `text-[15px] font-medium rounded-full px-8 py-3.5`, hover `scale-[1.03] + shadow-[0_0_32px_4px_rgba(255,255,255,0.2)]`, active `scale-[0.97]`. Label: "Plan my escape today"
3. Trust signal row: Lock icon (lucide-react, `size={13} strokeWidth={1.5}`) + `text-[11px] font-medium tracking-[0.14em] text-white/70`. Text: "SECURE BY DESIGN. ZERO DATA LEAKS."

**Unique patterns from T15 (worth keeping in the your agency toolbox):**
- **`playbackRate = 1.25`** on background video — adds energy without recutting the source
- **GSAP mouse parallax** on video — premium depth effect (not framer-motion-friendly, GSAP only)
- **Travel-specific trust signal** at the bottom — "secure by design" pattern adapts to any privacy-aware vertical
- **Two-color heading split** (white + 55% white) — emphasizes the value prop without italic

---

---

## Template 16 — Animated Gradient CTA + FAQ + Footer (CSS @property color blobs)

**Origin:** you paste 2026-05-11. CTA + FAQ + Footer section with animated multi-color gradient using modern CSS `@property` for GPU-friendly custom-property interpolation.

**Best for:** Page-bottom CTA blocks, conversion-focused gradient cards, anywhere you need a "vibrant punchy CTA" without using video. Universal — drops into any tier of build.

**Tech:** React + TypeScript + Vite + Tailwind + lucide-react (ChevronDown, ChevronUp). Font: Inter.

**KEY UNIQUE TECHNIQUE — CSS `@property` animated gradient:**
- Uses 5 radial-gradient blobs that drift across wide paths AND pulse in size
- `@property --c5-x1: <percentage>` declarations enable smooth interpolation (modern, GPU-friendly)
- Base color `#ff8e53`, blob colors: `#fff1aa`, `#ff4b2b`, `#8aff8a`, `#ffd000`, `#ff1493`
- Animation durations: 3-6.5s, each offset for organic motion
- Respects `prefers-reduced-motion`
- ZERO JavaScript, ZERO canvas — pure CSS animation

**Two-column layout (`grid grid-cols-[1.6fr_1fr] gap-[30px]`, mobile 1-col):**

**Left — Animated Gradient CTA card:**
- `c5-animated-gradient rounded-[24px] py-20 px-10 text-white flex flex-col justify-center items-center text-center`
- Box shadow: `0 10px 30px rgba(0,0,0,0.05)`
- H2: "Ready to Transfer<br/>Without Borders?" — `font-normal leading-[1.1] mb-[15px]`, inline `fontSize: '3.5rem', letterSpacing: '-0.03em'`
- P: subtitle, `text-[0.9rem] mb-[30px] font-normal opacity-85`
- Button: dark bg, white text, `padding: '14px 32px', borderRadius: '12px', boxShadow: '0 10px 20px rgba(0,0,0,0.3)'`. Hover bumps shadow to `0 14px 30px rgba(0,0,0,0.4)`

**Right — FAQ accordion:**
- State: `activeIndex` toggles open/closed
- 5 FAQ items, each: `bg-white border rounded-[10px] py-[18px] px-5`. Border `#eaeaea` active / `#f0f0ee` inactive. Shadow `0 4px 12px rgba(0,0,0,0.04)` active / `0 2px 8px rgba(0,0,0,0.02)` inactive
- Question row: ChevronUp (size 20) when active, ChevronDown when not
- Answer block (when active): `mt-3 text-[0.9rem] text-[#666] leading-[1.6]`

**Footer (separate section, `bg-[#fafafa] pt-20 pb-5`):**
- 4-column grid: Logo+description, Navigation links, Pages links, Newsletter
- Newsletter has email input + Subscribe button (dark bg, hover translate-y)
- Bottom bar: copyright left, "Designed by Peter Design" right (or your name)

**Why this template matters:** First library entry with a pure-CSS animated background (no video). Useful when:
- Page weight budget is tight
- Mobile performance matters most
- Brand has multi-color identity (not single-accent)
- Need a "vibrant" hero or CTA without video bloat

---

## Template 17 — Parallax Truck Landing (HAUL! reference — vertical parallax with foreground image)

**Origin:** you paste 2026-05-11. Parallax landing where a foreground image (truck) moves at different speed than the background. Two-section flow: "View Below" spacer → main parallax with footer card at top + truck at bottom.

**Best for:** Logistics, transportation, automotive, industrial brands. Anywhere a single hero image needs cinematic motion without a video.

**Tech:** React + Tailwind + `motion/react` (Framer Motion) + lucide-react

**Sections:**

1. **Top spacer "View Below" (h-50vh / md:30vh, bg `#FDFDFD`):**
   - Centered text "View Below" — `text-gray-300 small bold uppercase tracking-[0.5em]`
   - Framer Motion fade-in opacity 0 → 1

2. **Main parallax (h-screen, relative overflow-hidden):**
   - Background image (set via inline style): `https://images.higgs.ai/?default=1&output=webp&url=...png&w=1280&q=85` reference. `bg-cover bg-center`
   - Framer Motion `useScroll` on this container. Map `scrollYProgress [0,1] → [-50, 150]` via `useTransform`. Apply to foreground truck image y
   
3. **Top-aligned footer card (absolute top-0 w-full, pt-12 lg / pt-24 md):**
   - Card constrained `max-w-7xl mx-auto`, `bg-white/95 backdrop-blur-sm shadow-xl rounded-2xl mobile / rounded-3xl desktop overflow-hidden`
   - Animation: slide down + fade in (`initial={{opacity:0, y:-20}}, animate={{opacity:1, y:0}}, duration 0.8s easeOut`)
   - Footer content top half: orange-500 logo square (40x40 mobile / 48x48 desktop, rounded-lg, shadow-inner, p-2) with white SVG inside + brand name "HAUL!" (text-gray-900 2xl/3xl font-bold tracking-tighter). 3 link columns: Company, Mobile, Contracts (uppercase tracking-widest text-sm bold headers; gray-500 hover:orange-600 link items)
   - Bottom bar: border-gray-100 top border, white bg, flex justify-between. © text + social icons (Facebook, Twitter, Instagram, Linkedin from lucide-react, w-5 h-5). Icons in 40x40 circles with border-gray-100, hover bg-orange-500 + white text + orange-500 border

4. **Foreground parallax truck layer (`motion.div` absolute inset-x-0 bottom-0 h-full pointer-events-none z-20):**
   - y axis tied to `useTransform` from step 2
   - Image: `w-full h-full object-contain object-bottom origin-bottom`
   - Scale responsive: `scale-[1.5] mobile / scale-110 sm / scale-[2.0] md / scale-105 lg`

**Unique technique:** Different scroll speeds on layers without video. Foreground image moves -50 → 150 while background stays fixed. Pure motion/react implementation.

---

## Template 18 — Marquee Logo Scroller + Rounded Hero Card (premium SaaS landing)

**Origin:** you paste 2026-05-11. Modern SaaS landing with white-card hero (rounded-3xl + soft shadow) and a high-performance CSS marquee logo scroller below.

**Best for:** Premium SaaS / B2B / agency landings where the brand wants to feel "premium-modern" rather than "premium-cinematic." Lighter, brighter, professional.

**Tech:** React + TypeScript + Tailwind v4 + Motion + lucide-react + clsx + tailwind-merge

**Fonts (Google Fonts):** Inter (sans, 400/500/600/700) + Outfit (display, 400/500/600). Config Tailwind `--font-sans` and `--font-display`. Body bg `#f9fafb`.

**Hero container (the key design feature):**
```
relative w-full max-w-[1400px] mx-auto 
rounded-[48px] 
bg-white border border-slate-200/50 
shadow-[0_40px_100px_-20px_rgba(0,0,0,0.03)] 
overflow-hidden h-[600px] flex flex-col
```

Inside: absolutely-positioned background video layer (`absolute inset-0 pointer-events-none z-0 overflow-hidden`). Video URL: `https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260505_101331_74f9b798-3f00-4e86-8a01-377aa16ffeaa.mp4`. Classes: `w-full h-full object-cover scale-105 transition-transform duration-1000`. NO overlays.

**Hero content (z-20 flex-1 px-8 md:px-16 pt-12 md:pt-16 flex flex-col items-start):**
- Headline: "Foundation of the<br/>new digital epoch" — `font-display, text-[42px] md:text-[56px], medium weight, tight tracking, color #0a1b33`
- Subhead: `font-sans, text-[14px] md:text-[15px], color #64748b`
- "Contact Us" button: `bg-[#0a152d] text-white rounded-full` with motion hover scale

**Floating bottom navbar (absolute bottom-10 left-1/2 -translate-x-1/2 z-30):**
- `flex items-center bg-white/90 backdrop-blur-2xl px-1.5 py-1.5 rounded-full shadow-[0_12px_40px_rgba(0,0,0,0.08)] border border-slate-200/40`
- Circular logo (w-9 h-9 bg-white border-slate-100 shadow-sm) with "✦"
- 2 text buttons: "Products", "Docs" (text-[12px] font-semibold text-slate-500 hover:text-[#0a1b33])
- "Get in touch" button with ChevronRight (bg-white px-5 py-2 rounded-full text-[12px] font-semibold text-[#0a1b33] border border-slate-200/60 shadow-sm hover:border-slate-300)

**Marquee logo scroller (KEY UNIQUE FEATURE) — below hero, mt-10:**
- Pure CSS @keyframes animation (`transform: translateX(0) → translateX(-50%)`), infinite scroll, pauses on hover
- Left/right edge mask: `maskImage linear-gradient` fading to transparent
- 8 logo objects from `svgl.app`: Procure, Shopify, Blender, Figma, Spotify, Lottielab, Google Cloud, Bing — each with hex gradient
- Each logo card: `group relative h-24 w-40 shrink-0 flex items-center justify-center rounded-full bg-white border border-slate-200/60 shadow-sm hover:border-slate-300 transition-all overflow-hidden`
- Inside: absolute div with brand-specific gradient, scale 1.5 + opacity 0 default → scale 1 + opacity 100 on group-hover
- Image: turns black on hover (`group-hover:brightness-0 group-hover:invert`)
- Render list TWICE inline for seamless loop

**Why this template is important:** First library entry that's "light theme premium SaaS" instead of dark cinematic OR magazine editorial. Different audience (B2B SaaS founders, dev tools, enterprise software). Demonstrates that Viktor patterns apply equally to bright + modern.

---

## More Viktor templates (incoming — to be added as you pastes)

- Template 19 — TBD
- Template 20 — TBD
