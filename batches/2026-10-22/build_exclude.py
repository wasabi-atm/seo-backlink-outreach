"""Build exclude_domains.txt: every root domain already contacted, researched, pooled or a client."""
import csv, glob, os, sys
REPO = "/home/user/seo-backlink-outreach"
sys.path.insert(0, f"{REPO}/skill/mta-backlink-outreach/scripts")
from dedupe import root_domain

doms = set()
def add(v):
    r = root_domain(v or "")
    if r and "." in r:
        doms.add(r)

def scan(path, cols):
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            for c in cols:
                if c in row:
                    add(row[c])

scan(f"{REPO}/outreach_ledger.csv", ["webDomain", "rootDomain", "emailDomain", "articleUrl"])
scan(f"{REPO}/low_dr_pool.csv", ["webDomain", "rootDomain"])
scan(f"{REPO}/form-outreach/form_outreach_master.csv", ["webDomain"])
scan(f"{REPO}/client_collab_opportunities.csv", ["Domain"])
scan(f"{REPO}/output/Motion_Clients_DR_Location.csv", ["Domain"])
for p in glob.glob(f"{REPO}/batches/*/**/*.csv", recursive=True) + glob.glob(f"{REPO}/form-outreach/batches/**/*.csv", recursive=True):
    if False:
        continue
    try:
        scan(p, ["webDomain", "domain", "rootDomain"])
    except Exception as e:
        print("skip", p, e)
for p in glob.glob(f"{REPO}/batches/*/exclude_domains.txt"):
    if "/2026-10-22/" not in p:
        for line in open(p):
            add(line.strip())
import json
for p in glob.glob(f"{REPO}/batches/2026-10-*/work/results_*.jsonl"):
    for l in open(p):
        if l.strip():
            try: add(json.loads(l).get("webDomain"))
            except Exception: pass
scan(f"{REPO}/batches/2026-10-21/work/prev/04_backlink_emails.csv", ["webDomain"]) if os.path.exists(f"{REPO}/batches/2026-10-21/work/prev/04_backlink_emails.csv") else None
with open("exclude_domains.txt", "w") as f:
    f.write("\n".join(sorted(doms)) + "\n")
print(len(doms), "domains")
