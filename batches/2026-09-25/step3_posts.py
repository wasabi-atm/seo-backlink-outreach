"""Step 3, part 1: pick up to 5 recent post URLs per approved site from its crawled blog index
(crawl/blog/<domain>.md), and note any contributor or guest-post page linked from the homepage or blog.
Writes step3/posts_plan.json and step3/crawl_posts_in.json (Apify website-content-crawler input)."""
import csv, json, os, re
from urllib.parse import urlparse, urljoin

def root(h):
    h = (h or "").lower().split(":")[0]
    return h[4:] if h.startswith("www.") else h

SKIP = re.compile(r"/(category|categories|tag|tags|topic|topics|author|authors|page|feed|search|login|signin|sign-in|signup|"
                  r"pricing|product|products|features|solutions|platform|about|careers|jobs|contact|demo|legal|privacy|terms|"
                  r"cookie|events?|webinars?|podcasts?|case-stud(y|ies)|customers|partners|integrations|docs|help|support|"
                  r"subscribe|newsletter|press|glossary|practice|services?|sectors?|policies|enquiry|resources|investors|"
                  r"blog-posts|brand-stories|whitepapers-and-reports|knowledge)(/|$)|(form|get-in-touch|book-a-demo|"
                  r"how-to-get-started|data-as-a-service|field-marketing-event-kit)(/|$)|\.cfm$", re.I)
MEDIA = re.compile(r"\.(png|jpe?g|gif|webp|svg|avif|pdf|mp4|zip)(\?|$)", re.I)
CONTRIB = re.compile(r"(write-for-us|writeforus|contribute|contributor|guest-post|guest-author|submit-a-post|become-a-contributor)", re.I)
LINK = re.compile(r"\]\((https?://[^\s)\"]+|/[^\s)\"]*)")

prospects = list(csv.DictReader(open("01_prospects.csv")))
os.makedirs("step3", exist_ok=True)
plan, urls = {}, []
for p in prospects:
    d = p["webDomain"]
    f = f"crawl/blog/{d}.md"
    md = open(f).read() if os.path.exists(f) else ""
    blog_url = md.split("\n", 1)[0].strip() if md else p["blogUrl"]
    bpath = urlparse(blog_url).path.rstrip("/")
    home = ""
    for hd in (d, p.get("oldDomain") or ""):
        if hd and os.path.exists(f"crawl/home/{hd}.md"):
            home = open(f"crawl/home/{hd}.md").read()
    contrib = sorted({urljoin(blog_url, u) for u in LINK.findall(md + home) if CONTRIB.search(u)})
    posts = []
    for u in LINK.findall(md):
        u = urljoin(blog_url, u).split("#")[0].split("?")[0]
        pu = urlparse(u)
        if not (root(pu.hostname) == d or root(pu.hostname).endswith("." + d) or root(pu.hostname) == root(urlparse(blog_url).hostname)):
            continue
        path = pu.path.rstrip("/")
        rel = path[len(bpath):] if bpath and path.startswith(bpath + "/") else path
        if not path or path == bpath or MEDIA.search(path) or SKIP.search(rel + "/"):
            continue
        slug = path.split("/")[-1]
        under_blog = bpath and path.startswith(bpath + "/")
        sluggy = slug.count("-") >= 3
        if not (under_blog and len(slug) > 8) and not sluggy:
            continue
        if u not in posts:
            posts.append(u)
    plan[d] = {"blogUrl": blog_url, "posts": posts[:5], "contributorPages": contrib[:3]}
    urls += posts[:5]
json.dump(plan, open("step3/posts_plan.json", "w"), indent=1)
inp = {"startUrls": [{"url": u} for u in urls], "crawlerType": "cheerio", "maxCrawlDepth": 0,
       "maxCrawlPages": len(urls) + 20, "saveMarkdown": True, "maxRequestRetries": 1, "requestTimeoutSecs": 40,
       "proxyConfiguration": {"useApifyProxy": True}}
json.dump(inp, open("step3/crawl_posts_in.json", "w"))
few = {d: len(v["posts"]) for d, v in plan.items() if len(v["posts"]) < 3}
print("sites", len(plan), "post urls", len(urls), "sites with <3 posts:", len(few))
print(few)
print("contributor pages:", {d: v["contributorPages"] for d, v in plan.items() if v["contributorPages"]})
