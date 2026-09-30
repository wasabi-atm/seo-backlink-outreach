"""Builds 12_video_seo_by_scale.csv: the 126 companies in 07 (with contacts) plus the 34 the user added
on 30 Sep (added34/), grouped by company scale, with Ahrefs and Similarweb metrics. Also writes one file
per scale: 12a_startup.csv, 12b_scaleup.csv, 12c_enterprise.csv (and 12d_scale_unknown.csv if any).

    <repo>/.venv-crawl/bin/python build_12_by_scale.py

Scale is by headcount: Startup up to 50 staff, Scaleup 51 to 500, Enterprise 501 and up. The band comes
from Apollo's free company search filtered by domain and staff range (metrics/apollo_bands.csv, the same
source the list was built from), with exact counts where an Apollo company lookup was done
(metrics/apollo_sizes.csv). Where Apollo has nothing, Similarweb's company range is used
(radeance/similarweb-scraper with in-depth data). scaleOverrides.csv, if present (webDomain, employees,
source), beats both.

Metrics:
  Ahrefs      metrics/ahrefs_api.csv if present (webDomain, domainRating, organicTraffic, ahrefsRank, from
              the Ahrefs connector), else the Apify actor scrapesage/ahrefs-scraper (metrics/ahrefs_*.json),
              which only covers domains with a public Ahrefs page.
  Similarweb  metrics/similarweb*.json: visits, bounce rate, average visit duration (dwell time), pages
              per visit, global rank.

A company that is already in a backlink campaign (outreach_ledger.csv) is flagged in backlinkCampaign and
must not be emailed (user's rule, 30 Sep).
"""
import csv, glob, json, os, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "skill", "mta-backlink-outreach", "scripts"))
from contacts import brand  # noqa: E402

CONTACT = ["firstName", "lastName", "jobTitle", "email", "contactRole", "emailSource", "instantlyCampaign", "manualCheck"]
COLS = (["companyScale", "employees", "scaleSource", "similarwebEmployees", "companyName", "webDomain", "country", "inList", "backlinkCampaign",
         "hasVideo", "videoPlatform", "videoSchema", "videoSchemaGap", "videoNote", "richResultsTestUrl",
         "ahrefsDR", "ahrefsOrganicTraffic", "ahrefsRank", "ahrefsSource",
         "similarwebVisits", "bounceRate", "avgVisitDuration", "avgVisitSeconds", "pagesPerVisit", "similarwebGlobalRank",
         "similarwebMonth", "similarwebConfidence"] + CONTACT + ["userVideo", "userOrganicTraffic", "category"])
ORDER = {"Startup": 0, "Scaleup": 1, "Enterprise": 2, "Unknown": 3}


def rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write(path, data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(data)


def scale(n):
    if n is None:
        return "Unknown"
    return "Startup" if n <= 50 else "Scaleup" if n <= 500 else "Enterprise"


def num(v):
    return "" if v in (None, "") else f"{v:g}" if isinstance(v, float) else str(v)


# Similarweb: later runs win over the test run
sw = {}
for f in sorted(glob.glob("metrics/similarweb*.json"), key=lambda p: "test" not in p):
    for it in json.load(open(f)):
        d = (it.get("domain") or "").lower().removeprefix("www.")
        if d and (d not in sw or it.get("totalVisits")):
            sw[d] = it
ahrefs = {}
for f in glob.glob("metrics/ahrefs_*.json"):
    for it in json.load(open(f)):
        ahrefs[it["domain"]] = dict(domainRating=it.get("domainRating"), organicTraffic=it.get("organicTraffic"),
                                    ahrefsRank=it.get("globalRank"), source="Apify scrapesage/ahrefs-scraper")
if os.path.exists("metrics/ahrefs_api.csv"):
    for r in rows("metrics/ahrefs_api.csv"):
        ahrefs[r["webDomain"]] = dict(r, source="Ahrefs API")
overrides = {r["webDomain"]: r for r in rows("scaleOverrides.csv")} if os.path.exists("scaleOverrides.csv") else {}
bands = {r["webDomain"]: r["apolloBand"] for r in rows("metrics/apollo_bands.csv")}
exact = {r["webDomain"]: int(r["employees"]) for r in rows("metrics/apollo_sizes.csv") if r["employees"]}
BAND_MAX = {"1-50": 50, "51-500": 500, "501+": 10 ** 6}
ledger = [r for r in rows(os.path.join(REPO, "outreach_ledger.csv")) if r["status"].strip().lower() != "not_sent"]  # as dedupe.py
by_domain = {r["rootDomain"] or r["webDomain"]: r for r in ledger}
by_brand = {brand(r["rootDomain"] or r["webDomain"]): r for r in ledger}

data = [dict(r, inList="07 (video, no schema)", videoSchemaGap="yes") for r in rows("11_video_seo_07_contacts.csv")]
video = {r["webDomain"]: r for r in rows("added34/video_result.csv")} if os.path.exists("added34/video_result.csv") else {}
for r in rows("added34/targets.csv"):
    v = video.get(r["webDomain"], {})
    data.append(dict(r, inList="added 30 Sep", country="", **{k: v.get(k, "") for k in
                     ("hasVideo", "videoPlatform", "videoSchema", "videoSchemaGap", "videoNote", "richResultsTestUrl")}))

for r in data:
    d = r["webDomain"]
    s, a = sw.get(d, {}), ahrefs.get(d, {})
    lo, hi = s.get("company_employees_min"), s.get("company_employees_max")
    r["similarwebEmployees"] = f"{lo:,}-{hi:,}" if lo and hi else f"up to {hi:,}" if hi else ""
    if d in overrides:
        n = int(overrides[d]["employees"])
        r.update(employees=overrides[d]["employees"], scaleSource=overrides[d]["source"])
    elif d in exact:
        n = exact[d]
        r.update(employees=str(n), scaleSource="Apollo")
    elif d in bands:
        n = BAND_MAX[bands[d]]
        r.update(employees=bands[d], scaleSource="Apollo")
    elif hi:
        n = hi
        r.update(employees=r["similarwebEmployees"], scaleSource="Similarweb")
    else:
        n = None
        r.update(employees="", scaleSource="")
    r["companyScale"] = scale(n)
    if not r.get("country") and s.get("company_headquarters"):  # the added 34: HQ country from Similarweb
        r["country"] = {"GB": "UK", "AE": "UAE"}.get(s["company_headquarters"], s["company_headquarters"])
    visits = s.get("totalVisits") or 0
    if not visits:  # Similarweb has no panel data for the site: it reports zeros, which are not real values
        s = {k: v for k, v in s.items() if k not in ("bounceRate", "timeOnSite", "pagesPerVisit")}
    r["similarwebConfidence"] = ("no data (site too small)" if not visits else
                                 "low (under 5,000 visits a month)" if visits < 5000 else "ok")
    secs = s.get("timeOnSite")
    r.update(similarwebVisits=num(visits) if visits else "",
             bounceRate=f"{s['bounceRate'] * 100:.1f}%" if s.get("bounceRate") is not None else "",
             avgVisitSeconds=f"{secs:.0f}" if secs is not None else "",
             avgVisitDuration=f"{int(secs // 60)}:{int(secs % 60):02d}" if secs is not None else "",
             pagesPerVisit=f"{s['pagesPerVisit']:.1f}" if s.get("pagesPerVisit") is not None else "",
             similarwebGlobalRank=num(s.get("rankGlobal")),
             similarwebMonth=(s.get("snapshotDate") or "")[:7],
             ahrefsDR=num(a.get("domainRating")), ahrefsOrganicTraffic=num(a.get("organicTraffic")),
             ahrefsRank=num(a.get("ahrefsRank")), ahrefsSource=a.get("source", ""))
    hit = by_domain.get(d)
    if not hit and r["inList"].startswith("added"):  # the 07 list was deduped already (Cube's brand match is CUBE, cube.global)
        hit = by_brand.get(brand(d))
    r["backlinkCampaign"] = f"{hit['campaign']} ({hit['status']} {hit['sentDate']}) - do not email" if hit else ""

data.sort(key=lambda r: (ORDER[r["companyScale"]], bool(r["backlinkCampaign"]), r["inList"], r["companyName"].lower()))
write("12_video_seo_by_scale.csv", data)
for i, s in enumerate(ORDER):
    part, path = [r for r in data if r["companyScale"] == s], f"12{'abcd'[i]}_{s.lower()}{'' if s != 'Unknown' else '_scale'}.csv"
    if part:
        write(path, part)
    elif os.path.exists(path):
        os.remove(path)
count = lambda key: {v: sum(r[key] == v for r in data) for v in sorted({r[key] for r in data})}
print(len(data), "companies; scale", count("companyScale"))
print("Similarweb confidence:", count("similarwebConfidence"))
print("no Similarweb engagement:", [r["webDomain"] for r in data if not r["bounceRate"]])
print("no Ahrefs DR:", sum(not r["ahrefsDR"] for r in data), "| no Ahrefs traffic:", sum(not r["ahrefsOrganicTraffic"] for r in data))
print("backlink campaign, do not email:", [r["webDomain"] for r in data if r["backlinkCampaign"]])
