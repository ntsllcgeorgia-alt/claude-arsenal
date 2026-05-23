# Install Guide

The 60-second version is in [README.md](README.md). This guide is for when something didn't work, or you want to know what each step is actually doing.

---

## What you're installing

| Tool | Why | Required? |
|---|---|---|
| **VS Code** | The editor Claude Code runs inside | Yes |
| **Claude Code extension** | The AI itself, runs inside VS Code | Yes |
| **An Anthropic account** | To sign in to Claude Code | Yes (free signup, $20/mo for Pro recommended) |
| **Git** | To clone the arsenal repo | Yes (bootstrap auto-installs on Windows) |
| **Node.js** | Used by some MCP servers (GitHub, Firecrawl) | Only if you use those MCPs |
| **Python** | Used by some skills (image generation, video processing) | Recommended |
| **Higgsfield account** | Image & video generation | Optional |
| **Late.dev account** | Auto-posting to social media | Optional |

---

## Step 1 — Install VS Code

1. Go to https://code.visualstudio.com/download
2. Pick **macOS Universal** (or your OS).
3. Drag VS Code.app to your Applications folder.
4. Open it once to make sure it works.

---

## Step 2 — Install Claude Code

1. Inside VS Code, click the Extensions icon on the left sidebar (or press `Cmd+Shift+X` on Mac / `Ctrl+Shift+X` on Windows).
2. Search for: **Claude Code**
3. Click "Install" on the one published by **Anthropic**.
4. Press `Cmd+Shift+P` (Mac) / `Ctrl+Shift+P` (Windows) to open the command palette.
5. Type: `Claude: Open chat`
6. A chat panel will appear. It'll ask you to sign in. Click "Sign in" and complete the flow.

**Recommended:** Subscribe to Claude Pro ($20/mo) for higher usage limits. The free tier will cap you fast once you start using the arsenal heavily.

---

## Step 3 — Install Git

**Mac (recommended — installs Xcode Command Line Tools which include git, make, clang):**
```bash
xcode-select --install
```
A dialog box pops up. Click "Install." Takes ~5 minutes. You only do this once per Mac.

**Windows:**
```powershell
winget install --id Git.Git -e --source winget
```
(The bootstrap script auto-installs via winget if missing.)

**Linux:**
```bash
sudo apt-get install git    # Debian/Ubuntu
sudo dnf install git         # Fedora
```

Confirm it works:
```bash
git --version
```

---

## Step 4 — Run the arsenal bootstrap

**Mac:**

Open Terminal (`Cmd+Space` → type `terminal` → Enter), then paste:

```bash
curl -fsSL https://raw.githubusercontent.com/ntsllcgeorgia-alt/claude-arsenal/main/bootstrap/bootstrap.sh | bash
```

**Windows:**

Open PowerShell (`Win+R` → type `powershell` → Enter), then paste:

```powershell
iex (iwr "https://raw.githubusercontent.com/ntsllcgeorgia-alt/claude-arsenal/main/bootstrap/bootstrap.ps1").Content
```

**Linux:**

Same curl command as Mac.

What this does:
1. Clones the repo to `~/claude-realtor-arsenal/`
2. Runs `install.ps1` (or `install.sh`)
3. Copies all 41 skills to `~/.claude/skills/`
4. Copies all 5 agents to `~/.claude/agents/`
5. Copies the welcome animation to `~/.claude/arsenal-intro.ps1`
6. Sets a `.arsenal-first-run` marker file so the next time you type `hey`, the animation plays

If you already had a `~/.claude/skills/` or `~/.claude/agents/`, **they get backed up first** to `~/.claude-backup-<timestamp>/`. Nothing of yours gets overwritten silently.

---

## Step 5 — Type `hey`

1. Open VS Code.
2. Press `Cmd+Shift+P` (Mac) / `Ctrl+Shift+P` (Windows) → `Claude: Open chat`.
3. Type: `hey`

The intro animation plays. Then you're armed.

---

## Step 6 — (Optional) Install Node.js for MCP servers

Some MCP servers (GitHub, Firecrawl) need Node.js. Skip this if you don't plan to use those.

**Windows:**
```powershell
winget install OpenJS.NodeJS.LTS
```

**Mac:**
```bash
brew install node    # if you have Homebrew, else download from nodejs.org
```

**Linux:**
```bash
sudo apt-get install nodejs npm    # or use nvm
```

Confirm:
```bash
node --version    # should print v20.x.x or higher
```

---

## Step 7 — (Optional) Install Python

Several skills (image generation scripts, video processing) use Python.

**Windows:**
```powershell
winget install Python.Python.3.12
```

**Mac:**
```bash
brew install python
```

**Linux:**
Usually pre-installed. Confirm with `python3 --version`.

---

## Step 8 — (Optional) Set up Higgsfield

See [`docs/03-higgsfield-setup.md`](docs/03-higgsfield-setup.md). 5 minutes. Free tier available, paid for serious volume.

---

## Step 9 — (Optional) Set up Late.dev

See [`docs/04-late-setup.md`](docs/04-late-setup.md). 10 minutes (most of it is connecting your social accounts). Free tier available.

---

## Step 10 — (Optional) Add API keys to settings.json

Open `~/.claude/settings.json`. You'll see placeholders like `sk_YOUR_LATE_API_KEY_HERE`. Replace them with real keys as you sign up for each service. Delete the entire block for any service you're not using.

---

## Verifying the install worked

After running the bootstrap, you should have:

```
~/.claude/
├── skills/         (41 folders, one per skill)
├── agents/         (5 .md files)
├── CLAUDE.md       (your global instructions)
├── settings.json   (from template, no keys yet)
├── arsenal-intro.ps1
├── arsenal-intro.sh
└── .arsenal-first-run    (marker file — gets deleted after first 'hey')
```

To check:

**Windows:**
```powershell
ls $HOME\.claude\skills | Measure-Object | Select Count
# Should print 41
```

**Mac/Linux:**
```bash
ls -1 ~/.claude/skills | wc -l
# Should print 41
```

---

## Updating later

```bash
cd ~/claude-realtor-arsenal
git pull
./install.ps1     # Windows
./install.sh      # Mac/Linux
```

Your existing setup gets backed up first. Safe to run repeatedly.

---

## Uninstalling

```powershell
# Windows
Remove-Item -Recurse -Force "$HOME\.claude\skills"
Remove-Item -Recurse -Force "$HOME\.claude\agents"
Remove-Item "$HOME\.claude\CLAUDE.md"
Remove-Item "$HOME\.claude\arsenal-intro.*"
```

```bash
# Mac/Linux
rm -rf ~/.claude/skills ~/.claude/agents
rm ~/.claude/CLAUDE.md ~/.claude/arsenal-intro.*
```

Leave `~/.claude/settings.json` alone if you've added API keys you want to keep.
