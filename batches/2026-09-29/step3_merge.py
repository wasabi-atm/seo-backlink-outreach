"""Step 3 for backlink-2026-09-29: merge the agents' link-habit results (step3/result_*.json) into 02_enriched.csv.
Same rules as 28 Sep: Yes = 10+ outside business domains, 2+ outside companies quoted, or a guest/contributor page;
Some = 3-9 domains or 1 outside company quoted; No = fewer. DR comes from the 28 Sep free-endpoint check (all 150 are 40+),
so 02_low_dr.csv is empty this run (no new candidates were researched)."""
import csv, glob, json
from collections import Counter

prospects = list(csv.DictReader(open("01_prospects.csv")))
res = {}
for f in sorted(glob.glob("step3/result_*.json")):
    for r in json.load(open(f)):
        res[r["webDomain"]] = r

COLS = ["companyName", "webDomain", "domainRating", "country", "serviceType", "segment", "visualScore", "backlinkExchange",
        "backlinkEvidence", "dataSource", "competitor", "drStatus", "videoSchemaGap"]
rows, missing = [], []
for p in prospects:
    d = p["webDomain"]
    r = res.get(d)
    if r is None:
        missing.append(d)
        r = {}
    n_posts = int(r.get("postsRead") or 0)
    doms = sorted(set(r.get("outsideDomains") or []))
    quoted = sorted(set(r.get("quotedCompanies") or []))
    guest = (r.get("guestSigns") or "").strip()
    if n_posts == 0 and not guest:
        bx, ev = "", "not checked: " + (r.get("note") or "no posts could be read")
    else:
        bx = "Yes" if (len(doms) >= 10 or len(quoted) >= 2 or guest) else "Some" if (len(doms) >= 3 or quoted) else "No"
        ev = f"{len(doms)} outside business domains linked in {n_posts} recent posts"
        if doms:
            ev += " (e.g. " + ", ".join(doms[:5]) + ")"
        if quoted:
            ev += "; quotes people from " + ", ".join(quoted[:3]) + (f" and {len(quoted) - 3} more" if len(quoted) > 3 else "")
        if guest:
            ev += "; guest post or contributor signs: " + guest
        if r.get("note"):
            ev += "; note: " + r["note"]
    ev = ev.replace("—", ",").replace("–", "-")
    rows.append(dict(companyName=p["companyName"], webDomain=d, domainRating=int(float(p["domainRating"])),
                     country=p["country"], serviceType=p["serviceType"], segment=p["segment"],
                     visualScore=p["visualScore"], backlinkExchange=bx, backlinkEvidence=ev,
                     dataSource="ahrefs-free (DR, 28 Sep), apify (posts)", competitor=p["competitor"], drStatus="pass",
                     videoSchemaGap="", competitorDecision=p.get("competitorDecision", ""),
                     blogUrl=r.get("blogUrlUsed") or p["blogUrl"], postsChecked=n_posts))

with open("02_enriched.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS + ["competitorDecision", "blogUrl", "postsChecked"])
    w.writeheader(); w.writerows(rows)
with open("02_low_dr.csv", "w", newline="") as f:
    csv.DictWriter(f, fieldnames=COLS).writeheader()

print("enriched", len(rows), Counter(r["backlinkExchange"] or "not checked" for r in rows))
print("missing from results:", missing)
print("not checked:", [(r["webDomain"], r["backlinkEvidence"][:90]) for r in rows if not r["backlinkExchange"]])
print("notes:", [(d, res[d]["note"]) for d in res if res[d].get("note")])
