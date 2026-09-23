# MTA backlink outreach

Private workspace for Motion The Agency's backlink outreach, synced between devices.

- `skill/mta-backlink-outreach/`: the Claude skill (SKILL.md) and its scripts. This copy is the source of truth.
- `outreach_ledger.csv`: every company already contacted. The dedupe check reads it so no company is emailed twice.
- `low_dr_pool.csv`: companies under DR 40, kept for manual outreach on request.
- `batches/<date>/`: the CSVs from each run. `sent/`: copies of sent batches.

## New device setup

```
git clone https://github.com/wasabi-atm/seo-backlink-outreach.git ~/Desktop/mta-backlink-automation
cd ~/Desktop/mta-backlink-automation
python3 -m venv .venv
.venv/bin/pip install webscreenshotter "selenium<4.10" webdriver-manager pillow
```

Google Chrome must be installed for screenshots.

## Sync

`sh skill/mta-backlink-outreach/scripts/sync.sh pull` before a run, `sh skill/mta-backlink-outreach/scripts/sync.sh push "message"` after. The skill does both on its own.

To update the skill in claude.ai after changing it here: `cd skill && zip -r mta-backlink-outreach.zip mta-backlink-outreach`, then upload the zip.
