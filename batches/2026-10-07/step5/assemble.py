"""Builds 04_backlink_emails.csv for backlink-2026-10-07: merges emails_0..5 onto targets_final.csv and gives each sendable
row one subject from the user's four templates, mixed through the list (no 'fresh data' line: no Internal data rows)."""
import csv, random, collections, re, html
B = "/home/user/seo-backlink-outreach/batches/2026-10-07"
rows = list(csv.DictReader(open(f"{B}/step5/targets_final.csv")))
em = {}
for i in range(6):
    for r in csv.DictReader(open(f"{B}/step5/emails_{i}.csv")):
        em[r["webDomain"].strip()] = r
for r in rows:
    e = em.get(r["webDomain"])
    r["videoSchemaGap"] = ""; r["subjectTemplate"] = ""; r["emailSubject"] = ""
    if e and r["email"]:
        r["emailBody"] = e["emailBody"].strip(); r["articleShortName"] = e["articleShortName"].strip(); r["manualCheck"] = e["manualCheck"].strip()
    else:
        r["emailBody"] = ""; r["articleShortName"] = ""; r["manualCheck"] = r.get("dropReason", "") or "no email"
send = [r for r in rows if r["emailBody"]]
missing = [r["webDomain"] for r in rows if r["email"] and not r["emailBody"]]
assert not missing, missing
random.Random(20261007).shuffle(send)
T = ["quick_question", "noticed_something", "quick_intro", "asap"]
used = set()
for i, r in enumerate(send):
    s = r["articleShortName"]
    name = r["firstName"] if r["emailType"] != "generic" and r["firstName"] else f"{r['companyName']} team"
    subj = {"quick_question": f"quick question about your {s} piece",
            "noticed_something": f"noticed something in your {s} article",
            "quick_intro": f"Quick intro, {name}?",
            "asap": f"ASAP: need your response on your {s} piece!!"}
    k = T[i % 4]
    if subj[k] in used:
        k = next(t for t in T if subj[t] not in used)
    r["emailSubject"], r["subjectTemplate"], r["subjectType"] = subj[k], k, k
    used.add(subj[k])
cols = ("companyName,webDomain,domainRating,country,serviceType,segment,offer,firstName,lastName,jobTitle,email,emailSource,emailType,"
        "linkedinUrl,articleTitle,articleUrl,articleTopic,articleDate,articlePublished,publishedSource,linkPlacement,articleHook,"
        "videoSchemaGap,fit,backlinkExchange,competitor,competitorDecision,articleShortName,emailSubject,subjectTemplate,subjectType,emailBody,"
        "manualCheck,instantlyCampaign,droppedEmail,pool").split(",")
with open(f"{B}/04_backlink_emails.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
def words(b):
    t = re.sub(r"<p>\s*Cheers,.*$", "", b, flags=re.S | re.I)
    return len(html.unescape(re.sub(r"<[^>]+>", " ", t)).split())
print(len(rows), "rows,", len(send), "emails;", collections.Counter(r["subjectTemplate"] for r in send))
print("manualCheck on", sum(1 for r in send if r["manualCheck"]), "of", len(send))
print("over 110 words:", [(r["webDomain"], words(r["emailBody"])) for r in send if words(r["emailBody"]) > 110])
print("dashes:", [r["webDomain"] for r in rows if re.search("[–—]", " ".join(str(v) for v in r.values()))])
print("braces:", [r["webDomain"] for r in send if "{{" in r["emailBody"] or "{{" in r["emailSubject"]])
print("bad sign-off:", [r["webDomain"] for r in send if not r["emailBody"].rstrip().endswith("Sam</p>")])
print("no ask:", [r["webDomain"] for r in send if "open to exploring this?" not in r["emailBody"]])
print("no article link:", [r["webDomain"] for r in send if r["articleUrl"] not in r["emailBody"]])
print("dup subjects:", [s for s, c in collections.Counter(r["emailSubject"] for r in send).items() if c > 1])
print("longest subject:", max(len(r["emailSubject"]) for r in send))
