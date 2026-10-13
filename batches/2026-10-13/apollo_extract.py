import json,sys,re
p=sys.argv[1]
t=open(p).read()
try:
    d=json.loads(t)
except Exception:
    i=t.find('{'); d=json.loads(t[i:])
if isinstance(d,list): d=d[0]
if isinstance(d,dict) and 'text' in d: d=json.loads(d['text'])
rows=[]
for k in ('organizations','accounts'):
    for o in d.get(k,[]):
        dom=o.get('primary_domain') or o.get('domain') or ''
        rows.append((dom,o.get('name'),o.get('estimated_num_employees'),o.get('country') or o.get('organization_country'),(o.get('industry') or '')))
for r in rows: print("\t".join(str(x) for x in r))
