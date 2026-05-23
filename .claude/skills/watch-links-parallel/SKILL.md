# watch-links-parallel — Claude watches N videos at once

## What this skill does

Wraps the `watch-link` skill in a thread pool so 2+ X/YouTube/TikTok/Vimeo videos can be downloaded + Gemini-analyzed concurrently instead of one after another.

Heavy work is network I/O (download + Gemini upload) — threads are the right tool. Each URL gets its own download folder + analysis artifacts, identical to running `watch-link` alone.

## When to use

| Situation | Use this skill? |
|---|---|
| User pastes 2+ video URLs in one message | ✅ Yes |
| "Watch these videos" / "compare these" / "all of them" | ✅ Yes |
| Single URL | ❌ Use `watch-link` directly |
| Already-downloaded videos | ❌ Use `watch-video` directly |
| Audio-only files | ❌ Use `watch-video` directly |

## Usage

```bash
python $HOME/.claude/skills/watch-links-parallel/watch_links_parallel.py URL1 URL2 [URL3 ...]
```

Each URL → its own `watch-link` subprocess → runs concurrently in a thread pool.

Output folders land in standard `watch-link` locations (next to each downloaded video, named `<basename>_watch/` with `analysis.md`, `transcript.txt`, `frames/`, etc.).

## After the script returns

Claude reads each video's `analysis.md` + relevant frames + transcript snippets, then synthesizes across all videos. This script doesn't combine outputs — that's the parent agent's job, where comparison and judgment matter.

## Limits + tradeoffs

- **Practical max:** 3-4 URLs at a time. More than that hits network bandwidth ceilings and Gemini API rate limits.
- **Per-URL timeout:** 30 minutes. Long videos (45+ min) eat most of this.
- **Total wall time:** roughly equal to the longest single video, not the sum.
- **Privacy:** same as `watch-link` — videos pass through Gemini Files API. Warn the user if any URL points at sensitive content.

## Failure modes

- Any single URL fails → that result is marked `FAIL` with stderr tail; other URLs still complete and their artifacts remain.
- `watch_link.py` not found → script exits 3 with clear error.
- `yt-dlp` not installed → handled by `watch-link` (auto-installs via pip).

## Example

```bash
python watch_links_parallel.py \
  https://x.com/eng_khairallah1/status/2047424070418075976 \
  https://x.com/0xMovez/status/2055413076661350631
```

Both videos download + analyze in parallel. Final summary prints OK/FAIL + elapsed per URL.
