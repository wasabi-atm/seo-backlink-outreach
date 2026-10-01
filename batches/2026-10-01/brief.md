# Brief: backlink-2026-10-01

- Target: 150 sites at DR 40 or higher, 75 in Segment A and 75 in Segment B. UK and UAE first, then US.
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given. Ledger before this run: 769 rows (backlink-2026-09-23 to -30).

## Progress log

- Sync pull done (main 6464efd). Repo SKILL.md differs from the claude.ai copy, so the repo version is followed.
- Tools: the cloud network blocks prospect sites (403 on hubspot.com, hallam.agency, wistia.com), so this run follows the Apify route like 28 to 30 Sep. No screenshots, so no design score; Step 2c (video schema) skipped, videoSchemaGap left blank. Ahrefs has about 118k units until 30 Oct.
- Spares: the vetted spares from 28 to 30 Sep are used up, so all candidates are new research. exclude_domains.txt lists the 2,340 domains already contacted or researched.
- Candidate research (1 Oct): six agents (research/RESEARCH_BRIEF.md), slices A_UK 55, A_UAE 30, A_US 35, B_UK 55, B_UAE 30, B_US 35. Each checks HQ, DR 40+ on the free endpoint and a dated blog post since Oct 2025.
- Research done so far: B_US 38, A_US 36, B_UK 55. Spare UK B names with DR and dates confirmed (not in the file): krystal.io, ans.co.uk, 6dg.co.uk, quartix.com, fleetcheck.co.uk, achilles.com, workspace.co.uk, homeflow.co.uk, kortext.com, century.tech, cpoms.co.uk, unifrog.org, sparx-learning.com, pandle.com, takepayments.com, fleximize.com, natterbox.com, croner.co.uk, landlordvision.co.uk, signable.com, boxphish.com, performanta.com, redflagalert.com, matillion.com. US spares: osano, numeric, expel, canopy, guru. clay.com held out (brand match with clay.global), ask the user.
- A_UK done: 62 rows. Check: Webgains HQ (German parent), WPP is a holding company. Velstar, Toward, adam&eveTBWA recorded on their new domains.
- B_UAE done: 19 rows (UAE DR 40+ B2B pool mostly used up). 8 are Dubai real estate brokerages (B2C lean): ask the user. Check HQ: First Bit, REIDIN. DTS Solution acquired by Beyon Cyber, domain live.
- A_UAE done: 21 rows. Total 230 candidates (A 119, B 111). commonroom.io was in two slices, kept once.
- Dedupe of 00_candidates.csv: 230 clean, 0 removed. HubSpot by domain: no customers or open deals. Tavus, Zeno Group, Search Atlas and causaLens are leads with no deal and stay in.
- Vetting: Apify cheerio-scraper homepage scan of all 230 (ad scripts, farm words, write-for-us, redirects), about $0.10. 225 loaded. Hard fails: Improvado (Taboola script), Luxhabitat (DoubleClick, consumer portal), Yaspa (casino and sportsbook payments). "cbd" hits are inside page code and ignored. Make (makeagency.co.uk) has a betting/sportsbook hit, likely a client, check at Step 4.
- Competitor answers (1 Oct): Rewind Productions and Animation Studio: include, quote swap only. Dubai brokerages: user dropped all 8 (fill with US B2B). clay.com: user confirmed a different company from clay.global, added as a candidate.
- Selection (select.py): 150 in 01_prospects.csv. A 75 (UK 58, UAE 17); B 75 (UK 54, UAE 11, US 10). Ranked UK and UAE first, then newest post, then DR. 146 of 150 have a dated post since Oct 2025 (4 UAE B rows without a visible date). 71 spares in 01_spares.csv (63 US). 01_dropped.csv holds the 3 hard fails and 7 brokerages.
- Checkpoint 1: waiting on the user.
- Checkpoint 1 approved by the user (1 Oct). Step 3 started: four agents check DR (site-explorer-domain-rating) and outbound linked domains in Ahrefs (step3/STEP3_BRIEF.md).
- Step 3 done (1 Oct, Ahrefs paid endpoints, about 33k units, no sign-outs): all 150 at DR 40 to 86, so 02_low_dr.csv is empty and nothing goes to the pool. 120 Yes, 16 Some, 14 No, 0 unchecked. Ahrefs returned no outbound links at all for Mother, venturethree and Grizzly ("No" is missing data). Mirriad links to about 75 spam or Ukrainian local news domains (possibly injected links); Jadu shows a few spam domains too. Tango's own site now points to tango.ai (counted there).
- Checkpoint 2: waiting on the user.
- Checkpoint 2 approved by the user (1 Oct), all 150 kept (Mirriad stays; Step 4 checks for spam links). Step 4 started: five agents pick one article and hook per company via Apify cheerio (crawl4ai cannot reach sites from the cloud; the user agreed to the Apify route at Checkpoint 2). step4/STEP4_BRIEF.md.
- Step 4 group 0: 14 strong, 10 ok, 6 weak (Dalziel & Pow, Mirriad (RNS lists intention to appoint administrators, Apr 2026), Social Chain, adam&eveTBWA, Saatchi & Saatchi, Holistic AI). Cake is a Shopify agency; Igloo sells video production (kept to quote).
