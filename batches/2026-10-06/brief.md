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
