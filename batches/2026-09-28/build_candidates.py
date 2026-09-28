"""Build 00_candidates.csv from every source for backlink-2026-09-28:
- pool_spares.csv: the 105 vetted DR 40+ spares from 2026-09-25 (Video SEO companies removed)
- pool_vs.csv: SaaS from the Video SEO research, not among the 178 skipped, DR 40+ (build_pool_vs.py)
- new_*.txt: new UK and UAE candidates from research agents (companyName|webDomain|country|serviceType|segment|competitorReason)
Drops HubSpot customers and open deals (hubspot_drop.json)."""
import csv, glob, json

hub = json.load(open("hubspot_drop.json"))
cols = ["companyName", "webDomain", "country", "serviceType", "segment", "competitor", "competitorReason", "source"]
rows, seen = [], set()

def add(r):
    d = r["webDomain"].strip().lower()
    if d in seen or d in hub:
        return
    seen.add(d)
    r["webDomain"] = d
    rows.append({k: r.get(k, "") for k in cols})

for r in csv.DictReader(open("pool_spares.csv")):
    r["source"] = "2026-09-25 spares"
    add(r)
for r in csv.DictReader(open("pool_vs.csv")):
    add(r)
for f in sorted(glob.glob("new_*.txt")):
    for line in open(f):
        p = [x.strip() for x in line.rstrip("\n").split("|")]
        if len(p) < 5 or not p[1]:
            continue
        comp = p[5] if len(p) > 5 else ""
        add(dict(companyName=p[0], webDomain=p[1], country=p[2], serviceType=p[3], segment=p[4],
                 competitor="yes" if comp else "no", competitorReason=comp, source=f.replace(".txt", "")))
with open("00_candidates.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter((r["segment"], r["country"]) for r in rows))
