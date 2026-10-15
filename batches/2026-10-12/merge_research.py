import csv, glob, os, sys, re
sys.path.insert(0, "/home/user/seo-backlink-outreach/skill/mta-backlink-outreach/scripts")
from dedupe import root_domain
cols = ["companyName","webDomain","country","serviceType","segment","competitor","competitorReason","domainRating","blogUrl","latestPost","notes"]
rows, seen, issues = [], {}, []
for p in sorted(glob.glob("research/*.csv")):
    sl = os.path.basename(p)[:-4]
    with open(p, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            d = root_domain(r.get("webDomain",""))
            if not d: issues.append((sl, "no domain", r)); continue
            if d in seen: issues.append((sl, f"dup of {seen[d]}", d)); continue
            seen[d] = sl
            r = {c: (r.get(c) or "").strip() for c in cols}
            r["webDomain"] = d
            r["slice"] = sl
            for c in cols:
                if "—" in r[c] or "–" in r[c]:
                    r[c] = r[c].replace("—", ",").replace("–", "-")
            try:
                if float(r["domainRating"] or 0) < 40: issues.append((sl, "DR<40", d))
            except ValueError: issues.append((sl, "bad DR", d))
            rows.append(r)
with open("00_candidates.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols + ["slice"]); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), "rows")
print(Counter(r["segment"] for r in rows))
print(Counter(r["country"] for r in rows))
print(Counter(r["competitor"] for r in rows))
print(Counter((r["segment"], r["country"]) for r in rows))
for i in issues: print("ISSUE", i)
