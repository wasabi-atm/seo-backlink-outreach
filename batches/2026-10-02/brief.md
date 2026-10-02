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
