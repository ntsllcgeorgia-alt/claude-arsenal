#!/usr/bin/env python3
"""watch-and-implement: video URL -> verbatim transcript -> structured actions.

Pipeline:
  1. If URL given, call watch-link (which downloads + runs watch-video).
  2. Read analysis.md, transcript.txt, summary.json from the watch folder.
  3. Use Gemini Flash to parse the artifacts into a structured actions.md
     checklist that the parent Claude agent can execute.

Modes:
  python watch_and_implement.py <url>
  python watch_and_implement.py --from-existing <path-to-_watch-folder>

Output: actions.md inside the watch folder.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
WATCH_LINK = SKILL_DIR.parent / "watch-link" / "watch_link.py"


def run_watch_link(url: str) -> Path:
    """Run watch-link, then find the most recently created _watch folder."""
    print(f"==> watch-link {url}", flush=True)
    started = time.time()
    result = subprocess.run(
        [sys.executable, str(WATCH_LINK), url],
        capture_output=False,
        text=True,
    )
    if result.returncode != 0:
        raise SystemExit(f"watch-link failed (rc={result.returncode})")

    downloads = Path(os.path.expanduser("~")) / "Downloads"
    candidates = sorted(
        downloads.glob("*_watch"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise SystemExit("no _watch folder produced by watch-link")
    folder = candidates[0]
    print(f"==> watch folder: {folder}  ({int(time.time()-started)}s)", flush=True)
    return folder


def read_artifacts(folder: Path) -> dict:
    """Pull the three artifact strings out of the watch folder."""
    def safe_read(p: Path, limit: int = 200_000) -> str:
        if not p.exists():
            return ""
        try:
            return p.read_text(encoding="utf-8", errors="replace")[:limit]
        except Exception as e:
            return f"<read error: {e}>"

    return {
        "analysis": safe_read(folder / "analysis.md"),
        "transcript": safe_read(folder / "transcript.txt"),
        "summary": safe_read(folder / "summary.json", limit=50_000),
    }


def call_gemini_for_actions(artifacts: dict, source_label: str) -> str:
    """Ask Gemini Flash to extract a structured actions.md from the artifacts."""
    try:
        from google import genai
    except ImportError:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-q", "google-genai"]
            )
            from google import genai
        except Exception as e:
            return _fallback_actions(artifacts, source_label, reason=f"genai unavailable: {e}")

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return _fallback_actions(artifacts, source_label, reason="GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    prompt = f"""You are extracting actionable items from a video that the user
just watched. The user runs multiple businesses (NTP wholesale truck parts, TPP retail,
Launch & Manage digital agency, NTP Mobile App) and uses Claude Code + Obsidian as his
working environment. He wants to USE what's in the video to improve his system.

Read the analysis and transcript below, then output an actions.md file using EXACTLY this
format. Every cited quote must be a verbatim substring of the transcript. Use timestamps
from the transcript when available. Do NOT invent quotes.

Source: {source_label}

==== ANALYSIS ====
{artifacts['analysis'][:60000]}

==== TRANSCRIPT (verbatim, may be truncated) ====
{artifacts['transcript'][:80000]}

==== SUMMARY.JSON ====
{artifacts['summary'][:20000]}

==== OUTPUT FORMAT ====
Produce ONLY the markdown below — no preface, no explanation, no code fences.

# Actions from {source_label}

## Quick wins (< 5 min to implement)
- [ ] <action>  — "<verbatim quote>" [hh:mm:ss]

## New skills to install
- [ ] <skill name> — <purpose> — <install command or source>

## Vault changes
- [ ] <vault file path> — <what to write/change>

## Workflow / ritual additions
- [ ] <step to add to JARVIS daily/weekly ritual>

## Patterns worth stealing (no immediate action)
- <pattern> — <where it would apply in the user's work>

## Out of scope (won't apply)
- <thing> — <why not>

==== RULES ====
- Every section must appear, even if empty (write "- (none)" if so).
- Every quote must be a verbatim substring of the transcript.
- Be specific: "create vault/05-CLAUDE/skills/X.md" beats "add a skill."
- Prefer actions that compound (each action makes the next one easier).
- Skip generic motivational content. Only real, applicable steps.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
        )
        text = (response.text or "").strip()
        if not text:
            return _fallback_actions(artifacts, source_label, reason="empty gemini response")
        return text
    except Exception as e:
        return _fallback_actions(artifacts, source_label, reason=f"gemini call failed: {e}")


def _fallback_actions(artifacts: dict, source_label: str, reason: str) -> str:
    """Without Gemini, emit a stub that the parent agent can fill in by reading artifacts."""
    return f"""# Actions from {source_label}

> NOTE: automatic extraction failed — {reason}
> Parent Claude agent should read analysis.md + transcript.txt directly
> and fill in this checklist by hand.

## Quick wins (< 5 min to implement)
- (extract from transcript)

## New skills to install
- (extract from transcript)

## Vault changes
- (extract from transcript)

## Workflow / ritual additions
- (extract from transcript)

## Patterns worth stealing (no immediate action)
- (extract from transcript)

## Out of scope (won't apply)
- (extract from transcript)
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="watch a video and extract actionable items")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("url", nargs="?", help="video URL to watch end-to-end")
    g.add_argument("--from-existing", dest="from_existing",
                   help="skip download — extract from an existing _watch folder")
    args = parser.parse_args()

    if args.from_existing:
        folder = Path(args.from_existing).resolve()
        if not folder.is_dir():
            print(f"ERROR: not a directory: {folder}", file=sys.stderr)
            return 2
        source_label = folder.name
    else:
        if not WATCH_LINK.exists():
            print(f"ERROR: watch-link not found at {WATCH_LINK}", file=sys.stderr)
            return 3
        folder = run_watch_link(args.url)
        source_label = args.url

    artifacts = read_artifacts(folder)
    if not artifacts["analysis"] and not artifacts["transcript"]:
        print(f"ERROR: no analysis.md or transcript.txt in {folder}", file=sys.stderr)
        return 4

    print(f"==> extracting actions for {source_label}", flush=True)
    actions_md = call_gemini_for_actions(artifacts, source_label)

    out = folder / "actions.md"
    out.write_text(actions_md, encoding="utf-8")
    print(f"==> wrote {out}", flush=True)
    print()
    print(actions_md[:4000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
