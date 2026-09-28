#!/usr/bin/env python3
"""Check the A/B subject lines in an emails CSV against the SKILL.md subject rules.

    python subject_check.py 04_backlink_emails.csv [--single]

--single checks emailSubject and subjectTypeA only, for a batch sent without an A/B test.

Reads emailSubject, emailSubjectB, subjectTypeA, subjectTypeB (and firstName, emailBody when present)
and prints every rule a row breaks. Exits 1 if anything is wrong, so it can gate a save.
"""
import csv
import re
import sys
from collections import Counter

MAX_CHARS = 45
TYPES = {"trigger", "question", "value"}
BANNED = [r"\blinks?\b", r"backlinks?", r"link building", r"guest post", r"\bseo\b", r"opportunit", r"collaborat",
          r"partnership", r"\bfree\b", r"quick question", r"following up", r"^\s*(re|fwd?)\s*:", r"!", r"[–—]|\s-\s"]


def problems(row, single=False):
    out = []
    subs = [(row.get("emailSubject", ""), row.get("subjectTypeA", ""), "A"),
            (row.get("emailSubjectB", ""), row.get("subjectTypeB", ""), "B")]
    if single:
        subs = subs[:1]
    for s, t, v in subs:
        s = s.strip()
        if not s:
            out.append(f"{v}: empty")
            continue
        n = len(s.split())
        if not 3 <= n <= 8:
            out.append(f"{v}: {n} words")
        if len(s) > MAX_CHARS:
            out.append(f"{v}: {len(s)} chars")
        if s.endswith("."):
            out.append(f"{v}: full stop")
        for p in BANNED:
            if re.search(p, s, re.I):
                out.append(f"{v}: banned {p!r}")
        if re.search(r"[\U0001F300-\U0001FAFF]", s):
            out.append(f"{v}: emoji")
        if re.search(r"\b[A-Z]{2,}\b", s) and s == s.upper():
            out.append(f"{v}: all caps")
        first = (row.get("firstName") or "").strip().lower()
        if first and re.search(rf"\b{re.escape(first)}\b", s.lower()):
            out.append(f"{v}: uses first name")
        if t not in TYPES:
            out.append(f"{v}: type {t!r} not in {sorted(TYPES)}")
    if not single and subs[0][1] and subs[0][1] == subs[1][1]:
        out.append("A and B are the same type")
    if not single and subs[0][0].strip().lower() == subs[1][0].strip().lower() and subs[0][0].strip():
        out.append("A and B are identical")
    return out


def main(path, single=False):
    rows = [r for r in csv.DictReader(open(path, newline="")) if (r.get("emailBody") or "").strip()]
    bad = 0
    for r in rows:
        p = problems(r, single)
        if p:
            bad += 1
            print(r.get("webDomain", "?"), "|", "; ".join(p))
    subs = [s.strip().lower() for r in rows for s in (r.get("emailSubject", ""), "" if single else r.get("emailSubjectB", "")) if s.strip()]
    dupes = [s for s, c in Counter(subs).items() if c > 1]
    if dupes:
        bad += 1
        print("duplicate subjects:", dupes)
    starts = Counter(" ".join(s.split()[:1]) + (" ... " + s.split()[-1] if len(s.split()) > 1 else "") for s in subs)
    common, count = starts.most_common(1)[0] if starts else ("", 0)
    if subs and count > len(subs) / 3:
        bad += 1
        print(f"too uniform: {count} of {len(subs)} subjects look like '{common}'")
    print(f"{len(rows)} rows with a body; {bad} problem lines;",
          "types:", dict(Counter(r.get(k, "") for r in rows for k in (("subjectTypeA",) if single else ("subjectTypeA", "subjectTypeB")))))
    return 1 if bad else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--single"]
    if len(args) != 1:
        sys.exit(__doc__)
    sys.exit(main(args[0], "--single" in sys.argv[1:]))
