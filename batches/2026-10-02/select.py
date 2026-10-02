"""Builds 01_prospects.csv, 01_spares.csv, 01_dropped.csv for backlink-2026-10-02 from 00_candidates_clean.csv and vetting.csv.
No screenshots in the cloud, so visualScore is blank; vetting is the Apify homepage scan plus the research agents' blog checks."""
import csv, collections
v = {r["webDomain"]: r for r in csv.DictReader(open("vetting.csv"))}
rows = list(csv.DictReader(open("00_candidates_clean.csv")))
def hard(d):
    r = v.get(d)
    if not r: return "no vetting row"
    if r["loaded"] != "True": return "hard fail: homepage does not load"
    if r["adNetworks"].strip(): return "hard fail: ad network " + r["adNetworks"]
    fw = r["farmWords"].lower()
    if any(w in fw for w in ("casino", "betting", "sportsbook", "cbd", "payday")): return "farm word: " + r["farmWords"]
    return ""
keep, drop = [], []
for r in rows:
    d = r["webDomain"]; h = hard(d); r["competitorDecision"] = ""; r["visualScore"] = ""
    note = "not scored (no screenshots in cloud); homepage scan clean"
    if v.get(d) and v[d]["writeForUs"] == "True": note += "; write for us or contribute link (shows they take outside content)"
    r["visualNotes"] = note
    if h and d != "treasuryprime.com": r["dropReason"] = h; drop.append(r)
    else:
        if d == "treasuryprime.com": r["visualNotes"] = "farm word betting in visible text, check context; " + note
        keep.append(r)
def key(r):
    pri = 0 if r["country"] in ("UK", "UAE") else 1
    dated = 0 if r["latestPost"] else 1
    return (pri, dated, -(int(r["latestPost"].replace("-", "")) if r["latestPost"] else 0), -int(r["domainRating"] or 0))
out, spares = [], []
for seg in "AB":
    s = sorted([r for r in keep if r["segment"] == seg], key=key)
    out += s[:75]; spares += s[75:]
cols = "companyName,webDomain,country,serviceType,segment,visualScore,visualNotes,competitor,competitorDecision,domainRating,blogUrl,latestPost,notes".split(",")
for fn, data in (("01_prospects.csv", out), ("01_spares.csv", spares)):
    w = csv.DictWriter(open(fn, "w", newline=""), fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(data)
w = csv.DictWriter(open("01_dropped.csv", "w", newline=""), fieldnames=cols + ["dropReason"], extrasaction="ignore"); w.writeheader(); w.writerows(drop)
print(len(out), collections.Counter((r["segment"], r["country"]) for r in out))
print("spares", len(spares), collections.Counter((r["segment"], r["country"]) for r in spares))
print("undated in picks", [(r["webDomain"], r["segment"]) for r in out if not r["latestPost"]])
print("dropped", [(r["webDomain"], r["dropReason"]) for r in drop])
