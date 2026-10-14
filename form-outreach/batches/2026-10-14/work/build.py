import json,csv,re,sys
sys.path.insert(0,'work'); from rows import R
M={x['webDomain']:x for x in json.load(open('work/merged.json'))}
DR=json.load(open('work/dr_today.json'))
alias={'reddico.co.uk':'thisisgain.com'}
def title(t): return t.replace('’',"'").replace('‘',"'").replace('–','-').replace('—','-').replace('“','"').replace('”','"')
def msg(d):
  g,k,hook,off,subj,bs=R[d]; x=M[d]
  p=[f"Hey {g} team,", f'Just read your piece "{title(x["articleTitle"])}" ({x["articleUrl"]}). {hook}']
  if k=='Q':
    p+=[f'I run a motion studio. Happy to swap founder quotes: one from me for your "{off}" section, and one from you for ours.',
        "In return, a credit link back to motiontheagency.com with my quote, and one to yours with your quote on ours, or we'll pay for placement instead."]
  else:
    p+=[f'I run a motion studio. Happy to {off}, free.', "In return, just a credit link back to motiontheagency.com, or we'll pay for placement instead."]
  p+=["Would you be open to exploring this?","Cheers,\nSam\nFounder @ Motion The Agency"]
  return "\n\n".join(p)
T=[];S=[];bad=0
for d in R:
  x=M[d]; g,k,hook,off,subj,bs=R[d]; m=msg(d)
  dash=re.findall('[–—]',m+bs+subj)
  try: lim=int(x.get('messageMaxChars') or 0)
  except: lim=0
  over=lim and len(m)>lim
  print(f"{d:28} {len(m.split()):4}w {len(m):5}c lim={lim or '-'} {'DASH' if dash else ''} {'OVER' if over else ''}")
  bad+= bool(dash or over)
  live=alias.get(d,d)
  country={'United Kingdom':'UK'}.get(x['country'],x['country'])
  if d=='appinstitute.com': country='UK'
  T.append(dict(companyName=x['companyName'],webDomain=d,domainRating=DR[live],drSource='Apify ahrefs-scraper',drDate='2026-10-14',country=country,segment=x['segment'],offer="Founder's quote swap" if k=='Q' else x.get('offerSuggestion'),formUrl=x['formUrl'],formSteps=x.get('formSteps',''),articleTitle=title(x['articleTitle']),articleUrl=x['articleUrl'],articleTopic=x.get('articleTopic',''),linkPlacement=x.get('linkPlacement',''),articleHook=hook,captcha=x.get('captcha',''),consentBox=x.get('consentBox',''),source=x.get('source','') or '',liveDomain=live if live!=d else ''))
  S.append(dict(companyName=x['companyName'],formUrl=x['formUrl'],beforeSubmit=bs,subjectText=subj,messageText=m))
print('bad',bad,len(R))
w=csv.DictWriter(open('03_form_targets.csv','w',newline=''),fieldnames=list(T[0])); w.writeheader(); w.writerows(T)
w=csv.DictWriter(open('06_form_outreach.csv','w',newline=''),fieldnames=list(S[0])); w.writeheader(); w.writerows(S)
