"""Candidates from the Video SEO SaaS research (2026-09-25-video-seo/00_candidates_all.csv) that are
not among the 178 skipped companies, not in the ledger, pool or past vetting, and have DR 40+ (free endpoint).
Consumer apps, non-UK/UAE companies and dead or acquired sites are dropped; marketing tools go to Segment A."""
import csv

DROP = {
    # consumer apps or not B2B
    "dice.fm", "flo.health", "withplum.com", "runna.com", "justpark.com", "designmynight.com", "what3words.com",
    "doctify.com", "mynewterm.com", "dragonpass.com", "astratech.ae", "overleaf.com", "affinity.studio",
    # not UK/UAE based
    "kovai.co", "mozilor.com", "venpep.com", "ant.works", "exlibrisgroup.com", "teknikforce.com", "paysyslabs.com",
    "trasna.io", "iproyal.com", "smithii.io", "cequens.com",
    # dead, acquired or part of a bigger group
    "imimobile.com", "swap.com", "learningpool.com", "tungsten-network.com", "climate.ai", "dyedurham.co.uk", "demica.com", "tdxgroup.com", "edenred.co.uk", "parentpaygroup.com",
    # dropped in the Video SEO screen (hardware, forensics) or web3 or other weak fit
    "vicon.com", "forensicanalytics.io", "biconomy.io", "availproject.org", "allo.xyz", "coinpayments.net",
    "radixdlt.com", "kezana.net", "notch.one", "move.ai", "foundry.com",
}
SEG_A = {  # marketing and adtech tools, web agencies: same buyers as MTA
    "mapp.com": "Customer engagement and marketing platform", "lolly.com": "Marketing intelligence platform",
    "lunio.ai": "Ad traffic verification software", "loopme.ai": "Mobile advertising platform",
    "infosum.com": "Data collaboration for advertisers", "snowplow.io": "Customer data platform",
    "triptease.com": "Hotel direct booking marketing software", "gleanin.com": "Community marketing platform",
    "force24.co.uk": "Marketing automation software", "wetracked.io": "Ad tracking software",
    "iamgaia.com": "Recruitment marketing software", "pagesuite.com": "Digital publishing platform",
    "coniq.com": "Retail loyalty and marketing platform", "eventsforce.com": "Event management software",
    "headbox.com": "Corporate events platform", "zap.co.uk": "Web design agency", "atarim.io": "Web agency collaboration software",
    "admitad.com": "Affiliate marketing network", "sprii.io": "Live shopping platform", "wellows.com": "AI search visibility platform",
    "datahash.com": "First-party data activation platform",
}
dr = {l.split()[0]: float(l.split()[1]) for l in open("dr_free_vs.txt")}
out = []
for r in csv.DictReader(open("../2026-09-25-video-seo/00_candidates_all.csv")):
    d = r["webDomain"]
    if d not in dr or dr[d] < 40 or d in DROP:
        continue
    seg = "A" if d in SEG_A else "B"
    svc = SEG_A.get(d) or r["serviceType"] or ""
    out.append(dict(companyName=r["companyName"].replace(" UK", "").replace(" Ltd", "").replace(" Limited", ""),
                    webDomain=d, country=r["country"], serviceType=svc, segment=seg, competitor="no",
                    competitorReason="", source="video-seo pool", domainRating=int(dr[d]), homeTitle=r["pageTitle"]))
cols = ["companyName", "webDomain", "country", "serviceType", "segment", "competitor", "competitorReason", "source", "domainRating", "homeTitle"]
w = csv.DictWriter(open("pool_vs.csv", "w", newline=""), fieldnames=cols); w.writeheader(); w.writerows(out)
from collections import Counter
print(len(out), Counter((o["segment"], o["country"]) for o in out))
