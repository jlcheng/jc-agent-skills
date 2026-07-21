# jc-agent-skills

A Claude Code plugin marketplace hosting agent skills I have vetted and am
comfortable publishing. See [VETTING.md](VETTING.md) for the audit record of
each skill.

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

| Plugin    | Skill     | Invocation         | Origin                                                                          |
| --------- | --------- | ------------------ | ------------------------------------------------------------------------------- |
| `jc-code` | `drawio`  | `/jc-code:drawio`  | [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) (MIT) |
| `jc-code` | `mermaid` | `/jc-code:mermaid` | First-party (authored in this repo)                                             |

## Layout

```
.claude-plugin/marketplace.json      # marketplace: jc-agent-skills
plugins/jc-code/
├── .claude-plugin/plugin.json       # plugin: jc-code, version 1.1.0
├── skills/drawio/                   # skill: drawio (vetted upstream copy)
└── skills/mermaid/                  # skill: mermaid (first-party)
```

Most skills here are vetted copies of other people's work (see
[VETTING.md](VETTING.md)); `mermaid` is the first one authored in this repo.

## Updating a vetted skill

1. Pull upstream and diff against the audited commit recorded in VETTING.md.
2. Re-review the diff (or re-run a full audit for large changes).
3. Copy the subtree in, update VETTING.md with the new commit, bump the plugin
   `version` in `plugin.json`.
