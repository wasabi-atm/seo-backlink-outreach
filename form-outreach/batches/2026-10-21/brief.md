# Form outreach brief, 2026-10-21 (daily scheduled run)

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

- Step 0: the 2026-10-20 canvas (F0CBE7C43EC) has no ticked boxes (0 of 50), so nothing was marked sent. Template checked against the newest Instantly backlink campaign, "20 Oct Backlink Cold Outreach" (90 leads read, all already in the ledger as backlink-2026-10-20). Shared lines unchanged (greeting, "I run a motion studio", "Would you be open to exploring this?", "Cheers, Sam"). One wording change: the live quote swap credit line reads "In return, a credit link back to motiontheagency.com with my quote, and one to yours with yours, or we'll pay for placement instead." (the skill file says "with your quote on ours"). The forms follow the live campaign.
- Reading pages: the built-in browser was used (read only), as the task prompt said. No form was typed into or submitted, no CAPTCHA touched, no account created.
- Leftovers: none available. Every not_sent ledger row with DR 40+ in the target countries has already been tried in an earlier form batch.
- Candidates: 336 new names in round 1 (196 at DR 40+ on the free Ahrefs screen, 135 under 40, 4 already in the ledger) and 160 in round 2 (133 at DR 40+, 26 under 40, 1 dropped as not a company site). 329 sites researched in the built-in browser. 93 passed the form and article checks; 25 were left out as unsure and 18 held as spares (all in 07_left_out.csv with competitors).
- Round 2 workers stopped partway when the account's weekly usage limit was hit; they were restarted after it reset and finished every row.
- DR: Ahrefs API had 19 units left this month (needs about 1,000), so DR was checked today with Apify radeance/ahrefs-scraper for 68 domains (all 40+), about $0.68. A first run with default options returned nothing (about $0.001). Cost: 0 Ahrefs units.
- HubSpot: none of the 50 domains (or their old domains) is a company in the CRM.
- After the canvas went out, the pull before the push brought in today's email batch (backlink-2026-10-21, logged on another device). Simple Strat (simplestrat.com) was in both, so it was set to not_sent in this campaign, removed from the master list and marked "removed, do not submit" in the canvas. 49 forms remain.
- The same pull brought in a skill change merged at 12:18 UTC today (PR #40): DR 60+ and articles with video, explainer, animation, demo or sales enablement in the title or URL. This batch was built to the rules pulled at the start of the run and stated in the task (DR 40+, broader topics). Only 7 rows meet the new rule: Webspec Design, SeedProd, TrueCoach, Smartzer, The Seventh Sense, MemberPress, PT Distinction. Flagged in the canvas and Slack for a decision.
- Also seen: yesterday's form batch (backlinkform-2026-10-20, 50 rows) is in form_outreach_master.csv but not in outreach_ledger.csv, so email batches do not see it. 3 of those domains were already in the 10-19 and 10-20 email campaigns. Not changed by this run.
