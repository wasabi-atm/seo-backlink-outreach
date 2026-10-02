# Homepage vetting brief: backlink-2026-10-02

Input: /home/user/seo-backlink-outreach/batches/2026-10-02/00_candidates_clean.csv (159 rows, column webDomain).
Output: /home/user/seo-backlink-outreach/batches/2026-10-02/vetting.csv with columns
webDomain,loaded,finalUrl,redirectedToOtherDomain,adNetworks,farmWords,writeForUs,outboundLinks,wordCount,title,notes

The cloud network blocks company sites, so use Apify (mcp__Apify_Neu__call-actor, actor apify/cheerio-scraper, one run for all homepages, callOptions.maxTotalChargeUsd 0.40). Call mcp__Apify_Neu__fetch-actor-details first for the input schema. Page function: for each homepage record final URL, title, text word count, count of distinct external hostnames linked, script/iframe/link src hosts matching ad networks (doubleclick, googlesyndication, adsbygoogle, taboola, outbrain, mgid, revcontent, adnxs, criteo, media.net, amazon-adsystem), farm words in the visible text (casino, betting, sportsbook, cbd, payday, loans, viagra; only count visible text, not script code), and any link or text for "write for us", "guest post", "contribute". Set proxyConfiguration {useApifyProxy:true}, and use a few retries. Read results with mcp__Apify_Neu__get-dataset-items (limit 200). For domains that fail to load, retry once with apify proxy group RESIDENTIAL only if cost stays under the cap, else mark loaded=False.

Hard fails to flag in notes (do not delete rows): site does not load, parked, redirects to a different company domain, adNetworks not empty, farmWords includes casino, betting, sportsbook, cbd or payday.
No em dashes or en dashes in anything you write. Reply with: rows written, hard fails (domain and reason), failed loads, Apify spend.
