import json, glob, csv, collections
rows = collections.OrderedDict()
skips = set()
for p in sorted(glob.glob("work/results_*.jsonl")):
    for l in open(p):
        l = l.strip()
        if not l: continue
        try: r = json.loads(l)
        except Exception: continue
        d = (r.get("webDomain") or "").lower().replace("www.", "")
        if r.get("verdict") == "pass": rows.setdefault(d, r)
        else: skips.add(d)
conflict = [d for d in rows if d in skips]
print("passes", len(rows), "conflicts (pass in one file, skip in another):", conflict)
keep = [r for d, r in rows.items() if d not in conflict]
cols = ["companyName","webDomain","country","segment","competitor","drChecked","articleTitle","articleUrl","articleDate","articleTopic","linkPlacement","articleHook","offerSuggestion","offerLine","articleShortName","publicEmail","notes"]
with open("03_backlink_targets_raw.csv", "w", newline="") as f:
    w = csv.DictWriter(f, cols, extrasaction="ignore"); w.writeheader()
    for r in keep: w.writerow(r)
print("kept", len(keep), "competitors", sum(1 for r in keep if r.get("competitor") == "yes"))
