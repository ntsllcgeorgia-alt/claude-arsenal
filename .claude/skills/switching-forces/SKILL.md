---
name: switching-forces
description: |
  Apply the Push / Pull / Habit / Anxiety framework to any audience and any product. Most marketing only addresses Pull ("our product is great") and ignores the 3 forces that actually prevent conversion. Use to improve cold DMs, landing-page hero copy, ad creative, sales scripts. Output drives every other downstream marketing artifact.

  Triggers on: "/switching-forces", "analyze switching forces for [audience]", "why won't they buy", "improve this DM with switching forces", "Push/Pull/Habit/Anxiety analysis".
---

# switching-forces skill

The most underused framework in marketing. Codifies the Push / Pull / Habit / Anxiety pattern from playbook article 16.

> Push → what's frustrating about the current solution
> Pull → what's attractive about ours
> Habit → what keeps people stuck even when unhappy
> Anxiety → fears about switching that hold them back even when they want to move

---

## Why this matters

Most copy only addresses **Pull** ("here's why our product is great"). That ignores the 3 forces that actually keep people from converting:
- They're frustrated but don't know it (Push)
- They've adapted to the broken state (Habit)
- They're afraid the switch will break things (Anxiety)

A landing page or DM that addresses all 4 forces converts 2-3x higher than one that only sells Pull.

---

## Workflow when invoked

### Step 1 — Load context

Read `MARKETING.md` for this project (built by `/marketing-context` skill). If it doesn't exist, gently push back:
> "I'd recommend running `/marketing-context` first — it gives me the ICP and customer language to do this analysis well. Want to do that first, or push forward with what we know?"

If user pushes forward without it: ask the 4 minimum-viable questions:
1. Who is the target customer? (specific role/context)
2. What are they doing today instead of using us? (the current solution)
3. What's the artifact we're improving? (cold DM / landing page / ad / etc.)
4. What's our offer / Pull? (so we can score the existing Pull strength)

### Step 2 — Map all 4 forces with verbatim language

Output structure:

```markdown
# Switching Forces — [Audience] for [Product/Offer]

## PUSH — what's frustrating about the current state
*(What pain is bad enough that they're searching for an alternative?)*

- [Specific frustration with verbatim language if available]
- [Frustration #2]
- [Frustration #3]

**The headline Push:** [the ONE pain that, when articulated, makes them stop scrolling]

## PULL — what's attractive about us
*(What outcome do we promise?)*

- [Specific outcome — measurable]
- [Outcome #2]
- [Outcome #3]

**The headline Pull:** [the ONE promise worth their entire decision]

## HABIT — what keeps them stuck even when unhappy
*(Status quo bias. Why do they put up with the broken state?)*

- [Habit force — e.g. "they've been operating without it for 12 years and it 'works'"]
- [Habit #2 — e.g. "switching costs feel high relative to perceived gain"]
- [Habit #3 — e.g. "they don't believe a better option exists for someone like them"]

**How to overcome:** [specific tactic — e.g. "show a peer who switched and what happened"]

## ANXIETY — fears about switching
*(What could go wrong? What do they fear losing?)*

- [Anxiety #1 — e.g. "what if the new system breaks?"]
- [Anxiety #2 — e.g. "what if it's expensive and I can't justify it?"]
- [Anxiety #3 — e.g. "what if my customers/team don't adapt?"]

**How to defuse:** [specific tactic — money-back guarantee, free trial, no-contract, white-glove migration]

---

## Force Balance Score
- **Push strength:** [1-10] — how loud is the pain?
- **Pull strength:** [1-10] — how strong is our hook?
- **Habit strength:** [1-10] — how strong is status quo bias? (HIGHER = harder to convert)
- **Anxiety strength:** [1-10] — how big are the fears? (HIGHER = harder to convert)

**Net force toward switching:** (Push + Pull) − (Habit + Anxiety) = [score]

If net is positive → conversion is possible with the right copy.
If net is negative → either Push isn't loud enough OR Anxiety/Habit are dominating. Address those before pushing harder on Pull.

---

## Copy applications
**For the artifact** ([cold DM / hero / ad / etc.]):
- **Lead with the Push** (3-7 words that name the frustration in customer language)
- **Promise the Pull** (the after-state, specific)
- **Acknowledge the Habit** (validate they've been getting by — don't shame them)
- **Defuse the Anxiety** (the specific fear they have AND the proof we won't break it)

### Rewrite suggestion
[If user provided existing copy, surface a Switching-Forces-aware rewrite here]
```

### Step 3 — Apply to the specific artifact

If the user is using this to fix a specific cold DM / landing page / ad, do the rewrite. Otherwise just save the analysis and let downstream skills (`/headline-writer`, `/cold-email`, etc.) consume it.

---

## Worked example — Tony Nguyen (your agency's first cold prospect)

**Original DM (only addressed Pull):**
> Tony — I built a website for you. Look: [link]. If you like it, it's yours.

**Switching Forces analysis:**
- **Push:** he's losing customers who Google "Weatherford nail salon" and find him with no site (or a Yelp listing only)
- **Pull:** I built him a free site that shows his portfolio + 238 reviews
- **Habit:** he's run the salon 12 years without a website — he believes it's "fine"
- **Anxiety:** what if it costs to maintain? What if it breaks? What if he doesn't know how to update it? What's the catch?

**Switching-Forces-aware rewrite:**
> Tony — every Friday a customer Googles "nails Weatherford" and clicks the salon with the website, not yours. I built you one to match your 238 reviews. No charge, no contract, no maintenance worry — it just sits there working. If you don't want it, ignore me. If you do: [link]. — you, in Weatherford.

**What changed:**
- Push: opened with the loss happening RIGHT NOW (Friday Google search)
- Pull: kept the offer
- Habit: didn't shame him for 12 years without a site — implicit acknowledgment
- Anxiety: explicitly defused 3 fears (cost / contract / maintenance) in one line

---

## Hard rules

- **Always quote real customer language for Push when possible.** Generic "they have problems" is useless. "They Google us at 9pm and find nothing" is a knife.
- **Don't ignore Habit.** It's the silent killer. People will rather suffer than change.
- **Anxiety must be addressed BEFORE the CTA, not after.** Address fears, then ask for the action.
- **Don't claim to defuse Anxiety with vague reassurance.** "Don't worry" is not a defuse. "Money-back if you cancel in 14 days" is.
