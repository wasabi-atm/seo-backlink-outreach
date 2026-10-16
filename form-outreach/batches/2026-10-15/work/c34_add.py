import json,sys
keys="companyName webDomain country segment verdict skipReason competitor formUrl formSteps formPurpose formFields hasSubjectField messageMaxChars requiredExtras captcha consentBox altEmail articleTitle articleUrl articleDate articleTopic linkPlacement articleHook offerSuggestion offerLine greetingName notes".split()
d=json.loads(sys.stdin.read())
o={k:d.get(k,"") for k in keys}
open("/home/claude/seo-backlink-outreach/form-outreach/batches/2026-10-15/work/results_34.jsonl","a").write(json.dumps(o,ensure_ascii=False)+"\n")
print("ok",o["companyName"],o["verdict"])
