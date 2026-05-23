# arsenal-intro.ps1
# The "type hey" welcome animation. Runs once on first launch after install.
# Pure native PowerShell — no dependencies, works on any Windows 10/11 machine.

$ErrorActionPreference = 'SilentlyContinue'

function Show-Glitch {
    param([string]$Text, [int]$Iterations = 6)
    $glyphs = '!@#$%^&*<>?/\|~+=01'.ToCharArray()
    $rand = New-Object Random
    for ($i = 0; $i -lt $Iterations; $i++) {
        $line = -join (1..$Text.Length | ForEach-Object { $glyphs[$rand.Next($glyphs.Length)] })
        Write-Host "`r$line" -NoNewline -ForegroundColor DarkGreen
        Start-Sleep -Milliseconds 35
    }
    Write-Host "`r$Text" -ForegroundColor Green
}

function Show-Rain {
    param([int]$Rows = 8, [int]$Width = 70)
    $chars = '01アイウエオカキクケコサシスセソタチツテト░▒▓█'.ToCharArray()
    $rand = New-Object Random
    for ($r = 0; $r -lt $Rows; $r++) {
        $line = -join (1..$Width | ForEach-Object { $chars[$rand.Next($chars.Length)] })
        $shade = if ($r -lt 2) { 'DarkGreen' } elseif ($r -lt 5) { 'Green' } else { 'White' }
        Write-Host $line -ForegroundColor $shade
        Start-Sleep -Milliseconds 40
    }
}

function Show-Bar {
    param([string]$Label, [int]$DurationMs = 700)
    $width = 30
    $steps = 15
    Write-Host ("  {0,-22} " -f $Label) -NoNewline -ForegroundColor Cyan
    for ($i = 0; $i -le $steps; $i++) {
        $filled = [int]([Math]::Round(($i / $steps) * $width))
        $bar = ('█' * $filled) + ('░' * ($width - $filled))
        $pct = [int](($i / $steps) * 100)
        Write-Host "`r  $($Label.PadRight(22)) [$bar] $pct%" -NoNewline -ForegroundColor Green
        Start-Sleep -Milliseconds ([int]($DurationMs / $steps))
    }
    Write-Host ""
}

Clear-Host
Write-Host ""

# ── Phase 1: Matrix rain ──────────────────────────────────────────
Show-Rain -Rows 6 -Width 70
Write-Host ""

# ── Phase 2: Glitchy boot sequence ────────────────────────────────
Show-Glitch "  > BOOT SEQUENCE INITIATED..."
Start-Sleep -Milliseconds 200
Show-Glitch "  > AUTHENTICATING USER..."
Start-Sleep -Milliseconds 200
Show-Glitch "  > LOADING CLAUDE ARSENAL..."
Write-Host ""

# ── Phase 3: ASCII logo ───────────────────────────────────────────
$logo = @'

   ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗
  ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝
  ██║     ██║     ███████║██║   ██║██║  ██║█████╗
  ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝
  ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗
   ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝

      █████╗ ██████╗ ███████╗███████╗███╗   ██╗ █████╗ ██╗
     ██╔══██╗██╔══██╗██╔════╝██╔════╝████╗  ██║██╔══██╗██║
     ███████║██████╔╝███████╗█████╗  ██╔██╗ ██║███████║██║
     ██╔══██║██╔══██╗╚════██║██╔══╝  ██║╚██╗██║██╔══██║██║
     ██║  ██║██║  ██║███████║███████╗██║ ╚████║██║  ██║███████╗
     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝

'@
foreach ($line in $logo -split "`n") {
    Write-Host $line -ForegroundColor Green
    Start-Sleep -Milliseconds 18
}

Write-Host "         ──────────  BUILT FOR REALTORS  ──────────" -ForegroundColor DarkGreen
Write-Host "         ──────────   POWERED BY CLAUDE  ──────────" -ForegroundColor DarkGreen
Write-Host ""
Start-Sleep -Milliseconds 400

# ── Phase 4: Loading bars ─────────────────────────────────────────
Write-Host "  ▶ LOADING MODULES" -ForegroundColor Yellow
Write-Host ""
Show-Bar "Skills"        600
Show-Bar "Agents"        450
Show-Bar "Plugins"       400
Show-Bar "Settings"      300
Show-Bar "MCP Servers"   400
Write-Host ""
Start-Sleep -Milliseconds 200

# ── Phase 5: Stats readout ────────────────────────────────────────
$skillCount  = (Get-ChildItem "$env:USERPROFILE\.claude\skills"  -Directory -ErrorAction SilentlyContinue | Measure-Object).Count
$agentCount  = (Get-ChildItem "$env:USERPROFILE\.claude\agents" -File -ErrorAction SilentlyContinue | Measure-Object).Count

Write-Host "  ╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "  ║                                                          ║" -ForegroundColor Green
Write-Host ("  ║   ARSENAL ONLINE                                         ║") -ForegroundColor Green
Write-Host "  ║                                                          ║" -ForegroundColor Green
Write-Host ("  ║   ▸ {0,3} skills loaded                                    ║" -f $skillCount) -ForegroundColor Green
Write-Host ("  ║   ▸ {0,3} agents armed                                     ║" -f $agentCount) -ForegroundColor Green
Write-Host "  ║   ▸   3 plugins enabled                                  ║" -ForegroundColor Green
Write-Host "  ║                                                          ║" -ForegroundColor Green
Write-Host "  ║   Status: READY                                          ║" -ForegroundColor Green
Write-Host "  ║                                                          ║" -ForegroundColor Green
Write-Host "  ╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Start-Sleep -Milliseconds 600

# ── Phase 6: What to do next ──────────────────────────────────────
Write-Host "  Welcome to your arsenal." -ForegroundColor White
Write-Host ""
Write-Host "  This was hand-built over months of 8-hour sessions inside" -ForegroundColor Gray
Write-Host "  Claude Code. Every skill, every agent, every workflow." -ForegroundColor Gray
Write-Host "  You just got it for free." -ForegroundColor Gray
Write-Host ""
Write-Host "  Try one of these to get moving:" -ForegroundColor Yellow
Write-Host ""
Write-Host "    /find-skills" -ForegroundColor Cyan -NoNewline; Write-Host "             discover everything you can do"
Write-Host "    'design a landing page for my listing on 123 Maple St.'" -ForegroundColor Cyan
Write-Host "    'write a cold email to FSBO sellers in my zip code'" -ForegroundColor Cyan
Write-Host "    'make a 15-second video of this house for Instagram'" -ForegroundColor Cyan
Write-Host "    'audit my last 50 social posts and find what worked'" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Open docs/01-real-estate-playbook.md for the full menu." -ForegroundColor DarkGray
Write-Host ""
