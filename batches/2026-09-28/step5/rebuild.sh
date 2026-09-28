#!/bin/sh
# Rebuild 04_backlink_emails.csv, the send-only file and the variant columns from step5 sources. Run from the batch folder.
set -e
python3 step5/merge_step5.py > /dev/null
python3 - <<'PY'
import csv
rows=list(csv.DictReader(open('04_backlink_emails.csv')))
with open('04_backlink_emails_send.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); # Instantly reads {{...}} as merge tags, so no field in the upload file may contain double braces.
    w.writerows([{k: v.replace('{{', '{').replace('}}', '}') for k, v in r.items()} for r in rows if r['emailBody'].strip()])
PY
python3 step5/add_variants.py
