# Round 2 research brief: backlink-2026-10-13

Round 1 (8 agents) found 115 candidates, short of the 150-email goal. Round 2 adds more. Same rules as /home/user/seo-backlink-outreach/batches/2026-10-13/research/RESEARCH_BRIEF.md (read it first: HQ UK/US/UAE only, DR 40+ from the free Ahrefs tool `mcp__Ahrefs__public-domain-rating-free` only, live dated blog post since Oct 2025, competitor rows kept with competitor=yes, no em or en dashes, no padding, check_domains.py before spending anything). exclude_domains.txt now also contains today's 115 round 1 candidates, so only NEW domains count.

## What round 1 learned (use it)

- The blocker is confirming a post date, not finding companies. Cheerio crawls of blog index pages fail on JS-rendered blogs. These routes work better, through `mcp__Apify_Neu__apify--web-fetch` (or apify/web-fetch via call-actor), roughly one call per URL:
  1. WordPress REST: `https://DOMAIN/wp-json/wp/v2/posts?per_page=3&_fields=date,link,title` (gives exact dates).
  2. RSS: `https://DOMAIN/feed/`, `/blog/feed/`, `/blog/rss.xml`, `/rss.xml`, `/feed.xml`, `/blog/feed`.
  3. Sitemaps with lastmod: `/post-sitemap.xml`, `/blog-sitemap.xml`, `/sitemap.xml`.
  4. Open the newest post URL itself and read article:published_time, JSON-LD datePublished or the visible date.
  5. WebSearch snippets showing a dated post are acceptable as a last resort; say so in notes.
- Apify account allows few concurrent runs and sibling agents share it. Prefer web-fetch (light). If a crawler run is queued, wait and retry; do not abort and move on. Set crawler memory to 1024.
- The `render-scorecard` hint the Ahrefs tool prints can be ignored.
- HQ: confirm from the site (footer, contact page, JSON-LD address) or a search snippet when you can; if it is only from memory, say "HQ from memory" in notes.
- Keep Apify spend under $1.50 per agent. Report spend honestly.

## Slices

| slice | scope | target |
|---|---|---|
| R1_RECHECK_A | Re-verify these undated or unverified companies (find the real domain if needed; each must still pass check_domains.py as NEW, DR 40+, HQ, then get a confirmed post date): Segment A: Spotlightr, Hyperise, Slidebean, Postal.io, Justuno, Bluecore, Airmeet, ConvertFlow, Mailmunch, Zight, Guidde, Flixier, Ecamm, PageProof, Cincopa, 100ms, Dyte, Wipster, BIGVU, Yac, Covideo, Element Three, Rawnet, Accent Design, Yoyo Design, Zazzle Media, Viget, Sparkbox, Teknicks, Newfangled, UpCity, Wondersauce, Bluecadet, Blue Fountain Media, Ethos3, Duarte, Webstacks, Octiv Digital, Carmichael Lynch, Mindgrub, Nerdery, Blue State, Barkley, Augurian, Mutually Human | 20 |
| R1_RECHECK_B | Same job for Segment B: Passfort, Cogna, Experis UK, Onecom, Dionach, Gradwell, AccessPlanit, Hometrack, Paymentsense, PeopleHR, Brightmine UK, Snap Surveys, CloudCall, JobTrain, Fasthosts, Harvey Nash, Payzone, PropertyFile, Contractzen, Marketfinance, Skilljar, QuotaPath, Litify, LawPay, CasePeer, Accurate, Textio, Traliant, UpLead, Floify, Next Insurance, Material Security, ServiceTitan, Rapid7, DoorLoop, CompanyCam, Robert Half, Insight Global, Lucidworks, Dataiku, Stord, EPAM, Toptal, Packsize, Blue Yonder, Crowe, Mondo | 25 |
| S2_SEGA | New companies from Apollo or Instantly company search, Segment A: marketing, content, SEO, PR, design and demand gen agencies, martech and video tech platforms, UK, US and UAE HQ, 11 to 500 staff, outside the biggest brands. Run many queries (cities, sub-niches, keywords) to get hundreds of domains, check_domains.py in bulk, then DR, then date | 40 |
| S2_SEGB_UKUAE | Same method, Segment B, UK and UAE HQ B2B SaaS, AI, FinTech, HR tech, dev tools, cybersecurity, proptech, legal tech, B2B services, 11 to 500 staff | 40 |
| S2_SEGB_US | Same method, Segment B, US HQ, mid-size (11 to 500 staff), all B2B verticals above | 40 |

## Search tools for the S2 slices (company discovery)

- Instantly: `mcp__Instantly__enrichment_preview`, `enrichment_count`, `enrichment_generate_filters` (free) and `company_list_*` tools. Use filters for HQ country, industry, employee count. Do NOT run `enrichment_enrich` or anything that spends Instantly credits.
- Apollo: `mcp__Apollo_io__apollo_mixed_companies_search` (organization search; check its schema; use `apollo_organizations_enrich` only for single ambiguous cases). Do NOT bulk enrich, reveal emails or create contacts. If a call returns a credit usage block, record it and stop using that tool if it spends credits.
- Do not use HubSpot. WebSearch up to 25 calls.

## Output

Write `/home/user/seo-backlink-outreach/batches/2026-10-13/research2/<slice>.csv` with the same 11 columns as round 1: companyName,webDomain,country,serviceType,segment,competitor,competitorReason,domainRating,blogUrl,latestPost,notes. Use the Python csv module. Only rows that pass every rule; do not pad. Put how the date was confirmed in notes, and "HQ from memory" where it applies.

Reply with a short summary: rows written, how many candidates you screened, Apify spend, Apollo/Instantly credits used, searches used, competitors flagged.
