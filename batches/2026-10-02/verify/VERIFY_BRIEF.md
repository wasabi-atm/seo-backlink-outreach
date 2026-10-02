# Verify brief: manual checks for backlink-2026-10-02 emails

Folder: /home/user/seo-backlink-outreach/batches/2026-10-02/verify. Input: verify/in_<N>.csv (12 rows): webDomain, companyName, articleUrl, articleTitle, articleHook, emailBody, manualCheck. Output: verify/out_<N>.csv.

Each row is a cold email (from Sam of Motion The Agency, a motion design studio) about one blog article. The email makes claims about the live page, and the row's manualCheck says a browser check is needed because the original crawl was plain HTML (it may have missed content that loads by script, such as images, charts, videos, diagrams, tables, tabs).

## What to do

The cloud network blocks company sites, so use Apify. Load `mcp__apify__call-actor` and `mcp__apify__get-dataset-items` (or the `mcp__Apify_Neu__` versions) with ToolSearch. Use actor `apify/website-content-crawler` with crawlerType "playwright:adaptive" (a real rendered page), startUrls = all 12 articleUrls in ONE run, maxCrawlDepth 0, saveMarkdown true, saveHtml true if available, proxyConfiguration {"useApifyProxy":true}, callOptions {"memory":4096,"timeout":900,"maxTotalChargeUsd":0.40}, waitSecs 0. Poll with get-dataset-items fields "url" limit 1 and read totalItemCount; do not call get-actor-run. Fetch results with fields "url,crawl.httpStatusCode,metadata.title,markdown,html" and a limit; large results are saved to a file, copy it to your scratchpad and parse with python. For a page that fails or returns a bot check, retry those once. Total Apify spend for you: under $0.80.

For each row, read the email and list every factual claim about the page (quotes, headings, "no chart/video/image", counts, dates, "empty table of contents"). Check each against the rendered page (markdown plus html: look for img, picture, svg, video, iframe, canvas, table tags and alt text where the claim is about a missing visual). Then give a verdict:
- `confirmed`: every claim holds on the rendered page.
- `fix`: a claim is wrong or no longer true (page has an image, video, chart or the text differs). Give the exact corrected sentence or say what to cut.
- `unverifiable`: page blocked, a bot check, or content cannot be read; say what is unknown.

## Output

verify/out_<N>.csv with columns: webDomain, verdict, evidence, suggestedFix. evidence is one or two plain sentences saying what you saw (quote exact page text where useful). suggestedFix is blank for confirmed. No em or en dashes anywhere (use commas). Do not edit any other file, the emails, the ledger or Instantly, and do not commit.

Reply with counts of confirmed, fix and unverifiable, and the fix and unverifiable rows with one line each, plus Apify runs and estimated spend.
