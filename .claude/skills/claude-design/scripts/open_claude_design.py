"""
Open claude.ai/design in browser + copy the 4-input prompt to clipboard.

Usage:
    python open_claude_design.py "<prompt text>"
    python open_claude_design.py --file <path-to-prompt-file>

Cross-platform: Windows (clip), macOS (pbcopy), Linux (xclip / xsel).
"""
import sys, os, subprocess
from pathlib import Path


def copy_to_clipboard(text: str) -> bool:
    """Returns True on success."""
    try:
        if sys.platform == "win32":
            p = subprocess.Popen("clip", stdin=subprocess.PIPE, shell=True)
            p.communicate(text.encode("utf-16le"))
            return p.returncode == 0
        elif sys.platform == "darwin":
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            p.communicate(text.encode("utf-8"))
            return p.returncode == 0
        else:
            for tool in (["xclip", "-selection", "clipboard"], ["xsel", "-bi"]):
                try:
                    p = subprocess.Popen(tool, stdin=subprocess.PIPE)
                    p.communicate(text.encode("utf-8"))
                    if p.returncode == 0:
                        return True
                except FileNotFoundError:
                    continue
    except Exception as e:
        print(f"clipboard error: {e}")
    return False


def open_url(url: str):
    if sys.platform == "win32":
        os.startfile(url)
    elif sys.platform == "darwin":
        subprocess.run(["open", url])
    else:
        subprocess.run(["xdg-open", url])


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print(__doc__)
            sys.exit(1)
        text = Path(sys.argv[2]).read_text(encoding="utf-8")
    else:
        text = sys.argv[1]

    ok = copy_to_clipboard(text)
    if ok:
        print(f"✓ prompt copied to clipboard ({len(text)} chars)")
    else:
        print("⚠ clipboard copy failed — paste manually:")
        print()
        print(text)
        print()

    print("opening claude.ai/design...")
    open_url("https://claude.ai/design")
    print()
    print("Your move:")
    print("  1. New Project → name it whatever fits")
    print("  2. Upload your DESIGN.md")
    print("  3. Ctrl+V to paste the prompt (already on clipboard)" if ok else "  3. Paste the prompt above manually")
    print("  4. Hit Generate")
    print("  5. Watch the build live — STOP IT if it goes the wrong way")


if __name__ == "__main__":
    main()
