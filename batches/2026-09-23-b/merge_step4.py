"""Rebuild 03_backlink_targets.csv from the Apify live-page crawl (24 Sep) and hook extraction."""
import csv, glob, re, sys
S = sys.argv[1]
base = list(csv.DictReader(open("03_backlink_targets.csv")))
hooks = {}
for f in sorted(glob.glob(S + "/hooks_out_[0-3].csv")):
    for r in csv.DictReader(open(f)): hooks[r["webDomain"]] = r
new = {r["webDomain"]: r for r in csv.DictReader(open(S + "/hooks_out_4.csv"))}
reasons = {"brightcove.com": "earlier article 404, no usable replacement found",
           "modulrfinance.com": "earlier article 404, no usable replacement found",
           "faculty.ai": "earlier article 404, no usable replacement found",
           "airbase.com": "blog redirects to Paylocity (acquired)"}
cols = ["companyName","webDomain","domainRating","country","serviceType","segment","offer","articleTitle","articleUrl","articleDate",
        "articleTopic","linkPlacement","articleHook","fit","status","hookSource","competitorDecision"]
out = []
for b in base:
    d = b["webDomain"]; row = {k: b.get(k, "") for k in cols}
    h = new.get(d) or hooks.get(d)
    if h and h.get("fit") != "dead":
        row.update(articleTitle=h["articleTitle"], articleDate=h.get("articleDate",""), articleTopic=h["articleTopic"],
                   linkPlacement=h["linkPlacement"], articleHook=h["articleHook"], fit=h["fit"],
                   hookSource="live page, Apify crawl 24 Sep 2026")
        if d in new: row["articleUrl"] = h["articleUrl"]
        row["status"] = "ready" if h["fit"] in ("strong", "ok") else "review: weak fit"
    else:
        row.update(articleTitle="", articleUrl="", articleDate="", linkPlacement="", fit="", hookSource="",
                   articleHook=(h or {}).get("articleHook", ""),
                   articleTopic=reasons.get(d) or ("article gone: " + (h or {}).get("articleHook","")[:120] if h else "no article found in blog crawl"))
        row["status"] = "no article"
    for k, v in row.items(): row[k] = re.sub("[–—]", "-", str(v))
    out.append(row)
order = {"ready": 0, "review: weak fit": 1, "no article": 2}
out.sort(key=lambda r: (order[r["status"]], {"strong":0,"ok":1}.get(r["fit"],2), r["segment"], -float(r["domainRating"])))
w = csv.DictWriter(open("03_backlink_targets.csv", "w", newline=""), fieldnames=cols); w.writeheader(); w.writerows(out)
from collections import Counter
print(Counter(r["status"] for r in out), Counter(r["fit"] for r in out))
print("no article:", [r["webDomain"] for r in out if r["status"] == "no article"])
