# The 4-input prompt formula

From article 09 (Ruben Hassid). Lock these four every time:

1. **Goal** — what's being built + why + for whom
2. **Layout** — explicit section structure (don't leave Claude to guess)
3. **Content** — real headlines, real copy, real CTA text — not placeholder
4. **Constraints** — tone, audience, what to avoid, output format/aspect

---

## Template

```
Build a [GOAL: type of thing] for [PROJECT/PRODUCT NAME].

Audience: [who specifically — age, role, context, what they're tired of]
Tone: [3-5 specific adjectives — e.g. "premium but approachable, not corporate, not playful"]

Layout (top to bottom):
1. [Section name + what's in it]
2. [Section name + what's in it]
3. [...]

Content:
- Headline: "[exact text]"
- Subhead: "[exact text]"
- CTA: "[exact button label]"
- [Other key copy with exact wording]

Constraints:
- Use brand from the uploaded DESIGN.md
- [Aspect ratio / output format — e.g. "mobile portrait 9:19.5", "16:9 landscape", "9:16 reel", "Letter PDF"]
- Avoid: [specific things — "no stock photos", "no purple", "no exclamation marks", etc.]
- [Any explicit do-include rules — "include accessible color contrast", "must work in dark mode"]
```

---

## Worked examples

### your client mobile app — dealer login screen
```
Build a mobile app login screen for the your client B2B dealer app.

Audience: heavy-duty truck parts dealers — service shop owners and parts managers, 35-65, time-poor, professional, no patience for marketing fluff.
Tone: industrial, fast, dealer-respect-the-time, professional.

Layout (top to bottom):
1. your client logo (centered, top 15% of screen)
2. Welcome text + tagline (1 line each)
3. Email field
4. Password field
5. "Forgot password" link (right-aligned, small)
6. Primary "Log in" button (full width)
7. Divider with "or"
8. Secondary "Request dealer access" outline button
9. Footer micro-copy: "Authorized dealers only"

Content:
- Welcome: "Welcome back."
- Tagline: "Your dealer portal."
- Email label: "Email"
- Password label: "Password"
- Forgot link: "Forgot password?"
- Primary button: "Log in"
- Secondary button: "Request dealer access"

Constraints:
- Use brand from the uploaded DESIGN.md
- Mobile portrait, 9:19.5 (iPhone-friendly)
- Avoid: no consumer-marketing copy, no chrome-glitz, no emoji, no exclamation marks
- Include: WCAG AA contrast on all text + buttons
- Include: visible focus states for keyboard navigation
```

### client demo — restaurant landing page
```
Build a high-fidelity landing page for a small-town family-run restaurant.

Audience: 35-55-year-old locals + tourists searching "best [restaurant type] near me." They want to know the menu, hours, and how to get there. They are NOT looking for a story or a manifesto.
Tone: warm, confident, local-pride, premium-but-approachable. NOT cute, NOT generic.

Layout (top to bottom):
1. Hero with full-bleed photo (kitchen action or signature dish), restaurant name in serif italic, eyebrow tagline, "Reserve a table" CTA
2. Live-feeling open/closed status + today's hours
3. Featured menu section (3-4 dishes with photos)
4. Reviews block — 3 real Google reviews with star count
5. Visit section: address + map embed + phone
6. Footer with hours grid + social links

Content:
- Restaurant name: "[NEEDS INPUT]"
- Hero tagline: "[NEEDS INPUT — pull from existing brand]"
- CTA: "Reserve a table" (or "Order pickup" if no reservations)
- 3 menu items with name, 1-line description, price

Constraints:
- Use brand from uploaded DESIGN.md (Launch & Manage demo system)
- Mobile-first, also works on desktop
- Avoid: lorem ipsum, "passion for food", "experience our cuisine", stock photo restaurant interiors
- Include: phone number tap-to-call, address tap-to-map
```

---

## Anti-patterns to avoid

- ❌ "Build a landing page for our SaaS" (no goal, no audience, no content, no constraints)
- ❌ "Make it pop" (vague, ignored)
- ❌ "Use orange" (constraint without context — DESIGN.md should already specify)
- ❌ Placeholder copy ("Lorem ipsum" / "Insert headline here") — Claude Design will leave it as placeholder

If a prompt lacks even one of the 4 inputs, the output suffers. Always check before generating.
