"""Add emailSubjectB (hook-based subject, from step5/subjects/out_*.csv) and followUpBody (in-thread bump)
to 04_backlink_emails.csv and 04_backlink_emails_send.csv."""
import csv, glob, os, re

subj = {}
for f in sorted(glob.glob("step5/subjects/out_*.csv")):
    for r in csv.DictReader(open(f)):
        subj[r["webDomain"].strip()] = r["emailSubjectB"].strip()

OPENERS = ["Just bumping this in case it got buried.", "Popping this back to the top of your inbox."]
OFFER_LINE = {
    "Founder's quote swap": "I'm happy to write my quote first and send it over, so you can see if it fits the piece before you commit to anything.",
    "Video for the blog post": "If it helps, I can send a rough outline of the video first, so you can see how it would sit in the post before saying yes.",
    "Blog graphic or infographic": "If it helps, I can send a rough sketch of the graphic first, so you can see how it would look on the page before saying yes.",
    "Founder's quote": "I can write the quote first and send it over, so you can see if it fits before deciding.",
    "Internal data": "I can send the figures over first, so you can see if they fit the piece before deciding.",
}

def follow_up(r, i):
    if not r["emailBody"].strip():
        return ""
    greet = f"Hey {r['companyName']} team," if r.get("emailType") == "generic" or not r["firstName"].strip() else f"Hey {r['firstName'].split()[0]},"
    return (f"<p>{greet}</p><p>{OPENERS[i % 2]} {OFFER_LINE[r['offer']]}</p>"
            "<p>No worries if the timing's off.</p><p>Cheers,<br>Sam</p>")

for path in ["04_backlink_emails.csv", "04_backlink_emails_send.csv"]:
    rows = list(csv.DictReader(open(path)))
    cols = [c for c in rows[0].keys() if c not in ("emailSubjectB", "followUpBody")]
    cols.insert(cols.index("emailBody"), "emailSubjectB")
    cols.insert(cols.index("emailBody") + 1, "followUpBody")
    sent = 0
    for r in rows:
        r["emailSubjectB"] = subj.get(r["webDomain"], "") if r["emailBody"].strip() else ""
        r["followUpBody"] = follow_up(r, sent)
        sent += bool(r["emailBody"].strip())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    live = [r for r in rows if r["emailBody"].strip()]
    print(path, len(rows), "rows;", sum(1 for r in live if r["emailSubjectB"]), "with subject B;",
          sum(1 for r in live if r["followUpBody"]), "with follow-up")
    bad = [r["webDomain"] for r in live if re.search("[–—]", r["emailSubjectB"] + r["followUpBody"])]
    print("  dashes:", bad)
