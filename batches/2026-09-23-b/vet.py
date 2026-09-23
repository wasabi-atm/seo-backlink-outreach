"""Text-based vetting from website-content-crawler output (homepage + /blog per domain).
Screenshots were not possible from the cloud session, so design is not scored here."""
import csv, json, glob, re, sys
from urllib.parse import urlparse

def root(u):
    h = (urlparse(u).hostname or "").lower()
    h = h[4:] if h.startswith("www.") else h
    return h

items = []
for f in glob.glob("crawl/*.json"):
    d = json.load(open(f))
    items += d["items"] if isinstance(d, dict) else d
rows = list(csv.DictReader(open("dr_pass.csv")))
doms = {r["webDomain"]: r for r in rows}
pages = {d: {"home": None, "blog": None} for d in doms}
for it in items:
    start = it.get("url", "")
    dom = root(start)
    if dom not in pages:
        m = [d for d in doms if dom.endswith(d)]
        if not m: continue
        dom = m[0]
    kind = "blog" if urlparse(start).path.rstrip("/").endswith("/blog") else "home"
    pages[dom][kind] = it

FARM = ["casino", "betting", "sportsbook", "cbd oil", "payday loan", "escort", "viagra"]
WFU = ["write for us", "guest post guidelines", "submit a guest post", "sponsored post"]
YEAR_RE = re.compile(r"\b(2025|2026)\b")
MONTH_RE = re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{1,2},? (2025|2026)\b|\b\d{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (2025|2026)\b")
BY_RE = re.compile(r"\b(By|Written by|Author)\s*:?\s*\[?[A-Z][a-z]+ [A-Z][a-z]+")
out = []
for dom, r in doms.items():
    h, b = pages[dom]["home"], pages[dom]["blog"]
    hmd = (h or {}).get("markdown") or ""
    bmd = (b or {}).get("markdown") or ""
    bstat = ((b or {}).get("crawl") or {}).get("httpStatusCode") if b else None
    bloaded = ((b or {}).get("crawl") or {}).get("loadedUrl", "") if b else ""
    alltxt = (hmd + " " + bmd).lower()
    farm = [w for w in FARM if w in alltxt]
    wfu = [w for w in WFU if w in alltxt]
    blog_ok = bool(b) and (bstat in (200, None)) and len(bmd) > 800
    dates = len(MONTH_RE.findall(bmd))
    years = len(YEAR_RE.findall(bmd))
    authors = len(BY_RE.findall(bmd))
    links = len(re.findall(r"\]\(", bmd))
    home_ok = bool(h) and len(hmd) > 300
    real = 5 if home_ok and len(hmd) > 1500 else 4 if home_ok else 2
    if not blog_ok: blogq = 2
    else:
        blogq = 3 + (1 if (dates >= 3 or years >= 5) else 0) + (1 if authors >= 2 else 0)
        if links > 20 and blogq == 3: blogq = 3.5
    clean = 1 if farm else 4 if wfu else 5
    score = round((real + blogq + clean) / 3, 1)
    hard = []
    if not h and not b: hard.append("did not load")
    if farm: hard.append("farm words: " + ",".join(farm))
    notes = []
    notes.append("homepage ok" if home_ok else "homepage thin or not loaded")
    if blog_ok: notes.append(f"blog at {urlparse(bloaded).path or '/blog'}; {dates} dated posts, {authors} bylines")
    else: notes.append(f"no blog found at /blog (status {bstat})")
    if wfu: notes.append("mentions " + wfu[0])
    out.append(dict(companyName=r["companyName"], webDomain=dom, country=r["country"], serviceType=r["serviceType"],
                    segment=r["segment"], domainRating=r["domainRating"], visualScore=score, realScore=real, blogScore=blogq,
                    cleanScore=clean, blogFound=blog_ok, blogUrl=bloaded, hardFail="; ".join(hard), visualNotes="; ".join(notes),
                    competitor=r["competitor"], competitorReason=r["competitorReason"],
                    homeTitle=((h or {}).get("metadata") or {}).get("title", "")))
w = csv.DictWriter(open("vetting.csv", "w", newline=""), fieldnames=list(out[0]))
w.writeheader(); w.writerows(out)
ok = [o for o in out if o["visualScore"] >= 3.5 and not o["hardFail"]]
print("vetted", len(out), "keep", len(ok), "noblog", sum(not o["blogFound"] for o in out), "hardfail", sum(bool(o["hardFail"]) for o in out))
