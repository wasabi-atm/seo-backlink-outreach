"""03_backlink_targets.csv + step5/contacts_final.csv -> step5/in_0..5.csv (25 rows each) for the email agents."""
import csv, re
T = list(csv.DictReader(open("03_backlink_targets.csv")))
C = {r["webDomain"]: r for r in csv.DictReader(open("step5/contacts_final.csv"))}
FOUNDER = r"founder|\bceo\b|chief executive|owner|managing director|managing partner|president"
cols = ["companyName", "webDomain", "country", "segment", "offer", "competitorDecision", "firstName", "lastName",
        "jobTitle", "email", "emailType", "contactIsFounder", "articleTitle", "articleUrl", "articleDate",
        "linkPlacement", "articleHook", "fit", "notes"]
# Step 4 agents said these also do video or motion work; asked the user, emails use the competitor-safe wording meanwhile.
FLAGGED = {"neue.world": "flagged: does some motion work itself", "engageweb.co.uk": "flagged: sells video production itself"}
rows = []
for t in T:
    if t["webDomain"] in FLAGGED and not t.get("competitorDecision"):
        t["competitorDecision"] = FLAGGED[t["webDomain"]]
    c = C.get(t["webDomain"], {})
    title = c.get("jobTitle", "")
    tl = re.sub(r"vice president|\bvp\b", "", title.lower())
    founder = "yes" if re.search(FOUNDER, tl) and not re.search(r"apac|emea|international|regional", tl) else "no"
    rows.append({**{k: t.get(k, "") for k in cols}, **{k: c.get(k, "") for k in ("firstName", "lastName", "jobTitle", "email", "emailType")},
                 "contactIsFounder": founder if t["segment"] == "A" else ""})
for i in range(6):
    with open(f"step5/in_{i}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows[i * 25:(i + 1) * 25])
print(len(rows), "rows;", sum(1 for r in rows if r["email"]), "with email")
