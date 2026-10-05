"""Builds 04_backlink_emails.csv: merges emails_0..4 onto targets_final.csv, adds one subject per row from the user's templates (mixed), checks."""
import csv, random, collections, re
rows = list(csv.DictReader(open("step5/targets_final.csv")))
em = {}
for i in range(3):
    for r in csv.DictReader(open(f"step5/emails_{i}.csv")): em[r["webDomain"]] = r
for r in rows:
    e = em.get(r["webDomain"])
    r["videoSchemaGap"] = ""; r["subjectTemplate"] = ""; r["emailSubject"] = ""
    if e:
        r["emailBody"] = e["emailBody"]; r["articleShortName"] = e["articleShortName"]; r["manualCheck"] = e["manualCheck"]
    else:
        r["emailBody"] = ""; r["articleShortName"] = ""
        r["manualCheck"] = ("already in Instantly campaign: " + r["instantlyCampaign"] + " (dropped by user)") if r.get("instantlyCampaign") else "no contact found"
send = [r for r in rows if r["emailBody"]]
assert len(send) == len(em) == 51, (len(send), len(em))
random.Random(20261005).shuffle(send)
T = ["quick_question", "noticed_something", "quick_intro", "asap"]
for i, r in enumerate(send):
    k = T[i % 4]
    name = r["firstName"] if r["emailType"] != "generic" and r["firstName"] else f"{r['companyName']} team"
    s = r["articleShortName"].strip()
    subj = {"quick_question": f"quick question about your {s} piece",
            "noticed_something": f"noticed something in your {s} article",
            "quick_intro": f"Quick intro, {name}?",
            "asap": f"ASAP: need your response on your {s} piece!!"}[k]
    r["emailSubject"], r["subjectTemplate"] = subj, k
cols = "companyName,webDomain,domainRating,country,serviceType,segment,offer,firstName,lastName,jobTitle,email,emailSource,emailType,linkedinUrl,articleTitle,articleUrl,articleTopic,articleDate,articlePublished,publishedSource,linkPlacement,articleHook,videoSchemaGap,fit,competitor,competitorDecision,articleShortName,emailSubject,subjectTemplate,emailBody,manualCheck,instantlyCampaign".split(",")
w = csv.DictWriter(open("04_backlink_emails.csv", "w", newline=""), fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
print(len(rows), len(send), collections.Counter(r["subjectTemplate"] for r in send))
print("manualCheck rows:", sum(1 for r in send if r["manualCheck"]), "blank:", sum(1 for r in send if not r["manualCheck"]))
bad = [r["webDomain"] for r in rows if re.search("[–—]", " ".join(r.values()))]
print("dashes:", bad)
subs = [r["emailSubject"] for r in send]; print("dup subjects:", [s for s, c in collections.Counter(subs).items() if c > 1])
print("longest subject:", max(len(s) for s in subs))
