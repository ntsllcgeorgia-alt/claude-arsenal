"""
watch_video.py — Make Claude actually watch a video.

Usage: python watch_video.py <path-to-video>

Outputs a folder named <video_basename>_watch/ next to the video, containing:
  - frames/         keyframes for visual inspection
  - audio.mp3       extracted audio track
  - transcript.txt  full transcript with timestamps
  - analysis.md     Gemini's combined visual + audio analysis
  - summary.json    structured key moments, topics, sentiment

Requirements: ffmpeg on PATH, google-generativeai (pip install google-generativeai).
Reads GEMINI_API_KEY from env, falls back to a hardcoded key path if needed.
"""
from __future__ import annotations
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or "YOUR_GEMINI_API_KEY_HERE"
MODEL = "gemini-2.5-flash"
MAX_FRAMES = 12


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


def probe_duration(path: Path) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)])
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def has_audio(path: Path) -> bool:
    r = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
             "stream=codec_type", "-of", "csv=p=0", str(path)])
    return "audio" in r.stdout


def extract_frames(video: Path, out_dir: Path, duration: float) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    if duration <= 0:
        return []
    interval = max(duration / MAX_FRAMES, 1.0)
    fps = 1.0 / interval
    cmd = ["ffmpeg", "-y", "-i", str(video), "-vf", f"fps={fps},scale=1024:-1",
           "-frames:v", str(MAX_FRAMES), "-q:v", "3",
           str(out_dir / "frame_%02d.jpg")]
    run(cmd)
    return sorted(out_dir.glob("frame_*.jpg"))


def extract_audio(video: Path, out_path: Path) -> Path | None:
    if not has_audio(video):
        return None
    cmd = ["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
           "-b:a", "64k", str(out_path)]
    r = run(cmd)
    return out_path if out_path.exists() else None


def gemini_analyze(video: Path) -> dict:
    """Upload the video and ask Gemini for transcript + visual analysis + structured summary."""
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)

    print(f"[gemini] uploading {video.name} ({video.stat().st_size / 1e6:.1f} MB)...")
    f = genai.upload_file(str(video))
    while f.state.name == "PROCESSING":
        time.sleep(2)
        f = genai.get_file(f.name)
    if f.state.name != "ACTIVE":
        raise RuntimeError(f"Gemini file processing failed: {f.state.name}")

    model = genai.GenerativeModel(MODEL)

    prompt = """You are watching a video for someone who cannot see or hear it. Provide a complete walkthrough.

Output FOUR sections, in this exact order, separated by the markers shown:

===TRANSCRIPT===
A verbatim transcript of all spoken audio with [MM:SS] timestamps every 15-30 seconds or at speaker changes. Include speaker labels if multiple speakers (Speaker 1, Speaker 2, etc). If the speaker is identifiable by context (a known company/person), note it.

===VISUAL===
A scene-by-scene description of what is visually shown. Include: setting, who is on camera, on-screen text/captions, slides/screen-shares, products shown, cuts, b-roll, lower thirds. Use [MM:SS] timestamps.

===ANALYSIS===
A structured analysis answering:
- Who is the speaker (or main subject)?
- What is the core message or pitch?
- What is the speaker trying to get the viewer to do?
- What's the emotional tone?
- 5 most important quotes or moments (with timestamps)
- Any claims that should be fact-checked or sound suspicious

===JSON===
A JSON object with these keys (output valid JSON only in this section):
{
  "title_guess": "...",
  "duration_seconds": 0,
  "speakers": [{"label": "Speaker 1", "identity_guess": "...", "role": "..."}],
  "topic": "...",
  "summary_one_line": "...",
  "summary_three_lines": ["...", "...", "..."],
  "key_moments": [{"time": "MM:SS", "moment": "..."}],
  "call_to_action": "...",
  "tone": "...",
  "red_flags": []
}

Be thorough — the person reading this depends entirely on you."""

    print(f"[gemini] analyzing with {MODEL}...")
    resp = model.generate_content([f, prompt], request_options={"timeout": 600})
    text = resp.text

    try:
        genai.delete_file(f.name)
    except Exception:
        pass

    sections = {"transcript": "", "visual": "", "analysis": "", "json": {}}
    for marker, key in [("===TRANSCRIPT===", "transcript"),
                        ("===VISUAL===", "visual"),
                        ("===ANALYSIS===", "analysis"),
                        ("===JSON===", "json_raw")]:
        if marker in text:
            after = text.split(marker, 1)[1]
            for stop in ["===TRANSCRIPT===", "===VISUAL===", "===ANALYSIS===", "===JSON==="]:
                if stop in after and stop != marker:
                    after = after.split(stop, 1)[0]
            sections[key if key != "json_raw" else "json_raw"] = after.strip()

    raw_json = sections.pop("json_raw", "")
    raw_json = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_json.strip(), flags=re.MULTILINE)
    try:
        sections["json"] = json.loads(raw_json)
    except Exception:
        sections["json"] = {"_parse_error": True, "_raw": raw_json}

    sections["_full_text"] = text
    return sections


def main():
    if len(sys.argv) < 2:
        print("usage: watch_video.py <video-path>")
        sys.exit(1)

    video = Path(sys.argv[1]).resolve()
    if not video.exists():
        print(f"not found: {video}")
        sys.exit(1)

    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("ffmpeg/ffprobe required on PATH")
        sys.exit(1)

    out_dir = video.parent / f"{video.stem}_watch"
    out_dir.mkdir(exist_ok=True)
    frames_dir = out_dir / "frames"

    print(f"[probe] {video.name}")
    duration = probe_duration(video)
    audio_track = has_audio(video)
    print(f"[probe] duration={duration:.1f}s audio={audio_track}")

    print(f"[ffmpeg] extracting up to {MAX_FRAMES} keyframes...")
    frames = extract_frames(video, frames_dir, duration)
    print(f"[ffmpeg] extracted {len(frames)} frames")

    if audio_track:
        print(f"[ffmpeg] extracting audio...")
        extract_audio(video, out_dir / "audio.mp3")

    sections = gemini_analyze(video)

    (out_dir / "transcript.txt").write_text(sections.get("transcript", ""), encoding="utf-8")

    analysis_md = (
        f"# Watch report — {video.name}\n\n"
        f"- Duration: {duration:.1f}s\n"
        f"- Has audio: {audio_track}\n"
        f"- Frames: {len(frames)}\n\n"
        "## Visual walkthrough\n\n"
        f"{sections.get('visual', '')}\n\n"
        "## Analysis\n\n"
        f"{sections.get('analysis', '')}\n"
    )
    (out_dir / "analysis.md").write_text(analysis_md, encoding="utf-8")
    (out_dir / "summary.json").write_text(json.dumps(sections.get("json", {}), indent=2),
                                          encoding="utf-8")
    (out_dir / "_full_gemini_response.txt").write_text(sections.get("_full_text", ""),
                                                       encoding="utf-8")

    print(f"\n[done] {out_dir}")
    print(f"  - frames/         {len(frames)} images")
    print(f"  - transcript.txt")
    print(f"  - analysis.md")
    print(f"  - summary.json")


if __name__ == "__main__":
    main()
