"""Builds 04_backlink_emails.csv for backlink-2026-10-20: merges step5/emails_*.csv onto targets + contacts, gives each sendable row one subject
from the user's four templates (set on 7 Oct), mixed through the list."""
import csv, glob, random, collections, re, html
B = "/home/user/seo-backlink-outreach/batches/2026-10-20"
tg = {r["webDomain"]: {**r, "domainRating": r.get("drChecked",""), "offer": ("Founder's quote swap" if r["segment"]=="A" else r.get("offerSuggestion",""))} for r in csv.DictReader(open(f"{B}/work/step5_rows.csv"))}
ct = {r["webDomain"]: r for r in csv.DictReader(open(f"{B}/work/contacts_final.csv"))}
em = {}
for p in sorted(glob.glob(f"{B}/work/emails_e*.csv")):
    for r in csv.DictReader(open(p)):
        em[r["webDomain"].strip()] = r
cc = {r["email"].lower(): r["instantlyCampaign"] for r in csv.DictReader(open(f"{B}/work/campaign_check.csv"))}
rows = []
for d, c in ct.items():
    t = tg.get(d)
    if not t: continue
    e = em.get(d)
    r = {**t, **{k: c.get(k, "") for k in ["firstName", "lastName", "jobTitle", "email", "emailSource", "emailType", "linkedinUrl"]}}
    r["firstName"] = re.sub(r"\s+", " ", r["firstName"]).strip()
    r["instantlyCampaign"] = cc.get(r["email"].lower(), "")
    r["videoSchemaGap"] = ""; r["subjectTemplate"] = ""; r["emailSubject"] = ""; r["subjectType"] = ""
    if e:
        r["emailBody"] = e["emailBody"].strip(); r["articleShortName"] = e["articleShortName"].strip()
        mc = [x.strip() for x in e["manualCheck"].replace("campaign check pending", "").split(";") if x.strip()]
        if r["instantlyCampaign"]: mc.append("already in Instantly campaign: " + r["instantlyCampaign"])
        r["manualCheck"] = "; ".join(mc)
    else:
        r["emailBody"] = ""; r["articleShortName"] = ""; r["manualCheck"] = "no email written"
    rows.append(r)
send = [r for r in rows if r["emailBody"]]
random.Random(20261020).shuffle(send)
T = ["quick_question", "noticed_something", "quick_intro", "asap"]
used = set()
for i, r in enumerate(send):
    s = r["articleShortName"]
    first = r["firstName"].split(" ")[0] if r["emailType"] != "generic" and r["firstName"] else f"{r['companyName']} team"
    subj = {"quick_question": f"quick question about your {s} piece",
            "noticed_something": f"noticed something in your {s} article",
            "quick_intro": f"Quick intro, {first}?",
            "asap": f"ASAP: need your response on your {s} piece!!"}
    k = T[i % 4]
    if subj[k] in used: k = next(t for t in T if subj[t] not in used)
    r["emailSubject"], r["subjectTemplate"], r["subjectType"] = subj[k], k, k
    used.add(subj[k])
    # greeting: use first token of the first name
    r["emailBody"] = re.sub(r"^<p>Hey ([^,<]+),</p>", lambda m: f"<p>Hey {m.group(1).split(' ')[0]},</p>" if r["emailType"] != "generic" else m.group(0), r["emailBody"])
cols = ("companyName,webDomain,domainRating,country,serviceType,segment,offer,firstName,lastName,jobTitle,email,emailSource,emailType,"
        "linkedinUrl,articleTitle,articleUrl,articleTopic,articleDate,articlePublished,publishedSource,linkPlacement,articleHook,"
        "videoSchemaGap,fit,backlinkExchange,competitor,competitorDecision,articleShortName,emailSubject,subjectTemplate,subjectType,emailBody,"
        "manualCheck,instantlyCampaign,pool").split(",")
with open(f"{B}/04_backlink_emails.csv", "w", newline="") as f:
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
print("in other campaigns:", [(r["webDomain"], r["instantlyCampaign"]) for r in send if r["instantlyCampaign"]])
