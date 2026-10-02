"""Builds 03_backlink_targets.csv from 02_enriched.csv and step4/out_0..4.csv. Dead rows go to 03_dropped.csv (not logged)."""
import csv, collections
base = {r["webDomain"]: r for r in csv.DictReader(open("02_enriched.csv"))}
picks = {}
for i in range(5):
    for r in csv.DictReader(open(f"step4/out_{i}.csv")):
        picks[r["webDomain"]] = r
assert set(picks) == set(base), set(base) ^ set(picks)
cols = "companyName,webDomain,domainRating,country,serviceType,segment,offer,articleTitle,articleUrl,articleTopic,linkPlacement,articleHook,videoSchemaGap,articleDate,articlePublished,publishedSource,fit,competitor,competitorDecision,backlinkExchange,hookSource,notes".split(",")
keep, drop = [], []
for d, b in base.items():
    r = {**b, **picks[d]}
    (drop if r["fit"] == "dead" else keep).append(r)
for fn, rows in (("03_backlink_targets.csv", keep), ("03_dropped.csv", drop)):
    w = csv.DictWriter(open(fn, "w", newline=""), fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
print(len(keep), len(drop), collections.Counter(r["fit"] for r in keep), collections.Counter(r["segment"] for r in keep), collections.Counter(r["offer"] for r in keep))
print("weak:", [r["companyName"] for r in keep if r["fit"] == "weak"])
print("dead:", [r["companyName"] for r in drop])
print("old published:", [(r["webDomain"], r["articlePublished"], r["articleDate"]) for r in keep if r["articlePublished"] and r["articlePublished"] < "2024-10-01"])
print("no date:", sum(1 for r in keep if not r["articlePublished"] and not r["articleDate"]))
