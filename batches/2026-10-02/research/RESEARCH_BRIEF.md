# Candidate research brief: backlink-2026-10-02

Motion The Agency (motiontheagency.com) is a motion design and animation studio. We are building a list of companies for SEO backlink exchange outreach. You find NEW candidate companies for one slice of the list.

## Rules

- Never include a domain listed in `/home/user/seo-backlink-outreach/batches/2026-10-02/exclude_domains.txt` (2,500 domains already contacted or already researched). Also treat a different TLD of the same brand as excluded (hallam.agency = hallam.co.uk). Check with grep before adding a row.
- HQ must be in the country your slice names (UK, UAE or US). A big global brand counts only if it is headquartered there.
- It must run a real, live blog (or insights/resources section with articles) with at least one dated post since October 2025. Record the blog URL and the latest post date you saw.
- Domain rating 40 or higher. Check DR with the free Ahrefs tool `mcp__Ahrefs__public-domain-rating-free` (targets list, up to 1000 domains per call, costs nothing; call `mcp__Ahrefs__doc` with tool "public-domain-rating-free" once first). Do NOT use any other paid Ahrefs endpoint. Drop anything under 40.
- Competitors: any video, animation, motion graphics or explainer video agency/studio, plus Vidico, Wyzowl, Zelios, Superside. Do NOT drop them; keep them with competitor=yes and a one-line competitorReason from the site. Everyone else competitor=no.
- Avoid: SEO link farms, sites with display ads or casino/betting/CBD/payday content, consumer-only apps, parked or acquired sites (domain redirects to another company).
- No em dashes or en dashes in anything you write.

## Segments

- Segment A (same industry, not making videos): video hosting and video tech platforms, content marketing and SEO agencies, B2B marketing and demand gen agencies, web and brand design studios, podcast production, PR and comms firms, marketing SaaS tools (martech).
- Segment B (different industry, B2B, real blog): SaaS, AI, FinTech, HR tech, dev tools, cybersecurity, proptech, legal tech, B2B services.

## Tools

- The cloud sandbox network blocks most company sites (curl gets 403), and WebFetch may be blocked too. To check a blog, use Apify via `mcp__Apify_Neu__call-actor` with actor `apify/website-content-crawler` (crawlerType "cheerio", maxCrawlDepth 0, startUrls = several blog index URLs at once, maxCrawlPages = number of URLs, saveMarkdown true, callOptions.maxTotalChargeUsd 0.30) and read results with `mcp__Apify_Neu__get-dataset-items` (fields "url,metadata.title,markdown", and use limit). Batch 15 to 25 blog indexes per run to save money. Look for post dates in the markdown. Keep total Apify spend for your slice under $1.50.
- WebSearch is shared and limited across the session (about 200 calls in total for everyone). Use at most 30 searches. Lean on your own knowledge of companies, then verify with the DR tool and the Apify crawl.
- Do not use HubSpot, Apollo or Instantly.

## Output

Write `/home/user/seo-backlink-outreach/batches/2026-10-02/research/<slice>.csv` with columns:

companyName,webDomain,country,serviceType,segment,competitor,competitorReason,domainRating,blogUrl,latestPost,notes

- webDomain: bare root domain, no www, no path.
- serviceType: a few words, e.g. "B2B content marketing agency", "HR SaaS".
- latestPost: YYYY-MM-DD of the newest dated post you saw, blank if not confirmed.
- notes: where HQ was confirmed, anything odd (write for us page, redirects).

Only include rows that pass: not excluded, right country, DR 40+, live blog. Aim for the target count in your slice. Reply with a short summary: rows written, how many with a confirmed post date since Oct 2025, Apify spend, searches used, and any competitors flagged.

## Extra notes for 2 Oct

- The UK and UAE pools are close to used up, so look further down the list: smaller but real companies, niche B2B SaaS, regional agencies (Manchester, Leeds, Bristol, Edinburgh, Abu Dhabi, Sharjah), and US companies from any city. For US slices go past the famous names.
- Already researched and vetted spares live in `research/spares_from_1oct.csv` (do not re-research those; they are added separately). Do not include them in your output.
- Spare UK Segment B names that were DR and date confirmed but not yet in a file, include them in B_UK if you can re-confirm DR with the free tool and one dated post: krystal.io, ans.co.uk, 6dg.co.uk, quartix.com, fleetcheck.co.uk, achilles.com, workspace.co.uk, homeflow.co.uk, kortext.com, century.tech, cpoms.co.uk, unifrog.org, sparx-learning.com, pandle.com, takepayments.com, fleximize.com, natterbox.com, croner.co.uk, landlordvision.co.uk, signable.com, boxphish.com, performanta.com, redflagalert.com, matillion.com. (B_UK agent only. Check each against exclude_domains.txt first.) Spare US B names: osano.com, numeric.io, expel.com, canopy.com, guru.com (B_US agent only; check them too).
- Consumer property brokerages, consumer apps and anything B2C-leaning are out.
