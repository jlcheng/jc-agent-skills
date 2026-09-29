# jc-agent-skills

A Claude Code and Codex plugin marketplace hosting agent skills I have vetted and am comfortable
publishing. See [VETTING.md](VETTING.md) for the audit record of each skill.

## Install

Claude Code:

```
/plugin marketplace add jlcheng/jc-agent-skills
/plugin install jc-code@jc-agent-skills
```

Codex:

```sh
codex plugin marketplace add jlcheng/jc-agent-skills
codex plugin add jc-code@jc-agent-skills
```

Invoke skills with `/jc-code:<skill>` in Claude Code or `$jc-code:<skill>` in Codex.

While developing locally in Claude Code:

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
| `jc-code` | `grilling` | `/jc-code:grilling` | First-party (authored in this repo) |
| `jc-code` | `grill-with-docs` | `/jc-code:grill-with-docs` | First-party (authored in this repo) |
| `jc-code` | `domain-modeling` | `/jc-code:domain-modeling` | First-party (authored in this repo) |

## Layout

```
.claude-plugin/marketplace.json      # Claude marketplace: jc-agent-skills
.agents/plugins/marketplace.json     # Codex marketplace: jc-agent-skills
plugins/jc-code/
├── .claude-plugin/plugin.json       # plugin: jc-code, version 1.7.3
├── .codex-plugin/plugin.json        # same plugin, version 1.7.3
└── skills/${skill_name}/            # One directory per skill
```

Some skills here are vetted copies of other people's work (see [VETTING.md](VETTING.md)). Other
skills: `mermaid`, `guided-review`, `claude-setup`, `grilling`, `grill-with-docs`, and
`domain-modeling` were authored in this repo.

## Updating a vetted skill

1. Pull upstream and diff against the audited commit recorded in VETTING.md.
2. Re-review the diff (or re-run a full audit for large changes).
3. Copy the subtree in, update VETTING.md with the new commit, bump the plugin `version` in both
   plugin manifests.

## Validate the repository

Run the static checks before publishing:

```sh
uv run scripts/validate_repo.py
```

The script checks matching Claude/Codex manifests, marketplace paths, skill metadata, explicit-only
invocation policies, and README/VETTING inventories. Unknown metadata fields are accepted so skills
can carry settings for other agents.

Errors include the relevant file path and produce a nonzero exit status. The validator does not
modify files or execute skills. It checks this checkout by default, even when invoked from another
directory; use `--root /path/to/checkout` to check a different copy. These checks establish
consistency, not the quality or safety of a skill's instructions.

Run the validator's tests with:

```sh
uv run --with 'PyYAML>=6,<7' python -m unittest discover -s tests
```

## Change Log

Versions are `jc-code` plugin versions, shared by the Claude and Codex manifests. Newest first. One
bullet per user-visible change: what changed, and why it matters to someone using the skill. Skip
anything invisible from outside the repo.

### 1.7.3 — 2026-09-28

- Added Codex’s explicit-only activation policy for `claude-setup`, matching its Claude setting.

### 1.7.2 — 2026-09-28

- Enforced explicit-only activation for `guided-review` through both Claude and Codex settings.

### 1.7.1 — 2026-09-28

- Removed the `ping` activation-check skill and its Codex default prompt.

### 1.7.0 — 2026-09-28

- Added `grilling`: stress-tests plans and ideas through rounds of questions.

- Added `grill-with-docs`: combines grilling with domain modeling to capture glossary terms and
  architectural decisions during the discussion.

- Added `domain-modeling`: helps maintain a project glossary and record architectural decisions,
  with format guides in the skill's `references/` directory.

### 1.6.1 — 2026-09-25

- Changed only the inert `ping` evaluation marker to distinguish installed release B from A during
  manager update tests. Its explicit-only policy and exact `pong` response are unchanged.

### 1.6.0 — 2026-09-25

- Added Codex packaging using the same skills tree and `jc-code` namespace as Claude Code.
- Added explicit-only `ping`, which replies with `pong`, for checking installed skill activation.

### 1.5.0 — 2026-09-24

- `guided-review` now starts only when you explicitly invoke it or ask to start or continue a guided
  review. The model no longer infers activation from review files or review discussion.

### 1.4.1 — 2026-09-06

- The `guided-review` testing guide no longer tells you to paste one specific machine's absolute
  paths. It uses a `<repo-root>` placeholder you fill in with your own clone.
- The Review contract now cites the published post the vocabulary came from,
  ["Throwing Away What You Built"](https://www.jcheng.org/post/throwing-away-what-you-built/),
  instead of an unpublished journal file nobody else can open.

### 1.4.0 — 2026-09-06

- Replaced the seven-phase `guided-review` workflow with a guided examination of an existing Review
  JSON: opening and closing tables, detailed Finding cards, explicit machine disagreement, and saved
  human judgments. Reviews persist under `~/.jc-guided-review/<repo-name>/`.
- Removed automatic review generation, fix phases, and source-comment trimming from this skill.
  Added three fictional Review inputs for trying the interaction in separate sessions.

### 1.3.1 — 2026-09-02

- The `claude-setup` status line now shows raw token counts next to the context percentage, for
  example `12% (118k/1M)`. The counts are the same numbers the percentage is computed from, so they
  cannot disagree with it.

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
