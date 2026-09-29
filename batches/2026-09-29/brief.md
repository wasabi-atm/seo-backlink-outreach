# Brief: backlink-2026-09-29

- Target: 150 sites at DR 40 or higher, 75 in Segment A and 75 in Segment B. UK and UAE first, then US (the ledger is already US-heavy).
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given. Ledger before this run: 480 rows (backlink-2026-09-23, -23-b, -25, -28).
- Still skipped: the 178 Video SEO companies from 2026-09-25-video-seo (none are in the spares).
- Tools: the cloud network blocks prospect sites again (403 on hubspot.com and hallam.agency), so this run follows the 28 Sep Apify route. Design is not re-scored and Step 2c (video schema) is skipped, videoSchemaGap left blank.
- Candidate source: the 302 spares from 2026-09-28/01_spares.csv, vetted and DR-checked (free endpoint) on 28 Sep. No new research needed.

## Progress log

- Dedupe of the 302 spares: 1 removed, The Writer (thewriter.com) matching Writer (writer.com). The user confirmed on 28 Sep that it is a different company, so it stays a candidate.
- Competitor answers (29 Sep): include, quote swap only: Prohibition, ProfileTree, TEAM LEWIS, Socially Powerful, Our Own Brand, One Agency, Disrupt, Influencer, Radley Yeldar (Column Five keeps its 25 Sep include). Exclude for good, logged in the ledger as excluded: The Social Shepherd, NeoMam Studios, Definition.
- Selection: 150 picked, A 75 UK; B 16 UAE (all UAE B spares) and 59 UK. The spares have no UAE Segment A and no US row outranked UK. Ranked by blog dates in the last 12 months, then score, then DR. 94 of 150 have dated posts in the last 12 months. 8 included competitors made the cut (Radley Yeldar and Column Five sit in spares).
- Presight dropped (same G42 group as Core42), replaced by the next UK Segment B spare, Arbor Education (arbor-education.com, DR 69, score 4.3).
- HubSpot by domain: no customers or open deals. Shop Circle, Fourth, Attio and Juro are leads with no deal and stay in.
- Checkpoint 1: waiting on the user.
- Checkpoint 1 approved by the user (29 Sep).
- Step 3 (link habits, Apify path; Ahrefs has 36 units until 30 Sep): six agents crawled the 150 blog indexes and up to 5 recent posts each (apify/website-content-crawler), then two retry agents covered the 36 sites the first pass could not read (cheerio-scraper link extraction, sitemaps, htmlTransformer none). step3_merge.py applies the 28 Sep rules (Yes = 10+ outside business domains, 2+ outside companies quoted, or guest signs; Some = 3-9 domains or 1 company quoted; No = fewer).
- Result: 50 Yes, 38 Some, 56 No, 6 not checked (Show + Tell: article text not in the page; Eastside Co: blocks Apify's proxy; Little Warden: no blog; Talentera: gated library only; Letswork: index times out; Saal.ai: broken insights page).
- Dead or stale blogs found: GBM (2021), Okadoc (2021), Pyypl (2024), Gleanin (Feb 2023), Turner Duckworth (news only, Jul 2025), TEAM LEWIS, Monite, TASC, Reason Digital, Airfinity, Robin AI, Shop Circle, Authoritas and Lumen Research (last post Sep to Dec 2025).
- Maquae: the Step 3 agent read it as a digital marketing agency (PPC, SEO, AI development); on 28 Sep it was moved to Segment B as a software development company. Asked the user.
- 02_enriched.csv: all 150 at DR 40 to 84 (28 Sep free endpoint). 02_low_dr.csv is empty: no new candidates were researched, so nothing was added to the pool.
- Checkpoint 2 (user, 29 Sep): option 1. Dropped the 6 unreadable and 5 dead-blog sites (Show + Tell, Eastside Co, Little Warden, Gleanin, Turner Duckworth; Talentera, Letswork, Saal.ai, GBM, Okadoc, Pyypl), moved to 01_spares.csv with a note, not logged. Kept the 9 stale blogs. Maquae moved to Segment A (digital marketing agency, founder's quote swap).
- Replacements needed: 4 Segment A and 7 Segment B. No UAE spares and no spares with dated posts were left, so the next 8 UK A and 14 UK B spares by score and DR go through the Step 3 link check (group 7), and the first 4 A and 7 B with live, readable blogs join the list.
- Group 7 link check (22 UK spares): picked in rank order with a live, readable blog: A Varn, Pi Datametrics, Celebrus, StreamAMG; B Zego, Aurora Energy Research, SeedLegals, Quantexa, Proactis, Oleeo, Bulb. Opteo skipped (blog dead since 2021). Dedupe of the final 150 against the ledger: clean.
- Final Step 3 list: 150 (A 75: 74 UK, 1 UAE (Maquae); B 75: 67 UK, 8 UAE). 49 Yes, 43 Some, 58 No, none unchecked. 02_enriched.csv rebuilt.
