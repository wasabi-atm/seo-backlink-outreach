import json,csv,re,sys
sys.path.insert(0,'work'); from rows import R,SPARE,DUP
DRtxt="""ajmarketing.io 45,awebstar.com.sg 56,brick.work 66,buildxact.com 68,clearwateragency.com.au 43,cloudcampaign.com 67,contentfac.com 64,digitalpresence.com.au 47,digitrends.co 41,digitrio.com.sg 41,embryo.com 73,emotedigital.com.au 44,ezycollect.io 41,gotolstoy.com 71,hellobar.com 76,hivelearning.com 58,hyperproof.io 72,impactbc.com.sg 50,juicebox.ai 70,loop-digital.co.uk 59,loukengroup.com 44,marginmedia.com.au 55,marketbridge.com 59,mblm.com 59,mediaone.sg 53,mojodojo.io 45,netstripes.com 60,neuentity.com 48,odysseynewmedia.com 40,onlineroad.com.au 45,onspring.com 63,ordergroove.com 70,pageuppeople.com 79,pixability.com 64,preset.io 66,propertyme.com.au 63,pubnub.com 76,qagency.com.au 60,readingroom.com 44,recurpost.com 73,redeye.com 66,reefdigital.com.au 45,richpanel.com 71,roi.com.au 53,ruleranalytics.com 78,seeresponse.com 61,servagency.com.au 65,shorthand.com 81,skale.so 67,studiobinder.com 78,thedesignocracy.com 48,thedigitalpicnic.com.au 40,thedigitalring.com 45,theinsightcollective.com 59,thesocialelement.agency 55,transmissionagency.com 65,trewmarketing.com 56,unlimit.com 64,userled.io 46,wearecatalyst.co.uk 40,wearehype.co.uk 41,weave.asia 41,webqem.com 55,wiise.com 42,wiseupmarketing.com.au 58,zandahealth.com 82,zeroseven.com.au 44"""
DR={k:int(v) for k,v in (x.split() for x in DRtxt.split(','))}
P={r['webDomain']:r for r in json.load(open('work/passes.json'))}
M=json.load(open('work/merged.json')); U=json.load(open('work/unsure.json'))
PHONE='+44 2039847787'
def clean(s): return (s or '').replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('–',',').replace('—',',')
def msg(d):
    g,k,hook,off,subj,cn=R[d]; x=P[d]
    t=clean(x['articleTitle']).strip()
    p=[f"Hey {g} team,", f'Just read your piece "{t}" ({x["articleUrl"]}). {hook}']
    if k=='Q':
        sec=off[5:] if off.startswith('PART:') else f'your "{off}" section'
        p+=[f'I run a motion studio. Happy to swap founder quotes: one from me for {sec}, and one from you for ours.',
            "In return, a credit link back to motiontheagency.com with my quote, and one to yours with your quote on ours, or we'll pay for placement instead."]
    else:
        p+=[f'I run a motion studio. Happy to {off}, free.', "In return, just a credit link back to motiontheagency.com, or we'll pay for placement instead."]
    p+=["Would you be open to exploring this?","Cheers,\nSam\nFounder @ Motion The Agency"]
    return "\n\n".join(p)
def before(x):
    parts=[]
    st=clean(x.get('formSteps')).strip().rstrip('.')
    if st: parts.append(st+'.')
    rq=clean(x.get('requiredExtras')).strip().rstrip('.')
    if rq and not rq.lower().startswith('none'):
        rq=re.sub(r'Phone( number| Number)? required[^;]*', f'Phone is required: {PHONE}', rq)
        rq=re.sub(r'(Mobile( phone)?|Telephone|Contact number) required[^;]*', f'Phone is required: {PHONE}', rq)
        parts.append('Also fill in: '+rq+'.')
    cap=x.get('captcha','')
    if cap in ('recaptchaCheckbox','hcaptcha'): parts.append('Tick the CAPTCHA box yourself.')
    elif cap=='turnstile': parts.append('A Cloudflare check may show; complete it yourself.')
    cons=x.get('consentBox','')
    if cons=='requiredTerms' and 'consent' not in ' '.join(parts).lower() and 'tick' not in ' '.join(parts).lower(): parts.append('Tick the required privacy or terms box.')
    if cons=='optionalMarketing': parts.append('Leave the marketing opt-in unticked.')
    return ' '.join(parts) or 'Nothing extra'
targets=[];sub=[];bad=0
for d in R:
    x=P[d]; g,k,hook,off,subj,cn=R[d]; m=msg(d)
    lim=x.get('messageMaxChars')
    try: lim=int(lim)
    except: lim=None
    dash=re.findall('[–—]',m+before(x)+subj)
    flag=('DASH ' if dash else '')+('OVER' if lim and len(m)>lim else '')
    if flag: bad+=1
    print(f"{d:26} {len(m.split()):4}w {len(m):5}c lim={lim} {flag}")
    live=x['liveDomain']
    offer="Founder's quote swap" if k=='Q' else x.get('offerSuggestion')
    targets.append({'companyName':cn or x['companyName'],'webDomain':d,'domainRating':DR[live],'drSource':'Ahrefs public-domain-rating-free','drDate':'2026-10-15','country':{'Singapore':'SG','Australia':'AU'}.get(x['country'],x['country']),'segment':x['segment'],'offer':offer,'formUrl':x['formUrl'],'formSteps':clean(x.get('formSteps')),'articleTitle':clean(x['articleTitle']),'articleUrl':x['articleUrl'],'articleDate':x.get('articleDate',''),'articleTopic':clean(x.get('articleTopic')),'linkPlacement':clean(x.get('linkPlacement')),'articleHook':hook,'captcha':x.get('captcha',''),'consentBox':x.get('consentBox',''),'source':x.get('source',''),'liveDomain':live if live!=d else ''})
    sub.append({'companyName':cn or x['companyName'],'formUrl':x['formUrl'],'beforeSubmit':before(x),'subjectText':subj,'messageText':m})
print('bad',bad,len(sub))
w=csv.DictWriter(open('03_form_targets.csv','w',newline=''),fieldnames=list(targets[0])); w.writeheader(); w.writerows(targets)
w=csv.DictWriter(open('06_form_outreach.csv','w',newline=''),fieldnames=list(sub[0])); w.writeheader(); w.writerows(sub)
cols=['companyName','webDomain','country','segment','verdict','skipReason','competitor','formUrl','formSteps','formPurpose','formFields','hasSubjectField','messageMaxChars','requiredExtras','captcha','consentBox','altEmail','articleTitle','articleUrl','articleDate','notes']
w=csv.DictWriter(open('02_forms.csv','w',newline=''),fieldnames=cols,extrasaction='ignore'); w.writeheader(); w.writerows(M)
w=csv.writer(open('02_low_dr.csv','w',newline='')); w.writerow(['companyName','webDomain','domainRating','country','segment','dataSource','drStatus'])
lo=[]
for d,why in SPARE.items():
    live=P[d]['liveDomain']; lo.append({'companyName':P[d]['companyName'],'webDomain':d,'reason':f'{why} (DR {DR[live]}); spare for a later batch','altEmail':''})
for d,why in DUP.items(): lo.append({'companyName':P[d]['companyName'],'webDomain':d,'reason':why,'altEmail':''})
for n,d,why in U: lo.append({'companyName':n,'webDomain':d,'reason':'Passed but left out as unsure: '+why,'altEmail':''})
for x in M:
    if x['verdict']!='pass':
        rs=clean(x.get('skipReason'))
        if x.get('competitor')=='yes': rs='Competitor: '+rs
        lo.append({'companyName':x['companyName'],'webDomain':x['webDomain'],'reason':rs,'altEmail':x.get('altEmail','')})
for r in csv.DictReader(open('00_candidates_duplicates.csv')):
    lo.append({'companyName':r['companyName'],'webDomain':r['webDomain'],'reason':'Already in the ledger or a likely brand match','altEmail':''})
for r in csv.DictReader(open('work/new_candidates_duplicates.csv')):
    lo.append({'companyName':r['companyName'],'webDomain':r['webDomain'],'reason':'Already in the ledger or a likely brand match','altEmail':''})
for l in lo: l['reason']=clean(l['reason'])
w=csv.DictWriter(open('07_left_out.csv','w',newline=''),fieldnames=['companyName','webDomain','reason','altEmail']); w.writeheader(); w.writerows(lo)
print('leftout',len(lo))
