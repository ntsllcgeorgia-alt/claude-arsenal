# Viktor patterns — shared reference for all design skills

Captured from a 12-min walkthrough by **Viktor Oddy** (founder of Design Rocket + motionsites.ai), the workflow that powers his 100+ Claude Code-built websites. Used by `/website-design`, `/hero-section`, `/landing-page`, `/coming-soon`, `/case-study`, `/pricing-page`, `/app-design`.

## When to apply (decision rule)

| Signal | Default Viktor application |
|---|---|
| **Creative-class client** (designer, photographer, tattoo artist, premium spa, agency, video producer, musician, influencer portfolio) | ✅ Full Viktor — editorial-bold typography + animated hero + reverse-loop video + preloader |
| **Tech / SaaS / D2C / agency homepage** | ✅ Full Viktor — same |
| **Restaurant with destination angle** (fine dining, themed, "an experience") | ✅ Full Viktor — adapt typography to feel curated |
| **your agency agency itself** (your-agency.com) | ✅ Already this style — keep |
| **Premium service business** (high-end nails, beauty, fitness studios) | ✅ Apply Viktor — but soften: less aggressive motion, lighter palette OK |
| **Family restaurant / casual eatery** | ❌ NO — feels pretentious, customers want warmth |
| **Plumber / contractor / HVAC / locksmith** | ❌ NO — feels too edgy, customers want trust |
| **Service trade with 50+ audience** | ❌ NO — heavy motion confuses |
| **High-conversion ecommerce product page** | ⚠️ PARTIAL — keep clean Viktor typography, skip preloader (slows TTFB) |
| **Mobile app screen** | ⚠️ PARTIAL — magnetic CTAs and reverse-loop hero video translate; full editorial typography does NOT (mobile screens too small) |

**Default:** Apply Viktor for creative class + premium + your agency-self. Refuse politely for service trades + family-mass-market.

**Override triggers:**
- `viktor mode` / `viktor style` → force Viktor patterns regardless of client
- `simple mode` / `traditional` / `conservative` → skip Viktor patterns even if creative class
- `motion-heavy` → maximum Viktor (every section animated)
- `motion-light` → editorial typography only, no video, no preloader

## The exact prompts Viktor uses (verbatim, from his demo)

### Reference image → AI hero image
> Create me an image like this in 8K, same layout of text. Remove the background, just keep text and any cards and icons, on plain black background. I do not want the background image. I need the aspect ratio to be 16 by 9 and the quality to be 4K.

### AI image → built hero section
> create me a hero section like this in 8k, same layout of text. remove the background, just keep text and any cards and icons, on plain black background. I do not want the background image. it should also be mobile responsive.

### Static image → looping video element (after replacing image URL with video URL)
> When the video finishes, let's reverse it to play from the end to the beginning. So we don't have this cut, if you know what I mean.

### Add preloader
> Let's create a preloader and have this video as the loader maybe at the half point or once the content is loaded we can fade out this video and show the content of our page.

### Apply font globally (drag font file into Claude Code chat first)
> For all the Sans Serif fonts let's use this font.

### Higgsfield image-gen command pattern
> use GPT IMAGE 2 4k quality 1t

(The `1t` is Higgsfield's Turbo quality preset for `gpt_image_2`.)

### Higgsfield video-gen pattern (Kling 3.0)
- Model: `kling_3_0` (or `seedance_2_0` for product motion)
- Duration: **12 seconds**
- Resolution: **1080p**
- Magic suffix: **"for website perfect loop"**

## The 4 core code patterns

These should appear in every Viktor-style site. Reference these snippets when handing off to Claude Code build:

### 1. Reverse-loop video (the throttled-seek pattern)

```html
<video id="hero-video" autoplay muted playsinline loop preload="auto">
  <source src="hero.mp4" type="video/mp4">
</video>

<script>
  const v = document.getElementById('hero-video');
  let dir = 1;
  v.addEventListener('ended', () => { dir = -1; v.playbackRate = 1; v.play(); });
  v.addEventListener('timeupdate', () => {
    if (dir === -1) {
      if (v.currentTime <= 0.05) { dir = 1; v.play(); return; }
      v.currentTime = Math.max(0, v.currentTime - 0.033); // ~30fps reverse
    }
  });
</script>
```

(For framer-motion / GSAP stacks, use their built-in `yoyo` / `reverse` properties instead of manual timeupdate.)

### 2. Magnetic mouse-follow (CTA + 3D elements)

```css
.magnetic { transition: transform 200ms cubic-bezier(0.2, 0.8, 0.2, 1); }
```

```js
document.querySelectorAll('.magnetic').forEach(el => {
  el.addEventListener('mousemove', (e) => {
    const r = el.getBoundingClientRect();
    const x = e.clientX - r.left - r.width / 2;
    const y = e.clientY - r.top - r.height / 2;
    el.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
  });
  el.addEventListener('mouseleave', () => { el.style.transform = ''; });
});
```

### 3. Preloader → fade-in hero

```html
<div id="preloader">
  <video src="preloader-scatter.mp4" autoplay muted playsinline></video>
</div>
<main class="hidden">...rest of page...</main>

<script>
  const pre = document.getElementById('preloader');
  const main = document.querySelector('main');
  const preVideo = pre.querySelector('video');
  preVideo.addEventListener('ended', () => {
    pre.style.opacity = 0;
    main.classList.remove('hidden');
    setTimeout(() => pre.remove(), 600);
  });
</script>
```

```css
#preloader { position: fixed; inset: 0; background: #000; z-index: 9999; transition: opacity 600ms ease; }
.hidden { opacity: 0; }
main { transition: opacity 800ms ease 200ms; }
```

### 4. Editorial-bold typography hero

```css
.hero-mega-headline {
  font-family: 'Helvetica Neue', system-ui, sans-serif;
  font-weight: 900;
  font-size: clamp(4rem, 14vw, 14rem);
  line-height: 0.9;
  letter-spacing: -0.04em;
  color: #fff;
  text-transform: uppercase;
}
.hero-italic-tag {
  font-family: 'Playfair Display', 'Times New Roman', serif;
  font-style: italic;
  font-weight: 500;
  font-size: clamp(1.5rem, 3vw, 3rem);
  color: #fff;
}
.hero-bg { background: #000; }
```

## The full Viktor stack (for new builds)

| Layer | Tool / Choice |
|---|---|
| Frontend framework | **React + Vite + TypeScript** |
| Styling | **Tailwind CSS** |
| Motion | **framer-motion** (declarative) + **GSAP** (timeline-heavy) |
| 3D (when needed) | **Three.js** via `@react-three/fiber` + `@react-three/drei` |
| Image gen | **Higgsfield CLI** → `gpt_image_2` (typography hero), `nano_banana_2` (refs/cleanup), `text2image_soul_v2` (faces) |
| Video gen | **Higgsfield CLI** → `kling_3_0` or `seedance_2_0` (12s, 1080p, "for website perfect loop") |
| Inspiration | **Land-book.com**, **Pinterest**, **motionsites.ai** |
| Hosting | **GitHub Pages** (default for your agency demos) or **Vercel** for SSR |
| Fonts | **font.download** for Helvetica Neue / Playfair / display fonts |

## Higgsfield CLI quick-reference

```powershell
# Bold editorial hero typography (Viktor's go-to)
hf generate create gpt_image_2 --prompt "Bold editorial hero typography. Massive white sans-serif text 'CLIENT NAME' on plain pure black background. Below in white italic serif 'tagline'. 16:9 aspect ratio, 4K quality, magazine-cover quality." --aspect-ratio 16:9

# Hero looping video
hf generate create kling_3_0 --prompt "[describe motion] for website perfect loop" --duration 12 --resolution 1080p

# Cost check before generating
hf generate cost <model> --prompt "..."

# Wait for job
hf generate wait <job-id>

# Account credits
hf account status
```

## Anti-patterns (refuse these)

- **"Make it look like every site on Pinterest"** — Pinterest is the inspiration, not the deliverable. Pick ONE reference, ONE direction.
- **"Make it animated everywhere"** — Viktor uses motion strategically, not constantly. Hero + magnetic CTAs + preloader. Most other sections stay static.
- **"Don't use a preloader, it slows things down"** — preloader VIDEO under 2MB + content fades in concurrently = perceived faster, not slower. Don't skip it.
- **"Generate every image with AI"** — for product e-commerce, the actual product photo wins. Use AI for hero, atmospheric, brand imagery — not for "what does the product look like."

## Performance budget (when applying Viktor)

- Total page weight: ≤ 4 MB (Viktor sites typically 3-5 MB)
- Hero looping video: ≤ 1.5 MB (compress with ffmpeg `-crf 28 -preset slow`)
- Preloader video: ≤ 1.5 MB
- Lighthouse Performance target: ≥ 80 (acceptable trade-off for the visual lift)
- LCP target: < 2.5s (preloader hides the cost)

If a build pushes past 5 MB, mitigate before ship: lower video bitrate, lazy-load below-fold imagery, defer GSAP/Three.js until after first interaction.

## Cost reality (Higgsfield credits)

Per typical Viktor-style client demo:
- 1× hero typography image (gpt_image_2): **7 credits**
- 1× hero looping video (kling_3_0, 12s, 1080p): **~80-150 credits**
- 1× preloader video (kling_3_0, 6s, 1080p): **~50-100 credits**
- 4-6× section imagery (nano_banana_2 or product-photoshoot): **~30 credits total**

**Per demo: ~200-350 credits** (roughly $4-7 worth at Creator-plan rates).

Worth it: each demo justifies $1,500-5,000 in agency fees.

## When NOT to apply Viktor patterns

If client is in any of these categories, default to traditional layouts and skip the Viktor stack:
- Plumber, electrician, HVAC, locksmith, roofer, contractor (trust > vibe)
- Family restaurant, casual diner, takeout joint
- Auto repair, oil change, tire shop
- Lawn care, pest control, cleaning service
- Daycare, eldercare, medical / healthcare with conservative audience
- Funeral home (obviously)
- Anything where the customer explicitly wants "simple, clean, easy to use"

For these, route to standard `/website-design` flow without the Viktor layer.
