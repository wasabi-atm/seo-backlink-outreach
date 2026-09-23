---
name: "mta-backlink-outreach"
description: "Run a Motion The Agency SEO backlink outreach batch. Interview, dedupe against every company already contacted, build and visually vet 40 UK/US/UAE sites with webscreenshotter, ask the user about any competitor, check DR and link habits in Ahrefs, pick one article per site, and draft emails on request."
---

# MTA backlink outreach

This skill builds a batch of 40 sites for SEO backlink exchange outreach for Motion The Agency (MTA, motiontheagency.com). The work runs in four main steps, in order. Step 5 (email drafting) only runs when the user asks for it.

Stop at the checkpoints below. Each one needs a yes from the user before you continue.

## Sync with GitHub before and after every task

The workflow, the ledger, the low-DR pool and every batch live in a private repo that the user shares between devices: `https://github.com/wasabi-atm/seo-backlink-outreach.git`. The local copy (`<repo>` below) is `~/Desktop/mta-backlink-automation` unless `$MTA_REPO` says otherwise. On the user's main Mac that is `/Users/wira/Desktop/mta-backlink-automation`.

**Before anything else**, including the Step 1 interview and any small task such as marking a batch as sent:

1. Run `sh <repo>/skill/mta-backlink-outreach/scripts/sync.sh pull`. If `<repo>` is missing, first run the same script from this skill's own `scripts/` folder; it will clone the repo.
2. If it exits with an error (conflict, no network, no access), stop and tell the user. Never run a batch on a ledger that might be out of date, as that is how a company gets emailed twice.
3. The repo copy of the skill is the source of truth. If `<repo>/skill/mta-backlink-outreach/SKILL.md` differs from the skill you loaded, read the repo version and follow it instead. Tell the user their claude.ai copy is out of date and should be re-uploaded (see README).
4. From here on, run scripts from `<repo>/skill/mta-backlink-outreach/scripts/`, not from the loaded skill folder.

**After the task**, and also straight after any command that changes `outreach_ledger.csv` or `low_dr_pool.csv` (log, set-status, remove, pool), run:

`sh <repo>/skill/mta-backlink-outreach/scripts/sync.sh push "<short message>"`

Examples: "backlink-2026-10-01: 40 prospects to Checkpoint 1", "backlink-2026-10-01: logged 38 emails as queued", "mark backlink-2026-09-23 as sent". Pushing after each ledger change keeps the window small where another device could pick the same company. If the push fails, stop and tell the user. The ledger and pool use git's union merge, so rows added on two devices at once are both kept. After a merge, run `dedupe.py status` to check the ledger still reads cleanly.

Screenshots (`batches/**/shots/`), `.venv` and the zip are not synced. Each device keeps its own.

Output rules for every file and message:

- No em dashes or en dashes anywhere. Plain, simple words.
- CSV column names use camelCase with no spaces (companyName, not "Company name"), so the files load straight into Instantly.
- Save files to `/mnt/user-data/outputs/backlink-outreach/<YYYY-MM-DD>/`. If a folder on the user's computer is connected, also commit the final CSV there. When running in Claude Code, save to `<repo>/batches/<YYYY-MM-DD>/` so the batch syncs to the user's other devices.

## Never email the same company twice

Every company MTA has emailed is recorded in the dedupe ledger, `<repo>/outreach_ledger.csv`, synced through the GitHub repo above.

In a cloud session, reach it through the connected `mta-backlink-automation` folder, or clone the repo if git and access are available. If you cannot read an up-to-date ledger, stop and ask the user. Never build or email a batch without it.

The helper is `<repo>/skill/mta-backlink-outreach/scripts/dedupe.py` (standard library only, any Python 3.8+). It matches on root domain (website, email address and article URL), exact email, cleaned company name, and brand name across TLDs, so `hallam.agency` and `hallam.co.uk`, `chaserhq.com` and `chaser.io`, or `blog.digitalnexa.com` and `digitalnexa.com` count as the same company. It also removes repeats inside the batch. Rows marked `not_sent` in the ledger (for example no email was found) never block. Rows marked `excluded` (competitors the user turned down) do block, and the reason shows in the duplicates file.

- `python dedupe.py check <file.csv> --ledger <ledger>` writes `<file>_clean.csv` and `<file>_duplicates.csv` with a reason per row. Carry on with the clean file only.
- `python dedupe.py log <04_backlink_emails.csv> --ledger <ledger> --status queued --campaign backlink-<YYYY-MM-DD>` records a batch.
- `python dedupe.py set-status --ledger <ledger> --campaign backlink-<YYYY-MM-DD> --status sent` (or `not_sent`, optionally `--domains a.com,b.com`) updates it after sending.
- `python dedupe.py status <ledger>` prints what is in it.
- `python dedupe.py remove --ledger <ledger> --campaign <name>` deletes a whole campaign. Use it only when the user says a run was a test and should be forgotten. Name test runs `backlink-<YYYY-MM-DD>-test` so they are easy to find.

A `possible` match (brand name only) is still removed. Show it to the user at the checkpoint and only put it back if they say it is a different company. Do not edit the ledger by hand.

## Who is a competitor (ask the user, never decide alone)

Vidico, Wyzowl, Zelios, Superside, and any video, animation or motion graphics agency that sells to B2B SaaS, AI or FinTech companies (for example explainer video studios). If a site's main offer is making videos or motion design for other companies, it is a competitor.

Do not drop competitors on your own, and do not quietly keep them either. Flag them and let the user decide:

1. Tag every competitor, and every site you are unsure about, with `competitor` = yes and a one-line `competitorReason` taken from what the site says (for example its homepage title or hero line). All other rows get `competitor` = no.
2. Run the dedupe check and the visual check on them like any other site, so the user sees the score and screenshot facts when deciding.
3. Before Checkpoint 1, ask with AskUserQuestion, one question per flagged site (up to four per call, more calls if needed). Put the company, domain, what they sell, visualScore and any hard fail in the question. Options:
   - "Exclude": drop it and log it in the ledger as `excluded`, so later batches skip it without asking again.
   - "Include, quote swap only": keep it in Segment A. Its offer is always the founder's quote swap (or paid placement). Never offer to make a video, animation or graphic for a competitor.
   - "Exclude this batch only": drop it now, but ask again if it comes up in a later batch. Do not log it.
4. Record the answer in `competitorDecision` (exclude, include, skip) and carry included rows through the rest of the steps.

To log exclusions, put the excluded rows in a CSV and run `dedupe.py log <file> --ledger <ledger> --status excluded --campaign backlink-<YYYY-MM-DD>`.

## The two segments

Segment A, same industry, not a competitor. Companies that sell to the same marketing buyers as MTA without making videos for them: video hosting and video tech platforms, content marketing and SEO agencies, B2B marketing and demand gen agencies, web and brand design studios, podcast production, PR and comms firms, marketing SaaS tools.

Segment B, different industry. B2B companies outside marketing and creative services that run a real blog: SaaS, AI, FinTech, HR tech, dev tools, B2B services. These are also MTA's buyers, so a link from them helps twice.

## Step 1: Interview the user

Before any research, use AskUserQuestion. Ask up to four questions in one call and give defaults so the user can click through:

1. Offer for Segment A. Default: founder's quote exchange (each founder gives a quote for the other's article, both sides link back). This builds thought leadership and domain authority. Confirm or change.
2. Offer for Segment B (multi-select): video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. No default. The user must pick.
3. Batch shape. Default: 40 sites, 20 per segment, spread across UK, US and UAE. Ask if they want a different split or country weighting.
4. Sender and fallback. Default: Lia sends, and the email offers paid placement if they don't want a swap. Confirm the sender name and whether to offer paid placement.

Also ask, in plain text if needed, for any domains to exclude (current partners, clients). Past outreach does not need listing: it comes from the ledger. Run `dedupe.py status` and tell the user how many companies are already in it. Write the answers into `brief.md` in the output folder and use them for every later step.

## Step 2: Build the list and vet it visually

### 2a. Gather candidates

Collect about 60 candidates so 40 survive the filters. Skip any domain already in the ledger while you search, so the 60 are all new. Good sources, in this order:

- Ahrefs `serp-overview` for the target keywords (SaaS video, B2B video, video marketing, advertising, content marketing) with country set to gb, us and ae. Domains that rank for these already have relevant articles and some authority.
- Web search for lists like "B2B content marketing agency London", "SaaS marketing agency Dubai", "video hosting platform".
- Apollo `apollo_mixed_companies_search` to confirm HQ country and industry.

Flag competitors as described above (do not drop them). Drop anything that has no blog or is not based in the UK, US or UAE. Check HubSpot (`search_crm_objects` on companies by domain) and drop current clients and open deals.

Tag each candidate with segment (A or B), country and serviceType (what the company does, in a few words, for example "Video hosting platform" or "HR SaaS").

Save the list as `00_candidates.csv` (companyName, webDomain, country, serviceType, segment, competitor, competitorReason) and run `dedupe.py check` on it before any screenshots or Ahrefs calls. Use `00_candidates_clean.csv` from here on. If the clean list is under 55, find more candidates and check again.

### 2b. Visual scoring

The goal is to keep out SEO farms and low-effort sites. Take screenshots with webscreenshotter, then look at each one yourself with the Read tool and score it.

The script is `<repo>/skill/mta-backlink-outreach/scripts/visual_check.py`. Run it on the clean candidate file:

```
<repo>/.venv/bin/python <repo>/skill/mta-backlink-outreach/scripts/visual_check.py 00_candidates_clean.csv shots/ --workers 4
```

For each domain it saves one screenshot, `shots/<domain>.png`: the first screen as a 16:9 image (1440x810). No full-page shots. It also writes `shots/signals.csv` with ad networks, farm words, outbound link count, word count and whether a blog link exists. Each site has a 150 second limit, so one slow page cannot stall the batch. About 30 seconds per site, so 60 sites take roughly 8 minutes with 4 workers. Run it in the background and wait for it to finish.

Read each `.png` for design and first impressions. For blog quality, look at the blog itself (fetch the blog index and one or two posts for authors, dates and topics) rather than guessing from the homepage.

Setup, once per machine (needs Google Chrome installed):

```
python3 -m venv .venv
.venv/bin/pip install webscreenshotter "selenium<4.10" webdriver-manager pillow
```

Make the venv at `<repo>/.venv` (it is not synced, so each device needs it once; on the main Mac it already exists) and run the script with `<repo>/.venv/bin/python`. The selenium pin matters because webscreenshotter passes the driver path in a way Selenium 4.10 and later removed. webdriver-manager downloads a matching chromedriver on first run.

Where to run it:

1. In Claude Code on the user's Mac, run it directly. This is the tested path.
2. In a cloud session, first test the network with `curl -sI https://<one candidate domain>`. The cloud workspace often blocks arbitrary sites and has no Chrome. If a folder on the user's computer is connected, run the script there with device_bash, then stage the `.png` files back to look at them.
3. For any domain listed under "No screenshots" at the end of the run, or if nothing above works, use the Apify actor `apify/screenshot-url` (urls list, viewportWidth 1440, viewportHeight 810, fullPage false, waitUntil "load", delay 2000) and read the images from its key-value store. Or open each homepage in the built-in browser and take a screenshot. signals.csv still has that site's checks if it loaded; if `loaded` is False too, check the homepage text for farm words by hand.

Score each site 1 to 5 on each of these, from the 16:9 screenshot, the blog pages you fetched and signals.csv:

- Design: custom, current, consistent brand. A template with stock photos scores low.
- Real business: clear product or service, team, customers or case studies.
- Blog quality: named authors, recent dates, topics that fit the business.
- Clean: no display ads, no "write for us" price list, no casino, CBD or payday content, no pages of unrelated outbound links.

Hard fails (drop regardless of score): the site does not load, it is parked, adNetworks is not empty, farmWords includes casino, betting, CBD or payday, or the blog covers topics unrelated to the business. A "write for us" page on its own is not a fail if the site is otherwise real. Note it, because it shows they already do link exchanges.

Keep sites with an average of 3.5 or higher and no hard fail. visualScore is that average, rounded to one decimal.

Save `01_prospects.csv` with: companyName, webDomain, country, serviceType, segment, visualScore, visualNotes, competitor, competitorDecision. Only include competitors the user said to include.

**Checkpoint 1.** Show the user the list as a short table (company, domain, country, segment, score) plus the excluded sites with one-line reasons. List the dedupe removals separately with their reason, and flag any `possible` matches so the user can say if they are really a different company. Any swap the user suggests goes through `dedupe.py check` before it joins the list. Wait for approval, and apply any removals or swaps, before Step 3.

## Step 3: Check domain rating and link habits

Run `mcp__Ahrefs__subscription-info-limits-and-usage` first to see remaining API units. If fewer than about 1,000 units are left, go straight to the Apify fallback below instead of waiting for errors. Call the Ahrefs `doc` tool once before using each Ahrefs endpoint for the first time.

For each approved domain:

- Domain rating: `site-explorer-domain-rating` with target the domain and date today.
- Link habits: `site-explorer-linked-domains` (mode subdomains) for how many other sites their pages link out to, and `site-explorer-backlinks-stats` for their own link profile. Also look for contributor pages, "expert roundup" posts, or recent posts quoting founders from other companies.

Set backlinkExchange:

- Yes: their blog links out to 30 or more unrelated business domains, or they have a contributor or guest post page, or recent posts quote outside founders.
- Some: a few of these signs.
- No: almost no outbound editorial links.

Fallback: if Ahrefs is low on units or returns an out-of-units or limit error, switch to Apify `radeance/ahrefs-scraper` with `urls` (up to 100 domains), `mode` "subdomains", `include_web_authority` true, `include_backlinks` true, `include_traffic` false. Mark the rows filled this way with dataSource "apify". Read its output carefully, or DR will look missing:

- Set `callOptions.maxTotalChargeUsd` to at least 0.25 (Apify refuses lower caps). Cost is about $0.01 per row, two rows per domain, so 40 domains is about $0.80.
- It writes two rows per domain. `type` "backlinks" has only `total_referring_domains` and no DR. `type` "authority" has `domain_rating`, `refdomains`, `dofollow_refdomains` and `backlinks`. Take DR from the authority row only.
- `get-dataset-items` returns 20 rows by default. Set `limit` to at least twice the number of domains, and pass `fields` "domain,type,domain_rating,refdomains,dofollow_refdomains,backlinks" to keep it small.
- If a domain still has no authority row, try the free Ahrefs endpoint `public-domain-rating-free` (targets list, costs no units) for DR.

The scraper does not show which sites a domain links out to, so on the Apify path check link habits by hand: fetch three to five recent blog posts and count distinct outside business domains they link to in the article body, plus any contributor page or quotes from outside founders.

Split the results into two files. Both use the same columns, in this order: companyName, webDomain, domainRating, country, serviceType, segment, visualScore, backlinkExchange, backlinkEvidence, dataSource, competitor, drStatus.

- `02_enriched.csv`: domainRating 40 or higher, drStatus "pass". Only these rows go on to Step 4.
- `02_low_dr.csv`: domainRating under 40 (drStatus "low"), or no DR found by any source (drStatus "unknown", domainRating left blank). Still fill in backlinkExchange and the other columns, so the file is ready if the user wants to use it later. Do not delete these rows or leave them out.

Then add the low-DR rows to the shared pool on the user's Mac, so they can be found again in later sessions and on other devices:

`python3 <repo>/skill/mta-backlink-outreach/scripts/dedupe.py pool 02_low_dr.csv --pool <repo>/low_dr_pool.csv --batch backlink-<YYYY-MM-DD>`

It keeps one row per company (the newest DR check wins) and adds a checkedDate. In Step 2a of later batches, skip pool domains checked in the last 90 days unless the user asks for them, as their DR is unlikely to have moved.

If fewer than 40 rows pass, go back to the spare candidates from Step 2, vet them the same way, and top the list up. Tell the user how many were topped up. Low-DR rows never count towards the 40.

**Checkpoint 2.** Show the user the count that passed, the DR range, and the low-DR list (company, domain, DR) with a note that it is saved in `02_low_dr.csv` and the pool for manual outreach later. Wait for a yes before Step 4.

## Step 4: Pick one article per company

Use the Apify actor `apify/website-content-crawler` to crawl each site's blog. Run it in batches of about 10 domains per run:

- startUrls: each blog index (for example `https://domain.com/blog`)
- includeUrlGlobs: `https://domain.com/blog/**` (match the real blog path)
- crawlerType "cheerio" (switch to "playwright:adaptive" if a site comes back empty)
- maxCrawlDepth 2, maxCrawlPages about 40 per domain, saveMarkdown true

Pull the title, URL and markdown with `get-dataset-items`. Look for articles about SaaS video, B2B video, video marketing, advertising or content marketing. Don't be strict. The test is whether a link to MTA would sit naturally in the article and pass authority to motiontheagency.com. Prefer articles that:

- mention video, explainers, animation, demos or visual content, or recommend something MTA could make
- are live and updated within the last two years
- are not listicles of video agencies (they would be linking to competitors)

When Ahrefs units allow, use `site-explorer-top-pages` to break ties by traffic.

For each company, record one article and a hook for Step 5. A hook is something specific and checkable on that page: the article recommends infographics but has none, a broken table of contents, a date error, a spot where a short video would explain a step better. Write down what you saw, not a guess.

Save the final file as `03_backlink_targets.csv` with: companyName, webDomain, domainRating, country, serviceType, segment, offer, articleTitle, articleUrl, articleTopic, linkPlacement (the section where MTA's link fits and suggested anchor text), articleHook.

The offer column comes from the brief. Segment A uses the Segment A offer. Segment B uses whichever picked offer fits the article best (for example a blog graphic if the article asks for visuals).

Send the CSV to the user and stop. Tell them Step 5 is ready when they want it.

## Step 5: Draft the emails (only when the user asks)

Do not start this step on your own.

First find one contact per company: the founder for founder's quote swaps, otherwise the head of content, content marketing lead or head of marketing. Use Apollo (`apollo_mixed_people_api_search`, then `apollo_people_match` for the email). Show the expected credit cost before spending Apollo credits. Add firstName, lastName, jobTitle, email.

Then run `dedupe.py check` on the file again, now with the email column. This catches companies whose email domain differs from their website (for example hallam.agency with hallam.co.uk addresses) and anything added to the ledger since Step 2, such as a batch sent from another session. Drop every removed row and tell the user which ones and why. Do not write emails for them.

Write one email per row (a single step, no follow-ups) and add emailSubject and emailBody columns. Follow this shape:

```
Hey Phuong,

Just read your piece [5 B2B Content Pillars](https://www.journeyh.io/blog/content-pillars-b2b-content-marketing-strategy). The table of contents still reads "Text Link" three times, and the page says published 11 June and updated 10 June, so the dates are the wrong way round.

Your third pillar also says to visualise findings through infographics, and the five pillars themselves don't have one.

I run a motion studio. Happy to design them, free, and it would carry across your German version of the page too.

In return, just a credit link back to [motiontheagency.com](http://motiontheagency.com), or we'll pay for placement instead.

Would you be open to exploring this?

Cheers,
```

Rules:

- Open with the article, linked by its title. Then one or two specific things you saw on that page, taken from articleHook. Check them again on the live page before writing.
- State the free offer in one line and tie it to the page. For a founder's quote swap, say both founders give a quote for each other's article.
- For a competitor the user chose to include, only offer the founder's quote swap (or paid placement if the brief allows). Do not say "I run a motion studio" as a pitch to make something for them. Say it plainly as context, for example "we're both in motion and video, so a quote swap could work well for both of us".
- Ask for a credit link back to motiontheagency.com. Only add "or we'll pay for placement instead" if the brief says to offer paid placement.
- End with "Would you be open to exploring this?" then "Cheers," and the sender name from the brief.
- Under 110 words. British spelling. No em dashes. Never ask for a call.
- Subject lines are short and lower case, and name their article (for example "your content pillars piece").
- Run every email through the humanizer skill before saving. Invoke it with the Skill tool (`humanizer`) and apply its fixes. Do not skip it or hand-edit instead, even for one email or a test run.

Save `04_backlink_emails.csv`, send it to the user, and say which rows need a manual check (for example no contact found, or the hook could not be confirmed on the live page).

Straight after saving, log the batch in the ledger with `dedupe.py log 04_backlink_emails.csv --ledger <ledger> --status queued --campaign backlink-<YYYY-MM-DD>`. Do this every time, even if the user has not said they will send it. Queued rows block future batches just like sent ones, so a batch is never picked twice. Rows with no email are logged as `not_sent` on their own. Tell the user it is logged, then:

- When they confirm the batch went out, run `set-status --status sent` for that campaign.
- If some rows were not sent (for example they removed them in Instantly), run `set-status --status not_sent --domains <those domains>` so those companies can be picked again later.
- If the user adds rows before sending, put only the new rows in a CSV, run `check` on it, and log the clean file. Logging a row that is already in the ledger does nothing, so it never creates a second entry.

## Low DR companies (only when the user asks)

Companies under DR 40 are never researched, emailed or logged on your own. Only work on them when the user clearly asks, for example "reach out to the low DR ones", "do the under-40 list too" or "email <company> even though its DR is low". Asking about them, or looking at the file, is not a request to email them. If it is unclear, ask with AskUserQuestion first.

When asked:

1. Work from `02_low_dr.csv` of the batch the user means, or from `low_dr_pool.csv` if they mean earlier batches. Use only the rows they name. If they say "all", confirm how many that is first.
2. Run `dedupe.py check` on those rows first. A company may have been contacted since its DR check.
3. Run Step 4 and Step 5 on them exactly as for the main list, with the same rules, the same competitor handling, the humanizer pass and the Apollo credit check. Mark each row with `lowDr` = yes in `03_backlink_targets.csv` and `04_backlink_emails.csv`, or save them as separate `03_low_dr_targets.csv` and `04_low_dr_emails.csv` if the main batch is already done.
4. Log them in the ledger the same way (`--status queued`), with campaign `backlink-<YYYY-MM-DD>-lowdr`, so they are never emailed twice either.
