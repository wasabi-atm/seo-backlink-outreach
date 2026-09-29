"""Merge step4/out_*.csv (one agent per group of 25) into 03_backlink_targets.csv.
Skill columns first, then helper columns for Step 5 (articleDate, fit, status, hookSource, notes, ...)."""
import csv, glob, re
from collections import Counter

base = {r["webDomain"]: r for r in csv.DictReader(open("02_enriched.csv"))}
p1 = {r["webDomain"]: r for r in csv.DictReader(open("01_prospects.csv"))}
for d, b in base.items():
    b["competitorDecision"] = p1.get(d, {}).get("competitorDecision", "")
# Sites the Step 4 agents flag as also selling video or motion work go here after the user decides (webDomain -> reason).
STEP4_COMPETITORS = {}  # filled after the user decides on any site flagged in Step 4
for d, why in STEP4_COMPETITORS.items():
    base[d].update(competitor="yes", competitorReason=why, competitorDecision="include")
picks = {}
for f in sorted(glob.glob("step4/out_*.csv")):
    for r in csv.DictReader(open(f)):
        picks[r["webDomain"].strip()] = r

cols = ["companyName", "webDomain", "domainRating", "country", "serviceType", "segment", "offer", "articleTitle",
        "articleUrl", "articleTopic", "linkPlacement", "articleHook", "videoSchemaGap",
        "articleDate", "fit", "status", "hookSource", "notes", "backlinkExchange", "competitor", "competitorDecision"]
out, missing = [], []
for d, b in base.items():
    p = picks.get(d)
    if not p:
        missing.append(d)
        p = {}
    fit = (p.get("fit") or "").strip().lower()
    offer = p.get("offer", "")
    if b["segment"] == "A" or b.get("competitorDecision") == "include":
        offer = "Founder's quote swap"
    row = dict(companyName=b["companyName"], webDomain=d, domainRating=b["domainRating"], country=b["country"],
               serviceType=b["serviceType"], segment=b["segment"], offer=offer,
               articleTitle=p.get("articleTitle", ""), articleUrl=p.get("articleUrl", ""),
               articleTopic=p.get("articleTopic", ""), linkPlacement=p.get("linkPlacement", ""),
               articleHook=p.get("articleHook", ""), videoSchemaGap="", articleDate=p.get("articleDate", ""), fit=fit,
               status=("ready" if fit in ("strong", "ok") else "review: weak fit" if fit == "weak" else "no article"),
               hookSource=p.get("hookSource", ""), notes=p.get("notes", ""),
               backlinkExchange=b["backlinkExchange"], competitor=b.get("competitor", "no"),
               competitorDecision=b.get("competitorDecision", ""))
    for k, v in row.items():
        row[k] = re.sub("[–—]", "-", str(v)).strip()
    out.append(row)

order = {"ready": 0, "review: weak fit": 1, "no article": 2}
out.sort(key=lambda r: (order[r["status"]], {"strong": 0, "ok": 1}.get(r["fit"], 2), r["segment"], -float(r["domainRating"])))
with open("03_backlink_targets.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(out)
print(Counter(r["status"] for r in out), Counter(r["fit"] for r in out))
print("offers:", Counter(r["offer"] for r in out))
print("missing from agent outputs:", missing)
dash = [r["webDomain"] for r in out if any(c in "".join(r.values()) for c in "–—")]
print("rows with dashes left:", dash)
