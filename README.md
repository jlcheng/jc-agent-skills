# jc-agent-skills

A Claude Code plugin marketplace hosting agent skills I have vetted and am comfortable publishing.
See [VETTING.md](VETTING.md) for the audit record of each skill.

## Install

```
/plugin marketplace add jcheng/jc-agent-skills
/plugin install jc-code@jc-agent-skills
```

While developing locally:

```
/plugin marketplace add ~/privprjs/jc-agent-skills
```

## Plugins

| Plugin | Skill | Invocation | Origin |
| -- | -- | -- | -- |
| `jc-code` | `drawio` | `/jc-code:drawio` | [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) (MIT) |
| `jc-code` | `mermaid` | `/jc-code:mermaid` | First-party (authored in this repo) |
| `jc-code` | `guided-review` | `/jc-code:guided-review` | First-party (authored in this repo) |
| `jc-code` | `claude-setup` | `/jc-code:claude-setup` | First-party (authored in this repo) |

## Layout

```
.claude-plugin/marketplace.json      # marketplace: jc-agent-skills
plugins/jc-code/
├── .claude-plugin/plugin.json       # plugin: jc-code, version 1.3.1
├── skills/drawio/                   # skill: drawio (vetted upstream copy)
├── skills/mermaid/                  # skill: mermaid (first-party)
├── skills/guided-review/            # skill: guided-review (first-party)
└── skills/claude-setup/             # skill: claude-setup (first-party)
```

Some skills here are vetted copies of other people's work (see [VETTING.md](VETTING.md)); `mermaid`,
`guided-review`, and `claude-setup` were authored in this repo.

## Updating a vetted skill

1. Pull upstream and diff against the audited commit recorded in VETTING.md.
2. Re-review the diff (or re-run a full audit for large changes).
3. Copy the subtree in, update VETTING.md with the new commit, bump the plugin `version` in
   `plugin.json`.

## Change Log

Versions are `jc-code` plugin versions, from `plugins/jc-code/.claude-plugin/plugin.json`. Newest
first. One bullet per user-visible change: what changed, and why it matters to someone using the
skill. Skip anything invisible from outside the repo.

### 1.3.1 — 2026-09-02

- The `claude-setup` status line now shows raw token counts next to the context percentage, for
  example `12% (118k/1M)`. The counts are the same numbers the percentage is computed from, so
  they cannot disagree with it.

### 1.3.0 — 2026-09-02

- Added `claude-setup`: installs the owner's preferred Claude Code machine setup. Today that is the
  status line, a script showing the session name, the model, the repo and branch, and how much of
  the context window is used. Run `/jc-code:claude-setup` on a new machine instead of rebuilding the
  status line from scratch.

### 1.2.0 — 2026-08-29

- Added `guided-review`: an interactive, seven-phase code review. It wraps the built-in
  `code-review` skill, then puts every Finding in front of a fresh adversarial verifier to strip
  false alarms before anything gets fixed. Asks before each phase; declining skips just that phase.
- Keeps its state in a gitignored `.guided-review/` directory, so a review survives a long session
  and can be resumed.

### 1.1.0 — 2026-07-20

- Added `mermaid`: authors and repairs Mermaid diagrams, and validates them by actually rendering
  with mermaid-cli, so a diagram that will not parse never reaches you.
- `drawio` image exports (PNG/SVG/PDF/JPG) are now strictly opt-in. The default deliverable is the
  `.drawio` file alone.
- `drawio` still runs its vision self-check by default, against a temporary render that is deleted
  straight after the check.

### 1.0.0 — 2026-07-02

- First release. Marketplace plus the `jc-code` plugin, carrying a vetted copy of `drawio` for
  generating `.drawio` diagrams and exporting them through the draw.io desktop CLI.
