"""Step 3, part 2: link habits from the crawled posts (crawl/raw/posts/*.json, Apify website-content-crawler,
readable-text markdown so nav and footer links are mostly gone).
For each approved site: distinct outside business domains linked from the post bodies, outside people quoted
(title + "at/of" + another company), and guest-post or contributor pages.
backlinkExchange: Yes = 10+ outside business domains, or 2+ outside companies quoted, or a guest/contributor page;
Some = 3-9 domains or 1 outside company quoted; No = fewer.
Writes 02_enriched.csv (all 150 have DR 40+) and 02_low_dr.csv (new candidates under DR 40, not vetted)."""
import csv, glob, json, re
from collections import defaultdict
from urllib.parse import urlparse

def root(h):
    h = (h or "").lower().split(":")[0].strip(".")
    h = h[4:] if h.startswith("www.") else h
    parts = h.split(".")
    if len(parts) > 2 and parts[-2] in ("co", "com", "org", "ac", "gov", "net") and len(parts[-1]) == 2:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else h

IGNORE = {"twitter.com", "x.com", "linkedin.com", "lnkd.in", "facebook.com", "fb.com", "instagram.com", "youtube.com",
          "youtu.be", "tiktok.com", "pinterest.com", "reddit.com", "threads.net", "bsky.app", "wikipedia.org",
          "wikimedia.org", "google.com", "goo.gl", "g.co", "apple.com", "spotify.com", "bit.ly", "t.co", "ow.ly",
          "cloudfront.net", "amazonaws.com", "googleusercontent.com", "gstatic.com", "googleapis.com", "gravatar.com",
          "wp.com", "wordpress.com", "w.org", "list-manage.com", "hsforms.com", "hs-sites.com", "hubspotusercontent-na1.net",
          "hubspot.net", "website-files.com", "webflow.io", "ctfassets.net", "sanity.io", "imgix.net", "cdn.com",
          "vimeo.com", "wistia.com", "wistia.net", "loom.com", "addtoany.com", "sharethis.com", "typeform.com",
          "calendly.com", "zoom.us", "eventbrite.com", "podcasts.apple.com", "open.spotify.com", "feedburner.com",
          "cloudflare.com", "mailto", "whatsapp.com", "wa.me", "t.me", "medium.com", "substack.com", "github.io",
          "storyblok.com", "prismic.io", "contentful.com", "datocms-assets.com", "b-cdn.net", "unsplash.com",
          "shutterstock.com", "gettyimages.com", "istockphoto.com", "giphy.com", "canva.com", "rackcdn.com", "blog.google",
          "akamaized.net", "fastly.net", "azureedge.net", "jsdelivr.net", "unpkg.com", "doubleclick.net", "g.page", "go.link", "rebrand.ly", "tinyurl.com"}
NON_BIZ = re.compile(r"((^|\.)gov(\.[a-z]{2})?$|(^|\.)edu(\.[a-z]{2})?$|(^|\.)ac\.[a-z]{2}$|(^|\.)nhs\.uk$|(^|\.)police\.uk$|europa\.eu$|\.int$|(^|\.)mil$)")
GENERIC = {"integrated", "north", "south", "east", "west", "global", "search", "marketing", "sales", "digital", "brand",
           "content", "growth", "product", "customer", "client", "strategy", "operations", "people", "the", "our", "a",
           "partnerships", "communications", "engineering", "design", "data", "finance", "technology", "media", "uk", "us",
           "emea", "europe", "americas", "america", "asia", "apac", "mena", "large", "small", "enterprise", "business"}
LINK = re.compile(r"\]\((https?://[^\s)\"]+)")
QUOTE = re.compile(r"\b(CEO|CMO|CTO|COO|CFO|CRO|[Ff]ounder|[Cc]o-[Ff]ounder|Managing Director|Managing Partner|President|"
                   r"(?:Global |Senior )?(?:Head|VP|Director) of [A-Z][A-Za-z&]+(?: [A-Z][A-Za-z&]+)?|Chief [A-Z][a-z]+ Officer)"
                   r",?\s+(?:at|of)\s+([A-Z][A-Za-z0-9&.\-]+(?:\s(?:[A-Z][A-Za-z0-9&.\-]+|&))?)")
GUEST = re.compile(r"(this is a guest post|guest post by|guest author|written by our guest|contributed by|write for us|"
                   r"become a contributor|submit a guest post)", re.I)

prospects = list(csv.DictReader(open("01_prospects.csv")))
vet = {r["webDomain"]: r for r in csv.DictReader(open("01_prospects.csv"))}
plan = json.load(open("step3/posts_plan.json"))
doms = {p["webDomain"]: p for p in prospects}

items = []
for f in sorted(glob.glob("crawl/raw/posts/*.json")):
    d = json.load(open(f))
    items += d["items"]

ALIAS = {"bulldogdigitalmedia.com": "bulldogdigitalmedia.co.uk"}  # posts served from another domain of the same company

def owner(url):
    h = (urlparse(url).hostname or "").lower()
    r = root(h)
    if r in ALIAS:
        return ALIAS[r]
    for d in doms:
        if r == root(d):
            return d
    return None

posts = defaultdict(list)
seen = set()
for it in items:
    u = it.get("crawl.loadedUrl") or it.get("url") or ""
    if u in seen:
        continue
    seen.add(u)
    d = owner(it.get("url") or u) or owner(u)
    md = it.get("markdown") or ""
    if d and len(md) > 400:
        posts[d].append((u, md))

rows = []
for p in prospects:
    d = p["webDomain"]
    own = {root(d)} | {a for a, b in ALIAS.items() if b == d}
    name_tokens = {t.lower() for t in re.findall(r"[A-Za-z]{4,}", p["companyName"])} | {root(d).split(".")[0]}
    biz, nonbiz, quoted = defaultdict(int), set(), set()
    guest = bool(plan.get(d, {}).get("contributorPages"))
    guest_phrase = "contributor page linked" if guest else ""
    for u, md in posts.get(d, []):
        for link in LINK.findall(md):
            r = root(urlparse(link).hostname)
            if not r or r in own or r in IGNORE or any(r.endswith("." + i) for i in IGNORE):
                continue
            if r.split(".")[0] in name_tokens:
                continue
            if NON_BIZ.search(r):
                nonbiz.add(r)
                continue
            biz[r] += 1
        for m in QUOTE.finditer(md):
            comp = re.split(r"\.\s|\.$", m.group(2))[0].strip(" .,")
            low = comp.lower()
            if not comp or low.split()[0] in GENERIC or any(t in low for t in name_tokens) \
                    or root(d).split(".")[0] in low.replace(" ", ""):
                continue
            quoted.add(comp)
        gm = GUEST.search(md)
        if gm:
            guest = True
            guest_phrase = guest_phrase or f'"{gm.group(1).lower()}" in {u}' 
    n_biz, n_q, n_posts = len(biz), len(quoted), len(posts.get(d, []))
    if n_posts == 0:
        bx, ev = "", "not checked: no posts could be read"
    else:
        bx = "Yes" if (n_biz >= 10 or n_q >= 2 or guest) else "Some" if (n_biz >= 3 or n_q >= 1) else "No"
        top = sorted(biz, key=lambda k: -biz[k])[:5]
        ev = f"{n_biz} outside business domains linked in {n_posts} recent posts"
        if top:
            ev += " (e.g. " + ", ".join(top) + ")"
        if n_q:
            ev += "; quotes people from " + ", ".join(sorted(quoted)[:3]) + (f" and {n_q - 3} more" if n_q > 3 else "")
        if guest:
            ev += "; guest post or contributor signs: " + guest_phrase
            cp = plan.get(d, {}).get("contributorPages")
            if cp:
                ev += " (" + cp[-1] + ")"
    v = vet.get(d, {})
    rows.append(dict(companyName=p["companyName"], webDomain=d, domainRating=int(float(p["domainRating"])),
                     country=p["country"], serviceType=p["serviceType"], segment=p["segment"],
                     visualScore=p["visualScore"], backlinkExchange=bx, backlinkEvidence=ev,
                     dataSource="ahrefs-free (DR), apify (posts)", competitor=p["competitor"], drStatus="pass", videoSchemaGap="",
                     competitorDecision=p.get("competitorDecision", ""), blogUrl=plan.get(d, {}).get("blogUrl", v.get("blogUrl", "")),
                     postsChecked=n_posts))

# Read by hand from posts that did not come through in the saved crawl output (28 Sep).
MANUAL = {
    "cavendishmaxwell.com": ("Yes", "4 September posts republish press articles with links back to The National, AGBI, Lana and Hospitality News ME; "
                             "they quote people from CBRE, Springfield Properties, betterhomes, Oxford Economics and Tumodo"),
    "adido-digital.co.uk": ("", "not checked: post links on the blog index resolve to 404 (doubled /insights/ path); check by hand"),
}
for r in rows:
    if r["webDomain"] in MANUAL:
        r["backlinkExchange"], r["backlinkEvidence"] = MANUAL[r["webDomain"]]

COLS = ["companyName", "webDomain", "domainRating", "country", "serviceType", "segment", "visualScore", "backlinkExchange",
        "backlinkEvidence", "dataSource", "competitor", "drStatus", "videoSchemaGap"]
with open("02_enriched.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS + ["competitorDecision", "blogUrl", "postsChecked"], extrasaction="ignore")
    w.writeheader(); w.writerows(rows)

# Low DR: new candidates under 40 on the free Ahrefs endpoint (research-agent lists). Not vetted, so link habits were not checked.
cand = [r for r in csv.DictReader(open("00_candidates_clean.csv")) if r["source"].startswith("new_")]
dr = {l.split()[0]: float(l.split()[1]) for l in open("dr_free_new.txt")}
hub = json.load(open("hubspot_drop.json"))
low = []
for c in cand:
    d = c["webDomain"]
    if d not in dr or dr[d] >= 40 or d in hub:
        continue
    note = "not checked: under DR 40, so not vetted or crawled"
    if dr[d] == 0:
        note += "; DR 0 may mean the domain redirects or changed, check before use"
    low.append(dict(companyName=c["companyName"], webDomain=d, domainRating=int(dr[d]) if dr[d] >= 1 else round(dr[d], 1),
                    country=c["country"], serviceType=c["serviceType"], segment=c["segment"], visualScore="",
                    backlinkExchange="", backlinkEvidence=note, dataSource="ahrefs-free", competitor=c["competitor"],
                    drStatus="low", videoSchemaGap=""))
with open("02_low_dr.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader(); w.writerows(low)

from collections import Counter
print("enriched", len(rows), Counter(r["backlinkExchange"] for r in rows))
print("not checked:", [r["webDomain"] for r in rows if not r["backlinkExchange"]])
print("low dr", len(low))
