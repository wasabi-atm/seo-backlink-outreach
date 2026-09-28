"""03_backlink_targets.csv + step5/contacts_final.csv + step5/emails_*.csv + campaign checks -> 04_backlink_emails.csv."""
import csv, glob, re
from collections import Counter

T = list(csv.DictReader(open("03_backlink_targets.csv")))
C = {r["webDomain"]: r for r in csv.DictReader(open("step5/contacts_final.csv"))}
E = {}
for f in sorted(glob.glob("step5/emails_*.csv")):
    for r in csv.DictReader(open(f)):
        E[r["webDomain"].strip()] = r
camp = {}
for f in sorted(glob.glob("step5/campaign_check_*.csv")):
    for r in csv.DictReader(open(f)):
        if r["instantlyCampaign"].strip():
            camp[r["email"].strip().lower()] = r["instantlyCampaign"].strip()

# Contact notes a human should see before sending (webDomain -> note).
CONTACT_NOTES = {
    "majestic.com": "email is the Apify actor's pattern guess, not verified",
    "litmus.com": "email is the Apify actor's pattern guess, not verified",
    "podcast.co": "contact is the CTO, no founder or marketing email found",
    "codeweavers.net": "contact is Head of Retail and Partnerships, no marketing email found",
    "pearllemon.com": "contact name looks like a pen name (Joseph Expert), email on pearllemongroup.com",
    "mhrglobal.com": "email on midlandhr.co.uk, MHR's old domain",
    "grcsolutions.io": "email on grci.group, the parent GRC International Group",
    "summize.com": "contact is a junior content executive",
}
SAME = {"hackajob.co": "hackajob.com"}

cols = ["companyName", "webDomain", "country", "segment", "offer", "firstName", "lastName", "jobTitle", "email",
        "emailSource", "emailType", "linkedinUrl", "articleTitle", "articleUrl", "articleDate", "linkPlacement",
        "articleHook", "videoSchemaGap", "fit", "emailSubject", "emailSubjectB", "subjectTypeA", "subjectTypeB", "emailBody", "manualCheck", "instantlyCampaign"]
out = []
for t in T:
    d = t["webDomain"]
    c, e = C.get(d, {}), E.get(d, {})
    email = (c.get("email") or "").lower()
    notes = [x.strip() for x in (e.get("manualCheck") or "").split(";") if x.strip()]
    if d in CONTACT_NOTES:
        notes.append(CONTACT_NOTES[d])
    if c.get("emailType") == "generic":
        notes.append("shared inbox from the website")
    edom = email.split("@")[-1] if email else ""
    if edom and edom != d and not edom.endswith("." + d) and SAME.get(edom) != d and d not in CONTACT_NOTES:
        notes.append(f"email domain differs: {edom}")
    if email in camp:
        notes.append(f"already in Instantly campaign: {camp[email]} (waiting on the user)")
    row = {**{k: t.get(k, "") for k in cols}, **{k: c.get(k, "") for k in ("firstName", "lastName", "jobTitle", "email", "emailSource", "emailType", "linkedinUrl")},
           **{k: e.get(k, "") for k in ("emailSubject", "emailSubjectB", "subjectTypeA", "subjectTypeB")}, "emailBody": e.get("emailBody", ""),
           "manualCheck": "; ".join(dict.fromkeys(notes)), "instantlyCampaign": camp.get(email, "")}
    out.append(row)

with open("04_backlink_emails.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)

def words(body):
    b = re.sub(r"<p>Cheers,<br>Sam</p>", "", body)
    return len(re.sub(r"<[^>]+>", " ", b).split())
print(len(out), "rows;", sum(1 for r in out if r["emailBody"]), "with a body;", sum(1 for r in out if r["manualCheck"]), "with manualCheck")
print("missing email body but have email:", [r["webDomain"] for r in out if r["email"] and not r["emailBody"]])
print("over 110 words:", [(r["webDomain"], words(r["emailBody"])) for r in out if r["emailBody"] and words(r["emailBody"]) >= 110])
print("dashes:", [r["webDomain"] for r in out if re.search("[–—]", "".join(r.values()))])
print("no sign-off:", [r["webDomain"] for r in out if r["emailBody"] and "<p>Cheers,<br>Sam</p>" not in r["emailBody"]])
print("no closing question:", [r["webDomain"] for r in out if r["emailBody"] and "Would you be open to exploring this?" not in r["emailBody"]])
print("no paid placement:", [r["webDomain"] for r in out if r["emailBody"] and "placement" not in r["emailBody"]])
print("no MTA link:", [r["webDomain"] for r in out if r["emailBody"] and "motiontheagency.com" not in r["emailBody"]])
print("no article link:", [r["webDomain"] for r in out if r["emailBody"] and r["articleUrl"] not in r["emailBody"]])
print("call or meeting:", [r["webDomain"] for r in out if re.search(r"\b(call|meeting|chat)\b", r["emailBody"], re.I)])
print("US spelling:", [r["webDomain"] for r in out if re.search(r"\b(optimiz|visualiz|organiz|color\b|favorite|analyz)", r["emailBody"], re.I)])
print("campaign rows:", sum(1 for r in out if r["instantlyCampaign"]))

import subprocess, sys
subprocess.run([sys.executable, "../../skill/mta-backlink-outreach/scripts/subject_check.py", "04_backlink_emails.csv"])
