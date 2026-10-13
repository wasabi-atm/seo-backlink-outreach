# Contact search via Apify leads scraper (backlink-2026-10-13)

Input: /home/user/seo-backlink-outreach/batches/2026-10-13/step5/todo_apify.csv (column webDomain, plus country/segment). These companies still have no contact. Goal: one marketing/content/founder contact with an email per company.

Use the Apify MCP (load with ToolSearch `select:mcp__Apify_Neu__call-actor,mcp__Apify_Neu__get-dataset-items,mcp__Apify_Neu__fetch-actor-details`). Actor `peakydev/leads-scraper-ppe`: read its input schema first (fetch-actor-details). Input as the schema allows: companyDomain = the domains (up to 100 per run; do two runs if more), personTitle = [Head of Content, Content Marketing, Head of Marketing, Marketing Director, VP Marketing, Chief Marketing Officer, Head of Growth, Founder, CEO, Owner, Managing Director], maxPerCompany 3, totalResults about 3 x number of domains. Cost is about $0.10 per run plus $0.0017 per lead; set maxTotalChargeUsd 2.00. Do not use Apollo, Instantly or Ahrefs.

Read results with get-dataset-items (limit 500; big results are saved to a file, copy it into your scratchpad and parse with Python, never paste whole results). Map to a CSV `step5/leads_apify.csv` with columns exactly: webDomain, firstName, lastName, jobTitle, email, location, linkedinUrl. webDomain must be the TARGET company domain from todo_apify.csv (match organizationWebsite / companyDomain back to it), NOT the email domain. Keep only rows with an email. Keep up to 3 people per company, the script picks one.

Then run: `python3 /home/user/seo-backlink-outreach/skill/mta-backlink-outreach/scripts/contacts.py pick step5/leads_apify.csv step5/contacts.csv --source apify --targets targets_step5.csv` from /home/user/seo-backlink-outreach/batches/2026-10-13, then `contacts.py todo targets_step5.csv step5/contacts.csv -o step5/todo_site.csv`.

Reply with: leads returned, companies covered, companies still missing (count), Apify spend. No em or en dashes in files. Do not touch other files or git.
