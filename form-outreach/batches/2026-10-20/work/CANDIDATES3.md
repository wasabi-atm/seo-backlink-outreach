# Candidate finder, round 3 (2026-10-20)

Find agencies and small B2B companies for a Motion The Agency (motion design / video studio) backlink outreach batch sent through contact forms. You only produce a list of NAMES + DOMAINS with a DR check. Another worker opens every site in a browser later, so you do NOT need to fetch any website. Unattended: never ask questions.

Tools: load with ToolSearch `select:mcp__Ahrefs__public-domain-rating-free,WebSearch`. Use public-domain-rating-free (free; pass up to 100 domains in one call) to check DR. WebSearch (mode standard) is optional and its budget is small and shared, so use at most 8 searches, mostly to find agency directory or "top agencies in <city>" pages for names. Mostly rely on your own knowledge of real companies.

Want (in your assigned slice):
- Ahrefs DR 40 or more (check every domain; drop under 40 or 0).
- Roughly 11 to 200 staff. Real companies with an active blog (insights, news, journal).
- Agencies: SEO, PPC, content marketing, B2B marketing, inbound/HubSpot partners, PR and comms, web design and development, branding, ecommerce agencies, social media agencies. NOT agencies that list video production, animation, motion graphics or explainer videos as a service (competitors), and not link building / guest post sellers.
- Agencies tend to have simple "Contact us" forms with a message box, which is what we need.

Exclusion: /home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-20/work/exclude_domains.txt (about 7,200 root domains already contacted or checked). Drop exact matches and brand matches across TLDs (`grep -i "^<brand>\." file`). Check with one small python script before the DR call.

Output CSV header: companyName,webDomain,country,serviceType,segment,articleHint,drFree
(country UK, US, AU, SG or UAE; segment A for marketing/creative adjacent, B for other B2B; articleHint blank unless you know a real post URL). No em or en dashes. Write to your output file. Target 30 rows that pass DR 40. Reply with just the row count.
