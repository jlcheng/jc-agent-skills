# Vetting Log

Every skill in this repo was security-reviewed before inclusion. This file records
what was audited, when, and from where, so future upstream updates can be diffed
against a known-good baseline.

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
