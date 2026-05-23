# Late Setup (Social Media Auto-Posting)

Late.dev is one API that posts to all 13 social platforms. Without it, the social media skills (`late-social-media`, `short-form-posting`, `youtube-content-package`) can't actually post — they can only draft.

Setup is 10-15 minutes, most of it connecting your social accounts.

---

## What you can post with Late

YouTube · Instagram · LinkedIn · TikTok · Twitter/X · Facebook · Threads · Bluesky · Pinterest · Reddit · Google Business · Telegram · Snapchat

---

## Step 1 — Sign up

1. Go to https://getlate.dev
2. Free tier gives you 10 posts/month. Pro tier ($25/mo) gives unlimited.
3. Create an account.

---

## Step 2 — Connect your social accounts

Inside Late:
1. Go to **Settings → Accounts**
2. Click "Connect" next to each platform you use
3. Authorize the OAuth flow

For real estate, connect at minimum:
- **Instagram** (must be a Business or Creator account, not Personal)
- **Facebook** (the page tied to your IG)
- **YouTube** (your channel)
- **LinkedIn** (your personal + your business page if you have one)
- **TikTok** (if you post short-form)

---

## Step 3 — Grab your API key

1. Inside Late, go to **Settings → API Keys**
2. Click "Generate new key"
3. Copy the key (starts with `sk_...`)
4. Store it somewhere safe — Late only shows it once

---

## Step 4 — Add the key to your Claude settings

Open `~/.claude/settings.json` in any text editor.

Find this block:
```json
"late": {
  "command": "uvx",
  "args": ["--from", "late-sdk[mcp]", "late-mcp"],
  "env": {
    "LATE_API_KEY": "sk_YOUR_LATE_API_KEY_HERE"
  }
}
```

Replace `sk_YOUR_LATE_API_KEY_HERE` with your actual key.

---

## Step 5 — Install `uvx` (the Python tool Late uses)

Late's MCP server runs through `uvx`, part of the Python `uv` toolkit.

**Windows:**
```powershell
winget install --id=astral-sh.uv -e
```

**Mac:**
```bash
brew install uv
```

**Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify:
```bash
uvx --version
```

---

## Step 6 — Restart Claude Code

Close VS Code completely and reopen it. Claude needs to reload `settings.json` to pick up the new MCP server.

---

## Step 7 — Test it

In Claude Code, type:
```
List my connected Late accounts.
```

If everything's wired right, Claude calls the Late MCP and prints your connected accounts (Instagram username, YouTube channel, etc.).

If you get an error about authentication — re-check the API key in `settings.json`.

---

## Step 8 — Update the skill's reference table

Open `~/.claude/skills/late-social-media/SKILL.md` and update this table with your real account IDs (replace `YOUR_USERNAME`, `YOUR_YOUTUBE_ACCOUNT_ID`, etc.):

```markdown
| Platform | Username | Account ID |
|----------|----------|------------|
| YouTube | @your_handle | acc_abc123 |
| LinkedIn | Your Name | acc_def456 |
| Instagram | @your_handle | acc_ghi789 |
```

To get the IDs: ask Claude `Run mcp__late__accounts_list` and copy them in.

This step is optional but makes the skill smarter — it can target specific accounts without asking you every time.

---

## How to use it

Once set up, just describe what you want:

```
Post a single image to Instagram + LinkedIn.
Image: C:\Users\me\Pictures\new-listing.jpg
Caption (Instagram): "🏡 New listing in Madison ..."
Caption (LinkedIn): "Just listed this 4-bed colonial..."
Schedule: tomorrow at 9am.
```

Claude triggers `late-social-media`. The skill:
1. Asks you to confirm the captions
2. Asks for a thumbnail if it's video content
3. Uploads to Late storage
4. Schedules the post
5. Reports back with the post URLs

It will **never post without your explicit approval**. Built in.

---

## Common gotchas

- **Instagram Personal accounts can't post via API.** You need to convert your IG to Business or Creator. (Free, takes 2 minutes in IG settings.)
- **YouTube needs a verified channel.** New channels can't post via API until they're verified.
- **Late's free tier caps at 10 posts/month.** If you're posting daily, get Pro.
- **First post on a new platform may need manual approval** — TikTok in particular flags new automated accounts. Post 1-2 manually first.
