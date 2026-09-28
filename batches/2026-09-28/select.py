"""Pick 150 prospects (75 per segment) for backlink-2026-09-28, UK and UAE first, then US.
Sources: vetting_vs.csv (SaaS pool), vetting_m.csv (UK martech and studios), vetting_u.csv (UAE),
vetting_a.csv (UK agencies), and the 25 Sep spares (vetted 25 Sep, 2026-09-25/vetting.csv).
Keep: visualScore 3.5+, no hard fail, DR 40+, not a HubSpot drop, clean in dedupe (00_candidates_clean.csv).
Rank in each bucket: blog dates found in the last 12 months first, then visualScore, then DR.
Rows flagged as possible competitors go last in their bucket; only those picked are asked about.
One company per group (G42, Core42 and Presight are all G42)."""
import csv, json

QUOTA = {"A": [("UAE", 12), ("UK", 45), ("US", 75)], "B": [("UAE", 22), ("UK", 38), ("US", 75)]}
PER_SEG = 75
GROUPS = [["g42.ai", "core42.ai", "presight.ai"]]
DECISIONS = {"columnfivemedia.com": "include"}  # user, 25 Sep: include, quote swap only
SVC = json.load(open("service_types.json")) if __import__("os").path.exists("service_types.json") else {}

clean = {r["webDomain"] for r in csv.DictReader(open("00_candidates_clean.csv"))}
cand = {r["webDomain"]: r for r in csv.DictReader(open("00_candidates.csv"))}
hub = json.load(open("hubspot_drop.json"))
dr = {}
for f in ("dr_free_vs.txt", "dr_free_new.txt"):
    for l in open(f):
        d, v = l.split()
        dr[d] = float(v)

rows = []
for f in ("vetting_vs.csv", "vetting_m.csv", "vetting_u.csv", "vetting_a.csv"):
    for r in csv.DictReader(open(f)):
        rows.append(r)
spares = {r["webDomain"] for r in csv.DictReader(open("pool_spares.csv"))}
for r in csv.DictReader(open("../2026-09-25/vetting.csv")):
    if r["webDomain"] in spares:
        r["source"] = "2026-09-25 spares"
        rows.append(r)

ok = []
seen = set()
for r in rows:
    d = r["webDomain"]
    if d in seen or d not in clean or d in hub:
        continue
    seen.add(d)
    c = cand[d]
    r["competitor"], r["competitorReason"] = c["competitor"], c["competitorReason"]
    r["segment"], r["country"] = c["segment"], c["country"]
    r["serviceType"] = SVC.get(d) or c["serviceType"] or r.get("serviceType", "")
    r["domainRating"] = int(float(r.get("domainRating") or dr.get(d, 0)))
    r["competitorDecision"] = DECISIONS.get(d, "")
    if float(r["visualScore"]) < 3.5 or r["hardFail"] or r["domainRating"] < 40:
        continue
    if r["competitorDecision"] in ("exclude", "skip"):
        continue
    ok.append(r)

def key(o):
    return (o["competitor"] == "yes" and o["competitorDecision"] != "include", -int(int(o["recentPosts"] or 0) > 0),
            -float(o["visualScore"]), -o["domainRating"])

picked = []
for seg, plan in QUOTA.items():
    chosen = []
    for country, cap in plan:
        pool = sorted([o for o in ok if o["segment"] == seg and o["country"] == country], key=key)
        for o in pool:
            if len([x for x in chosen if x["country"] == country]) >= cap or len(chosen) >= PER_SEG:
                break
            grp = next((g for g in GROUPS if o["webDomain"] in g), None)
            if grp and any(x["webDomain"] in grp for x in picked + chosen):
                continue
            chosen.append(o)
    picked += chosen
ids = {o["webDomain"] for o in picked}
spare = sorted([o for o in ok if o["webDomain"] not in ids], key=key)

cols = ["companyName", "webDomain", "country", "serviceType", "segment", "domainRating", "visualScore", "visualNotes",
        "competitor", "competitorReason", "competitorDecision", "blogUrl", "latestPost", "recentPosts", "source"]
for name, rs in (("01_prospects.csv", picked), ("01_spares.csv", spare)):
    with open(name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(rs)
from collections import Counter
print("ok", len(ok), "picked", len(picked), Counter((o["segment"], o["country"]) for o in picked))
print("spares", len(spare), Counter((o["segment"], o["country"]) for o in spare))
print("flagged in picked:", [o["webDomain"] for o in picked if o["competitor"] == "yes"])
