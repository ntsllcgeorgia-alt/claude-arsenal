#!/usr/bin/env bash
# bootstrap.sh — Mac/Linux one-line installer.
#
# Paste this one-liner into Terminal:
#
#   curl -fsSL https://raw.githubusercontent.com/ntsllcgeorgia-alt/claude-arsenal/main/bootstrap/bootstrap.sh | bash

set -euo pipefail

REPO_URL="https://github.com/ntsllcgeorgia-alt/claude-arsenal.git"
TARGET_DIR="$HOME/claude-realtor-arsenal"

echo ""
echo "  Downloading the Claude Realtor Arsenal..."
echo ""

# Check for git
if ! command -v git >/dev/null 2>&1; then
  echo "  Git not found. Please install git first:"
  echo "    Mac:   xcode-select --install"
  echo "    Linux: sudo apt-get install git    (or your distro's equivalent)"
  exit 1
fi

# Clone or update
if [ -d "$TARGET_DIR" ]; then
  echo "  Repo already exists at $TARGET_DIR — pulling latest..."
  git -C "$TARGET_DIR" pull --quiet
else
  echo "  Cloning to $TARGET_DIR ..."
  git clone --quiet "$REPO_URL" "$TARGET_DIR"
fi

# Run installer
echo ""
echo "  Running install.sh..."
echo ""
bash "$TARGET_DIR/install.sh"
