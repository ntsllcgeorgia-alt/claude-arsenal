---
name: watch-link
description: Watch any video link (X/Twitter, YouTube, TikTok, Instagram, Vimeo, etc.) by downloading it locally via yt-dlp, then analyzing it with the watch-video skill. Use when you pastes a URL and asks to watch it, when the URL is to X/Twitter/YouTube/TikTok/Instagram/Vimeo or any video-hosting platform yt-dlp supports, when previous WebFetch on a social-media URL returned a login wall or 402, or when the user says "watch this link" or "look at this post." Especially for X.com (Twitter) links since X blocks unauthenticated WebFetch with HTTP 402.
allowed-tools: Bash(python:*) Bash(yt-dlp:*) Bash(pip:*)
---

# Watch Link — Download + Watch ANY video URL

## What this does

Bridges the gap between Claude Code's WebFetch (which X.com, Twitter, TikTok, and some YouTube videos block with login walls) and the watch-video skill (which needs a local file). Pipeline:

1. Accept ANY URL (X, Twitter, YouTube, TikTok, Vimeo, Instagram, Reddit, Facebook, LinkedIn, ~1000 sites yt-dlp supports)
2. Download the video to `~/Downloads/` using yt-dlp (uses guest tokens, no auth needed for public posts)
3. Invoke watch-video on the downloaded file
4. Return Gemini's analysis (visual walkthrough + transcript + summary)

## Why this exists

WebFetch on `x.com/*` returns HTTP 402 because X blocks unauthenticated scraping. Nitter mirrors are mostly dead. But yt-dlp's guest-token approach still works for public posts. So: download → watch local file → analyze.

## How to invoke

```bash
python $HOME/.claude/skills/watch-link/watch_link.py "<URL>"
```

The script:
1. Validates the URL
2. Pulls the video via `python -m yt_dlp --merge-output-format mp4 -o <Downloads>/<safe-filename>.%(ext)s <URL>`
3. Runs `watch_video.py` on the downloaded mp4
4. Returns the path to the watch report folder

Then Claude reads:
- `<download_dir>_watch/analysis.md` for Gemini's structured walkthrough
- `<download_dir>_watch/transcript.txt` for verbatim speech (if any)
- 3-6 frames from `<download_dir>_watch/frames/` to visually confirm key moments

## Prerequisites (auto-handled)

The script auto-installs yt-dlp via pip if not present. Requires:
- Python 3.10+ (you has 3.12 at C:\Python312)
- ffmpeg on PATH (you has it via choco)
- Gemini API key (already set up for watch-video)

## Supported sites (partial list)

- **X / Twitter** — `x.com/*`, `twitter.com/*` ← primary motivator for this skill
- **YouTube** — `youtube.com/watch?v=*`, `youtu.be/*`
- **TikTok** — `tiktok.com/@*/video/*`
- **Instagram** — `instagram.com/p/*`, `instagram.com/reel/*`
- **Vimeo** — `vimeo.com/*`
- **Reddit** — `reddit.com/r/*/comments/*` (with v.redd.it videos)
- **Facebook** — `facebook.com/*/videos/*`
- **LinkedIn** — `linkedin.com/posts/*` (sometimes)
- Plus ~1000 more via yt-dlp's extractors

## Failure modes + responses

- **Private/locked post** → yt-dlp errors with "Private video" or "Login required". Tell you the post is private and ask if he wants to provide login (saved cookies via `--cookies-from-browser firefox`).
- **Geo-blocked** → try `--geo-bypass`
- **Live stream** → yt-dlp will record what's playing now; warn user it's a partial capture
- **Audio-only post / image post** → yt-dlp downloads audio or images; watch-video adapts (no-audio mode, image-list mode)
- **Rate-limited by platform** → wait 30s and retry once
- **Gemini API down** → skip Step 3, return raw frames + transcript only

## Privacy note

Downloaded videos land in `~/Downloads/`. They get uploaded to Gemini for analysis (Files API). Per Gemini TOS, content isn't used for training, but it does pass through Google servers. If a video is sensitive, tell Claude "don't upload" and the script can fall back to local-only frame extraction.

## Cost

- yt-dlp + ffmpeg: free, local
- Gemini analysis: ~$0.001–$0.01 per video depending on length
- Typical 30s X video: <$0.005

## Example use

```
User: "Watch this https://x.com/noisyb0y1/status/2054446384535793867"

Claude triggers watch-link:
  → python watch_link.py "https://x.com/noisyb0y1/status/2054446384535793867"
  → yt-dlp downloads to ~/Downloads/noisyb0y1_2054446384535793867.mp4
  → watch_video.py runs analysis
  → output at ~/Downloads/noisyb0y1_2054446384535793867_watch/

Claude reads analysis.md + sample frames + responds with what's actually in the video.
```
