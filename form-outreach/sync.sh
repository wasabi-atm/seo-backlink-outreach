#!/bin/sh
# Keeps the form outreach files in sync with GitHub, from any folder on any device.
#
#   sh form-outreach/sync.sh pull                 get the latest ledger, master list and batches (run before every task)
#   sh form-outreach/sync.sh push "what changed"  commit and push everything (run after every change)
#
# It uses the same script as the email workflow (skill/mta-backlink-outreach/scripts/sync.sh),
# pointed at the repo this file lives in, so the shared ledger and the form files always move together.
# Exit codes: 0 ok, 2 bad usage, 3 needs a person (conflict, no network, no access, repo public).
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/.." && pwd)
MTA_REPO="$REPO" exec sh "$REPO/skill/mta-backlink-outreach/scripts/sync.sh" "$@"
