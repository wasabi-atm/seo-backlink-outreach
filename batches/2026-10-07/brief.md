# Brief: backlink-2026-10-07

- Target: 160 sites at DR 40 or higher, 80 in Segment A and 80 in Segment B. UK and UAE first, then US. Plus a 40 site buffer carried through Steps 3 and 4 (best 160 kept).
- Segment A offer: founder's quote swap. Each founder gives a quote for the other's article and both link back.
- Segment B offers: video for the blog post, founder's quote, internal data (MTA figures they can cite), blog graphic or infographic. Pick whichever fits the article best.
- Sender: Sam. Offer paid placement if they don't want a swap.
- Excluded domains: none given beyond the ledger. Ledger before this run: 1311 rows.
- Batch shape: 160 sites, 80 A / 80 B, vetted in chunks of 40.

## Progress log

- Sync (7 Oct): main pulled, session branch claude/awesome-archimedes-n8zrlt equals origin/main (4a81c97). Repo SKILL.md followed (it is newer than the claude.ai copy: re-upload the zip per README).
- Interview answered (7 Oct): all defaults as above, all four Segment B offers allowed.
- Network: cloud proxy blocks company sites (hubspot.com 403), no Chrome in PATH for webscreenshotter and no .venv, so Apify route again, no screenshots, no video schema check.
- exclude_domains.txt (3022 root domains) built by build_exclude.py: ledger, pool, form master, client lists, all earlier batch files. Yesterday's unused spares (98, reusable_spares.txt) are NOT excluded so they can be reused.
