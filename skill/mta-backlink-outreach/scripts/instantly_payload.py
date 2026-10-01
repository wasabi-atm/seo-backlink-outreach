#!/usr/bin/env python3
"""Turn 04_backlink_emails.csv into lead batches for the Instantly MCP tool add_leads_to_campaign_or_list_bulk.

    python instantly_payload.py 04_backlink_emails.csv <outdir> [--chunk 40]

Writes <outdir>/leads_1.json, leads_2.json, ... (a JSON array each, ready to pass as `leads`) and prints the counts.
Rows with no email or no emailBody are skipped and listed. Nothing is sent; the campaign stays a draft.
"""
import csv
import json
import os
import sys

CUSTOM = ["emailSubject", "emailBody", "webDomain", "articleUrl", "articleTitle", "jobTitle", "country", "segment",
          "offer", "subjectType", "videoSchemaGap", "manualCheck"]


def lead(r):
    cv = {k: r[k].strip() for k in CUSTOM if (r.get(k) or "").strip()}
    out = {"email": r["email"].strip(), "custom_variables": cv}
    for src, dst in (("firstName", "first_name"), ("lastName", "last_name"), ("companyName", "company_name")):
        if (r.get(src) or "").strip():
            out[dst] = r[src].strip()
    if (r.get("webDomain") or "").strip():
        out["website"] = r["webDomain"].strip()
    return out


def main(path, outdir, chunk=40):
    rows = list(csv.DictReader(open(path, newline="")))
    ok, skipped, seen = [], [], set()
    for r in rows:
        e = (r.get("email") or "").strip().lower()
        if not e or not (r.get("emailBody") or "").strip() or not (r.get("emailSubject") or "").strip():
            skipped.append(r.get("webDomain", "?"))
        elif e in seen:
            skipped.append(f"{r.get('webDomain', '?')} (duplicate email)")
        else:
            seen.add(e)
            ok.append(lead(r))
    os.makedirs(outdir, exist_ok=True)
    for i in range(0, len(ok), chunk):
        json.dump(ok[i:i + chunk], open(os.path.join(outdir, f"leads_{i // chunk + 1}.json"), "w"), ensure_ascii=False)
    print(f"{len(ok)} leads in {-(-len(ok) // chunk)} files; skipped {len(skipped)}: {skipped}")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if x != "--chunk"]
    chunk = 40
    if "--chunk" in sys.argv:
        chunk = int(sys.argv[sys.argv.index("--chunk") + 1])
        a.remove(str(chunk))
    if len(a) != 2:
        sys.exit(__doc__)
    main(a[0], a[1], chunk)
