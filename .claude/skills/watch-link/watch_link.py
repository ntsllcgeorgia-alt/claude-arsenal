#!/usr/bin/env python3
"""watch-link — download any video URL (X, YouTube, TikTok, etc.) then run watch-video on it.

Usage:
    python watch_link.py <URL>

Pipeline:
  1. Ensure yt-dlp installed (auto-install if missing)
  2. Download video to ~/Downloads/<safe-name>.mp4 via yt-dlp guest tokens
  3. Invoke ~/.claude/skills/watch-video/watch_video.py on the file
  4. Print the path to the watch report folder
"""

import sys
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse


def ensure_yt_dlp():
    """Make sure yt-dlp is importable. Install via pip if not."""
    try:
        import yt_dlp  # noqa: F401
        return True
    except ImportError:
        print("[watch-link] yt-dlp not found — installing via pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "yt-dlp"], check=True)
        return True


def safe_filename_from_url(url: str) -> str:
    """Derive a safe filename stem from any video URL.
    Examples:
      https://x.com/noisyb0y1/status/2054446384535793867 -> noisyb0y1_2054446384535793867
      https://www.youtube.com/watch?v=dQw4w9WgXcQ -> youtube_dQw4w9WgXcQ
      https://www.tiktok.com/@user/video/12345 -> tiktok_user_12345
    """
    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "").replace(".com", "").replace(".net", "").replace(".tv", "")
    path_parts = [p for p in parsed.path.split("/") if p]
    # x.com/<user>/status/<id>
    if "x" in host or "twitter" in host:
        if len(path_parts) >= 3 and path_parts[1] == "status":
            return f"{path_parts[0]}_{path_parts[2]}"
    # tiktok.com/@user/video/12345
    if "tiktok" in host:
        if len(path_parts) >= 3:
            user = path_parts[0].replace("@", "")
            return f"tiktok_{user}_{path_parts[-1]}"
    # youtube
    if "youtube" in host or "youtu" in host:
        # ?v=ID
        from urllib.parse import parse_qs
        qs = parse_qs(parsed.query)
        vid = qs.get("v", [None])[0] or path_parts[-1]
        if vid:
            return f"youtube_{vid}"
    # generic fallback
    safe = re.sub(r"[^a-zA-Z0-9_-]+", "_", "_".join(path_parts) or host)
    return f"{host}_{safe}"[:80]


def download_video(url: str, out_dir: Path) -> Path:
    """Download a video URL via yt-dlp. Returns path to the resulting mp4."""
    stem = safe_filename_from_url(url)
    out_template = str(out_dir / f"{stem}.%(ext)s")
    print(f"[watch-link] downloading: {url}")
    print(f"[watch-link] output template: {out_template}")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--no-playlist",
        "--no-warnings",
        "--quiet",
        "--progress",
        "--merge-output-format", "mp4",
        "--output", out_template,
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[watch-link] yt-dlp stderr:\n{result.stderr[-1500:]}")
        raise RuntimeError(f"yt-dlp failed with exit {result.returncode}")
    # Find the resulting file
    candidates = sorted(out_dir.glob(f"{stem}.*"), key=lambda p: p.stat().st_mtime, reverse=True)
    mp4 = next((c for c in candidates if c.suffix.lower() == ".mp4"), None)
    if not mp4:
        mp4 = next((c for c in candidates if c.suffix.lower() in (".webm", ".mkv", ".mov", ".m4v")), None)
    if not mp4:
        raise FileNotFoundError(f"No video file produced in {out_dir} for stem {stem}")
    print(f"[watch-link] downloaded: {mp4}")
    return mp4


def watch_video(path: Path) -> Path:
    """Invoke the watch-video skill on a local file. Returns the _watch directory."""
    watch_script = Path.home() / ".claude" / "skills" / "watch-video" / "watch_video.py"
    if not watch_script.exists():
        raise FileNotFoundError(f"watch-video skill missing at {watch_script}")
    print(f"[watch-link] invoking watch-video on: {path}")
    result = subprocess.run(
        [sys.executable, str(watch_script), str(path)],
        capture_output=False
    )
    if result.returncode != 0:
        raise RuntimeError(f"watch-video exited with {result.returncode}")
    watch_dir = path.with_name(path.stem + "_watch")
    if not watch_dir.exists():
        raise FileNotFoundError(f"Expected output dir not found: {watch_dir}")
    return watch_dir


def main():
    if len(sys.argv) < 2:
        print("Usage: python watch_link.py <URL>")
        sys.exit(2)
    url = sys.argv[1]

    downloads = Path.home() / "Downloads"
    downloads.mkdir(exist_ok=True)

    ensure_yt_dlp()
    video_path = download_video(url, downloads)
    watch_dir = watch_video(video_path)

    print()
    print("=" * 60)
    print(f"[watch-link] DONE")
    print(f"  Video:  {video_path}")
    print(f"  Report: {watch_dir}")
    print(f"  Read:   {watch_dir / 'analysis.md'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
