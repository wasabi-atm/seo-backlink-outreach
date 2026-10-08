# Brief: backlink-2026-10-08

- Target: 160 sites at DR 40 or higher, 80 in Segment A and 80 in Segment B. UK and UAE first, then US. Plus a buffer of about 40 carried through Steps 3 and 4 (best 160 kept).
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Scope: through Step 6 (Instantly draft), checkpoints still pause for the user. Contact caps as 7 Oct: Instantly 250 credits, Apollo 20, Apify $1.
- Excluded domains: none given beyond the ledger. Ledger before this run: 1471 rows.

## Progress log

- Sync (8 Oct): checkout equals origin/main (d7a58fd). Interview answered, all defaults.
- Network: cloud proxy blocks company sites (hubspot.com 403), no Chrome in PATH, no .venv, so Apify route again, no screenshots, no video schema check.
- exclude_domains.txt: 3225 root domains (ledger, pool, form master, clients, all earlier batch files incl. 7 Oct). Yesterday's weak spares are excluded too.
- Research (8 Oct): 12 agents (research/RESEARCH_BRIEF.md) returned 101 rows against about 200 targeted (A_UK_AGENCY 5, A_UKUAE_MARTECH 3, A_UK_CREATIVE 3, A_US_AGENCY_E 12, A_US_AGENCY_W 4, A_US_MARTECH 17, A_US_CREATIVE 2, B_UKUAE 3, B_US_PEOPLE 11, B_US_FIN 11, B_US_TECH 17, B_US_VERT 13). Main limit: blog post dates could not be read from the sandbox. dedupe.py check removed 6 (digitalnexa, clickintelligence, torchbox, thedigitalmaze, evolvedsearch already in ledger; impact.com brand-only match with IMPACT, probably a different company). 95 clean: A 40 (UK 6, US 34), B 55 (UK 3, US 52), no UAE. 1 competitor: rotorvideos.com.
- Short of 160: waiting on the user to choose how to close the gap.
- Checkpoint (8 Oct): user chose a second research pass for the gap, and to include rotorvideos.com as a competitor, quote swap only. impact.com stays removed (ledger brand match, no answer given).
- Second pass: 143 unverified DR 40+ leads (research2/leads_new.txt, all NEW) split over 4 agents (research2/BRIEF2.md) to read real post dates with browser crawls, sitemaps and searches.
- impact.com put back (user 8 Oct: keep, different company from IMPACT). 96 clean.
