# Brief: backlink-2026-09-23-b

Second batch of 23 Sep 2026. A batch called backlink-2026-09-23 was already sent today, so this run is named backlink-2026-09-23-b.

- Target: 200 sites at DR 40 or higher, 100 in Segment A and 100 in Segment B, spread across UK, US and UAE.
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given yet. The ledger already holds 40 companies from backlink-2026-09-23.
- Tools: Ahrefs has 36 units left until 30 Sep, so DR comes from Apify radeance/ahrefs-scraper. The cloud proxy blocks prospect sites, so screenshots come from Apify apify/screenshot-url.

## Status at handoff (23 Sep, cloud session)

Checkpoint 1 approved: keep the 187 in `01_prospects.csv` and top up to 200 from `01_needs_check.csv`.

- Brafton: include, quote swap only (competitorDecision = include).
- DR is already done for every candidate (Apify ahrefs-scraper, in `dr1.txt`). The 187 all have DR 40 or higher. The 29 under 40 are in `02_low_dr.csv` and `low_dr_pool.csv`.
- Vetting was text-based: homepage plus /blog crawl, scored on real business, blog and clean. The cloud proxy blocked screenshots, so design is not scored. `vetting.csv` has the detail.
- `01_needs_check.csv` (95 rows) was not fully checked. Either the crawl stopped at the Apify cap, or /blog did not return 200 (the blog may live at another path, for example blog.airtable.com or pipeline.zoominfo.com).

Next, on the Mac:
1. `sh skill/mta-backlink-outreach/scripts/sync.sh pull`
2. Optional: run `visual_check.py` on `01_prospects.csv` to add design scores from screenshots.
3. Vet enough of `01_needs_check.csv` to reach 200 (13 more). UAE is thin, so prefer UAE rows.
4. Step 3 link habits (backlinkExchange) for the 200, then write `02_enriched.csv`. Ahrefs units reset 30 Sep.
5. Step 4 article pick, then `03_backlink_targets.csv`.
Campaign name for the ledger: backlink-2026-09-23-b.
