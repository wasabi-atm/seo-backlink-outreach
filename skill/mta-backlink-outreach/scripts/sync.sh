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
    # Always bring in the latest main from GitHub, also when working on a branch (cloud sessions use one).
    git -C "$REPO" fetch -q origin main || fail "could not fetch main from GitHub (network or access)."
    if [ "$(git -C "$REPO" rev-parse --abbrev-ref HEAD)" = "main" ]; then
      git -C "$REPO" pull -q --rebase --autostash origin main || fail "pull failed. Resolve it in $REPO before running the task."
    else
      git -C "$REPO" merge -q --no-edit --autostash origin/main || fail "merging main into this branch failed. Resolve it in $REPO before running the task."
    fi
    echo "Up to date with main: $(git -C "$REPO" log -1 --format='%h %s (%cr)' origin/main)"
    ;;
  push)
    [ -n "${2:-}" ] || { echo "usage: sync.sh push \"message\"" >&2; exit 2; }
    # The ledger holds real contact emails. Read the "private" field rather than the status code:
    # a private repo answers 404 without login, but 200 with "private": true when the request carries
    # credentials (cloud sessions add them through a proxy).
    info=$(curl -s https://api.github.com/repos/wasabi-atm/seo-backlink-outreach)
    echo "$info" | grep -Eq '"private": *false' && fail "the GitHub repo is PUBLIC. Make it private before pushing contact data."
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
