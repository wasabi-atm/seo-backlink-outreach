# Steps 3 + 4 combined brief (backlink-2026-10-13)

Working folder: `/home/user/seo-backlink-outreach/batches/2026-10-13` (BATCH below). Today is 2026-10-13.

Motion The Agency (MTA, motiontheagency.com) is a motion design and video studio (animated explainers, product demos, motion graphics, blog graphics for B2B SaaS, AI and FinTech). We email each company below to ask for a link to motiontheagency.com from one of their existing blog articles, offering something free in return. For each company you do two jobs from the same crawl: (A) check link habits, (B) pick the one article where an MTA link would sit naturally and record a checkable hook.

DR is already known (free Ahrefs tool): keep `domainRating` from the input. Do NOT call any Ahrefs tool. Do not call Apollo, Instantly, HubSpot. Do not edit any other file, do not touch the ledger, do not commit to git. WebSearch: at most 10 calls, last resort only.

## Input and output

Input: `BATCH/step34/in_<N>.csv` (about 25 rows): companyName, webDomain, country, serviceType, segment, domainRating, blogUrl, latestPost, notes. blogUrl and latestPost come from research agents and can be wrong or approximate (blog may be at /insights, /resources, /news, a subdomain, or the research agent left the site root). Notes may say "HQ from memory" and how the date was confirmed.
Output: `BATCH/step34/out_<N>.csv`, Python csv module, one row per input row in input order (all rows, even dead ones), columns exactly:

webDomain,backlinkExchange,backlinkEvidence,postsRead,outsideDomainCount,blogUrl,latestPostConfirmed,articleTitle,articleUrl,articleDate,articlePublished,publishedSource,articleTopic,linkPlacement,articleHook,offer,fit,hookSource,notes

## Tools (the sandbox cannot reach company sites; use Apify only)

Load with ToolSearch `select:mcp__Apify_Neu__call-actor,mcp__Apify_Neu__get-dataset-items,mcp__Apify_Neu__apify--web-fetch`.
Apify is shared with 11 other agents: memory is scarce and runs can queue. Use small memory (1024), do not abort queued runs, wait and retry. Prefer a few BIG batched runs over many small ones. Keep total Apify spend for your chunk under $0.80.

1. Blog index: actor `apify/cheerio-scraper`, ONE run for all rows. pageFunction = exact contents of `BATCH/step34/indexFunction.js` (build the run input JSON with a Python script and print it). startUrls = [{"url": blogUrl, "userData": {"domain": webDomain}}], proxyConfiguration {"useApifyProxy": true}, maxRequestRetries 2, linkSelector "", pageLoadTimeoutSecs 45, maxConcurrency 20. Returns posts (url, title, date).
2. Posts: same actor, ONE run for chosen post URLs with `BATCH/step34/postFunction.js` (userData.domain = webDomain). Returns published, modified, author, words, outsideDomains (own domain, socials, Google, CDNs and video hosts already excluded), h2, images, videoEmbeds, quoteHits. Choose about 4 posts per company: the 4 newest articles (skip pagination, topic pages, product pages, newsletters, job posts, press releases) and make sure your candidate article(s) for job B are among them.
3. To READ a chosen article's text for the hook, use `apify/website-content-crawler` (crawlerType "cheerio", maxCrawlDepth 0, saveMarkdown true, proxyConfiguration {"useApifyProxy": true}, memory 1024) with one or two candidate URLs per company in ONE run (at most about 40 pages for your chunk). For JS-rendered pages retry with `"crawlerType":"playwright:adaptive"` or use `mcp__Apify_Neu__apify--web-fetch`.
4. If an index returns no posts: try `<blog>/feed/`, `/rss.xml`, `/sitemap.xml`, `/post-sitemap.xml`, `/blog/sitemap.xml`, `/wp-json/wp/v2/posts?per_page=10&_fields=date,link,title` via web-fetch (these worked on about half of sites in earlier rounds).
5. Do not poll with get-actor-run (huge output). Poll with get-dataset-items on the run's dataset id, fields "url", limit 1, read totalItemCount. Large results are saved to a file; copy it into the scratchpad as `s34_<N>_*.json` (unique names, others share the scratchpad) and parse with Python. Never paste whole pages into context.

## Job A: backlinkExchange

outsideDomainCount = distinct outside business domains linked in the article bodies of the posts read (remove sister domains, parent brands, app stores, shorteners, tracking links). Government, university, standards bodies and news sites count.
- Yes: 8 or more distinct outside domains, or a contributor / guest post / "write for us" page, or a post quoting a named founder or exec from another company.
- Some: 3 to 7 outside domains, or one weak sign.
- No: 0 to 2 and no other sign.
- unchecked: no post could be read (say why in notes).
backlinkEvidence: one line, e.g. "11 outside domains in 4 posts (gartner.com, hbr.org ...); quotes CMO of Acme".

## Job B: pick one article and a hook

Look for articles about SaaS video, B2B video, video marketing, advertising or content marketing. Not strict: the test is whether a link to MTA would sit naturally in the article and pass authority. Prefer articles that mention video, explainers, animation, demos, onboarding or visual content, or recommend something MTA could make; are live and published or updated after October 2024; and are NOT listicles of video agencies (they link to MTA's competitors). Segment B companies are not in marketing: pick an article where a short explainer, product walkthrough, data graphic or founder quote would genuinely help (how-X-works guides, onboarding and setup guides, customer education, sales enablement, recruiting, reports full of numbers with no chart). Prefer guides and evergreen pieces over news, funding, jobs, event recaps, newsletters.

Live blog check: confirm at least one post dated after 2025-10-13 on the post itself (page date, article:published_time, JSON-LD, or sitemap lastmod); put the newest date you saw in latestPostConfirmed (YYYY-MM-DD, or YYYY-MM if only the month is known). If the blog is dormant or nothing dated since Oct 2025 can be confirmed, set fit `dead`.

The hook (most important): one or two specific, checkable things you saw on the live page, quoted exactly where you can: the article recommends video or visuals but the page has none; a step a short animation would explain better (name the heading); a date problem (title says 2024 or 2025; updated date before published date); a broken or placeholder element ("Text Link" left in a table of contents, empty "[video]" embed, "Lorem ipsum"); a statistic with no source, or two numbers that disagree. Write what you saw, not a guess. If you cannot confirm anything specific, say so in notes and set fit `weak`.

Fields:
- articleDate: date shown on the page (YYYY-MM-DD; updated date if shown, else published), else blank.
- articlePublished: first published date YYYY-MM-DD from page code (article:published_time, JSON-LD datePublished, time tag), else the date on the page, else blank. publishedSource: `page code`, `page text`, `url or index` or blank. If first published before October 2024, say so in notes.
- articleTopic: a few words.
- linkPlacement: section where MTA's link fits plus a natural anchor, e.g. `Under "3. Choose a style"; anchor: animated explainer video`.
- offer: Segment A always `Founder's quote swap`. Segment B: whichever fits best of `Video for the blog post`, `Founder's quote`, `Internal data`, `Blog graphic or infographic`.
- fit: `strong` (natural link spot and a solid, confirmed hook), `ok`, `weak` (thin fit, forced link, or hook not confirmed), `dead` (no usable article or no dated post since Oct 2025).
- hookSource: `live page, Apify crawl 13 Oct 2026` or what else you used (e.g. "index snippet only").
- notes: anything the email writer should know (paywall, guest author, blog moved, "HQ looks non-US/UK/UAE", company sells video or visual content, large corporate, etc.). If you see evidence the HQ is outside UK/US/UAE or the company is a competitor (makes videos, animation or motion graphics for other companies), say so plainly.

Style: no em dashes or en dashes anywhere (commas or plain hyphens), plain simple words, British spelling.

## When you finish

Reply with a short summary: counts of Yes/Some/No/unchecked, counts of strong/ok/weak/dead, any HQ or competitor concerns, and Apify runs, pages and approximate spend.
