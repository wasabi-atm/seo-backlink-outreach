# Step 3 brief: DR and link habits (backlink-2026-10-02)

Input: step3/in_<n>.csv (about 38 domains). Output: step3/out_<n>.csv. Folder: /home/user/seo-backlink-outreach/batches/2026-10-02/

For each webDomain:

1. Call `mcp__Ahrefs__doc` once for each endpoint before first use.
2. Domain rating: use the FREE `mcp__Ahrefs__public-domain-rating-free` (targets list, all your domains in one call). Do NOT use the paid `site-explorer-domain-rating` (units are low this month: about 33,000 left until 30 Oct). Record it in domainRating, dataSource ahrefs-free.
3. Link habits: `mcp__Ahrefs__site-explorer-linked-domains` with target the domain, mode "subdomains", limit 50 (not 100, to save units), ordered by links if possible, selecting just the domain and link count fields. Count distinct outside business domains the site links out to (ignore social networks, CDNs, the company's own other domains, Google, Apple app stores, and obvious spam or gambling domains). Do NOT pull referring domains, backlink stats or `site-explorer-backlinks-stats`.
4. Also note any contributor or guest post page, "write for us", expert roundup, or posts quoting outside founders, if you see signs of them in the linked domains or in the input notes. Do not crawl sites (the network blocks them).

backlinkExchange:
- Yes: 30 or more distinct outside business domains, or a contributor or guest post page, or recent posts quote outside founders.
- Some: 10 to 29 domains, or one of the other signs is weak.
- No: under 10.

If Ahrefs signs out or returns an out-of-units or limit error, stop, write what you have, and mark the remaining rows backlinkExchange "unchecked".

Output columns, in this order:
companyName,webDomain,domainRating,country,serviceType,segment,visualScore,backlinkExchange,backlinkEvidence,dataSource,competitor,drStatus,videoSchemaGap,latestPost,blogUrl,competitorDecision

- backlinkEvidence: one line, e.g. "45 outside business domains linked; top: hubspot.com, hbr.org, gartner.com".
- dataSource: ahrefs (or ahrefs-free for DR from the free endpoint).
- drStatus: pass if DR 40+, low if under 40, unknown if no DR.
- videoSchemaGap blank. Carry the other columns from the input.
- No em or en dashes anywhere.

Reply with a short summary: rows done, Yes/Some/No/unchecked counts, any DR under 40, Ahrefs units used if shown.


Units are tight: do not call any endpoint other than the free DR tool and `site-explorer-linked-domains` with limit 50. Report the units used (the tool result shows units-cost-total). If you see the limit hit, stop and mark the rest unchecked.
