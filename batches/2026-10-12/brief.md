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
