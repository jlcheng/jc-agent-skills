#!/usr/bin/env python3
"""Validate Mermaid diagrams by actually rendering them with mermaid-cli (mmdc).

Why render instead of eyeballing? Mermaid's grammar has footguns whose error
messages point at the *wrong line* (see references/pitfalls.md). The only
trustworthy check is to feed the diagram to the real parser. This wraps mmdc,
strips its noisy Puppeteer/Node stack traces, and reports a clean PASS/FAIL per
diagram.

Inputs (one or more):
  - a .mmd / .mermaid file            -> validated as a single diagram
  - a .md / .markdown file            -> every ```mermaid fenced block is
                                         extracted and validated independently,
                                         so you get all failures with block
                                         numbers, not just the first
  - "-"                               -> read one raw diagram from stdin

Exit status is non-zero if any diagram fails, so this is safe to gate on in a
script or a pre-delivery check.

mmdc resolution order:
  1. --mmdc PATH (explicit)
  2. an `mmdc` already on PATH
  3. `npx -y @mermaid-js/mermaid-cli` (downloads on first use, then cached)

Rendering happens in a temp dir and the output images are discarded — this tool
only cares whether the parse/render succeeds, never about the image.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

FENCE_RE = re.compile(
    r"^[ \t]*```[ \t]*mermaid[ \t]*\r?\n(.*?)^[ \t]*```[ \t]*$",
    re.DOTALL | re.MULTILINE | re.IGNORECASE,
)


def resolve_mmdc(explicit: str | None) -> list[str]:
    """Return the argv prefix used to invoke mmdc."""
    if explicit:
        return [explicit]
    found = shutil.which("mmdc")
    if found:
        return [found]
    if shutil.which("npx"):
        return ["npx", "-y", "@mermaid-js/mermaid-cli"]
    sys.exit(
        "error: could not find `mmdc` or `npx`. Install Node.js, then either\n"
        "  npm install -g @mermaid-js/mermaid-cli   (installs `mmdc`)\n"
        "or rely on npx (bundled with Node) to fetch it on demand."
    )


def clean_error(raw: str) -> str:
    """Keep the human-meaningful parse error, drop the JS stack trace."""
    lines = raw.splitlines()
    kept: list[str] = []
    for line in lines:
        stripped = line.strip()
        # The stack trace starts at the first `at ...` / `Parser.parseError (`
        # frame — everything from there on is noise for our purpose.
        if stripped.startswith("at ") or stripped.startswith("Parser.parseError ("):
            break
        # mmdc's progress preamble carries no diagnostic value.
        if stripped in ("", "Generating single mermaid chart"):
            if not kept:  # skip only leading blanks/preamble
                continue
        # The "Expecting <dozens of token names> got 'X'" line is overwhelmingly
        # noise; the actionable part is what was actually seen.
        if stripped.startswith("Expecting ") and len(stripped) > 80:
            got = re.search(r"got\s+('[^']*'|\S+)\s*$", stripped)
            line = f"Expecting a different token; got {got.group(1)}" if got else "Expecting a different token"
        kept.append(line.rstrip())
    text = "\n".join(kept).strip()
    return text or raw.strip()


def render_once(mmdc: list[str], src: str, config: str, workdir: str) -> tuple[bool, str]:
    """Render one diagram string. Return (ok, cleaned_error)."""
    in_path = os.path.join(workdir, "diagram.mmd")
    out_path = os.path.join(workdir, "out.svg")
    with open(in_path, "w", encoding="utf-8") as fh:
        fh.write(src)
    proc = subprocess.run(
        [*mmdc, "-p", config, "-i", in_path, "-o", out_path],
        capture_output=True,
        text=True,
    )
    combined = f"{proc.stdout}\n{proc.stderr}"
    # mmdc is unreliable about exit codes across versions (it has returned 0 on
    # parse errors), so treat "no output file" or a visible error as failure.
    produced = os.path.exists(out_path)
    looks_like_error = re.search(r"\berror\b", combined, re.IGNORECASE) is not None
    ok = produced and not looks_like_error
    return ok, clean_error(combined)


def extract_blocks(md_text: str) -> list[str]:
    return [m.group(1) for m in FENCE_RE.finditer(md_text)]


def units_for(path: str) -> list[tuple[str, str]]:
    """Return a list of (label, diagram_source) to validate for one input."""
    if path == "-":
        return [("stdin", sys.stdin.read())]
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    ext = os.path.splitext(path)[1].lower()
    if ext in (".md", ".markdown", ".mdx"):
        blocks = extract_blocks(text)
        if not blocks:
            return []
        return [(f"{path} [block {i}]", b) for i, b in enumerate(blocks, 1)]
    return [(path, text)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help=".mmd / .md file(s), or - for stdin")
    ap.add_argument("--mmdc", help="explicit path to the mmdc binary")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON results")
    ap.add_argument("-q", "--quiet", action="store_true", help="only print failures")
    args = ap.parse_args()

    mmdc = resolve_mmdc(args.mmdc)

    results = []
    with tempfile.TemporaryDirectory() as tmp:
        config = os.path.join(tmp, "puppeteer.json")
        # --no-sandbox is required when Chrome runs as root or inside many CI
        # sandboxes; it is harmless elsewhere.
        with open(config, "w", encoding="utf-8") as fh:
            json.dump({"args": ["--no-sandbox", "--disable-setuid-sandbox"]}, fh)

        units: list[tuple[str, str]] = []
        for path in args.inputs:
            found = units_for(path)
            if not found and path != "-":
                results.append({"label": path, "ok": None, "error": "no mermaid blocks found"})
            units.extend(found)

        for label, src in units:
            if not src.strip():
                results.append({"label": label, "ok": None, "error": "empty diagram"})
                continue
            workdir = tempfile.mkdtemp(dir=tmp)
            ok, err = render_once(mmdc, src, config, workdir)
            results.append({"label": label, "ok": ok, "error": "" if ok else err, "source": src})

    if args.json:
        print(json.dumps([{k: v for k, v in r.items() if k != "source"} for r in results], indent=2))
    else:
        for r in results:
            if r["ok"] is True:
                if not args.quiet:
                    print(f"PASS  {r['label']}")
            elif r["ok"] is None:
                print(f"SKIP  {r['label']}: {r['error']}")
            else:
                print(f"FAIL  {r['label']}")
                for line in r["error"].splitlines():
                    print(f"      {line}")

    failed = sum(1 for r in results if r["ok"] is False)
    if not args.quiet and not args.json:
        passed = sum(1 for r in results if r["ok"] is True)
        print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
