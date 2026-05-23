#!/usr/bin/env python3
"""Recovery script for videos too long for one-shot Gemini analysis.

When watch-video fails on a long video (Gemini Files API 504 DEADLINE_EXCEEDED),
the watch folder still has audio.mp3 + frames/ extracted by ffmpeg.

This script:
  1. Chunks the audio into 10-min slices (only if total > 12 min) via ffmpeg.
  2. Transcribes each chunk in PARALLEL through Gemini Flash audio understanding.
  3. Re-stamps timestamps with each chunk's global offset.
  4. Analyzes the 12 keyframes for visual context.
  5. Writes transcript.txt + analysis.md + summary.json.

Uses google.generativeai (same package as watch-video) for compatibility.

Usage:
  python recover_from_artifacts.py <watch-folder>
"""
from __future__ import annotations

import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

GEMINI_API_KEY = (
    os.environ.get("GEMINI_API_KEY")
    or os.environ.get("GOOGLE_API_KEY")
    or "YOUR_GEMINI_API_KEY_HERE"
)
MODEL = "gemini-2.5-flash"
CHUNK_SECONDS = 600          # 10 minutes per chunk
CHUNK_THRESHOLD_SECONDS = 720  # only chunk if audio > 12 min
MAX_PARALLEL_CHUNKS = 3      # respect rate limits
PER_CHUNK_TIMEOUT = 600      # 10 min per chunk transcription


def get_genai():
    import google.generativeai as genai  # type: ignore
    genai.configure(api_key=GEMINI_API_KEY)
    return genai


def upload_and_wait(genai, path: Path):
    print(f"[gemini] uploading {path.name} ({path.stat().st_size/1024/1024:.1f} MB)...", flush=True)
    f = genai.upload_file(str(path))
    while f.state.name == "PROCESSING":
        time.sleep(2)
        f = genai.get_file(f.name)
    if f.state.name != "ACTIVE":
        raise RuntimeError(f"Gemini file state: {f.state.name}")
    return f


def probe_duration_sec(audio_path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
        capture_output=True, text=True,
    )
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def chunk_audio(audio_path: Path, chunks_dir: Path, chunk_sec: int) -> list[Path]:
    """Split audio into chunk_sec-second slices. Returns chunk paths in order."""
    chunks_dir.mkdir(parents=True, exist_ok=True)
    for old in chunks_dir.glob("chunk_*.mp3"):
        old.unlink()
    pattern = chunks_dir / "chunk_%03d.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(audio_path),
         "-f", "segment", "-segment_time", str(chunk_sec),
         "-c", "copy", str(pattern)],
        capture_output=True, text=True,
    )
    return sorted(chunks_dir.glob("chunk_*.mp3"))


# ---- timestamp re-stamping ----
TS_RE = re.compile(r"\[(\d{1,2}):(\d{2})(?::(\d{2}))?\]")


def shift_timestamps(text: str, offset_sec: int) -> str:
    """Find every [HH:MM:SS] or [MM:SS] in text and add offset_sec."""
    def _repl(m: re.Match) -> str:
        a, b, c = m.group(1), m.group(2), m.group(3)
        if c is None:
            total = int(a) * 60 + int(b)
        else:
            total = int(a) * 3600 + int(b) * 60 + int(c)
        total += offset_sec
        hh = total // 3600
        mm = (total % 3600) // 60
        ss = total % 60
        return f"[{hh:02d}:{mm:02d}:{ss:02d}]"
    return TS_RE.sub(_repl, text)


def transcribe_chunk(chunk_idx: int, chunk_path: Path, offset_sec: int) -> tuple[int, str]:
    """Transcribe a single chunk in a fresh genai client (thread-safe)."""
    genai = get_genai()
    print(f"[chunk {chunk_idx:03d}] uploading {chunk_path.name} (offset {offset_sec}s)...", flush=True)
    f = genai.upload_file(str(chunk_path))
    while f.state.name == "PROCESSING":
        time.sleep(2)
        f = genai.get_file(f.name)
    if f.state.name != "ACTIVE":
        return chunk_idx, f"[chunk {chunk_idx}: upload failed — state {f.state.name}]"

    prompt = """Transcribe this audio file COMPLETELY and VERBATIM.

Rules:
- Every single word must be captured. Do not summarize or paraphrase.
- Include filler words (um, uh, like) when spoken.
- Add timestamps in [hh:mm:ss] format at the start of every new speaker turn AND every 30 seconds.
- If multiple speakers, label them Speaker 1 / Speaker 2 / etc., based on voice.
- Preserve emphasis and punctuation as spoken.
- If a word is unclear, write [inaudible].
- Do NOT add commentary, headers, or analysis — just the transcript.

Output format:
[00:00:00] Speaker 1: ...
[00:00:30] Speaker 1: ...
[00:01:00] Speaker 2: ...
"""

    model = genai.GenerativeModel(MODEL)
    try:
        resp = model.generate_content([f, prompt], request_options={"timeout": PER_CHUNK_TIMEOUT})
        text = (resp.text or "").strip()
        text = shift_timestamps(text, offset_sec)
        print(f"[chunk {chunk_idx:03d}] done — {len(text)} chars", flush=True)
        return chunk_idx, text
    except Exception as e:
        print(f"[chunk {chunk_idx:03d}] FAILED: {type(e).__name__}: {e}", flush=True)
        return chunk_idx, f"[chunk {chunk_idx} transcription failed: {e}]"
    finally:
        try:
            genai.delete_file(f.name)
        except Exception:
            pass


def transcribe_audio_chunked(audio_path: Path, watch_folder: Path) -> str:
    """Transcribe long audio by splitting into chunks and parallelizing."""
    duration = probe_duration_sec(audio_path)
    print(f"[audio] duration={duration:.1f}s ({duration/60:.1f} min)", flush=True)

    if duration <= CHUNK_THRESHOLD_SECONDS:
        # Short enough for single-shot
        return transcribe_chunk(0, audio_path, 0)[1]

    chunks_dir = watch_folder / "audio_chunks"
    chunk_paths = chunk_audio(audio_path, chunks_dir, CHUNK_SECONDS)
    if not chunk_paths:
        raise RuntimeError("ffmpeg produced no chunks")
    print(f"[chunk] {len(chunk_paths)} chunks of ~{CHUNK_SECONDS}s each (max {MAX_PARALLEL_CHUNKS} parallel)", flush=True)

    jobs = [(i, p, i * CHUNK_SECONDS) for i, p in enumerate(chunk_paths)]
    results: dict[int, str] = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_PARALLEL_CHUNKS) as ex:
        futures = [ex.submit(transcribe_chunk, idx, path, off) for idx, path, off in jobs]
        for fut in concurrent.futures.as_completed(futures):
            idx, text = fut.result()
            results[idx] = text

    # Concatenate in chunk order, each separated by a blank line
    parts = []
    for idx in sorted(results.keys()):
        parts.append(f"## chunk {idx:03d} (offset {idx*CHUNK_SECONDS}s)\n")
        parts.append(results[idx])
        parts.append("\n")
    full = "\n".join(parts)

    # Clean up chunks
    try:
        shutil.rmtree(chunks_dir)
    except Exception:
        pass

    return full


def analyze_frames(genai, frames_dir: Path) -> str:
    frame_files = sorted(frames_dir.glob("*.jpg"))
    if not frame_files:
        return "(no frames available)"

    print(f"[gemini] uploading {len(frame_files)} keyframes...", flush=True)
    uploaded = [upload_and_wait(genai, fp) for fp in frame_files]

    prompt = f"""You are analyzing {len(frame_files)} keyframes extracted evenly across a long video.
Frames are in chronological order (frame_01 = earliest, frame_{len(frame_files):02d} = latest).

For each frame:
1. Describe what's visible (UI / scene / text / who's on screen).
2. Identify the apparent topic or stage of the video at that moment.

Then provide:
- A unified visual narrative across the frames (what is this video about?)
- Key visual claims or screenshots that matter (named tools, code, charts, brand names)
- Who appears to be speaking or presenting
- The overall pitch or call to action

Use markdown. Be specific. Quote any visible text VERBATIM.
"""

    model = genai.GenerativeModel(MODEL)
    resp = model.generate_content([*uploaded, prompt], request_options={"timeout": 600})

    for f in uploaded:
        try:
            genai.delete_file(f.name)
        except Exception:
            pass

    return (resp.text or "").strip()


def summarize(genai, transcript: str, visual: str) -> dict:
    print(f"[gemini] generating structured summary...", flush=True)
    prompt = f"""You will produce a JSON summary of a video given its verbatim audio transcript
and a visual walkthrough of keyframes.

Return ONLY valid JSON matching this schema (no markdown, no code fences):

{{
  "title_guess": "...",
  "duration_seconds": <integer>,
  "speakers": [{{"label": "Speaker 1", "identity_guess": "...", "role": "..."}}],
  "topic": "...",
  "summary_one_line": "...",
  "summary_three_lines": ["...", "...", "..."],
  "key_moments": [{{"time": "00:00", "moment": "..."}}],
  "call_to_action": "...",
  "tone": "...",
  "red_flags": ["..."]
}}

==== TRANSCRIPT (first 80k chars) ====
{transcript[:80000]}

==== VISUAL WALKTHROUGH ====
{visual[:30000]}
"""

    model = genai.GenerativeModel(MODEL)
    resp = model.generate_content(prompt, request_options={"timeout": 300})
    raw = (resp.text or "").strip()
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        return {"_parse_error": str(e), "_raw": raw[:5000]}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: recover_from_artifacts.py <watch-folder>", file=sys.stderr)
        return 2

    folder = Path(sys.argv[1]).resolve()
    if not folder.is_dir():
        print(f"ERROR: not a directory: {folder}", file=sys.stderr)
        return 3

    audio = folder / "audio.mp3"
    frames = folder / "frames"

    if not audio.exists() and not (frames.is_dir() and any(frames.glob("*.jpg"))):
        print(f"ERROR: no audio.mp3 or frames/*.jpg in {folder}", file=sys.stderr)
        return 4

    started = time.time()
    genai = get_genai()

    # ---- audio transcript (chunked if long) ----
    transcript = ""
    if audio.exists():
        transcript = transcribe_audio_chunked(audio, folder)
        (folder / "transcript.txt").write_text(transcript, encoding="utf-8")
        print(f"[done] transcript.txt ({len(transcript)} chars)", flush=True)
    else:
        print("[skip] no audio.mp3", flush=True)

    # ---- frame analysis ----
    visual = ""
    n_frames = 0
    if frames.is_dir():
        n_frames = len(list(frames.glob("*.jpg")))
        if n_frames:
            visual = analyze_frames(genai, frames)
        else:
            print("[skip] frames/ empty", flush=True)
    else:
        print("[skip] no frames/", flush=True)

    # ---- assemble analysis.md ----
    analysis_md = f"""# Watch report — {folder.name}  (recovered)

> Original Gemini full-video analysis timed out (Files API DEADLINE_EXCEEDED).
> This report is reconstructed from chunked audio transcript + keyframe analysis.

## Visual walkthrough (from {n_frames} keyframes)

{visual}

## Transcript

See `transcript.txt` for the full verbatim transcript. First 3000 chars below for quick scan:

```
{transcript[:3000]}{'...' if len(transcript) > 3000 else ''}
```
"""
    (folder / "analysis.md").write_text(analysis_md, encoding="utf-8")
    print(f"[done] analysis.md", flush=True)

    # ---- summary.json ----
    summary = summarize(genai, transcript, visual)
    (folder / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[done] summary.json", flush=True)

    elapsed = int(time.time() - started)
    print(f"\n==> recovery complete in {elapsed}s ({elapsed//60}m {elapsed%60}s)")
    print(f"    transcript.txt: {(folder / 'transcript.txt').stat().st_size / 1024:.1f} KB")
    print(f"    analysis.md:    {(folder / 'analysis.md').stat().st_size / 1024:.1f} KB")
    print(f"    summary.json:   {(folder / 'summary.json').stat().st_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
