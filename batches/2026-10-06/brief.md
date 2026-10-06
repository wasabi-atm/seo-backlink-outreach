# Brief: backlink-2026-10-06

- Target: 160 sites at DR 40 or higher, 80 in Segment A and 80 in Segment B. UK and UAE first, then US.
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given beyond the ledger. Ledger before this run: 1108 rows (backlink-2026-09-23 to -10-05, plus backlinkform-2026-10-05).

## Progress log

- Sync (6 Oct): session branch already equal to main (ac58e6d), so the ledger is current. Repo SKILL.md followed.
- Interview answered (6 Oct): all defaults as above, all four Segment B offers allowed.
- Network: the cloud proxy blocks company sites (curl and WebFetch both refused), so the Apify route again: no screenshots (no design score) and no Step 2c video schema check, videoSchemaGap blank. Apify usage this cycle: $4.06 of $60.
- exclude_domains.txt: 2839 root domains (ledger, low-DR pool, form outreach master, client lists, every earlier batch file).
- Research (6 Oct): eight agents (research/RESEARCH_BRIEF.md, check_domains.py against exclude_domains.txt). Rows: A_UKUAE 32, A_US_AGENCY 35, A_US_MARTECH 38, A_US_CREATIVE 27, B_UKUAE 40, B_US_PEOPLE 34, B_US_FIN 35, B_US_TECH 35 (276). Spares lists in research/spares_*.txt. Apify about $1.30 in total across the agents.
- merge_research.py: 274 rows after 2 in-batch repeats (bluetext.com, cognitoforms.com). dedupe.py check: 273 clean, 1 removed (SEO Inc, seoinc.com: name match to SEO.co, likely a different company, ask at Checkpoint 1). A 31, A_UAE 1, A_US 99; B_UK 39, B_UAE 1, B_US 103. UAE pool nearly empty.
- HubSpot (search_crm_objects by domain, all 273): Teleport (goteleport.com) has an open deal, dropped. Leads with no deals, kept and noted: HockeyStack, Crunch, Krisp, Impartner, Joblogic (step2/hubspot_check.csv).
- Vetting: Apify cheerio homepage scan (step2/pageFunction.js), vetting_1.csv (214) and vetting_2.csv (58).
- Vetting done (Apify about $0.05 for both scans). Hard fails (01_dropped.csv): no load after normal and residential retries (bruceclay, bitmovin, buildertrend, ebiquity, lullabot, mhpgroup, fatbeehive), ad networks (doubleclick: terakeet, patriotsoftware, terryberry, digitalauthority, staxpayments, wordbank; AdSense: artversion), alcumus.com (site says no longer available). Plus Teleport (HubSpot open deal). harmonicinc.com moved to Segment B (homepage now broadband only).
- Competitors (user, 6 Oct): all 8 flagged sites included, quote swap only: niftymarketing, bluetext, abstraktmg, thriveagency, visla.us, trypencil, whalar, bravebison. Brave Bison owns Builtvisible (form outreach queued 5 Oct); user still chose include.
- select.py: 160 in 01_prospects.csv, A 80 (UK 27, UAE 1, US 52), B 80 (UK 38, UAE 1, US 41); UK and UAE first, then newest post, then DR. 97 US spares in 01_spares.csv (A 39, B 58). DR 40 to 93, median 66.
- Ahrefs: 196,762 of 200,000 units used until 30 Oct (about 3,200 left), so Step 3 link habits will use the Apify fallback (outbound domains in recent posts); DR from the free endpoint.
- Checkpoint 1: waiting on the user.
- Checkpoint 1 approved by the user (6 Oct): all 160 as is. Carry the 40 best spares (20 A, 20 B) through Steps 3 and 4 as a buffer, then keep the best 160 targets. Ad-tag drops stay out. SEO Inc (seoinc.com) is a different company from SEO.co: add it to the spares pool (dedupe.py log will not add it as its own ledger row, as with seo.co on 5 Oct).
- Step 3 done (6 Oct): five agents (step3/STEP3_BRIEF.md), Apify cheerio only: blog index (step3/indexFunction.js), then 4 recent posts per site (step3/postFunction.js, fixed as postFunction_v2.js for co.uk roots and empty bodies; affected rows re-read and noted). DR kept from the free Ahrefs endpoint (checked 6 Oct during research); no paid Ahrefs units used. Apify about $0.40 for all five chunks.
- backlinkExchange rule on the Apify path: Yes = 8+ distinct outside domains in the posts read, or a contributor/guest page, or a post quoting an outside founder or exec; Some = 3 to 7 or one weak sign; No = 0 to 2.
- Results, 200 rows, all DR 40 to 93 (02_enriched.csv, 02_low_dr.csv empty, nothing to pool): main 160 = Yes 51, Some 56, No 50, unchecked 3 (whalar, drip, iomart: script-rendered or blocked); buffer 40 = Yes 15, Some 10, No 15. recentPosts (up to 12 per site) kept for Step 4.
- Checkpoint 2: waiting on the user.
- Checkpoint 2 approved by the user (6 Oct): all 200 go to Step 4; keep the best 160 after it (fit first, then link habits, 80 per segment).
- Step 4 done (6 Oct): five agents (step4/STEP4_BRIEF.md), Apify cheerio and website-content-crawler, about 430 article pages in total, hooks from today's live crawl. 200 rows: strong 89+, ok, weak 22, dead 0.
- merge_step4.py: best 160 in 03_backlink_targets.csv, A 80 (UK 25, UAE 1, US 54), B 80 (UK 34, UAE 1, US 45). Fit strong 89, ok 71, no weak. Links Yes 61, Some 56, No 42, unchecked 1. 131 from the original list, 29 from the buffer. Offers: Founder's quote swap 81 (all A plus Stability AI), Video for the blog post 44, Blog graphic or infographic 29, Founder's quote 6. 03_spares.csv holds the other 40 (22 weak, 18 ok with No links; Bluetext and Whalar among them). 03_dropped.csv empty.
- Flags for Step 5: 9 articles first published before Oct 2024 (all updated since), 12 with no readable date. Hooks to check in a browser: freshconsulting (leftover AI assistant line), securenvoy (editing note), babelquest (placeholder copy), tive (Webflow placeholder), slcyber (lorem ipsum, may be hidden), stability.ai, yugabyte, webershandwick, cobalt, thanksben, crunch. wpengine's post already cites Wyzowl. Video sellers kept on quote swap: equinetmedia, gorilla76, gofishdigital, mindstamp, vidizmo plus the 6 approved competitors in the list.
- Step 4 sent to the user. Step 5 only when the user asks.
- Step 5 requested by the user (6 Oct, "continue"). Caps (user): Instantly 250 credits (598 available), Apollo 50 lead credits (54 left until 10 Oct), Apify $1. Subjects: the user's four templates mixed (quick question about your X piece / noticed something in your X article / Quick intro, name? / ASAP: need your response on your X piece!!), one per row, no fresh data line (no Internal data rows).
- Contacts: two agents (step5/CONTACTS_BRIEF.md), 80 companies each (targets_0/1.csv), half the caps each, own Instantly lists "Backlink 2026-10-06 contacts 0/1".
