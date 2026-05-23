"""
Fetch a brand DESIGN.md from getdesign.md (or fall back to opening it in browser).

Usage:
    python pull_getdesign_md.py <BRAND_NAME> <OUTPUT_PATH>

Example:
    python pull_getdesign_md.py caterpillar D:/Projects/ntp-mobile-app/DESIGN.md

Tries common URL patterns. If none resolve, opens getdesign.md in browser
and surfaces instructions for manual download.
"""
import sys, os, subprocess, urllib.request, urllib.error
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# Best-guess URL patterns (getdesign.md API is undocumented as of 2026-05-03)
URL_PATTERNS = [
    "https://getdesign.md/{slug}.md",
    "https://getdesign.md/brands/{slug}.md",
    "https://getdesign.md/api/brand/{slug}",
    "https://getdesign.md/{slug}/DESIGN.md",
    "https://raw.githubusercontent.com/getdesign-md/brands/main/{slug}.md",
]


def slugify(name: str) -> str:
    return name.lower().strip().replace(" ", "-").replace("_", "-")


def try_fetch(url: str, timeout: int = 10):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            if r.status == 200:
                return r.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception):
        pass
    return None


def open_in_browser(url: str):
    """Cross-platform browser open."""
    if sys.platform == "win32":
        os.startfile(url)
    elif sys.platform == "darwin":
        subprocess.run(["open", url])
    else:
        subprocess.run(["xdg-open", url])


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    brand = sys.argv[1]
    out_path = Path(sys.argv[2])
    slug = slugify(brand)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"trying to fetch DESIGN.md for '{brand}' (slug='{slug}')...")
    for pattern in URL_PATTERNS:
        url = pattern.format(slug=slug)
        print(f"  trying {url}")
        content = try_fetch(url)
        if content and ("# " in content or "##" in content):
            out_path.write_text(content, encoding="utf-8")
            print(f"\n  fetched {len(content)} chars")
            print(f"  saved: {out_path}")
            return

    # Fallback — open getdesign.md in browser
    print()
    print("Auto-fetch failed. Falling back to manual download.")
    print()
    print("Opening getdesign.md in browser. Steps:")
    print(f"  1. Search for '{brand}'")
    print(f"  2. Click the brand → Download DESIGN.md")
    print(f"  3. Save to: {out_path}")
    print()
    fallback_url = f"https://getdesign.md/?q={slug}"
    open_in_browser(fallback_url)
    print(f"  opened {fallback_url}")
    print()
    print("If getdesign.md doesn't have the brand, options:")
    print(f"  A) Use the scrape_brand_to_design_md.py script with the brand's website")
    print(f"  B) Build DESIGN.md from scratch via Claude Code conversation")


if __name__ == "__main__":
    main()
