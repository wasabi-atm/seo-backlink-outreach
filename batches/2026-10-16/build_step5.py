"""Merge article results + contacts + campaign check -> work/step5_rows.csv; chunk rows not yet written into work/in_e<N>.csv."""
import csv, json, glob, os, sys
B = "/home/user/seo-backlink-outreach/batches/2026-10-16"
DROP = {"swordandthescript.com"}
tg = {}
for p in sorted(glob.glob(f"{B}/work/results_*.jsonl")):
    for l in open(p):
        if l.strip():
            r = json.loads(l)
            if r.get("verdict") == "pass" and r["webDomain"].lower() not in DROP:
                tg.setdefault(r["webDomain"].lower(), r)
ct = {r["webDomain"].lower(): r for r in csv.DictReader(open(f"{B}/work/contacts.csv"))}
cc = {r["email"].lower(): r["instantlyCampaign"] for r in csv.DictReader(open(f"{B}/work/campaign_check.csv"))}
done = set()
for p in glob.glob(f"{B}/work/emails_e*.csv"):
    done |= {r["webDomain"] for r in csv.DictReader(open(p))}
cols = ["companyName","webDomain","country","segment","offer","firstName","lastName","jobTitle","email","emailSource","emailType","contactIsFounder",
        "articleTitle","articleUrl","articleDate","linkPlacement","offerLine","articleHook","notes","instantlyCampaign"]
rows, held = [], []
for d, c in ct.items():
    t = tg.get(d)
    if not t: continue
    r = {k: t.get(k, "") for k in cols}
    r["offer"] = t.get("offerSuggestion", "")
    for k in ["firstName","lastName","jobTitle","email","emailSource","emailType"]: r[k] = c.get(k, "")
    r["emailType"] = r["emailType"] or "person"
    jt = r["jobTitle"].lower()
    r["contactIsFounder"] = "yes" if any(w in jt for w in ["founder","ceo","chief executive","owner","managing director","president","principal"]) else "no"
    r["instantlyCampaign"] = cc.get(r["email"].lower(), "")
    (held if r["instantlyCampaign"] else rows).append(r)
for name, rs in [("step5_rows", rows), ("step5_held", held)]:
    w = csv.DictWriter(open(f"{B}/work/{name}.csv", "w", newline=""), fieldnames=cols); w.writeheader(); w.writerows(rs)
todo = [r for r in rows if r["webDomain"] not in done]
n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
for i in range(n):
    ch = todo[i::n]
    if not ch: continue
    w = csv.DictWriter(open(f"{B}/work/in_e{start+i}.csv", "w", newline=""), fieldnames=cols); w.writeheader(); w.writerows(ch)
    print(f"in_e{start+i}", len(ch))
print(len(rows), "sendable rows;", len(held), "held (in other campaigns);", len(todo), "to write")
