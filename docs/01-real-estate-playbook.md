# The Real Estate Playbook

How a working agent uses this arsenal day-to-day. Organized by the actual job-to-be-done — not by skill name.

---

## How to use this doc

You don't need to memorize anything. Each section has:
- **The situation** — what you're trying to do
- **The prompt** — copy-paste it into Claude Code, edit the bracketed parts
- **What happens** — which skills fire behind the scenes

You're talking to Claude like a team. Don't ask "what skill should I use?" Just describe the situation honestly and let Claude pick.

---

## Listing prep & marketing

### 1. Build a listing landing page

**Situation:** You just got a new listing. You want a dedicated landing page (separate from your brokerage site) where you can drive ads and capture interested buyers.

**Prompt:**
```
Design a landing page for my new listing at [123 Maple St., Madison, WI 53703].
4-bed colonial, 2,400 sqft, $485K, on the market 3 days.
Target buyer: young families relocating to the school district.
Hero: drone shot of the house. Section 2: 3 reasons this neighborhood is rising.
Section 3: walkthrough video embed. Section 4: lead capture form.
One CTA: 'Schedule a private showing'.
```

**What happens:** Triggers `landing-page` + `hero-section` + `cro-audit` (audits the design before showing it to you). You get HTML/CSS you can host anywhere.

---

### 2. Write a listing description that doesn't sound like every other listing

**Situation:** MLS gives you 1,000 characters. You always run out of room writing real-estate-speak. You want copy that actually sells.

**Prompt:**
```
Write a 250-word listing description for [123 Maple St].
4-bed, 2.5-bath colonial. Privacy fence, finished basement with home office,
detached 2-car garage, .4 acre lot.
Buyer profile: remote-work couple, one kid, dog.
Lean into: privacy, the basement office, the dog-friendly yard.
Avoid: 'cozy', 'charming', 'must-see', 'won't last'.
```

**What happens:** Triggers `marketing-context` + `switching-forces` (under the hood). The output addresses what the buyer actually fears (loud neighbors, no workspace, tiny yard) before they raise the objection.

---

### 3. Generate listing photos that don't look like phone shots

**Situation:** You took photos on your iPhone. They're fine but not magazine-quality. You want hero shots for the landing page.

**Prompt:**
```
Generate a hero image for my listing landing page.
Reference: [paste 1-3 URLs of your actual photos].
Style: golden hour exterior, warm light through the windows,
shallow depth of field, lifestyle/aspirational tone.
Aspect ratio: 16:9 for the website hero.
```

**What happens:** Triggers `higgsfield-product-photoshoot` — Higgsfield Nano Banana 2 with your reference images so the AI doesn't invent a fake house, it just stylizes yours.

---

### 4. Make a 15-second video tour of the property

**Situation:** You want a short video for Instagram Reels / YouTube Shorts / TikTok. You're not shooting it yourself.

**Prompt:**
```
Make a 15-second cinematic walkthrough of [123 Maple St].
Reference photos: [URL 1, URL 2, URL 3].
Vibe: warm, golden hour, slow camera moves, music: indie-folk.
End with a graphic overlay: 'Open House Saturday 1-3pm — Schedule a private showing'.
Output formats: 9:16 vertical for Reels/TikTok, 1:1 square for IG feed, 16:9 for YouTube.
```

**What happens:** Triggers `lm-cinematic-spot` → generates the spot in all three aspect ratios. Use the `lm-product-showcase` skill if you want a cleaner product-focused (less cinematic) version.

---

### 5. UGC-style testimonial video (talking head)

**Situation:** A past client gave you a glowing testimonial in text form. You want it as a video on social — but the client doesn't want to be on camera.

**Prompt:**
```
Make a UGC-style testimonial video.
Script (paste verbatim): "Hazem helped us sell our house in 9 days at full ask.
We'd interviewed three other agents — Hazem was the only one who pushed back
on our pricing and was right. Saved us 30 days on market."
Style: phone-shot, natural light, 30-something woman in a casual kitchen setting.
Format: 9:16 vertical, 30 seconds.
```

**What happens:** Triggers `lm-ugc-testimonial` (with Higgsfield Soul character or a generic avatar). You can use a `higgsfield-soul-id`-trained version of YOURSELF if you want all the testimonials to look consistent.

---

## Lead generation

### 6. Cold email to FSBO sellers

**Situation:** You found 5 For-Sale-By-Owner listings in your area. You want to reach out without sounding like a vulture.

**Prompt:**
```
Use the cold-email agent.
Prospect: [Owner name] selling [123 Maple] on FSBO since [Jan 15, 2026].
Listed at $485K. Comps suggest $510K-$525K range.
The house has been listed 47 days with one showing per week.
Their pain point: probably the showings + paperwork burnout, not the commission.
Output: 3-line email + 6-word subject line.
```

**What happens:** Triggers the `cold-email` agent. Returns a tight 3-liner. The agent will reject its own draft if it can't pass the "swap their name and the line still works" test.

---

### 7. Build a pre-meeting brief on a prospect

**Situation:** You have a listing presentation tomorrow with the Andersons. They interviewed two other agents already. You want to walk in knowing more about them than they expect.

**Prompt:**
```
Use lead-researcher.
Prospects: Mark and Jennifer Anderson, 142 Linden Lane, Madison WI.
Bought the house in 2014 for $268K. Now valued ~$520K (Zestimate).
They have a daughter graduating from Madison West HS this June.
Listing presentation tomorrow at 6pm.
```

**What happens:** Triggers `lead-researcher`. Pulls a 1-page brief: life events (daughter graduating = empty nesters), property history, neighborhood comps, equity position. Ends with "the most likely reason they took this meeting" — which gives you your opening line.

---

### 8. Find prospects you should be reaching out to

**Situation:** You want to find homeowners in your farm area who are about to sell but haven't listed yet.

**Prompt:**
```
Help me find prospect signals in zip code 53703.
Pull recent: marriage announcements, retirement news, kids' college acceptances,
job changes to other states (LinkedIn), expired listings (>180 days off market),
absent-owner LLC transfers.
For each, tell me what trigger fired and why it's an opportunity.
```

**What happens:** Triggers `lead-researcher` in batch mode. Combines public records + LinkedIn + social signals. You get a ranked list.

---

## Content & social media

### 9. Audit your existing social media

**Situation:** You've been posting on IG/Facebook for a year. You have no idea which posts actually worked. You want to stop guessing.

**Prompt:**
```
Use content-audit.
My Instagram handle: @[your_handle].
Audit my last 50 posts.
I want to know which 5 patterns consistently get higher engagement than average,
and a playbook for what to post next quarter.
```

**What happens:** Triggers `content-audit` agent. Returns top 5 named patterns ("listing reveal videos posted on Sunday evenings outperformed by 2.4x", etc.) + a concrete playbook.

---

### 10. Write a week of social media content in 10 minutes

**Situation:** It's Sunday night. You need 7 posts scheduled for the week.

**Prompt:**
```
Plan and write 7 social media posts for me, one per day this week.
Mix:
- 2 listing-related (new listing reveal + open house promo)
- 2 educational ('what closing costs actually include', 'why pre-approval matters')
- 1 personal/behind-the-scenes
- 1 market update
- 1 client win story
For each: write IG caption, write LinkedIn version, generate one hero image.
Schedule them via Late for 9am posting Mon-Sun.
```

**What happens:** Triggers `late-social-media` + `marketing-context` + `higgsfield-generate` + `lm-carousel` for the listing reveal. Each post gets platform-specific copy (LinkedIn doesn't need the emojis IG does).

---

### 11. Carousel post for Instagram

**Situation:** You want to do a "5 things first-time buyers in Wisconsin always miss" carousel.

**Prompt:**
```
Make a 5-slide Instagram carousel: '5 things first-time buyers in Wisconsin miss'.
Slides:
  1. Cover (the hook)
  2. Property tax assessments vary wildly between Madison vs suburbs
  3. Wisconsin Buyer's Agency Agreement is mandatory now
  4. Closing costs run 2-5% — most lenders won't tell you that
  5. Inspector vs appraiser is not the same thing
  6. CTA: 'DM me "guide" for the full PDF'
Style: clean, editorial, navy + cream. Square 1:1.
```

**What happens:** Triggers `lm-carousel`. Generates the cover in 4 variations, you pick one, then it uses that as the style reference for slides 2-6 so the whole carousel looks consistent.

---

### 12. Post a Reel / Short / TikTok of a listing

**Situation:** You shot a 30-second house tour on your phone. You want to post it to YouTube Shorts, IG Reels, and TikTok with platform-tuned captions.

**Prompt:**
```
Post this video as a short-form to YouTube Shorts, IG Reels, and TikTok.
Video: C:\Users\me\Videos\maple-st-tour.mp4
Property: 4-bed colonial in Madison, $485K.
Hook me with platform-specific titles + captions + hashtags.
DO NOT post until I approve the package.
```

**What happens:** Triggers `short-form-posting`. Transcribes the video, writes 3 different captions (YouTube wants SEO keywords, TikTok wants trend-aware, IG wants personality), uploads to Late, posts after your approval.

---

## YouTube

### 13. Build a YouTube content package for a market-update video

**Situation:** You recorded a 8-minute market update for Q2 2026. You want it to actually get found.

**Prompt:**
```
Build a YouTube content package for this video.
Video: C:\Users\me\Videos\q2-market-update.mp4
Topic: Q2 2026 Madison WI real estate market — inventory up 18%, days-on-market down 11%.
Target viewer: Madison-area homeowners considering selling.
Output: SEO-tuned title (5 variations to pick from), description with timestamps,
20 keywords, 3 thumbnail concepts, and a posting strategy.
DO NOT post until I confirm.
```

**What happens:** Triggers `youtube-content-package`. Transcribes the video, builds timestamps, writes SEO-optimized title options, suggests thumbnail concepts. Asks for your approval before publishing.

---

## Website & online presence

### 14. Build a personal agent website

**Situation:** Your brokerage gave you a generic profile page. You want a real personal site that converts.

**Prompt:**
```
Design a personal website for me.
About: Madison, WI buyer's agent specializing in [your niche, e.g., relocation buyers from Chicago].
Sections needed:
- Hero (the promise)
- About me (the story)
- How I work (the process — 4 steps)
- Recent wins (3 case studies)
- Testimonials (4 reviews)
- Lead capture (book a buyer consult)
Style: modern, warm, editorial. Personal but not amateur.
```

**What happens:** Triggers `website-design` + `hero-section` + `case-study` + `cro-audit`. Returns a deployable HTML site you can publish to GitHub Pages or any host.

---

### 15. Pricing page for your services (if you sell beyond commission)

**Situation:** You're starting to offer paid services — consultations, property reviews, video tours for FSBOs. You need a pricing page.

**Prompt:**
```
Design a pricing page for my services.
Tiers:
  - Consultation: $150/hr (1-on-1, no commitment)
  - Property review: $497 flat (FSBO sellers — I review the listing and give feedback)
  - Full representation: traditional commission, no upfront
Anchor 'Property review' as Most Popular.
Add an FAQ for the top 5 objections.
```

**What happens:** Triggers `pricing-page`. Returns a comparison table with the FAQ, "Most Popular" callout, and CTAs.

---

## Behind-the-scenes / power moves

### 16. Audit your existing landing page for conversion

**Situation:** You have a landing page running ads. You're getting clicks but not leads.

**Prompt:**
```
Audit my landing page for conversion.
URL: [yoursite.com/listings/maple-st]
Goal: schedule a private showing.
Tell me the top 5 reasons people aren't converting, ranked by impact,
and the exact change to make for each.
```

**What happens:** Triggers `cro-audit`. Returns prioritized fix list (hero copy, CTA position, social proof gap, etc.).

---

### 17. Analyze why a specific prospect isn't moving

**Situation:** You've been in touch with a couple for 6 weeks. They keep saying "we love it but we're not ready." You can't figure out what's actually stopping them.

**Prompt:**
```
Apply switching-forces analysis to this prospect:
The Hendersons. Renting at $2,200/mo. Saved $80K for down payment.
Looked at 14 houses with me. Said "we love it" twice. Both times pulled back at offer stage.
What's the Push, Pull, Habit, and Anxiety here? Where are they actually stuck?
```

**What happens:** Triggers `switching-forces`. You get a diagnosis: probably HABIT (comfort of the rental) + ANXIETY (mortgage feels like a trap) outweighing the PULL of any specific house. Then it tells you what to say next.

---

### 18. Triage your inbox

**Situation:** You haven't checked email in two days. There are 87 unread messages. You don't have time to read them all.

**Prompt:**
```
Use inbox-hawk.
Surface only what needs me today across all my inboxes.
Max 7 items. Don't draft replies.
```

**What happens:** Triggers `inbox-hawk`. Returns the 7 most-actionable emails ranked by sender tier + deadline + revenue impact. Everything else is filtered out as noise or "this-week" bucket.

---

## When you're starting from scratch

### 19. Build a marketing brain for your business

**Situation:** You want Claude to STOP asking who your customers are every time and just remember.

**Prompt:**
```
Build a MARKETING.md file for my real estate business.
- Niche: relocation buyers moving to Madison, WI from Chicago
- ICP: 30-45, two-career household, $150K+ income, 1-2 kids
- Pain points: school district overwhelm, neighborhood research, remote-work setup needs
- Differentiator: I personally tour neighborhoods on video for out-of-state clients
- Voice: warm, direct, no real-estate-speak
- Proof: 14 successful relocations in 2025
```

**What happens:** Triggers `marketing-context`. Writes a `MARKETING.md` in your working folder. Every other marketing skill (cold-email, cro-audit, landing-page, etc.) reads this file first so they all stay on-brand.

---

### 20. Find a skill you don't know exists

**Situation:** You have a use case but you don't know what to call it.

**Prompt:**
```
/find-skills
I want to [describe the situation in plain English].
```

**What happens:** Triggers `find-skills`. Returns matching skills with one-line summaries. If nothing matches, suggests building a new one with `skill-creator`.

---

## The meta-skill: just describe what you want

The single most-useful pattern: describe your audience first, then describe what you want. Skip the "what skill should I use" middleman.

Bad: "use the cold-email skill"
Good: "the prospect is a FSBO seller 47 days in, one showing a week — what's the right opener?"

Claude picks the skill. You stay focused on the work.

---

**Next:** [`02-skills-cheatsheet.md`](02-skills-cheatsheet.md) — one-line reference for every skill in the arsenal.
