#!/usr/bin/env python3
"""
token-check — count Claude tokens + estimate API cost for any text/file.

Modes:
  - DEFAULT: tiktoken (GPT-4 cl100k_base) approximation. ~10% off Claude.
    No API key needed, runs offline after first install.
  - EXACT: if ANTHROPIC_API_KEY is set, calls Anthropic's free count_tokens
    endpoint for exact Claude tokenization.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


MODELS = [
    # (display_name, model_id, $/M_input, $/M_output)
    ("Opus 4.7",   "claude-opus-4-7",          15.00, 75.00),
    ("Sonnet 4.6", "claude-sonnet-4-6",         3.00, 15.00),
    ("Haiku 4.5",  "claude-haiku-4-5-20251001", 1.00,  5.00),
]


def pip_install(pkg: str):
    print(f"[token-check] {pkg} missing, installing...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pkg])
    print(f"[token-check] installed {pkg}.", file=sys.stderr)


def load_input(args) -> tuple[str, str]:
    """Return (label, text) for the input source."""
    if args.text:
        return ("inline text", args.text)
    if args.file:
        p = Path(args.file).expanduser().resolve()
        if not p.exists():
            sys.exit(f"[token-check] file not found: {p}")
        return (str(p.name), p.read_text(encoding="utf-8", errors="replace"))
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        if not data.strip():
            sys.exit("[token-check] empty stdin, nothing to count")
        return ("stdin", data)
    sys.exit("[token-check] no input. Use --text \"...\", --file PATH, or pipe via stdin.")


def count_via_tiktoken(text: str) -> int:
    try:
        import tiktoken
    except ImportError:
        pip_install("tiktoken")
        import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def count_via_anthropic(text: str, api_key: str) -> dict[str, int]:
    """Return {model_id: token_count}. Calls API once per model."""
    try:
        import anthropic
    except ImportError:
        pip_install("anthropic")
        import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    out = {}
    for _, model_id, _, _ in MODELS:
        resp = client.messages.count_tokens(
            model=model_id,
            messages=[{"role": "user", "content": text}],
        )
        out[model_id] = resp.input_tokens
    return out


def fmt_money(x: float) -> str:
    return f"${x:,.5f}" if x < 1 else f"${x:,.2f}"


def main():
    parser = argparse.ArgumentParser(description="Count Claude tokens + estimate API cost.")
    parser.add_argument("--text", help="inline text to count")
    parser.add_argument("--file", help="path to a file whose contents to count")
    parser.add_argument(
        "--output-tokens",
        type=int,
        default=500,
        help="expected output token count for cost projection (default 500)",
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="force exact (Anthropic API) mode. Requires ANTHROPIC_API_KEY.",
    )
    parser.add_argument(
        "--approx",
        action="store_true",
        help="force approximate (tiktoken) mode even if API key is set.",
    )
    args = parser.parse_args()

    label, text = load_input(args)
    char_count = len(text)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    use_exact = (api_key and not args.approx) or args.exact
    if args.exact and not api_key:
        sys.exit("[token-check] --exact requires ANTHROPIC_API_KEY in env.")

    print()
    print("=== Token check ===")
    print(f"Input:  {label} ({char_count:,} chars)")
    print(f"Output projection: {args.output_tokens:,} tokens")
    if use_exact:
        print("Mode:   EXACT (Anthropic count_tokens API)")
        per_model = count_via_anthropic(text, api_key)
    else:
        print("Mode:   APPROXIMATE (tiktoken cl100k_base - within ~10% of Claude)")
        approx = count_via_tiktoken(text)
        per_model = {m[1]: approx for m in MODELS}  # same estimate across models
    print()

    header = f"{'Model':<14}{'In tokens':>12}{'In cost':>14}{'Est out cost':>18}{'Total':>14}"
    print(header)
    print("-" * len(header))

    for display_name, model_id, in_price, out_price in MODELS:
        n_in = per_model[model_id]
        in_cost = (n_in / 1_000_000) * in_price
        out_cost = (args.output_tokens / 1_000_000) * out_price
        total = in_cost + out_cost
        print(
            f"{display_name:<14}{n_in:>12,}{fmt_money(in_cost):>14}{fmt_money(out_cost):>18}{fmt_money(total):>14}"
        )

    print()
    if use_exact:
        print("Source: Anthropic count_tokens API (free, exact)")
    else:
        print("Source: tiktoken cl100k_base (GPT-4 tokenizer, ~10% approximation for Claude)")
        print("        For exact counts: set ANTHROPIC_API_KEY (console.anthropic.com -> API Keys)")


if __name__ == "__main__":
    main()
