# install.ps1 — Windows installer for the Claude Realtor Arsenal.
#
# Run from the repo root:
#   powershell -ExecutionPolicy Bypass -File .\install.ps1
#
# What it does:
#   1. Backs up your existing ~/.claude/skills, agents, CLAUDE.md, settings.json
#      (so nothing of yours gets overwritten without a copy)
#   2. Copies the arsenal's skills + agents into ~/.claude/
#   3. Installs CLAUDE.md (only if you don't already have one)
#   4. Installs settings.json from template (only if you don't already have one)
#   5. Copies the intro animation to ~/.claude/arsenal-intro.ps1
#   6. Sets the .arsenal-first-run marker so "hey" triggers the welcome

$ErrorActionPreference = 'Stop'

$repoRoot   = Split-Path -Parent $MyInvocation.MyCommand.Path
$claudeDir  = Join-Path $env:USERPROFILE '.claude'
$timestamp  = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupRoot = Join-Path $env:USERPROFILE ".claude-backup-$timestamp"

function Say { param([string]$msg, [string]$color='White') Write-Host $msg -ForegroundColor $color }

Say ""
Say "  ┌──────────────────────────────────────────────────────────┐" 'Green'
Say "  │       Installing the Claude Realtor Arsenal              │" 'Green'
Say "  └──────────────────────────────────────────────────────────┘" 'Green'
Say ""

# 1. Make sure ~/.claude exists
if (-not (Test-Path $claudeDir)) {
    New-Item -ItemType Directory -Path $claudeDir | Out-Null
    Say "  ✓ Created $claudeDir" 'Gray'
}

# 2. Backup anything that's already there
$toBackup = @('skills', 'agents', 'CLAUDE.md', 'settings.json')
$didBackup = $false
foreach ($item in $toBackup) {
    $src = Join-Path $claudeDir $item
    if (Test-Path $src) {
        if (-not $didBackup) {
            New-Item -ItemType Directory -Path $backupRoot | Out-Null
            Say "  ✓ Backing up existing setup to $backupRoot" 'Yellow'
            $didBackup = $true
        }
        Copy-Item -Path $src -Destination $backupRoot -Recurse -Force
        Say "    · backed up $item" 'DarkGray'
    }
}

# 3. Install skills
$srcSkills = Join-Path $repoRoot '.claude\skills'
$dstSkills = Join-Path $claudeDir 'skills'
if (-not (Test-Path $dstSkills)) { New-Item -ItemType Directory -Path $dstSkills | Out-Null }
$skillCount = 0
Get-ChildItem $srcSkills -Directory | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $dstSkills -Recurse -Force
    $skillCount++
}
Say "  ✓ Installed $skillCount skills" 'Green'

# 4. Install agents
$srcAgents = Join-Path $repoRoot '.claude\agents'
$dstAgents = Join-Path $claudeDir 'agents'
if (-not (Test-Path $dstAgents)) { New-Item -ItemType Directory -Path $dstAgents | Out-Null }
$agentCount = 0
Get-ChildItem $srcAgents -File | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $dstAgents -Force
    $agentCount++
}
Say "  ✓ Installed $agentCount agents" 'Green'

# 5. Install CLAUDE.md (only if missing)
$dstClaudeMd = Join-Path $claudeDir 'CLAUDE.md'
if (-not (Test-Path $dstClaudeMd)) {
    Copy-Item -Path (Join-Path $repoRoot '.claude\CLAUDE.md.template') -Destination $dstClaudeMd -Force
    Say "  ✓ Installed CLAUDE.md" 'Green'
} else {
    Say "  · CLAUDE.md already exists — left it alone" 'DarkYellow'
}

# 6. Install settings.json (only if missing)
$dstSettings = Join-Path $claudeDir 'settings.json'
if (-not (Test-Path $dstSettings)) {
    Copy-Item -Path (Join-Path $repoRoot '.claude\settings.template.json') -Destination $dstSettings -Force
    Say "  ✓ Installed settings.json (you'll fill in API keys later)" 'Green'
} else {
    Say "  · settings.json already exists — left it alone" 'DarkYellow'
}

# 7. Copy intro animation
Copy-Item -Path (Join-Path $repoRoot 'bootstrap\arsenal-intro.ps1') -Destination (Join-Path $claudeDir 'arsenal-intro.ps1') -Force
Copy-Item -Path (Join-Path $repoRoot 'bootstrap\arsenal-intro.sh')  -Destination (Join-Path $claudeDir 'arsenal-intro.sh')  -Force
Say "  ✓ Installed welcome animation" 'Green'

# 8. Set the first-run marker
$marker = Join-Path $claudeDir '.arsenal-first-run'
Set-Content -Path $marker -Value (Get-Date -Format 'o') -Encoding utf8
Say "  ✓ First-run marker set" 'Green'

Say ""
Say "  ┌──────────────────────────────────────────────────────────┐" 'Green'
Say "  │   DONE                                                   │" 'Green'
Say "  └──────────────────────────────────────────────────────────┘" 'Green'
Say ""
Say "  Next steps:" 'Yellow'
Say ""
Say "    1. Open VS Code" 'White'
Say "    2. Launch Claude Code (Ctrl+Shift+P → 'Claude: Open chat')" 'White'
Say "    3. Type:  hey" 'Cyan'
Say ""
Say "  Animation will play. Then you're armed." 'Gray'
Say ""
if ($didBackup) {
    Say "  (Your previous setup is safe at: $backupRoot)" 'DarkGray'
    Say ""
}
