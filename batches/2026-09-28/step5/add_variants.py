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

# Proper casing for the short article name ("topic") taken from emailSubject, which is all lower case.
CASE = {"ai": "AI", "ai,": "AI,", "api": "API", "b2b": "B2B", "cde": "CDE", "cdp": "CDP", "cism": "CISM", "clm": "CLM",
        "cx": "CX", "dam": "DAM", "dbs": "DBS", "geo": "GEO", "hr": "HR", "jtbd": "JTBD", "kyc": "KYC", "l&d": "L&D",
        "ppc": "PPC", "pr": "PR", "q1": "Q1", "rcs": "RCS", "rfq": "RFQ", "seo": "SEO", "trn": "TRN", "uae": "UAE",
        "us": "US", "uwtsd": "UWTSD", "v7": "V7", "goaml": "goAML", "airbnb": "Airbnb", "centrica": "Centrica",
        "dubai": "Dubai", "european": "European", "gitlab": "GitLab", "hassantuk": "Hassantuk", "instagram": "Instagram",
        "iris": "Iris", "january": "January", "mexico": "Mexico", "city": "City", "ras": "Ras", "al": "al",
        "khaimah": "Khaimah", "reuters": "Reuters", "september": "September", "whatsapp": "WhatsApp",
        "woocommerce": "WooCommerce", "youtube": "YouTube", "act": "Act", "accessibility": "Accessibility"}

# Hand-shortened topics where the generated one runs long on a phone or needs a proper name.
TOPIC_FIX = {"chilipiper.com": "demo button piece", "qureos.com": "hiring funnel guide", "helpag.com": "AI threat actor piece",
             "commitbiz.com": "UAE Pass guide", "engagehub.com": "RCS debt collection piece", "v7labs.com": "V7 Go skills post",
             "winnowsolutions.com": "impact report page", "9fin.com": "secondaries crash course", "cpx.net": "AI security post"}

def topic(r):
    if r["webDomain"] in TOPIC_FIX:
        return TOPIC_FIX[r["webDomain"]]
    words = re.sub(r"^(your|the)\s+", "", r["emailSubject"].strip()).split()
    out = [CASE.get(w, w) for w in words]
    t = " ".join(out)
    # "accessibility act" and "mexico city" only take capitals as names
    if "Accessibility" in t and "European" not in t:
        t = t.replace("Accessibility", "accessibility")
    if "City" in t and "Mexico" not in t:
        t = t.replace("City", "city")
    if "Act" in t.split() and "European" not in t:
        t = t.replace(" Act", " act")
    return t

def subject_c(r):
    """Template #6 (proven in March) for quote swaps, #4 (name plus curiosity) for the other offers."""
    if r["offer"] == "Founder's quote swap" or not r["firstName"].strip():
        return f"{r['companyName']} x Motion: a quote swap"
    return f"{r['firstName'].split()[0]}, spotted something in your {topic(r)}"

def follow_up(r, i):
    if not r["emailBody"].strip():
        return ""
    greet = f"Hey {r['companyName']} team," if r.get("emailType") == "generic" or not r["firstName"].strip() else f"Hey {r['firstName'].split()[0]},"
    return (f"<p>{greet}</p><p>{OPENERS[i % 2]} {OFFER_LINE[r['offer']]}</p>"
            "<p>No worries if the timing's off.</p><p>Cheers,<br>Sam</p>")

for path in ["04_backlink_emails.csv", "04_backlink_emails_send.csv"]:
    rows = list(csv.DictReader(open(path)))
    cols = [c for c in rows[0].keys() if c not in ("emailSubjectB", "emailSubjectC", "topic", "followUpBody")]
    cols.insert(cols.index("emailBody"), "emailSubjectB")
    cols.insert(cols.index("emailBody"), "emailSubjectC")
    cols.insert(cols.index("emailBody"), "topic")
    cols.insert(cols.index("emailBody") + 1, "followUpBody")
    sent = 0
    for r in rows:
        live = bool(r["emailBody"].strip())
        r["emailSubjectB"] = subj.get(r["webDomain"], "") if live else ""
        r["topic"] = topic(r) if live else ""
        r["emailSubjectC"] = subject_c(r) if live else ""
        r["followUpBody"] = follow_up(r, sent)
        sent += bool(r["emailBody"].strip())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    live = [r for r in rows if r["emailBody"].strip()]
    print(path, len(rows), "rows;", sum(1 for r in live if r["emailSubjectB"]), "with subject B;", sum(1 for r in live if r["emailSubjectC"]), "with subject C;",
          sum(1 for r in live if r["followUpBody"]), "with follow-up")
    bad = [r["webDomain"] for r in live if re.search("[–—]", r["emailSubjectB"] + r["emailSubjectC"] + r["topic"] + r["followUpBody"])]
    print("  dashes:", bad)
