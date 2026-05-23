# bootstrap.ps1 — the one-line installer for the Claude Realtor Arsenal.
#
# What this script does (you paste ONE line, it does everything):
#   1. Checks for git, installs via winget if missing
#   2. Clones the repo to ~/claude-realtor-arsenal
#   3. Runs install.ps1
#
# Paste this one-liner into PowerShell:
#
#   iex (iwr "https://raw.githubusercontent.com/ntsllcgeorgia-alt/claude-arsenal/main/bootstrap/bootstrap.ps1").Content

$ErrorActionPreference = 'Stop'

# CHANGE THIS if you forked the repo or renamed it:
$repoUrl = 'https://github.com/ntsllcgeorgia-alt/claude-arsenal.git'

$targetDir = Join-Path $env:USERPROFILE 'claude-realtor-arsenal'

Write-Host ""
Write-Host "  Downloading the Claude Realtor Arsenal..." -ForegroundColor Cyan
Write-Host ""

# 1. Check for git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "  Git not found. Installing via winget..." -ForegroundColor Yellow
    winget install --id Git.Git -e --source winget --silent
    # Refresh PATH so we can use git in this session
    $env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')
}

# 2. Clone or update
if (Test-Path $targetDir) {
    Write-Host "  Repo already exists at $targetDir — pulling latest..." -ForegroundColor Gray
    git -C $targetDir pull --quiet
} else {
    Write-Host "  Cloning to $targetDir ..." -ForegroundColor Gray
    git clone --quiet $repoUrl $targetDir
}

# 3. Run the installer
Write-Host ""
Write-Host "  Running install.ps1..." -ForegroundColor Cyan
Write-Host ""
& powershell -ExecutionPolicy Bypass -File (Join-Path $targetDir 'install.ps1')
