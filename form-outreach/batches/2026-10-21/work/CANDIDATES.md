# Candidate finder (Motion The Agency backlink form outreach, 2026-10-21)

Motion The Agency (motiontheagency.com) is a motion graphics / animation / video studio. We want sites to approach for a backlink swap via their contact form. You only FIND candidates; do not visit contact forms, do not type into anything. Unattended: do not ask questions.

Find companies that:
- are based in (head office or main market) your assigned countries
- have roughly 11 to 500 staff (skip household names / public companies / obviously huge firms)
- run a real company blog with posts about video marketing, B2B video, SaaS video, content marketing, advertising, social media, brand, demand gen, or posts that recommend video/visuals (published or updated in the last 2 years)
- Segment A = marketing and creative adjacent but NOT a competitor: content marketing and SEO agencies, B2B marketing / demand gen agencies, PR and comms firms, web and brand design studios (only if they do not sell video/animation), podcast production, marketing SaaS tools, video hosting/video tech platforms.
- Segment B = B2B SaaS, AI, FinTech, HR tech, dev tools, B2B services with a real marketing-ish blog.
- NOT competitors: skip any company whose main offer is making video, animation, explainers or motion design for other companies.
- Skip link farms, sites that sell guest posts/link placements, and blogs full of off-topic listicles.

Exclusion: a domain list of everyone already contacted is at
/home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-21/work/exclude_domains.txt (one root domain per line, no www).
Before adding a candidate, check it is not in that file: `grep -ix "<domain>" exclude_domains.txt`, and ALSO check the brand name across TLDs: `grep -i "^<brand>\." exclude_domains.txt` (e.g. hallam.agency vs hallam.co.uk count as the same). Drop any match. Check in batches with a small python script to save time.

How to find them: WebSearch (mode standard) queries like "B2B content marketing agency Manchester blog", "SaaS marketing agency Sydney", "video marketing guide site:.co.uk blog", "HR software blog employer branding video", "fintech blog content marketing Singapore", Clutch/DesignRush style lists (use them only to get names, then confirm the domain), and your own knowledge of real companies. Prefer companies likely to have Ahrefs DR 40+ (established sites with real backlinks), mid-size, with a contact page.

Output: write a CSV with header
companyName,webDomain,country,serviceType,segment,articleHint
to the output file you are given (country codes: UK, US, UAE, AU, SG; webDomain = bare root domain, no www, no path; articleHint = a URL of a relevant blog post if you saw one, else blank). Target the number of rows you are given, all unique and all NOT in the exclusion file. Accuracy of the domain matters more than volume. No em or en dashes. Reply with just the row count when done.

## Notes for this run (2026-10-21)
- ROUND 2. About 8,700 domains are already excluded (everyone contacted or researched before), so the obvious, well-known names are gone. Dig into the long tail: regional and city-level agencies (smaller cities too), niche vertical SaaS (proptech, legal tech, edtech, B2B healthtech, logistics, construction, nonprofit, hospitality, ecommerce tools, field service, church/membership software, events), Shopify/HubSpot app vendors, martech tools, PR and comms firms, B2B fintech, and niche marketing agencies (healthcare, dental, law firm, higher ed, nonprofit, manufacturing, B2B tech marketing, franchise marketing).
- Agencies and marketing tools pass our later form check far more often than mid-size SaaS (SaaS sites often only have demo forms). Aim for roughly two thirds Segment A unless your brief says otherwise.
- Favour companies that have a real contact, partnerships, press or "write for us" page with a general form (not only "book a demo").
- Prefer established sites likely to have Ahrefs DR 40+ (around for 8+ years, real clients, press mentions, active blog).
- Do not use Ahrefs. Use WebSearch (mode standard) and your own knowledge. If WebSearch stops working (budget used up), continue from your own knowledge of real companies, but only add domains you are confident are correct.
- Write the CSV with Python's csv module so commas in names are quoted.
- Round 1 lesson: mid-size vertical SaaS mostly had demo-only forms or no form at all, and many agencies sell video (competitors). What passed: agencies and marketing SaaS tools with a general contact or partnership form and an active marketing blog, nonprofit/comms consultancies, B2B SaaS that write marketing advice for their customers (salon, fitness, restaurant, field service, membership, events) AND have a plain contact form. Prefer companies whose contact page has a general form with a message box.
