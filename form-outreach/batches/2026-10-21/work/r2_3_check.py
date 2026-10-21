import sys
ex=set(l.strip().lower() for l in open('exclude_domains.txt') if l.strip())
brands={}
for d in ex: brands.setdefault(d.split('.')[0],[]).append(d)
import glob,csv
other=set()
for f in glob.glob('cand_*.csv'):
    if 'r2_3' in f: continue
    try:
        for r in csv.DictReader(open(f)): other.add(r['webDomain'].lower())
    except Exception: pass
for d in sys.argv[1].split():
    d=d.lower();b=d.split('.')[0]
    st='EX' if d in ex else ('BRAND:'+','.join(brands[b]) if b in brands else ('OTHER' if d in other else 'ok'))
    print(d,st)
