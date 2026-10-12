# Step 3 brief: link habits (backlink-2026-10-12-b2)

Working folder: `/home/user/seo-backlink-outreach/batches/2026-10-12-b2` (BATCH below).

Motion The Agency (motiontheagency.com) is a motion design studio doing SEO backlink outreach. For each company in your input we need to know whether its blog links out to other businesses (a sign it would accept a link or a quote swap). We use Apify (Ahrefs paid units are not used): read 3 to 5 recent posts per blog and count the distinct outside business domains they link to in the article body.

DR is already known (free Ahrefs endpoint, checked today (first pass and again in Step 3)): keep `domainRating` from the input, do NOT call any Ahrefs tool.

## Input

`BATCH/step3/in_<N>.csv` (about 16 rows): companyName, webDomain, country, serviceType, segment, visualScore, visualNotes, competitor, competitorDecision, domainRating, blogUrl, latestPost, notes. There is no pool column, leave pool blank in the output.

## Tools

The sandbox cannot reach company sites (curl and WebFetch are blocked). Use Apify only: load with ToolSearch `select:mcp__Apify_Neu__call-actor,mcp__Apify_Neu__get-dataset-items`. Actor `apify/cheerio-scraper` (free apart from tiny compute). Two tested page functions are on disk; pass the file contents exactly as `pageFunction` (build the input JSON with a Python script in your scratchpad and print it):

1. Blog index: `BATCH/step3/indexFunction.js`. ONE run for all rows blog URLs. startUrls = [{"url": blogUrl, "userData": {"domain": webDomain}}]. Input: proxyConfiguration {"useApifyProxy": true}, maxRequestRetries 2, linkSelector "", pageLoadTimeoutSecs 45, maxConcurrency 20. Returns posts (url, title, date) found on the index.
2. Posts: `BATCH/step3/postFunction.js`. ONE run for all chosen post URLs (about 4 per company, so about 64 URLs), same settings, userData.domain = webDomain. Returns published, modified, author, words, outsideDomains (already excludes social networks, Google, CDNs, video hosts and the site's own domain), h2, images, videoEmbeds, quoteHits.

waitSecs 45; if the run is still running, poll with `get-dataset-items` (fields "webDomain", limit 1, read totalItemCount) rather than get-actor-run. Read results with `get-dataset-items` (limit 250, the fields you need); large results are saved to a file whose path the tool gives you: copy it into your scratchpad as `s3_<N>_*.json` (other agents share the scratchpad) and parse it with Python. Do not paste whole results into your context.

Pick posts: from each index take the 4 newest article URLs (by date if shown, else index order, which is usually newest first). Skip pagination, topic pages, product pages, newsletters, job posts and press releases where you can tell. If an index returns no posts (script-rendered blog or blocked), try in one shared retry run: the blog URL with proxyConfiguration {"useApifyProxy": true, "apifyProxyGroups": ["RESIDENTIAL"]}, or `<blog>/feed/`, `/sitemap.xml`, `/post-sitemap.xml`, `/blog/sitemap.xml` with `additionalMimeTypes` ["application/xml", "text/xml", "application/rss+xml"] and a tiny page function that returns every `loc` or `link` text. Keep total Apify spend for your chunk under $0.90 (cheerio runs cost cents; residential retries cost more).

## Scoring

For each company: outsideDomainCount = distinct outside domains across the posts you read. Remove the company's own sister domains or parent brands, app stores, URL shorteners and obvious tracking links before counting. Government, university, standards bodies and news sites count (they show the blog cites outside sources) but note them.

backlinkExchange:
- Yes: 8 or more distinct outside domains across the posts read, or a contributor, guest post or "write for us" page (contributorLink True or seen), or a post quoting a named founder or exec from another company (quoteHits help; check they are outside people).
- Some: 3 to 7 outside domains, or only one weak sign.
- No: 0 to 2 outside domains and no other sign.
- unchecked: no post could be read (say why in notes).

## Output

Write `BATCH/step3/out_<N>.csv` with Python's csv module, one row per input row (all rows, in input order), columns exactly:

companyName,webDomain,domainRating,country,serviceType,segment,visualScore,backlinkExchange,backlinkEvidence,dataSource,competitor,drStatus,videoSchemaGap,latestPost,blogUrl,competitorDecision,pool,postsRead,outsideDomainCount,recentPosts,notes

- backlinkEvidence: one line, e.g. "11 outside domains in 4 posts (gartner.com, hbr.org, statista.com ...); quotes CMO of Acme".
- dataSource: `ahrefs-free DR; apify links`.
- drStatus: `pass` if domainRating is 40 or higher, `low` if under 40.
- videoSchemaGap: blank. visualScore: blank. Carry companyName, country, serviceType, segment, competitor, competitorDecision, pool, latestPost from the input. If the blog URL you actually used differs, put the working one in blogUrl.
- postsRead: number of posts read.
- recentPosts: a JSON list (json.dumps) of up to 12 posts from the index, newest first, each {"url","title","date"}; titles cleaned (strip "Click to read" and category labels glued to the front where obvious) and cut to 100 characters. Step 4 uses this list to pick an article, so include the real post URLs.
- notes: anything odd (blog moved, script-rendered index, posts are all press releases, very thin posts). Update latestPost if you saw a newer dated post.

No em dashes or en dashes anywhere. Do not edit any other file, do not touch the ledger, do not commit to git.

Reply with: rows written, Yes/Some/No/unchecked counts, any row with drStatus low, the unchecked rows with reasons, and Apify runs and approximate spend.


Extra notes for this batch:

- The input `blogUrl` and `latestPost` come from the research agents and can be approximate (a different path such as insights, resources, news, a blog subdomain, month-only dates). If the given blogUrl returns no posts, find the real blog index from the homepage links. Script-rendered blogs: use the sitemap or WordPress REST (`/wp-json/wp/v2/posts?_fields=date,link`, readable through `apify/web-fetch`) or feed retry from the brief, and mark `unchecked` with the reason only if nothing works. Update latestPost when you see a real date.
- All rows are competitor "no" (none flagged). Several agencies and studios offer video as one of many services (fox.agency, threerooms.com, fantasticmedia.co.uk, healthcaresuccess.com, ignitesocialmedia.com, godfrey.com). Score them like the rest and say in notes if the blog is mostly about video or animation work.
- gurucul.com and veem.com could not be loaded at vetting (they block Apify). If you also cannot read their blogs, mark `unchecked` and write "blocks Apify" in notes.
- limble.com was limblecmms.com. buildingengines.com is owned by JLL but runs its own domain. regal.ai moved from regal.io.
- Rows with HQ notes in `visualNotes` are context only. Do not use `visualNotes` except as context.
- Do not call any Ahrefs tool: DR is already rechecked today.
