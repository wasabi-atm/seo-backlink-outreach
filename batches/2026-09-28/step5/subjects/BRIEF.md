# Brief: hook-based subject lines (backlink-2026-09-28, variant B)

Folder: /home/user/seo-backlink-outreach/batches/2026-09-28/step5/subjects. Input `in_<N>.csv`, output `out_<N>.csv`.

Each row is a cold email Sam (Motion The Agency, a motion design studio) is sending about one of the company's own articles. `emailText` is the email body as plain text. Variant A of the subject is `emailSubject` (it just names the article). You write variant B: a subject that names the specific problem or detail the email points out, so it reads like a note about their page, with some curiosity. The user liked this received subject for its angle: "Update your article list NOW!! Not for me. But for freshness angle!" (keep the angle, not the capitals or "!!").

Good examples (from this batch):
- "your website cost guide still says 2025"
- "272% or 172%?"
- "36 campaigns, 33 on the page"
- "10 SEO problems, 9 bullets"
- "18% or 17% in your cism post"

Rules:
- The subject must point at something that is actually said in `emailText`. Never use a point that is only in articleHook or manualCheck but not in the email (those were left out on purpose, often because they need a browser check).
- 2 to 7 words. Lower case, except numbers, acronyms and proper names where lower case would look wrong (SEO, AI, GA4, UAE, a product name). Plain words, the way a colleague would write it.
- Helpful, not smug or alarming. No "mistake", "error", "wrong", "broken", "oops", "urgent", "!!", capitals for shouting, emoji, or clickbait. A short neutral question is fine ("272% or 172%?").
- Never use "free", "tweak", "suggest", "quick question", "collab", "backlink", "link", "SEO opportunity", "video" as a pitch word, or the company name as the whole subject.
- British spelling. No em dashes or en dashes. No colons at the start. No quotation marks unless you quote a short phrase from the page (then use straight quotes).
- If the email only offers something and names no concrete detail, name the section or the gap in a neutral way, for example "a visual for your onboarding steps" or "the missing chart in your rates report".
- Each subject must be different from the others in your file.

Write `out_<N>.csv` with columns `webDomain, emailSubjectB` (one row per input row, same order) using python's csv module. Then check with a script: row count matches, no empty values, no em or en dash, 2 to 7 words, none of the banned words.

Do not edit any other file and do not commit. Reply with the row count and any rows where you were unsure.
