"""Builds the 178-company validation files from the deep render and the Apify API results.

    python build_validation.py

Reads 02_video_seo_list.csv (the 100), 02_video_seo_spares.csv (78), 03_video_seo_contacts.csv
(contacts for the 100) and video_v2/ (video_check.csv after the deep render, apify_results.csv from
the API, player_scan.csv from player_scan.py: the video iframes each homepage loads the way Google renders it). Writes 04_video_seo_all.csv and four parts, 05_validate_part1.csv to part4.csv, with a
Google Rich Results Test link per row and an empty yourCheck column.
"""
import csv, os, subprocess, sys
from urllib.parse import quote

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRIPT = os.path.join(REPO, "skill", "mta-backlink-outreach", "scripts", "video_schema.py")
RICH_TEST = "https://search.google.com/test/rich-results?url="
CONTACT = ["firstName", "lastName", "jobTitle", "email", "contactRole", "emailSource", "instantlyCampaign", "manualCheck"]
COLS = ["part", "companyName", "webDomain", "country", "inList", "pageTitle", "homepageUrl", "richResultsTestUrl",
        "videoSchemaGap", "videoNote", "rrtCheckedByClaude", "vimeoAtLoad", "playersAtLoad",
        "videoPlatform", "renderedVideoObject", "iframeVideoObject", "apifyStatus", "apifyVideoObject", "apifyDetectedTypes",
        "videoSchema"] + CONTACT + ["yourCheck"]
# Google's Rich Results Test, run by hand on 25 Sep. It is the final word: (gap, what it showed).
RRT = {
    "posit.co": ("yes", "No items detected"),
    "toggl.com": ("yes", "No items detected"),
    "jumpcloud.com": ("yes", "Breadcrumbs, Local business, Organization; no Videos"),
    "netacea.com": ("yes", "Videos: hero_mobile only (Vimeo hero clip); the user confirmed the real video has no schema"),
    "alpheya.com": ("no", "Videos: 1 valid item, from the Vimeo player's own VideoObject"),
    "tribepad.com": ("no", "Videos: 1 valid item, from the Vimeo player's own VideoObject"),
    "altruistiq.com": ("yes", "Software Apps only; no Videos (its Vimeo player is hidden until clicked)"),
}


def rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write(path, cols, data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(data)


contacts = {r["webDomain"]: r for r in rows("03_video_seo_contacts.csv")}
checks = {r["webDomain"]: r for r in rows("video_v2/video_check.csv")}
apify = {r["webDomain"]: r for r in rows("video_v2/apify_results.csv")}
data = [dict(r, inList="main 100") for r in rows("02_video_seo_list.csv")] + \
       [dict(r, inList="spare") for r in rows("02_video_seo_spares.csv")]
for r in data:
    d = r["webDomain"]
    c, a = checks.get(d, {}), apify.get(d, {})
    home = c.get("url") or "https://" + d
    r.update(homepageUrl=home, richResultsTestUrl=RICH_TEST + quote(home, safe=""),
             videoPlatform=c.get("videoPlatform", r.get("videoPlatform", "")),
             renderedVideoObject=c.get("pageVideoObject", ""), iframeVideoObject=c.get("iframeVideoObject", ""),
             apifyStatus=a.get("apifyStatus", ""), apifyVideoObject=a.get("videoObject", ""),
             apifyDetectedTypes=a.get("detectedTypes", ""), yourCheck="")
    r.update({k: contacts.get(d, {}).get(k, "") for k in CONTACT})
write("04_video_seo_all.csv", COLS, data)

# Recompute videoSchema / videoSchemaGap / videoNote from the new checks.
subprocess.run([sys.executable, SCRIPT, "merge", "04_video_seo_all.csv", "video_v2/"], check=True, stdout=subprocess.DEVNULL)
data = rows("04_video_seo_all.csv")
scan = {r["webDomain"]: r for r in rows("video_v2/player_scan.csv")} if os.path.exists("video_v2/player_scan.csv") else {}
for r in data:
    ps = scan.get(r["webDomain"], {})
    r.update(vimeoAtLoad=ps.get("vimeoVerdict") or ps.get("error", ""), playersAtLoad=ps.get("players", ""),
             rrtCheckedByClaude=RRT.get(r["webDomain"], ("", ""))[1])
    if r["webDomain"] in RRT:
        gap = RRT[r["webDomain"]][0]
        r.update(videoSchema="FALSE" if gap == "yes" else "TRUE", videoSchemaGap=gap,
                 videoNote=("Google's Rich Results Test (25 Sep) shows no VideoObject for the real video" if gap == "yes"
                            else "Google's Rich Results Test (25 Sep) shows a Video item from the Vimeo player"))
    elif r["vimeoAtLoad"] == "real vimeo player":
        r.update(videoSchema="TRUE", videoSchemaGap="no",
                 videoNote="A real Vimeo player loads with the page. Vimeo's player carries its own VideoObject, which "
                           "Google's Rich Results Test shows as a Video item (confirmed on Alpheya and Tribepad). Not a gap.")
    elif r["vimeoAtLoad"] == "vimeo hero only" and r["videoSchemaGap"] == "yes":
        others = [x for x in r["playersAtLoad"].split("; ") if x and ("vimeo" not in x or "(hidden)" in x)]
        if others or set(r["videoPlatform"].split(", ")) - {"vimeo"}:
            r["videoNote"] += ("; Google shows a Video item only for a Vimeo hero loop, which does not count (the user's rule, "
                               "from Netacea); the real video has no schema")
        else:
            r.update(videoSchemaGap="check",
                     videoNote="The only video found is a Vimeo hero loop (Google shows it as a Video item). Check the site "
                               "has a real video before using the video lines")
    elif r["vimeoAtLoad"] == "vimeo hidden only" and r["videoSchemaGap"] == "yes":
        r["videoNote"] += "; the Vimeo player is hidden until clicked, so Google does not see its schema (as on Altruistiq)"
    elif r["vimeoAtLoad"] and r["vimeoAtLoad"] not in ("no vimeo at load",) and r["videoSchemaGap"] == "yes":
        r["videoNote"] += f"; the Vimeo check could not load the page ({r['vimeoAtLoad'][:60]}), so check it in the Rich Results Test"
size = -(-len(data) // 4)
for i in range(4):
    part = data[i * size:(i + 1) * size]
    for r in part:
        r["part"] = str(i + 1)
    write(f"05_validate_part{i + 1}.csv", COLS, part)
for r in data:
    r["part"] = str(data.index(r) // size + 1)
write("04_video_seo_all.csv", COLS, data)
gap = {v: sum(r["videoSchemaGap"] == v for r in data) for v in ("yes", "no", "check", "unknown")}
print(f"{len(data)} companies, videoSchemaGap {gap}; parts of {size}")
for r in data:
    if r["videoSchemaGap"] != "yes":
        print(f"  {r['videoSchemaGap']:7} {r['inList']:8} {r['webDomain']}: {r['videoNote']}")
