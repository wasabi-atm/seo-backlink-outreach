import csv, glob, os
from collections import Counter
cols = ["companyName","webDomain","domainRating","country","serviceType","segment","visualScore","backlinkExchange","backlinkEvidence","dataSource","competitor","drStatus","videoSchemaGap","latestPost","blogUrl","competitorDecision","pool","postsRead","outsideDomainCount","recentPosts","notes"]
DROP_UNREADABLE = {"gurucul.com", "veem.com"}   # Checkpoint 1: keep, verify at Step 3, drop if blogs unreadable
tot = Counter()
for n in ["2026-10-12","2026-10-12-b2","2026-10-12-b3","2026-10-12-b4"]:
    rows = []
    inp = []
    for i in range(4):
        inp += list(csv.DictReader(open(f"{n}/step3/in_{i}.csv", encoding="utf-8")))
        p = f"{n}/step3/out_{i}.csv"
        rows += list(csv.DictReader(open(p, encoding="utf-8")))
    assert [r["webDomain"] for r in rows] == [r["webDomain"] for r in inp], n
    enriched, low, dropped = [], [], []
    for r in rows:
        r = {c: r.get(c, "") for c in cols}
        try: dr = float(r["domainRating"])
        except ValueError: dr = None
        if r["webDomain"] in DROP_UNREADABLE and r["backlinkExchange"] == "unchecked":
            dropped.append(r); continue
        if dr is None or dr < 40:
            r["drStatus"] = "unknown" if dr is None else "low"; low.append(r)
        else:
            r["drStatus"] = "pass"; enriched.append(r)
    for name, data in (("02_enriched.csv", enriched), ("02_low_dr.csv", low), ("02_dropped_unreadable.csv", dropped)):
        with open(f"{n}/{name}", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(data)
    c = Counter(r["backlinkExchange"] for r in enriched)
    drs = [float(r["domainRating"]) for r in enriched]
    print(n, "rows", len(rows), "enriched", len(enriched), "low", len(low), "dropped", [r["webDomain"] for r in dropped], dict(c), "DR", min(drs), "-", max(drs))
    tot.update(c); tot["_enriched"] += len(enriched)
print(dict(tot))
