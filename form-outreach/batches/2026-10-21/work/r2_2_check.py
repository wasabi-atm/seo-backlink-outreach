import sys
ex=set(l.strip().lower() for l in open('exclude_domains.txt') if l.strip())
brands={}
for d in ex: brands.setdefault(d.split('.')[0],[]).append(d)
for d in sys.argv[1:]:
    d=d.lower(); b=d.split('.')[0]
    if d in ex: print('EXCL',d)
    elif b in brands: print('BRAND',d,brands[b][:3])
    else: print('OK',d)
