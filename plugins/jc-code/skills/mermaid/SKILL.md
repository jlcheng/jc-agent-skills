---
name: mermaid
description: >-
  Author and repair Mermaid diagrams (flowchart, sequence, class, state, ER,
  gantt, pie, mindmap) so they actually render instead of failing with a parse
  error. Use whenever the user asks for a Mermaid diagram, pastes ```mermaid that
  won't render, hits a Mermaid "Parse error on line N", or is writing Markdown/
  docs/READMEs that embed Mermaid. Also use proactively when you're about to hand
  the user a Mermaid diagram in any response — validate it with mermaid-cli first
  so you never ship a diagram that breaks. Especially valuable for sequence
  diagrams with rich message text (auth flows, API call chains), where a stray
  semicolon or unescaped character silently corrupts the parse.
---

# Mermaid

LLMs write Mermaid that looks right but fails to render — a `;` in a sequence
message, an unquoted parenthesis in a flowchart label, a `<int>` where Mermaid
wants `~int~`. The failure is worse than a typo because **the error message
frequently points at the wrong line**, so guessing wastes time. This skill's
core discipline is simple: *don't reason about whether Mermaid will accept your
diagram — render it and find out.*

## Workflow

1. **Write** the diagram. Keep the common footguns (below) in mind so the first
   draft is usually clean.

2. **Validate** it by rendering with mermaid-cli, using the bundled script:

   ````bash
   python3 scripts/validate_mermaid.py path/to/diagram.mmd
   # or a whole Markdown doc — every ```mermaid block is checked independently:
   python3 scripts/validate_mermaid.py README.md
   # or pipe a diagram you just wrote, without touching disk:
   printf '%s' "$DIAGRAM" | python3 scripts/validate_mermaid.py -
   ````

   It prints `PASS`/`FAIL` per diagram and, on failure, the cleaned parse error.
   It exits non-zero if anything fails, so you can gate on it. First run may take
   a few seconds while `npx` fetches mermaid-cli (then it's cached).

3. **Fix and re-validate** until everything passes. If the reported line looks
   innocent, the real defect is usually a line or two *above* it (see below).

4. **Deliver** only diagrams that have passed. When you validated, say so briefly
   ("rendered clean with mermaid-cli") so the user knows it's not a guess.

Do this even when a diagram looks obviously fine — the whole point is that
"looks fine" and "renders" diverge in Mermaid, and validation is cheap.

## The footguns worth memorizing

Most special characters are actually fine in modern Mermaid — parentheses,
colons, commas, slashes, `%`, `&`, em-dashes, Unicode arrows all render in
ordinary text. **Do not over-escape.** These few are the real traps:

- **`;` in a sequence-diagram message or note is a statement separator.** It
  splits your sentence mid-message and produces a parse error that often blames
  the wrong line. This is the single most common LLM Mermaid bug. Never write a
  raw `;` in sequence text — use a comma, an em-dash (`—`), or a `<br/>` break:

  ```
  A-->>B: login form; user authenticates      # BREAKS (misleading error line)
  A-->>B: login form, user authenticates       # fine
  A-->>B: login form<br/>user authenticates     # fine, and reads better
  ```

- **Punctuation in a flowchart/state/class/ER label → wrap the label in double
  quotes.** Quoting neutralizes `()`, `;`, `:`, `%`, etc.:

  ```
  A["Call foo(bar); retry at 50%"] --> B
  A -->|"yes; really"| B
  ```

- **Characters you can't type literally → HTML entities:** `#quot;` for `"`,
  `#35;` for `#`, `#nbsp;` for a non-breaking space. Multi-line text → `<br/>`.

- **Class-diagram generics use tildes, not angle brackets:** `List~int~`, not
  `List<int>`.

For the full, render-verified catalog — including exactly which characters are
safe unescaped (so you can stop over-escaping) and how to chase a misleading
error line — read `references/pitfalls.md`.

## Requirements

Validation shells out to [mermaid-cli](https://github.com/mermaid-js/mermaid-cli)
(`mmdc`), which needs Node.js. The script finds `mmdc` on `PATH`, else falls back
to `npx -y @mermaid-js/mermaid-cli` (downloaded on first use, then cached). It
renders into a temp directory and discards the image — it only reports whether
the diagram parses. First use of `npx` fetches the package from npm; if the
environment is offline or Node is absent, the script says so clearly.
