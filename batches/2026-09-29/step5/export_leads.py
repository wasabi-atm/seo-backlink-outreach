"""Instantly list_leads JSON pages -> leads_instantly.csv (contacts.py columns)."""
import csv, json, sys
out, pages = sys.argv[1], sys.argv[2:]
rows, seen = [], set()
for p in pages:
    for x in json.load(open(p))["items"]:
        pl = x.get("payload") or {}
        email = (x.get("email") or pl.get("email") or "").strip().lower()
        if not email or email in seen:
            continue
        seen.add(email)
        rows.append(dict(webDomain=pl.get("sourceCompanyDomain") or x.get("company_domain") or "",
                         firstName=x.get("first_name") or pl.get("firstName") or "",
                         lastName=x.get("last_name") or pl.get("lastName") or "",
                         jobTitle=x.get("job_title") or pl.get("jobTitle") or "",
                         email=email, location=pl.get("location") or "",
                         linkedinUrl=pl.get("linkedIn") or "", companyName=x.get("company_name") or "",
                         emailDomain=email.split("@")[-1], verification=x.get("verification_status")))
cols = ["webDomain", "firstName", "lastName", "jobTitle", "email", "location", "linkedinUrl", "companyName", "emailDomain", "verification"]
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(len(rows), "leads with email")
