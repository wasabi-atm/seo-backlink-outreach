"""Builds the Video SEO list from every candidate file, render and Apify result in this folder.

    python build_list.py

1. 00_candidates_all.csv: all candidate files in one, first file wins on a repeated domain.
2. video/video_check.csv: all renders in one. video_retry rows replace earlier rows (the retry
   re-rendered failed pages and old-rule html5 hits).
3. video/apify_results.csv: all apify_out_*.csv in one.
4. Runs video_schema.py merge on 00_candidates_all.csv, then writes 01_video_gap.csv with every
   videoSchemaGap = yes row that is not in drop.txt.
"""
import csv, glob, os, subprocess, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRIPT = os.path.join(REPO, "skill", "mta-backlink-outreach", "scripts", "video_schema.py")
CANDIDATES = ["00_candidates_old.csv", "00_candidates_ukuae.csv", "00_candidates_us.csv",
              "00_candidates_uk2.csv", "00_candidates_us2.csv", "00_candidates_uae2.csv"]
RENDERS = ["video_old", "video_ukuae", "video_us", "video_uk2", "video_us2", "video_uae2", "video_retry"]
CHECK_COLS = ["webDomain", "url", "pageTitle", "hasVideo", "videoPlatform", "pageVideoObject", "error"]


def rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write(path, cols, data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(data)


cands, seen = [], set()
for f in CANDIDATES:
    for r in rows(f):
        if r["webDomain"] not in seen:
            seen.add(r["webDomain"])
            cands.append(r)
checks = {}
for d in RENDERS:
    p = os.path.join(d, "video_check.csv")
    if os.path.exists(p):
        for r in rows(p):
            checks[r["webDomain"]] = r
for r in cands:
    r["pageTitle"] = checks.get(r["webDomain"], {}).get("pageTitle", "")
    r["videoPlatform"] = checks.get(r["webDomain"], {}).get("videoPlatform", "")
cols = ["companyName", "webDomain", "country", "serviceType", "pageTitle", "videoPlatform", "source"]
write("00_candidates_all.csv", cols, cands)

os.makedirs("video", exist_ok=True)
write("video/video_check.csv", CHECK_COLS, checks.values())
write("video/apify_results.csv", ["webDomain", "videoObject", "apifyStatus"],
      [r for f in sorted(glob.glob("apify_out_*.csv")) for r in rows(f)])
subprocess.run([sys.executable, SCRIPT, "merge", "00_candidates_all.csv", "video/"], check=True,
               stdout=subprocess.DEVNULL)

drop = set(open("drop.txt").read().split()) if os.path.exists("drop.txt") else set()
merged = rows("00_candidates_all.csv")
gap = [r for r in merged if r.get("videoSchemaGap") == "yes" and r["webDomain"] not in drop]
write("01_video_gap.csv", list(merged[0].keys()), gap)
count = lambda key: {v: sum(r[key] == v for r in gap) for v in sorted({r[key] for r in gap})}
print(f"{len(cands)} candidates, {len(checks)} rendered. videoSchemaGap yes, not dropped: {len(gap)} {count('country')}")
unk = [r for r in merged if r.get("videoSchemaGap") == "unknown" and r["webDomain"] not in drop]
print(f"unknown: {len(unk)}")
