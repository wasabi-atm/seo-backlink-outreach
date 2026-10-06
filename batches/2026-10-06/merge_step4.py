"""Builds 03_backlink_targets.csv (best 160, 80 per segment), 03_spares.csv and 03_dropped.csv (dead, not logged)
from 02_enriched.csv and step4/out_0..4.csv for backlink-2026-10-06.
Ranking inside each segment: article fit (strong, ok, weak), then link habits (Yes, Some, unchecked, No),
then UK and UAE before US, then the original 160 before the buffer, then DR."""
import csv, collections
PER_SEG = 80
base = {r["webDomain"]: r for r in csv.DictReader(open("02_enriched.csv"))}
picks = {}
for i in range(5):
    for r in csv.DictReader(open(f"step4/out_{i}.csv")):
        picks[r["webDomain"].strip()] = r
assert set(picks) == set(base), sorted(set(base) ^ set(picks))
cols = ("companyName,webDomain,domainRating,country,serviceType,segment,offer,articleTitle,articleUrl,articleTopic,"
        "linkPlacement,articleHook,videoSchemaGap,articleDate,articlePublished,publishedSource,fit,competitor,"
        "competitorDecision,backlinkExchange,backlinkEvidence,hookSource,pool,notes").split(",")
rows, dead = [], []
for d, b in base.items():
    p = picks[d]
    r = {**b, **{k: v for k, v in p.items() if k != "notes"}}
    r["notes"] = "; ".join(x for x in (p.get("notes", "").strip(), ) if x)
    r["fit"] = (r.get("fit") or "").strip().lower()
    (dead if r["fit"] == "dead" else rows).append(r)
FIT = {"strong": 0, "ok": 1, "weak": 2}
LINK = {"Yes": 0, "Some": 1, "unchecked": 2, "No": 3}
def key(r):
    return (FIT.get(r["fit"], 3), LINK.get(r["backlinkExchange"], 2), 0 if r["country"] in ("UK", "UAE") else 1,
            0 if r["pool"] == "main" else 1, -int(r["domainRating"] or 0))
keep, spare = [], []
for seg in "AB":
    s = sorted([r for r in rows if r["segment"] == seg], key=key)
    keep += s[:PER_SEG]; spare += s[PER_SEG:]
for fn, data in (("03_backlink_targets.csv", keep), ("03_spares.csv", spare), ("03_dropped.csv", dead)):
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(data)
print("targets", len(keep), collections.Counter((r["segment"], r["country"]) for r in keep))
print("fit", collections.Counter(r["fit"] for r in keep), "links", collections.Counter(r["backlinkExchange"] for r in keep))
print("pool", collections.Counter(r["pool"] for r in keep), "offers", collections.Counter(r["offer"] for r in keep))
print("weak kept:", [r["webDomain"] for r in keep if r["fit"] == "weak"])
print("main rows left out:", [(r["webDomain"], r["fit"], r["backlinkExchange"]) for r in spare if r["pool"] == "main"])
print("buffer rows taken in:", [(r["webDomain"], r["fit"], r["backlinkExchange"]) for r in keep if r["pool"] == "buffer"])
print("dead:", [(r["webDomain"], r["notes"][:70]) for r in dead])
print("old published:", [(r["webDomain"], r["articlePublished"]) for r in keep if r["articlePublished"] and r["articlePublished"] < "2024-10-01"])
print("no date:", sum(1 for r in keep if not r["articlePublished"] and not r["articleDate"]))
bad = [r["webDomain"] for r in keep for c in cols if any(ch in (r.get(c) or "") for ch in "—–")]
print("dash rows:", sorted(set(bad)))
