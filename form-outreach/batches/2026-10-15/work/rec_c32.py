import json,sys
KEYS="companyName webDomain country segment verdict skipReason competitor formUrl formSteps formPurpose formFields hasSubjectField messageMaxChars requiredExtras captcha consentBox altEmail articleTitle articleUrl articleDate articleTopic linkPlacement articleHook offerSuggestion offerLine greetingName notes".split()
d=json.loads(sys.stdin.read())
o={k:d.get(k,"") for k in KEYS}
for k,v in o.items():
    if isinstance(v,str) and ("—" in v or "–" in v): o[k]=v.replace("—",",").replace("–","-")
open("results_32.jsonl","a").write(json.dumps(o,ensure_ascii=False)+"\n")
print("ok",o["companyName"],o["verdict"])
