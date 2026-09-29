# Step 3 agent brief: link habits (backlink-2026-09-29)

You check the outbound link habits of 25 company blogs for Motion The Agency's backlink outreach. Your group file lists companyName, webDomain and blogUrl.

The container cannot reach the sites or the Apify API directly (both blocked). Use only the Apify MCP tools (`mcp__apify__call-actor`, `mcp__apify__get-dataset-items`; load them with ToolSearch "select:mcp__apify__call-actor,mcp__apify__get-dataset-items,mcp__apify__get-actor-run").

## 1. Crawl the 25 blog indexes (one run)

`call-actor` actor `apify/website-content-crawler`, waitSecs 45, callOptions.maxTotalChargeUsd 0.5, input:

```
{"startUrls": [{"url": "<blogUrl>"}, ...], "crawlerType": "cheerio", "maxCrawlDepth": 0, "maxCrawlPages": 40,
 "saveMarkdown": true, "maxRequestRetries": 1, "requestTimeoutSecs": 40, "proxyConfiguration": {"useApifyProxy": true}}
```

If the run is still running, poll `get-actor-run` until it finishes. Then `get-dataset-items` with fields "url,markdown", limit 40 (page with offset if long). From each index pick up to 5 of the most recent real article URLs on that company's own site (not category, tag, author, pagination, product, case study, event or webinar pages). Keep the title and date if the index shows them.

A blog index that comes back empty or with no post links: try once more in the second run with `"crawlerType": "playwright:adaptive"` for that URL only, or an obvious alternative path (/blog, /insights, /news, /resources). If still nothing, record it and move on.

## 2. Crawl the chosen posts (one or two runs)

Same actor, startUrls = all chosen post URLs (about 125), `maxCrawlDepth` 0, `maxCrawlPages` 160, maxTotalChargeUsd 1.0, same other settings. Read the markdown with `get-dataset-items` (fields "url,metadata.title,markdown", pages of 15 to 20 items so results stay readable).

## 3. For each company, record from the post bodies

- outsideDomains: distinct root domains of other businesses linked in the article bodies. Ignore the company's own domains, social networks, YouTube, Wikipedia, Google, CDNs and image hosts, form and scheduling tools, government, education and NHS sites.
- quotedCompanies: other companies whose people are quoted (for example "said Jane Doe, CMO at Acme"). Not the company's own staff or its clients shown in its own case studies.
- guestSigns: a "write for us", contributor or guest post page, or posts marked as guest posts, with the URL.
- postsRead: how many posts you actually read.
- posts: the post URLs, titles and dates you read (Step 4 will reuse them to pick one article).
- note: anything odd (redirect to another domain, blog dead or last post over a year ago, the site looks like a different business than expected, gambling or adult content).

Write down only what you saw. Never guess.

## Output

Write `step3/result_<group number>.json` in this folder, a list with one object per company, in the group file's order:

```
{"webDomain": "...", "blogUrlUsed": "...", "postsRead": 5, "outsideDomains": ["hubspot.com", ...],
 "quotedCompanies": ["Acme"], "guestSigns": "", "posts": [{"url": "...", "title": "...", "date": "2026-09-10"}], "note": ""}
```

Every company in your group must have a row, even if nothing could be read (postsRead 0 and a note saying why). Then reply with a short summary: counts, the Apify runs you made and their cost, and any company that could not be read. No em or en dashes in anything you write.
