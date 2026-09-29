# jc-agent-skills

A Claude Code and Codex plugin marketplace. One plugin so far, `jc-code`, holding vetted skills.

## Adding or changing a skill

Every skill change ships as a plugin version bump. Do all of these, in order:

1. **Bump both `plugins/jc-code/.claude-plugin/plugin.json` and
   `plugins/jc-code/.codex-plugin/plugin.json` to the same version.** New skill or new capability is a minor
   bump; a fix to an existing skill is a patch bump. Update the `description` too — it lists every
   skill, one clause each.
2. **Update the plugin descriptions in both manifests and `.claude-plugin/marketplace.json`.**
   The marketplace description is the short version of the same list. Keep the Codex
   `interface.longDescription` in sync. Both `.claude-plugin/marketplace.json` and
   `.agents/plugins/marketplace.json` must resolve `jc-code` to `./plugins/jc-code`; preserve
   the Codex catalog policy and category fields.
3. **Add a `## Change Log` entry in `README.md`.** Newest version first. See the format there.
4. **Update the Plugins table and the Layout block in `README.md`**, including the version number
   written into the Layout block.
5. **Add a `VETTING.md` entry.** Required for every skill, first-party ones included — it records
   what the skill executes and what it sends over the network.

Individual skills may carry their own `version` in their `SKILL.md` frontmatter. That is separate
from the plugin version and does not need to move in step with it. First-party skills here
deliberately carry no `version`; they track the plugin version alone. A vetted upstream copy keeps
whatever `version` upstream set, as `drawio` does.

Both formats share `plugins/jc-code/skills/`. For explicit-only skills, set Claude’s
`disable-model-invocation: true` and Codex’s `policy.allow_implicit_invocation: false` in
`agents/openai.yaml`. Validate both plugin formats and any changed skill before publishing.
