# Brief: backlink-2026-10-02

- Target: 150 sites at DR 40 or higher, 75 in Segment A and 75 in Segment B. UK and UAE first, then US.
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given. Ledger before this run: 902 rows (backlink-2026-09-23 to -10-01).

## Progress log

- Sync pull done (main efb3072). Repo SKILL.md followed (Step 2c video schema, crawl4ai Step 4, subject rules, Step 6 Instantly draft).
- Interview answered (2 Oct): all defaults as above, all four Segment B offers allowed.
- Research (2 Oct): six agents (research/RESEARCH_BRIEF.md). Rows: A_UK 5, A_UAE 2, A_US 28, B_UK 20, B_UAE 4, B_US 35, plus 71 spares from 1 Oct. The UK and UAE pools are nearly used up. Dedupe of 00_candidates.csv: 165 in, 7 removed (6 repeats between spares and A_US, plus Clay matching clay.global). clay.com added back (user confirmed on 1 Oct it is a different company). 159 clean.
- Network: cloud blocks company sites, so Apify route again. No screenshots (no design score), Step 2c video schema skipped, videoSchemaGap blank. Homepage scan via Apify cheerio-scraper (vetting.csv, under $0.10).
- Hard fails (8, 01_dropped.csv): contentful.com, century.tech, netdocuments.com, amvbbdo.com (do not load), spyfu.com, expel.com, buildium.com (doubleclick), shipbob.com (outbrain). treasuryprime.com has the word betting in visible text, kept to check.
- Selection (select.py): 148 in 01_prospects.csv, A 73 (UK 8, UAE 6, US 59), B 75 (UK 19, UAE 4, US 52). 3 spares. 21 picks have no visible post date.
- Checkpoint 1: waiting on the user.
- Checkpoint 1 approved by the user (2 Oct), all 148 go to Step 3. Ahrefs had about 33k units left until 30 Oct, so DR came from the free endpoint and linked-domains was capped at 50 rows (about 14k units in total). Counts of outside domains are lower bounds.
- Step 3 done: all 148 at DR 40 or higher, so 02_low_dr.csv is empty and nothing goes to the pool. See Checkpoint 2.
- Checkpoint 2: waiting on the user.
- Checkpoint 2 approved by the user (2 Oct), all 148 kept. Step 4 started: five agents pick one article and hook per company via Apify (step4/STEP4_BRIEF.md), crawl4ai cannot reach sites from the cloud. They also record articlePublished and publishedSource.
- Step 4 done. merge_step4.py: see 03_backlink_targets.csv and 03_dropped.csv. Dead (not logged): paytabs.com (blog renders by script, no posts readable).
- Checkpoint 3 (2 Oct): user dropped the 15 weak fits (03_dropped_weak.csv, not logged), 132 targets, go to Step 5. Caps not given, so 1 Oct caps apply: Instantly 200, Apollo 100, Apify $1. Contacts agent running (step5/CONTACTS_BRIEF.md).
- User (2 Oct): use all five of their subject templates, mixed through the list (quick question about your X / noticed something in your X article / fresh data for your X piece / ASAP: need your response on your X piece!! / Quick intro, name?). One subject per row, no A/B. Plan: "fresh data" only on a row whose offer is Internal data (none this batch), since it would not be true otherwise; the other four mixed through the list.
- Contacts (agent, step5/CONTACTS_BRIEF.md): 117 named people (Instantly 94, Apollo 15, Apify 8), 6 shared inboxes from websites, 9 with nothing (rentmanager, onelogin, unitedseo, cience, wordagents, mailgun, elevationb2b, localiq, takepayments). Credits: Instantly 124 (674.8 left), Apollo 19 spent but balance fell 193 to 96 (about 78 drawn by something else on the account), Apify about $0.17. Apify emails are unverified.
- Already in another Instantly campaign: 11 (4 live: sybill.ai, samsara, spektrix, conga; 7 completed: mailshake, thegood, logicmonitor, criteriacorp, coalitioninc, netskope, highnote). User (2 Oct): drop all 11 (emails blanked, logged not_sent).
- Emails: five agents wrote 112 emails (step5/STEP5_BRIEF.md), then three review agents ran the humanizer and a fact check against the hooks (20 emails fixed). 04_backlink_emails.csv via step5/assemble.py: 132 rows, 112 with an email, 71 with a manualCheck note.
- Subjects: one per row from the user's templates, mixed (29 noticed something, 28 quick question, 28 ASAP, 27 Quick intro; 0 fresh data because no row offers data). subject_check.py flags 'quick question', '!' and length on these by design; left as the user asked. One duplicate (Quick intro, David?) changed to noticed something.
- Dedupe with emails: 131 clean, clay.com matches clay.global by brand (user confirmed different on 1 Oct), so it was not logged again by dedupe.py log. Logged under backlink-2026-10-02: 111 queued, 20 not_sent. clay.com is therefore not in the ledger as its own row.
- Step 6: Instantly draft "2 October 2026 - Backlink Cold Outreach Campaign" (id in instantly/campaign.txt), 112 leads, status draft, no sender accounts set, not activated.
