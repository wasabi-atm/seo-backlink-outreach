# Brief: backlink-2026-10-09-b2 (batch 2 of 4)

- Same brief as backlink-2026-10-09 (batch 1): Segment A quote swap, Segment B video / founder's quote / internal data / graphic, sender Sam, paid placement offered, 20 A / 20 B target, UK and UAE first, DR 40 or higher.
- User approved batch 2 on 9 Oct after dropping the 3 held rows of batch 1 (triplewhale, audiomob, lancedb marked not_sent).
- Batch 1 yield: 52 candidates, 50 vetted, 41 usable, 38 emails. Main limits: dated blogs and UK/UAE supply. For batch 2, a rescue slice re-checks domains dropped in batch 1 research only because their blogs are script-rendered.
- Ledger before this run: 1663 rows.

## Progress log

- Research started (9 Oct): 7 agents (RESCUE, A_UK_AGENCY, A_US_AGENCY, A_MARTECH, B_UKUAE, B_US_PEOPLE_FIN, B_US_TECH_VERT) with the script-rendered blog method. Exclude list 3428 domains.
- Step 2b vetting (9 Oct): no screenshots possible. One Apify cheerio run on 52 homepages (51 loaded; constantcontact.com blocked). No parked sites, no redirects off-domain. Doubleclick: kixie.com, codesignal.com, okteto.com. Farm word betting: motherduck.com. Possible link vendors: thehoth.com, respona.com. Possible competitors: idomoo.com, nowsourcing.com. HubSpot: only lupl.com (lead, no deal). 01_prospects_proposed.csv holds the status per row. Checkpoint 1: waiting on the user.
- Checkpoint 1 answers (9 Oct): include idomoo.com and nowsourcing.com as quote swap only; keep the Hoth and Respona; keep kixie, codesignal, okteto, motherduck. 01_prospects.csv = 52 rows. Step 3: DR rechecked with the free Ahrefs tool, all 52 are 40 or higher; five agents (step3/STEP3_BRIEF.md) read posts for backlinkExchange.
- Step 3 done (9 Oct): five agents, 52 rows, 02_enriched.csv (all DR 40+), 02_low_dr.csv empty. Checkpoint 2: waiting on the user.
- Step 3 approved by the user (9 Oct): run Step 4 on all 52. Step 4 started: five agents (step4/STEP4_BRIEF.md), Apify, one article per company with a hook.
- Step 4 done (9 Oct): five agents, 52 rows. merge_step4.py -> 03_backlink_targets.csv (strong 19, ok 23, weak 10, dead 0). Step 5 only when the user asks.
- Step 5 requested by the user (9 Oct) on the 42 strong and ok rows (targets_42.csv); the 10 weak rows are held in 03_held_weak.csv, not contacted. Subject style: the user's four templates as batch 1 (to reconfirm).
- Step 5 contacts done (9 Oct): Instantly SuperSearch three passes (list "backlink-2026-10-09-b2 contacts"; balance 110.8 before, 84.8 after the first two passes), Apollo 0 lead credits left (resets 10 Oct) so not used, Apify leads scraper not used, company-site emails via cheerio (hello@lupl.com taken; support@ and sales@ inboxes at kixie, qventus and dynamicplanner skipped as poor targets). 35 of 42 have an email (34 instantly, 1 website). No email: zype.com, thehoth.com, kixie.com, sigmacomputing.com, dynamicplanner.com, phreesia.com, qventus.com (step5/no_contact.csv). dedupe.py check: 0 removed.
- Correction (9 Oct): batch 1 Instantly credit use was about 80 (190.8 to 110.8), not about 31 as reported earlier.
- Emails: four agents (step5/STEP5_BRIEF.md) writing; Instantly campaign check by a background agent (step5/campaign_check.csv). Subjects: the user's four templates, as in batch 1.
- Emails done (9 Oct): four agents wrote 35 emails, assemble.py -> 04_backlink_emails.csv (the user's four subject templates: 9 quick_question, 9 noticed_something, 9 quick_intro, 8 asap). Checks: no dashes, no braces, all under 110 words, article link, ask and paid placement in every body, no duplicate subjects. 27 of 35 carry a manualCheck. Logged under backlink-2026-10-09-b2 (35 queued).
- Campaign check (9 Oct, re-verified directly for the 7): sam.lulla@constantcontact.com, ashleigh.cook@rainfocus.com, saldworth@augury.com, maxim@temporal.io, howard.brown@revenue.io, ryan@motherduck.com and dan@linearb.io are already in other Instantly campaigns. The user chose to drop all 7 (marked not_sent, ledger: queued 28, not_sent 7).
- Step 6 done (9 Oct): draft campaign "9 October 2026 (Batch 2) - Backlink Cold Outreach Campaign" (4d1f55db-3af3-4a1b-be61-9fca21171593), status draft, no senders, not activated; 28 leads added and compared with 04_backlink_emails.csv (0 mismatches). Batch 2 of 4 ends at 28 sendable emails.
- Credits (9 Oct): Instantly 110.8 before batch 2, 63.8 after (47 used; batch 1 used 80; total 127 of 190.8). Apollo 0 lead credits left (resets 10 Oct). Apify about $1 across batch 2.
