# Skills Cheatsheet

One-line reference for every skill and agent in the arsenal. Sorted by category. Use Cmd+F / Ctrl+F to search.

## How to invoke a skill

Three ways:
1. **Just describe what you want** in plain English. Claude picks the skill.
2. **Type `/skill-name`** for a direct invocation (e.g. `/landing-page`).
3. **Trigger phrases** (listed in each skill's description) — Claude detects them automatically.

---

## Marketing brain

| Skill | One-liner |
|---|---|
| `marketing-context` | Build a MARKETING.md so every other skill stays on-brand. |
| `switching-forces` | Diagnose why prospects aren't converting (Push/Pull/Habit/Anxiety). |
| `cro-audit` | Audit a landing page for conversion. Returns prioritized fixes + copy alternatives. |

## Design + websites

| Skill | One-liner |
|---|---|
| `claude-design` | End-to-end design workflow — idea → mockup → code. |
| `website-design` | Full multi-section website (client, agent, brokerage). |
| `app-design` | Mobile app screens (React Native / Expo). |
| `landing-page` | Single-goal lead-gen / sales / waitlist page. |
| `hero-section` | 4 variations of just the hero (cheap iteration). |
| `pricing-page` | Tier comparison + FAQ for objections. |
| `case-study` | Long-form proof story for a past win. |
| `coming-soon` | Email-capture waitlist page. |
| `frontend-design` | Anthropic's polished frontend code generator (anti-AI-aesthetic). |

## Image & video generation (Higgsfield)

| Skill | One-liner |
|---|---|
| `higgsfield-generate` | Generic image/video gen — GPT Image 2, Seedance, Nano Banana 2. |
| `higgsfield-product-photoshoot` | Brand-quality product photography from reference photos. |
| `higgsfield-marketplace-cards` | Marketplace listing images (Amazon, Etsy, Zillow-style). |
| `higgsfield-soul-id` | Train Higgsfield on a face — for identity-consistent video/photo series. |

## Video production flows

| Skill | One-liner |
|---|---|
| `lm-hero-video` | 5-8s loopable hero video for the top of a landing page. |
| `lm-cinematic-spot` | 10-15s broadcast-quality brand film (no presenter). |
| `lm-product-showcase` | Clean product-focused video (great for listing reveals). |
| `lm-ugc-testimonial` | Phone-style talking-head testimonial. |
| `lm-virtual-tryon` | Person wearing/holding/using a product. |
| `lm-click-to-ad` | Paste a URL → publish-ready ad in 9:16, 1:1, 16:9. |
| `lm-carousel` | 5-10 slide Instagram/LinkedIn carousel, consistent style. |
| `lm-motion-design` | Animated motion graphics, logo reveals, section dividers. |

## Social media automation

| Skill | One-liner |
|---|---|
| `late-social-media` | Post & schedule to 13 platforms via Late API. |
| `short-form-posting` | Posts Reels/Shorts/TikTok with platform-specific captions. |
| `youtube-content-package` | Full YouTube SEO package (title, description, tags, timestamps, thumbnail concept). |

## Productivity & utility

| Skill | One-liner |
|---|---|
| `watch-video` | Claude watches a local video file and extracts content. |
| `watch-link` | Watches a video from any URL (YT, TikTok, IG, X). |
| `watch-and-implement` | Watches a tutorial and ships what it taught. |
| `watch-links-parallel` | Watches N videos in parallel. |
| `handoff` | Generates a restart prompt for a fresh chat (when context gets heavy). |
| `token-check` | Counts Claude tokens + estimates cost across Sonnet/Opus/Haiku. |
| `find-skills` | Searches the registry for installable skills you don't have yet. |
| `skill-creator` | Builds new custom skills (you tell it the spec). |
| `project-init` | Scaffolds CLAUDE.md + project_specs.md for any new project folder. |
| `quality-gate` | Scores any deliverable 1-10 before you ship + names exact fixes. |
| `clone-design` | Rebuilds a website's visual pattern from URL or screenshot. |

## Documents

| Skill | One-liner |
|---|---|
| `docx` | Read/edit/create Word documents (.docx). |
| `pdf` | Read/merge/split/OCR/watermark PDFs. |
| `xlsx` | Read/edit/create Excel spreadsheets. |

## Developer

| Skill | One-liner |
|---|---|
| `react-native-expert` | Builds & optimizes React Native / Expo mobile apps. |
| `playwright-cli` | Automates web browsers (form-filling, scraping). |
| `playwright-best-practices` | Test patterns for Playwright. |

## Agents (subagents, not skills)

Agents are launched via the `Agent` tool. You can also just describe a use case and Claude picks the right agent.

| Agent | One-liner |
|---|---|
| `cold-email` | 3-line cold email + 6-word subject. FSBO/expired/sphere-tuned. |
| `lead-researcher` | 1-page pre-call brief on a prospect/household. |
| `content-audit` | Audit last 50 social posts → top 5 engagement patterns. |
| `counterargument` | Stress-test a decision before you commit. |
| `inbox-hawk` | Triage all inboxes — only surface emails that need YOU today. |

## Built-in Anthropic plugins (enabled by default)

| Plugin | What's in it |
|---|---|
| `marketing` | Anthropic's marketing workflows |
| `productivity` | Anthropic's productivity tools |
| `frontend-design` | Anthropic's frontend code generator |

---

## Skill chaining (this is where it gets powerful)

Many skills auto-chain. Examples:

- `lm-carousel` → calls `higgsfield-generate` for the cover, then `late-social-media` to schedule
- `landing-page` → calls `cro-audit` on the result before showing you
- `youtube-content-package` → calls `watch-video` to transcribe, then `late-social-media` to post
- `marketing-context` → every other marketing skill reads its output

You don't have to wire these up. They happen automatically when you describe the goal.
