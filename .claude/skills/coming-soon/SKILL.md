---
name: coming-soon
description: |
  Design a coming-soon / pre-launch / waitlist page. Single goal: capture email. For new product launches before the actual product is built — sets expectations, builds the list, validates demand cheaply.

  Triggers on: "/coming-soon", "build a waitlist page for [product]", "pre-launch page for [thing]", "I want to validate this idea before building".
---

# coming-soon skill

Specialized landing page for one job: capture an email before launch.

**Reuses:** `/landing-page` patterns + `/claude-design` scripts.

## When to invoke

User has an idea but hasn't built it yet. Wants to:
- Validate demand before development
- Build a waitlist for launch
- Reserve a domain with something better than a parking page

## The 90-second rule

Coming-soon pages convert in 90 seconds or not at all. Visitor lands, sees the promise, gives email or bounces. Anything that takes longer to read = bounce.

## Workflow

### Step 1 — Inputs (one bundled question)

- **What's the product?** One sentence
- **Why does this matter to the audience?** One sentence
- **Launch timeframe?** "Q3 2026" / "Soon" / "When 1,000 sign up"
- **Email capture only, or also social follow?**
- **Brand source?** Existing DESIGN.md / scrape / from scratch

### Step 2 — Build the prompt

```
Build a coming-soon waitlist page for [PRODUCT].

Goal: capture email address. ONE input field, ONE button. That's it.

Sections:
1. Hero (full viewport height)
   - Eyebrow: "[COMING SOON / IN BETA / LAUNCHING Q3 2026]"
   - Headline: [the promise — 6-12 words]
   - Subhead: [one sentence explainer]
   - Email input (full width on mobile, 480px max desktop)
   - "Join the waitlist" button (or product-specific verb — "Reserve your spot", "Get early access")
   - Counter: "[X] already on the list" (optional, only if real)
2. Three proof points — why this matters / why we can build it
3. Footer — minimal: copyright, legal, social handles

Content (real):
- Headline: "[exact]"
- Subhead: "[exact]"
- Three proof points: "[1]", "[2]", "[3]"
- Button label: "[exact verb-led]"
- Footer text: "[exact]"

Constraints:
- Use brand from uploaded DESIGN.md
- Mobile-first, single column, single viewport (ideally above-the-fold completes)
- ONE input + ONE button. No nav, no menu, no other CTAs.
- Email validation visible (live as user types)
- Submit success state: "You're in. Check your email." with confetti or subtle success animation
- Page weight under 800KB total
- Animation: subtle ambient background motion (gradient drift / particle field / gentle parallax)
- Avoid: "Subscribe to our newsletter", multiple inputs, "Tell us about yourself", quiz funnels
- Include: Open Graph share preview, favicon, viewport meta, email capture POST endpoint placeholder
```

### Step 3 — Email capture wiring

Coming-soon pages are useless without email capture working. Default targets:

- **your agency / your-agency.com:** ConvertKit / Beehiiv / a Google Form-backed Apps Script endpoint
- **your clients:** Google Sheets via Apps Script web app (no auth required for POST)
- **Standalone:** Buttondown.email or Resend with a Cloudflare Worker

Skill output should include the form `action=` placeholder + a comment block explaining where to paste the real endpoint.

### Step 4 — Validation

```
Squint test: above-the-fold on mobile (390x844) — can a visitor sign up without scrolling? If not, name the fix.
```
```
Test the email capture: simulate a submit. Does the success state work? Is there a clear next-step (check inbox / share with friends / etc.)?
```

### Step 5 — Export & deploy

Coming-soon URLs:
- `your-agency.com/<product-slug>/` — quickest deploy via existing GitHub Pages repo
- `<custom-domain>.com/` — if user already owns the domain, set up Cloudflare Pages + email worker

Always set up:
- Open Graph preview image (auto-generated from DESIGN.md hero treatment)
- Favicon + apple-touch-icon
- Sitemap.xml (single URL is fine)
- robots.txt allowing indexing

## Hard rules

- **One input + one button.** A coming-soon page with a 4-question form converts at 0%.
- **Above-the-fold completion.** Visitor should be able to sign up without scrolling on a 390x844 phone.
- **Real email capture.** A page that says "join the waitlist" but doesn't actually capture is malpractice. Wire it to a real backend before deploying.
- **No "About us" link.** It's a coming-soon page. There's nothing to be about yet.
