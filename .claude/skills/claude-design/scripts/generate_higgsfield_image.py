"""
Generate an image via Higgsfield Soul API (Nano Banana 2 model).

Hazem's Higgsfield account. Auth pattern matches his existing prompt_to_image.py
in $HOME/OneDrive/Desktop/json prompt/.

Usage:
    python generate_higgsfield_image.py --prompt "..." --out PATH [options]

Options:
    --prompt "..."          Required. Image description (under 500 chars).
    --out PATH              Required. Output file path (.png or .jpg).
    --aspect 1:1|16:9|9:16|4:3|3:2|2:3   Default: 1:1
    --quality 1080p|2048p   Default: 1080p
    --refs URL1,URL2,URL3   Optional. Up to 3 reference image URLs.
    --consistency-id ID     Optional. snake_case ID for series consistency.

Example:
    python generate_higgsfield_image.py \\
      --prompt "Mobile app login screen, dark modern bold, NTP truck parts dealer brand, hot accent CTAs, slick" \\
      --out "D:/Projects/ntp-mobile-app/assets/login_concept.png" \\
      --aspect 9:16 \\
      --quality 1080p
"""
import argparse
import os
import sys
import time
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import requests

# Set these as environment variables. Get them from your Higgsfield dashboard.
HIGGSFIELD_API_KEY = os.environ.get("HIGGSFIELD_API_KEY") or "YOUR_HIGGSFIELD_API_KEY_HERE"
HIGGSFIELD_API_SECRET = os.environ.get("HIGGSFIELD_API_SECRET") or "YOUR_HIGGSFIELD_API_SECRET_HERE"
HIGGSFIELD_BASE = "https://platform.higgsfield.ai"


def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)


def generate(prompt: str, out_path: str, aspect: str = "1:1",
             quality: str = "1080p", refs: list = None,
             consistency_id: str = None) -> str:
    """Submit a Higgsfield Nano Banana 2 job and download the result."""

    if not refs:
        refs = []
    refs = refs[:3]  # API limit

    if len(prompt) > 500:
        log(f"  prompt too long ({len(prompt)} chars), truncating to 500")
        prompt = prompt[:500]

    headers = {
        "hf-api-key": HIGGSFIELD_API_KEY,
        "hf-secret": HIGGSFIELD_API_SECRET,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    input_images = [{"type": "image_url", "image_url": u} for u in refs]

    payload = {
        "params": {
            "prompt": prompt,
            "aspect_ratio": aspect,
            "quality": quality,
            "input_images": input_images,
        }
    }
    if consistency_id:
        payload["params"]["consistency_id"] = consistency_id

    log(f"submitting Higgsfield Nano Banana job (aspect={aspect}, quality={quality})")
    if refs:
        log(f"  with {len(refs)} reference image(s)")

    resp = requests.post(
        f"{HIGGSFIELD_BASE}/v1/text2image/nano-banana",
        headers=headers, json=payload, timeout=30,
    )
    if not resp.ok:
        body_safe = resp.text[:500].encode("ascii", "replace").decode("ascii")
        log(f"  API error {resp.status_code}: {body_safe}")
    resp.raise_for_status()
    data = resp.json()
    job_set_id = data.get("job_set_id") or data.get("id")
    if not job_set_id:
        raise RuntimeError(f"no job_set_id returned: {data}")
    log(f"  job_set_id: {job_set_id}")

    log("  waiting for completion (max 3 min)...")
    image_url = None
    for i in range(60):
        time.sleep(3)
        status_resp = requests.get(
            f"{HIGGSFIELD_BASE}/v1/job-sets/{job_set_id}",
            headers=headers, timeout=15,
        )
        status_resp.raise_for_status()
        status_data = status_resp.json()
        jobs = status_data.get("jobs", [])
        if jobs:
            status = jobs[0].get("status", "")
            if status == "completed":
                log(f"  completed after {(i+1)*3}s")
                results = jobs[0].get("results", {})
                image_url = (
                    results.get("raw", {}).get("url")
                    or results.get("min", {}).get("url")
                )
                break
            elif status in ("failed", "cancelled"):
                raise RuntimeError(f"job {status}: {status_data}")
    else:
        raise TimeoutError("generation timed out after 3 minutes")

    if not image_url:
        raise RuntimeError("no image URL in completed job")

    log(f"  downloading: {image_url[:80]}...")
    img_resp = requests.get(image_url, timeout=60)
    img_resp.raise_for_status()

    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(img_resp.content)
    log(f"  saved: {out_path} ({len(img_resp.content)//1024} KB)")
    return out_path


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--prompt", required=True, help="Image prompt (under 500 chars)")
    parser.add_argument("--out", required=True, help="Output file path")
    parser.add_argument("--aspect", default="1:1", choices=["1:1", "16:9", "9:16", "4:3", "3:2", "2:3"])
    parser.add_argument("--quality", default="1080p", choices=["1080p", "2048p"])
    parser.add_argument("--refs", default="", help="Comma-separated reference image URLs (max 3)")
    parser.add_argument("--consistency-id", default=None, help="Optional consistency_id for series")
    args = parser.parse_args()

    refs = [u.strip() for u in args.refs.split(",") if u.strip()]

    try:
        generate(
            prompt=args.prompt,
            out_path=args.out,
            aspect=args.aspect,
            quality=args.quality,
            refs=refs,
            consistency_id=args.consistency_id,
        )
        log("DONE")
    except Exception as e:
        err = str(e).encode("ascii", "replace").decode("ascii")[:300]
        log(f"ERR: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
