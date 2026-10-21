import csv, glob, sys, json
REPO="/home/claude/seo-backlink-outreach"
sys.path.insert(0, f"{REPO}/skill/mta-backlink-outreach/scripts")
from dedupe import root_domain
doms=set()
def add(v):
    r=root_domain(v or "")
    if r and "." in r: doms.add(r)
def scan(p, cols):
    try:
        with open(p, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                for c in cols:
                    if c in row: add(row[c])
    except Exception as e: print("skip",p,e)
scan(f"{REPO}/outreach_ledger.csv",["webDomain","rootDomain","emailDomain","articleUrl"])
scan(f"{REPO}/low_dr_pool.csv",["webDomain","rootDomain"])
scan(f"{REPO}/form-outreach/form_outreach_master.csv",["webDomain"])
scan(f"{REPO}/client_collab_opportunities.csv",["Domain"])
for p in glob.glob(f"{REPO}/output/**/*.csv",recursive=True): scan(p,["Domain","domain","webDomain"])
for p in glob.glob(f"{REPO}/batches/**/*.csv",recursive=True)+glob.glob(f"{REPO}/form-outreach/batches/**/*.csv",recursive=True):
    if "/2026-10-21/" in p: continue
    scan(p,["webDomain","domain","rootDomain","liveDomain"])
for p in glob.glob(f"{REPO}/batches/**/exclude_domains.txt",recursive=True)+glob.glob(f"{REPO}/form-outreach/batches/**/exclude_domains.txt",recursive=True):
    if "/2026-10-21/" in p: continue
    for l in open(p): add(l.strip())
for p in glob.glob(f"{REPO}/form-outreach/batches/*/work/results_*.jsonl")+glob.glob(f"{REPO}/batches/*/work/*.jsonl"):
    for l in open(p):
        try:
            j=json.loads(l); add(j.get("webDomain")); add(j.get("liveDomain"))
        except Exception: pass
open(f"{REPO}/form-outreach/batches/2026-10-21/work/exclude_domains.txt","w").write("\n".join(sorted(doms))+"\n")
print(len(doms))
