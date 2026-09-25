# Step 5 brief: contacts and emails (backlink-2026-09-25)

Working folder: `/home/user/seo-backlink-outreach/batches/2026-09-25` (BATCH). Repo root: `/home/user/seo-backlink-outreach` (REPO).

Motion The Agency (MTA, motiontheagency.com) is a motion design and explainer video studio run by its founder, Sam Jupp. Each company below has one article picked (Step 4). You will find one contact per company, check them against the outreach ledger, then write one email per company in Sam's voice.

Your input: `BATCH/step5/in_<N>.csv` (25 rows from 03_backlink_targets.csv, plus `wantFounder`). Your outputs: `BATCH/step5/contacts_<N>.csv` and `BATCH/step5/emails_<N>.csv`.

## Part 1: find one contact per company (Apollo)

Load tools with ToolSearch: `select:mcp__Apollo_io__apollo_mixed_people_api_search,mcp__Apollo_io__apollo_people_bulk_match`. Use `_conversation_ref` "bl0925step5" on every Apollo call.

- Who: if `wantFounder` is yes (founder's quote swap or founder's quote), the founder, co-founder or CEO. If the company is large (roughly 500+ staff) or the founder has no email in Apollo, take the most senior content or marketing person instead (CMO, VP or Head of Marketing, Head of Content, Content Marketing Lead or Manager, Editor). If `wantFounder` is no: Head of Content, Content Marketing Lead or Manager, Head of Marketing or CMO, in that order; in a small company the founder is fine.
- Search (free): `apollo_mixed_people_api_search` with `q_organization_domains_list: [webDomain]` and `person_seniorities` (for founders: ["founder","owner","c_suite"]; for marketing: ["c_suite","vp","head","director","manager"]) or `person_titles`. If the domain returns nothing, try once more with `q_keywords` set to the company name. Prefer people with `has_email: true`, based in the UK, US or UAE, and recently refreshed.
- Reveal (costs 1 lead credit each): `apollo_people_bulk_match` with `details: [{"id": <apollo id>}]`, up to 10 per call. Never set reveal_personal_emails, reveal_phone_number or any waterfall option. HARD CAP: at most 33 people revealed in your group. Only reveal people Apollo marks has_email true. If a reveal returns no email or an email on a different company's domain, you may reveal one alternative for that company (still within the cap). If the tool response includes an `mcp_credits` block, note the credits used.
- Check the person still works there (title and organisation in the match result) and the email domain belongs to the company (a parent company or rebrand domain is fine; note it).
- No usable contact: leave the name and email blank and write `no contact found` in contactNote. Never guess an email address.

Write `BATCH/step5/contacts_<N>.csv` with columns: `webDomain, firstName, lastName, jobTitle, email, emailStatus, apolloId, contactNote`, one row per company (all 25).

## Part 2: dedupe against the ledger

Build a CSV with columns `companyName, webDomain, email` for your rows that have an email, and run:

`python3 REPO/skill/mta-backlink-outreach/scripts/dedupe.py check <that file> --ledger REPO/outreach_ledger.csv`

It writes `<file>_clean.csv` and `<file>_duplicates.csv`. Any company in the duplicates file is dropped: do not write an email for it, and record the reason in manualCheck as `dropped by dedupe: <reason>`. Do not edit the ledger.

## Part 3: write the emails

First invoke the Skill tool with skill `anthropic-skills:humanizer` and read its guidance. Every email must go through it before you save: apply its fixes to each email (keep the facts, links and structure).

One email per company, a single step, no follow-ups. The body is HTML so it pastes into Instantly: paragraphs in `<p>...</p>`, links as `<a href="URL">text</a>`, sign-off `<p>Cheers,<br>Sam</p>`.

Shape (reference only; do not copy its facts):

```
<p>Hey Phuong,</p>
<p>Just read your piece <a href="https://www.journeyh.io/blog/content-pillars-b2b-content-marketing-strategy">5 B2B Content Pillars</a>. The table of contents still reads "Text Link" three times, and the page says published 11 June and updated 10 June, so the dates are the wrong way round.</p>
<p>Your third pillar also says to visualise findings through infographics, and the five pillars themselves don't have one.</p>
<p>I run a motion studio. Happy to design them, free, and it would carry across your German version of the page too.</p>
<p>In return, just a credit link back to <a href="http://motiontheagency.com">motiontheagency.com</a>, or we'll pay for placement instead.</p>
<p>Would you be open to exploring this?</p>
<p>Cheers,<br>Sam</p>
```

Rules:
- Open with `Hey {firstName},` then the article, linked by its title: `<a href="{articleUrl}">{articleTitle}</a>`. If the title contains square brackets or quotes, keep it readable in the link text.
- Then one or two specific things from articleHook. These were read from the live page on 25 Sep 2026. Keep exact quoted words where the hook quotes them. Do not add facts that are not in articleHook, linkPlacement or notes. If notes say a point needs a browser check (for example "no video in the crawl", "may load by script"), leave that point out of the email or phrase it so it stays true, and put it in manualCheck.
- Tone for mistakes: helpful, not smug ("small thing, but...").
- The offer, in one line, tied to the page (use linkPlacement to name the section):
  - `Founder's quote swap` (all Segment A): both founders give a quote for each other's article, and both link back. For example: "Happy to swap founder quotes: one from me for this piece, and one from you for ours." If your contact is not the founder, say "one from your side for ours".
  - Rows with competitorDecision `include` (they also make video, animation or video tools): never offer to make a video, animation or graphic for them. Say it plainly as context, for example "We're both in the video space, so a quote swap could work well for both of us."
  - `Video for the blog post`: a short explainer video for that section, free.
  - `Blog graphic or infographic`: a graphic or infographic for that section, free.
  - `Founder's quote`: Sam gives a quote for the piece.
  - `Internal data`: figures from MTA client projects they can cite. Keep it generic and never invent numbers.
- Then the link ask: "In return, just a credit link back to <a href="http://motiontheagency.com">motiontheagency.com</a>, or we'll pay for placement instead." For a quote swap the link is mutual, so phrase it to fit, for example "a credit link back to motiontheagency.com with my quote, and one to yours with your quote on ours, or we'll pay for placement instead."
- End with `<p>Would you be open to exploring this?</p>` then `<p>Cheers,<br>Sam</p>`.
- Under 110 words in the body, not counting the sign-off. British spelling (optimise, colour, organisation). No em dashes or en dashes anywhere. Never ask for a call or meeting. No flattery, no "I hope this finds you well".
- emailSubject: short, lower case, names their article, for example "your content pillars piece" or "the onboarding videos post".

Write `BATCH/step5/emails_<N>.csv` with columns exactly:
`companyName, webDomain, country, segment, offer, firstName, lastName, jobTitle, email, emailStatus, articleTitle, articleUrl, linkPlacement, articleHook, emailSubject, emailBody, manualCheck, contactNote`

One row per company in your input (all 25). Rows with no contact or dropped by dedupe keep the company fields, leave emailSubject and emailBody blank, and say why in manualCheck. Also use manualCheck for: weak fit rows (fit is weak), hooks that need a browser check, founder not reached for a quote swap, contact domain differs from webDomain, and anything else a human should look at before sending. Leave it blank when nothing needs checking.

Use python's csv module. Check with a script that no field contains an em or en dash and that every body is under 110 words (strip the HTML and the sign-off before counting).

Do not edit any other file, do not touch the ledger, do not commit.

## When you finish

Reply with: Apollo credits used (reveals made), contacts found, companies with no contact, companies dropped by dedupe, and the manualCheck rows with a one-line reason each.
