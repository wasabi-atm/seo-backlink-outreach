# Candidate research brief: backlink-2026-10-09-b2

Motion The Agency (motiontheagency.com) is a motion design and animation studio. We are building a list of companies for SEO backlink exchange outreach. You find NEW candidate companies for one slice of the list. Seven agents work in parallel (batch 2 of 4 for a 160 site run; about 1,600 companies have been contacted since September, so the easy names are gone: go deeper, mid-size and niche companies, regional cities), each on its own slice, so stay inside yours.

## Rules

- Never include a domain that is already known. Check every domain with:
  `python3 /home/user/seo-backlink-outreach/batches/2026-10-09-b2/check_domains.py dom1.com dom2.com ...`
  (or `-f file.txt` for a list). It prints NEW or EXCLUDED. It compares root domains and brand names across TLDs against 3,428 domains already contacted, researched, pooled or that are clients. Only NEW domains may go in your file. Check candidates in bulk BEFORE spending any Apify or DR calls on them.
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

UK and UAE first. Easy names are gone (batch 1 used 52 and about 1,600 are contacted), so go deeper: mid-size and niche companies, regional cities, newer firms, DR 40 to 65 are fine. Aim for the target but report honestly if the pool is dry.

| slice | scope | target |
|---|---|---|
| RESCUE | Re-verify these domains that batch 1 research dropped only because their blog dates could not be read. Check each with check_domains.py, then DR, then the script-rendered method above. Keep those that pass. fly.io, varonis.com, prefect.io, dataiku.com, scale.com, temporal.io, doppler.com, transcend.io, ketch.com, skyflow.com, llamaindex.ai, clarifai.com, augury.com, motherduck.com, infisical.com, paymentsense.com, peoplehr.com, hireful.com, aridhia.com, foregenix.com, brightsolid.com, craneware.com, rimes.com, glasswall.com, jobtrain.co.uk, pitchbox.com, viget.com, sparkbox.com, sendlane.com, hunter.io, convert.com, ardorseo.com, revenuezen.com, growthmachine.com, crowdcontent.com, madfish.com, bluecorona.com, flyingvdigital.com, nationalpositions.com, mailchimp.com, outgrow.co, verbit.ai, constantcontact.com. Segment by what the company does; HQ must still be UK, UAE or US. | 15 |
| A_UK_AGENCY | Segment A, UK HQ: content marketing, SEO, B2B marketing, demand gen, PR and comms agencies and design studios, outside London first (Manchester, Leeds, Bristol, Edinburgh, Glasgow, Birmingham, Brighton, Cardiff, Belfast, Newcastle, Nottingham, Sheffield, Liverpool, Cambridge, Oxford). | 8 |
| A_US_AGENCY | Segment A, US HQ: content, SEO, B2B, demand gen, ABM, growth, PR agencies, web and brand design studios, podcast production. Mid-size and regional. | 10 |
| A_MARTECH | Segment A, UK, UAE or US HQ: marketing SaaS (email, social, SEO tools, analytics, CRO, ABM, ad tech, CMS, webinar, events, influencer) and video hosting or video tech platforms. | 10 |
| B_UKUAE | Segment B, UK or UAE HQ: B2B SaaS, FinTech, HR tech, AI, cybersecurity, proptech, legal tech, B2B services, including Dubai and Abu Dhabi tech firms. | 10 |
| B_US_PEOPLE_FIN | Segment B, US HQ: FinTech, payments, insurtech, accounting and spend SaaS, legal tech, HR tech, recruiting, L&D, sales tech, customer success, B2B ed tech. Mid-size. | 10 |
| B_US_TECH_VERT | Segment B, US HQ: dev tools, data and AI platforms, cybersecurity, IT ops, cloud infra, vertical B2B SaaS (healthcare, proptech, supply chain, energy, retail tech, field service, manufacturing). Mid-size. | 10 |

## Tools

- The cloud sandbox blocks company sites (curl gets 403, WebFetch says EGRESS_BLOCKED). To check a blog, use Apify via `mcp__Apify_Neu__call-actor` with actor `apify/website-content-crawler` (crawlerType "cheerio", maxCrawlDepth 0, startUrls = several blog index URLs at once, maxCrawlPages = number of URLs, saveMarkdown true, callOptions.maxTotalChargeUsd 0.30). Read results with `mcp__Apify_Neu__get-dataset-items` (fields "url,metadata.title,markdown", and use limit). Batch 15 to 25 blog indexes per run to save money. Look for post dates in the markdown. If a blog index shows no dates, the newest post URL from the index can go in a second batched run. Keep total Apify spend for your slice under $1.00.
- WebSearch is shared across the session. Use at most 25 searches. Lean on your own knowledge of companies first, go past the famous names (most big ones are already in the exclude list), then verify with check_domains.py, the free DR tool and the Apify crawl.
- Do not use HubSpot, Apollo or Instantly.

## Output

Write `/home/user/seo-backlink-outreach/batches/2026-10-09-b2/research/<slice>.csv` with columns:

companyName,webDomain,country,serviceType,segment,competitor,competitorReason,domainRating,blogUrl,latestPost,notes

- webDomain: bare root domain, no www, no path.
- country: UK, US or UAE.
- serviceType: a few words, e.g. "B2B content marketing agency", "HR SaaS".
- latestPost: YYYY-MM-DD of the newest dated post you saw.
- notes: where HQ was confirmed, anything odd (write for us page, redirects).

Only include rows that pass: NEW per check_domains.py, right country, DR 40+, live blog with a dated post since October 2025. Aim for the target count in your slice; going over by a few is fine. Report honestly if you cannot reach it; do not pad with weak or excluded sites. Write the CSV with Python's csv module so commas in text are quoted.

Reply with a short summary: rows written, Apify spend, searches used, and any competitors flagged.

## Extra for batch 2: script-rendered blogs

Batch 1 lost many good names because the cheap cheerio crawl cannot read script-rendered blogs. For batch 2, when a promising DR 40+ NEW domain returns no post dates from cheerio, do not drop it yet: try the post sitemap (`/post-sitemap.xml`, `/sitemap.xml`, `/blog/sitemap.xml`) for `lastmod` dates on blog URLs, or one `apify/website-content-crawler` run with `"crawlerType":"playwright:adaptive"` on the blog index and the newest 2 post URLs (memory 2048, maxTotalChargeUsd 0.30). Only keep the row if you see a post dated after October 2025 (page date, article:published_time, JSON-LD datePublished or a post's sitemap lastmod). Say in `notes` how you confirmed the date.
