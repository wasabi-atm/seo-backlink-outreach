"""Usage: python3 check_domains.py [--claim SLICE] dom1 dom2 ...  (or -f path for a file of domains)
Prints NEW or EXCLUDED (with reason) per domain, against exclude_domains.txt by root domain and brand across TLDs.
With --claim SLICE, every NEW domain is also written to research/claims.tsv for that slice, and domains
already claimed by another slice print as EXCLUDED, so parallel research agents never pick the same company."""
import fcntl, os, sys
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
slice_name = None
if args[:1] == ["--claim"]:
    slice_name, args = args[1], args[2:]
if args[:1] == ["-f"]:
    args = [l.strip() for l in open(args[1]) if l.strip()]

claims_path = os.path.join(HERE, "research", "claims.tsv")
os.makedirs(os.path.dirname(claims_path), exist_ok=True)
with open(claims_path, "a+") as cf:
    fcntl.flock(cf, fcntl.LOCK_EX)
    cf.seek(0)
    claimed = {}
    claimed_brands = {}
    for line in cf:
        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 2:
            claimed.setdefault(parts[0], parts[1])
            b = brand(parts[0])
            if b:
                claimed_brands.setdefault(b, (parts[0], parts[1]))
    for d in args:
        r = root_domain(d)
        b = brand(r)
        if r in roots:
            print(f"EXCLUDED {d} (already known: {r})")
        elif b and b in brands:
            print(f"EXCLUDED {d} (brand match: {brands[b]})")
        elif r in claimed and claimed[r] != slice_name:
            print(f"EXCLUDED {d} (claimed by slice {claimed[r]})")
        elif b and b in claimed_brands and claimed_brands[b][1] != slice_name:
            print(f"EXCLUDED {d} (brand claimed by slice {claimed_brands[b][1]}: {claimed_brands[b][0]})")
        else:
            print(f"NEW {d}")
            if slice_name and r not in claimed:
                cf.write(f"{r}\t{slice_name}\n")
                claimed[r] = slice_name
                if b:
                    claimed_brands.setdefault(b, (r, slice_name))
    fcntl.flock(cf, fcntl.LOCK_UN)
