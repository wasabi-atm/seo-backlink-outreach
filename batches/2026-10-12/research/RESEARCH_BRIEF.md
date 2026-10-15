# Candidate research brief: backlink-2026-10-12

Motion The Agency (motiontheagency.com) is a motion design and animation studio. We are building a list of companies for SEO backlink exchange outreach. You find NEW candidate companies for one slice of the list. Fifteen agents work in parallel on a 170 site run, each on its own slice, so stay inside yours. About 1,700 companies have been contacted since September and 3,480 domains are already known, so the famous names are gone: go deeper, mid-size and niche companies, regional cities, newer firms.

Working folder: `/home/user/seo-backlink-outreach/batches/2026-10-12` (BATCH below).

## Rules

- Never include a domain that is already known or taken by another slice. Check every domain with:
  `python3 BATCH/check_domains.py --claim <YOUR_SLICE> dom1.com dom2.com ...`
  (or `--claim <YOUR_SLICE> -f file.txt` for a list). It prints NEW or EXCLUDED. It compares root domains and brand names across TLDs against every domain already contacted, researched, pooled or that is a client, and against domains other slices claimed today. Every NEW domain is claimed for your slice at that moment, so check a domain only once you would really verify it, and always pass your own slice name. Only NEW domains may go in your file. Check in bulk BEFORE spending any Apify or DR calls.
- HQ must be in the country your slice names (UK, UAE or US). A big global brand counts only if it is headquartered there.
- It must run a real, live blog (or insights, resources or news section with articles, not just press releases) with at least one dated post since October 2025, ideally within the last six months. Record the blog index URL that really lists the posts and the newest post date you saw.
- Domain rating 40 or higher. Check DR with the free Ahrefs tool `mcp__Ahrefs__public-domain-rating-free` (input `{"targets": ["a.com", "b.com", ...]}`, many domains per call, costs nothing). Load it with ToolSearch `select:mcp__Ahrefs__public-domain-rating-free`. Do NOT use any other Ahrefs endpoint (the paid units are used up). Drop anything under 40. Good order: brainstorm and search, run check_domains.py, run the free DR tool on the NEW ones, then check blogs only for DR 40+.
- Competitors: any video, animation, motion graphics or explainer video agency or studio, plus Vidico, Wyzowl, Zelios, Superside. Do NOT drop them; keep them with competitor=yes and a one-line competitorReason from the site. Everyone else competitor=no. Agencies that offer video as one of many services are not competitors, but note it in notes.
- Avoid: SEO link farms and link vendors, sites with display ads or casino, betting, CBD or payday content, consumer-only apps and B2C brands, parked or acquired sites (domain redirects to another company), companies that only sell to consumers.
- No em dashes or en dashes in anything you write.

## Segments

- Segment A (same industry as MTA, but not making videos): video hosting and video tech platforms, content marketing and SEO agencies, B2B marketing and demand gen agencies, web and brand design studios, podcast production, PR and comms firms, marketing SaaS tools (martech).
- Segment B (different industry, B2B, real blog): SaaS, AI, FinTech, HR tech, dev tools, cybersecurity, proptech, legal tech, B2B services.

## Slices (file name, scope, target rows)

| slice | scope | target |
|---|---|---|
| A_UK_AGENCY_NORTH | Segment A, UK HQ outside London and the South: content marketing, SEO, B2B marketing, demand gen, PR and comms agencies, web and brand design studios. Manchester, Leeds, Sheffield, Liverpool, Newcastle, York, Hull, Edinburgh, Glasgow, Aberdeen, Dundee, Cardiff, Swansea, Belfast, Birmingham, Nottingham, Leicester, Derby, Coventry, Stoke, Lancashire, Cheshire. | 12 |
| A_UK_AGENCY_SOUTH | Segment A, UK HQ in London and the South: content marketing, SEO, B2B, demand gen, PR and comms agencies, design studios. London first (mid-size and niche B2B specialists, tech PR, fintech PR, SaaS SEO), then Bristol, Bath, Brighton, Oxford, Cambridge, Reading, Guildford, Southampton, Bournemouth, Exeter, Norwich, Milton Keynes. | 12 |
| A_UKUAE_MARTECH | Segment A, UK or UAE HQ: marketing SaaS (email, social, SEO tools, analytics, CRO, ABM, ad tech, CMS, webinar, events, influencer, PR software, review and survey tools, video hosting or video tech), plus UAE marketing, content, SEO, PR and design agencies in Dubai and Abu Dhabi. | 12 |
| A_US_AGENCY_EAST | Segment A, US HQ in the Northeast, Midwest and Southeast: content, SEO, B2B, demand gen, ABM, growth, PR agencies. Boston, NYC, Philadelphia, Pittsburgh, DC, Baltimore, Chicago, Minneapolis, Detroit, Columbus, Cleveland, Cincinnati, Indianapolis, Milwaukee, St Louis, Kansas City, Atlanta, Charlotte, Raleigh, Nashville, Tampa, Miami, Orlando. Mid-size and regional. | 15 |
| A_US_AGENCY_WEST | Segment A, US HQ in the West, Southwest and Texas: content, SEO, B2B, demand gen, ABM, growth, PR agencies. San Francisco, LA, San Diego, Seattle, Portland, Denver, Boulder, Salt Lake City, Phoenix, Las Vegas, Austin, Dallas, Houston, San Antonio, Boise, Sacramento. Mid-size and regional. | 15 |
| A_US_MARTECH_1 | Segment A, US HQ martech: email and SMS marketing, social media management, SEO and content tools, AI writing tools for marketers, web analytics, CRO and A/B testing, personalisation, forms, surveys, landing page builders, marketing automation. | 15 |
| A_US_MARTECH_2 | Segment A, US HQ martech: ABM, intent data, ad tech and ad management, CMS, website builders, DAM, webinar and virtual events, event tech, influencer and creator platforms, affiliate and partner marketing, PR and media monitoring software, review platforms, video hosting and video tech, podcast hosting. | 15 |
| A_US_CREATIVE_PR | Segment A, US HQ: web design and development studios, brand and UX design agencies, PR and comms firms (tech, B2B, fintech, healthcare PR), podcast production companies, B2B copywriting and content studios. Not video or animation studios (those are competitors). | 13 |
| B_UK_FIN_LEGAL | Segment B, UK HQ: fintech, payments, open banking, insurtech, accounting and spend SaaS, wealth and pensions tech, proptech, legal tech, regtech, compliance SaaS. | 14 |
| B_UK_TECH_PEOPLE | Segment B, UK HQ: HR tech, payroll, recruiting, L&D, B2B ed tech, cybersecurity, AI, dev tools, data platforms, IT managed services, B2B consultancies with a real blog. | 14 |
| B_UAE_UK_VERT | Segment B: UAE HQ B2B tech first (Dubai and Abu Dhabi: fintech, proptech, logistics, AI, SaaS, B2B services), then UK HQ vertical B2B SaaS (construction, logistics, supply chain, energy, climate tech, healthtech sold to businesses, retail tech, hospitality tech, field service, manufacturing). | 12 |
| B_US_FIN | Segment B, US HQ: fintech, payments, insurtech, accounting, AP and AR, spend management, lending infrastructure, B2B wealth tech, regtech, tax tech. Mid-size. | 15 |
| B_US_PEOPLE_SALES | Segment B, US HQ: HR tech, payroll, benefits, recruiting, L&D, employee engagement, sales tech, revenue intelligence, sales enablement, customer success, CX and support software, B2B ed tech. Mid-size. | 15 |
| B_US_DEV_SEC | Segment B, US HQ: dev tools, APIs, data platforms, AI and ML platforms, observability, cybersecurity, identity, IT ops, cloud infrastructure, low-code. Mid-size. | 15 |
| B_US_VERT | Segment B, US HQ vertical B2B SaaS: healthcare and practice management, proptech and property management, construction, supply chain and logistics, manufacturing, energy, retail tech, restaurant tech, field service, legal tech, nonprofit tech, govtech, agtech, fleet. Mid-size. | 15 |

Aim for the target but report honestly if the pool is dry. Going over by a few is fine.

## Tools

- The cloud sandbox blocks company sites (curl gets 403, WebFetch says EGRESS_BLOCKED). To check a blog, use Apify. Load with ToolSearch `select:mcp__Apify_Neu__call-actor,mcp__Apify_Neu__get-dataset-items`.
  - Cheap first pass: actor `apify/website-content-crawler` with `{"startUrls":[{"url": blog1}, {"url": blog2}, ...], "crawlerType":"cheerio", "maxCrawlDepth":0, "maxCrawlPages":<number of URLs>, "saveMarkdown":true, "maxRequestRetries":1, "proxyConfiguration":{"useApifyProxy":true}}`, callOptions `{"memory":2048,"timeout":600,"maxTotalChargeUsd":0.30}`. Batch 15 to 25 blog indexes per run. Read with `get-dataset-items` (fields "url,metadata.title,markdown", limit at least the URL count). Large results are saved to a file whose path the tool gives you: copy it into your scratchpad as `r_<SLICE>_*.json` (other agents share the scratchpad) and parse it with Python. Do not paste whole pages into your context. Look for post dates in the markdown.
  - Script-rendered blogs: when a promising DR 40+ NEW domain shows no post dates, do not drop it yet. Try the post sitemap (`/post-sitemap.xml`, `/sitemap.xml`, `/blog/sitemap.xml`) for `lastmod` dates on blog URLs, or one run with `"crawlerType":"playwright:adaptive"` on the blog index and the newest 2 post URLs (memory 2048). Only keep the row if you see a post dated after October 2025 (page date, article:published_time, JSON-LD datePublished, or a post's sitemap lastmod). Say in notes how you confirmed the date.
  - Do not call `get-actor-run` to poll (its output is huge). With waitSecs 45 most runs finish; otherwise poll with `get-dataset-items` (fields "url", limit 1) and read totalItemCount.
  - Keep total Apify spend for your slice under $0.70.
- WebSearch (load with ToolSearch `select:WebSearch`, mode "standard") is shared across the session. Use at most 20 searches. Lean on your own knowledge of companies first, go past the famous names, then verify with check_domains.py, the free DR tool and the Apify crawl. Directories (Clutch, DesignRush, G2 category pages, Built In, Tech Nation, Dubai Chamber lists) are good for finding mid-size names; search results are good for HQ checks.
- Do not use HubSpot, Apollo or Instantly.

## Output

Write `BATCH/research/<SLICE>.csv` with columns:

companyName,webDomain,country,serviceType,segment,competitor,competitorReason,domainRating,blogUrl,latestPost,notes

- webDomain: bare root domain, no www, no path.
- country: UK, US or UAE.
- serviceType: a few words, e.g. "B2B content marketing agency", "HR SaaS".
- latestPost: YYYY-MM-DD of the newest dated post you saw.
- notes: where HQ was confirmed, how the date was confirmed, anything odd (write for us page, redirects, offers video as one service).

Only include rows that pass: NEW per check_domains.py, right country, DR 40+, live blog with a dated post since October 2025. Do not pad with weak sites. Write the CSV with Python's csv module so commas in text are quoted. Write the file as you go (rewrite it after each verified group) so partial work is never lost.

Do not edit any other file, do not touch the ledger, do not commit to git.

Reply with a short summary: rows written, Apify spend, searches used, and any competitors flagged.
