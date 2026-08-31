# jc-agent-skills

A Claude Code plugin marketplace. One plugin so far, `jc-code`, holding vetted skills.

## Adding or changing a skill

Every skill change ships as a plugin version bump. Do all of these, in order:

1. **Bump `plugins/jc-code/.claude-plugin/plugin.json`.** New skill or new capability is a minor
   bump; a fix to an existing skill is a patch bump. Update the `description` too — it lists every
   skill, one clause each.
2. **Update `.claude-plugin/marketplace.json`.** The `jc-code` `description` there is the short
   version of the same list.
3. **Add a `## Change Log` entry in `README.md`.** Newest version first. See the format there.
4. **Update the Plugins table and the Layout block in `README.md`**, including the version number
   written into the Layout block.
5. **Add a `VETTING.md` entry.** Required for every skill, first-party ones included — it records
   what the skill executes and what it sends over the network.

Individual skills may carry their own `version` in their `SKILL.md` frontmatter. That is separate
from the plugin version and does not need to move in step with it.
