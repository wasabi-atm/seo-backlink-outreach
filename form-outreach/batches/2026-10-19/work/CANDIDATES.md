# Candidate finder (Motion The Agency backlink form outreach, 2026-10-19)

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
/home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-19/work/exclude_domains.txt (one root domain per line, no www).
Before adding a candidate, check it is not in that file: `grep -ix "<domain>" exclude_domains.txt`, and ALSO check the brand name across TLDs: `grep -i "^<brand>\." exclude_domains.txt` (e.g. hallam.agency vs hallam.co.uk count as the same). Drop any match. Check in batches with a small python script to save time.

How to find them: WebSearch (mode standard) queries like "B2B content marketing agency Manchester blog", "SaaS marketing agency Sydney", "video marketing guide site:.co.uk blog", "HR software blog employer branding video", "fintech blog content marketing Singapore", Clutch/DesignRush style lists (use them only to get names, then confirm the domain), and your own knowledge of real companies. Prefer companies likely to have Ahrefs DR 40+ (established sites with real backlinks), mid-size, with a contact page.

Output: write a CSV with header
companyName,webDomain,country,serviceType,segment,articleHint
to the output file you are given (country codes: UK, US, UAE, AU, SG; webDomain = bare root domain, no www, no path; articleHint = a URL of a relevant blog post if you saw one, else blank). Target the number of rows you are given, all unique and all NOT in the exclusion file. Accuracy of the domain matters more than volume. No em or en dashes. Reply with just the row count when done.
