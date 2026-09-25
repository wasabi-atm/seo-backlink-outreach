"""Writes an Apify input list (webDomain,url) from one or more video_check.csv files:
homepages with a video and no VideoObject in the render, minus dropped domains and anything
already sent to Apify (apify_in_*.csv). The first three renders ran before plain <video> tags
needed player controls, so their html5-only hits are skipped (video_retry re-renders them).

    python make_apify_in.py apify_in_2.csv video_us/video_check.csv [more video_check.csv ...]
"""
import csv, glob, sys

DROP = set(open("drop.txt").read().split()) if __import__("os").path.exists("drop.txt") else set()
OLD_RULE = {"video_old", "video_ukuae", "video_us"}
done = {r["webDomain"] for f in glob.glob("apify_in_*.csv") for r in csv.DictReader(open(f))}
out = []
for f in sys.argv[2:]:
    for r in csv.DictReader(open(f)):
        if (r["hasVideo"] == "yes" and r["pageVideoObject"] == "no" and not (r["videoPlatform"] == "html5" and f.split("/")[0] in OLD_RULE)
                and r["webDomain"] not in DROP and r["webDomain"] not in done):
            out.append({"webDomain": r["webDomain"], "url": r["url"]})
with open(sys.argv[1], "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["webDomain", "url"])
    w.writeheader()
    w.writerows(out)
print(len(out), "rows ->", sys.argv[1])
