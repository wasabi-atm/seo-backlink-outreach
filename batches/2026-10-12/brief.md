# Brief: backlink-2026-10-12 (170 sites, 4 batches)

- Goal: 170 new sites at DR 40 or higher, through Step 4, run as 4 batches of about 43 (half Segment A, half Segment B). UK and UAE first, then US. Campaigns: backlink-2026-10-12, backlink-2026-10-12-b2, backlink-2026-10-12-b3, backlink-2026-10-12-b4.
- Research for all four batches runs once, here in `batches/2026-10-12/research/`. After Checkpoint 1 the approved list is split into the four batch folders (`2026-10-12`, `2026-10-12-b2`, `-b3`, `-b4`), and Steps 3 to 6 run per folder.
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given beyond the ledger. Ledger before this run: 1698 rows.
- Each batch is logged in the ledger and pushed separately.

## Credits at the start (12 Oct)

- Instantly: 1559.8 credits (refreshed).
- Apollo: 2500 lead credits (cycle 10 Oct to 10 Nov).
- Ahrefs: 19 API units left until 30 Oct, so DR comes from the free `public-domain-rating-free` tool, with Apify `radeance/ahrefs-scraper` as backup.
- Apify: $25.83 of the $60 monthly cap used (cycle to 2 Nov), so about $34 left for the whole run.

## Environment

- Cloud session. Company sites are blocked from the sandbox (proxy 403), so no screenshots, no crawl4ai: vetting, blog reads and article picks run through Apify, as on 9 Oct.

## Progress log

- Sync (12 Oct): checkout equals origin/main (7ea9c65). Interview answered with the recommended defaults (same brief as 9 Oct). Exclude list 3480 domains. Research started with a shared claims file (research/claims.tsv) so parallel agents never pick the same company.
- Research done (12 Oct): 15 agents, 248 rows (A 137, B 111; US 165, UK 82, UAE 1). dedupe.py check: 248 clean, 0 removed. UAE pool is nearly dry (only WebBeds). Unused slice claims stay in research/claims.tsv; slices left reserves of DR 40+ domains without a blog check.
- Step 2b vetting (12 Oct): no screenshots possible (sandbox blocks sites). One Apify cheerio run on 248 homepages, 245 loaded; gurucul.com and veem.com fail even with residential proxy and www. HubSpot: raintreeinc.com has an open deal (dropped); leads only (kept): addpeople.co.uk, athenahq.ai, writesonic.com, doola.com, usepylon.com, vectara.com. Hard fails: censornet.com redirects to trustlayer.co.uk (dropped); doubleclick/taboola/adnxs on bkacontent, uscreen, businessolver, perceptyx, quotapath, crunchtime, doola; farm words betting (salience.co.uk) and casino (complycube.com); limblecmms.com is now limble.com. No competitors flagged. 01_prospects_proposed.csv holds the status per row. Checkpoint 1: waiting on the user.
- Checkpoint 1 answers (12 Oct): keep the 7 ad-network sites (bkacontent, uscreen, businessolver, perceptyx, quotapath, crunchtime, doola), keep salience.co.uk and complycube.com, keep gurucul.com and veem.com (verify at Step 3, drop if blogs unreadable), send everything forward in 4 batches. limblecmms.com renamed to limble.com (DR 70). 246 prospects; DR rechecked with the free Ahrefs tool, all 40 or higher.
- Split (12 Oct): batch 1 = 2026-10-12 (62: UK 61, UAE 1), batch 2 = 2026-10-12-b2 (62: UK 20, US 42), batch 3 = 2026-10-12-b3 (61 US), batch 4 = 2026-10-12-b4 (61 US). Each folder has 01_prospects.csv and step3/in_0..3.csv. 16 Step 3 agents started (4 per batch, Apify, link habits). Steps 3 to 4 per folder; Step 5 only on request. Surplus over 170 is the spare pool, so batches may be trimmed to the best 43 after Step 4.
- Step 3 done (12 Oct): 16 agents, 246 rows read with Apify (about $1 in total). merge_step3.py -> 02_enriched.csv in each of the four folders: 244 rows, DR 40 to 86, 02_low_dr.csv empty in all four (nothing to pool). backlinkExchange Yes 77, Some 88, No 76, unchecked 3 (explori.com and bigmotive.com in batch 1 are script-rendered, plansource.com in batch 3). gurucul.com (b2) and veem.com (b3) blocked Apify at Step 3 as well, so they are dropped per the Checkpoint 1 answer (02_dropped_unreadable.csv). Per batch: b1 62 (Yes 19, Some 22, No 19, unchecked 2), b2 61, b3 60, b4 61. Checkpoint 2: waiting on the user.
- Checkpoint 2 approved (12 Oct): Step 4 on all 244. 16 Step 4 agents started (4 per batch, step4/STEP4_BRIEF.md in each folder, Apify, one article plus hook per company). Then merge_step4 -> 03_backlink_targets.csv per folder, trim each batch to its best ~43 (strong, then ok), hold the rest as spares. Step 5 only on request.
- Step 4 done (12 Oct): 16 agents, 243 rows (dead: skale.so, studiorepublic.com). merge_step4.py -> 03_backlink_targets.csv per folder (b1 60, b2 61, b3 60, b4 61 non-dead; strong 90, ok 114, weak 38). select_best.py picks the best 170 (all strong, then ok ranked by link habits, UK and UAE first): targets_43.csv (b1), targets_43.csv (b2), targets_42.csv (b3), targets_42.csv (b4). Weak rows held in 03_held_weak.csv, surplus ok rows in 03_spares.csv (34). Combined file: batches/2026-10-12/backlink_targets_170.csv. dedupe.py check on all four: 0 removed. Nothing logged in the ledger yet (that happens at Step 5, when emails are drafted). Step 5 only on request.
- Cost (12 Oct): Apify $1.87 for the whole run (account usage $25.83 before, $27.71 after, of the $60 monthly cap). Instantly, Apollo and Ahrefs credits not used (DR from the free Ahrefs tool).

## Batch 1 (2026-10-12), Step 5

- Step 5 requested by the user (12 Oct) for batch 1 (targets_43.csv). Subjects: the user's four templates, as on 9 Oct (confirmed 12 Oct).
- Contacts (12 Oct): Instantly SuperSearch for Segment A founders and CEOs (22 contacts imported, 15 companies; the Segment B import with one lead per company stayed "in progress" with no leads for 30+ minutes, so it was dropped), Apollo for Segment B marketing leads and the A and B leftovers (26 standard reveals, 26 lead credits; 2500 before), the Apify leads scraper returned nothing (needs maxPerCompany 10 and totalResults 100, still no leads), website emails via cheerio (hopperhq.com has only support@, skipped; pixeledeggs.com has none). 41 of 43 have an email (15 instantly, 26 apollo). No email: pixeledeggs.com, hopperhq.com. Overrides: fox.agency set to Ben Fox (CEO) not the UK MD; fieldmotion.com added by hand (title MD). dedupe.py check: 0 removed.
- Flags: summit.co.uk email is on summitmedia.com (confirm same company); scribeless.co Apollo title reads 'Co-Founder of Yuzu'; armstrongb2b.com and addpeople.co.uk contacts are not founders (quote swap: 'one from your side for ours').
- Emails: four agents (step5/STEP5_BRIEF.md) writing; Instantly campaign check by a background agent (step5/campaign_check.csv).
