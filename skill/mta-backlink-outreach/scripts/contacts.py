"""Contact waterfall: one contact and email per company.

Order: Instantly SuperSearch, then Apollo, then Apify peakydev/leads-scraper-ppe, then the public
contact email on the company's own website. Each source only works on the companies the earlier
ones did not cover. Claude runs the first three through their MCP tools and saves what they
return as a leads CSV; this script picks one contact per company, tracks what is still missing,
and finds website emails. It never calls Instantly, Apollo or Apify itself.

    python contacts.py pick  leads.csv contacts.csv --source instantly --targets targets.csv
    python contacts.py todo  targets.csv contacts.csv -o todo.csv
    python contacts.py site  todo.csv contacts.csv [--workers 4]
    python contacts.py merge targets.csv contacts.csv -o out.csv

leads.csv needs webDomain and email, plus any of firstName, lastName, jobTitle, location,
linkedinUrl. Rows without an email are ignored.

contacts.csv holds one row per company: webDomain, firstName, lastName, jobTitle, email,
emailSource (instantly, apollo, apify, website), emailType (person or generic), linkedinUrl,
location. A company already in it is never replaced, so the waterfall order holds.

pick ranks people by role (SEO, then content, then marketing lead, growth, digital marketing,
founder or CEO, other marketing, marketing operations) and prefers someone based in the company's
country (targets.csv country column: UK, US or UAE). People outside those roles (engineers, sales,
finance) are skipped, as the company's own contact inbox reaches the right person more often.

site (needs crawl4ai, run it with <repo>/.venv-crawl/bin/python) renders the homepage and up to
three contact, about or support pages, and keeps addresses on the company's own domain,
preferring hello@, info@ and contact@ over support@. Nothing is guessed.
"""
import argparse, asyncio, csv, os, re, sys
from urllib.parse import urljoin, urlparse

COLS = ["webDomain", "firstName", "lastName", "jobTitle", "email", "emailSource", "emailType", "linkedinUrl", "location"]
OUT_COLS = ["firstName", "lastName", "jobTitle", "email", "emailSource", "emailType", "linkedinUrl"]

# Lower is better. The first matching pattern wins.
ROLES = [
    (0, r"\bseo\b|search engine|organic"),
    (1, r"content(?! design)|editorial"),
    (7, r"marketing op|mops|revops|marketing analyst|events?\b|field marketing|product marketing manager"),
    (2, r"chief marketing|\bcmo\b|(vp|vice president|head|director|lead)\b.*marketing|marketing (director|lead|head)"),
    (3, r"growth"),
    (4, r"digital marketing|brand|communications|demand gen"),
    (5, r"founder|\bceo\b|chief executive|owner|managing director"),
    (6, r"marketing"),
]
COUNTRY = {"UK": r"united kingdom|england|scotland|wales|northern ireland|london|\buk\b",
           "US": r"united states|\busa\b|\bus\b",
           "UAE": r"united arab emirates|\buae\b|dubai|abu dhabi|sharjah"}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
SKIP_LOCAL = re.compile(r"^(no-?reply|donotreply|privacy|gdpr|dpo|data|legal|abuse|security|compliance|careers?|jobs|"
                        r"recruit\w*|hr|talent|billing|accounts?|invoices?|finance|unsubscribe|postmaster|webmaster)$", re.I)
PREFER = ["hello", "info", "contact", "marketing", "partnerships", "partners", "sales", "team", "enquiries",
          "inquiries", "hi", "office", "press", "media", "support", "help"]
CONTACT_LINK = re.compile(r"contact|about|support|company|get-in-touch|reach-us", re.I)


def root(d):
    d = re.sub(r"^https?://", "", (d or "").strip().lower()).split("/")[0]
    return d[4:] if d.startswith("www.") else d


def read(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


SUFFIXES = sorted(["co.uk", "org.uk", "ltd.uk", "com.au", "co.ae", "com", "co", "io", "ai", "ae", "uk", "net", "org",
                   "me", "us", "app", "tech", "asia", "so", "to", "one", "dev", "cloud", "global", "health"],
                  key=len, reverse=True)


def brand(domain):
    """acme from acme.com, acme.co.uk or mail.acme.io."""
    d = root(domain)
    for s in SUFFIXES:
        if d.endswith("." + s):
            d = d[: -len(s) - 1]
            break
    return re.sub(r"[^a-z0-9]", "", d.split(".")[-1])


def same_company(email, domain):
    """False when the email sits on another company's domain (often a past employer).
    Brand match covers group or old domains: polyai.com for poly.ai, pexa.com.au for pexa.co.uk."""
    a, b = brand(email.split("@")[-1]), brand(domain)
    return bool(a and b) and (a in b or b in a)


def clean_name(name):
    """'Turner, Cfa' -> 'Turner', "Sumeru 'sumo'" -> 'Sumeru', drops emoji and (maiden) names."""
    n = re.sub(r"\([^)]*\)|'[^']*'|\"[^\"]*\"", " ", name or "").split(",")[0]
    n = "".join(ch for ch in n if ch.isalpha() or ch in " -.'")
    return " ".join(n.split())


def role_rank(title):
    t = (title or "").lower()
    for rank, pat in ROLES:
        if re.search(pat, t):
            return rank
    return 8


def pick(args):
    countries = {root(r["webDomain"]): r.get("country", "") for r in read(args.targets)} if args.targets else {}
    contacts = read(args.contacts)
    have = {root(r["webDomain"]) for r in contacts if r.get("email")}
    best = {}
    for r in read(args.leads):
        d, email = root(r.get("webDomain")), (r.get("email") or "").strip().lower()
        if not d or not email or d in have:
            continue
        if role_rank(r.get("jobTitle")) > args.max_rank:
            continue
        if not same_company(email, d):
            print(f"  skipped {email} for {d}: email is on another company's domain")
            continue
        away = not re.search(COUNTRY.get(countries.get(d, ""), r"$^"), (r.get("location") or "").lower())
        score = (role_rank(r.get("jobTitle")), away and bool(countries.get(d)))
        if d not in best or score < best[d][0]:
            best[d] = (score, r)
    for d, (_, r) in best.items():
        contacts.append(dict(webDomain=d, firstName=clean_name(r.get("firstName")), lastName=clean_name(r.get("lastName")),
                             jobTitle=r.get("jobTitle", ""), email=r["email"].strip().lower(), emailSource=args.source,
                             emailType="person", linkedinUrl=r.get("linkedinUrl", ""), location=r.get("location", "")))
    write(args.contacts, COLS, contacts)
    print(f"{args.source}: added {len(best)} companies, contacts.csv now has {sum(1 for r in contacts if r.get('email'))}")


def todo(args):
    have = {root(r["webDomain"]) for r in read(args.contacts) if r.get("email")}
    rows = [r for r in read(args.targets) if root(r["webDomain"]) not in have]
    write(args.out, list(rows[0].keys()) if rows else ["webDomain"], rows)
    print(f"{len(rows)} companies still without an email -> {args.out}")


def best_email(emails, domain):
    own = [e for e in emails if root(e.split("@")[1]) == domain or e.split("@")[1].endswith("." + domain)]
    own = [e for e in own if not SKIP_LOCAL.match(e.split("@")[0]) and not re.search(r"\.(png|jpe?g|gif|svg|webp)$", e)]
    if not own:
        return ""
    def key(e):
        local = e.split("@")[0]
        return PREFER.index(local) if local in PREFER else len(PREFER)
    return sorted(set(own), key=key)[0]


async def site_all(domains, workers):
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig

    cfg = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, page_timeout=45000, wait_until="domcontentloaded",
                           delay_before_return_html=2, verbose=False)
    browser = BrowserConfig(headless=True, verbose=False, extra_args=["--no-sandbox", "--disable-dev-shm-usage"])
    sem, out = asyncio.Semaphore(workers), {}

    async with AsyncWebCrawler(config=browser) as crawler:
        async def one(domain):
            async with sem:
                found, pages = set(), ["https://" + domain]
                try:
                    home = await asyncio.wait_for(crawler.arun(pages[0], config=cfg), 90)
                    if home.success:
                        found |= {e.lower() for e in EMAIL_RE.findall(home.html or "")}
                        links = [l.get("href", "") for l in (home.links or {}).get("internal", [])]
                        extra = [l for l in dict.fromkeys(links) if CONTACT_LINK.search(urlparse(l).path)][:3]
                        for link in extra:
                            r = await asyncio.wait_for(crawler.arun(urljoin(home.url, link), config=cfg), 90)
                            if r.success:
                                found |= {e.lower() for e in EMAIL_RE.findall(r.html or "")}
                except Exception as e:  # one bad site must not stop the batch
                    print(f"{domain}: {type(e).__name__}", flush=True)
                out[domain] = best_email(found, domain)
                print(f"{domain}: {out[domain] or 'none'}", flush=True)
        await asyncio.gather(*(one(d) for d in domains))
    return out


def site(args):
    contacts = read(args.contacts)
    have = {root(r["webDomain"]) for r in contacts if r.get("email")}
    domains = [d for d in dict.fromkeys(root(r["webDomain"]) for r in read(args.todo)) if d and d not in have]
    found = asyncio.run(site_all(domains, args.workers))
    for d in domains:
        if found.get(d):
            contacts.append(dict(webDomain=d, email=found[d], emailSource="website", emailType="generic"))
    write(args.contacts, COLS, contacts)
    missing = [d for d in domains if not found.get(d)]
    print(f"\nwebsite: found {len(domains) - len(missing)} of {len(domains)}. No email anywhere: {', '.join(missing) or 'none'}")


def merge(args):
    contacts = {root(r["webDomain"]): r for r in read(args.contacts) if r.get("email")}
    rows = read(args.targets)
    cols = list(rows[0].keys()) + [c for c in OUT_COLS if c not in rows[0]]
    for r in rows:
        c = dict(contacts.get(root(r["webDomain"]), {}))
        for k in ("firstName", "lastName"):
            c[k] = clean_name(c.get(k))
        r.update({k: c.get(k, "") for k in OUT_COLS})
    write(args.out, cols, rows)
    by = {}
    for r in rows:
        by[r["emailSource"] or "none"] = by.get(r["emailSource"] or "none", 0) + 1
    print(f"{args.out}: {len(rows)} rows, by source {by}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick", help="add the best person per company from a source's leads")
    p.add_argument("leads"); p.add_argument("contacts")
    p.add_argument("--source", required=True, choices=["instantly", "apollo", "apify"])
    p.add_argument("--targets", help="CSV with webDomain and country, to prefer people based there")
    p.add_argument("--max-rank", type=int, default=7, help="worst role rank to accept (8 = any title)")
    t = sub.add_parser("todo", help="list companies that still have no email")
    t.add_argument("targets"); t.add_argument("contacts"); t.add_argument("-o", "--out", required=True)
    s = sub.add_parser("site", help="find the public contact email on each remaining company's website")
    s.add_argument("todo"); s.add_argument("contacts"); s.add_argument("--workers", type=int, default=4)
    m = sub.add_parser("merge", help="add the contact columns to the targets file")
    m.add_argument("targets"); m.add_argument("contacts"); m.add_argument("-o", "--out", required=True)
    args = ap.parse_args()
    {"pick": pick, "todo": todo, "site": site, "merge": merge}[args.cmd](args)


if __name__ == "__main__":
    main()
