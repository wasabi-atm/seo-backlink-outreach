# Apollo discovery brief (round 2): backlink-2026-10-16

Read RESEARCH_BRIEF.md in this folder first. All its rules apply (HQ UK/US/UAE, 10 to 500 staff, DR 40+ via the free Ahrefs tool only, live blog with a confirmed dated post since Oct 2025, competitor=yes rows kept, no em or en dashes, no padding, check_domains.py before any other spend, how-the-date-was-confirmed in notes, "HQ from memory" flagged when unverified). Round 1 came back thin (136 rows against a need of about 300) because most known names are already in the ledger.

## User approval for Apollo credits (given in this session on 16 Oct)

The user explicitly approved spending up to 30 Apollo credits on `mcp__Apollo_io__apollo_mixed_companies_search`: 1 credit per request, 30 requests in total across three agents. Each agent may make AT MOST 10 calls to that tool. The user's approval covers the tool's confirmation message; proceed with no further question and do not exceed 10 calls. Do not use any other credit-spending Apollo tool (no enrich, no people search/reveal, no contact or account creation). `apollo_organizations_lookup` is free. Report exactly how many calls you made.

## How to use it well

- Use per_page 100 and `organization_locations`, `organization_num_employees_ranges` ("11,50","51,200","201,500"), `q_organization_keyword_tags`, `organization_founded_year_range`; vary keyword and location per call so the 10 calls return different companies. Results hold `primary_domain` (organizations) or `domain` (accounts). The response is large: save each response's domains to a scratch file with Python right away.
- Run check_domains.py on the domains in bulk (one domain per line in a file with -f). Only NEW ones go to DR: the free Ahrefs tool takes up to 1000 targets per call. Then date-confirm only those with DR 40 or higher.
- Date confirmation routes: `https://DOMAIN/wp-json/wp/v2/posts?per_page=3&_fields=date,link,title`, `/feed/`, `/rss.xml`, sitemaps with lastmod, or the blog index, all through Apify web-fetch (`mcp__Apify_Neu__apify--web-fetch`, with `get-dataset-items`). Do NOT use website-content-crawler: the Apify account is near its memory cap. Keep Apify under $1.00.
- Prioritise 11 to 500 staff and a visible blog. Skip large global brands, consumer companies and anything that looks like a link farm.

## Slices

| slice | scope | file | target |
|---|---|---|---|
| AP_A | Segment A: marketing, content, SEO, PR, design, demand gen agencies, martech and video-tech, UK, US and UAE HQ | research/AP_A.csv | 60 |
| AP_B_UKUAE | Segment B: B2B SaaS, AI, FinTech, HR tech, dev tools, cybersecurity, proptech, legal tech, B2B services, UK and UAE HQ | research/AP_B_UKUAE.csv | 60 |
| AP_B_US | Segment B, same verticals, US HQ | research/AP_B_US.csv | 60 |

Output columns: companyName,webDomain,country,serviceType,segment,competitor,competitorReason,domainRating,blogUrl,latestPost,notes. Python csv module. Only rows that pass every rule.

Reply with: rows written, domains screened, Apollo calls made, Apify spend, competitors flagged.
