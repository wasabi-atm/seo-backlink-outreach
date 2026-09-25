# Brief: backlink-2026-09-25

- Target: 150 sites at DR 40 or higher, 75 in Segment A and 75 in Segment B, spread across UK, US and UAE.
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given. The ledger holds 180 companies from backlink-2026-09-23 (40) and backlink-2026-09-23-b (140).
- Tools: Ahrefs has 36 units left until 30 Sep, so DR comes from the free Ahrefs endpoint public-domain-rating-free (0 units). The cloud network policy blocks prospect sites (403 on CONNECT, WebFetch blocked too), so the user chose the Apify route: screenshots via apify/screenshot-url, homepage and blog reads via apify/website-content-crawler (cheerio, shallow), article picks via web search plus reading only the chosen posts. No deep blog crawls.
- Candidate sources: the 95 rows in batches/2026-09-23-b/01_needs_check.csv (DR 40+ on 23 Sep, never vetted because of the Apify cap), plus new candidates. The 47 weak-fit or no-article rows from 2026-09-23-b/03_backlink_targets.csv are not in the ledger and are kept as spares only.

## Progress log

- Candidates: 354 (95 from 2026-09-23-b needs_check, 259 new). Dedupe against the ledger: 0 removed. No overlap with the low-DR pool or past candidate lists.
- DR (free endpoint, 0 units): 315 at 40 or higher. 39 under 40 (kept out of vetting; UAE agencies were mostly low).
- HubSpot: dropped Blink (customer), Pipedrive (open deal), Big Human (open deal). Tillo has an open deal but is under DR 40 anyway. Several others exist as leads with no open deal and stay in.
- Screenshots: apify/screenshot-url works, but the images sit on api.apify.com, which this session cannot open, so design is not scored (same as 2026-09-23-b).
- Acquired or merged, dropped: Search Laboratory (Havas Market), Terminus (DemandScience), RollWorks (AdRoll), Mosaic (HiBob), ClearVoice (Fiverr), Pento (HiBob), Clari (Salesloft), BLASTmedia (PANBlast), Banked (Pay by Bank).
- Rebranded, moved to the new domain (dedupe, DR and HubSpot checked again): tmpb2b.com, teamhighwire.com, instrumental.net, confirm.com, bonusly.com, gladly.ai, scribe.com, zip.com, koto.com, arabaddigital.com, fathom.ai.
- Crawls (Apify website-content-crawler, cheerio): homepages for 312, then 347 blog-index URLs, then 23 fix-up URLs (playwright:adaptive). Raw output and markdown are in crawl/ (not synced). vet2.py scores real business, blog and clean from that text; visualScore is their average. Hard fails: acquired or merged, no blog found, blog inactive (latest post over 18 months old), did not load (bot block), not based in UK/US/UAE (Vadecom, Egypt).
- Farm-word hits on navattic, digitalsilk, bonusly and 5wpr were checked by hand: client case studies and phrases like "betting on", not farm content.
- Competitors: Vyond and Column Five flagged. User chose "Include, quote swap only" for both (25 Sep). Vyond is in the 150; Column Five is a spare.
- Selection (select.py): 75 per segment, UK and UAE filled first because 2026-09-23-b was mostly US. 150 in 01_prospects.csv, 113 spares in 01_spares.csv.
- Checkpoint 1 approved by the user as-is (25 Sep).
- Step 3 (link habits, Apify path since Ahrefs has 36 units): step3_posts.py picks up to 5 recent posts per site from the crawled blog index; 6 cheerio runs read about 670 posts; step3_analyze.py counts distinct outside business domains linked in the post bodies (social, CDN, search and .gov/.edu/.ac links excluded), outside people quoted (job title "at/of" another company) and guest-post or contributor pages. Yes = 10+ domains, 2+ outside companies quoted, or a guest/contributor page; Some = 3-9 domains or 1 company quoted; No = fewer.
- Found during Step 3 and swapped for the next spare in the same bucket: JKR (spam pages on subdomain abi.jkrglobal.com) -> Pearlfisher; Egress (blog now served from blog.knowbe4.com after the KnowBe4 acquisition) -> Sumsub; Alef Education (press releases only, no blog) -> Bayut. The Checkpoint 1 list is kept in step3/01_prospects_checkpoint1.csv.
- 02_low_dr.csv: 38 candidates under DR 40 (Tillo left out: open HubSpot deal). They were never vetted or crawled, so backlinkExchange is blank. Added to low_dr_pool.csv.
- Checkpoint 2 approved by the user (25 Sep).
- Step 4 (article picks): crawl4ai can't reach sites from the cloud, so six parallel agents (step4/STEP4_BRIEF.md, 25 sites each) used web search to find candidate articles and read the chosen pages with Apify website-content-crawler (12 runs, about 330 pages). Every hook comes from the live page text crawled on 25 Sep. merge_step4.py builds 03_backlink_targets.csv: 142 ready (91 strong, 51 ok) and 8 "review: weak fit" (Air, Reflect Digital, Pearlfisher, Mediaworks: thin fit; Six & Flow, LogRocket, Beehive, Pluto: article body did not come through the crawler, so the hook needs a browser check).
- Competitors flagged in Step 4 (they also sell video or motion work): Mediaworks, Reflect Digital, Red Berries, Fifty Five and Five. User chose "Include, quote swap only" for all four.
- Notes for Step 5: hooks that say a page has "no video" or "no image" come from crawled text, which drops iframes and some lazy-loaded media; check those in a browser. Competitor studios already linked on some picked pages (Storylane: Breadnbeyond; Kayako: Levitate Media; Gainsight: Wyzowl; Ceros: BreadnBeyond). CybSafe's article is about Cybersecurity Awareness Month, so send before 1 October. Quill Podcasting links point to cohostpodcasting.com, so check for a rebrand.
