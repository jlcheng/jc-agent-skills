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

| Plugin    | Skill    | Invocation        | Upstream                                                                        |
| --------- | -------- | ----------------- | ------------------------------------------------------------------------------- |
| `jc-code` | `drawio` | `/jc-code:drawio` | [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) (MIT) |

## Layout

```
.claude-plugin/marketplace.json      # marketplace: jc-agent-skills
plugins/jc-code/
├── .claude-plugin/plugin.json       # plugin: jc-code, version 1.0.0
└── skills/drawio/                   # skill: drawio (vetted upstream copy)
```

## Updating a vetted skill

1. Pull upstream and diff against the audited commit recorded in VETTING.md.
2. Re-review the diff (or re-run a full audit for large changes).
3. Copy the subtree in, update VETTING.md with the new commit, bump the plugin
   `version` in `plugin.json`.
