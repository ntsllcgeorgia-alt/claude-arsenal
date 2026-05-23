#!/usr/bin/env bash
# arsenal-intro.sh — Mac/Linux version of the welcome animation.

set -u

GREEN='\033[0;32m'
DGREEN='\033[2;32m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
GRAY='\033[0;90m'
WHITE='\033[1;37m'
NC='\033[0m'

clear

# ── Phase 1: Matrix rain ──
chars='01アイウエオカキクケコサシスセソタチツテト░▒▓█'
for r in 1 2 3 4 5 6; do
  line=''
  for i in $(seq 1 70); do
    idx=$((RANDOM % ${#chars}))
    line+="${chars:$idx:1}"
  done
  if [ "$r" -lt 3 ]; then echo -e "${DGREEN}${line}${NC}";
  else echo -e "${GREEN}${line}${NC}"; fi
  sleep 0.04
done
echo ""

# ── Phase 2: Boot sequence ──
echo -e "${GREEN}  > BOOT SEQUENCE INITIATED...${NC}";    sleep 0.3
echo -e "${GREEN}  > AUTHENTICATING USER...${NC}";        sleep 0.3
echo -e "${GREEN}  > LOADING CLAUDE ARSENAL...${NC}";     sleep 0.3
echo ""

# ── Phase 3: ASCII logo ──
cat <<'LOGO' | while IFS= read -r line; do echo -e "${GREEN}${line}${NC}"; sleep 0.02; done

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

LOGO
echo -e "${DGREEN}         ──────────  BUILT FOR REALTORS  ──────────${NC}"
echo -e "${DGREEN}         ──────────   POWERED BY CLAUDE  ──────────${NC}"
echo ""
sleep 0.4

# ── Phase 4: Loading bars ──
bar() {
  local label="$1"
  local total=15
  for i in $(seq 0 $total); do
    local filled=$i
    local empty=$((total - i))
    local pct=$((i * 100 / total))
    local f=$(printf '█%.0s' $(seq 1 $filled 2>/dev/null))
    local e=$(printf '░%.0s' $(seq 1 $empty 2>/dev/null))
    printf "\r  ${CYAN}%-22s${NC} ${GREEN}[%s%s] %d%%${NC}" "$label" "$f" "$e" "$pct"
    sleep 0.04
  done
  echo ""
}
echo -e "${YELLOW}  ▶ LOADING MODULES${NC}"
echo ""
bar "Skills"
bar "Agents"
bar "Plugins"
bar "Settings"
bar "MCP Servers"
echo ""
sleep 0.2

# ── Phase 5: Stats ──
skill_count=$(find "$HOME/.claude/skills" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
agent_count=$(find "$HOME/.claude/agents" -maxdepth 1 -mindepth 1 -type f 2>/dev/null | wc -l | tr -d ' ')

echo -e "${GREEN}  ╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}  ║                                                          ║${NC}"
echo -e "${GREEN}  ║   ARSENAL ONLINE                                         ║${NC}"
echo -e "${GREEN}  ║                                                          ║${NC}"
printf "${GREEN}  ║   ▸ %3d skills loaded                                    ║${NC}\n" "$skill_count"
printf "${GREEN}  ║   ▸ %3d agents armed                                     ║${NC}\n" "$agent_count"
echo -e "${GREEN}  ║   ▸   3 plugins enabled                                  ║${NC}"
echo -e "${GREEN}  ║                                                          ║${NC}"
echo -e "${GREEN}  ║   Status: READY                                          ║${NC}"
echo -e "${GREEN}  ║                                                          ║${NC}"
echo -e "${GREEN}  ╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
sleep 0.6

# ── Phase 6: Next steps ──
echo -e "${WHITE}  Welcome to your arsenal.${NC}"
echo ""
echo -e "${GRAY}  This was hand-built over months of 8-hour sessions inside${NC}"
echo -e "${GRAY}  Claude Code. Every skill, every agent, every workflow.${NC}"
echo -e "${GRAY}  You just got it for free.${NC}"
echo ""
echo -e "${YELLOW}  Try one of these to get moving:${NC}"
echo ""
echo -e "    ${CYAN}/find-skills${NC}             discover everything you can do"
echo -e "    ${CYAN}'design a landing page for my listing on 123 Maple St.'${NC}"
echo -e "    ${CYAN}'write a cold email to FSBO sellers in my zip code'${NC}"
echo -e "    ${CYAN}'make a 15-second video of this house for Instagram'${NC}"
echo -e "    ${CYAN}'audit my last 50 social posts and find what worked'${NC}"
echo ""
echo -e "${GRAY}  Open docs/01-real-estate-playbook.md for the full menu.${NC}"
echo ""
