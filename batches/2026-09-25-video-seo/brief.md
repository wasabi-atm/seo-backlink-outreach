# Brief: Video SEO (video-seo-2026-09-25)

- Goal: 100 SaaS companies whose homepage has a video but no VideoObject schema (videoSchemaGap = yes). The email opens with the two fixed video lines from Step 5 of the skill.
- Countries: UK, US and UAE. Size: 11 to 1,000 staff.
- Companies only for now. No contacts, no Apollo credits.
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
