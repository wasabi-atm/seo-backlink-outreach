# MTA backlink outreach

Private workspace for Motion The Agency's backlink outreach, synced between devices.

- `skill/mta-backlink-outreach/`: the Claude skill (SKILL.md) and its scripts. This copy is the source of truth.
- `outreach_ledger.csv`: every company already contacted. The dedupe check reads it so no company is emailed twice.
- `low_dr_pool.csv`: companies under DR 40, kept for manual outreach on request.
- `batches/<date>/`: the CSVs from each email run. `sent/`: copies of sent batches.
- `form-outreach/`: the contact form workflow. Its skill is `skill/mta-backlink-form-outreach/SKILL.md`, every form batch is in `form-outreach/batches/<date>/`, and `form-outreach/form_outreach_master.csv` lists every company reached through a form. It shares the ledger above, so no company gets both an email and a form.

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

The Step 2c video schema check (`video_schema.py`) runs in the same `.venv-crawl`. The script never calls Apify: Claude runs the actor `dev00/google-rich-results-checker` through the Apify MCP.

The Step 5 contact waterfall (`contacts.py`: Instantly, then Apollo, then Apify `peakydev/leads-scraper-ppe`, then the website's contact email) also runs in `.venv-crawl` for its website step. The paid sources run through their MCP tools; the script only picks and tracks contacts.

## Sync

`sh skill/mta-backlink-outreach/scripts/sync.sh pull` before a run, `sh skill/mta-backlink-outreach/scripts/sync.sh push "message"` after. The skill does both on its own.

To update the skill in claude.ai after changing it here: `cd skill && zip -r mta-backlink-outreach.zip mta-backlink-outreach`, then upload the zip.
