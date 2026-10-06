"""Combine research/<slice>.csv into 00_candidates.csv, normalise domains, drop in-batch repeats (first wins)."""
import csv, glob, os, sys
sys.path.insert(0, "/home/user/seo-backlink-outreach/skill/mta-backlink-outreach/scripts")
from dedupe import root_domain
COLS = ["companyName", "webDomain", "country", "serviceType", "segment", "competitor", "competitorReason",
        "domainRating", "blogUrl", "latestPost", "notes", "slice"]
rows, seen = [], set()
for p in sorted(glob.glob("research/*.csv")):
    sl = os.path.basename(p)[:-4]
    with open(p, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            d = root_domain(r.get("webDomain", ""))
            if not d:
                continue
            r["webDomain"] = d
            r["slice"] = sl
            r["country"] = (r.get("country") or "").strip().upper().replace("UNITED KINGDOM", "UK")
            r["segment"] = (r.get("segment") or "").strip().upper()
            r["competitor"] = (r.get("competitor") or "no").strip().lower()
            for k in r:
                if isinstance(r[k], str):
                    r[k] = r[k].replace("—", ",").replace("–", "-").strip()
            if d in seen:
                print("repeat inside batch:", d, sl)
                continue
            seen.add(d)
            rows.append({c: r.get(c, "") for c in COLS})
with open("00_candidates.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)
from collections import Counter
print(len(rows), "rows")
print(Counter((r["segment"], r["country"]) for r in rows))
print("competitors:", [r["webDomain"] for r in rows if r["competitor"] == "yes"])
