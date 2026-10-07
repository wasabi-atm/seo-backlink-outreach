# Brief: backlink-2026-10-07

- Target: 160 sites at DR 40 or higher, 80 in Segment A and 80 in Segment B. UK and UAE first, then US. Plus a 40 site buffer carried through Steps 3 and 4 (best 160 kept).
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given beyond the ledger. Ledger before this run: 1311 rows.
- Batch shape: 160 sites, 80 A / 80 B, vetted in chunks of 40.

## Progress log

- Sync (7 Oct): main pulled, session branch claude/awesome-archimedes-n8zrlt equals origin/main (4a81c97). Repo SKILL.md followed (it is newer than the claude.ai copy: re-upload the zip per README).
- Interview answered (7 Oct): all defaults as above, all four Segment B offers allowed.
- Network: cloud proxy blocks company sites (hubspot.com 403), no Chrome in PATH for webscreenshotter and no .venv, so Apify route again, no screenshots, no video schema check.
- exclude_domains.txt (3022 root domains) built by build_exclude.py: ledger, pool, form master, client lists, all earlier batch files. Yesterday's unused spares (98, reusable_spares.txt) are NOT excluded so they can be reused.
- Research (7 Oct): eight agents (research/RESEARCH_BRIEF.md). New rows A_UKUAE 3, A_US_AGENCY 14, A_US_MARTECH 14, A_US_CREATIVE 10, B_UKUAE 21, B_US_PEOPLE 12, B_US_FIN 14, B_US_TECH 14 plus 98 reusable spares from 6 Oct. merge_research.py: 195 rows, dedupe.py check removed Red Sift (queued 6 Oct), 194 clean.
- HubSpot: 2 matches (Cowbell, HockeyStack), both leads with no deals, kept.
- Vetting (Apify cheerio, step2/vetting.csv): hard fails digitalcurrent.com (redirects to semify.com), hookagency.com (doubleclick), netcall.com (media.net), pond5.com (no load). Held pending user: wickedreports.com and puzzle.io (farm word "betting", likely incidental, sentence not visible). 7 "loans" checks on finance sites, kept.
- 01_prospects.csv: 188 rows, A 74 (UK 5, US 69), B 114 (UK 23, US 91). No UAE. Competitors included yesterday by user: bluetext.com, whalar.com (quote swap only), carried over, to reconfirm.
- Checkpoint 1: waiting on the user.
- Checkpoint 1 approved by the user (7 Oct): all 188 as is, wickedreports.com and puzzle.io kept (190 rows), bluetext and whalar included quote swap only. Carry all 190 through Steps 3 and 4, keep best 160 after.
- Step 3 done (7 Oct): five agents (step3/STEP3_BRIEF.md), Apify cheerio only, DR from the free Ahrefs endpoint (research day), no paid Ahrefs units. 190 rows, all DR 40 to 91 (02_enriched.csv, 02_low_dr.csv empty). Yes 36, Some 62, No 71, unchecked 21 (script-rendered or missing blogs; Step 4 will try to read them). Weak Yes: jobscore, passle, thrivecart.
- Checkpoint 2: waiting on the user.
- Checkpoint 2 approved by the user (7 Oct): all 190 go to Step 4; keep best 160 after (fit first, then link habits, balance A/B as far as the pool allows).
- Step 4 done (7 Oct): five agents (step4/STEP4_BRIEF.md), Apify cheerio, website-content-crawler and playwright retries. 190 rows: dead 6 (3sidedcube, accesswire, nexhealth, rillet, whalar, iomart; 03_dropped.csv, not logged).
- merge_step4.py: 160 in 03_backlink_targets.csv, A 73 (UK 4, US 69), B 87 (UK 12, US 75), no UAE. Fit strong 51, ok 88, weak 21. Links Yes 35, Some 53, No 62, unchecked 10. Offers: Founder's quote swap 73, Video for the blog post 52, Blog graphic or infographic 34, Internal data 1. 03_spares.csv holds the other 24 weak rows. Old first-published: copypress (2023-12), goguardian (2019, updated 2026-07). 71 rows have no confirmed article date, check before emailing.
- Competitors in the list (quote swap only): bluetext.com. Whalar dead, not carried.
- Step 5 requested by the user (7 Oct, "continue with step 5"). Credit caps still to confirm.
- Contacts (7 Oct): two agents (step5/CONTACTS_BRIEF.md) within the user's caps (Instantly 250, Apollo 20, Apify $1): Instantly list balance 442.8 to 310.8 (132 credits), Apollo 23 to 7 (16 credits), Apify about $0.24. 143 of 160 with an email (130 named, 13 shared inboxes), 17 with none. 19 emails already in another Instantly campaign dropped by the user (blanked, logged not_sent). 124 emails.
- Emails: six agents with the humanizer pass, subjects from the user's four templates mixed (quick question 34, noticed something 31, ASAP 31, Quick intro 28). assemble.py checks pass: all under 110 words, no dashes, no merge tags. 96 of 124 carry a manualCheck note. 04_backlink_emails.csv.
- Logged under backlink-2026-10-07: 124 queued, 36 not_sent.
