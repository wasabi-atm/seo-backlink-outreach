"""Merge step5/emails_*.csv into 04_backlink_emails.csv and validate every email.
Checks: one row per company in 03, no em/en dashes, body under 110 words (HTML and sign-off stripped),
greeting, article link, motiontheagency.com link, closing line, sign-off, no call or meeting ask.
Writes step5/04_for_dedupe.csv (rows with an email) for the batch-wide dedupe check."""
import csv, glob, html, re
from collections import Counter

targets = {r["webDomain"]: r for r in csv.DictReader(open("03_backlink_targets.csv"))}
rows = {}
for f in sorted(glob.glob("step5/emails_*.csv")):
    for r in csv.DictReader(open(f)):
        rows[r["webDomain"].strip()] = r

cols = ["companyName", "webDomain", "country", "segment", "offer", "firstName", "lastName", "jobTitle", "email",
        "articleTitle", "articleUrl", "linkPlacement", "articleHook", "emailSubject", "emailBody", "manualCheck",
        "emailStatus", "contactNote"]

def words(body):
    t = re.sub(r"<p>\s*Cheers,<br>\s*Sam\s*</p>", " ", body)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return len(t.split())

problems = []
out = []
for d, t in targets.items():
    r = rows.get(d)
    if not r:
        problems.append((d, "missing from agent outputs"))
        continue
    row = {k: (r.get(k) or "").strip() for k in cols}
    body = row["emailBody"]
    if row["email"] and body:
        n = words(body)
        checks = {
            "dash": not re.search("[–—]", "".join(row.values())),
            "under 110 words": n < 110,
            "greeting": body.startswith("<p>Hey ") or body.startswith("<p>Hi "),
            "article link": (t["articleUrl"] in body) if t["articleUrl"] else True,
            "mta link": "motiontheagency.com" in body,
            "closing": "Would you be open to exploring this?" in body,
            "sign-off": body.rstrip().endswith("<p>Cheers,<br>Sam</p>"),
            "no call ask": not re.search(r"\b(call|meeting|zoom|calendar|chat next week)\b", html.unescape(re.sub(r"<[^>]+>", " ", body)), re.I),
            "subject lower": row["emailSubject"] == row["emailSubject"].lower(),
        }
        bad = [k for k, ok in checks.items() if not ok]
        if bad:
            problems.append((d, ", ".join(bad) + f" ({n} words)"))
    out.append(row)

with open("04_backlink_emails.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(out)
with open("step5/04_for_dedupe.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["companyName", "webDomain", "email"])
    w.writeheader()
    for r in out:
        if r["email"] and r["emailBody"]:
            w.writerow({k: r[k] for k in ("companyName", "webDomain", "email")})

print("rows", len(out), "with email + body", sum(1 for r in out if r["email"] and r["emailBody"]))
print("no email:", [r["webDomain"] for r in out if not r["email"]])
print("manualCheck:", sum(1 for r in out if r["manualCheck"]))
print("offers:", Counter(r["offer"] for r in out if r["emailBody"]))
print("problems:", problems)
dup_emails = [e for e, c in Counter(r["email"].lower() for r in out if r["email"]).items() if c > 1]
print("duplicate emails inside batch:", dup_emails)
