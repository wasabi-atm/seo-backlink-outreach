import json,glob,csv,sys
sys.path.insert(0,'/home/user/seo-backlink-outreach/skill/mta-backlink-outreach/scripts')
from dedupe import root_domain
p={}
for f in sorted(glob.glob('work/results_*.jsonl')):
    for l in open(f):
        l=l.strip()
        if not l: continue
        try:d=json.loads(l)
        except: continue
        if d.get('verdict')=='pass' and d.get('competitor','no')!='yes':
            p.setdefault(root_domain(d['webDomain']),d)
cols=['companyName','webDomain','country','segment','competitor','drChecked','articleTitle','articleUrl','articleDate','articleTopic','linkPlacement','articleHook','offerSuggestion','offerLine','articleShortName','publicEmail','notes']
with open('work/merged1.csv','w',newline='') as o:
    w=csv.DictWriter(o,fieldnames=cols,extrasaction='ignore');w.writeheader()
    for d in p.values(): w.writerow(d)
print(len(p))
