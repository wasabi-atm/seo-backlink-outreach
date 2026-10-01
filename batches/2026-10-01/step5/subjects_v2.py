"""One subject per row from the user's five templates (1 Oct). No A/B test.
quick question about your {article_title} / noticed something in your {topic} article /
fresh data for your {article_title} piece / ASAP: need your response on your {article_title} piece!! / Quick intro, {name}?"""
import csv, re
ACR = {"ai","uk","uae","us","geo","sec","finra","cftc","pmp","b2b","seo","eaa","ux","cro","ichra","aml","soc","hr","pdp","pdps","q4","ccaas","x","tiktok","shopify","linkedin","youtube","instagram"}
def short_title(t):
    t = t.replace("’", "'").strip()
    for sep in (": ", " - ", " | ", " (", "? "):
        head = t.split(sep)[0]
        if len(head.split()) >= 3 and len(head) < len(t):
            t = head; break
    t = t.rstrip("?.!")
    words = t.split()
    while len(" ".join(words)) > 42 and len(words) > 4: words = words[:-1]
    t = " ".join(words).rstrip(",:;&")
    return t
def tidy_topic(s):
    w = s.strip().rstrip(".").split()
    if w and w[0].lower() not in ACR and not w[0][1:].isupper(): w[0] = w[0][0].lower() + w[0][1:]
    t = " ".join(w)
    while len(t) > 40 and len(t.split()) > 3: t = " ".join(t.split()[:-1]).rstrip(",:;&")
    return t
rows = list(csv.DictReader(open("04_backlink_emails.csv"))); cols = list(rows[0].keys())
for c in ("emailSubjectB", "subjectTypeB"):
    if c in cols: cols.remove(c)
cols[cols.index("subjectTypeA")] = "subjectTemplate"
n = 0
for r in rows:
    r.pop("emailSubjectB", None); r.pop("subjectTypeB", None); r.pop("subjectTypeA", None); r["subjectTemplate"] = ""
    if not r["emailBody"]: r["emailSubject"] = ""; continue
    title = short_title(r["articleTitle"]); topic = tidy_topic(r["articleTopic"])
    name = r["firstName"] if r["emailType"] != "generic" and r["firstName"] else f"{r['companyName']} team"
    if r["offer"] == "Internal data":
        k, s = "fresh_data", f"fresh data for your {title} piece"
    elif r["segment"] == "A":
        n += 1
        k, s = (("quick_intro", f"Quick intro, {name}?") if n % 2 else ("quick_question", f"quick question about your {title}"))
    elif r["offer"] == "Founder's quote":
        k, s = "quick_question", f"quick question about your {title}"
    else:
        k, s = "noticed_something", f"noticed something in your {topic} article"
    r["emailSubject"], r["subjectTemplate"] = s, k
w = csv.DictWriter(open("04_backlink_emails.csv", "w", newline=""), fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
send = [r for r in rows if r["emailBody"]]
sc = "email,firstName,lastName,companyName,webDomain,emailSubject,emailBody".split(",")
w = csv.DictWriter(open("04_backlink_emails_send.csv", "w", newline=""), fieldnames=sc, extrasaction="ignore"); w.writeheader(); w.writerows(send)
import collections; print(collections.Counter(r["subjectTemplate"] for r in send))
for r in send: print(len(r["emailSubject"]), "|", r["emailSubject"])
