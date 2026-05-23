# MCP Servers (Optional Add-Ons)

MCP = Model Context Protocol. Think of them as plug-ins for Claude that let it talk to external services (GitHub, your email, your Drive, Firecrawl scraping, etc.).

The arsenal works without ANY of these. They're power-ups. Add only what you'll use — each one consumes memory in every Claude session.

---

## What's available

| MCP | What it adds | Cost | Realtor relevance |
|---|---|---|---|
| **Late** | Auto-post to 13 social platforms | Free tier / $25mo | High — used by 3 skills |
| **GitHub** | Read/write your repos, manage PRs/issues | Free | Low — only if you publish projects |
| **Firecrawl** | Clean web scraping (research, lead gen) | Free tier / $19mo | Medium — useful for lead-researcher |
| **Gmail** | Read/search/send email | Free | High — used by `inbox-hawk` |
| **Google Calendar** | Read/manage calendar events | Free | Medium — schedule showings, blocking time |
| **Google Drive** | Read/write Drive files | Free | Medium — pull listing photos, contracts |
| **AgentMemory** | Long-term memory across sessions | Free | Medium — Claude remembers your preferences |

---

## How to add an MCP

All MCPs go in `~/.claude/settings.json` under the `mcpServers` block. Restart VS Code after adding one.

The arsenal's `settings.template.json` already has the **most common 3 pre-configured (Late, GitHub, Firecrawl)** — you just add the API keys.

---

## Late — already covered

See [`04-late-setup.md`](04-late-setup.md). This is the most important one for a realtor.

---

## GitHub

**Why a realtor might want it:** Publishing your personal website to GitHub Pages, version-controlling your prompt library, sharing landing-page templates.

**Skip if:** You don't plan to use GitHub.

### Setup

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name like "Claude Code"
4. Expiration: 90 days (or longer)
5. Scopes: check `repo` and `read:user` at minimum
6. Click Generate. Copy the token (starts with `github_pat_...`).
7. Open `~/.claude/settings.json`, find the `github` block, paste your token where it says `github_pat_YOUR_GITHUB_PAT_HERE`.

You'll also need Node.js installed (see [INSTALL.md](../INSTALL.md) Step 6).

---

## Firecrawl

**Why a realtor might want it:** Cleanly scraping competitor agent sites, MLS pages, neighborhood data sites. Used by `lead-researcher` for company/household research.

**Skip if:** You only do basic web search.

### Setup

1. Go to https://firecrawl.dev
2. Sign up (free tier = 500 scrapes/month)
3. Settings → API Keys → Generate
4. Copy the key (starts with `fc-...`)
5. Open `~/.claude/settings.json`, find the `firecrawl` block, paste your key.

---

## Gmail (for inbox-hawk)

**Why a realtor needs it:** The `inbox-hawk` agent surfaces emails that need YOU today. Without Gmail MCP, it can't read your inbox.

**Skip if:** You don't use Gmail (use Outlook? See bottom of this doc.)

### Setup

Gmail uses OAuth, not a static API key. The flow is interactive:

1. Add this block to `~/.claude/settings.json` under `mcpServers`:
   ```json
   "gmail": {
     "command": "npx",
     "args": ["-y", "@anthropic-ai/gmail-mcp"],
     "env": {}
   }
   ```
2. Restart VS Code.
3. In Claude Code, type: `Authenticate to Gmail.`
4. Claude calls `mcp__gmail__authenticate` — opens a browser, you grant access.
5. Token gets saved automatically.

If you have multiple Gmail accounts, repeat the flow for each one. Each authenticates separately.

---

## Google Calendar

**Why a realtor needs it:** Block showing times, see your availability before responding to lead emails, schedule open houses.

### Setup

Same OAuth flow as Gmail:

1. Add to `settings.json`:
   ```json
   "google_calendar": {
     "command": "npx",
     "args": ["-y", "@anthropic-ai/google-calendar-mcp"],
     "env": {}
   }
   ```
2. Restart VS Code.
3. `Authenticate to Google Calendar.`
4. Approve in browser.

---

## Google Drive

**Why a realtor needs it:** Pull listing photos from your Drive, save generated marketing assets to Drive, read contracts.

### Setup

Same OAuth flow:

1. Add to `settings.json`:
   ```json
   "google_drive": {
     "command": "npx",
     "args": ["-y", "@anthropic-ai/google-drive-mcp"],
     "env": {}
   }
   ```
2. Restart VS Code.
3. `Authenticate to Google Drive.`

---

## AgentMemory (long-term memory)

**Why a realtor wants it:** Claude remembers your niche, your style, your past listings, your VIP contacts — across sessions, automatically. Saves you re-explaining context every time.

### Setup

```bash
npm install -g @agentmemory/agentmemory
```

Then add to `~/.claude/settings.json`:

```json
"agentmemory": {
  "command": "npx",
  "args": ["-y", "@agentmemory/mcp"]
}
```

And add SessionStart and UserPromptSubmit hooks (replace `<USERNAME>` with your Windows username):

```json
"hooks": {
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "node \"C:/Users/<USERNAME>/AppData/Roaming/npm/node_modules/@agentmemory/agentmemory/plugin/scripts/session-start.mjs\""
        }
      ]
    }
  ],
  "UserPromptSubmit": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "node \"C:/Users/<USERNAME>/AppData/Roaming/npm/node_modules/@agentmemory/agentmemory/plugin/scripts/prompt-submit.mjs\""
        }
      ]
    }
  ]
}
```

(On Mac/Linux, the path is `~/.npm-global/lib/node_modules/@agentmemory/...` or similar — `npm root -g` will show you.)

Restart VS Code. Claude now has persistent memory between sessions.

---

## On Outlook (not Gmail)

There's no official Outlook MCP yet. Workarounds:
- Forward your Outlook to Gmail and use Gmail MCP
- Use the `playwright-cli` skill to script Outlook web UI
- Wait — community MCPs for Outlook are in active development

---

## Picking what to install

If you do nothing else, install **Late** + **Gmail** (if Gmail-based). Those two unlock the most realtor-specific value.

Add the rest only when you have a specific use case for them.
