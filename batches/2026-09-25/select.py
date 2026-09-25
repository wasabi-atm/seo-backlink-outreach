"""Pick 150 prospects (75 per segment) from vetting.csv, spread across UK, US and UAE.
The last batch was mostly US, so UK and UAE are filled first. Ranked by visualScore, then posts in
the last 12 months, then DR. Everything else that passed is kept in 01_spares.csv for top-ups."""
import csv
from collections import Counter

QUOTA = {"A": [("UAE", 12), ("UK", 36), ("US", 75)], "B": [("UAE", 20), ("UK", 30), ("US", 75)]}
PER_SEG = 75
DECISIONS = {"vyond.com": "include", "columnfivemedia.com": "include"}  # user, 25 Sep: include, quote swap only

v = list(csv.DictReader(open("vetting.csv")))
ok = [o for o in v if float(o["visualScore"]) >= 3.5 and not o["hardFail"]]
key = lambda o: (-float(o["visualScore"]), -int(o["recentPosts"] or 0), -float(o["domainRating"]))
picked = []
for seg, plan in QUOTA.items():
    chosen = []
    for country, cap in plan:
        pool = sorted([o for o in ok if o["segment"] == seg and o["country"] == country], key=key)
        room = PER_SEG - len(chosen)
        chosen += pool[:min(cap, room)]
    picked += chosen
ids = {o["webDomain"] for o in picked}
spares = sorted([o for o in ok if o["webDomain"] not in ids], key=key)

cols = ["companyName", "webDomain", "country", "serviceType", "segment", "domainRating", "visualScore", "visualNotes",
        "competitor", "competitorReason", "competitorDecision", "blogUrl", "latestPost", "recentPosts"]
for name, rows in (("01_prospects.csv", picked), ("01_spares.csv", spares)):
    with open(name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            r["competitorDecision"] = DECISIONS.get(r["webDomain"], "")
            w.writerow(r)
print("picked", len(picked), Counter((o["segment"], o["country"]) for o in picked))
print("spares", len(spares), Counter((o["segment"], o["country"]) for o in spares))
print("competitors in picked:", [o["webDomain"] for o in picked if o["competitor"] == "yes"])
