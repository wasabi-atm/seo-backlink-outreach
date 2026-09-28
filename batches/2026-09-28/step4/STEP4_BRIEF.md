# Step 4 brief: pick one article per company (backlink-2026-09-28)

Working folder: `/home/user/seo-backlink-outreach/batches/2026-09-28` (call it BATCH below).

## What this is for

Motion The Agency (MTA, motiontheagency.com) is a motion design and video studio. It makes animated explainer videos, product demo videos, motion graphics and blog graphics for B2B SaaS, AI and FinTech companies. We are emailing each company below to ask for a link to motiontheagency.com from one of their existing blog articles. In return we offer something free (see "offer" below). Your job is to pick the one article per company where a link to MTA would sit naturally, and to record one specific, checkable hook on that page that the email can open with.

## Your input

`BATCH/step4/in_<N>.csv` (N is given in your task): 25 companies with companyName, webDomain, segment, country, serviceType, domainRating, competitor, competitorDecision, blogUrl, backlinkExchange.

Already on disk for most companies (read these first, they are free):
- `BATCH/step4/posts/<webDomain>/*.md`: up to 5 recent posts (some are service pages), already crawled today with Apify. Line 1 is the URL, line 2 the title, then the page as markdown. If you pick one of these, it already counts as today's live page: no need to crawl it again.
- `BATCH/crawl/blog/<webDomain>.md`: the blog index page as markdown (post titles and links, often 10 to 60 posts). This is your main list of candidate articles. Line 1 is the index URL. Relative links resolve against the site root (watch out: Adido's index links resolve to a doubled `/insights/insights/` path that 404s; try the single `/insights/` path).

## Tools and network

This environment cannot reach company websites directly (curl, WebFetch and the Apify API host are all blocked). Web search is NOT available: the session's search limit is used up, so do not call WebSearch. Use only:
- The files above to find candidate articles by title (grep the blog index markdown for words like video, explainer, demo, onboarding, guide, how to, content, visual, infographic, report).
- The Apify MCP tools to read live pages. Load them with ToolSearch `select:mcp__apify__call-actor,mcp__apify__get-dataset-items`. Use actor `apify/website-content-crawler` with input `{"startUrls":[{"url":...}, ...], "crawlerType":"cheerio", "maxCrawlDepth":0, "maxCrawlPages":<count+5>, "saveMarkdown":true, "maxRequestRetries":1, "requestTimeoutSecs":40, "proxyConfiguration":{"useApifyProxy":true}}`, callOptions `{"memory":2048,"timeout":900}`, waitSecs 0.
  - Put all your chosen URLs (1 or 2 candidates per company, about 50 URLs) into ONE run. At most one more run for retries or failures (for pages cheerio cannot load, the retry may use `"crawlerType":"playwright:adaptive"`). No more than about 80 pages in total.
  - Do not call `get-actor-run` to poll: its output is huge. Poll with `get-dataset-items` on the run's dataset id, `fields:"url"`, `limit:1`, and read `totalItemCount`. Also check the run's `errors` dataset id for failed URLs.
  - Fetch results with `get-dataset-items`, `fields:"url,crawl.loadedUrl,crawl.httpStatusCode,metadata.title,markdown"`, limit about 60. Large results are saved to a file whose path the tool gives you. Copy that file into `BATCH/step4/raw_<N>/` and parse it with python (it is JSON with an `items` list). Do not paste whole pages into your context.

## How to choose the article

Look for articles about SaaS video, B2B video, video marketing, advertising or content marketing. Don't be strict: the test is whether a link to MTA would sit naturally in the article and pass authority to motiontheagency.com. Prefer articles that:
- mention video, explainers, animation, demos, onboarding or visual content, or recommend something MTA could make;
- are live and published or updated within the last two years (after September 2024);
- are NOT listicles of video agencies or video production companies (those link to MTA's competitors).

Segment B companies are not in marketing. For them, pick an article where a short explainer, a product walkthrough, a data graphic or a founder quote would genuinely help the reader: "how X works" guides, onboarding or setup guides, customer education, sales enablement, recruitment or employer branding, reports full of numbers with no chart, and so on.

Prefer a guide or evergreen article over company news, funding announcements, job posts, event recaps or newsletters.

## The hook (most important)

One or two specific things you saw on that live page, taken from the Apify crawl you ran today, written so the reader can check them. Quote exact text where you can. Good hooks:
- the article recommends video, infographics or visuals, or says "watch" or "see the demo", but the page has none;
- a step or section that a short animation would explain better (name the heading);
- a date problem (title says 2024 or 2025 but it is now late September 2026; updated date before published date);
- a broken or placeholder element that shows in the text (for example "Text Link" left in a table of contents, an empty "[video]" embed, "Lorem ipsum");
- a statistic with no source, or two numbers on the page that disagree.

Write what you saw, not a guess. If you cannot confirm anything specific on the live page, say so in `notes` and set fit to weak.

## Output

Write `BATCH/step4/out_<N>.csv` with python's csv module, one row per company in your input (all 25, even dead ones), columns exactly:

`webDomain, articleTitle, articleUrl, articleDate, articleTopic, linkPlacement, articleHook, offer, fit, hookSource, notes`

- articleDate: date shown on the page as YYYY-MM-DD (updated date if shown, otherwise published), else blank.
- articleTopic: a few words.
- linkPlacement: the section where MTA's link fits plus suggested natural anchor text, for example `Under "3. Choose a style"; anchor: animated explainer video`.
- offer: Segment A, and any row with competitorDecision "include", always gets `Founder's quote swap`. Segment B gets whichever one fits the article best: `Video for the blog post`, `Founder's quote`, `Internal data` or `Blog graphic or infographic`.
- fit: `strong` (natural link spot and a solid hook), `ok`, `weak` (thin fit or hook not confirmed), or `dead` (no usable article found; explain in notes).
- hookSource: `live page, Apify crawl 28 Sep 2026`, or say what else you used.
- notes: anything the email writer should know (for example "page loads a paywall", "article is by a guest author", "blog moved to X").

Style for every field: no em dashes or en dashes anywhere (use commas or plain hyphens), plain simple words, British spelling.

Do not edit any other file, do not touch the ledger, do not commit to git.

## When you finish

Reply with a short summary: counts of strong, ok, weak and dead; the weak and dead rows with a one-line reason each; and the number of Apify runs and pages you used.
