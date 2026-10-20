# Candidate finder, round 2 (Motion The Agency backlink form outreach, 2026-10-20)

Motion The Agency (motiontheagency.com) is a motion graphics / animation / video studio. We approach sites for a backlink swap via their website contact form. Round 1 failed mostly because big SaaS companies only have "book a demo" forms. This round you PRE-QUALIFY each candidate. Unattended: never ask questions. Never type into or submit any form.

Tools: load WebSearch, WebFetch and mcp__Ahrefs__public-domain-rating-free with ToolSearch first (`select:WebSearch,WebFetch,mcp__Ahrefs__public-domain-rating-free`). Do not use any other Ahrefs tool (no units left). Use WebSearch mode "standard".

A candidate must:
1. Be based in your assigned country, roughly 11 to 500 staff (no public companies or household names).
2. Have Ahrefs DR 40 or more: check with public-domain-rating-free (free, pass a list of up to 50 domains at once). Drop anything under 40.
3. Have a general contact, partnerships, press or "write for us"/contribute page with a FORM that has a free text message box and is NOT a demo/sales/quote form (no required budget, revenue, company size, seats, services-to-buy fields). Check with WebFetch on the contact page (try the link from the homepage, or /contact, /contact-us). Many WordPress sites render the form in HTML (Contact Form 7, Gravity Forms, WPForms, HubSpot embeds show as script). If you see a form with a message/textarea field, or a HubSpot/Typeform embed on a page titled Contact with "general enquiry"-style copy, keep it and write the contact URL in formHint. If the contact page only has emails, a calendar booking, or "book a demo", drop it.
4. Have a blog post on its own domain about video marketing, B2B/SaaS video, content marketing, advertising, social media, brand, or a post that recommends video/visual content, published or updated on or after 2024-10-20. Put that URL in articleHint (from WebSearch `site:domain video` or the blog index via WebFetch).
5. Not be a competitor (anyone whose main offer is making video, animation, explainers or motion design for others), not sell guest posts or link placements, not a link farm.

Good hunting grounds: marketing, SEO, PR, web design and branding agencies (without video services); martech and sales tools; ecommerce tools; event and hospitality tech; HR and L&D tech; nonprofit tech; B2B service firms with real blogs; companies with genuine "write for us" or "contribute" forms. Searches like "<city> B2B marketing agency blog video", "\"write for us\" marketing SaaS", "<industry> software blog video marketing", "contact us partnerships form <industry> software".

Exclusion: /home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-20/work/exclude_domains.txt holds every domain already contacted or checked (one root domain per line). Drop exact matches AND brand matches across TLDs (grep -i "^<brand>\." on the file). Check before spending time on a site.

Output CSV header: companyName,webDomain,country,serviceType,segment,articleHint,formHint,drFree
country codes UK, US, UAE, AU, SG. segment A (marketing/creative adjacent, not competitor) or B (other B2B). webDomain bare root, no www. No em or en dashes. Write the rows to your output file as you go (append), so progress is saved. Aim for the target row count; quality over volume. Reply with just the row count.
