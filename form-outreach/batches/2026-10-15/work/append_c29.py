import json,sys
KEYS="companyName webDomain country segment verdict skipReason competitor formUrl formSteps formPurpose formFields hasSubjectField messageMaxChars requiredExtras captcha consentBox altEmail articleTitle articleUrl articleDate articleTopic linkPlacement articleHook offerSuggestion offerLine greetingName notes".split()
d=json.loads(sys.stdin.read())
row={k:d.get(k,"") for k in KEYS}
for k,v in row.items():
    if isinstance(v,str) and ("—" in v or "–" in v): raise SystemExit("dash in "+k)
open("/home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-15/work/results_29.jsonl","a").write(json.dumps(row,ensure_ascii=False)+"\n")
print("ok",row["companyName"],row["verdict"])
