#!/usr/bin/env python3
"""watch-links-parallel: run watch_link.py for N URLs concurrently.

Usage: python watch_links_parallel.py URL1 URL2 [URL3 ...]

Each URL spawns its own watch-link subprocess. They run concurrently in
threads (since the heavy work is download + remote Gemini analysis, not CPU).
Each subprocess downloads + Gemini-analyzes independently. Output folders
land next to each downloaded video, in standard watch-link locations.

Total wall time ~= the longest single video. Saves 50-70% vs serial for
batches of 2-4 videos.
"""
import sys
import subprocess
import concurrent.futures
import time
from pathlib import Path

# Resolve sibling watch-link skill
SKILL_DIR = Path(__file__).resolve().parent
WATCH_LINK = SKILL_DIR.parent / "watch-link" / "watch_link.py"

TIMEOUT_PER_URL = 30 * 60  # 30 minutes


def run_one(url: str) -> dict:
    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, str(WATCH_LINK), url],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_PER_URL,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = int(time.time() - start)
        return {
            "url": url,
            "ok": result.returncode == 0,
            "rc": result.returncode,
            "elapsed_sec": elapsed,
            "stdout_tail": (result.stdout or "")[-2000:],
            "stderr_tail": (result.stderr or "")[-1000:] if result.returncode else "",
        }
    except subprocess.TimeoutExpired:
        return {
            "url": url,
            "ok": False,
            "rc": -1,
            "elapsed_sec": TIMEOUT_PER_URL,
            "stdout_tail": "",
            "stderr_tail": f"TIMEOUT after {TIMEOUT_PER_URL // 60} minutes",
        }
    except Exception as e:
        return {
            "url": url,
            "ok": False,
            "rc": -2,
            "elapsed_sec": int(time.time() - start),
            "stdout_tail": "",
            "stderr_tail": f"EXCEPTION: {type(e).__name__}: {e}",
        }


def main() -> int:
    urls = sys.argv[1:]
    if not urls:
        print("usage: watch_links_parallel.py URL1 URL2 [URL3 ...]", file=sys.stderr)
        return 2

    if not WATCH_LINK.exists():
        print(f"ERROR: watch_link.py not found at {WATCH_LINK}", file=sys.stderr)
        return 3

    print(f"==> watching {len(urls)} videos in parallel (timeout {TIMEOUT_PER_URL // 60}min each)")
    for u in urls:
        print(f"    - {u}")
    print()

    started = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(urls)) as ex:
        future_to_url = {ex.submit(run_one, u): u for u in urls}
        results = []
        for fut in concurrent.futures.as_completed(future_to_url):
            r = fut.result()
            status = "OK  " if r["ok"] else "FAIL"
            print(f"[{status}] {r['url']}  ({r['elapsed_sec']}s)")
            results.append(r)

    total = int(time.time() - started)
    print()
    print("========== SUMMARY ==========")
    print(f"total wall time: {total}s ({total // 60}m {total % 60}s)")
    ok_count = sum(1 for r in results if r["ok"])
    print(f"succeeded: {ok_count}/{len(results)}")

    for r in results:
        print()
        print(f"--- {r['url']} ---")
        print(f"  rc={r['rc']} elapsed={r['elapsed_sec']}s")
        if not r["ok"] and r["stderr_tail"]:
            print(f"  stderr: {r['stderr_tail']}")
        if r["stdout_tail"]:
            tail_lines = r["stdout_tail"].splitlines()[-6:]
            for line in tail_lines:
                print(f"  | {line}")

    return 0 if ok_count == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
