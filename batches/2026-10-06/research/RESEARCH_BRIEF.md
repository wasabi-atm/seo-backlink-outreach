# Candidate research brief: backlink-2026-10-06

Motion The Agency (motiontheagency.com) is a motion design and animation studio. We are building a list of companies for SEO backlink exchange outreach. You find NEW candidate companies for one slice of the list. Eight agents work in parallel, each on its own slice, so stay inside yours.

## Rules

- Never include a domain that is already known. Check every domain with:
  `python3 /home/user/seo-backlink-outreach/batches/2026-10-06/check_domains.py dom1.com dom2.com ...`
  (or `-f file.txt` for a list). It prints NEW or EXCLUDED. It compares root domains and brand names across TLDs against 2,839 domains already contacted, researched, pooled or that are clients. Only NEW domains may go in your file. Check candidates in bulk BEFORE spending any Apify or DR calls on them.
- HQ must be in the country your slice names (UK, UAE or US). A big global brand counts only if it is headquartered there.
- It must run a real, live blog (or insights/resources section with articles) with at least one dated post since October 2025. Record the blog URL and the newest post date you saw.
- Domain rating 40 or higher. Check DR with the free Ahrefs tool `mcp__Ahrefs__public-domain-rating-free` (targets list, many domains per call, costs nothing; call `mcp__Ahrefs__doc` with tool "public-domain-rating-free" once first). Do NOT use any other Ahrefs endpoint. Drop anything under 40. A good order: brainstorm and search, run check_domains.py, run the free DR tool on the NEW ones, then crawl blogs only for DR 40+.
- Competitors: any video, animation, motion graphics or explainer video agency or studio, plus Vidico, Wyzowl, Zelios, Superside. Do NOT drop them; keep them with competitor=yes and a one-line competitorReason from the site. Everyone else competitor=no.
- Avoid: SEO link farms, sites with display ads or casino/betting/CBD/payday content, consumer-only apps and B2C brands, parked or acquired sites (domain redirects to another company), companies that only sell to consumers.
- No em dashes or en dashes in anything you write.

## Segments

- Segment A (same industry as MTA, but not making videos): video hosting and video tech platforms, content marketing and SEO agencies, B2B marketing and demand gen agencies, web and brand design studios, podcast production, PR and comms firms, marketing SaaS tools (martech).
- Segment B (different industry, B2B, real blog): SaaS, AI, FinTech, HR tech, dev tools, cybersecurity, proptech, legal tech, B2B services.

## Slices (file name, scope, target rows)

| slice | scope | target |
|---|---|---|
| A_UKUAE | Segment A, HQ in UK or UAE. Agencies (content, SEO, B2B, PR, design, podcast) and martech. Regional cities too: Manchester, Leeds, Bristol, Edinburgh, Glasgow, Birmingham, Brighton, Cardiff, Belfast, Abu Dhabi, Sharjah. | 30 |
| A_US_AGENCY | Segment A, US HQ: content marketing, SEO, B2B marketing, demand gen, ABM, growth agencies. Any US city. | 30 |
| A_US_MARTECH | Segment A, US HQ: marketing SaaS (email, social, SEO tools, analytics, CRO, ABM, ad tech, CMS, webinar, events, influencer), video hosting and video tech platforms. | 35 |
| A_US_CREATIVE | Segment A, US HQ: web and brand design studios, branding agencies, PR and comms firms, podcast production and hosting. | 25 |
| B_UKUAE | Segment B, HQ in UK or UAE: B2B SaaS, FinTech, HR tech, AI, cybersecurity, proptech, legal tech, B2B services. | 35 |
| B_US_PEOPLE | Segment B, US HQ: HR tech, recruiting, payroll, L&D, sales tech, customer success, productivity and collaboration SaaS, B2B ed tech. | 30 |
| B_US_FIN | Segment B, US HQ: FinTech, payments, banking infra, insurtech, accounting and spend SaaS, legal tech, proptech and construction tech. | 30 |
| B_US_TECH | Segment B, US HQ: dev tools, data and AI platforms, cybersecurity, IT ops and observability, cloud infra, supply chain and logistics SaaS, healthcare B2B SaaS. | 30 |

## Tools

- The cloud sandbox blocks company sites (curl gets 403, WebFetch says EGRESS_BLOCKED). To check a blog, use Apify via `mcp__Apify_Neu__call-actor` with actor `apify/website-content-crawler` (crawlerType "cheerio", maxCrawlDepth 0, startUrls = several blog index URLs at once, maxCrawlPages = number of URLs, saveMarkdown true, callOptions.maxTotalChargeUsd 0.30). Read results with `mcp__Apify_Neu__get-dataset-items` (fields "url,metadata.title,markdown", and use limit). Batch 15 to 25 blog indexes per run to save money. Look for post dates in the markdown. If a blog index shows no dates, the newest post URL from the index can go in a second batched run. Keep total Apify spend for your slice under $1.50.
- WebSearch is shared across the session. Use at most 25 searches. Lean on your own knowledge of companies first, go past the famous names (most big ones are already in the exclude list), then verify with check_domains.py, the free DR tool and the Apify crawl.
- Do not use HubSpot, Apollo or Instantly.

## Output

Write `/home/user/seo-backlink-outreach/batches/2026-10-06/research/<slice>.csv` with columns:

companyName,webDomain,country,serviceType,segment,competitor,competitorReason,domainRating,blogUrl,latestPost,notes

- webDomain: bare root domain, no www, no path.
- country: UK, US or UAE.
- serviceType: a few words, e.g. "B2B content marketing agency", "HR SaaS".
- latestPost: YYYY-MM-DD of the newest dated post you saw.
- notes: where HQ was confirmed, anything odd (write for us page, redirects).

Only include rows that pass: NEW per check_domains.py, right country, DR 40+, live blog with a dated post since October 2025. Aim for the target count in your slice; going over by a few is fine. Report honestly if you cannot reach it; do not pad with weak or excluded sites. Write the CSV with Python's csv module so commas in text are quoted.

Reply with a short summary: rows written, Apify spend, searches used, and any competitors flagged.
