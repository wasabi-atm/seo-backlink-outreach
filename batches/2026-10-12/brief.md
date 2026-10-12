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
