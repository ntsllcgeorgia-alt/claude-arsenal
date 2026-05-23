"""
Scrape a brand from a URL → produce raw brand data Claude turns into DESIGN.md.

Usage:
    python scrape_brand_to_design_md.py <URL> <OUTPUT_PATH>

Example:
    python scrape_brand_to_design_md.py https://nationaltruckparts.com D:/Projects/ntp-mobile-app/_brand_scrape.json

The output is a JSON dump of:
  - logo / favicon URLs
  - computed CSS colors (top 8 by frequency)
  - font families (display + body)
  - extracted copy (headlines, taglines, CTAs)
  - screenshots (full-page + above-fold)
  - meta info (title, og:image, theme color, etc.)

Claude then post-processes this into DESIGN.md using
~/.claude/skills/claude-design/templates/design-md-template.md as the structure.
"""
import asyncio, json, sys, os
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)


async def scrape(url: str, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    screenshot_dir = out_path.parent / "_brand_screenshots"
    screenshot_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        print(f"loading {url}...")
        await page.goto(url, wait_until="networkidle", timeout=45000)

        # screenshots
        af_path = screenshot_dir / "above_fold.png"
        full_path = screenshot_dir / "full_page.png"
        await page.screenshot(path=str(af_path), full_page=False)
        await page.screenshot(path=str(full_path), full_page=True)
        print(f"  saved screenshots to {screenshot_dir}")

        # extract meta
        meta = await page.evaluate("""
            () => ({
                title: document.title,
                description: document.querySelector('meta[name="description"]')?.content || null,
                ogTitle: document.querySelector('meta[property="og:title"]')?.content || null,
                ogDescription: document.querySelector('meta[property="og:description"]')?.content || null,
                ogImage: document.querySelector('meta[property="og:image"]')?.content || null,
                themeColor: document.querySelector('meta[name="theme-color"]')?.content || null,
                favicon: (document.querySelector('link[rel="icon"]')?.href ||
                          document.querySelector('link[rel="shortcut icon"]')?.href ||
                          null),
                appleTouchIcon: document.querySelector('link[rel="apple-touch-icon"]')?.href || null,
            })
        """)

        # extract logo (look for common patterns)
        logo_candidates = await page.evaluate("""
            () => {
                const out = [];
                document.querySelectorAll('header img, nav img, [class*="logo" i] img, [id*="logo" i] img').forEach(img => {
                    if (img.src && img.naturalWidth > 30) {
                        out.push({src: img.src, alt: img.alt, width: img.naturalWidth, height: img.naturalHeight});
                    }
                });
                return out.slice(0, 5);
            }
        """)

        # color frequency from computed styles
        colors = await page.evaluate("""
            () => {
                const counter = {};
                const all = document.querySelectorAll('*');
                let i = 0;
                for (const el of all) {
                    if (i++ > 2000) break;
                    const cs = window.getComputedStyle(el);
                    [cs.color, cs.backgroundColor, cs.borderColor].forEach(c => {
                        if (c && !c.includes('rgba(0, 0, 0, 0)') && c !== 'transparent') {
                            counter[c] = (counter[c] || 0) + 1;
                        }
                    });
                }
                return Object.entries(counter).sort((a,b) => b[1]-a[1]).slice(0, 20);
            }
        """)

        # font families
        fonts = await page.evaluate("""
            () => {
                const counter = {};
                const all = document.querySelectorAll('h1, h2, h3, h4, p, a, button, span, div');
                let i = 0;
                for (const el of all) {
                    if (i++ > 1500) break;
                    const ff = window.getComputedStyle(el).fontFamily;
                    if (ff) counter[ff] = (counter[ff] || 0) + 1;
                }
                return Object.entries(counter).sort((a,b) => b[1]-a[1]).slice(0, 10);
            }
        """)

        # copy extraction — h1/h2/h3 + buttons + nav + first paragraphs
        copy = await page.evaluate("""
            () => ({
                h1: Array.from(document.querySelectorAll('h1')).map(e => e.innerText.trim()).filter(Boolean).slice(0, 5),
                h2: Array.from(document.querySelectorAll('h2')).map(e => e.innerText.trim()).filter(Boolean).slice(0, 10),
                h3: Array.from(document.querySelectorAll('h3')).map(e => e.innerText.trim()).filter(Boolean).slice(0, 10),
                buttons: Array.from(document.querySelectorAll('button, a[class*="btn" i], a[class*="cta" i]')).map(e => e.innerText.trim()).filter(t => t && t.length < 60).slice(0, 15),
                nav: Array.from(document.querySelectorAll('header a, nav a')).map(e => e.innerText.trim()).filter(Boolean).slice(0, 12),
                firstParagraphs: Array.from(document.querySelectorAll('p')).map(e => e.innerText.trim()).filter(t => t.length > 20 && t.length < 400).slice(0, 6),
            })
        """)

        await browser.close()

    result = {
        "url": url,
        "scraped_at": __import__("datetime").datetime.now().isoformat(),
        "screenshots": {
            "above_fold": str(af_path),
            "full_page": str(full_path),
        },
        "meta": meta,
        "logo_candidates": logo_candidates,
        "top_colors": colors,
        "top_fonts": fonts,
        "copy": copy,
    }

    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"  scrape saved: {out_path}")
    print()
    print("Next: Claude reads this JSON + screenshots and produces DESIGN.md")
    print(f"  using template at ~/.claude/skills/claude-design/templates/design-md-template.md")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    url = sys.argv[1]
    out_path = Path(sys.argv[2])
    asyncio.run(scrape(url, out_path))


if __name__ == "__main__":
    main()
