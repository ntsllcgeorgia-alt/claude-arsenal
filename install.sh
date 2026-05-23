#!/usr/bin/env bash
# install.sh — Mac/Linux installer for the Claude Realtor Arsenal.
#
# Run from the repo root:
#   bash ./install.sh

set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[0;33m'; CYAN='\033[0;36m'
GRAY='\033[0;90m';  WHITE='\033[1;37m';  NC='\033[0m'

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
claude_dir="$HOME/.claude"
timestamp="$(date +%Y%m%d-%H%M%S)"
backup_root="$HOME/.claude-backup-$timestamp"

echo ""
echo -e "${GREEN}  ┌──────────────────────────────────────────────────────────┐${NC}"
echo -e "${GREEN}  │       Installing the Claude Realtor Arsenal              │${NC}"
echo -e "${GREEN}  └──────────────────────────────────────────────────────────┘${NC}"
echo ""

mkdir -p "$claude_dir"

# Backup existing
did_backup=false
for item in skills agents CLAUDE.md settings.json; do
  if [ -e "$claude_dir/$item" ]; then
    if ! $did_backup; then
      mkdir -p "$backup_root"
      echo -e "${YELLOW}  ✓ Backing up existing setup to $backup_root${NC}"
      did_backup=true
    fi
    cp -R "$claude_dir/$item" "$backup_root/"
    echo -e "${GRAY}    · backed up $item${NC}"
  fi
done

# Skills
mkdir -p "$claude_dir/skills"
skill_count=0
for d in "$repo_root/.claude/skills"/*/; do
  cp -R "$d" "$claude_dir/skills/"
  skill_count=$((skill_count + 1))
done
echo -e "${GREEN}  ✓ Installed $skill_count skills${NC}"

# Agents
mkdir -p "$claude_dir/agents"
agent_count=0
for f in "$repo_root/.claude/agents"/*; do
  cp "$f" "$claude_dir/agents/"
  agent_count=$((agent_count + 1))
done
echo -e "${GREEN}  ✓ Installed $agent_count agents${NC}"

# CLAUDE.md
if [ ! -f "$claude_dir/CLAUDE.md" ]; then
  cp "$repo_root/.claude/CLAUDE.md.template" "$claude_dir/CLAUDE.md"
  echo -e "${GREEN}  ✓ Installed CLAUDE.md${NC}"
else
  echo -e "${YELLOW}  · CLAUDE.md already exists — left it alone${NC}"
fi

# settings.json
if [ ! -f "$claude_dir/settings.json" ]; then
  cp "$repo_root/.claude/settings.template.json" "$claude_dir/settings.json"
  echo -e "${GREEN}  ✓ Installed settings.json (you'll fill in API keys later)${NC}"
else
  echo -e "${YELLOW}  · settings.json already exists — left it alone${NC}"
fi

# Intro animation
cp "$repo_root/bootstrap/arsenal-intro.ps1" "$claude_dir/arsenal-intro.ps1"
cp "$repo_root/bootstrap/arsenal-intro.sh"  "$claude_dir/arsenal-intro.sh"
chmod +x "$claude_dir/arsenal-intro.sh"
echo -e "${GREEN}  ✓ Installed welcome animation${NC}"

# First-run marker
date -u +"%Y-%m-%dT%H:%M:%SZ" > "$claude_dir/.arsenal-first-run"
echo -e "${GREEN}  ✓ First-run marker set${NC}"

echo ""
echo -e "${GREEN}  ┌──────────────────────────────────────────────────────────┐${NC}"
echo -e "${GREEN}  │   DONE                                                   │${NC}"
echo -e "${GREEN}  └──────────────────────────────────────────────────────────┘${NC}"
echo ""
echo -e "${YELLOW}  Next steps:${NC}"
echo ""
echo -e "${WHITE}    1. Open VS Code${NC}"
echo -e "${WHITE}    2. Launch Claude Code${NC}"
echo -e "${CYAN}    3. Type:  hey${NC}"
echo ""
echo -e "${GRAY}  Animation will play. Then you're armed.${NC}"
echo ""
if $did_backup; then
  echo -e "${GRAY}  (Your previous setup is safe at: $backup_root)${NC}"
  echo ""
fi
