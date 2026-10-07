"""After contacts: merge contacts_0/1 into contacts.csv, run contacts.py merge, add campaign check, write in_0..5.csv for the email agents."""
import csv, subprocess, re, collections
B = "/home/user/seo-backlink-outreach/batches/2026-10-07"
S = "/home/user/seo-backlink-outreach/skill/mta-backlink-outreach/scripts"
rows, seen = [], set()
for i in range(2):
    for r in csv.DictReader(open(f"{B}/step5/contacts_{i}.csv")):
        if r["webDomain"] not in seen:
            seen.add(r["webDomain"]); rows.append(r)
cols = list(csv.DictReader(open(f"{B}/step5/contacts_0.csv")).fieldnames)
with open(f"{B}/step5/contacts.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
subprocess.run(["python3", f"{S}/contacts.py", "merge", f"{B}/03_backlink_targets.csv", f"{B}/step5/contacts.csv", "-o", f"{B}/step5/targets_contacts.csv"], check=True)
camp = {}
for i in range(2):
    for r in csv.DictReader(open(f"{B}/step5/campaign_check_{i}.csv")):
        camp[r["email"].strip().lower()] = r.get("instantlyCampaign", "")
t = list(csv.DictReader(open(f"{B}/step5/targets_contacts.csv")))
FOUNDER = re.compile(r"\b(founder|co-founder|cofounder|ceo|chief executive|owner|managing director|president)\b", re.I)
for r in t:
    r["instantlyCampaign"] = camp.get(r["email"].strip().lower(), "") if r["email"] else ""
    r["contactIsFounder"] = "yes" if FOUNDER.search(r.get("jobTitle", "")) else "no"
with open(f"{B}/step5/targets_contacts.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(t[0].keys())); w.writeheader(); w.writerows(t)
print(len(t), "rows;", sum(1 for r in t if r["email"]), "with email;", collections.Counter(r.get("emailSource", "") for r in t))
print("in other campaigns:", [(r["webDomain"], r["instantlyCampaign"]) for r in t if r["instantlyCampaign"]])
print("no email:", [r["webDomain"] for r in t if not r["email"]])
