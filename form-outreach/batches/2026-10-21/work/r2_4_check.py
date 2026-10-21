import sys
ex=set(l.strip().lower() for l in open('exclude_domains.txt') if l.strip())
brands={}
for d in ex:
    brands.setdefault(d.split('.')[0],[]).append(d)
import glob
others=set()
for f in glob.glob('cand_r2_*.csv'):
    if 'r2_4' in f: continue
    for l in open(f).read().splitlines()[1:]:
        p=l.split(',')
        if len(p)>1: others.add(p[1].strip().lower())
for d in sys.stdin.read().split():
    d=d.lower(); b=d.split('.')[0]
    if d in ex: print('EX',d)
    elif b in brands: print('BR',d,brands[b])
    elif d in others: print('OTH',d)
    else: print('OK',d)
