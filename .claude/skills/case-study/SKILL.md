---
name: case-study
description: |
  Design a long-form case study page that turns one client win into proof for the next 10 prospects. Structured around the Hero Story Arc (situation → tension → action → outcome → unbox-the-process). For your client wins (Example Client), your client product wins, your client dealer wins, or any project with a "we shipped this" story.

  Triggers on: "/case-study", "build a case study for [project]", "turn the [client] win into a case study", "publish the [project] story".
---

# case-study skill

Long-form proof artifact. The thing you link prospects to BEFORE the call.

**Reuses:** `/claude-design` scripts + `/website-design` deploy hooks.

## Why this is its own skill

A case study isn't a landing page (no single CTA) and isn't a website (single subject). It's a proof artifact. Different rules.

## The Hero Story Arc structure

Every your agency / your clients case study follows this 5-act arc:

1. **Situation** — who the client is, what they were doing, why it was working / not
2. **Tension** — the specific problem that triggered the project (with real numbers)
3. **Action** — what we shipped, in concrete terms (specific deliverables, not "we built solutions")
4. **Outcome** — measurable result (real numbers — leads, time saved, conversion lift, etc.)
5. **Unbox the process** — the methodology / tools / playbook so prospects see it can be repeated

Skip any of these and the case study reads as a brag, not proof.

## Workflow

### Step 1 — Inputs (one bundled question)

- **Project name** — Example Client, your client mobile app, etc.
- **Client (or project) brief** — who, where, scale
- **The numbers** — before/after metrics (be honest — if there isn't one yet, mark it as "[NEEDS INPUT — collect after 30 days live]")
- **Deliverables** — what shipped (concrete list)
- **Quote** — pull a real client testimonial if available, or mark as TODO
- **Visual assets** — screenshots, photos, charts, before/after pairs

### Step 2 — Generate / locate DESIGN.md

Use the project's brand DESIGN.md. For your agency case studies → `your-agency/templates/DESIGN.md`.

### Step 3 — Build the prompt — case-study-specific

```
Build a long-form case study page for [PROJECT].

<context>
Audience: prospects who are CONSIDERING us — they're warm, they want proof we can do their thing.
Tone: confident but not braggy. Specific over general. Numbers over adjectives.
</context>

<sections>
Top to bottom:
1. Hero — eyebrow ("CASE STUDY"), headline (the result, not the project name), subhead (the project name + year), primary visual (the deliverable in context — phone mockup, screenshot, hero photo)
2. Situation — 2-3 sentences. Who they are, what they were doing, why it was working (or not). Real numbers (years in business, review count, location).
3. Tension — 1 sentence. The specific problem.
4. Action — 4-6 deliverables, each with: icon, name, 1-line description. List format, not paragraph.
5. Outcome — big-number stat block (3-5 stats). Each stat: huge number + small label. Real or marked TODO.
6. Quote — pull-quote treatment, 1-2 sentences from the client, attribution.
7. Process unbox — collapsible / expandable timeline showing the 4-step process: Discovery → Design → Launch → Manage (or project-specific).
8. Live preview embed — iframe or large screenshot of the actual deliverable.
9. CTA — "Want one for your business?" with the same DM/email actions as the homepage.
10. Footer.
</sections>

<content>
Real, not placeholder:
- Hero headline: "[Result-led, e.g. '12 years and 238 reviews finally have a website to match']"
- All stats with real numbers OR explicit [NEEDS INPUT] markers
- Real client quote OR explicit [NEEDS INPUT — collect after launch]
- Real screenshots / photos
</content>

<constraints>
- Use brand from uploaded DESIGN.md
- Mobile-first responsive
- Page weight under 3MB total
- Embedded preview iframe must be tap-friendly (lazy-loaded)
- Avoid: hyperbolic claims, "transformation", "10x", "revolutionary", lorem ipsum
- Include: real numbers, specific deliverables, dates, attribution
</constraints>
```

### Step 4 — Validation

In addition to `/website-design` validators:
```
Surface every claim or number in this case study. For each, mark whether it's: VERIFIED (real, sourced), TODO (needs input), or HALLUCINATED (made up — must remove).
```

### Step 5 — Export & deploy

your agency case studies live at:
- Source: `your-agency/marketing/case-studies/<slug>.md` (for the writeup)
- Web: `_repos/launch-and-manage/case-studies/<slug>/index.html`
- Live URL: `your-agency.com/case-studies/<slug>/`
- Linked from: `/work/` portfolio page (add as new card)

After deploy: update `your-agency/marketing/case-studies/INDEX.md` with new entry.

## Hard rules

- **No fake numbers.** Every stat is verified or marked TODO. Made-up case study stats kill agency credibility instantly.
- **Real quote or TODO.** Don't write a "client quote" yourself.
- **Process unbox is mandatory.** Prospects don't just want to see the result — they want to know they can buy it.
- **Always link from /work/ after publishing.** A case study no one finds is wasted.
