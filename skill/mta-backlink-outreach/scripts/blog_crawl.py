"""Blog crawl built on crawl4ai (local Playwright Chromium). NOT part of the normal Step 4 any more:
Step 4 reads sites with WebFetch (see "Crawling websites (WebFetch first)" in SKILL.md). This script
reaches websites through the shell, which is blocked in cloud sessions, so it is only an optional
Mac-only tool. It costs no Apify credits.

    python blog_crawl.py 02_enriched.csv crawl/ [--workers 4] [--max-pages 40] [--depth 2]

The CSV needs webDomain. An optional blogUrl column skips the blog-index guess for that row.
For every domain it finds the blog index, crawls pages on the blog's host reachable from it
(skipping pricing, login, docs and similar), and writes:

  crawl/<domain>/<n>.md   markdown of each page (first line is the URL, second the title)
  crawl/articles.csv      one row per page: webDomain, url, title, published, wordCount, isListing, mdFile
  crawl/summary.csv       one row per domain: webDomain, blogUrl, pages, articles, error

Setup (once per machine, Python 3.10+):
  python3.12 -m venv .venv-crawl
  .venv-crawl/bin/pip install -U crawl4ai
  .venv-crawl/bin/crawl4ai-setup        # downloads Playwright Chromium
  .venv-crawl/bin/crawl4ai-doctor       # optional check
"""
import argparse, asyncio, csv, os, re, sys, time
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.filters import DomainFilter, FilterChain, URLPatternFilter

# Tried in order when the homepage has no obvious blog link.
BLOG_PATHS = ["/blog", "/resources/blog", "/insights", "/articles", "/resources", "/learn", "/news"]
BLOG_WORDS = re.compile(r"/(blog|insights|articles|resources|learn|news|guides|library)(/|$)", re.I)
LISTING = re.compile(r"/(page|tags?|categor(y|ies)|authors?|topics?)/|[?&][\w-]*page=", re.I)
# Posts often live outside the blog path (/post/..., or at the root), so the crawl follows any
# page on the blog's host except these sections, which are never articles. Links in nav, header,
# footer and sidebars are ignored too, so the crawl follows the post list rather than the site menu.
SKIP_SECTIONS = ["pricing", "plans", "login", "signin", "sign-in", "signup", "sign-up", "register", "demo",
                 "contact", "contact-us", "about", "about-us", "company", "team", "careers", "jobs", "legal",
                 "privacy", "privacy-policy", "terms", "cookie-policy", "security", "status", "docs", "api",
                 "integrations", "partners", "services", "solutions", "features", "product", "products",
                 "platform", "customers", "case-studies", "reviews", "locations", "cart", "checkout",
                 "wp-admin", "wp-json", "feed", "cdn-cgi", "search"]
NOT_ARTICLE = [p for sec in SKIP_SECTIONS for p in (f"*/{sec}", f"*/{sec}/", f"*/{sec}/*", f"*/{sec}?*")] + \
              ["*.pdf", "*.jpg", "*.jpeg", "*.png", "*.webp", "*.zip", "*.xml", "*#*"]
CHROME_TAGS = ["nav", "header", "footer", "aside"]


class CappedBFS(BFSDeepCrawlStrategy):
    """crawl4ai's BFS checks max_pages against pages already crawled, not pages already queued,
    so every page on a level can queue another max_pages links. Count the queue too."""

    async def link_discovery(self, result, source_url, current_depth, visited, next_level, depths):
        crawled = self._pages_crawled
        self._pages_crawled = crawled + len(next_level)
        try:
            await super().link_discovery(result, source_url, current_depth, visited, next_level, depths)
        finally:
            self._pages_crawled = crawled


def clean_domain(d):
    d = d.strip().lower()
    d = re.sub(r"^https?://", "", d).split("/")[0]
    return d[4:] if d.startswith("www.") else d


def page_config(**kw):
    return CrawlerRunConfig(cache_mode=CacheMode.BYPASS, page_timeout=45000, wait_until="domcontentloaded",
                            exclude_external_images=True, verbose=False, **kw)


def internal_links(result):
    return [l.get("href", "") for l in (result.links or {}).get("internal", [])]


async def find_blog(crawler, domain, given):
    """Returns the blog index URL, or '' if none was found."""
    if given:
        return given if given.startswith("http") else "https://" + given
    home = await crawler.arun("https://" + domain, config=page_config())
    if home.success:
        host = urlparse(home.url).netloc
        hits = [h for h in internal_links(home) if BLOG_WORDS.search(urlparse(h).path)]
        # Prefer a link that is the index itself (/blog), not a post under it.
        hits.sort(key=lambda h: (urlparse(h).path.rstrip("/").count("/"), "blog" not in h.lower()))
        for h in hits:
            if urlparse(h).netloc in (host, "") or urlparse(h).netloc.endswith("." + domain):
                return h.split("#")[0]
        base = f"https://{host}"
    else:
        base = f"https://{domain}"
    for path in BLOG_PATHS:
        r = await crawler.arun(base + path, config=page_config())
        if r.success and (r.status_code or 200) < 400 and urlparse(r.url).path.rstrip("/") != "":
            return r.url
    return ""


async def crawl_domain(crawler, domain, given, out_dir, args):
    blog = await find_blog(crawler, domain, given)
    if not blog:
        return blog, [], "no blog index found"
    u = urlparse(blog)
    filters = FilterChain([
        DomainFilter(allowed_domains=[u.netloc]),
        URLPatternFilter(patterns=NOT_ARTICLE, reverse=True),
    ])
    cfg = page_config(excluded_tags=CHROME_TAGS, deep_crawl_strategy=CappedBFS(
        max_depth=args.depth, max_pages=args.max_pages, filter_chain=filters))
    results = await crawler.arun(blog, config=cfg)
    rows, seen, d_dir = [], set(), os.path.join(out_dir, domain)
    os.makedirs(d_dir, exist_ok=True)
    for i, r in enumerate(results if isinstance(results, list) else [results]):
        key = r.url.split("#")[0].rstrip("/")
        if not r.success or key in seen:
            continue
        seen.add(key)
        md = str(r.markdown.raw_markdown if hasattr(r.markdown, "raw_markdown") else r.markdown or "")
        meta = r.metadata or {}
        title = (meta.get("title") or meta.get("og:title") or "").strip()
        published = (meta.get("article:published_time") or meta.get("article:modified_time") or "")[:10]
        md_file = os.path.join(d_dir, f"{i:03d}.md")
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(f"{r.url}\n{title}\n\n{md}")
        rows.append(dict(webDomain=domain, url=r.url, title=title, published=published,
                         wordCount=len(md.split()),
                         isListing=(r.url.rstrip("/") == blog.rstrip("/") or urlparse(r.url).path.strip("/") == ""
                                    or bool(LISTING.search(r.url))),
                         mdFile=os.path.relpath(md_file, out_dir)))
    return blog, rows, "" if rows else "blog index found but no pages crawled"


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("out_dir")
    ap.add_argument("--workers", type=int, default=4, help="domains crawled at once")
    ap.add_argument("--max-pages", type=int, default=40, help="pages per domain")
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=300, help="seconds per domain")
    args = ap.parse_args()

    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        todo = [(clean_domain(r["webDomain"]), (r.get("blogUrl") or "").strip())
                for r in csv.DictReader(f) if r.get("webDomain", "").strip()]
    os.makedirs(args.out_dir, exist_ok=True)

    browser = BrowserConfig(headless=True, text_mode=True, verbose=False,
                            extra_args=["--no-sandbox", "--disable-dev-shm-usage"])
    sem = asyncio.Semaphore(args.workers)
    all_rows, summary = [], []

    async with AsyncWebCrawler(config=browser) as crawler:
        async def one(domain, given):
            async with sem:
                t = time.time()
                try:
                    blog, rows, err = await asyncio.wait_for(
                        crawl_domain(crawler, domain, given, args.out_dir, args), args.timeout)
                except asyncio.TimeoutError:
                    blog, rows, err = given, [], f"timed out after {args.timeout}s"
                except Exception as e:  # one bad site must not stop the batch
                    blog, rows, err = given, [], f"{type(e).__name__}: {e}"[:200]
                arts = sum(1 for r in rows if not r["isListing"])
                print(f"{domain}: {len(rows)} pages, {arts} articles, {time.time() - t:.0f}s {err}", flush=True)
                all_rows.extend(rows)
                summary.append(dict(webDomain=domain, blogUrl=blog, pages=len(rows), articles=arts, error=err))
        await asyncio.gather(*(one(d, g) for d, g in todo))

    order = {d: i for i, (d, _) in enumerate(todo)}
    all_rows.sort(key=lambda r: (order[r["webDomain"]], r["url"]))
    summary.sort(key=lambda r: order[r["webDomain"]])
    for name, rows, cols in [
        ("articles.csv", all_rows, ["webDomain", "url", "title", "published", "wordCount", "isListing", "mdFile"]),
        ("summary.csv", summary, ["webDomain", "blogUrl", "pages", "articles", "error"]),
    ]:
        with open(os.path.join(args.out_dir, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)

    failed = [s for s in summary if s["error"]]
    print(f"\nDone: {len(summary)} domains, {len(all_rows)} pages. {len(failed)} need a retry or a blogUrl:")
    for s in failed:
        print(f"  {s['webDomain']}: {s['error']}")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
