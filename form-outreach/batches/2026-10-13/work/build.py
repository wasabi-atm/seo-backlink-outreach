import json,csv,re,sys
sys.path.insert(0,'work'); from rows import R
B='.'
M=json.load(open('work/merged.json')); LO=json.load(open('work/review_leftout.json'))
DR={"luxhabitat.ae":55,"visdum.com":46,"hyperproof.io":72,"helmwms.com":55,"adit.com":77,"milestoneinternet.com":79,"bigchange.com":62,"pinewood.ai":50,"equinetacademy.com":47,"celtra.com":75,"wrappedagency.co.uk":42,"robot-food.com":45,"socialchain.com":55,"aeolidia.com":70,"rocketreach.co":76,"paytabs.com":70,"ducttapemarketing.com":77,"brandpie.com":43,"3sidedcube.com":62,"medianet.com.au":70,"digitalthirdcoast.com":67,"reloadmedia.com.au":57,"scorchedmedia.com.au":61,"lexer.io":63,"particularaudience.com":51,"rezdy.com":85,"squiz.net":72,"marketplacer.com":60,"jobadder.com":80,"expert360.com":52,"bigtincan.com":73,"2stallions.com":55,"whispir.com":60,"relevanceai.com":75,"bringdigital.co.uk":47,"osome.com":71,"inspire.scot":57,"measuremindsgroup.com":64,"pixeledeggs.com":40,"nivo.co.uk":54,"i-com.net":50,"wearehype.co.uk":41,"ketchup-marketing.co.uk":45,"zoocha.com":43,"logicdigital.co.uk":41,"boxchilli.com":65,"hedgehogdigital.co.uk":59,"bigfork.co.uk":64,"betterproposals.io":75,"tmpw.co.uk":59,"talos360.co.uk":73,"claromentis.com":52,"workbooks.com":68,"webrecruit.co":48,"savanta.com":73,"viget.com":74,"instrument.com":73,"elementthree.com":59,"firefishsoftware.com":71,"marceldigital.com":56,"fusion92.com":53,"perfectsearchmedia.com":51,"ologie.com":50,"launchsquad.com":41,"covideo.com":66,"switcherstudio.com":71,"homebot.ai":75,"alertmedia.com":69}
alias={'despatchcloud.com':'helmwms.com'}
byd={x['webDomain']:x for x in M}
def msg(d):
  g,k,hook,off,subj,bs=R[d]; x=byd[d]
  t=x['articleTitle'].replace('’',"'").replace('–','-').replace('—','-')
  p=[f"Hey {g} team,", f'Just read your piece "{t}" ({x["articleUrl"]}). {hook}']
  if k=='Q':
    p+= [f'I run a motion studio. Happy to swap founder quotes: one from me for your {off}, and one from you for ours.' if not off.startswith('the part') else f'I run a motion studio. Happy to swap founder quotes: one from me for {off}, and one from you for ours.',
         "In return, a credit link back to motiontheagency.com with my quote, and one to yours with your quote on ours, or we'll pay for placement instead."]
  else:
    p+= [f'I run a motion studio. Happy to {off}, free.', "In return, just a credit link back to motiontheagency.com, or we'll pay for placement instead."]
  p+= ["Would you be open to exploring this?", "Cheers,\nSam\nFounder @ Motion The Agency"]
  return "\n\n".join(p)
sel=list(R)
# quote-swap section phrase: "your the X section" fix
targets=[];sub=[];bad=0
for d in sel:
  x=byd[d]; g,k,hook,off,subj,bs=R[d]
  m=msg(d).replace('your the ','your ')
  dash=re.findall('[–—]',m)
  lim=x.get('messageMaxChars')
  try: lim=int(lim)
  except: lim=None
  print(f"{d:28} {len(m.split()):4}w {len(m):5}c lim={lim} {'DASH' if dash else ''} {'OVER' if lim and len(m)>lim else ''}")
  if dash or (lim and len(m)>lim): bad+=1
  live=alias.get(d,d)
  offer='Founder\'s quote swap' if k=='Q' else x.get('offerSuggestion')
  targets.append({'companyName':x['companyName'],'webDomain':d,'domainRating':DR[live],'drSource':'Apify ahrefs-scraper','drDate':'2026-10-13','country':x['country'],'segment':x['segment'],'offer':offer,'formUrl':x['formUrl'],'formSteps':x.get('formSteps',''),'articleTitle':x['articleTitle'],'articleUrl':x['articleUrl'],'articleTopic':x.get('articleTopic',''),'linkPlacement':x.get('linkPlacement',''),'articleHook':hook,'captcha':x.get('captcha',''),'consentBox':x.get('consentBox',''),'source':x.get('source',''),'liveDomain':live if live!=d else ''})
  sub.append({'companyName':x['companyName'],'formUrl':x['formUrl'],'beforeSubmit':bs,'subjectText':subj,'messageText':m})
print('bad',bad,len(sel))
w=csv.DictWriter(open('03_form_targets.csv','w',newline=''),fieldnames=list(targets[0])); w.writeheader(); w.writerows(targets)
w=csv.DictWriter(open('06_form_outreach.csv','w',newline=''),fieldnames=list(sub[0])); w.writeheader(); w.writerows(sub)
# 02_forms: all researched
cols=['companyName','webDomain','country','segment','verdict','skipReason','formUrl','formSteps','formPurpose','formFields','hasSubjectField','messageMaxChars','requiredExtras','captcha','consentBox','altEmail','articleTitle','articleUrl','articleDate','notes']
w=csv.DictWriter(open('02_forms.csv','w',newline=''),fieldnames=cols,extrasaction='ignore'); w.writeheader(); w.writerows(M)
# low DR
low=[{'companyName':'Social Garden (now The Garden)','webDomain':'socialgarden.com.au','domainRating':28,'country':'Australia','segment':'A','dataSource':'ahrefs free (thegarden.com.au)','drStatus':'low'},
     {'companyName':'Parcel Perform (now Perform.AI)','webDomain':'parcelperform.com','domainRating':38,'country':'Singapore','segment':'B','dataSource':'ahrefs free (perform.ai)','drStatus':'low'}]
w=csv.DictWriter(open('02_low_dr.csv','w',newline=''),fieldnames=list(low[0])); w.writeheader(); w.writerows(low)
# left out
lo=[]
spare=[d for d in DR if d not in [alias.get(s,s) for s in sel]]
for x in M:
  if x['verdict']=='pass' and alias.get(x['webDomain'],x['webDomain']) in spare:
    lo.append({'companyName':x['companyName'],'webDomain':x['webDomain'],'reason':'Passed every check (DR %d); spare for a later batch, weaker hook or fit than today\'s 50'%DR[x['webDomain']]})
for d,r in LO.items(): lo.append({'companyName':byd[d]['companyName'],'webDomain':d,'reason':r})
for x in M:
  if x['verdict']!='pass':
    rs=(x.get('skipReason') or '').replace('—',',').replace('–',',')
    if x.get('competitor')=='yes': rs='Competitor: '+rs
    lo.append({'companyName':x['companyName'],'webDomain':x['webDomain'],'reason':rs})
for l in low: lo.append({'companyName':l['companyName'],'webDomain':l['webDomain'],'reason':'DR under 40 on its live domain (%d); added to the low DR pool'%l['domainRating']})
for r in csv.DictReader(open('00_candidates_duplicates.csv')):
  lo.append({'companyName':r['companyName'],'webDomain':r['webDomain'],'reason':'Already in the ledger or a likely brand match: '+r['dedupeReason'][:120]})
w=csv.DictWriter(open('07_left_out.csv','w',newline=''),fieldnames=['companyName','webDomain','reason']); w.writeheader(); w.writerows(lo)
print('leftout',len(lo))
