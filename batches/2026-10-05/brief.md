# Brief: backlink-2026-10-05

- Target: 150 sites at DR 40 or higher, 75 in Segment A and 75 in Segment B. UK and UAE first, then US.
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given. Ledger before this run: 1033 rows (backlink-2026-09-23 to -10-02).

## Progress log

- Sync pull done (main bb3b9b9). Repo SKILL.md followed.
- Interview answered (5 Oct): all defaults as above, all four Segment B offers allowed.
- Research (5 Oct): six agents. Rows: A_UK 6, A_UAE 1, A_US 32, B_UK 14, B_UAE 2, B_US 44 (99). Dedupe: 6 removed (Cactix, The SEO Works, Jellyfish UK already in ledger; one Insightly repeat; SEO.co possible match to SEO.AE; Jellyfish.co brand match to the UK agency, different company per agent). 93 clean.
- Vetting: Apify homepage scan (vetting.csv). Same as 2 Oct: no screenshots, no video schema, visualScore and videoSchemaGap blank. 10 hard fails dropped (01_dropped.csv). 83 in 01_prospects.csv: A 30, B 53; UK 17, UAE 2, US 64. Short of the 150 target.
- Checkpoint 1: waiting on the user.
- Checkpoint 1 approved by the user (5 Oct): run the 83 as is (no extra research round), put back jellyfish.co and seo.co (both homepage scans clean), drop the 12 undated sites (01_dropped_undated.csv). 73 go to Step 3.
- Step 3 done: DR from the free endpoint, linked-domains capped at 50 rows (about 6,900 units). All 73 at DR 40 or higher, so 02_low_dr.csv is empty and nothing goes to the pool. Link habits: Yes 55, Some 13, No 5, see 02_enriched.csv.
- Checkpoint 2: waiting on the user.
- Checkpoint 2 approved by the user (5 Oct), all 73 go to Step 4. Three agents picked one article per company via Apify (step4/STEP4_BRIEF.md). merge_step4.py: 73 targets, 0 dead. Fit: strong 26, ok 36, weak 11. 26 have no readable article date. Segment B offers: video 25, graphic 22, internal data 2, founder's quote 1.
- Step 4 done. 03_backlink_targets.csv sent to the user. Step 5 only when the user asks.
