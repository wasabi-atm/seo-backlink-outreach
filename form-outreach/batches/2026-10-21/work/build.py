import json,csv,sys,re
sys.path.insert(0,'/home/claude/seo-backlink-outreach/skill/mta-backlink-outreach/scripts')
sys.path.insert(0,'work')
from dedupe import root_domain
from msgdata import D
DATE='2026-10-21'
fin=json.load(open('work/final.json')); sp=json.load(open('work/spare.json'))
msgs=json.load(open('work/messages.json'))
allr=json.load(open('work/r1_all.json'))+json.load(open('work/r2_all.json'))
unsure=json.load(open('work/left_unsure.json'))['out']
def W(name,cols,rows):
    with open(name,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
# 02_forms
fc=['companyName','webDomain','liveDomain','country','segment','verdict','skipReason','competitor','formUrl','formSteps','formPurpose','formFields','hasSubjectField','messageMaxChars','requiredExtras','captcha','consentBox','altEmail','articleTitle','articleUrl','articleDate','articleTopic','linkPlacement','articleHook','offerSuggestion','notes']
W('02_forms.csv',fc,allr)
# 03 and 06
OFF={'Q':"Founder's quote swap"}
t3=[];t6=[]
for j in fin:
    g,hook,off,bs,subj=D[j['companyName']]
    live=root_domain(j.get('liveDomain') or j['webDomain'])
    offer="Founder's quote swap" if off[0]=='Q' else j.get('offerSuggestion')
    t3.append(dict(companyName=j['companyName'],webDomain=live,domainRating=j['domainRating'],drSource='Apify ahrefs-scraper',drDate=DATE,country=j['country'],segment=j['segment'],offer=offer,formUrl=j['formUrl'],formSteps=j.get('formSteps',''),articleTitle=j['articleTitle'],articleUrl=j['articleUrl'],articleDate=j.get('articleDate',''),articleTopic=j.get('articleTopic',''),linkPlacement=j.get('linkPlacement',''),articleHook=hook,captcha=j.get('captcha',''),consentBox=j.get('consentBox',''),originalDomain=j['webDomain'] if root_domain(j['webDomain'])!=live else ''))
    t6.append(dict(companyName=j['companyName'],formUrl=j['formUrl'],beforeSubmit=bs,subjectText=subj,messageText=msgs[j['companyName']]))
W('03_form_targets.csv',['companyName','webDomain','domainRating','drSource','drDate','country','segment','offer','formUrl','formSteps','articleTitle','articleUrl','articleDate','articleTopic','linkPlacement','articleHook','captcha','consentBox','originalDomain'],t3)
W('06_form_outreach.csv',['companyName','formUrl','beforeSubmit','subjectText','messageText'],t6)
# 07 left out: competitors + unsure + spares
lo=[]
for j in allr:
    if j.get('competitor')=='yes':
        lo.append(dict(companyName=j['companyName'],webDomain=root_domain(j.get('liveDomain') or j['webDomain']),reason='Competitor: '+re.sub(r'^(Likely competitor|Competitor)( and no longer independent)?:\s*','',(j.get('skipReason') or 'sells video or animation')).replace(' (competitor)',''),altEmail=j.get('altEmail','')))
byn={j['companyName']:j for j in allr}
for n,r in unsure.items():
    j=byn[n]; lo.append(dict(companyName=n,webDomain=root_domain(j.get('liveDomain') or j['webDomain']),reason='Passed the form and article checks but left out as unsure: '+r,altEmail=j.get('altEmail','')))
for j in sp:
    lo.append(dict(companyName=j['companyName'],webDomain=root_domain(j.get('liveDomain') or j['webDomain']),reason=(f"Left out as unsure (DR {j['domainRating']}): {j['holdReason']}" if j['companyName'] in ('Five Q','Rebrandly') else f"Passed every check (DR {j['domainRating']}); held as a spare because the batch is capped at 50. Weaker point: {j['holdReason']}"),altEmail=j.get('altEmail','')))
W('07_left_out.csv',['companyName','webDomain','reason','altEmail'],lo)
# low DR
low=list(csv.DictReader(open('work/screen_low.csv')))
W('02_low_dr.csv',['companyName','webDomain','domainRating','country','serviceType','segment','visualScore','backlinkExchange','backlinkEvidence','dataSource','competitor','drStatus','videoSchemaGap'],
  [dict(r,domainRating=r['drFree'],dataSource='Ahrefs public-domain-rating-free',competitor='no',drStatus='low' if r['drFree'] else 'unknown') for r in low])
print(len(t3),len(t6),len(lo),len(low),len(allr))
for r in t6+lo:
    for v in r.values():
        if re.search('[–—]',str(v)): print('DASH',r['companyName'])
