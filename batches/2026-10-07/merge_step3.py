"""Builds 02_enriched.csv (DR 40+) and 02_low_dr.csv from step3/out_0..4.csv for backlink-2026-10-07."""
import csv, collections
base = [r["webDomain"] for r in csv.DictReader(open("step3_input.csv"))]
out = {}
for i in range(5):
    for r in csv.DictReader(open(f"step3/out_{i}.csv")):
        out[r["webDomain"]] = r
missing = [d for d in base if d not in out]
assert not missing, missing
cols = ("companyName,webDomain,domainRating,country,serviceType,segment,visualScore,backlinkExchange,backlinkEvidence,"
        "dataSource,competitor,drStatus,videoSchemaGap,latestPost,blogUrl,competitorDecision,pool,postsRead,"
        "outsideDomainCount,recentPosts,notes").split(",")
rows = [out[d] for d in base]
for r in rows:
    dr = int(r["domainRating"] or 0)
    r["drStatus"] = "pass" if dr >= 40 else ("low" if r["domainRating"] else "unknown")
enriched = [r for r in rows if r["drStatus"] == "pass"]
low = [r for r in rows if r["drStatus"] != "pass"]
for fn, data in (("02_enriched.csv", enriched), ("02_low_dr.csv", low)):
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(data)
print("enriched", len(enriched), "low", len(low))
print(collections.Counter((r["pool"], r["backlinkExchange"]) for r in rows))
drs = [int(r["domainRating"]) for r in enriched]
print("DR", min(drs), max(drs))
print("unchecked:", [(r["webDomain"], r["notes"][:80]) for r in rows if r["backlinkExchange"] == "unchecked"])
print("No:", [r["webDomain"] for r in rows if r["backlinkExchange"] == "No"])
