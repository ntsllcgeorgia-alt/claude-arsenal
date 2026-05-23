# watch-and-implement — Claude watches, transcribes, extracts, and ships

## What this skill does

End-to-end pipeline: video URL or local file → full eyes/ears coverage → structured action items → autonomous implementation of the parts you approves.

Bridges `watch-link` / `watch-video` (which only consume) with the JARVIS pipeline (which produces). The output isn't just a summary — it's a working checklist of changes the system can apply to itself.

## When to use

| Situation | Use this skill? |
|---|---|
| Tutorial / demo video you wants to learn from | ✅ Yes |
| Article-as-video with techniques worth stealing | ✅ Yes |
| "Build a path to watch + implement" requests | ✅ Yes |
| 1-on-1 interviews with no actionable steps | ❌ Use `watch-link` only |
| Music videos / entertainment | ❌ Use `watch-video` only |
| Already-watched video — just need to implement | ❌ Use this skill in `--from-existing` mode |

## Pipeline stages

```
1. DOWNLOAD       ── yt-dlp pulls video + audio streams (HLS-fragmented)
2. EXTRACT        ── ffmpeg makes keyframes + audio.mp3
3. ANALYZE        ── Gemini Files API reads full video → analysis.md
4. TRANSCRIBE     ── Gemini Flash audio → transcript.txt (every word, timestamped)
5. EXTRACT-ACTIONS── this skill parses analysis + transcript into actions.md
6. APPROVE        ── you reviews + checks the boxes he wants applied
7. IMPLEMENT      ── parent agent reads actions.md and applies changes
```

Stages 1-4 are the existing `watch-link` skill. Stages 5-7 are this skill's contribution.

## Usage

```bash
# Full pipeline from URL
python watch_and_implement.py <video_url>

# Skip download — extract actions from already-watched output folder
python watch_and_implement.py --from-existing <path-to-watch-folder>
```

Output is `actions.md` inside the same `<filename>_watch/` folder as the other artifacts.

## actions.md schema

The skill writes a structured checklist with these sections:

```markdown
# Actions from <video title>

Source: <url or file>
Length: <mm:ss>
Watched: <timestamp>

## Quick wins (< 5 min to implement)
- [ ] <action>  — <quote from transcript> [hh:mm:ss]
- [ ] <action>  — <quote from transcript> [hh:mm:ss]

## New skills to install
- [ ] <skill name> — purpose — install command

## Vault changes
- [ ] <file path> — what to write/change
- [ ] <folder path> — what to create

## Workflow / ritual additions
- [ ] <step to add to JARVIS daily/weekly>

## Patterns worth stealing (no immediate action)
- <pattern> — <where it would apply in the user's work>

## Out of scope (won't apply)
- <thing> — <why not>
```

## ETA model (so we can quote real numbers, not vibes)

A video this skill processes goes through these stages with these typical durations:

| Stage | Time per minute of video | Notes |
|---|---|---|
| Download (HLS) | 7-12 sec/min | depends on connection + video bitrate |
| ffmpeg keyframes + audio | 0.5 sec/min | local, fast |
| Gemini upload | 0.5-1 sec/min | depends on upload bandwidth |
| Gemini full-video analysis | 4-8 sec/min | Files API serial |
| Gemini audio transcription | 1-2 sec/min | Flash audio |
| **action-extract (this skill)** | 0.5-1 sec/min | local LLM call to parse |
| **TOTAL** | ~13-25 sec per minute of video | so a 60-min video ≈ 13-25 min wall time |

In parallel mode (`watch-links-parallel`), wall time = max(per-video time), not sum.

## After implementation

Each applied action gets a one-line postmortem appended to the JARVIS log:

```markdown
2026-05-15 23:55 — applied: <action>  — source: <video url> [hh:mm:ss]
```

Compounding: every video watched makes the system more capable, with a paper trail of what came from where.

## Hard rules (same as JARVIS CLAUDE.md)

- Never touch files in `04-PUBLISHED/`
- Never modify the your-agency.com homepage or `clients/regal-nails/`
- Never apply an action without the user's checkbox approval
- Never invent quotes — every cited quote must be findable in `transcript.txt`
