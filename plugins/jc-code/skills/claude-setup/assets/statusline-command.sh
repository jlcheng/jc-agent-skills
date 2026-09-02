#!/usr/bin/env bash
# Claude Code status line.
# jc-code:claude-setup statusline v2, installed by scripts/install-statusline.sh
#
# Claude Code pipes a JSON payload to this script on every refresh and prints
# whatever comes back on stdout.
#
# Shell has no structs, so each item gets its own block below, in the order it
# is printed. Every block says what it shows and what color it uses. An item
# with nothing to show drops out, and the separators close up around it.
#
#   session | model | repo@branch | context
#
# This runs on every refresh, so it stays cheap: one jq call, and git only when
# there is a working directory to ask about. No network, ever.

input=$(cat)

# --- colors -------------------------------------------------------------------

BOLD=$'\033[1m'
DIM=$'\033[2m'
CYAN=$'\033[36m'
GREEN=$'\033[32m'
YELLOW=$'\033[33m'
RED=$'\033[31m'
RESET=$'\033[0m'

# --- payload ------------------------------------------------------------------
# One jq call for everything. Missing fields come back empty. The separator is
# the ASCII unit separator rather than a tab: read collapses runs of whitespace,
# which would silently shift every field after an empty one.

IFS=$'\037' read -r cwd session model repo pct <<EOF
$(printf '%s' "$input" | jq -r '[
  (.workspace.current_dir // .cwd // ""),
  (.session_name // ((.session_id // "")[0:8])),
  (.model.display_name // ""),
  (.workspace.repo.name // ""),
  (.context_window.used_percentage | if . == null then "" else (round | tostring) end)
] | join("\u001f")' 2>/dev/null)
EOF

# --- items --------------------------------------------------------------------
# add <color> <text> appends one item. Empty text is skipped.

items=()
add() {
  [ -n "$2" ] || return 0
  if [ -n "$1" ]; then
    items+=("$1$2$RESET")
  else
    items+=("$2")
  fi
}

# Item: session
# Shows the session name set with /rename, or the first 8 characters of the
# session id when the session has not been named.
# Color: bold.
add "$BOLD" "$session"

# Item: model
# Shows the model's display name, for example "Opus 5 (1M context)".
# Color: dim. It changes rarely, so it gives up prominence to the repo.
add "$DIM" "$model"

# Item: repo and branch
# Shows "repo@branch". The repo name comes from the origin remote when there is
# one, otherwise from the name of the repository's top-level directory. A
# detached HEAD shows the short commit in place of a branch. Outside a git
# repository the whole item drops out.
# Color: repo terminal default, branch cyan. This is the one item that colors
# its own two halves, so it is added with no outer color.
branch=""
if [ -n "$cwd" ]; then
  toplevel=$(git -C "$cwd" --no-optional-locks rev-parse --show-toplevel 2>/dev/null)
  if [ -n "$toplevel" ]; then
    [ -n "$repo" ] || repo=$(basename "$toplevel")
    branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)
    [ -n "$branch" ] || branch=$(git -C "$cwd" --no-optional-locks rev-parse --short HEAD 2>/dev/null)
  else
    # The payload can name a repository we are not currently standing in.
    repo=""
  fi
fi

if [ -n "$repo" ] && [ -n "$branch" ]; then
  add "" "${repo}@${CYAN}${branch}${RESET}"
else
  add "" "$repo"
fi

# Item: context usage
# Shows how much of the context window is used, for example "42%". Absent until
# the first API response of the session.
# Color: green below 60, yellow from 60, red from 85.
if [[ "$pct" =~ ^[0-9]+$ ]]; then
  if [ "$pct" -ge 85 ]; then
    pct_color=$RED
  elif [ "$pct" -ge 60 ]; then
    pct_color=$YELLOW
  else
    pct_color=$GREEN
  fi
  add "$pct_color" "${pct}%"
fi

# --- render -------------------------------------------------------------------
# Items joined by a dim pipe.

line=""
for item in "${items[@]}"; do
  if [ -z "$line" ]; then
    line="$item"
  else
    line="${line} ${DIM}|${RESET} ${item}"
  fi
done

printf '%s' "$line"
