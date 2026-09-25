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

The Step 4 blog crawl uses crawl4ai, which needs Python 3.10+ (`brew install python@3.12` on a Mac) and its own venv:

```
python3.12 -m venv .venv-crawl
.venv-crawl/bin/pip install -U crawl4ai
.venv-crawl/bin/crawl4ai-setup
```

The Step 4b video schema check (`video_schema.py`) runs in the same `.venv-crawl`. It calls the Apify actor `dev00/google-rich-results-checker` itself when `APIFY_TOKEN` is set in the environment. Without the token, Claude runs the actor through the Apify connector instead.

## Sync

`sh skill/mta-backlink-outreach/scripts/sync.sh pull` before a run, `sh skill/mta-backlink-outreach/scripts/sync.sh push "message"` after. The skill does both on its own.

To update the skill in claude.ai after changing it here: `cd skill && zip -r mta-backlink-outreach.zip mta-backlink-outreach`, then upload the zip.
