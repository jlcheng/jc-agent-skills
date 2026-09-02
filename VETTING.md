# Vetting Log

Every skill in this repo was security-reviewed before inclusion. This file records
what was audited, when, and from where, so future upstream updates can be diffed
against a known-good baseline. First-party skills authored in this repo are
recorded here too, documenting their execution and network behavior.

## jc-code:claude-setup

- **Origin:** First-party — authored in this repo, not copied from upstream.
- **Added:** 2026-09-02.
- **What it does:** Installs the owner's preferred Claude Code machine setup. Ships
  two files: `assets/statusline-command.sh` (the status line itself) and
  `scripts/install-statusline.sh` (the installer).

### Behavior worth remembering

- **It writes to the user's Claude Code config directory, not the project.** The
  installer copies the status line script into `$CLAUDE_CONFIG_DIR` (default
  `~/.claude`) and sets the `statusLine` key in `settings.json`. Both files are
  copied to a `.bak-<timestamp>` sibling before being written. It touches nothing
  else in `settings.json`, and refuses to proceed if that file will not parse as
  JSON. Honors `CLAUDE_CONFIG_DIR`, which is what makes it testable against a
  throwaway directory.
- **It will not silently replace someone else's status line.** If `settings.json`
  already points at a different script, the installer prints that command and
  exits 3. Replacing it requires an explicit `--force`, and SKILL.md tells the
  agent to ask the user first.
- **User-invoked only.** `disable-model-invocation: true` in the frontmatter, so
  the model cannot decide on its own to run something that rewrites config.
  `allowed-tools` is limited to Bash and Read.
- **No network.** Neither script fetches anything. The installed status line runs
  on every refresh, and the only thing it shells out to is `git` in the current
  directory, always with `--no-optional-locks`: `rev-parse --show-toplevel`, then
  `branch --show-current`, and `rev-parse --short HEAD` only when HEAD is
  detached. Roughly 50 milliseconds per render, measured.
- **Payload values are never evaluated.** The session name, model name, and repo
  name come from Claude Code's JSON payload and are only ever concatenated into
  the output string, never used as a command or a path.
- **Dependency:** `jq`, used by both the status line and the installer's
  `settings.json` edit. The installer checks for it up front and exits 2 with an
  explanation rather than leaving a broken status bar behind.
- **Script hygiene:** `set -euo pipefail`; no `eval`; no `curl`/`wget`; JSON is
  edited through `jq` with the new value passed as `--arg`, never string
  interpolation, and written to a temp file that is moved into place.

### Verdict

Safe. Personal-configuration installer with a small, auditable footprint. The
thing to be aware of is that it is the one skill here that writes outside the
project, into `~/.claude`, by design.

## jc-code:mermaid

- **Origin:** First-party — authored in this repo, not copied from upstream.
- **Added:** 2026-07-20.
- **What it does:** Guides authoring/repair of Mermaid diagrams and validates
  them by rendering with [mermaid-cli](https://github.com/mermaid-js/mermaid-cli)
  (`mmdc`). Ships one script, `scripts/validate_mermaid.py`.

### Behavior worth remembering

- **Network egress + third-party execution on validation:** if `mmdc` is not
  already on `PATH`, the script invokes `npx -y @mermaid-js/mermaid-cli`, which
  downloads mermaid-cli (and its dependency tree, including a Chromium via
  Puppeteer) from npm on first use, then runs it. Rendering launches headless
  Chrome. This is the upstream tool the skill is built around, run only when the
  user validates a diagram — but it is real network + code execution, so keep it
  behind permission prompts in locked-down environments. Pre-installing
  `@mermaid-js/mermaid-cli` avoids the on-demand npm fetch.
- **Chrome flags:** the script writes a Puppeteer config enabling `--no-sandbox`
  / `--disable-setuid-sandbox` (needed when Chrome runs as root or in CI). This
  lowers the browser sandbox for the render subprocess only; the diagrams being
  rendered are local text the user authored.
- **Script hygiene:** stdlib only (`argparse`, `subprocess`, `tempfile`, `re`,
  `json`); no `eval`/`exec`/`pickle`; renders into a temp dir and discards the
  image; writes nothing outside temp. Diagram content is passed to mmdc via a
  temp file, never interpolated into a shell string.

### Verdict

Safe. Diagram-authoring aid whose only external action is running the official
mermaid-cli to validate the user's own diagrams. The one thing to be aware of is
the on-demand npm download + headless-Chrome launch on first validation.

## jc-code:guided-review

- **Origin:** First-party — authored in this repo, not copied from upstream.
- **Added:** 2026-08-29.
- **What it does:** Orchestrates an interactive, seven-phase code review on top of the
  built-in `code-review` skill. Ships no scripts. Prose only.

### Behavior worth remembering

- **No scripts, no network:** the skill is instructions only. Its network and
  execution footprint is whatever the built-in `code-review` skill and the agent's
  own tools do.
- **It edits the working tree.** Phases 3 and 5 apply fixes and Phase 6 removes
  source-code comments. Every edit is announced, and Phase 6 shows removals before
  applying them, but this is a skill that changes your code.
- **It never touches GitHub.** The skill forbids passing `--fix` to the built-in
  skill, and Phase 6 is explicitly scoped to source-code comments so it cannot be
  misread as deleting pull-request review comments.
- **It writes to `.guided-review/` in the repo** and asks for that path to be added
  to `.gitignore` in Phase 1, so an unfinished review does not land in a commit.

### Verdict

Safe. Prose-only orchestration skill. The thing to be aware of is that it modifies
source files by design, so run it where you can read the diff.

## jc-code:drawio

- **Upstream:** https://github.com/Agents365-ai/drawio-skill
- **Audited upstream commit:** `48452fdb08790e2981232762e080c13c45cc5fd3` (v1.19.0)
- **Vetted:** 2026-07-02, via manual review plus an independent subagent audit
- **Copied subtree:** `skills/drawio-skill/` → `plugins/jc-code/skills/drawio/`
- **Local modifications:** frontmatter `name: drawio-skill` → `name: drawio`
  (invocation naming only); upstream `LICENSE` (MIT) copied into the skill directory.
  2026-07-12: behavioral patch to `SKILL.md` — image exports (PNG/SVG/PDF/JPG) made
  strictly opt-in ("Default stop" rule): the default deliverable is the `.drawio` file
  only, and workflow steps 4–7 (draft export, vision self-check, PNG review loop,
  final export) run only when the user explicitly requests a rendered image; the
  vision self-check still runs by default against an ephemeral scratchpad render
  deleted after the check (owner preference — auto-generated images were never
  used). No script changes. Everything
  else is byte-identical to the audited commit; on upstream bumps, re-apply this
  patch after the diff audit.

### Verdict

Safe with caveats. No malicious code, no prompt injection, no obfuscation.

Findings worth remembering:

- **Network egress by design:** `scripts/aiicons.py` fetches brand SVGs from
  `unpkg.com` (version-pinned `@lobehub/icons-static-svg@1.91.0`) and
  `cdn.simpleicons.org`. With `--embed` it inlines fetched SVG unsanitized;
  without it, exported diagrams reference the CDN at render time.
- **Browser fallback shares diagram content:** `scripts/encode_drawio_url.py`
  packs full diagram XML into a diagrams.net URL fragment — client-side only,
  but the diagrams.net web app decodes it. Avoid for confidential diagrams.
- **The skill instructs the agent to install software** (brew/apt drawio +
  graphviz, and a third-party Docker image `tomkludy/drawio-renderer` as a
  last-resort fallback). Keep installs behind permission prompts; skip the
  Docker fallback.
- Scripts are clean: `yaml.safe_load`, `ast.parse`, fixed-argv subprocess
  (Graphviz `dot`/`tred` only), no eval/exec/pickle, writes only to `-o` paths
  and `~/.drawio-skill/styles/`.
- Upstream previously shipped a self-update mechanism in SKILL.md (since
  removed). **Re-audit the diff on every upstream version bump** before
  copying it in: `git diff 48452fd..<new> -- skills/drawio-skill/`.
