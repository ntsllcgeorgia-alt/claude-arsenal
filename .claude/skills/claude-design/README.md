# claude-design skill

End-to-end Claude Design workflow automation for the user.

## What this is

A user-invokable skill that runs the full play from "I have an idea" to "shippable design + code handoff." Codifies playbook articles 06, 08, 09, 10.

## Files

```
~/.claude/skills/claude-design/
├── SKILL.md                              ← Main skill definition (Claude reads this when invoked)
├── README.md                             ← This file
├── templates/
│   ├── design-md-template.md             ← Structure for every DESIGN.md
│   ├── 4-input-prompt.md                 ← Goal · Layout · Content · Constraints formula + worked examples
│   ├── validation-prompts.md             ← WCAG / responsive / A/B variation prompts
│   └── handoff-import-instructions.md    ← Bundle → Claude Code routing per project type
└── scripts/
    ├── scrape_brand_to_design_md.py      ← URL → JSON dump of brand DNA (Claude turns into DESIGN.md)
    ├── pull_getdesign_md.py              ← Fetch DESIGN.md from getdesign.md (or open browser to download)
    └── open_claude_design.py             ← Copy prompt to clipboard + open claude.ai/design
```

## How to use

### From inside Claude Code
Type `/claude-design` or just say "let's design the [thing]" / "use claude design for [project]" / "design a [landing page / pitch deck / app screen]".

The skill auto-routes — you don't need to remember the steps. Claude will:
1. Ask what's being designed and for which project (one bundled question, not five)
2. Generate or locate a DESIGN.md (scraping a URL, pulling from getdesign.md, analyzing a folder, or building from scratch via conversation)
3. Build the 4-input prompt and copy it to your clipboard
4. Open claude.ai/design in your browser
5. Walk you through iteration in the right channel (canvas tool > chat) to save quota
6. Run the 3 validation prompts before you export
7. Route the handoff bundle to Claude Code in the correct project folder

### Standalone script use

```bash
# Scrape a brand
python scripts/scrape_brand_to_design_md.py https://your-brand-site.com D:/Projects/your-project/_brand_scrape.json

# Pull from getdesign.md
python scripts/pull_getdesign_md.py caterpillar D:/Projects/your-project/DESIGN.md

# Open Claude Design with prompt pre-loaded
python scripts/open_claude_design.py "Build a mobile app login screen for..."
```

## What the skill does NOT do

- **It doesn't replace your taste.** Claude Design generates 10 versions; only you can pick the right one.
- **It doesn't burn quota for you mid-build.** If a generation goes wrong, the skill coaches you to STOP it, not let it finish.
- **It doesn't bypass the canvas.** Steps 4-7 happen in the browser. Skill makes them frictionless but doesn't automate the actual UI.

## Quota awareness

Claude Design uses a **separate weekly quota** from regular Claude/Code. you is on Max 20x ($200/mo). Author of article 10 burned 30% in a single day on a brand build. The skill bakes in cost-saving rules:

- Brainstorm in regular Claude, execute in Design
- Edit in canvas (3 surfaces), don't chat for tweaks
- Switch Opus 4.7 → Sonnet 4.6 mid-session for iteration
- ONE major change per prompt
- Watch the build live — STOP wrong-direction generations early

## Updating the skill

When new Claude Design articles drop:
1. Save to `claude-playbook/articles/NN-claude-design-*.md`
2. Update SKILL.md "Source articles" section
3. If genuinely new tactic — fold into SKILL.md + add to README
4. If just reinforcement of existing — leave SKILL.md alone, just save the article
