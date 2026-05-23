# Handoff bundle import instructions

When user exports a "handoff bundle" from claude.ai/design, this is the protocol for turning it into shipping code via Claude Code.

---

## Step 1 — User downloads the bundle

claude.ai/design → Export → "Send to Claude Code" → bundle .zip downloads.

## Step 2 — Place in target project folder

User drops the bundle into the project folder root:
- client demo: `your-agency/clients/<client-slug>/handoff/`
- your client mobile app screen: `D:/Projects/ntp-mobile-app/handoff/`
- your client retail experiment: `bc-builder/handoff/`
- New project: ask user where

If `handoff/` doesn't exist, create it. Unzip the bundle there.

## Step 3 — Open Claude Code in that folder's workspace

Per-folder CLAUDE.md auto-loads. Stack constraints, voice, sacred files all in scope.

## Step 4 — Hand the bundle to Claude

User pastes (or skill writes for them):

```
Build the design from /handoff/<screen-name>/ into <real implementation>.

Stack: per the project's CLAUDE.md (do NOT add new deps).
Pixel-fidelity: match the design where reasonable. Use taste to override
if a design choice fights the audience expectation (see CLAUDE.md voice section).
Validation: after building, run the 3 validation prompts from
~/.claude/skills/claude-design/templates/validation-prompts.md against the
final result and fix anything below WCAG AA.

Ask before installing any new package or making structural changes outside
the scope of this single screen.
```

## Step 5 — Build, review, ship

Claude Code:
1. Reads the bundle's HTML/CSS or component spec
2. Translates into the project's stack (React Native / vanilla HTML / whatever)
3. Wires real data sources where bundle has placeholder data (Apollo for NTP, etc.)
4. Adds the validation pass
5. Reports back with a `BUILT.md` in the screen's folder summarizing decisions made

User reviews, requests changes, ships.

---

## Stack-specific routing

### your client Mobile App (React Native + Expo)
- Components → functional components in TypeScript
- Navigation → React Navigation v7 (do not add a different router)
- State → Zustand for client, Apollo for server
- Forms → React Hook Form
- Auth tokens → Expo Secure Store
- Fonts → Montserrat via @expo-google-fonts/montserrat

### your agency Client Demos (vanilla HTML + CSS + JS)
- Match the editorial-dark + Playfair-italic patterns from `your-agency/clients/regal-nails/`
- Use mobile-first media queries
- Splash video pattern: JS-based source select (NEVER `<source media>` on `<video>`)
- Deploy via `_repos/launch-and-manage/preview/<slug>/`

### your-agency.com itself
- Sacred. Don't modify the homepage from a handoff bundle without explicit ask.
- New work goes in `/work/` (portfolio cards) or `/preview/<client>/` (full demo sites).

### your client retail (BigCommerce)
- Stencil framework if site-side
- Python automation if back-office
- Homepage CSS is locked — do not modify without confirmation

---

## What to do when the bundle has gaps

Bundles sometimes ship with:
- Animations the host stack can't render natively
- Asset references that didn't get bundled (logos, custom fonts)
- Placeholder copy that got exported as-is
- Data structures that don't match the real backend

Protocol:
1. **Build the parts that work** — don't block the whole screen
2. **List the gaps in the BUILT.md** — what's missing, what's a TODO, what needs a real asset
3. **Surface the first 3 gaps to the user** — don't bury them in commit messages
4. **For real-data swaps** — write the integration code with a clear `// TODO: wire to Apollo query / BC API` and the example query stub
