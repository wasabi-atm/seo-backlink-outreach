"""Turn the cheerio vetting dataset JSON into step2/vetting.csv with hard-fail notes. Usage: vet_convert.py items.json [items2.json ...]"""
import csv, json, sys
sys.path.insert(0, "/home/user/seo-backlink-outreach/skill/mta-backlink-outreach/scripts")
from dedupe import root_domain, brand
cands = {r["webDomain"]: r for r in csv.DictReader(open("00_candidates_clean.csv", encoding="utf-8"))}
items = {}
for p in sys.argv[1:]:
    data = json.load(open(p))
    data = data.get("items", data) if isinstance(data, dict) else data
    for it in data:
        if it.get("webDomain") and not it.get("#error"):
            items[it["webDomain"]] = it
cols = ["webDomain","loaded","finalUrl","redirectedToOtherDomain","adNetworks","farmWords","writeForUs","parked","outboundLinks","wordCount","title","h1","blogLink","notes"]
out = []
for d in cands:
    it = items.get(d)
    if not it:
        out.append({"webDomain": d, "loaded": False, "notes": "HARD FAIL: does not load (retry pending)"}); continue
    fin = root_domain(it.get("finalUrl", ""))
    redir = fin != d
    same_brand = redir and brand(fin) == brand(d)
    notes = []
    if redir and not same_brand: notes.append(f"HARD FAIL: redirects to {fin}")
    elif redir: notes.append(f"same brand, redirects to {fin}")
    if it.get("parked"): notes.append("HARD FAIL: parked")
    if it.get("adNetworks"): notes.append(f"HARD FAIL: ad network {it['adNetworks']}")
    for w in (it.get("farmWords") or "").split(";"):
        if w in ("casino","betting","sportsbook","cbd","payday"): notes.append(f"HARD FAIL: farm word {w}")
        elif w: notes.append(f"check: farm word {w}")
    if it.get("writeForUs"): notes.append("write for us")
    if it.get("httpStatus") and it["httpStatus"] >= 400: notes.append(f"http {it['httpStatus']}")
    row = {c: it.get(c, "") for c in cols}
    row.update(webDomain=d, loaded=True, redirectedToOtherDomain=redir and not same_brand, notes="; ".join(notes))
    out.append(row)
with open("step2/vetting.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
fails = [r for r in out if "HARD FAIL" in r["notes"]]
print(len(out), "rows;", sum(1 for r in out if r["loaded"] is True), "loaded;", len(fails), "hard fails")
for r in out:
    if r["notes"]: print(r["webDomain"], "|", r["notes"])
