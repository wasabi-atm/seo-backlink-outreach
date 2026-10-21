import json,re,sys
sys.path.insert(0,'.')
from msgdata import D
fin=json.load(open('final.json'))
def msg(j):
    g,hook,off,bs,subj=D[j['companyName']]
    t=j['articleTitle'].replace('—',', ').replace('–',', ').replace('’',"'")
    lines=[f"Hey {g} team,", "", f"Just read your piece \"{t}\" ({j['articleUrl']}). {hook}", ""]
    if off[0]=='Q':
        lines+=[f"I run a motion studio. Happy to swap founder quotes: one from me for your \"{off[1]}\" section, and one from you for ours.","",
                "In return, a credit link back to motiontheagency.com with my quote, and one to yours with yours, or we'll pay for placement instead."]
    else:
        lines+=[f"I run a motion studio. Happy to {off[1]}, free.","","In return, just a credit link back to motiontheagency.com, or we'll pay for placement instead."]
    lines+=["","Would you be open to exploring this?","","Cheers,","Sam","Founder @ Motion The Agency"]
    return "\n".join(lines)
out={}
for j in fin:
    m=msg(j); out[j['companyName']]=m
    bad=re.findall('[–—]',m)
    lim=j.get('messageMaxChars') or ''
    print(f"### {j['companyName']} words={len(m.split())} chars={len(m)} limit={lim} dashes={len(bad)}")
    print(m.split('\n')[2]); print(m.split('\n')[4]); print()
json.dump(out,open('messages.json','w'),indent=1)
