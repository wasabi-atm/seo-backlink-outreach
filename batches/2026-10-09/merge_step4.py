"""Builds 03_backlink_targets.csv (every non-dead row) and 03_dropped.csv (dead) from 02_enriched.csv and step4/out_0..4.csv for backlink-2026-10-09."""
import csv, collections
base = {r["webDomain"]: r for r in csv.DictReader(open("02_enriched.csv", encoding="utf-8-sig"))}
picks = {}
for i in range(5):
    for r in csv.DictReader(open(f"step4/out_{i}.csv", encoding="utf-8-sig")):
        picks[r["webDomain"].strip()] = r
assert set(picks) == set(base), sorted(set(base) ^ set(picks))
cols = ("companyName,webDomain,domainRating,country,serviceType,segment,offer,articleTitle,articleUrl,articleTopic,"
        "linkPlacement,articleHook,videoSchemaGap,articleDate,articlePublished,publishedSource,fit,competitor,"
        "competitorDecision,backlinkExchange,backlinkEvidence,hookSource,pool,notes").split(",")
rows, dead = [], []
for d, b in base.items():
    p = picks[d]
    r = {**b, **{k: v for k, v in p.items() if k != "notes"}}
    r["notes"] = p.get("notes", "").strip()
    r["fit"] = (r.get("fit") or "").strip().lower()
    (dead if r["fit"] == "dead" else rows).append(r)
FIT = {"strong": 0, "ok": 1, "weak": 2}
LINK = {"Yes": 0, "Some": 1, "unchecked": 2, "No": 3}
rows.sort(key=lambda r: (r["segment"], FIT.get(r["fit"], 3), LINK.get(r["backlinkExchange"], 2), 0 if r["country"] in ("UK", "UAE") else 1, -int(r["domainRating"] or 0)))
for fn, data in (("03_backlink_targets.csv", rows), ("03_dropped.csv", dead)):
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(data)
print("targets", len(rows), collections.Counter((r["segment"], r["country"]) for r in rows))
print("fit", collections.Counter(r["fit"] for r in rows), "links", collections.Counter(r["backlinkExchange"] for r in rows))
print("offers", collections.Counter(r["offer"] for r in rows))
print("weak:", [r["webDomain"] for r in rows if r["fit"] == "weak"])
print("dead:", [(r["webDomain"]) for r in dead])
print("no date:", sum(1 for r in rows if not r["articlePublished"] and not r["articleDate"]))
print("old:", [(r["webDomain"], r["articlePublished"]) for r in rows if r["articlePublished"] and r["articlePublished"] < "2024-10-01"])
bad = sorted({r["webDomain"] for r in rows for c in cols if any(ch in (r.get(c) or "") for ch in "—–")})
print("dash rows:", bad)
print("competitor offers:", [(r["webDomain"], r["offer"]) for r in rows if r["competitor"] == "yes"])
print("segA wrong offer:", [r["webDomain"] for r in rows if r["segment"] == "A" and r["offer"] != "Founder's quote swap"])
