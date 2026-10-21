import sys, glob, csv, os
W = os.path.dirname(os.path.abspath(__file__))
ex = set(l.strip().lower() for l in open(os.path.join(W, 'exclude_domains.txt')) if l.strip())
brands = {}
for d in ex:
    brands.setdefault(d.split('.')[0], []).append(d)
# also other candidate files in this dir (not mine)
other = set()
for f in glob.glob(os.path.join(W, 'cand*.csv')):
    if 'r2_1' in f:
        continue
    try:
        for r in csv.DictReader(open(f)):
            other.add((r.get('webDomain') or '').strip().lower())
    except Exception:
        pass
for line in open(sys.argv[1]):
    d = line.strip().lower()
    if not d:
        continue
    b = d.split('.')[0]
    hit = []
    if d in ex: hit.append('EXACT')
    if b in brands: hit.append('BRAND:' + ','.join(brands[b][:3]))
    if d in other: hit.append('OTHERCAND')
    print(('DROP ' if hit else 'OK   ') + d + ' ' + ' '.join(hit))
