# Candidate research brief: backlink-2026-10-13

Motion The Agency (motiontheagency.com) is a motion design and animation studio. We build a list of companies for SEO backlink exchange outreach. Goal today: 150 emailable companies, so we need about 280 vetted NEW candidates. About 1,750 companies have been contacted since September, so the easy names are gone: go deeper, mid-size and niche, regional cities, newer firms. Eight agents work in parallel, each on its own slice; stay inside yours and do not overlap with others.

## Rules

- Never include a domain already known. Check every domain first:
  `python3 /home/user/seo-backlink-outreach/batches/2026-10-13/check_domains.py dom1.com dom2.com ...` (or `-f file.txt`). It prints NEW or EXCLUDED against 3,571 domains. Only NEW domains may go in your file. Check in bulk BEFORE spending DR or Apify calls.
- HQ must be in UK, US or UAE (your slice says which). 
- A real, live blog (or insights/resources section) with at least one dated post since October 2025. Record blog URL and newest post date.
- Domain rating 40 or higher. Use the free Ahrefs tool `mcp__Ahrefs__public-domain-rating-free` (targets list, many per call; call `mcp__Ahrefs__doc` with tool "public-domain-rating-free" once first). Do NOT use any other Ahrefs endpoint (API units are exhausted). Drop DR under 40.
- Competitors (video, animation, motion graphics, explainer studios, Vidico, Wyzowl, Zelios, Superside): keep with competitor=yes and a one-line competitorReason. Everyone else competitor=no.
- Avoid: SEO link farms, display ads, casino/betting/CBD/payday, consumer-only or B2C brands, parked or acquired sites.
- No em dashes or en dashes anywhere.
- Segment A: video hosting and video tech platforms, content marketing and SEO agencies, B2B marketing and demand gen agencies, web and brand design studios, podcast production, PR and comms firms, martech. Segment B: B2B SaaS, AI, FinTech, HR tech, dev tools, cybersecurity, proptech, legal tech, B2B services.

## Slices (file, scope, target rows)

| slice | scope | target |
|---|---|---|
| A_UK_AGENCY | Segment A, UK HQ agencies and studios, outside London first (Manchester, Leeds, Bristol, Edinburgh, Glasgow, Birmingham, Brighton, Cardiff, Belfast, Newcastle, Nottingham, Sheffield, Liverpool, Cambridge, Oxford), then London | 35 |
| A_US_AGENCY_EAST | Segment A, US HQ agencies/studios in the East and Midwest (NY, Boston, DC, Philadelphia, Atlanta, Chicago, Minneapolis, Columbus, Pittsburgh, Charlotte, Miami) | 35 |
| A_US_AGENCY_WEST | Segment A, US HQ agencies/studios in the West and South (SF, LA, Seattle, Portland, Denver, Austin, Dallas, Phoenix, Salt Lake City, San Diego, Nashville) | 35 |
| A_MARTECH | Segment A, UK/UAE/US HQ marketing SaaS and video hosting/video tech platforms | 35 |
| B_UKUAE | Segment B, UK or UAE HQ (include Dubai and Abu Dhabi) | 35 |
| B_US_PEOPLE_FIN | Segment B, US HQ: FinTech, payments, insurtech, accounting, legal tech, HR tech, recruiting, L&D, sales tech, customer success, B2B ed tech | 35 |
| B_US_TECH_VERT | Segment B, US HQ: dev tools, data/AI platforms, cybersecurity, IT ops, cloud infra, vertical SaaS (health, proptech, supply chain, energy, retail tech, field service, manufacturing) | 35 |
| B_US_SERVICES_AI | Segment B, US HQ: B2B services (consulting, staffing, IT services, logistics tech), AI startups and applied AI companies | 35 |

## Tools

- The sandbox blocks company sites (curl 403, WebFetch EGRESS_BLOCKED). Check blogs with Apify via `mcp__Apify_Neu__call-actor`, actor `apify/website-content-crawler` (crawlerType "cheerio", maxCrawlDepth 0, startUrls = 15 to 25 blog index URLs per run, maxCrawlPages = number of URLs, saveMarkdown true, callOptions.maxTotalChargeUsd 0.30). Read results with `mcp__Apify_Neu__get-dataset-items` (fields "url,metadata.title,markdown", set limit). If the index shows no dates, try the post sitemap (`/post-sitemap.xml`, `/sitemap.xml`) or one `"crawlerType":"playwright:adaptive"` run on the index plus the newest 2 post URLs (memory 2048, maxTotalChargeUsd 0.30). Say in notes how the date was confirmed. Keep your Apify spend under $1.50.
- WebSearch: at most 25 searches. Lean on your own knowledge first, go past famous names, then verify.
- Do not use HubSpot, Apollo or Instantly.

## Output

Write `/home/user/seo-backlink-outreach/batches/2026-10-13/research/<slice>.csv` (Python csv module) with columns:
companyName,webDomain,country,serviceType,segment,competitor,competitorReason,domainRating,blogUrl,latestPost,notes
webDomain is the bare root domain. country is UK, US or UAE. latestPost is YYYY-MM-DD. Only rows that pass every rule. Aim for the target; report honestly if the pool is dry, do not pad.

Reply with a short summary: rows written, Apify spend, searches used, competitors flagged.
