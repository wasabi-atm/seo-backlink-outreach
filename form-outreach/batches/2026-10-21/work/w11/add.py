import json,sys
KEYS="companyName webDomain country segment verdict skipReason competitor formUrl formSteps formPurpose formFields hasSubjectField messageMaxChars requiredExtras captcha consentBox altEmail articleTitle articleUrl articleDate articleTopic linkPlacement articleHook offerSuggestion offerLine greetingName notes".split()
d=json.loads(sys.stdin.read())
o={k:d.get(k,"") for k in KEYS}
for k in d:
    if k not in o: o[k]=d[k]
if not o["competitor"]: o["competitor"]="no"
open("/home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-21/work/results_11.jsonl","a").write(json.dumps(o,ensure_ascii=False)+"\n")
print("ok",o["companyName"],o["verdict"])
