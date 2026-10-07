"""Combine research/<slice>.csv plus yesterday's reusable spares into 00_candidates.csv."""
import csv, glob, os, sys
sys.path.insert(0, "/home/user/seo-backlink-outreach/skill/mta-backlink-outreach/scripts")
from dedupe import root_domain
COLS = ["companyName","webDomain","country","serviceType","segment","competitor","competitorReason",
        "domainRating","blogUrl","latestPost","notes","slice"]
free = {l.strip() for l in open("reusable_spares.txt") if l.strip()}
dec = {}
for r in csv.DictReader(open("../2026-10-06/step2/competitor_decisions.csv")):
    dec[root_domain(r.get("webDomain",""))] = r
src = [(p, os.path.basename(p)[:-4]) for p in sorted(glob.glob("research/*.csv"))]
src += [("../2026-10-06/01_spares.csv","spare_y1"),("../2026-10-06/03_spares.csv","spare_y3")]
rows, seen = [], set()
for p, sl in src:
    for r in csv.DictReader(open(p, newline="", encoding="utf-8-sig")):
        d = root_domain(r.get("webDomain",""))
        if not d or (sl.startswith("spare") and d not in free): continue
        if d in seen: print("repeat:", d, sl); continue
        seen.add(d)
        r["webDomain"]=d; r["slice"]=sl
        r["country"]=(r.get("country") or "").strip().upper().replace("UNITED KINGDOM","UK")
        r["segment"]=(r.get("segment") or "").strip().upper()
        r["competitor"]=(r.get("competitor") or "no").strip().lower()
        for k in list(r):
            if isinstance(r[k], str): r[k]=r[k].replace("—",",").replace("–","-").strip()
        rows.append({c: r.get(c,"") for c in COLS})
w = csv.DictWriter(open("00_candidates.csv","w",newline=""), fieldnames=COLS); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows)); print(Counter((r["segment"],r["country"],r["slice"].startswith("spare")) for r in rows))
print("competitors:", [r["webDomain"] for r in rows if r["competitor"]=="yes"])
print("yesterday decisions available:", [d for d in dec if d in seen])
