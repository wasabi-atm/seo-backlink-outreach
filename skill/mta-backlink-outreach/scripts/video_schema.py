"""Video schema check for Step 2c. For each site it finds out whether the homepage has a video
and whether that video has VideoObject structured data. A video with no VideoObject
(videoSchemaGap yes) switches on the fixed opening lines of the Step 5 email.

    python video_schema.py detect 01_prospects.csv video/ [--workers 4]
    python video_schema.py merge  01_prospects.csv video/

detect renders the homepage of every webDomain with crawl4ai (local Playwright Chromium, free)
and writes

  video/video_check.csv  webDomain, url, pageTitle, hasVideo (yes/no/unknown), videoPlatform, pageVideoObject, error
  video/apify_todo.csv   webDomain, url of every homepage with a video and no VideoObject in the
                         rendered page (if the render already shows one, Apify can't change the answer)

Then Claude runs the Apify actor dev00/google-rich-results-checker through the Apify MCP on each
todo URL and writes video/apify_results.csv with the columns webDomain, videoObject (TRUE or
FALSE) and apifyStatus (ok, blocked or error). This script never calls Apify itself.

merge adds hasVideo, videoSchema, videoSchemaGap and videoNote to the CSV in place. Rows that are
not in video_check.csv keep their values, so swaps can be checked in their own folder and merged
in later.

The actor reads the raw HTML only. Some players (Wistia, for one) add their VideoObject by
script, which Google does see, so the rendered page is checked too. A gap is only reported when
neither finds a VideoObject.

Runs in the crawl4ai venv (<repo>/.venv-crawl), the same one blog_crawl.py uses.
"""
import argparse, asyncio, csv, json, os, re, sys, time
from html.parser import HTMLParser

ACTOR = "dev00/google-rich-results-checker"
NEW_COLS = ["hasVideo", "videoSchema", "videoSchemaGap", "videoNote"]

# Embed URLs, matched against src and data-* attributes (never href, so plain links don't count).
PLAYER_URLS = [
    ("youtube", r"youtube(?:-nocookie)?\.com/(?:embed|v)/"),
    ("vimeo", r"player\.vimeo\.com/video/"),
    ("wistia", r"wistia\.(?:com|net)/(?:embed|medias)/"),
    ("loom", r"loom\.com/embed/"),
    ("vidyard", r"(?:play|embed)\.vidyard\.com/"),
    ("brightcove", r"players\.brightcove\.net/"),
    ("hubspot", r"hubspotvideo\.com/"),
    ("jwplayer", r"(?:cdn|content)\.jwplayer\.com/"),
    ("dailymotion", r"dailymotion\.com/(?:embed|player)"),
    ("tiktok", r"tiktok\.com/embed"),
    ("facebook", r"facebook\.com/plugins/video"),
    ("descript", r"share\.descript\.com/embed"),
    ("streamable", r"streamable\.com/[eo]/"),
    ("mux", r"stream\.mux\.com/"),
]
PLAYER_URLS = [(name, re.compile(p, re.I)) for name, p in PLAYER_URLS]
PLAYER_TAGS = {"lite-youtube": "youtube", "lite-vimeo": "vimeo", "wistia-player": "wistia",
               "mux-player": "mux", "video-js": "videojs"}
PLAYER_CLASSES = [("wistia", re.compile(r"\bwistia_(?:async_|embed\b)")),
                  ("vidyard", re.compile(r"\bvidyard-player-embed\b"))]
# Site chrome: videos here are menu or footer promos, not part of the page. <header> is left out on
# purpose, as some homepages put their hero video in one.
CHROME_TAGS = {"nav", "footer", "aside"}
VIDEO_OBJECT_RE = re.compile(r'"@?type"\s*:\s*(?:\[[^\]]*)?"(?:https?://schema\.org/)?VideoObject"')


def clean_domain(d):
    d = d.strip().lower()
    d = re.sub(r"^https?://", "", d).split("/")[0]
    return d[4:] if d.startswith("www.") else d


def is_video_object(node):
    """True if a JSON-LD tree holds a VideoObject anywhere."""
    if isinstance(node, dict):
        t = node.get("@type", node.get("type"))
        if any(isinstance(x, str) and x.rsplit("/", 1)[-1] == "VideoObject" for x in (t if isinstance(t, list) else [t])):
            return True
        return any(is_video_object(v) for v in node.values())
    if isinstance(node, list):
        return any(is_video_object(v) for v in node)
    return False


class PageScan(HTMLParser):
    """Collects video players outside the site chrome, and VideoObject markup anywhere."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.platforms, self.video_object = [], False
        self.chrome = 0     # open nav, footer and aside tags
        self.ld = None      # text of the JSON-LD script being read

    def add(self, name):
        if not self.chrome and name not in self.platforms:
            self.platforms.append(name)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag in CHROME_TAGS:
            self.chrome += 1
        elif tag == "script" and "ld+json" in a.get("type", "").lower():
            self.ld = ""
        if re.search(r"schema\.org/VideoObject\b", a.get("itemtype", "") + " " + a.get("typeof", ""), re.I) \
                or a.get("typeof", "") == "VideoObject":
            self.video_object = True
        if tag in PLAYER_TAGS:
            self.add(PLAYER_TAGS[tag])
        for k, v in a.items():
            if k == "src" or k.startswith("data-"):
                for name, pat in PLAYER_URLS:
                    if pat.search(v):
                        self.add(name)
        for name, pat in PLAYER_CLASSES:
            if pat.search(a.get("class", "")):
                self.add(name)
        # A plain <video> only counts with player controls. Without them it's a background or UI
        # animation (React sets muted as a property, so a missing muted attribute proves nothing).
        if tag == "video" and "controls" in a:
            self.add("html5")

    def handle_endtag(self, tag):
        if tag in CHROME_TAGS:
            self.chrome = max(0, self.chrome - 1)
        elif tag == "script" and self.ld is not None:
            try:
                self.video_object |= is_video_object(json.loads(self.ld))
            except ValueError:
                self.video_object |= bool(VIDEO_OBJECT_RE.search(self.ld))
            self.ld = None

    def handle_data(self, data):
        if self.ld is not None:
            self.ld += data


def scan(html):
    p = PageScan()
    p.feed(html)
    p.close()
    plats = p.platforms
    # A JS player (Wistia, Vidyard, Mux) draws its own <video> tag, so html5 only counts on its own.
    if len(plats) > 1 and "html5" in plats:
        plats = [x for x in plats if x != "html5"]
    return plats, p.video_object


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), list(r)


def write_rows(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def short_error(msg):
    msg = msg or "did not load"
    m = re.search(r"net::ERR_[A-Z_]+|Timeout \d+ms exceeded", msg)
    return m.group(0) if m else msg.strip().splitlines()[0][:150]


async def render_all(domains, workers, timeout):
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig

    # 20 screens of scrolling is plenty for a homepage and stops endless pages from stalling a worker.
    base = dict(cache_mode=CacheMode.BYPASS, page_timeout=45000, scan_full_page=True, scroll_delay=0.2,
                max_scroll_steps=20, verbose=False)
    fast = CrawlerRunConfig(wait_until="domcontentloaded", delay_before_return_html=3, **base)
    # Players that add VideoObject by script can be slow to start when several pages render at
    # once, so a video with no VideoObject is rendered again, alone and slowly, before it counts.
    slow = CrawlerRunConfig(wait_until="load", delay_before_return_html=10, **base)
    browser = BrowserConfig(headless=True, verbose=False, extra_args=["--no-sandbox", "--disable-dev-shm-usage"])
    out = {}

    async with AsyncWebCrawler(config=browser) as crawler:
        async def one(domain, cfg, sem, label=""):
            """Renders one homepage and returns its video_check row."""
            async with sem:
                url = "https://" + domain
                t, row = time.time(), dict(webDomain=domain, url=url, pageTitle="", hasVideo="unknown",
                                           videoPlatform="", pageVideoObject="", error="")
                try:
                    r = await asyncio.wait_for(crawler.arun(url, config=cfg), timeout)
                    if not r.success or (r.status_code or 200) >= 400:
                        row["error"] = f"HTTP {r.status_code}" if r.status_code else short_error(r.error_message)
                    else:
                        plats, vo = scan(r.html or "")
                        title = ((r.metadata or {}).get("title") or "").strip()
                        row.update(pageTitle=" ".join(title.split())[:150], hasVideo="yes" if plats else "no",
                                   videoPlatform=", ".join(plats), pageVideoObject="yes" if vo else "no")
                except asyncio.TimeoutError:
                    row["error"] = f"timed out after {timeout}s"
                except Exception as e:  # one bad page must not stop the batch
                    row["error"] = short_error(f"{type(e).__name__}: {e}")
                print(f"{label}{domain}: video {row['hasVideo']} {row['videoPlatform']} "
                      f"{'VideoObject ' if row['pageVideoObject'] == 'yes' else ''}{time.time() - t:.0f}s {row['error']}", flush=True)
                return row

        sem = asyncio.Semaphore(workers)
        for row in await asyncio.gather(*(one(d, fast, sem) for d in domains)):
            out[row["webDomain"]] = row
        again = [d for d in domains if out[d]["hasVideo"] == "yes" and out[d]["pageVideoObject"] == "no"]
        if again:
            print(f"\nRechecking {len(again)} homepages with a video but no VideoObject, slowly:", flush=True)
            sem = asyncio.Semaphore(min(2, workers))
            # A recheck can only add a VideoObject it finds; it never drops the video from the first pass.
            for row in await asyncio.gather(*(one(d, slow, sem, "recheck ") for d in again)):
                if row["pageVideoObject"] == "yes":
                    out[row["webDomain"]]["pageVideoObject"] = "yes"
    return [out[d] for d in domains]


def detect(args):
    domains = []
    for r in read_rows(args.csv)[1]:
        d = clean_domain(r.get("webDomain") or "")
        if d and d not in domains:
            domains.append(d)
    os.makedirs(args.out_dir, exist_ok=True)
    rows = asyncio.run(render_all(domains, args.workers, args.timeout))
    write_rows(os.path.join(args.out_dir, "video_check.csv"),
               ["webDomain", "url", "pageTitle", "hasVideo", "videoPlatform", "pageVideoObject", "error"], rows)
    todo = [r for r in rows if r["hasVideo"] == "yes" and r["pageVideoObject"] == "no"]
    write_rows(os.path.join(args.out_dir, "apify_todo.csv"), ["webDomain", "url"], todo)

    failed = [r for r in rows if r["hasVideo"] == "unknown"]
    print(f"\nRendered {len(rows)} homepages: {sum(r['hasVideo'] == 'yes' for r in rows)} with a video "
          f"({len(todo)} of them with no VideoObject, for Apify), "
          f"{sum(r['hasVideo'] == 'no' for r in rows)} without, {len(failed)} did not load.")
    for r in failed:
        print(f"  {r['webDomain']}: {r['error']}")
    if todo:
        print(f"\nNext: run {ACTOR} through the Apify MCP on the {len(todo)} URLs in apify_todo.csv, write "
              f"apify_results.csv (webDomain,videoObject,apifyStatus), then run: video_schema.py merge")
    else:
        print("\nNo homepage has a video, so there is nothing for Apify. Run: video_schema.py merge")


def merge(args):
    check_file = os.path.join(args.out_dir, "video_check.csv")
    if not os.path.exists(check_file):
        sys.exit(f"{check_file} is missing. Run video_schema.py detect first.")
    checks = {r["webDomain"]: r for r in read_rows(check_file)[1]}
    res_file = os.path.join(args.out_dir, "apify_results.csv")
    results = {}
    if os.path.exists(res_file):
        for r in read_rows(res_file)[1]:
            results[clean_domain(r.get("webDomain") or "")] = ((r.get("apifyStatus") or "").strip().lower(),
                                                              (r.get("videoObject") or "").strip().upper())

    cols, rows = read_rows(args.csv)
    cols += [c for c in NEW_COLS if c not in cols]
    counts = {}
    for row in rows:
        domain = clean_domain(row.get("webDomain") or "")
        vc = checks.get(domain)
        if not vc:
            continue  # not in this check, keep whatever the row already has
        has, plats = vc["hasVideo"], vc["videoPlatform"]
        rendered = vc["pageVideoObject"] == "yes"
        status, vo = results.get(domain, ("", ""))
        if status == "ok" and vo not in ("TRUE", "FALSE"):
            status = "error"
        problem = {"": "Apify not run on this site", "blocked": "Apify could not load the page",
                   "error": "no usable Apify result"}.get(status, f"unknown apifyStatus {status!r}")
        notes = []
        if has == "unknown":
            schema, gap = "", "unknown"
            notes.append(f"homepage did not load for the video check ({vc['error']})")
        elif has == "no":
            schema, gap = ("TRUE" if rendered else "FALSE"), "no"
            notes.append("no video on the homepage, so Apify was skipped")
        elif status not in ("ok", "blocked") and not rendered:
            schema, gap = "", "unknown"
            notes.append(problem)
        else:
            # "blocked" falls back to the rendered page, which is what Google sees once it renders.
            schema = "TRUE" if vo == "TRUE" or rendered else "FALSE"
            gap = "no" if schema == "TRUE" else "yes"
            if rendered and status == "":
                notes.append(f"{plats} video with VideoObject in the rendered page, so Apify was skipped")
            elif status != "ok":
                notes.append(problem + "; schema read from the rendered page")
            elif rendered and vo == "FALSE":
                notes.append(f"VideoObject is added by script ({plats}): Apify reads raw HTML and missed it, Google renders it")
            if gap == "yes":
                notes.append(f"{plats} video with no VideoObject schema")
        row.update(hasVideo=has, videoSchema=schema, videoSchemaGap=gap, videoNote="; ".join(notes))
        counts[gap] = counts.get(gap, 0) + 1
    write_rows(args.csv, cols, rows)

    print(f"Updated {args.csv}: videoSchemaGap yes {counts.get('yes', 0)}, no {counts.get('no', 0)}, "
          f"unknown {counts.get('unknown', 0)}.")
    for row in rows:
        if row.get("videoSchemaGap") in ("yes", "unknown") and clean_domain(row.get("webDomain") or "") in checks:
            print(f"  {row['videoSchemaGap']:7} {row.get('webDomain', '')}: {row['videoNote']}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("detect", help="render each homepage and find videos and VideoObject markup")
    d.add_argument("csv")
    d.add_argument("out_dir")
    d.add_argument("--workers", type=int, default=4, help="pages rendered at once")
    d.add_argument("--timeout", type=int, default=90, help="seconds per page")
    m = sub.add_parser("merge", help="combine the render and the Apify results into the CSV")
    m.add_argument("csv")
    m.add_argument("out_dir")
    args = ap.parse_args()
    detect(args) if args.cmd == "detect" else merge(args)


if __name__ == "__main__":
    main()
