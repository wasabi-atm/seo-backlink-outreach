# Step 5 brief: emails (backlink-2026-10-05)

Working folder: `/home/user/seo-backlink-outreach/batches/2026-10-05` (BATCH). Repo root: `/home/user/seo-backlink-outreach` (REPO).

Motion The Agency (MTA, motiontheagency.com) is a motion design and explainer video studio run by its founder, Sam Jupp. Each company below has one article picked (Step 4) and one contact already found and checked against the ledger. You write one email per company in Sam's voice. You do not look for contacts and you do not spend any credits.

Your input: `BATCH/step5/in_<N>.csv` (about 17 rows). Your output: `BATCH/step5/emails_<N>.csv`.

Input columns: companyName, webDomain, country, segment, offer, competitorDecision, firstName, lastName, jobTitle, email, emailType, contactIsFounder, articleTitle, articleUrl, articleDate, articlePublished, linkPlacement, articleHook, fit, notes, instantlyCampaign.

## Before writing

Invoke the Skill tool with skill `anthropic-skills:humanizer` and read its guidance. Every email must go through it before you save: apply its fixes to each email (keep the facts, links and structure).

The article pages are not saved on disk and the live sites are blocked from this machine. Work only from articleHook, linkPlacement and notes; do not use WebSearch or WebFetch, and do not re-crawl.

## Writing the email

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
- Greeting: `Hey {firstName},`. If emailType is `generic` (a shared inbox, no name), use `Hey {companyName} team,`.
- Then the article, linked by its title: `<a href="{articleUrl}">{articleTitle}</a>`. If the title has square brackets or odd quotes, keep the link text readable.
- Then one or two specific things from articleHook. These were read from the live page through an Apify crawl on 5 Oct 2026. Keep exact quoted words where the hook quotes them. Do not add facts that are not in articleHook, linkPlacement or notes. If notes say a point needs a browser check (for example "may load by script", "not in the crawl"), leave that point out or phrase it so it stays true, and put it in manualCheck.
- Tone for mistakes: helpful, not smug ("small thing, but...").
- No video schema lines in this batch (videoSchemaGap is blank for every row).
- If notes say the page already has a video (YouTube, Vimeo, Wistia or a video tag), never say the page has no video.
- Never copy a double curly brace tag such as {{quote1}} into a subject or body: Instantly reads it as a merge tag. Describe it instead, for example: the tag "quote1" in double curly brackets.
- If a hook rests on outside knowledge rather than the page (notes say so), leave that point out and use another from the hook, or put it in manualCheck.
- The offer, in one line, tied to the page (use linkPlacement to name the section):
  - `Founder's quote swap` (all Segment A): both founders give a quote for each other's article, and both link back. For example: "Happy to swap founder quotes: one from me for this piece, and one from you for ours." If contactIsFounder is `no`, say "one from your side for ours" and add `founder not reached` to manualCheck.
  - Rows with competitorDecision `include` or starting `flagged` (they also make video, animation or video tools): only the founder's quote swap, and never offer to make a video, animation or graphic for them. Do not pitch "I run a motion studio" as a service; say it plainly as context, for example "We're both in the video space, so a quote swap could work well for both of us." For `flagged` rows also put `competitor flagged in Step 4, waiting on the user` in manualCheck.
  - `Video for the blog post`: a short explainer video for that section, free.
  - `Blog graphic or infographic`: a graphic or infographic for that section, free.
  - `Founder's quote`: Sam gives a quote for the piece, free.
  - `Internal data`: figures from MTA client projects they can cite. Keep it generic and never invent numbers.
- "I run a motion studio" (or similar) introduces Sam once, before the offer. For a founder's quote swap, "I run a motion studio" works too, since it says who the quote comes from.
- Then the link ask: "In return, just a credit link back to <a href="http://motiontheagency.com">motiontheagency.com</a>, or we'll pay for placement instead." For a quote swap the link is mutual, so phrase it to fit, for example "a credit link back to motiontheagency.com with my quote, and one to yours with your quote on ours, or we'll pay for placement instead." Always keep the paid placement option.
- End with `<p>Would you be open to exploring this?</p>` then `<p>Cheers,<br>Sam</p>`.
- Under 110 words in the body, not counting the sign-off. British spelling (optimise, colour, organisation, visualise). No em dashes or en dashes anywhere, in any field. Never ask for a call or meeting. No flattery, no "I hope this finds you well", no "I came across".
- Subjects: do NOT write subjects. Leave emailSubject blank; the subject is assigned afterwards from the user's templates (quick question about your X, noticed something in your X article, Quick intro, name?, ASAP: need your response on your X piece). Instead write `articleShortName`: 2 to 5 words, lower case (brands and acronyms keep capitals), naming the article the way a person would say it, for example "sportswear brands" or "buying group" or "GEO". It must fit after "your" and before "piece" or "article" ("quick question about your {articleShortName} piece"). No dashes, no merge-tag braces.
- Because "noticed something in your X article" is one possible subject, the first two lines of every body must open with the article and one specific, true detail from articleHook, so any of those subjects is paid off. Never open with the offer.

## Extra rules for this batch

- If instantlyCampaign is not blank, still write the email, but put `already in Instantly campaign: <name>` in manualCheck.
- A contact email on a different domain from the company website is fine (parent or rebrand domain); do not comment on it in the email.
- Sender is Sam. Offer paid placement as in the shape above.
- Rows with emailType `generic` use `Hey <companyName> team,`.
- Articles whose articleDate is blank: never state a date. Never say a page has no video, graphic or chart unless articleHook says it was confirmed in the raw HTML.

## Output

Write `BATCH/step5/emails_<N>.csv` with columns exactly:
`webDomain, emailSubject, articleShortName, emailBody, manualCheck`

One row per company in your input (all of them). Every input row has an email. Use manualCheck also for: weak fit rows (fit is weak), hooks that need a browser check, founder not reached for a quote swap, and anything else a human should look at before sending. Leave it blank when nothing needs checking.

Use python's csv module. Check with a script that no field contains an em or en dash (U+2014, U+2013) and that every body is under 110 words (strip the HTML and the sign-off before counting), and that articleShortName is filled for every row.

Do not edit any other file, do not touch the ledger, do not commit.

## When you finish

Reply with: emails written, rows left blank, and the manualCheck rows with a one-line reason each.

## Notes for backlink-2026-10-05

- Sender is Sam, offer paid placement as in the shape. Segment A is always the founder's quote swap.
- tella.tv is video-adjacent (screen recording and video tool): quote swap only, use the "we're both in the video space" wording, never offer to make video for them. Do not write "I run a motion studio" as a pitch for them.
- Articles first published before Oct 2024 but updated since (wpforms.com, marq.com, pinecone.io): never call the piece recent or new, never state a date unless articleHook gives it, and put `old article, check` in manualCheck.
- Articles with a blank articleDate: never state a date.
- seo.co and brandpoint.com sell links or placements: add `sells links, check fit` to manualCheck. kaseya.com also covers Datto (owned by Kaseya) and recordedfuture.com is not in this batch.
- rechargepayments.com redirects to getrecharge.com, webstrategiesinc.com to geear.io: use the contact's email domain as given, no comment in the email.
- Attentive's article text has a template tag in double curly braces: never copy it, and put `check in browser` in manualCheck.
- Oktopost: the "Watch the full video below" line may have no embed visible in the crawl. Do not claim the page lacks a video; leave that point out or phrase it so it stays true, and put `check in browser` in manualCheck.
- Weak contact roles (add `contact role check` to manualCheck): DataRobot (Sr. Director Corporate Marketing), TrustedSec (VP Sales and Marketing), Onfleet (Fractional CMO), LinkGraph (Head of Content on a founder row), Oktopost (MD EMEA on a founder row).
- If contactIsFounder is no on a quote swap row, say "one from your side for ours" and add `founder not reached` to manualCheck.
- Hooks that rest on a missing graphic or video, or a page that may load by script: leave that point out or phrase it so it stays true, and put `check in browser` in manualCheck.
- No row is in another Instantly campaign any more (those were dropped).
