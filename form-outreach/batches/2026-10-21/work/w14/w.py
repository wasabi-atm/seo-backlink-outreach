import json,sys
keys="companyName webDomain country segment verdict skipReason competitor formUrl formSteps formPurpose formFields hasSubjectField messageMaxChars requiredExtras captcha consentBox altEmail articleTitle articleUrl articleDate articleTopic linkPlacement articleHook offerSuggestion offerLine greetingName notes".split()
d=json.loads(sys.stdin.read())
r={k:"" for k in keys}; r["competitor"]="no"; r.update(d)
for k,v in r.items():
    if isinstance(v,str) and ('—' in v or '–' in v): print("DASH in",k)
open('/home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-21/work/results_14.jsonl','a').write(json.dumps(r)+"\n")
print("ok",r["companyName"],r["verdict"])
