"""Usage: python3 check_domains.py dom1 dom2 ...  (or a file of domains with -f path)
Prints NEW or EXCLUDED (with reason) per domain, against exclude_domains.txt by root domain and brand across TLDs."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/seo-backlink-outreach/skill/mta-backlink-outreach/scripts")
from dedupe import root_domain, brand

ex = [l.strip() for l in open(os.path.join(HERE, "exclude_domains.txt")) if l.strip()]
roots = set(ex)
brands = {}
for r in ex:
    b = brand(r)
    if b:
        brands.setdefault(b, r)
args = sys.argv[1:]
if args[:1] == ["-f"]:
    args = [l.strip() for l in open(args[1]) if l.strip()]
for d in args:
    r = root_domain(d)
    if r in roots:
        print(f"EXCLUDED {d} (already known: {r})")
    elif brand(r) and brand(r) in brands:
        print(f"EXCLUDED {d} (brand match: {brands[brand(r)]})")
    else:
        print(f"NEW {d}")
