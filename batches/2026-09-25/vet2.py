"""Text-based vetting (screenshots cannot be viewed from the cloud session, so design is not scored).
Inputs: 01_dr_pass.csv (+ swaps_clean.csv), home/<domain>.md from pass 1, raw/blog/*.json from pass 2.
Scores 1-5 on real business, blog quality and clean; visualScore is their average (as in 2026-09-23-b).
Writes vetting.csv and blog/<domain>.md (the best blog index page per domain)."""
import csv, glob, json, os, re, datetime
from urllib.parse import urlparse

TODAY = datetime.date(2026, 9, 25)
DROP = {  # acquired or merged: the homepage now belongs to another company
    "searchlaboratory.com": "acquired: redirects to Havas Market",
    "terminus.com": "acquired: redirects to DemandScience",
    "rollworks.com": "acquired: redirects to AdRoll",
    "mosaic.tech": "acquired: redirects to HiBob",
    "clearvoice.com": "acquired: redirects to Fiverr",
    "pento.io": "acquired: redirects to HiBob",
    "clari.com": "merged: redirects to Salesloft (also a candidate)",
    "blastmedia.com": "merged: redirects to PANBlast (PAN Communications is also a candidate)",
    "banked.com": "rebranded to Pay by Bank (paybyb.com), unclear company",
    "pure360.com": "rebranded to Spotler (Dutch parent, spotler.com)",
    "onfido.com": "acquired: homepage is now Entrust",
    "vadecom.net": "not UK/US/UAE: Egypt-based agency serving the Gulf",
}
# Farm-word hits checked by hand: client case studies or figurative use, not farm content.
FARM_OK = {"navattic.com": "betting on agentic demos", "digitalsilk.com": "betting on scale (post title)",
           "bonus.ly": "why we're betting on managers (post title)", "5wpr.com": "has a casino and gambling PR practice; not a farm",
           "pure360.com": "Holland Casino case study"}
EXTRA_PLAN = {"jaywing.com": ["https://www.jaywing.com/views/"], "themarketingpractice.com": ["https://www.tmpb2b.com/en-gb/insights"],
              "kaltura.com": ["https://corp.kaltura.com/blog/"], "highwirepr.com": ["https://www.teamhighwire.com/insights"],
              "moneypenny.com": ["https://www.moneypenny.com/uk/resources/blogs", "https://www.moneypenny.com/us/resources/blogs"],
              "smartrecruiters.com": ["https://www.smartrecruiters.com/resources/article/"], "hippovideo.io": ["https://www.hippovideo.io/blog/"],
              "upliftcontent.com": ["https://www.upliftcontent.com/content-marketing-blog-uplift-content/"], "webflow.com": ["https://webflow.com/blog"],
              "fathom.video": ["https://www.fathom.ai/blog", "https://www.fathom.ai/resource-hub"], "luminance.com": ["https://www.luminance.com/resources/index"],
              "network.ae": ["https://www.network.ae/en/about-us/blogs"], "koto.studio": ["https://koto.com/journal"],
              "smartinsights.com": ["https://www.smartinsights.com/digital-marketing-strategy/"], "bonus.ly": ["https://bonusly.com/resources/blog"],
              "scribehow.com": ["https://scribe.com/library"], "ziphq.com": ["https://zip.com/blog"], "gladly.com": ["https://www.gladly.ai/blog/"],
              "learningpool.com": ["https://www.confirm.com/blog/"], "revenueriver.co": ["https://www.instrumental.net/blog"],
              "arabadonline.com": ["https://www.arabaddigital.com/"]}

def root(h):
    h = (h or "").lower().split(":")[0]
    return h[4:] if h.startswith("www.") else h

rows = list(csv.DictReader(open("01_dr_pass.csv")))
swaps = {r["oldDomain"]: r for r in csv.DictReader(open("swaps_clean.csv"))}
dr_new = {"tmpb2b.com": 49, "teamhighwire.com": 45, "instrumental.net": 62, "confirm.com": 72, "bonusly.com": 75,
          "gladly.ai": 73, "scribe.com": 76, "zip.com": 63, "koto.com": 68, "arabaddigital.com": 55, "fathom.ai": 77}
plan = json.load(open("blog_plan.json"))

items = []
for f in sorted(glob.glob("crawl/raw/blog/*.json") + glob.glob("crawl/raw/blog2/*.json")):
    d = json.load(open(f))
    items += d["items"]
by_url = {}
for it in items:
    by_url.setdefault(it.get("url", "").rstrip("/"), it)

MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
DATE_RES = [
    (re.compile(r"\b(%s)[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d\d)\b" % MONTHS), "mdy"),
    (re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(%s)[a-z]*\.?,?\s+(20\d\d)\b" % MONTHS), "dmy"),
    (re.compile(r"\b(20\d\d)-(\d\d)-(\d\d)\b"), "iso"),
    (re.compile(r"\b(\d{1,2})/(\d{1,2})/(20\d\d)\b"), "slash"),
]
MIDX = {m: i + 1 for i, m in enumerate(MONTHS.split("|"))}

def dates_in(md):
    out = []
    for rx, kind in DATE_RES:
        for m in rx.findall(md):
            try:
                if kind == "mdy": d = datetime.date(int(m[2]), MIDX[m[0][:3]], int(m[1]))
                elif kind == "dmy": d = datetime.date(int(m[2]), MIDX[m[1][:3]], int(m[0]))
                elif kind == "iso": d = datetime.date(int(m[0]), int(m[1]), int(m[2]))
                else:
                    a, b, y = int(m[0]), int(m[1]), int(m[2])
                    d = datetime.date(y, a, b) if a <= 12 else datetime.date(y, b, a)
            except ValueError:
                continue
            if datetime.date(2015, 1, 1) <= d <= TODAY + datetime.timedelta(days=2):
                out.append(d)
    return out

FARM = ["casino", "betting", "sportsbook", "cbd oil", "payday loan", "escort", "viagra", "slot machine"]
WFU = ["write for us", "guest post guidelines", "submit a guest post", "sponsored post", "guest posting"]
BY_RE = re.compile(r"\b(By|Written by|Author:?)\s+\[?[A-Z][a-z]+ [A-Z][a-z]+")
REAL_WORDS = ["case stud", "customers", "clients", "pricing", "book a demo", "request a demo", "get a demo", "contact us",
              "our team", "about us", "careers", "trusted by", "our work", "get started", "talk to"]

os.makedirs("crawl/blog", exist_ok=True)
out = []
for r in rows:
    d = r["webDomain"]
    sw = swaps.get(d)
    rec = dict(r)
    if sw:
        rec.update(companyName=sw["companyName"], webDomain=sw["webDomain"], serviceType=sw["serviceType"],
                   domainRating=dr_new[sw["webDomain"]], source=sw["source"])
    hf = f"crawl/home/{d}.md"
    hmd = open(hf).read() if os.path.exists(hf) else ""
    htitle = hmd.split("\n")[1] if hmd.count("\n") > 1 else ""
    # best blog page among the planned URLs
    best, best_n = None, -1
    for u in plan.get(d, []) + EXTRA_PLAN.get(d, []):
        it = by_url.get(u.rstrip("/"))
        if not it or it.get("crawl.httpStatusCode") not in (200, None):
            continue
        md = it.get("markdown") or ""
        lu = it.get("crawl.loadedUrl") or u
        if urlparse(lu).path.strip("/") == "" and not urlparse(lu).hostname.startswith("blog"):
            continue  # redirected to a homepage
        n = len(dates_in(md)) * 3 + len(re.findall(r"\]\(", md)) / 20 + len(md) / 5000
        if n > best_n:
            best, best_n = it, n
    bmd = (best or {}).get("markdown") or ""
    burl = (best or {}).get("crawl.loadedUrl") or ""
    if bmd:
        open(f"crawl/blog/{rec['webDomain']}.md", "w").write(f"{burl}\n{(best or {}).get('metadata.title') or ''}\n\n{bmd}")
    ds = dates_in(bmd)
    latest = max(ds) if ds else None
    recent = [x for x in ds if (TODAY - x).days <= 365]
    authors = len(BY_RE.findall(bmd))
    alltxt = (hmd + " " + bmd).lower()
    farm = [] if d in FARM_OK else [w for w in FARM if w in alltxt]
    wfu = [w for w in WFU if w in alltxt]
    real_hits = sum(w in hmd.lower() for w in REAL_WORDS)
    home_ok = len(hmd) > 1500
    real = 5 if home_ok and real_hits >= 4 else 4 if home_ok and real_hits >= 2 else 3 if home_ok else 2 if hmd else 1
    if not bmd:
        blogq = 2
    else:
        blogq = 3.0
        if latest and (TODAY - latest).days <= 90: blogq += 1.0
        elif latest and (TODAY - latest).days <= 365: blogq += 0.5
        elif latest: blogq -= 0.5
        if len(recent) >= 3: blogq += 0.5
        if authors >= 1: blogq += 0.5
        blogq = max(1.0, min(5.0, blogq))
    clean = 1 if farm else 4 if wfu else 5
    score = round((real + blogq + clean) / 3, 1)
    hard = []
    if d in DROP: hard.append(DROP[d])
    if not hmd and not bmd: hard.append("did not load (homepage and blog)")
    if farm: hard.append("farm words: " + ",".join(farm))
    if not bmd and d not in DROP and (hmd or bmd): hard.append("no blog found")
    if latest and (TODAY - latest).days > 540: hard.append(f"blog inactive: latest post {latest}")
    notes = ["homepage ok" if home_ok else ("homepage thin" if hmd else "homepage not loaded (bot block)")]
    if bmd:
        notes.append(f"blog at {burl}; latest date {latest or 'none found'}; {len(recent)} dates in last 12 months; {authors} bylines")
    else:
        notes.append("no blog index loaded")
    if wfu: notes.append("mentions " + wfu[0] + " (already does link swaps)")
    if d in FARM_OK: notes.append("farm-word hit checked by hand: " + FARM_OK[d])
    rec.update(visualScore=score, realScore=real, blogScore=blogq, cleanScore=clean, blogUrl=burl,
               latestPost=str(latest or ""), recentPosts=len(recent), hardFail="; ".join(hard),
               visualNotes="; ".join(notes), homeTitle=htitle.strip()[:120], oldDomain=d if sw else "")
    out.append(rec)

cols = ["companyName", "webDomain", "country", "serviceType", "segment", "domainRating", "visualScore", "realScore",
        "blogScore", "cleanScore", "blogUrl", "latestPost", "recentPosts", "hardFail", "visualNotes", "competitor",
        "competitorReason", "homeTitle", "source", "oldDomain"]
w = csv.DictWriter(open("vetting.csv", "w", newline=""), fieldnames=cols, extrasaction="ignore")
w.writeheader(); w.writerows(out)
ok = [o for o in out if o["visualScore"] >= 3.5 and not o["hardFail"]]
print("vetted", len(out), "keep", len(ok), "no blog", sum(not o["blogUrl"] for o in out), "hard fail", sum(bool(o["hardFail"]) for o in out))
