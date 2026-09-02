#!/usr/bin/env bash
# Install the bundled status line script into the user's Claude Code config and
# point settings.json at it.
#
#   install-statusline.sh [--dry-run] [--force]
#
# Exit codes:
#   0  installed, or already up to date
#   2  precondition failed (missing jq, unreadable settings.json, missing asset)
#   3  settings.json already has a statusLine pointing somewhere else; needs --force
set -euo pipefail

DRY_RUN=0
FORCE=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --force) FORCE=1 ;;
    -h | --help)
      sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "unknown argument: $arg" >&2
      exit 2
      ;;
  esac
done

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$SKILL_DIR/assets/statusline-command.sh"
CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
DEST="$CONFIG_DIR/statusline-command.sh"
SETTINGS="$CONFIG_DIR/settings.json"
STAMP="$(date +%Y%m%d%H%M%S)"

say() { printf '%s\n' "$*"; }
plan() { if [ "$DRY_RUN" = 1 ]; then printf 'would: %s\n' "$*"; else printf '%s\n' "$*"; fi; }

# --- preconditions ------------------------------------------------------------

[ -f "$SRC" ] || {
  echo "missing bundled script: $SRC" >&2
  exit 2
}

if ! command -v jq >/dev/null 2>&1; then
  cat >&2 <<'EOF'
jq is not on PATH.

The status line script reads Claude Code's JSON payload with jq, and this
installer edits settings.json with it. Without jq the status line renders as an
empty bar. Install it first (macOS: brew install jq) and re-run.
EOF
  exit 2
fi

if [ -e "$SETTINGS" ] && ! jq empty "$SETTINGS" >/dev/null 2>&1; then
  echo "cannot parse $SETTINGS as JSON. Not touching it. Fix the file and re-run." >&2
  exit 2
fi

# --- the script ---------------------------------------------------------------

if [ -f "$DEST" ] && cmp -s "$SRC" "$DEST"; then
  say "script: already current at $DEST"
else
  if [ -f "$DEST" ]; then
    plan "script: backing up existing $DEST to $DEST.bak-$STAMP"
    [ "$DRY_RUN" = 1 ] || cp -p "$DEST" "$DEST.bak-$STAMP"
  fi
  plan "script: installing $DEST"
  if [ "$DRY_RUN" != 1 ]; then
    mkdir -p "$CONFIG_DIR"
    cp "$SRC" "$DEST"
    chmod +x "$DEST"
  fi
fi

# --- the setting --------------------------------------------------------------

DESIRED="bash $DEST"
CURRENT=""
[ -f "$SETTINGS" ] && CURRENT="$(jq -r '.statusLine.command // ""' "$SETTINGS")"

if [ -z "$CURRENT" ]; then
  NEEDS_WRITE=1
elif [ "$CURRENT" = "$DESIRED" ] || [[ "$CURRENT" == *"$DEST"* ]]; then
  # Already runs our script, possibly written with different quoting. Leave it.
  NEEDS_WRITE=0
  say "setting: already points at $DEST"
elif [ "$FORCE" = 1 ]; then
  NEEDS_WRITE=1
  say "setting: replacing existing status line command ($CURRENT)"
else
  cat >&2 <<EOF
settings.json already has a status line, pointing somewhere else:

  $CURRENT

Leaving it alone. Re-run with --force to replace it (settings.json is backed up
first), or keep what you have.
EOF
  exit 3
fi

if [ "$NEEDS_WRITE" = 1 ]; then
  plan "setting: writing statusLine into $SETTINGS"
  if [ "$DRY_RUN" != 1 ]; then
    if [ -f "$SETTINGS" ]; then
      cp -p "$SETTINGS" "$SETTINGS.bak-$STAMP"
      say "setting: backed up $SETTINGS to $SETTINGS.bak-$STAMP"
    else
      mkdir -p "$CONFIG_DIR"
      printf '{}\n' >"$SETTINGS"
    fi
    tmp="$SETTINGS.tmp-$STAMP"
    jq --arg cmd "$DESIRED" '.statusLine = {type: "command", command: $cmd}' \
      "$SETTINGS" >"$tmp"
    mv "$tmp" "$SETTINGS"
  fi
fi

# --- preview ------------------------------------------------------------------

if [ "$DRY_RUN" != 1 ] && [ -f "$DEST" ]; then
  preview="$(
    jq -nc --arg cwd "$PWD" \
      '{session_name: "preview",
        model: {display_name: "Opus 5"},
        workspace: {current_dir: $cwd},
        context_window: {used_percentage: 42}}' |
      bash "$DEST" || true
  )"
  printf 'preview: %s\n' "$preview"
fi

say "done. The status line picks this up on its next refresh, no restart needed."
