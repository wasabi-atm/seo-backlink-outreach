"""Pass 1 parser: read homepage crawl items (JSON files from get-dataset-items), save each homepage as
home/<domain>.md, and pick the most likely blog index URL from the homepage links.
Writes home_summary.csv: webDomain, loaded, loadedUrl, title, homeChars, blogUrl, blogCandidates."""
import csv, json, glob, os, re, sys
from urllib.parse import urlparse, urljoin

def root(host):
    host = (host or "").lower().split(":")[0]
    return host[4:] if host.startswith("www.") else host

rows = list(csv.DictReader(open("01_dr_pass.csv")))
doms = {r["webDomain"]: r for r in rows}
items = []
for f in sorted(glob.glob(sys.argv[1] + "/*.json")):
    d = json.load(open(f))
    items += d["items"] if isinstance(d, dict) and "items" in d else d

def match_domain(u):
    h = root(urlparse(u).hostname)
    if h in doms:
        return h
    for d in doms:
        if h.endswith("." + d):
            return d
    return None

os.makedirs("crawl/home", exist_ok=True)
home = {}
for it in items:
    start = it.get("crawl", {}).get("requestUrl") if isinstance(it.get("crawl"), dict) else None
    start = start or it.get("crawl.requestUrl") or it.get("url")
    d = match_domain(start) or match_domain(it.get("url", ""))
    if not d:
        continue
    home[d] = it

BLOG_WORDS = ["blog", "insights", "resources", "articles", "news", "learn", "journal", "thinking", "ideas",
              "perspectives", "hub", "library", "knowledge", "stories", "content", "guides", "academy", "media"]
LINK_RE = re.compile(r"\[([^\]]{0,80})\]\((https?://[^\s)]+|/[^\s)]*)")

def score_link(text, url, dom):
    p = urlparse(url)
    h = root(p.hostname)
    if not (h == dom or h.endswith("." + dom)):
        return -1
    path = p.path.rstrip("/").lower()
    segs = [s for s in path.split("/") if s]
    t = text.strip().lower()
    s = 0
    if h.startswith("blog."):
        s = 9 if not segs else 3
    if segs and segs[-1] in ("blog", "the-blog") and len(segs) <= 2:
        s = max(s, 10)
    elif segs and segs[-1] in ("insights", "articles", "journal", "thinking", "ideas", "perspectives") and len(segs) <= 2:
        s = max(s, 8)
    elif segs and segs[-1] in ("resources", "learn", "news", "hub", "library", "knowledge-hub", "stories", "guides") and len(segs) <= 2:
        s = max(s, 6)
    if t in ("blog", "our blog", "the blog", "read our blog", "insights", "articles", "latest insights", "news & insights", "news and insights"):
        s += 3
    if len(segs) > 2:
        s -= 3
    return s

out = []
for d, r in doms.items():
    it = home.get(d)
    md = (it or {}).get("markdown") or ""
    loaded = (it or {}).get("crawl", {}).get("loadedUrl") if isinstance((it or {}).get("crawl"), dict) else None
    loaded = loaded or (it or {}).get("crawl.loadedUrl") or (it or {}).get("url") or ""
    status = (it or {}).get("crawl", {}).get("httpStatusCode") if isinstance((it or {}).get("crawl"), dict) else (it or {}).get("crawl.httpStatusCode")
    title = ((it or {}).get("metadata") or {}).get("title") if isinstance((it or {}).get("metadata"), dict) else (it or {}).get("metadata.title")
    if md:
        open(f"crawl/home/{d}.md", "w").write(f"{loaded}\n{title or ''}\n\n{md}")
    cands = {}
    for text, href in LINK_RE.findall(md):
        u = urljoin(loaded or f"https://{d}/", href).split("#")[0].split("?")[0]
        s = score_link(text, u, d)
        if s > 0:
            cands[u] = max(cands.get(u, 0), s)
    ranked = sorted(cands.items(), key=lambda x: (-x[1], len(x[0])))
    out.append(dict(webDomain=d, loaded=bool(md), status=status or "", loadedUrl=loaded, title=(title or "").strip(),
                    homeChars=len(md), blogUrl=ranked[0][0] if ranked else "",
                    blogCandidates=" ".join(u for u, _ in ranked[1:4])))
w = csv.DictWriter(open("home_summary.csv", "w", newline=""), fieldnames=list(out[0]))
w.writeheader(); w.writerows(out)
print("domains", len(out), "loaded", sum(o["loaded"] for o in out), "blog found", sum(bool(o["blogUrl"]) for o in out))
print("not loaded:", " ".join(o["webDomain"] for o in out if not o["loaded"]))
print("no blog link:", " ".join(o["webDomain"] for o in out if o["loaded"] and not o["blogUrl"]))
