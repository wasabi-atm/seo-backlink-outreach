# Step 4 brief: pick one article per company (backlink-2026-10-09)

Working folder: `/home/user/seo-backlink-outreach/batches/2026-10-09` (call it BATCH below).

## What this is for

Motion The Agency (MTA, motiontheagency.com) is a motion design and video studio. It makes animated explainer videos, product demo videos, motion graphics and blog graphics for B2B SaaS, AI and FinTech companies. We are emailing each company below to ask for a link to motiontheagency.com from one of their existing blog articles. In return we offer something free (see "offer" below). Your job is to pick the one article per company where a link to MTA would sit naturally, and to record one specific, checkable hook on that page that the email can open with.

## Your input

`BATCH/step4/in_<N>.csv` (N is given in your task): 10 companies with companyName, webDomain, segment, country, serviceType, domainRating, competitor, competitorDecision, blogUrl, backlinkExchange, latestPost, notes, and recentPosts (a JSON list of up to 12 recent posts with url, title and date, read from the blog index during Step 3 today).

Start from recentPosts. If none of them fits (see "How to choose"), pull a longer list of titles from the blog index page 2, a category page or the sitemap (see Tools), then pick.

## Tools and network

This environment cannot reach company websites directly (curl, WebFetch and the Apify API host are all blocked). Do not call WebSearch. Use only:
- To list more candidate articles: `apify/cheerio-scraper` on the blog index page 2, a category page or the sitemap, with the tested page function in `BATCH/step3/indexFunction.js` (pass the file contents as pageFunction; userData.domain = webDomain), then grep the titles for video, explainer, demo, onboarding, guide, how to, content, visual, infographic, report. Many indexes today render post cards without links in plain markdown, so do not rely on website-content-crawler markdown for the index. A sitemap (`/sitemap.xml`, `/post-sitemap.xml`) also lists post URLs with lastmod dates. cheerio-scraper ignores maxTotalChargeUsd, so cap it with timeout and memory.
- The Apify MCP tools to read live pages. Load them with ToolSearch `select:mcp__Apify_Neu__call-actor,mcp__Apify_Neu__get-dataset-items`. Use actor `apify/website-content-crawler` with input `{"startUrls":[{"url":...}, ...], "crawlerType":"cheerio", "maxCrawlDepth":0, "maxCrawlPages":<count+5>, "saveMarkdown":true, "maxRequestRetries":1, "requestTimeoutSecs":40, "proxyConfiguration":{"useApifyProxy":true}}`, callOptions `{"memory":2048,"timeout":900}`, waitSecs 0.
  - Put all your chosen URLs (1 or 2 candidates per company, about 20 URLs) into ONE run. At most one more run for retries or failures (for pages cheerio cannot load, retry with `"htmlTransformer":"none"` or `"crawlerType":"playwright:adaptive"`). No more than about 40 pages in total for your chunk.
  - Do not call `get-actor-run` to poll: its output is huge. Poll with `get-dataset-items` on the run's dataset id, `fields:"url"`, `limit:1`, and read `totalItemCount`. Also check the run's `errors` dataset id for failed URLs.
  - Fetch results with `get-dataset-items`, `fields:"url,crawl.loadedUrl,crawl.httpStatusCode,metadata.title,markdown"`, limit about 60. Large results are saved to a file whose path the tool gives you. Copy that file into your scratchpad as `s4_<N>_*.json` (other agents share the scratchpad) and parse it with python (it is JSON with an `items` list). Do not paste whole pages into your context.

## How to choose the article

Look for articles about SaaS video, B2B video, video marketing, advertising or content marketing. Don't be strict: the test is whether a link to MTA would sit naturally in the article and pass authority to motiontheagency.com. Prefer articles that:
- mention video, explainers, animation, demos, onboarding or visual content, or recommend something MTA could make;
- are live and published or updated within the last two years (after October 2024);
- are NOT listicles of video agencies or video production companies (those link to MTA's competitors).

Segment B companies are not in marketing. For them, pick an article where a short explainer, a product walkthrough, a data graphic or a founder quote would genuinely help the reader: "how X works" guides, onboarding or setup guides, customer education, sales enablement, recruitment or employer branding, reports full of numbers with no chart, and so on.

Prefer a guide or evergreen article over company news, funding announcements, job posts, event recaps or newsletters.

## The hook (most important)

One or two specific things you saw on that live page, taken from the Apify crawl you ran today, written so the reader can check them. Quote exact text where you can. Good hooks:
- the article recommends video, infographics or visuals, or says "watch" or "see the demo", but the page has none;
- a step or section that a short animation would explain better (name the heading);
- a date problem (title says 2024 or 2025 but it is now October 2026; updated date before published date);
- a broken or placeholder element that shows in the text (for example "Text Link" left in a table of contents, an empty "[video]" embed, "Lorem ipsum");
- a statistic with no source, or two numbers on the page that disagree.

Write what you saw, not a guess. If you cannot confirm anything specific on the live page, say so in `notes` and set fit to weak.

## Output

Write `BATCH/step4/out_<N>.csv` with python's csv module, one row per company in your input (all of them, even dead ones), columns exactly:

`webDomain, articleTitle, articleUrl, articleDate, articlePublished, publishedSource, articleTopic, linkPlacement, articleHook, offer, fit, hookSource, notes`

- articleDate: date shown on the page as YYYY-MM-DD (updated date if shown, otherwise published), else blank.
- articlePublished: the first published date as YYYY-MM-DD, read from the page code in the Apify result (article:published_time meta, JSON-LD datePublished, a time tag), else the date shown on the page, else blank. publishedSource: `page code`, `page text`, `url or index` or blank. If the article was first published more than two years ago (before October 2024), say so in notes.
- articleTopic: a few words.
- linkPlacement: the section where MTA's link fits plus suggested natural anchor text, for example `Under "3. Choose a style"; anchor: animated explainer video`.
- offer: Segment A, and any row with competitorDecision "include", always gets `Founder's quote swap`. Segment B gets whichever one fits the article best: `Video for the blog post`, `Founder's quote`, `Internal data` or `Blog graphic or infographic`.
- fit: `strong` (natural link spot and a solid hook), `ok`, `weak` (thin fit or hook not confirmed), or `dead` (no usable article found; explain in notes).
- hookSource: `live page, Apify crawl 9 Oct 2026`, or say what else you used.
- notes: anything the email writer should know (for example "page loads a paywall", "article is by a guest author", "blog moved to X").

Style for every field: no em dashes or en dashes anywhere (use commas or plain hyphens), plain simple words, British spelling.

Do not edit any other file, do not touch the ledger, do not commit to git.

## When you finish

Reply with a short summary: counts of strong, ok, weak and dead; the weak and dead rows with a one-line reason each; and the number of Apify runs and pages you used.

## Notes for this batch

- Input columns: companyName, webDomain, country, serviceType, segment, visualScore, visualNotes, competitor, competitorDecision, domainRating, blogUrl, latestPost, notes, backlinkExchange, backlinkEvidence, dataSource, drStatus, videoSchemaGap, postsRead, outsideDomainCount, recentPosts, pool. Keep the pool column out of your output. `recentPosts` was built by the Step 3 agents and some titles are rebuilt from URL slugs, so confirm each article title on the live page.
- No competitors this batch. Segment A is always `Founder's quote swap`. Segment B offers: `Video for the blog post`, `Founder's quote`, `Internal data` or `Blog graphic or infographic`, whichever fits the article best.
- Live blog check: for every company, confirm at least one article with a date after October 2025 (page date, article:published_time, JSON-LD or sitemap lastmod on the post itself). If the blog is dormant, set fit `dead` and say so in notes.
- Unchecked for link habits (blog renders by script or blocks cheerio): federato.ai, intellum.com, taxdome.com. List posts from the sitemap, a category page or recentPosts and try playwright:adaptive in your retry run. TaxDome returned 403 on cheerio even through residential proxy, so say plainly in notes if it cannot be read.
- Known date doubts: yospace.com (dates inferred), nextroll.com (posts show no dates), hiddenlayer.com (newest dated post 2026-07-31), conductorone.com (one post dated 2023), rebuyengine.com (slow blog), searchberg.com and clinked.com (weak fit). Companies that may redirect: auditboard.com is now optro.ai, conductorone.com is now c1.ai, cleverbridge.com blog is grow.cleverbridge.com/blog, matchboxdesigngroup.com works only without www.
- Held at Checkpoint 1 but kept by the user: inventry.co.uk and mpulsesoftware.com (doubleclick on the homepage). Treat them as normal rows.
- Some sites have no strong video angle (security vendors, infrastructure software, tax and payments). Still pick the best article, but set fit `weak` if a link to MTA would look forced.
- Do not read from other batch folders; those companies are already contacted.
