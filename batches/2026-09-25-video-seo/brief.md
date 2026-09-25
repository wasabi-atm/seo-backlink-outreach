# Brief: Video SEO (video-seo-2026-09-25)

- Goal: 100 SaaS companies whose homepage has a video but no VideoObject schema (videoSchemaGap = yes). The email opens with the two fixed video lines from Step 5 of the skill.
- Countries: UK, US and UAE. Size: 11 to 1,000 staff.
- Companies first; contacts added later on request through the contact waterfall (see the log).
- Skip every company already in outreach_ledger.csv (330 on 25 Sep, all backlink campaigns).
- Not logged in the ledger yet, as nothing is emailed. When emails are queued, log them with campaign `video-seo-2026-09-25`.

## Progress log

- Candidates, part 1: 180 SaaS rows from past candidate pools (2026-09-23-b and 2026-09-25 00_candidates, low_dr_pool) that were never emailed. Apollo free lookup (no credits) kept 134 in the 11 to 1,000 staff range. Dropped 15: acquired or merged (Clari, Qualified, Pento, ClearVoice, Terminus/DemandScience, Egress, Banked, RollWorks), HubSpot customer or open deal (Blink, Pipedrive, Tillo), not SaaS (Audioboom, Swvl). 119 left, 0 removed by dedupe: 00_candidates_old.csv.
- Candidates, part 2: new companies from Apollo free lookup (SIC 7372 software with the saas keyword tag, 11 to 1,000 staff), one agent per country: US 230 (7 dropped as far over 1,000 staff or a parent's domain), UK 160, UAE 90.
- The gap rate was only about 8%, so round 3 used Apollo's tech filter (sites using Vimeo, Vidyard, Brightcove or JW Player, plus YouTube for UAE): US 287, UK 202, UAE 70. Its gap rate was about twice as high. Wistia was left out of the filter on purpose, as its player usually adds VideoObject by script.
- 1,148 homepages rendered with video_schema.py (6 render runs plus a retry of timeouts). During the run the rule for a plain video tag was tightened to need player controls, because React sites set muted as a property and looping UI animations were counting as video. The first three runs' plain-video hits were rendered again under the new rule (video_retry).
- Apify dev00/google-rich-results-checker, through the Apify MCP only, on every homepage with a video and no VideoObject in the render: 183 runs (about $0.37). 176 loaded with no VideoObject, 6 blocked the actor (the rendered page was used), 1 error (petex.com, left unknown). No page came back TRUE.
- Dropped by title while screening (drop.txt): casted.us (domain now an adult site), UKG, DICE, Flo, Disperse (now OpenSpace), Exafy, Zap (web agency), FairFace, Vicon (hardware), GSS, Redmill, Forensic Analytics, Demica (FIS), Dye & Durham, Ceribell, Empatica, Lumafield, D-ID (Israel), Digistore24 (Germany), Alchemy Group (agency), Decibel360 (Pakistan), SamTech, BE Club, Magnet Forensics (Canada).
- HubSpot (company domain search): dropped Dext (customer, open deal), MetaCompliance, Bluebeam and 73 Strings (open deals). Harvey, Ideagen, GumGum and Biz2X are leads with no open deal and stay in.
- Possible competitor held back: Icon (icon.com, AI video ad maker, title "The Agency | Icon"). It is at the end of the spares until the user decides.
- 178 companies with videoSchemaGap yes (01_video_gap.csv). 02_video_seo_list.csv has the 100: all 21 UAE, 40 UK, 39 US, ranked so that pages Apify read directly and named players come first. 02_video_seo_spares.csv has the other 78. Dedupe against the ledger on the final 100: 0 removed.
- Contacts (user asked, 25 Sep), waterfall Instantly, Apollo, Apify, website, all through MCP tools:
  - Instantly SuperSearch, 2 passes into the list "Video SEO 2026-09-25 enrichment" (76 credits): 60 companies. Dropped picks whose email sat on another company's domain (ntop.com for XYZ Reality, incorta.com for Causaly, amili.asia for Opus, bexelconsulting.com for BEXEL) and a fractional marketer mapped to Ideagen.
  - Apollo people search plus 28 lead credits of reveals: 25 companies.
  - Apify peakydev/leads-scraper-ppe, one run by domain (the title filter returned nothing), about $0.43: 9 companies. Engineers, sales and finance staff were skipped; Servme's COO was kept as a last resort.
  - Website contact email (contacts.py site): 5 companies, plus POP's parent sales inbox from its contact page.
  - All 100 have an email: 94 named people, 6 shared inboxes. Dedupe with emails: 0 removed.
  - Instantly campaign check: 9 emails are already in a campaign (Seez, Altruistiq, Alphalake, Mercaux, Harvey, Medallion, Posit, Board, Addepar). Flagged in instantlyCampaign; waiting on the user.
  - 03_video_seo_contacts.csv is the list with contacts; manualCheck notes on 11 rows.
- SEO owner pass (user asked, 25 Sep: the contact should be whoever is in charge of SEO or the website). The first pass mixed many marketing titles with one lead per company, so only 1 contact was an SEO person. Free Instantly preview and Apollo search for SEO and web titles on all 100 found an SEO lead or website owner at about 20 companies (Adit's and Milestone's large SEO teams mostly serve clients). Imported them by name in Instantly (14 credits, 9 emails), revealed the rest in Apollo (11 credits, 7 verified), and Apify found Pinewood's SEO manager (3 small runs, about $0.55). contacts.py pick --focus seo --upgrade replaced 18 contacts. Now 17 contacts are SEO or website owners; for the rest, no SEO or web person exists in any source and the marketing lead, content lead or founder stays. SocialPilot's SEO Manager has no email anywhere; Netlify's web project manager only has an extrapolated email, so its verified growth director was kept.
- None of the 18 new emails is in an Instantly campaign. Posit, Board and Addepar no longer use the CMO who is in a campaign, but the company overlap is noted. 6 contacts are still in other campaigns (Seez, Altruistiq, Alphalake, Mercaux, Harvey, Medallion).
- Re-validation (user asked, 25 Sep evening; their manual Rich Results Test check flagged Netacea, which turned out correct: its only Video item is a hero clip, the real video has no schema):
  - Apify dev00 actor re-run through the Apify API with the user's token, 16 runs at a time (the actor takes one URL per run), full results in video_v2/apify_raw/. 172 of 178 without VideoObject, 6 blocked, 0 with it.
  - Found the systematic error: the local ISP (XL Axiata) blocks player.vimeo.com, and a Vimeo player page carries its own VideoObject that Google's Rich Results Test counts for the host page when the player is visible at load. player_scan.py (now `video_schema.py players`) lists the players each homepage loads the Google way.
  - Rich Results Test by hand: Posit, Toggl, JumpCloud no Video item; Netacea hero only; Altruistiq no Video (hidden player); Alpheya and Tribepad a Video item from the Vimeo player.
  - Result for the 178: 126 real gaps, 36 not gaps (a real Vimeo player at load), 16 check (the only video is a Vimeo hero loop). Main 100: 69 yes, 22 no, 9 check. Spares: 57 yes, 14 no, 7 check.
  - Validation files for the user: 04_video_seo_all.csv and 05_validate_part1-4.csv (45, 45, 45, 43 rows) with a Rich Results Test link per row and an empty yourCheck column.
  - An Apify Playwright run from the cloud was tried and aborted (too slow with a tall viewport; cost $0.04). google_view.py belonged to it and is unused.
  - The deep render in video_schema.py now matches Google (Googlebot phone, tall viewport, no scrolling), so JumpCloud's scroll-only VideoObject no longer counts.
