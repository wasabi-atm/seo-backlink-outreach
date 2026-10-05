# Form outreach

Backlink outreach through prospects' own website contact forms, for companies where no email contact was found or where a form reaches the blog team better than a cold email. The workflow is the `mta-backlink-form-outreach` skill (`skill/mta-backlink-form-outreach/SKILL.md`). The repo copy is the source of truth.

## What lives here

- `form_outreach_master.csv`: every company sent through a form, across all batches, with the form link, article, DR and status (`ready`, `sent`, `not_sent`). This is the one place to see the whole form outreach list.
- `batches/<YYYY-MM-DD>/`: the files from one run.
  - `00_candidates*.csv`: candidates and the dedupe check.
  - `02_forms.csv`: what was found on each site's contact page, including skipped sites and any public email (`altEmail`) worth using in an email batch instead.
  - `02_low_dr.csv`: sites under DR 40 (also added to the shared `low_dr_pool.csv`).
  - `03_form_targets.csv`: tracking detail for each site: DR (checked that day with the Ahrefs API or Apify), article, segment, offer, CAPTCHA and consent notes.
  - `06_form_outreach.csv`: the file for whoever submits the forms. Five columns: companyName, formUrl, beforeSubmit (anything to do besides pasting), subjectText and messageText. Use the name and reply email from `brief.md` on every form.
  - `brief.md`: the answers from the interview.

## Keeping it synced

Run `sh form-outreach/sync.sh pull` before any form outreach work, and `sh form-outreach/sync.sh push "what changed"` straight after anything changes (a batch saved, rows logged in the ledger, the master list updated, forms marked sent). It works from any folder and uses the same sync script as the email workflow, so the ledger, the low DR pool, the master list and the batches always move together. If either command fails, stop and fix it before carrying on, so a company is never contacted twice.

## Shared with email outreach

The ledger (`outreach_ledger.csv`) and the low DR pool (`low_dr_pool.csv`) stay at the repo root and are shared with the email workflow, so a company is never contacted by both. Form rows are logged with `dedupe.py log ... --channel form`, which makes them block repeats even though they have no email address. Form campaigns are named `backlinkform-<YYYY-MM-DD>`.

## Rules in short

- The article has to match Motion: SaaS video, B2B video, video marketing, advertising or content marketing, live and updated within two years. A site with a form but no matching article is dropped.
- Messages copy the latest Instantly backlink email word for word, with URLs written out and "Founder @ Motion The Agency" under Sam.
- Nothing is filled in or submitted automatically. A person opens each link, pastes the message and submits.
- After sending, mark rows `sent` in the ledger (`set-status ... --channel form`) and in `form_outreach_master.csv`, then `sync.sh push`.
