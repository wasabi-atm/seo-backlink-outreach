"""Local dedupe ledger for backlink outreach. One company is only ever emailed once.

    python dedupe.py check  candidates.csv --ledger LEDGER [--out-dir DIR]
    python dedupe.py log    emails.csv     --ledger LEDGER --status queued|sent|not_sent|excluded --campaign NAME [--date YYYY-MM-DD]
    python dedupe.py status LEDGER
    python dedupe.py set-status --ledger LEDGER --campaign NAME --status sent|not_sent [--domains a.com,b.com]
    python dedupe.py remove     --ledger LEDGER --campaign NAME   (test runs only)
    python dedupe.py pool       02_low_dr.csv --pool POOL --batch NAME [--date YYYY-MM-DD]

check  Compares every row against the ledger and against earlier rows in the same
       file. Writes <name>_clean.csv (safe to use) and <name>_duplicates.csv (removed,
       with the reason). Exit code 2 when anything was removed.
log    Appends rows to the ledger. Rows with no email are logged as not_sent.

Match keys (any hit removes the row):
  domain   root domain of webDomain, the email address and articleUrl
           (blog.digitalnexa.com -> digitalnexa.com, hallam.co.uk stays hallam.co.uk)
  email    exact email address
  name     company name without punctuation, "the", Ltd, Inc and similar
  brand    domain label with hq/app/get/try trimmed (chaserhq.com and chaser.io both
           give "chaser"). A brand-only hit is flagged "possible", still removed,
           and the user decides at the checkpoint.
Ledger rows with status not_sent never block. Every other status does, including
excluded (a competitor the user turned down).
"""
import argparse, csv, datetime, os, re, sys
from urllib.parse import urlparse

LEDGER_FIELDS = ["companyName", "webDomain", "rootDomain", "email", "emailDomain", "firstName", "lastName",
                 "articleUrl", "segment", "offer", "status", "sentDate", "campaign"]
MULTI_TLDS = {"co.uk", "org.uk", "ac.uk", "gov.uk", "me.uk", "ltd.uk", "plc.uk", "co.ae", "com.au", "net.au",
              "org.au", "co.nz", "com.sg", "co.in", "com.br", "co.za", "com.mx", "co.jp", "com.tr"}
NAME_STOP = {"the", "ltd", "limited", "inc", "llc", "llp", "plc", "gmbh", "co", "corp", "company", "group",
             "agency", "fz", "fze", "fzco", "fzllc", "dmcc"}
BRAND_TRIM = [r"^(get|try|use|go|join)(?=.{3,})", r"(hq|app|io|ai)$"]
BLOCKING = lambda status: (status or "").strip().lower() != "not_sent"


def root_domain(value):
    v = (value or "").strip().lower()
    if not v:
        return ""
    if "@" in v and "/" not in v:
        v = v.split("@", 1)[1]
    host = urlparse(v if "://" in v else "http://" + v).hostname or ""
    parts = [p for p in host.split(".") if p]
    if len(parts) < 2:
        return ""
    n = 3 if ".".join(parts[-2:]) in MULTI_TLDS and len(parts) >= 3 else 2
    return ".".join(parts[-n:])


def brand(root):
    label = root.split(".")[0] if root else ""
    for pat in BRAND_TRIM:
        trimmed = re.sub(pat, "", label)
        if len(trimmed) >= 3:
            label = trimmed
    return label if len(label) >= 3 else ""


def norm_name(name):
    words = re.sub(r"[^a-z0-9 ]", " ", (name or "").lower().replace("&", " and ")).split()
    return "".join(w for w in words if w not in NAME_STOP)


def keys(row):
    """Returns {(kind, value): label} for one row."""
    k = {}
    for col in ("webDomain", "email", "articleUrl", "rootDomain", "emailDomain"):
        r = root_domain(row.get(col, ""))
        if r:
            k[("domain", r)] = f"domain {r}"
            b = brand(r)
            if b:
                k[("brand", b)] = f"brand '{b}'"
    email = (row.get("email") or "").strip().lower()
    if "@" in email:
        k[("email", email)] = f"email {email}"
    n = norm_name(row.get("companyName"))
    if len(n) >= 3:
        k[("name", n)] = f"name '{row.get('companyName', '').strip()}'"
        k[("brand", n)] = f"brand '{n}'"
    return k


def read_csv(path):
    if not os.path.exists(path):
        return [], []
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        return list(r), r.fieldnames or []


def build_index(ledger_rows):
    idx = {}
    for row in ledger_rows:
        if not BLOCKING(row.get("status")):
            continue
        for kv in keys(row):
            idx.setdefault(kv, row)
    return idx


def cmd_check(a):
    ledger, _ = read_csv(a.ledger)
    if not ledger and not a.allow_empty_ledger:
        sys.exit(f"Ledger not found or empty: {a.ledger}. Refusing to run without it (pass --allow-empty-ledger for a first run).")
    idx = build_index(ledger)
    rows, fields = read_csv(a.csv_path)
    clean, dupes, seen = [], [], {}
    for i, row in enumerate(rows, start=2):
        rk = keys(row)
        hit_ledger = [(kv, lbl) for kv, lbl in rk.items() if kv in idx]
        hit_batch = [(kv, lbl) for kv, lbl in rk.items() if kv in seen]
        if hit_ledger or hit_batch:
            strong = [h for h in hit_ledger + hit_batch if h[0][0] != "brand"]
            reasons = []
            for kv, lbl in hit_ledger:
                m = idx[kv]
                reasons.append(f"{lbl} matches {m.get('companyName')} ({m.get('status')} {m.get('sentDate')}, {m.get('campaign')})")
            for kv, lbl in hit_batch:
                reasons.append(f"{lbl} repeats row {seen[kv]} of this file")
            dupes.append({**row, "dedupeMatch": "exact" if strong else "possible", "dedupeReason": "; ".join(reasons)})
        else:
            clean.append(row)
        for kv in rk:
            seen.setdefault(kv, i)
    out_dir = a.out_dir or os.path.dirname(os.path.abspath(a.csv_path))
    base = os.path.splitext(os.path.basename(a.csv_path))[0]
    clean_path, dupe_path = os.path.join(out_dir, base + "_clean.csv"), os.path.join(out_dir, base + "_duplicates.csv")
    with open(clean_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(clean)
    with open(dupe_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields + ["dedupeMatch", "dedupeReason"]); w.writeheader(); w.writerows(dupes)
    print(f"Ledger: {len(ledger)} rows. Checked {len(rows)}: {len(clean)} clean, {len(dupes)} removed.")
    for d in dupes:
        print(f"  [{d['dedupeMatch']}] {d.get('companyName') or d.get('webDomain')}: {d['dedupeReason']}")
    print(f"Clean: {clean_path}\nRemoved: {dupe_path}")
    return 2 if dupes else 0


def cmd_log(a):
    ledger, _ = read_csv(a.ledger)
    idx = build_index(ledger)
    seen = {kv: r for r in ledger for kv in keys(r)}
    rows, _ = read_csv(a.csv_path)
    date = a.date or datetime.date.today().isoformat()
    new, skipped = [], []
    for row in rows:
        email = (row.get("email") or "").strip().lower()
        status = a.status if ("@" in email or a.status == "excluded") else "not_sent"
        rec = {
            "companyName": (row.get("companyName") or "").strip(),
            "webDomain": (row.get("webDomain") or "").strip().lower(),
            "rootDomain": root_domain(row.get("webDomain")),
            "email": email, "emailDomain": root_domain(email),
            "firstName": row.get("firstName", ""), "lastName": row.get("lastName", ""),
            "articleUrl": row.get("articleUrl", ""), "segment": row.get("segment", ""), "offer": row.get("offer", ""),
            "status": status, "sentDate": date, "campaign": a.campaign,
        }
        rk = [kv for kv in keys(rec) if kv[0] != "brand"]
        # Skip if already contacted, or if this is a repeat not_sent entry. A not_sent
        # company that is now being emailed does get a new blocking row.
        if any(kv in idx for kv in rk) or (not BLOCKING(status) and any(kv in seen for kv in rk)):
            skipped.append(rec["companyName"])
            continue
        new.append(rec)
        for kv in keys(rec):
            (idx if BLOCKING(status) else seen).setdefault(kv, rec)
    exists = os.path.exists(a.ledger) and os.path.getsize(a.ledger) > 0
    os.makedirs(os.path.dirname(os.path.abspath(a.ledger)), exist_ok=True)
    with open(a.ledger, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_FIELDS)
        if not exists:
            w.writeheader()
        w.writerows(new)
    print(f"Logged {len(new)} rows to {a.ledger} ({sum(r['status'] == 'not_sent' for r in new)} as not_sent).")
    if skipped:
        print("Already in the ledger, not logged again: " + ", ".join(skipped))
    return 0


def cmd_set_status(a):
    ledger, fields = read_csv(a.ledger)
    wanted = {root_domain(d) for d in (a.domains or "").split(",") if d.strip()}
    n = 0
    for r in ledger:
        if r.get("campaign") == a.campaign and (not wanted or r.get("rootDomain") in wanted):
            if r.get("status") != "not_sent" or a.status == "not_sent":  # rows with no email stay not_sent
                r["status"], n = a.status, n + 1
    with open(a.ledger, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields or LEDGER_FIELDS); w.writeheader(); w.writerows(ledger)
    print(f"Set {n} rows in {a.campaign} to {a.status}.")
    return 0


def cmd_remove(a):
    """Deletes every ledger row of one campaign. Only for test runs the user wants forgotten."""
    ledger, fields = read_csv(a.ledger)
    keep = [r for r in ledger if r.get("campaign") != a.campaign]
    with open(a.ledger, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields or LEDGER_FIELDS); w.writeheader(); w.writerows(keep)
    print(f"Removed {len(ledger) - len(keep)} rows of {a.campaign} from {a.ledger}.")
    return 0


def cmd_pool(a):
    """Merges low-DR rows into the shared pool, one row per root domain, newest check wins."""
    pool, pfields = read_csv(a.pool)
    rows, rfields = read_csv(a.csv_path)
    date = a.date or datetime.date.today().isoformat()
    fields = list(dict.fromkeys(pfields + rfields + ["rootDomain", "batch", "checkedDate"]))
    by_root = {r.get("rootDomain") or root_domain(r.get("webDomain")): r for r in pool}
    added = updated = 0
    for r in rows:
        root = root_domain(r.get("webDomain"))
        if not root:
            continue
        updated += root in by_root
        added += root not in by_root
        by_root[root] = {**r, "rootDomain": root, "batch": a.batch, "checkedDate": date}
    with open(a.pool, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(by_root.values())
    print(f"Pool {a.pool}: {added} added, {updated} updated, {len(by_root)} total.")
    return 0


def cmd_status(a):
    ledger, _ = read_csv(a.ledger)
    by = {}
    for r in ledger:
        by.setdefault((r.get("campaign"), r.get("sentDate")), {}).setdefault(r.get("status"), 0)
        by[(r.get("campaign"), r.get("sentDate"))][r.get("status")] += 1
    print(f"{a.ledger}: {len(ledger)} rows")
    for (camp, date), counts in sorted(by.items(), key=lambda x: x[0][1] or ""):
        print(f"  {date}  {camp}: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("csv_path"); c.add_argument("--ledger", required=True)
    c.add_argument("--out-dir"); c.add_argument("--allow-empty-ledger", action="store_true")
    l = sub.add_parser("log"); l.add_argument("csv_path"); l.add_argument("--ledger", required=True)
    l.add_argument("--status", required=True, choices=["queued", "sent", "not_sent", "excluded"])
    l.add_argument("--campaign", required=True); l.add_argument("--date")
    s = sub.add_parser("status"); s.add_argument("ledger")
    ss = sub.add_parser("set-status"); ss.add_argument("--ledger", required=True); ss.add_argument("--campaign", required=True)
    ss.add_argument("--status", required=True, choices=["queued", "sent", "not_sent", "excluded"])
    ss.add_argument("--domains", help="comma-separated; default is every row in the campaign")
    po = sub.add_parser("pool"); po.add_argument("csv_path"); po.add_argument("--pool", required=True)
    po.add_argument("--batch", required=True); po.add_argument("--date")
    rm = sub.add_parser("remove"); rm.add_argument("--ledger", required=True); rm.add_argument("--campaign", required=True)
    a = ap.parse_args()
    return {"check": cmd_check, "log": cmd_log, "status": cmd_status, "set-status": cmd_set_status,
            "remove": cmd_remove, "pool": cmd_pool}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
