"""Builds 11_video_seo_07_contacts.csv: the 126 companies in 07 (video, no VideoObject Google can see)
with one contact each. The 69 from the main 100 keep their contacts (03_video_seo_contacts.csv, after
the SEO owner pass); the other 57 come from the waterfall in enrich07/ (Instantly, Apollo, Apify,
website), picked with contacts.py --focus seo.

    <repo>/.venv-crawl/bin/python build_07_contacts.py
"""
import csv, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "skill", "mta-backlink-outreach", "scripts"))
from contacts import clean_name, role_rank  # noqa: E402

LABEL = {0: "SEO lead", 1: "Website owner", 2: "Marketing lead", 3: "Content", 4: "SEO specialist", 5: "Growth",
         6: "Digital marketing", 7: "Founder or CEO", 8: "Other marketing", 9: "Marketing ops or events", 10: "Other"}
NOTES = {  # the 57 new contacts
    "icon.com": "Possible competitor (AI video ad maker), still waiting on the user's call. Founder picked by hand: Apify's other icon.com people work at Icon's client brands",
    "pathai.com": "Clinical provider support inbox from the website; no marketing person found anywhere",
    "athelas.com": "Support inbox from the website; no marketing person found anywhere",
    "skyvera.com": "Chief Revenue Officer as a last resort; no marketing person found anywhere",
    "bookcreator.com": "VP of Engineering as a last resort (Book Creator is now part of Kami); no marketing person found anywhere",
    "evolving.com": "Content & SEO Specialist based in India",
    "abacus.ai": "Influencer Marketing Manager based in India; no marketing lead found",
    "workboard.com": "Senior Marketing Manager based in Bulgaria",
    "cubesoftware.com": "CEO; Cube's SEO & CRO Manager (Rudy Hernandez) has no email in any source",
    "wand.ai": "Instantly lists her at gathid.com; Apollo verified hope.f@wand.ai",
    "ripplematch.com": "Email on RippleMatch's ripplematch.net domain",
    "certa.ai": "Email on Certa's getcerta.net domain",
    "oneday.com": "Email on Oneday's oneday.io domain",
    "abtrace.com": "Email on Abtrace's abtrace.co domain",
    "krotos.studio": "Email on Krotos's krotosaudio.com domain",
    "manufacture2030.com": "Manufacture 2030 now trades as Secaro",
}


def read(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


base = read("07_video_true_schema_false.csv")
old_notes = {r["webDomain"]: r.get("manualCheck", "") for r in read("03_video_seo_contacts.csv")}
new = {r["webDomain"]: r for r in read("enrich07/contacts.csv") if r.get("email")}
camp_file = "enrich07/instantly_campaign_check.csv"
camp = {r["email"].lower(): r["campaignNames"] for r in read(camp_file)
        if r.get("campaignCount") not in ("", "0", None)} if os.path.exists(camp_file) else {}

cols = list(base[0].keys()) + ["manualCheck"]
for r in base:
    d = r["webDomain"]
    if r.get("email"):
        r["manualCheck"] = old_notes.get(d, "")
        continue
    c = new.get(d, {})
    r.update(firstName=clean_name(c.get("firstName")), lastName=clean_name(c.get("lastName")), jobTitle=c.get("jobTitle", ""),
             email=c.get("email", ""), emailSource=c.get("emailSource", ""),
             contactRole="Company inbox" if c.get("emailType") == "generic" else LABEL[role_rank(c.get("jobTitle"), "seo")],
             instantlyCampaign=camp.get((c.get("email") or "").lower(), ""), manualCheck=NOTES.get(d, ""))
with open("11_video_seo_07_contacts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    w.writerows(base)

count = lambda key: {}.fromkeys(sorted({r[key] for r in base}), 0) | {v: sum(r[key] == v for r in base) for v in {r[key] for r in base}}
print(f"{len(base)} companies, {sum(bool(r['email']) for r in base)} with an email")
print("by source:", count("emailSource"))
print("by role:", count("contactRole"))
print("in an Instantly campaign:", [r["webDomain"] for r in base if r.get("instantlyCampaign")])
print("with a manualCheck note:", sum(bool(r["manualCheck"]) for r in base))
