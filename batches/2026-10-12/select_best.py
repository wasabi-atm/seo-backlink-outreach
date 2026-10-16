"""Pick the best rows per batch folder: all strong, then ok ranked by link habits, until the quota. Weak rows are held, surplus ok rows are spares."""
import csv, collections
QUOTA = {"2026-10-12": 43, "2026-10-12-b2": 43, "2026-10-12-b3": 42, "2026-10-12-b4": 42}
FIT = {"strong": 0, "ok": 1}
LINK = {"Yes": 0, "Some": 1, "unchecked": 2, "No": 3}
def stale(r):
    pub, mod = r.get("articlePublished") or "", r.get("articleDate") or ""
    newest = max(pub, mod)
    return 1 if newest and newest < "2024-10-01" else 0
tot = collections.Counter()
for n, q in QUOTA.items():
    rows = list(csv.DictReader(open(f"{n}/03_backlink_targets.csv", encoding="utf-8")))
    cols = list(rows[0].keys())
    weak = [r for r in rows if r["fit"] == "weak"]
    good = [r for r in rows if r["fit"] in FIT]
    good.sort(key=lambda r: (FIT[r["fit"]], stale(r), LINK.get(r["backlinkExchange"], 2), 0 if r["country"] in ("UK", "UAE") else 1, -int(r["domainRating"] or 0)))
    sel, spare = good[:q], good[q:]
    for fn, data in ((f"targets_{q}.csv", sel), ("03_held_weak.csv", weak), ("03_spares.csv", spare)):
        with open(f"{n}/{fn}", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(data)
    print(n, "selected", len(sel), "spares", len(spare), "weak held", len(weak), "|", dict(collections.Counter(r["fit"] for r in sel)), dict(collections.Counter(r["backlinkExchange"] for r in sel)), dict(collections.Counter(r["segment"] for r in sel)), dict(collections.Counter(r["country"] for r in sel)))
    print("   spares:", [(r["webDomain"], r["fit"], r["backlinkExchange"]) for r in spare])
    tot.update({"sel": len(sel), "spare": len(spare), "weak": len(weak)})
print(dict(tot))
