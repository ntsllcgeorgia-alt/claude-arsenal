---
name: watch-video
description: Let Claude actually WATCH a video file (or audio file) end-to-end — transcript + visual scene analysis + key-moment timeline. Combines (a) ffmpeg keyframe extraction so Claude can read the frames as images via the Read tool, (b) full audio transcription via Gemini, and (c) Gemini's native video understanding for visual + audio analysis. Output is a unified watch report Claude can reason over the same way a human would after watching.

Use when: user shares a video file (.mp4, .mov, .webm, .mkv) and asks Claude to watch it, listen to it, analyze it, summarize it, find a moment, identify a speaker, react to a pitch, or extract any visual/audio content. Also use for audio-only files (.mp3, .wav, .m4a) — the visual stage is skipped.

Triggers on: "watch this video", "listen to this video", "analyze this video", "what does the guy say in this video", "summarize this clip", "/watch-video", "what's in this video".
---

# Watch Video — Claude's eyes & ears for video files

## What this skill does

Claude (the model) is multimodal — it can SEE images and READ text — but Claude Code can't natively play video or audio. This skill bridges the gap by converting any video into Claude-readable artifacts:

1. **Keyframes** (8-16 .jpg images extracted at scene changes) → Claude reads them with the Read tool to actually SEE the video
2. **Full audio transcript** (via Gemini 2.0 Flash audio understanding) → Claude reads the text
3. **Native video analysis** (full MP4 sent to Gemini Files API for combined visual+audio scene description) → Claude reads the structured analysis

Combined, Claude has the equivalent of "watched the video carefully" understanding.

## When to use

| Situation | Use this skill? |
|---|---|
| User shares a video file path | ✅ Yes |
| User says "watch this", "listen to this", "what's in this video" | ✅ Yes |
| User shares an audio file only | ✅ Yes (skips visual stage) |
| User shares a YouTube/Vimeo URL | ⚠️ First download with yt-dlp, then run this skill |
| User shares a still image | ❌ Use Read tool directly on the image |
| User shares a transcript already | ❌ Just read the transcript |

## How to invoke

```bash
python $HOME/.claude/skills/watch-video/watch_video.py "<path-to-video>"
```

Output folder is created next to the video, named `<filename>_watch/` containing:
- `frames/` — extracted keyframes
- `audio.mp3` — extracted audio
- `transcript.txt` — full audio transcript with timestamps
- `analysis.md` — Gemini's combined visual+audio analysis
- `summary.json` — structured: speakers, topics, key moments, sentiment, action items

After running, Claude reads `analysis.md`, `transcript.txt`, and 4-8 of the frames to form a complete picture. Then responds to the user's actual question.

## Workflow when user asks Claude to watch a video

1. **Find the file**: locate it (most-recent in Downloads if "the video I just downloaded")
2. **Run the script**: `python watch_video.py "<path>"`
3. **Wait for output** (typical: 30-90 sec depending on length)
4. **Read artifacts** in this order:
   - `analysis.md` (Gemini's structured walkthrough — fastest path to understanding)
   - `transcript.txt` (verbatim quotes if user wants quotes)
   - 3-6 frames from `frames/` (Claude visually inspects pivotal moments)
5. **Respond to user** with what was actually said + shown, plus answer their original question

## Cost & speed

- ffmpeg processing: ~1-2 sec for keyframes + audio extraction (free, local)
- Gemini upload + analysis: $0.001-$0.01 per video depending on length
- Typical 10-min video: <60 sec end-to-end

## Failure modes

- **Gemini API key missing**: skill has a fallback that uses keyframes + Whisper-via-CLI for transcription
- **Video > 2 GB**: warn user, suggest extracting a clip first
- **No audio track**: skill detects this and runs visual-only analysis
- **Corrupted video**: ffprobe pre-check fails, surface error to user

## Privacy note

Videos are uploaded to Google Gemini for analysis. If video is sensitive (client meeting, legal recording, personal content), warn the user before uploading. Gemini doesn't train on Files API content per their TOS, but it does pass through Google servers.
