# Homepage vetting brief: backlink-2026-10-06

Input: a domain list file named in your task (one root domain per line).
Output: the CSV named in your task, columns:
webDomain,loaded,finalUrl,redirectedToOtherDomain,adNetworks,farmWords,writeForUs,parked,outboundLinks,wordCount,title,h1,blogLink,notes

The cloud network blocks company sites, so use Apify: `mcp__Apify_Neu__call-actor` with actor `apify/cheerio-scraper`, ONE run for all homepages.
- Input: startUrls = [{"url": "https://<domain>", "userData": {"domain": "<domain>"}} ...], pageFunction = the exact contents of
  /home/user/seo-backlink-outreach/batches/2026-10-06/step2/pageFunction.js (tested, works), proxyConfiguration {"useApifyProxy": true},
  maxRequestRetries 2, linkSelector "", pageLoadTimeoutSecs 45, maxConcurrency 30. waitSecs 45; if the run is still running, poll with
  `mcp__Apify_Neu__get-actor-run` until it finishes. Cheerio scraper is free apart from tiny compute.
- Read results with `mcp__Apify_Neu__get-dataset-items` (limit 250, fields "webDomain,finalUrl,adNetworks,farmWords,writeForUs,parked,outboundLinks,wordCount,title,h1,blogLink").
- Domains missing from the dataset failed to load. Retry them once in a second run with proxyConfiguration {"useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"]}, and also try "https://www.<domain>" as the start URL. Keep the residential run small; cap with callOptions.maxTotalChargeUsd 0.50 if asked. Anything still missing gets loaded=False.
- redirectedToOtherDomain: True when the root domain of finalUrl differs from the input domain AND it is not obviously the same brand (e.g. directus.io -> directus.com is the same brand, so False but say so in notes). Compute root domains with
  `python3 -c "import sys; sys.path.insert(0,'/home/user/seo-backlink-outreach/skill/mta-backlink-outreach/scripts'); from dedupe import root_domain; print(root_domain('<url>'))"` or in a small Python script.
- Write the CSV with Python's csv module (write the dataset JSON to a scratch file first, then convert), so commas in titles are quoted. No em dashes or en dashes anywhere (replace with a comma or hyphen).

notes: flag hard fails here (do not delete rows): "HARD FAIL: does not load", "HARD FAIL: parked", "HARD FAIL: redirects to <domain>", "HARD FAIL: ad network <x>", "HARD FAIL: farm word <x>" for casino, betting, sportsbook, cbd, payday. "loans", "viagra" or "escort" alone: write "check: farm word <x>" and add the sentence it appears in if you can see it (a business lender saying "loans" is fine). Also note "write for us" when writeForUs is True (not a fail). If the title or h1 suggests the site is a different business from the domain (for example a parked page or an unrelated company), say so.

Reply with: rows written, loaded count, hard fails (domain and reason), checks, failed loads, Apify spend.
