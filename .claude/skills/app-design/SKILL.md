---
name: app-design
description: |
  Specialized Claude Design workflow for MOBILE & WEB APP screens (NTP mobile app, future apps). Optimized for screen-by-screen design (login, list, detail, dashboard, settings, onboarding) with React Native / Expo handoff. Layers on top of /claude-design with app-specific prompt templates, navigation patterns, component-level coaching, and stack-aware code routing.

  Use when: designing an app screen, building a new feature flow, mocking a dashboard, designing onboarding, designing component states (loading/empty/error). NOT for full-page websites — use /website-design for those.

  Triggers on: "/app-design", "design the [screen name] screen", "design the [feature] flow for the your client app", "let's design the dealer dashboard / login / order list / product detail".
---

# app-design skill

Specialized layer on top of `/claude-design`. Pre-loads app-specific patterns and routes output to React Native (or other native) builds.

**ALWAYS READ FIRST:** `~/.claude/skills/_shared/viktor-patterns.md` — Viktor patterns mostly target web, but several translate to app screens: (a) magnetic press effects on CTAs, (b) reverse-loop video for hero illustrations / onboarding splash, (c) preloader-as-design-statement on first launch, (d) bold typography display screens (settings hero, profile header). DO NOT apply editorial-massive-typography to general app screens — mobile real estate is too small. Apply Viktor patterns SELECTIVELY where the screen has hero/promotional intent.

**Reuses:**
- All 4 scripts from `~/.claude/skills/claude-design/scripts/`
- `~/.claude/skills/claude-design/templates/handoff-import-instructions.md` — bundle → Claude Code routing
- `~/.claude/skills/truck-product-image/` — for in-app product photography (NTP)
- `~/.claude/skills/_shared/viktor-patterns.md` — for the 4 motion patterns (used selectively in apps)
- **Higgsfield native skills:** `/higgsfield:generate`, `/higgsfield:soul-id` — for hero illustrations, onboarding video, avatar imagery

**Adds:**
- App-specific 4-input prompt templates (login, list, detail, dashboard, onboarding, settings, empty/loading/error states)
- Stack-aware constraints (Expo / React Native specifics for NTP)
- One-screen-at-a-time discipline (anti-pattern: "design the whole app")
- Component-state thinking (every screen → 4 states: default, loading, empty, error)
- **Viktor-pattern selective application** — magnetic press / reverse-loop / preloader / bold display where the screen warrants it; standard mobile-native otherwise

---

## When to invoke (vs /website-design vs /claude-design)

| Need | Use |
|------|-----|
| your client mobile app login / dashboard / detail screen | **/app-design** |
| New screen for any future app (web or mobile) | **/app-design** |
| Onboarding / signup flow | **/app-design** |
| Single component handoff to React Native | **/app-design** |
| Full landing page | `/website-design` |
| Pitch deck / one-pager | `/claude-design` (generic) |

## Hard rule: ONE screen per session

Don't design "the whole app" in one session. Article 10 burn-rate analysis: mega-prompts only land 1-2 of the asks. The discipline:

1. Pick ONE screen
2. Lock the spec
3. Design it
4. Validate it
5. Export handoff
6. Build with Claude Code
7. Then next screen

This is also how product designers actually work. Don't fight it.

## Workflow when invoked

### Step 1 — Scope ONE screen

Ask once:
- **Which app?** your client mobile app / new project / other (controls which CLAUDE.md applies)
- **Which screen?** Login / dashboard / list / detail / search / cart / settings / onboarding / specific feature
- **What state?** Default / loading / empty / error (always design default first; do other states only if explicitly asked)
- **Navigation context?** What screen is BEFORE this? What screen is AFTER? (informs CTAs and back-button behavior)
- **Hero / promotional intent?** Is this a screen where the user encounters the brand for the first time (onboarding, splash, login, profile header) — or a utility screen (list, detail, settings, search)? Hero/promotional screens are eligible for Viktor patterns; utility screens aren't.

If user says "design the whole app" — push back gently: "Let's start with one screen and replicate the pattern. Which one is the highest leverage?" (For NTP: probably login or order dashboard.)

### Step 2 — Pull stack constraints

Read the project's CLAUDE.md to get exact stack constraints. For NTP:
- Expo SDK 54
- React Native 0.81.5
- TypeScript ~5.9
- React Navigation v7 (bottom tabs + native stack)
- Apollo Client + GraphQL (BigCommerce)
- Zustand (client state)
- React Hook Form (forms)
- Expo Secure Store (auth tokens)
- Montserrat (font)
- DO NOT add new UI libraries unless explicitly asked

The Claude Design output must respect these. Don't generate a screen using a custom button system that requires a different RN library.

### Step 3 — Generate / locate DESIGN.md

Same as `/claude-design`. For your client specifically, recommend scraping `your-brand-site.com` for brand DNA, optionally layering in a getdesign.md brand for aesthetic direction (e.g. Linear, Cursor, Stripe Atlas for "modern bold slick").

### Step 4 — Build the 4-input prompt — APP-SPECIFIC

App prompts have a different structure than web. Use this template:

```
Design a [SCREEN NAME] screen for [APP NAME].

Context: this screen comes after [PREVIOUS SCREEN] and leads to [NEXT SCREEN].
State: default (full data loaded). [Or: loading / empty / error]

Audience: [who uses this app — depth per project CLAUDE.md]
Tone: [3-5 adjectives — match project brand]

Layout (mobile portrait 9:19.5, top to bottom):
1. Status bar area — [iOS/Android-aware]
2. Header / nav — [back button? title? right action?]
3. [Section 1] — [content + UI elements]
4. [Section 2] — [content + UI elements]
5. ...
N. Bottom CTA / nav bar — [primary action + tab bar if app uses bottom tabs]

Components on this screen:
- [List every reusable component with state machine — Button (default/pressed/disabled/loading), Input (empty/filled/focused/error), Card (default/hovered/selected), etc.]

Content (REAL, not placeholder):
- Headline: "[exact text]"
- Body: "[exact text]"
- Primary button: "[exact label]"
- Secondary actions: "[labels]"
- Real data examples: "[3 sample list items / 1 sample product / etc.]"

Constraints:
- Use brand from uploaded DESIGN.md
- Mobile portrait 9:19.5 (iPhone-friendly), also works on Android
- Tap targets minimum 44x44px
- Safe-area aware (notch, home indicator, dynamic island)
- WCAG AA contrast on all text + buttons
- Visible focus states for keyboard navigation (accessibility)
- [Stack-specific: e.g. use React Navigation v7 patterns, no Tab Bar custom — use built-in @react-navigation/bottom-tabs]
- Avoid: [things that violate brand — see project CLAUDE.md "Don't" section]
- Include: [specific motion / haptics / loading skeleton patterns]
```

### Step 5 — Iteration (app-specific cost discipline)

Same channels as `/claude-design` (Edit tool / Draw tool / Tweaks / Chat) BUT additional rules:

- **Don't iterate on multiple screens at once.** Finish one screen before opening the next.
- **Generate state variations IN THE SAME SESSION.** Once default is locked, ask Claude Design: "Now generate the loading, empty, and error states of this same screen using the same components. Keep the layout fixed."
- **For component-level changes** ("button needs to be more compact") — use the canvas Edit tool, not chat.
- **For motion / animation** — write WHAT the motion should do, not HOW to implement it. Claude Code handles the implementation in the handoff phase.

#### Viktor patterns for hero/promotional app screens

If this screen is hero/promotional (onboarding splash, login, profile header, "premium feature" upsell, share-card preview), layer in these patterns from `_shared/viktor-patterns.md`:

- **Reverse-loop hero video / illustration** — for onboarding intro animations or feature showcase. Generate via `/higgsfield:generate use kling_3_0 6 seconds 1080p "for app perfect loop"` (shorter than web, 6s plenty for mobile attention span). On RN, use `react-native-video` with `repeat={true}` + reverse-direction logic in `onEnd`.
- **Magnetic press effect on primary CTA** — RN equivalent is a haptic-backed scale/translate animation on press. Use `Animated.spring` with `damping: 8, mass: 0.5`.
- **Preloader / cold-start splash** — first-launch only, fade out after data hydration. Higgsfield-generated video as the splash → fade to home screen. Use `expo-splash-screen` + a custom video splash overlay.
- **Bold display typography for hero zones** — appropriate for: profile header card, settings header, premium-tier promo. NOT for: list rows, detail cards, navigation labels. Cap at clamp(2.25rem, 8vw, 3rem) on mobile (smaller than web because the screen is smaller).

Skip these patterns entirely for utility screens (list, detail, search, settings body, forms). Apple HIG / Material 3 patterns win for those — don't fight the platform.

### Step 6 — App-specific validation

Run THESE prompts (overrides the generic validation set):

```
Review this for accessibility. List any WCAG 2.1 AA violations, missing focus states, tap targets under 44x44px, missing alt/accessibility labels for screen readers.
```
```
Generate iPhone SE (smallest iOS), iPhone 15 Pro Max (large iOS), Pixel 7 (Android), Pixel 7 Pro (Android large) versions. Surface any layout that breaks at the smallest size.
```
```
Show all 4 states of every component on this screen — default, loading, empty, error. If a component doesn't need all 4, say so explicitly.
```
```
Map every visible action to a navigation outcome. Where does each button / link / gesture take the user? Flag any dead ends.
```

### Step 7 — Export → React Native handoff

Export "handoff bundle" → drop into project's `handoff/` folder (e.g. `D:/Projects/your-project/handoff/<screen-name>/`).

Then open Claude Code in that workspace and instruct:

```
Build the React Native screen from /handoff/<screen-name>/ following the project's CLAUDE.md stack constraints.

Specifically:
- Use existing React Navigation routes — don't add a new router
- State via Zustand for client-side, Apollo for server-side
- Forms via React Hook Form
- Screen file location: src/screens/<ScreenName>Screen.tsx
- Components extracted to: src/components/<ComponentName>.tsx if reused
- Theme tokens from: src/theme.ts (colors, spacing, typography from DESIGN.md)
- Wire real data: stub with sample data, mark "TODO: connect to Apollo query <queryName>"
- Run a quick lint pass; fix any TypeScript errors

Ask before installing any new package.
```

## Project-specific defaults

### your client mobile app
- Stack: Expo + RN 0.81 + TypeScript + React Navigation v7 + Apollo + Zustand + Montserrat
- Audience: B2B dealers, age 35-65, time-poor, professional, no-marketing-fluff
- Aesthetic direction (per you 2026-05-03): modern bold slick action — Linear / Cursor / Stripe Atlas references, NOT industrial-cliche, NOT chrome-glitz
- File targets: `D:/Projects/your-project/src/screens/<Name>.tsx`
- Don't: add new UI library, write retail copy, expose API keys in bundle, regenerate package.json deps without ask

### Future apps
Skill prompts user for stack constraints before designing (RN? Expo? SwiftUI? Flutter? Web app?). Locks them and applies forward.

## Don't

- **Don't design more than one screen per session.** Skill should refuse politely if asked to "design the whole app."
- **Don't mock data with lorem ipsum.** Use realistic sample data (real-feeling SKUs, real-feeling order numbers, real-feeling product names).
- **Don't generate hover states for mobile.** Hover doesn't exist on touch. Generate pressed states instead.
- **Don't put marketing copy in app screens.** "Welcome to the future of truck parts" belongs on the web landing page, not the app.
- **Don't ignore safe areas.** Notch, home indicator, dynamic island, status bar — always account for them.
- **Don't ship without running the 4-state validation.** Default is not enough. Loading + empty + error are not optional.
