# Candidate research brief: backlink-2026-10-19

Motion The Agency (motiontheagency.com) is a motion design and animation studio. We build a list of companies for SEO backlink exchange outreach. Goal today: 150 emailable companies, so we need as many vetted NEW candidates as possible (about 300). About 2,600 companies have been contacted since September and 6,876 domains are known (a similar run on 16 Oct dried up at 99 article-passed companies), so the easy names are gone: go deep, mid-size and niche, regional cities, newer firms. Ten agents work in parallel, each on its own slice; stay inside yours and do not overlap with others.

## Rules

- Never include a domain already known. Check every domain first:
  `python3 /home/user/seo-backlink-outreach/batches/2026-10-19/check_domains.py dom1.com dom2.com ...` (or `-f file.txt`). It prints NEW or EXCLUDED. Only NEW domains may go in your file. Check in bulk BEFORE spending DR or Apify calls.
- HQ must be in the country your slice says: UK, US, UAE, Australia, Canada or Singapore (Australia, Canada and Singapore are new this run).
- A real, live blog (or insights/resources section) with at least one dated post since 19 October 2025. Record blog URL and newest post date.
- Between 10 and 500 staff, not part of a big group. B2B. 
- Domain rating 40 or higher. Use the free Ahrefs tool `mcp__Ahrefs__public-domain-rating-free` (targets list, many per call; call `mcp__Ahrefs__doc` with tool "public-domain-rating-free" once first). Load with ToolSearch `select:mcp__Ahrefs__public-domain-rating-free,mcp__Ahrefs__doc`. Do NOT use any other Ahrefs endpoint (API units are exhausted). Drop DR under 40.
- Competitors (video, animation, motion graphics, explainer studios, Vidico, Wyzowl, Zelios, Superside): keep with competitor=yes and a one-line competitorReason. Everyone else competitor=no.
- Avoid: SEO link farms, sites that sell guest posts, display ads, casino/betting/CBD/payday, consumer-only or B2C brands, parked or acquired sites.
- No em dashes or en dashes anywhere. Plain words.
- Segment A: video hosting and video tech platforms, content marketing and SEO agencies, B2B marketing and demand gen agencies, web and brand design studios, podcast production, PR and comms firms, martech. Segment B: B2B SaaS, AI, FinTech, HR tech, dev tools, cybersecurity, proptech, legal tech, B2B services.

## Slices (file, scope, target rows)

| slice | scope | target |
|---|---|---|
| A_UK_REGIONS | Segment A, UK HQ agencies/studios outside London (Manchester, Leeds, Bristol, Edinburgh, Glasgow, Birmingham, Brighton, Cardiff, Belfast, Newcastle, Nottingham, Sheffield, Liverpool, Cambridge, Oxford, Reading, Bath, Exeter, Norwich, Southampton) | 25 |
| A_UK_LONDON | Segment A, London HQ niche B2B marketing, content, SEO, PR, design, demand gen agencies (10 to 200 staff) | 25 |
| A_US_EAST | Segment A, US HQ agencies/studios in the East and Midwest | 25 |
| A_US_WEST_SOUTH | Segment A, US HQ agencies/studios in the West and South | 25 |
| A_MARTECH | Segment A, UK/US/UAE HQ marketing SaaS, video hosting/video tech, podcast tools, content tools | 25 |
| A_UAE_PR_DESIGN | Segment A, UAE HQ (Dubai, Abu Dhabi, Sharjah) agencies, plus UK/US PR, comms, brand and web design studios | 25 |
| A_AU | Segment A, Australia HQ (Sydney, Melbourne, Brisbane, Perth, Adelaide, Canberra): B2B marketing, content, SEO, PR, design agencies and marketing SaaS | 30 |
| A_CA_SG | Segment A, Canada HQ (Toronto, Vancouver, Montreal, Calgary, Ottawa) and Singapore HQ: agencies, studios and marketing SaaS | 30 |
| B_UKUAE | Segment B, UK or UAE HQ (include Dubai and Abu Dhabi) | 25 |
| B_US_PEOPLE_FIN | Segment B, US HQ: FinTech, payments, insurtech, accounting, legal tech, HR tech, recruiting, L&D, sales tech, customer success, B2B ed tech | 25 |
| B_US_TECH_VERT | Segment B, US HQ: dev tools, data/AI platforms, cybersecurity, IT ops, cloud infra, vertical SaaS (health, proptech, supply chain, energy, retail tech, field service, manufacturing) | 25 |
| B_US_SERVICES_AI | Segment B, US HQ: B2B services (consulting, staffing, IT services, logistics tech), AI startups and applied AI companies | 25 |
| B_AU_CA_SG | Segment B, Australia, Canada or Singapore HQ: SaaS, AI, FinTech, HR tech, dev tools, cybersecurity, B2B services | 30 |

## Tools

- The sandbox blocks company sites (curl 403, WebFetch EGRESS_BLOCKED). Check blogs with Apify: load `select:mcp__Apify_Neu__apify--web-fetch,mcp__Apify_Neu__get-dataset-items,mcp__Apify_Neu__call-actor` with ToolSearch. Cheapest date check: `apify--web-fetch` on `https://DOMAIN/wp-json/wp/v2/posts?per_page=3&_fields=date,link,title`, `/feed/`, `/rss.xml`, a sitemap with lastmod, or the blog index. For many domains at once use `call-actor` `apify/website-content-crawler` (crawlerType "cheerio", maxCrawlDepth 0, startUrls = 15 to 25 blog index URLs per run, maxCrawlPages = number of URLs, saveMarkdown true, callOptions.maxTotalChargeUsd 0.30), read with `get-dataset-items` (fields "url,metadata.title,markdown", set limit). Say in notes how the date was confirmed. Keep your Apify spend under $1.50.
- WebSearch: at most 25 searches. Lean on your own knowledge first, go past famous names, then verify.
- Free discovery help: `mcp__Apollo_io__apollo_organizations_lookup` (free). Do not call `apollo_mixed_companies_search` (costs credits) or any other credit-spending Apollo or Instantly tool; the user did not approve Apollo company-search credits this run. Do not use HubSpot.

## Output

Write `/home/user/seo-backlink-outreach/batches/2026-10-19/research/<slice>.csv` (Python csv module) with columns:
companyName,webDomain,country,serviceType,segment,competitor,competitorReason,domainRating,blogUrl,latestPost,notes
webDomain is the bare root domain. country is UK, US, UAE, AU, CA or SG. latestPost is YYYY-MM-DD. Only rows that pass every rule. Aim for the target; report honestly if the pool is dry, do not pad. Mark "HQ from memory" in notes when you did not verify the HQ.

Reply with a short summary: rows written, Apify spend, searches used, competitors flagged.
