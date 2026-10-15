"""Builds 04_backlink_emails.csv for backlink-2026-10-12: merges step5/emails_0..3 onto step5/targets_final.csv and gives each
sendable row one subject from the user's four templates (set on 7 Oct), mixed through the list."""
import csv, random, collections, re, html
B = "/home/user/seo-backlink-outreach/batches/2026-10-12"
rows = list(csv.DictReader(open(f"{B}/step5/targets_final.csv")))
em = {}
for i in range(4):
    for r in csv.DictReader(open(f"{B}/step5/emails_{i}.csv")):
        em[r["webDomain"].strip()] = r
cc={r["webDomain"]:r["instantlyCampaign"] for r in csv.DictReader(open(f"{B}/step5/campaign_check.csv"))}
for r in rows:
    r["instantlyCampaign"]=cc.get(r["webDomain"],"")
    e = em.get(r["webDomain"])
    r["videoSchemaGap"] = ""; r["subjectTemplate"] = ""; r["emailSubject"] = ""; r["subjectType"] = ""
    if e and r["email"]:
        r["emailBody"] = e["emailBody"].strip()
        r["articleShortName"] = e["articleShortName"].strip(); r["manualCheck"] = "; ".join(x for x in [p.strip() for p in e["manualCheck"].replace("campaign check pending","").split(";")] if x)
        if r["instantlyCampaign"]: r["manualCheck"] = (r["manualCheck"] + "; " if r["manualCheck"] else "") + "already in Instantly campaign: " + r["instantlyCampaign"]
    else:
        r["emailBody"] = ""; r["articleShortName"] = ""; r["manualCheck"] = "no email"
DROPPED = {"antavo.com","segmentstream.com","chattermill.com"}
for r in rows:
    if r["webDomain"] in DROPPED and r["emailBody"]:
        r["manualCheck"] = (r["manualCheck"] + "; " if r["manualCheck"] else "") + "DROPPED by the user (12 Oct): already in Instantly campaign " + r["instantlyCampaign"]
send = [r for r in rows if r["emailBody"] and r["webDomain"] not in DROPPED]
missing = [r["webDomain"] for r in rows if r["email"] and not r["emailBody"]]
assert not missing, missing
random.Random(20261012).shuffle(send)
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
        "manualCheck,instantlyCampaign,pool").split(",")
with open(f"{B}/04_backlink_emails.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
def words(b):
    t = re.sub(r"<p>\s*Cheers,.*$", "", b, flags=re.S | re.I)
    return len(html.unescape(re.sub(r"<[^>]+>", " ", t)).split())
print(len(rows), "rows,", len(send), "emails;", collections.Counter(r["subjectTemplate"] for r in send))
print("with manualCheck:", sum(1 for r in send if r["manualCheck"].strip()), "of", len(send))
print("over 110 words:", [(r["webDomain"], words(r["emailBody"])) for r in send if words(r["emailBody"]) > 110])
print("dashes:", [r["webDomain"] for r in rows if re.search("[–—]", " ".join(str(v) for v in r.values()))])
print("braces:", [r["webDomain"] for r in send if "{{" in r["emailBody"] or "{{" in r["emailSubject"]])
print("bad sign-off:", [r["webDomain"] for r in send if not r["emailBody"].rstrip().endswith("Sam</p>")])
print("no ask:", [r["webDomain"] for r in send if "open to exploring this?" not in r["emailBody"]])
print("no article link:", [r["webDomain"] for r in send if r["articleUrl"] not in r["emailBody"]])
print("no placement offer:", [r["webDomain"] for r in send if "pay for placement" not in r["emailBody"]])
print("dup subjects:", [s for s, c in collections.Counter(r["emailSubject"] for r in send).items() if c > 1])
print("offers:", collections.Counter(r["offer"] for r in send))
