"""Builds 01_prospects.csv, 01_spares.csv, 01_dropped.csv for backlink-2026-10-06 from 00_candidates_clean.csv,
step2/vetting_*.csv and step2/competitor_decisions.csv. No screenshots in the cloud, so visualScore is blank and
videoSchemaGap is blank; vetting is the Apify homepage scan plus the research agents' blog checks."""
import csv, glob, collections, os
PER_SEG = 80
v = {}
for p in sorted(glob.glob("step2/vetting_*.csv")):
    for r in csv.DictReader(open(p)):
        v[r["webDomain"]] = r
hub = {r["webDomain"]: r for r in csv.DictReader(open("step2/hubspot_check.csv"))}
dec = {}
if os.path.exists("step2/competitor_decisions.csv"):
    dec = {r["webDomain"]: r["competitorDecision"] for r in csv.DictReader(open("step2/competitor_decisions.csv"))}
# Manual calls from reading the scan (see brief.md)
MANUAL_DROP = {"alcumus.com": "hard fail: homepage says the website is no longer available"}
RESEGMENT = {"harmonicinc.com": ("B", "Broadband network infrastructure (video business no longer on homepage)")}
FLAG_COMPETITOR = {"visla.us": "AI video creation platform for businesses (title: AI Video Workflow Platform for Business)",
                   "trypencil.com": "Generative AI ad creative platform, video and static ads for brands",
                   "whalar.com": "Creator and social agency, creator-led social video for brands",
                   "bravebison.com": "Digital marketing and social media group, social content arm"}
rows = list(csv.DictReader(open("00_candidates_clean.csv")))

def hard(d):
    r = v.get(d)
    if not r: return "no vetting row"
    if d in MANUAL_DROP: return MANUAL_DROP[d]
    if r["loaded"] != "True": return "hard fail: homepage does not load (Apify, normal and residential proxy)"
    if r["redirectedToOtherDomain"] == "True": return "hard fail: redirects to " + r["finalUrl"]
    if r["parked"] == "True": return "hard fail: parked"
    if r["adNetworks"].strip(): return "hard fail: ad network " + r["adNetworks"]
    fw = r["farmWords"].lower()
    if any(w in fw for w in ("casino", "betting", "sportsbook", "cbd", "payday")): return "hard fail: farm word " + r["farmWords"]
    return ""

keep, drop = [], []
for r in rows:
    d = r["webDomain"]
    if d in RESEGMENT:
        r["segment"], r["serviceType"] = RESEGMENT[d]
    if d in FLAG_COMPETITOR:
        r["competitor"], r["competitorReason"] = "yes", FLAG_COMPETITOR[d]
    r["visualScore"] = ""
    note = "not scored (no screenshots in cloud); homepage scan clean"
    vr = v.get(d, {})
    if vr.get("farmWords"): note += "; word '%s' on homepage, fits the business" % vr["farmWords"]
    if vr.get("writeForUs") == "True": note += "; write for us or contribute link"
    if d in hub and hub[d]["decision"].startswith("keep"): note += "; HubSpot lead, no deals"
    r["visualNotes"] = note
    if d in hub and hub[d]["decision"].startswith("drop"):
        r["dropReason"] = "HubSpot: open deal"; drop.append(r); continue
    h = hard(d)
    if h:
        r["dropReason"] = h; drop.append(r); continue
    if r["competitor"] == "yes":
        r["competitorDecision"] = dec.get(d, "")
        if r["competitorDecision"] != "include":
            r["dropReason"] = "competitor: " + (r["competitorDecision"] or "awaiting decision"); drop.append(r); continue
    else:
        r["competitorDecision"] = ""
    keep.append(r)

def key(r):
    pri = 0 if r["country"] in ("UK", "UAE") else 1
    lp = int(r["latestPost"].replace("-", "")) if r["latestPost"] else 0
    return (pri, -lp, -int(r["domainRating"] or 0))

out, spares = [], []
for seg in "AB":
    s = sorted([r for r in keep if r["segment"] == seg], key=key)
    out += s[:PER_SEG]; spares += s[PER_SEG:]
cols = ("companyName,webDomain,country,serviceType,segment,visualScore,visualNotes,competitor,competitorDecision,"
        "domainRating,blogUrl,latestPost,notes").split(",")
for fn, data in (("01_prospects.csv", out), ("01_spares.csv", spares)):
    with open(fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(data)
with open("01_dropped.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols + ["dropReason"], extrasaction="ignore"); w.writeheader(); w.writerows(drop)
print(len(out), collections.Counter((r["segment"], r["country"]) for r in out))
print("spares", len(spares), collections.Counter((r["segment"], r["country"]) for r in spares))
print("oldest picked post per segment:", {seg: min(r["latestPost"] for r in out if r["segment"] == seg) for seg in "AB"})
print("dropped", len(drop))
for r in drop: print("  ", r["webDomain"], "|", r["dropReason"])
