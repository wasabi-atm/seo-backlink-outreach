# Step 5 contacts brief (backlink-2026-09-30)

BATCH = /home/user/seo-backlink-outreach/batches/2026-09-30/round2, REPO = /home/user/seo-backlink-outreach, scripts in REPO/skill/mta-backlink-outreach/scripts/.
Read REPO/skill/mta-backlink-outreach/SKILL.md, section "Contact waterfall", and follow it. Targets: BATCH/03_backlink_targets.csv (50 companies). Role groups: BATCH/step5/domains.json ("founder": 29 founder's quote rows, want founder, co-founder, CEO or MD; "content": 21 Segment B rows, want head of content or content marketing, else head of marketing or CMO).

User caps (hard limits, never exceed, counted for the WHOLE 30 Sep run): Instantly 200 credits (Instantly is connected now; workspace credits were 1163 on 29 Sep, check `workspace_billing_plan_details` first), Apollo 150 lead credits in total of which 81 are already used, so at most 69 more (balance was 793 after the first pass), Apify $1 in total of which about $0.20 is already used, so at most about $0.80 more. Check balances before each paid pass and stop a source when its cap would be passed.

Tools: load with ToolSearch. Instantly (`mcp__Instantly__*`), Apollo (`mcp__Apollo_io__*`), Apify (`mcp__apify__*`). The Apify API host and company sites are blocked from this machine, so the website step runs through Apify (cheerio-scraper reading home, contact and about pages), not `contacts.py site`.

## Already done

Nothing for this round. Create a new Instantly list "Backlink 2026-09-30 round 2 contacts" when you use SuperSearch. The first 101 companies already have contacts in /home/user/seo-backlink-outreach/batches/2026-09-30/step5/contacts.csv; do not touch that file. Use round2/step5/contacts.csv for these 50. Apify tools may be mcp__apify__* or mcp__Apify_Neu__*. Reject picks whose email is on another company's domain, but note parent-company domains as "parent domain" instead of dropping them silently.

## Steps

1. Export the list with `list_leads` (list_id, limit 100, paginate with starting_after). Save each page as JSON in your scratchpad (prefix c5_), then `python3 /home/user/seo-backlink-outreach/batches/2026-09-29/step5/export_leads.py BATCH/step5/leads_instantly.csv <pages...>`.
2. `python3 contacts.py pick BATCH/step5/leads_instantly.csv BATCH/step5/contacts.csv --source instantly --targets BATCH/03_backlink_targets.csv`. Look over the picks: reject anyone at the wrong company (a matching domain can still be another firm), an email on another company's domain, or someone junior when a better person exists. Write rejects with a reason to BATCH/step5/leads_instantly_rejected.csv.
3. `contacts.py todo BATCH/03_backlink_targets.csv BATCH/step5/contacts.csv -o BATCH/step5/todo.csv`. If the founder import was cut short, rerun the founder search for the founder domains still missing. Then one broader Instantly pass on what is left: founder domains any founder, owner, CEO, MD or head of marketing; content domains any marketing leadership (Head of Marketing, Marketing Director, CMO, VP Marketing), then founder or CEO. Use `enrichment_count` and `enrichment_preview` (free) first, import into the same list with `resource_id`, `show_one_lead_per_company` true, `work_email_enrichment` true, `skip_rows_without_email` true. Export and pick again (another leads_instantly2.csv).
4. Apollo for what is still missing (`todo -o todo_apollo.csv`): `apollo_mixed_people_api_search` (free) by q_organization_domains_list and person_titles, choose one person per company, reveal with `apollo_people_bulk_match` (10 per call, by id). Only verified emails. Save leads_apollo.csv (same columns as leads_instantly.csv) and `pick --source apollo`.
5. Apify `peakydev/leads-scraper-ppe` for what is left (companyDomain list, personTitle, maxPerCompany 3, totalResults about 3 per domain, callOptions.maxTotalChargeUsd within the remaining Apify cap). Map organizationWebsite to webDomain, title to jobTitle. Save leads_apify.csv and `pick --source apify`.
6. Website contact email for anything still left: Apify cheerio-scraper on the homepage and /contact, /contact-us, /about pages, pageFunction returning every mailto and every email pattern in the text. Keep only addresses on the company's own domain (hello@, info@, contact@ first; never careers@, privacy@, no-reply@, press@ unless nothing else). Add these rows to contacts.csv with source site and emailType generic, in the same columns contacts.py writes.
7. `contacts.py merge BATCH/03_backlink_targets.csv BATCH/step5/contacts.csv -o BATCH/step5/targets_contacts.csv`.
8. Instantly campaign check: for every email in targets_contacts.csv call `search_campaigns_by_contact` (read only, about 15 in parallel per message). Write BATCH/step5/campaign_check.csv with email, webDomain, instantlyCampaign (campaign names joined with "; ", blank if none).

Rules: never guess or pattern-build an email. People marked isOwned in an Instantly preview are already in the workspace: note them. No em or en dashes in any file. Do not touch the ledger, do not run git, do not write emails.

## Reply

Short summary: companies with a named person, with a shared inbox, with nothing; credits used per source (Instantly, Apollo, Apify dollars) and balances after; rejected picks with reasons; emails already in an Instantly campaign with the campaign name.
