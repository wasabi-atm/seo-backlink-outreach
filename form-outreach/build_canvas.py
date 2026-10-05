"""Turns a form outreach batch into Slack canvas markdown.

    python form-outreach/build_canvas.py form-outreach/batches/<YYYY-MM-DD> > canvas.md

Reads 06_form_outreach.csv (companyName, formUrl, beforeSubmit, subjectText, messageText)
and brief.md from the batch folder. One section per company, with a tick box, the form link,
what to do before submitting, the subject if the form has one, and the message in a code block
so it copies cleanly. If 07_left_out.csv (companyName, webDomain, reason) exists, its rows
are listed at the end under "Left out".
"""
import csv, os, re, sys


def brief_value(brief, label):
    m = re.search(rf"^- {re.escape(label)}:\s*(.+)$", brief, re.M)
    return m.group(1).strip() if m else ""


def main(batch):
    rows = list(csv.DictReader(open(os.path.join(batch, "06_form_outreach.csv"), encoding="utf-8")))
    brief = open(os.path.join(batch, "brief.md"), encoding="utf-8").read() if os.path.exists(os.path.join(batch, "brief.md")) else ""
    email = brief_value(brief, "Reply email in forms") or "sam.jupp@globalmotiontheagency.com"
    phone = brief_value(brief, "Phone for forms that require it")
    out = []
    out.append("::: {.callout}")
    out.append(f"**{len(rows)} contact forms ready.** On every form use the name **Sam Jupp** and the email **{email}**"
               + (f". If a form asks for a phone number, use **{phone}**" if phone else "")
               + ". Open the link, do what Before submit says, paste the message, submit, then tick the box.")
    out.append(":::")
    out.append("")
    for i, r in enumerate(rows, 1):
        out.append(f"## {i}. {r['companyName']}")
        out.append("")
        out.append(f"- [ ] Submitted")
        out.append(f"- **Form:** [{r['formUrl']}]({r['formUrl']})")
        out.append(f"- **Before submit:** {r['beforeSubmit'] or 'Nothing extra'}")
        if r.get("subjectText"):
            out.append(f"- **Subject:** {r['subjectText']}")
        out.append("")
        out.append("```")
        out.append(r["messageText"].replace("```", "'''"))
        out.append("```")
        out.append("")
        out.append("---")
        out.append("")
    left = os.path.join(batch, "07_left_out.csv")
    if os.path.exists(left):
        lrows = list(csv.DictReader(open(left, encoding="utf-8")))
        if lrows:
            out.append("## Left out")
            out.append("")
            out.append("Not in today's list. Say if any should go in a later batch.")
            out.append("")
            for r in lrows:
                out.append(f"- **{r['companyName']}** ({r['webDomain']}): {r['reason']}")
            out.append("")
    sys.stdout.write("\n".join(out).rstrip("-\n") + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
