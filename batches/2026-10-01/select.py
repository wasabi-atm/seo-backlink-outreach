"""Builds 01_prospects.csv and 01_spares.csv for backlink-2026-10-01 from 00_candidates_clean.csv.
No screenshots in the cloud, so visualScore is blank; vetting is the Apify homepage scan (vetting.csv) plus the research agents' blog checks."""
import csv
HARD = {
 "improvado.io": "hard fail: Taboola ad script on homepage",
 "luxhabitat.ae": "hard fail: DoubleClick ads; also a consumer property portal",
 "yaspa.com": "hard fail: casino and sportsbook content (gambling payments)",
}
USER_DROP = {d: "user: drop Dubai real estate brokerages (consumer lean)" for d in
 ["famproperties.com","drivenproperties.com","metropolitan.realestate","bhomes.com","allsoppandallsopp.com","providentestate.com","hausandhaus.com"]}
COMP = {"rewind.ae": "include", "animationstudio.ae": "include"}
NOTES = {
 "makeagency.co.uk": "farm word hit (betting, sportsbook) on homepage, likely a client; check at Step 4",
 "thepodcasthost.com": "homepage behind a bot check for the scanner; blog checked by research agent",
 "railway.com": "homepage behind a bot check for the scanner; blog checked by research agent",
 "morohub.com": "homepage renders in JavaScript; blog checked by research agent",
 "amvbbdo.com": "homepage scan failed; blog checked by research agent",
 "amiviz.com": "homepage scan failed; blog checked by research agent",
 "meirc.com": "homepage scan failed; blog checked by research agent",
}
rows = list(csv.DictReader(open("00_candidates_clean.csv")))
rows.append(dict(companyName="Clay", webDomain="clay.com", country="US", serviceType="Sales data and GTM SaaS", segment="A",
    competitor="no", competitorReason="", domainRating="80", blogUrl="https://www.clay.com/blog", latestPost="2026-09-30",
    notes="HQ New York. Brand match with clay.global in the ledger; user confirmed a different company (1 Oct)", slice="A_US"))
keep, drop = [], []
for r in rows:
    d = r["webDomain"]
    r["competitorDecision"] = COMP.get(d, "")
    r["visualScore"] = ""
    r["visualNotes"] = NOTES.get(d, "not scored (no screenshots in cloud); homepage scan clean")
    if d in HARD or d in USER_DROP:
        r["dropReason"] = HARD.get(d) or USER_DROP[d]; drop.append(r)
    else: keep.append(r)
def key(r):
    pri = 0 if r["country"] in ("UK", "UAE") else 1
    return (pri, -(int(r["latestPost"].replace("-", "")) if r["latestPost"] else 0), -int(r["domainRating"] or 0))
out, spares = [], []
for seg in "AB":
    s = sorted([r for r in keep if r["segment"] == seg], key=key)
    out += s[:75]; spares += s[75:]
cols = "companyName,webDomain,country,serviceType,segment,visualScore,visualNotes,competitor,competitorDecision,domainRating,blogUrl,latestPost,notes".split(",")
for fn, data in (("01_prospects.csv", out), ("01_spares.csv", spares)):
    w = csv.DictWriter(open(fn, "w", newline=""), fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(data)
w = csv.DictWriter(open("01_dropped.csv", "w", newline=""), fieldnames=cols + ["dropReason"], extrasaction="ignore"); w.writeheader(); w.writerows(drop)
import collections
print(len(out), collections.Counter((r["segment"], r["country"]) for r in out))
print("spares", len(spares), collections.Counter((r["segment"], r["country"]) for r in spares))
print("no date in picks", sum(1 for r in out if not r["latestPost"]))
