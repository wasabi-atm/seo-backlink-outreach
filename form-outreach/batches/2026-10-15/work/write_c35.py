import json,sys
KEYS="companyName webDomain country segment verdict skipReason competitor formUrl formSteps formPurpose formFields hasSubjectField messageMaxChars requiredExtras captcha consentBox altEmail articleTitle articleUrl articleDate articleTopic linkPlacement articleHook offerSuggestion offerLine greetingName notes".split()
d=json.loads(sys.stdin.read())
row={k:d.get(k,"") for k in KEYS}
for k,v in row.items():
    if isinstance(v,str): assert '—' not in v and '–' not in v, k
open('results_35.jsonl','a').write(json.dumps(row,ensure_ascii=False)+"\n")
print("ok",row['companyName'],row['verdict'])
