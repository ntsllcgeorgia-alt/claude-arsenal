# Claude Realtor Arsenal

> **From me to you.** I spent months inside Claude Code on 8-hour daily sessions building this. Every skill. Every agent. Every workflow. You just got it for free. Open it, type `hey`, and watch it download itself onto your machine.

---

## The 30-second pitch

You're a real estate agent in Wisconsin. You have one head, two hands, and ~14 hours a day. The most successful agents in the country have all of that **plus a marketing department, a video team, a social media manager, a copywriter, an admin, and a designer.**

This repo is that team. Forty-one specialized skills, five autonomous agents, three Anthropic plugins — all loaded into Claude Code on your machine. You type what you want; the right tool fires. No menus. No clicking. No "let me circle back."

It does:

- **Marketing brain** — runs CRO audits on your site, analyzes Push/Pull/Habit/Anxiety on every prospect group, writes hero copy, names objections you didn't know your buyers had.
- **Image + video studio** — generates listing photos, virtual staging, talking-head UGC ads, 15-second house tours, cinematic spots, Instagram carousels. All photorealistic, all branded to YOU.
- **Auto social media** — drafts platform-specific posts (different copy for IG vs LinkedIn vs YouTube Shorts vs TikTok), schedules them through Late, handles thumbnails, never posts without your approval.
- **YouTube content packages** — title, description, keywords, timestamps, thumbnail concept, the whole SEO package. Optimized so your videos actually get found.
- **Site builder** — pricing pages, listing pages, hero sections, case studies, coming-soon pages. Conversion-focused from the first pixel.
- **Cold email + lead research** — pulls signals on a prospect (recent move, life event, neighborhood comp), writes a 3-line email that doesn't sound like a robot.
- **Inbox triage** — surfaces only the emails that need YOU today across all your accounts, ignores the noise.
- **Plus**: PDF/Word/Excel automation, file processing, web automation via Playwright, watch-a-video-and-extract-the-content, and a token-cost calculator so you don't blow your Claude bill.

---

## Quick start (Mac — 60 seconds)

You need three things installed before you start:

1. **VS Code for Mac** — https://code.visualstudio.com/download
2. **Claude Code extension** — install from the VS Code marketplace, then sign in with your Anthropic account
3. **Xcode Command Line Tools** — ships `git`. If missing, the bootstrap will tell you. (Or run `xcode-select --install` now to get ahead of it — 5-min download.)

Then open **Terminal** (Cmd+Space, type `terminal`, hit Enter) and paste this single line:

```bash
curl -fsSL https://raw.githubusercontent.com/ntsllcgeorgia-alt/claude-arsenal/main/bootstrap/bootstrap.sh | bash
```

That's it. The script clones the repo, copies everything to the right place, and arms the welcome animation.

**Now open VS Code, launch Claude Code (Cmd+Shift+P → "Claude: Open chat"), and type:**

```
hey
```

---

## What happens when you type `hey`

Claude detects that this is your first launch. It runs an animated boot sequence in your terminal — Matrix rain, glitchy text, ASCII logo, progress bars — then prints:

```
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║   ARSENAL ONLINE                                         ║
  ║                                                          ║
  ║   ▸  41 skills loaded                                    ║
  ║   ▸   5 agents armed                                     ║
  ║   ▸   3 plugins enabled                                  ║
  ║                                                          ║
  ║   Status: READY                                          ║
  ║                                                          ║
  ╚══════════════════════════════════════════════════════════╝
```

After that first run, `hey` just behaves like a normal greeting. The animation is a one-time deal.

---

## Quick start (Windows — alternate)

Open PowerShell (Win+R, type `powershell`, hit Enter) and paste:

```powershell
iex (iwr "https://raw.githubusercontent.com/ntsllcgeorgia-alt/claude-arsenal/main/bootstrap/bootstrap.ps1").Content
```

Same flow as Mac — clone, install, type `hey`, animation runs.

---

## What's in the box

### 41 skills (grouped by what they DO for you)

**🎯 Marketing brain**
| Skill | What it does in plain English |
|---|---|
| `marketing-context` | Reads your site/listings, builds a one-source-of-truth brief for every other marketing skill |
| `switching-forces` | Diagnoses why a prospect ISN'T converting (Push/Pull/Habit/Anxiety) |
| `cro-audit` | Audits any landing page for conversion — returns prioritized fixes |

**🎨 Design + site building**
| Skill | What it does |
|---|---|
| `claude-design` | End-to-end design workflow — idea → mockup → code |
| `website-design` | Full client website, conversion-focused |
| `app-design` | Mobile app screens |
| `landing-page` | Single-goal lead-gen / sales page |
| `hero-section` | 4 variations of just the hero (most-iterated section) |
| `pricing-page` | Tier comparison + objection-handling FAQ |
| `case-study` | Long-form "we did X for Y, here's how" story page |
| `coming-soon` | Waitlist / pre-launch capture page |
| `frontend-design` | Anthropic's official frontend-design plugin |

**📸 Image + video generation (Higgsfield AI)**
| Skill | What it does |
|---|---|
| `higgsfield-generate` | Generic image/video gen — GPT Image 2, Seedance, Nano Banana |
| `higgsfield-product-photoshoot` | Brand-quality product photography |
| `higgsfield-marketplace-cards` | Marketplace-compliant listing images |
| `higgsfield-soul-id` | Train Higgsfield on YOUR face — for identity-consistent video |

**🎬 Video flows (use these for real estate content)**
| Skill | What it does |
|---|---|
| `lm-hero-video` | 5-8s loopable hero video for the top of a landing page |
| `lm-cinematic-spot` | 10-15s broadcast-quality brand film (no presenter) |
| `lm-product-showcase` | Clean product-focused video (use it for listings — the HOUSE is the product) |
| `lm-ugc-testimonial` | Phone-style talking-head review |
| `lm-virtual-tryon` | Model wearing/holding/using a product |
| `lm-click-to-ad` | Paste a URL → publish-ready video ad in 3 aspect ratios |
| `lm-carousel` | 5-10 slide Instagram/LinkedIn carousel, consistent style |
| `lm-motion-design` | Animated motion graphics, logo reveals, dividers |

**📱 Social media automation**
| Skill | What it does |
|---|---|
| `late-social-media` | Post & schedule to all 13 platforms via Late API |
| `short-form-posting` | Posts Reels/Shorts/TikTok with platform-specific captions |
| `youtube-content-package` | Full YouTube SEO package (title, description, tags, timestamps, thumbnail) |

**🤖 Productivity + utility**
| Skill | What it does |
|---|---|
| `watch-video` | Claude watches a local video file and extracts content |
| `watch-link` | Watches a video from any URL (YouTube, TikTok, Instagram, X) |
| `watch-and-implement` | Watches a tutorial and ships what it taught |
| `watch-links-parallel` | Watches N videos in parallel |
| `handoff` | When chat gets long, generates a restart prompt for a fresh session |
| `token-check` | Counts Claude tokens + estimates cost across models |
| `find-skills` | Discovers & installs more skills from the registry |
| `skill-creator` | Builds NEW custom skills |

**📄 Documents**
| Skill | What it does |
|---|---|
| `docx` | Read/edit/create Word documents |
| `pdf` | Read/merge/split/OCR/watermark PDFs |
| `xlsx` | Read/edit/create Excel spreadsheets |

**🛠 Developer (you probably won't use these much, but they're powerful)**
| Skill | What it does |
|---|---|
| `react-native-expert` | Builds React Native / Expo mobile apps |
| `playwright-cli` | Automates web browsers (form filling, scraping) |
| `playwright-best-practices` | Test-writing patterns for Playwright |

### 5 agents (specialized AI subagents)

| Agent | What it does |
|---|---|
| `cold-email` | 3-line cold email + 6-word subject line. Realtor-tuned (FSBO, expired listings, sphere) |
| `lead-researcher` | 1-page pre-call brief on a prospect — life events, property history, equity signal |
| `content-audit` | Audits your last 50 social posts → top 5 patterns that drove engagement + a playbook |
| `counterargument` | Stress-tests a decision (listing price, marketing positioning) before you commit |
| `inbox-hawk` | Triages all your inboxes — only surfaces emails that need YOU today |

### 3 Anthropic plugins (enabled by default)

- `marketing` — official marketing tooling
- `productivity` — official productivity tooling
- `frontend-design` — official UI/UX design tooling

---

## What this repo does NOT include

- **My API keys** — Late, GitHub, Firecrawl, OpenAI, Anthropic. You'll add your own.
- **My business data** — no listings, no clients, no inboxes, no projects.
- **The truck parts skills** — I run a heavy-duty truck parts business; those skills (truck-research, truck-product-image, view-ntp, view-vault) are irrelevant to you and aren't included.
- **Machine-specific config** — my Alienware laptop fingerprint, OneDrive paths, etc. Stripped out.

---

## Optional power-ups (set up only what you'll use)

The arsenal works out of the box with just Claude Code. These add more firepower:

| Tool | What it unlocks | Setup time | Required? |
|---|---|---|---|
| [Higgsfield AI](https://higgsfield.ai) | All image/video generation | 5 min — sign up + paste API key | Only if you want video/image gen |
| [Late.dev](https://getlate.dev) | Auto-posting to 13 social platforms | 10 min — connect accounts | Only if you want to schedule posts |
| [Firecrawl](https://firecrawl.dev) | Clean website scraping for research | 2 min — get API key | Optional, for lead research |
| GitHub PAT | Push code to your repos | 2 min — make a token | Only if you'll publish projects |

Full setup walkthroughs:
- [`docs/03-higgsfield-setup.md`](docs/03-higgsfield-setup.md)
- [`docs/04-late-setup.md`](docs/04-late-setup.md)
- [`docs/05-mcp-setup.md`](docs/05-mcp-setup.md)

---

## Where to go next

| If you want to... | Open... |
|---|---|
| See concrete prompts for real estate use cases | [`docs/01-real-estate-playbook.md`](docs/01-real-estate-playbook.md) |
| Skim what every skill does in one line | [`docs/02-skills-cheatsheet.md`](docs/02-skills-cheatsheet.md) |
| Set up image/video generation | [`docs/03-higgsfield-setup.md`](docs/03-higgsfield-setup.md) |
| Set up auto social posting | [`docs/04-late-setup.md`](docs/04-late-setup.md) |
| Set up extras (Firecrawl, GitHub, etc.) | [`docs/05-mcp-setup.md`](docs/05-mcp-setup.md) |
| Just see 20 copy-paste prompts to try | [`examples/realtor-prompts.md`](examples/realtor-prompts.md) |

---

## How to use this thing day-to-day

You don't memorize the skill names. You just describe what you want, and Claude triggers the right skill automatically.

**Bad prompt (treating Claude like Google):**
> "what's a good listing description?"

**Good prompt (treating Claude like a team):**
> "Write a listing description for a 3-bed colonial on 2 acres in Whitewater, WI. Buyer profile: young family relocating from Chicago for the school district. Lean into the privacy + the basement office. 250 words, no fluff."

The good prompt fires `marketing-context` + `switching-forces` + the right copy generator behind the scenes. You don't have to know that — you just describe the situation honestly.

The single most useful habit: **describe your audience, then describe what you want.**

---

## Troubleshooting

**The animation didn't play when I typed `hey`.**
The marker file got deleted by an earlier run. Manually trigger it:
```bash
# Mac
bash ~/.claude/arsenal-intro.sh
```
```powershell
# Windows
powershell -ExecutionPolicy Bypass -File "$HOME\.claude\arsenal-intro.ps1"
```

**Claude says "skill not found" when I try to use one.**
The installer probably didn't have write permission to `~/.claude/`. Re-run:
```bash
# Mac
bash ~/claude-realtor-arsenal/install.sh
```
```powershell
# Windows (as administrator)
Start-Process powershell -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -File C:\Users\$env:USERNAME\claude-realtor-arsenal\install.ps1"
```

**I want to update to a newer version of the arsenal.**
```bash
# Mac
cd ~/claude-realtor-arsenal && git pull && ./install.sh
```
```powershell
# Windows
cd $HOME\claude-realtor-arsenal; git pull; .\install.ps1
```
Your existing skills get backed up automatically before being overwritten.

**I want to start fresh / uninstall.**
```bash
# Mac / Linux
rm -rf ~/.claude/skills ~/.claude/agents
rm ~/.claude/CLAUDE.md ~/.claude/arsenal-intro.*
```
```powershell
# Windows
Remove-Item -Recurse -Force "$HOME\.claude\skills"
Remove-Item -Recurse -Force "$HOME\.claude\agents"
Remove-Item "$HOME\.claude\CLAUDE.md"
Remove-Item "$HOME\.claude\arsenal-intro.*"
```
(Don't delete `settings.json` if you've added API keys you want to keep.)

---

## A note from Hazem

I built this for myself first. Every workflow in this repo solved a real problem I had running my businesses — too many tabs, too many tools, too little time. Now you have it, and you didn't have to do the months of trial and error.

Use it. Break it. Tell me what's missing. I'll add it.

Welcome to the arsenal.
