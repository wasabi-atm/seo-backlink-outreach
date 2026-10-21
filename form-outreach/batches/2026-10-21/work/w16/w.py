import json,sys
K="companyName webDomain country segment verdict skipReason competitor formUrl formSteps formPurpose formFields hasSubjectField messageMaxChars requiredExtras captcha consentBox altEmail articleTitle articleUrl articleDate articleTopic linkPlacement articleHook offerSuggestion offerLine greetingName notes".split()
d=json.loads(sys.stdin.read())
o={k:d.get(k,"") for k in K}
for k in d:
    if k not in o:o[k]=d[k]
open("results_16.jsonl","a").write(json.dumps(o,ensure_ascii=False)+"\n");print("written",o["companyName"],o["verdict"])
