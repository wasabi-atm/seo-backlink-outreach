#!/bin/sh
# Keeps the backlink outreach repo in sync between devices.
#
#   sh sync.sh pull                 clone if missing, else pull the latest (run before every task)
#   sh sync.sh push "what changed"  commit everything and push (run after every task)
#
# Repo folder: $MTA_REPO, default ~/Desktop/mta-backlink-automation
# Exit codes: 0 ok, 2 bad usage, 3 needs a person (conflict, no network, no access).
set -u
REPO="${MTA_REPO:-$HOME/Desktop/mta-backlink-automation}"
URL="https://github.com/wasabi-atm/seo-backlink-outreach.git"
export GIT_TERMINAL_PROMPT=0

fail() { echo "SYNC FAILED: $1" >&2; exit 3; }

case "${1:-}" in
  pull)
    if [ ! -d "$REPO/.git" ]; then
      [ -e "$REPO" ] && [ -n "$(ls -A "$REPO" 2>/dev/null)" ] && fail "$REPO exists but is not a git repo. Move it aside, then run pull again."
      git clone "$URL" "$REPO" || fail "could not clone $URL"
      echo "Cloned into $REPO"
      exit 0
    fi
    git -C "$REPO" pull --rebase --autostash || fail "pull failed. Resolve it in $REPO before running the task."
    echo "Up to date: $(git -C "$REPO" log -1 --format='%h %s (%cr)')"
    ;;
  push)
    [ -n "${2:-}" ] || { echo "usage: sync.sh push \"message\"" >&2; exit 2; }
    git -C "$REPO" add -A
    if git -C "$REPO" diff --cached --quiet; then
      echo "Nothing to push"
      exit 0
    fi
    git -C "$REPO" commit -q -m "$2" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || fail "commit failed"
    for attempt in 1 2 3; do
      if git -C "$REPO" push -q origin HEAD; then
        echo "Pushed: $(git -C "$REPO" log -1 --format='%h %s')"
        exit 0
      fi
      # Another device pushed first. CSV data files use the union merge driver, so rows from both sides are kept.
      git -C "$REPO" pull --rebase --autostash || fail "rebase conflict in $REPO. Resolve it, then push again."
    done
    fail "push rejected 3 times"
    ;;
  *)
    echo "usage: sync.sh pull | push \"message\"" >&2
    exit 2
    ;;
esac
