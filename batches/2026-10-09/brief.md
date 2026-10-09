# Brief: backlink-2026-10-09

- Goal: 160 new sites at DR 40 or higher, run as 4 batches of 40 (20 Segment A, 20 Segment B each). UK and UAE first, then US. Batch 1 is this folder; later batches use the suffix -b2, -b3, -b4.
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given beyond the ledger. Ledger before this run: 1625 rows.
- Each batch is logged in the ledger and pushed before the next one starts.

## Progress log

- Sync (9 Oct): checkout equals origin/main (52e5136). Repo SKILL.md is newer than the claude.ai copy (video schema check, crawl4ai, Step 6). Interview answered with the recommended defaults.
- Candidates (9 Oct): 8 research agents returned 52 rows (A_UK_CREATIVE 0, A_UK_AGENCY 3, A_UKUAE_MARTECH 7, A_US_AGENCY 6, A_US_MARTECH 5, B_UKUAE 6, B_US_FIN_PEOPLE 13, B_US_TECH_VERT 12). dedupe.py check: 52 clean, 0 removed. UAE: only secure.com.
- Step 2b vetting (9 Oct): no screenshots possible (sandbox blocks sites, no Chrome). One Apify cheerio run on 52 homepages (48 loaded first pass, nextroll and bridgehead on retry, taxdome 403, centerbase SSL error). No farm words, no parked, no write-for-us flags. Doubleclick: inventry.co.uk, mpulsesoftware.com (held for user). Acquired: pocus.com (Apollo), metronome.com (Stripe), proposed drops. HubSpot: lancedb, audiomob, pocus, auditboard, upkeep are leads only, no deals, kept. videoSchemaGap not checked. 01_prospects_proposed.csv holds the status per row.
- Checkpoint 1: waiting on the user.
- Checkpoint 1 answers (9 Oct): keep all 48, pocus.com and metronome.com dropped, inventry.co.uk and mpulsesoftware.com (doubleclick) kept. 01_prospects.csv = 50 rows. Step 3 starting.
- Step 3 DR (9 Oct): free Ahrefs tool on all 50, all 40 or higher (searchberg.com exactly 40), 02_low_dr.csv will be empty. Five agents (step3/STEP3_BRIEF.md, 10 rows each) read 3 to 5 posts per blog with Apify for backlinkExchange.
- Step 3 done (9 Oct): five agents, 50 rows, 02_enriched.csv (all DR 40+), 02_low_dr.csv empty. Checkpoint 2: waiting on the user.
- Step 3 approved by the user (9 Oct, 'next step'). Step 4 started: five agents (step4/STEP4_BRIEF.md), Apify, one article per company with a hook, also confirm a post dated after Oct 2025.
- Step 4 done (9 Oct): five agents, 50 rows. merge_step4.py -> 03_backlink_targets.csv. Step 5 only when the user asks.
- Step 5 requested by the user (9 Oct) on the 41 strong and ok rows (targets_41.csv); the 9 weak rows are held in 03_held_weak.csv, not contacted.
- Step 5 contacts done (9 Oct): Instantly SuperSearch two passes (list "backlink-2026-10-09 contacts", 31 verified emails; credits before 190.8), Apollo 2 standard reveals (2 of 2 left, waterfall not used to hold the cap), Apify peakydev leads scraper gave only sales roles (22 leads, about $0.1, discarded), company-site emails via cheerio (5 shared inboxes: highervisibility, flourish, lumanu, perpetua, cleverbridge support@). 38 of 41 have an email (31 instantly, 2 apollo, 5 website); no email for browsermedia.agency, jumpfly.com, tractivity.co.uk (no_contact.csv). dedupe.py check: 0 removed. Weak role picks flagged in contactNote.
- Emails: four agents (step5/STEP5_BRIEF.md) writing; Instantly campaign check by a background agent (step5/campaign_check.csv). Subjects pending the user's choice (7 and 8 Oct used the user's four templates; repo SKILL.md has stricter subject rules).
- Emails done (9 Oct): four agents wrote 38 emails, assemble.py -> 04_backlink_emails.csv (subjects from the user's four templates, chosen 9 Oct; 10 quick_question, 10 noticed_something, 9 quick_intro, 9 asap). Checks: no dashes, no braces, all under 110 words, article link, ask and paid placement in every body, no duplicate subjects. 32 of 38 carry a manualCheck. Logged under backlink-2026-10-09 (38 queued). No-contact rows (browsermedia.agency, jumpfly.com, tractivity.co.uk) not logged.
- Campaign check (9 Oct): jake@triplewhale.com (4. Campaign - Head of Content), wilfrid@audiomob.com (BB May Campaign) and chang@lancedb.com (3. Startups - March / Dec leads Campaign) are already in Instantly campaigns. Held out of the draft, waiting on the user.
- Step 6 done (9 Oct): draft campaign "9 October 2026 - Backlink Cold Outreach Campaign" (b3c97e56-2a8d-48f8-b08e-cb6e4de01aad), status draft, no senders, not activated; 35 leads added and compared with 04_backlink_emails.csv (0 mismatches). Batch 1 of 4 ends at 38 emails.
- Credits (9 Oct): Instantly 190.8 before; about 31 verified emails imported; Apollo 2 of 2 used; Apify about $0.5 across the day.
