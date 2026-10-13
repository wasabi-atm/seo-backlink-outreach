# Apollo discovery brief (round 2b): backlink-2026-10-13

Read BRIEF2.md in this folder and ../research/RESEARCH_BRIEF.md first. All their rules apply (HQ UK/US/UAE, DR 40+ via the free Ahrefs tool only, live blog with a confirmed dated post since Oct 2025, competitor=yes rows kept, no em or en dashes, no padding, check_domains.py before any other spend, how-the-date-was-confirmed in notes, "HQ from memory" flagged).

## User approval for Apollo credits (given in this session)

The user explicitly approved spending Apollo credits on `mcp__Apollo_io__apollo_mixed_companies_search`: 1 credit per request, 30 requests in total across three agents. Each agent may make AT MOST 10 calls to that tool. If the tool insists on a confirmation message, the user's approval above covers it; proceed with no further question and do not exceed 10 calls. Do not use any other credit-spending Apollo tool (no enrich, no people search/reveal, no contact or account creation). `apollo_organizations_lookup` is free and may be used for discovery. Report exactly how many calls you made.

## How to use it well

- Use per_page 100 and the `organization_locations`, `organization_num_employees_ranges` ("11,50","51,200","201,500"), `q_organization_keyword_tags`, `organization_founded_year_range` filters; vary keywords and location per call so the 10 calls return different companies, and use page 2 only if page 1 is rich. Results hold `primary_domain` (organizations) or `domain` (accounts).
- Save each response's domain list to a scratch file with Python as you go rather than re-reading it. Run check_domains.py on the domains in bulk. Only NEW ones go on to DR (free Ahrefs tool, many per call), then date confirmation.
- Date confirmation routes that worked: `https://DOMAIN/wp-json/wp/v2/posts?per_page=3&_fields=date,link,title`, `/feed/`, `/rss.xml`, sitemaps with lastmod, or the newest post page, through Apify web-fetch (`mcp__Apify_Neu__apify--web-fetch`), then a WebSearch snippet as last resort (note it). Keep Apify under $1.00. Skip large global brands and consumer companies.
- Prioritise companies with 11 to 500 staff and a visible blog.

## Slices

| slice | scope | file | target |
|---|---|---|---|
| AP_A | Segment A: marketing, content, SEO, PR, design, demand gen agencies and martech/video-tech, UK, US and UAE HQ | research2/AP_A.csv | 30 |
| AP_B_UKUAE | Segment B: B2B SaaS, AI, FinTech, HR tech, dev tools, cybersecurity, proptech, legal tech, B2B services, UK and UAE HQ | research2/AP_B_UKUAE.csv | 30 |
| AP_B_US | Segment B, same verticals, US HQ | research2/AP_B_US.csv | 30 |

Output columns, as before: companyName,webDomain,country,serviceType,segment,competitor,competitorReason,domainRating,blogUrl,latestPost,notes. Python csv module. Only rows that pass every rule.

Reply with: rows written, domains screened, Apollo calls made, Apify spend, searches used, competitors flagged.
