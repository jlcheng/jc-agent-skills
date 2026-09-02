---
name: claude-setup
description: >-
  Install John's preferred Claude Code machine setup: the status line script and
  the settings.json wiring that points at it. Run this on a new machine, or after
  a fresh `~/.claude`, to get the same status line everywhere. User-invoked only;
  it writes to the user's Claude Code config directory, so it never runs on its
  own initiative.
version: 1.0.0
disable-model-invocation: true
allowed-tools: Bash, Read
---

# claude-setup

Applies the owner's preferred Claude Code configuration to this machine. Right
now that is one component, the status line. More can be added later; each one
gets a section below and a script in `scripts/`.

This skill writes to the user's Claude Code config directory
(`$CLAUDE_CONFIG_DIR`, default `~/.claude`), which is personal configuration
rather than project code. Everything it touches is backed up first, and it is
safe to run repeatedly.

## Component: status line

The status line is a shell script that Claude Code runs on every refresh. Its
output becomes the line under the prompt. Claude Code pipes a JSON payload to it
on stdin, and the bundled script builds the line from that plus one or two quick
git calls.

Result looks like:

```
statusline work | Opus 5 (1M context) | jc-agent-skills@main | 42%
```

Four items, in this order. Each one is a block in the script with a comment
saying what it shows and what color it uses. An item with nothing to show drops
out and the separators close up.

| Item        | Shows                                                                                                                       | Color                                       |
| ----------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| session     | the name from `/rename`, else the first 8 of the session id                                                                 | bold                                        |
| model       | the model display name                                                                                                      | dim                                         |
| repo@branch | repo name from the origin remote, else the top-level directory name; short commit instead of a branch when HEAD is detached | repo default, branch cyan                   |
| context     | percent of the context window used                                                                                          | green below 60, yellow from 60, red from 85 |

Outside a git repository the repo item disappears. Before the first API response
of a session the context item disappears.

### Install it

```bash
bash scripts/install-statusline.sh --dry-run   # show what would change
bash scripts/install-statusline.sh             # do it
```

The installer:

1. Checks `jq` is on `PATH`, and stops with an explanation if not. The status
   line script parses its JSON input with `jq`, so without it the bar renders
   empty.
2. Copies `assets/statusline-command.sh` to `$CLAUDE_CONFIG_DIR` and makes it
   executable. An existing copy is backed up to `statusline-command.sh.bak-<timestamp>`
   first.
3. Points `settings.json` at it, backing that file up the same way and leaving
   every other setting untouched.
4. Prints a preview by feeding the installed script a sample payload, so a
   broken install shows up immediately instead of at the next session start.

Exit codes: `0` installed or already current, `2` a precondition failed, `3` the
user already has a different status line configured.

### If it exits 3

The user has a status line pointing at some other script. Do not overwrite it
silently. Show them the existing command that the installer printed, and ask
whether to replace it. Only if they say yes:

```bash
bash scripts/install-statusline.sh --force
```

`settings.json` is backed up before the replacement either way.

### After installing

Claude Code re-reads the script on every refresh, so the change is visible within
a second or two. No restart. Ask the user how it looks rather than guessing, and
tell them where the backups (if any) were written.

If they want the line to show something different, edit `assets/statusline-command.sh` in this skill and re-run the
installer, so the plugin stays the source of truth rather than the copy in
`~/.claude`.

### Changing what the line shows

Add or edit one block in `assets/statusline-command.sh`. Each block ends in a
call to `add <color> <text>`, and empty text is skipped, so an item that has
nothing to say costs nothing.

The payload on stdin carries more than the script uses, including
`.context_window.remaining_percentage`, `.cost.total_cost_usd`,
`.cost.total_lines_added`, `.output_style.name`, `.workspace.project_dir`,
`.workspace.git_worktree`, `.effort.level`, `.rate_limits.five_hour`, and
`.exceeds_200k_tokens`. Reach for those before computing anything by hand.

Two things to know before editing the jq call that reads the payload:

- The fields are joined with the ASCII unit separator, not a tab. `read`
  collapses runs of whitespace, so a tab would make one empty field silently
  shift every field after it.
- `.session_name`, `.workspace.repo`, and `.context_window.used_percentage` are
  all optional. Give every field a `//` fallback.

Whatever the script does, it does on every refresh, so keep it fast: no network
calls, no expensive git work.
