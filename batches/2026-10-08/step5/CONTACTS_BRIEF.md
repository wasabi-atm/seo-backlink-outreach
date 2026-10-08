# Step 5 contacts brief (backlink-2026-10-08)

BATCH = /home/user/seo-backlink-outreach/batches/2026-10-08, REPO = /home/user/seo-backlink-outreach, scripts in REPO/skill/mta-backlink-outreach/scripts/.
Read REPO/skill/mta-backlink-outreach/SKILL.md, section "Contact waterfall", and follow it.

Two agents work in parallel, each on its own half (N = 0 or 1, given in your task). Only touch files with your N.

- Targets: BATCH/step5/targets_<N>.csv (63 companies).
- Role groups: BATCH/step5/domains_<N>.json. "founder": founder's quote swap rows, want Founder, Co-Founder, CEO, Owner or Managing Director (for a big company where the founder is out of reach, head of marketing or CMO is fine). "content": the Segment B rows offered a video, graphic or founder's quote, want Head of Content, Content Marketing Manager or Lead, Editor, Head of Marketing, CMO or Marketing Director.
- Your contacts file: BATCH/step5/contacts_<N>.csv (contacts.py creates it). Your Instantly list: "Backlink 2026-10-08 contacts <N>".

User caps for YOUR half (hard limits, never exceed): Instantly 125 credits, Apollo 3 lead credits for N=0 and 4 for N=1 (Apollo has only 7 in total until 10 Oct), Apify $0.50. Check `workspace_billing_plan_details` (credits.available_credits) and `apollo_usage_stats_credit_usage_stats` (lead_credit.left_over) before and after each paid pass, and stop a source when its cap would be passed. The other agent spends from the same balances at the same time, so measure your spend by what you imported or revealed, not only by the balance change, and report both.

Tools: load with ToolSearch. Instantly (`mcp__Instantly__*`; if ToolSearch finds none, wait a moment and search again, the server reconnects), Apollo (`mcp__Apollo_io__*`), Apify (`mcp__Apify_Neu__*`). Company sites and the Apify API host are blocked from this machine, so the website step runs through Apify cheerio-scraper, not `contacts.py site`.

## Steps

0. Instantly SuperSearch imports per SKILL.md: pass 1 founder titles for the "founder" domains, pass 2 content titles for the "content" domains. Free `enrichment_count` and `enrichment_preview` first; import with `enrichment_enrich`, `show_one_lead_per_company` true, `work_email_enrichment` true, `skip_rows_without_email` true, list_name as above (second pass adds to the same list with `resource_id`). Wait until `enrichment_get` shows in_progress false.
1. Export the list with `list_leads` (list_id, limit 100, paginate with starting_after). Save each page as JSON in your scratchpad (prefix c<N>_), then `python3 /home/user/seo-backlink-outreach/batches/2026-09-29/step5/export_leads.py BATCH/step5/leads_instantly_<N>.csv <pages...>`.
2. `python3 contacts.py pick BATCH/step5/leads_instantly_<N>.csv BATCH/step5/contacts_<N>.csv --source instantly --targets BATCH/step5/targets_<N>.csv`. Look over the picks: reject anyone at the wrong company (a matching domain can still be another firm), an email on another company's domain, or someone junior when a better person exists. Write rejects with a reason to BATCH/step5/rejected_<N>.csv.
3. `contacts.py todo BATCH/step5/targets_<N>.csv BATCH/step5/contacts_<N>.csv -o BATCH/step5/todo_<N>.csv`. One broader Instantly pass on what is left (founder domains: any founder, owner, CEO, MD or head of marketing; content domains: any marketing leadership, then founder or CEO). Free count and preview first, import into the same list, export and pick again (leads_instantly2_<N>.csv).
4. Apollo for what is still missing (`todo -o todo_apollo_<N>.csv`): `apollo_mixed_people_api_search` (free) by q_organization_domains_list and person_titles, choose one person per company, reveal with `apollo_people_bulk_match` (10 per call, by id). Only verified emails. Save leads_apollo_<N>.csv (same columns as the Instantly leads file) and `pick --source apollo`.
5. Apify `peakydev/leads-scraper-ppe` for what is left (companyDomain list, personTitle, maxPerCompany 3, totalResults about 3 per domain, callOptions.maxTotalChargeUsd within your remaining Apify cap). Map organizationWebsite to webDomain, title to jobTitle. Save leads_apify_<N>.csv and `pick --source apify`.
6. Website contact email for anything still left: Apify cheerio-scraper on the homepage and /contact, /contact-us, /about pages, with a pageFunction returning every mailto and every email pattern in the text. Keep only addresses on the company's own domain (hello@, info@, contact@ first; never careers@, privacy@, no-reply@, press@ unless nothing else). Add these rows to contacts_<N>.csv with emailSource website and emailType generic, in the same columns contacts.py writes.
7. Instantly campaign check: for every email in contacts_<N>.csv call `search_campaigns_by_contact` (read only, about 15 in parallel per message). Write BATCH/step5/campaign_check_<N>.csv with email, webDomain, instantlyCampaign (campaign names joined with "; ", blank if none).

Rules: never guess or pattern-build an email. People marked isOwned in an Instantly preview are already in the workspace: note them. No em or en dashes in any file. Do not touch the ledger, do not run git, do not write emails.

## Reply

Short summary: companies with a named person, with a shared inbox, with nothing; credits used per source (Instantly, Apollo, Apify dollars) and balances after; rejected picks with reasons; emails already in an Instantly campaign with the campaign name.

## Batch notes

- Competitor rows (quote swap only, founder or CEO wanted): rotorvideos.com and plainlyvideos.com.
- Moved or renamed brands: cyera.io now serves cyera.com; fieldguide.io now serves fieldguide.com; abnormalsecurity.com is abnormal.ai; constructor.io is constructor.com; augmentir.com is augmentir.ai; tuffgrowth.com is part of Goodway Group (goodwaygroup.com); webolutions.com is webolutionsmarketingagency.com; emperor.works is a London agency. Search by both domains where a company has two.
- Parents and owners: Fictiv (fictiv.com) is owned by MISUMI; Stainless (stainless.com) is joining Anthropic; Nearpod (nearpod.com) is owned by Renaissance (renaissance.com): they are separate rows, pick a different person for each; Paycor (paycor.com) is owned by Paychex; Mimecast, Avalara, Fivetran and Sovos are large.
- Big companies (the founder is out of reach, so take the head of content or marketing, or a content or communications lead): Yotpo, Bazaarvoice, AdRoll, BigCommerce, CJ, impact.com, Mimecast, Avalara, Skillsoft, Insperity, Fivetran, Sysdig, Q2, Paysafe, HackerRank, CoreWeave, LangChain, Abnormal, Sovos, Paycor.
- Instantly credits: about 298 available in total (cap 125 per agent, 250 total). Apollo has only 7 lead credits left in total until 10 Oct, so your cap is 3 or 4 as above: spend them only on the companies that matter most, or none.
- Export helper: python3 /home/user/seo-backlink-outreach/batches/2026-09-29/step5/export_leads.py (if missing, write the CSV from the list_leads JSON yourself).
- The Instantly MCP server disconnects now and then. If its tools are missing, search again with ToolSearch after a moment and retry before giving up on a pass.
