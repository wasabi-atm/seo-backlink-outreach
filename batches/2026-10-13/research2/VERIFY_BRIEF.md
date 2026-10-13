# Verification brief for Apollo-sourced candidates: backlink-2026-10-13

Read ../research/RESEARCH_BRIEF.md and BRIEF2.md (this folder) first; all rules apply (HQ UK/US/UAE, DR 40+, live blog with a confirmed dated post since Oct 2025, competitor=yes rows kept, no em or en dashes, no padding).

You get a chunk file `research2/apollo/chunk_N.csv` (webDomain, companyName, country, segment). The domains came from Apollo company search with the HQ country filter already applied (country column; "UK/UAE" means one of the two, confirm which). They are already NEW against the exclusion list. Apollo industry codes are loose, so many are not what you want. Drop: consumer or B2C companies, media sites and publishers, staffing and recruitment firms, schools and non-profits, resellers, anything acquired or redirecting, and anything with no blog.

## Steps (cheapest first)

1. Look at the names and domains and drop obvious non-fits without any spend.
2. Run the free DR tool (`mcp__Ahrefs__public-domain-rating-free`, many domains per call; call `mcp__Ahrefs__doc` with tool "public-domain-rating-free" once first). Drop DR under 40. Only use that Ahrefs tool.
3. For DR 40+ domains, confirm a post dated since Oct 2025. Routes that worked, through `mcp__Apify_Neu__apify--web-fetch` (one call per URL, then read the dataset): `https://DOMAIN/wp-json/wp/v2/posts?per_page=3&_fields=date,link,title`, `/feed/`, `/blog/feed/`, `/rss.xml`, sitemaps with lastmod, the blog index page, then the newest post page for JSON-LD datePublished or a visible date. A WebSearch snippet showing a dated post is the last resort (note it). Up to 25 WebSearch calls.
4. HQ: confirm from the site (footer, contact page, JSON-LD address) when you can; otherwise write "HQ from memory" in notes. Keep the country column honest (UK, US or UAE).
5. Do not use Apollo, Instantly or HubSpot. Keep Apify under $1.00.

## Output

`research2/apollo/verified_N.csv` with columns: companyName,webDomain,country,serviceType,segment,competitor,competitorReason,domainRating,blogUrl,latestPost,notes (same as earlier slices; segment A = marketing/creative-adjacent agencies and martech/video-tech, segment B = other B2B). Python csv module. Only rows that pass every rule.

Reply with a short summary: chunk size, how many passed the name filter, how many passed DR, rows written, Apify spend, searches used, competitors flagged.
