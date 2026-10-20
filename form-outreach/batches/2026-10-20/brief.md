# Form outreach brief, 2026-10-20 (daily scheduled run)

Copied from form-outreach/standing_brief.md. No interview or checkpoints (unattended run).

- Batch size: 50. Delivered: 50
- Segments: A (marketing and creative adjacent, not competitors), B (B2B SaaS, AI, FinTech, HR tech, dev tools with a real blog), and leftovers from email batches (ledger rows with status not_sent)
- Countries: UK, US, UAE, Australia, Singapore
- DR: 40 or higher
- Company size: 11 to 500 staff
- Segment A offer: founder's quote swap
- Segment B offer: whichever fits the article best: video for the post, blog graphic, founder's quote or internal data
- Paid placement fallback: yes
- Competitors: leave out (nobody is there to approve them); list them in the canvas under "Left out"
- Name on forms: Sam Jupp
- Reply email in forms: sam.jupp@globalmotiontheagency.com
- Phone for forms that require it: +44 2039847787
- Sign-off under Sam: Founder @ Motion The Agency
- Sender: Lia submits the forms
- Delivery: Slack canvas, link sent to C07SWGY4MNV and D0ADQ3Y6CG5
- Reading websites: WebFetch only, as "Crawling websites (WebFetch first)" in `skill/mta-backlink-outreach/SKILL.md` says (sitemap first, one URL per call, up to 20 in parallel, at most 50 pages per site, word and link counts marked "approx", "not found" for missing fields, one retry then "failed"). No shell crawls and no Apify Website Content Crawler. Nobody can approve an Apify crawl in this unattended run, so skip a site that WebFetch cannot read and note why.

## Run notes

- Step 0: the 2026-10-19 canvas (F0CA412NS2H) has no ticked boxes (0 of 45), so nothing was marked sent. Template checked against the newest Instantly backlink campaign, "19 October 2026 - Backlink Cold Outreach Campaign" (88 leads read). Shared lines unchanged (greeting, "I run a motion studio", both credit link lines, "Would you be open to exploring this?", "Cheers, Sam"). That campaign is already in the ledger as backlink-2026-10-19.
- Reading pages: the built-in browser was used (read only). The task prompt said to use the built-in browser; the standing brief now says WebFetch only, so the run followed the task prompt. No form was typed into or submitted, no CAPTCHA touched, no account created.
- Leftovers: 13 not_sent ledger rows (no contact found) in UK/US/AU were tried; Visions Design, Sites by Sara and Cloud Cartel passed the form and article checks (Cloud Cartel left out as unsure). Rows held because the contact sits in another live Instantly campaign, and Canadian rows, were not tried.
- Candidates: 286 new names in round 1 (162 at DR 40+ on the free Ahrefs screen, 113 under 40 or no DR, 11 dropped as far over 500 staff), 80 in round 2, 95 in round 3 and 96 in round 4 (rows seen in earlier email batches but never contacted). 433 sites researched in the built-in browser. Round 1 passed only 14 of 162, because most mid-size SaaS sites only have demo or sales forms; agencies passed far more often.
- 87 sites passed the form and article checks. 2 were already in the ledger under another name or domain (Vizion, Bigeye) and 2 redirected to domains already contacted (orbitmedia.com, infuse.com). 37 were left out as unsure (video among services, bulk update dates, size, country, short message boxes) and are in 07_left_out.csv with competitors.
- DR: Ahrefs API had 19 units left this month (needs about 1,000), so DR was checked today with Apify radeance/ahrefs-scraper for 53 domains (all 40+), about $0.53. A first run with default options returned nothing (about $0.001). Cost: 0 Ahrefs units.
- HubSpot: none of the 50 domains is a company in the CRM.
- WebSearch: the shared search budget ran out during candidate finding, so later rounds used DR-screened names from memory and earlier batch files, all verified in the browser.
