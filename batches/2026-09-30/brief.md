# Brief: backlink-2026-09-30

- Target: 150 sites at DR 40 or higher, 75 in Segment A and 75 in Segment B. UK and UAE first, then US.
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given. Ledger before this run: 618 rows (backlink-2026-09-23 to -29).

## Progress log

- Sync pull done (main 8ec9223). Repo SKILL.md differs from the claude.ai copy, so the repo version is followed. The claude.ai copy is out of date and should be re-uploaded.
- Candidate research (30 Sep): four agents added 113 new candidates (A UK/UAE 28, A US 23, B UK/UAE 31, B US 30). Merged with 148 spares into 00_candidates.csv (260). Dedupe: 1 removed, Napier AI (possible match with Napier, backlink-2026-09-23-b).
- Vetting route: Apify only (cloud blocks prospect sites). No screenshots, so no design score. Step 2c skipped.
- Selection: 150 in 01_prospects.csv (A 75, B 75). UAE is thin: 9 A and 17 B. IFZA and DMCC (free-zone authorities) left out. 109 of 150 have a dated post since Oct 2025. Competitors held out for the user's decision: 01_competitors_to_decide.csv.
- Checkpoint 1: waiting on the user.
- Competitor answers (30 Sep): include, quote swap only: Here Now Films, Explainify, Lemonlight, Yum Yum Videos. Column Five and Radley Yeldar keep their earlier includes (25 and 29 Sep).
- Cleanup: 13 spares dropped because their blogs were found dead or duplicate on 29 Sep (Turner Duckworth, Show + Tell, Eastside Co, Gleanin, Little Warden, Opteo, Talentera, Okadoc, Letswork, GBM, Saal.ai, Pyypl, Presight). 4 dropped for a last post older than Oct 2025 (Mapp, Seeker, Eventsforce, PushON).
- Result: 01_prospects.csv has 111 (A 53, B 58) with a blog post since Oct 2025 or an included competitor. 01_unverified_spares.csv has 28 more (A 18, B 10) with no blog date. 150 is not reachable with verified blogs. Napier AI (possible match with Napier) is held out, awaiting the user.
- Checkpoint 1: waiting on the user.
- Step 3 (30 Sep, Ahrefs via 4 agents, in-content or all outbound links, capped at 100 rows per domain): all 111 have DR 40 or higher (40 to 91), so 02_low_dr.csv is empty and nothing goes to the pool. Ahrefs signed out mid-run, so 12 rows are backlinkExchange=unchecked (Cribl, Collibra, Seamless.ai, Filevine, gcc-marketing.com, Alation, Everlaw, Melio, Logikcull, Relativity, HireRight, GoodTime). Weak Yes calls flagged in the evidence: Zand, DP World, mrs.digital, Simplecast, Webcastle, Freuds, Ripjar, Yomly, OptinMonster.
- Checkpoint 2: waiting on the user.
- Step 4 (30 Sep, user approved Apify cheerio-scraper route): five agents picked one article and hook per company, checked no-video claims against raw HTML where they could. 03_backlink_targets.csv built from step4/out_0..4.csv.
- Checkpoint: waiting on the user to drop or keep the weak and dead rows before Step 5.
- User (30 Sep): drop the 10 weak and dead fits (Freuds, DP World, e& enterprise, eDirect, Checkr, Wrapped Agency, Simplecast, Pentagram, Telr, Code and Theory). Moved to 03_dropped_weak.csv, not logged in the ledger, so they can come up again. 03_backlink_targets.csv now holds 101 rows. Step 5 (emails) not started; waits for the user to ask.
