"""Video schema check for Step 4b. For each picked article it finds out whether the page has a
video and whether that video carries VideoObject structured data. A video with no VideoObject
means the SEO work on the page was not finished, which Step 5 can point out in the email.

    python video_schema.py detect 03_backlink_targets.csv video/ [--workers 4]
    python video_schema.py merge  03_backlink_targets.csv video/

detect renders every articleUrl with crawl4ai (local Playwright Chromium, free) and writes

  video/video_check.csv  articleUrl, hasVideo (yes/no/unknown), videoPlatform, pageVideoObject, error
  video/apify_todo.csv   articleUrl of every page with a video, for the Apify check

If APIFY_TOKEN is set, detect then runs the Apify actor dev00/google-rich-results-checker
($0.002 per URL) on each todo URL itself and writes video/apify_runs.csv. Without a token, run
the actor through the Apify MCP (one call per URL) and write video/apify_runs.csv yourself, with
the columns articleUrl,datasetId.

merge reads each actor result by datasetId (readable by ID, no token needed) and adds these
columns to the CSV in place: hasVideo, videoPlatform, videoSchema, videoSchemaGap, videoNote,
richResultsUrl.

The actor reads the raw HTML only. Some players (Wistia, for one) add their VideoObject by
script, which Google does see, so the rendered page is checked too. A gap is only reported
when neither finds a VideoObject.

Runs in the crawl4ai venv (<repo>/.venv-crawl), the same one blog_crawl.py uses.
"""
import argparse, asyncio, csv, json, os, re, sys, time
import urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.parse import quote

ACTOR = "dev00~google-rich-results-checker"
API = "https://api.apify.com/v2"
RICH_TEST = "https://search.google.com/test/rich-results?url="
NEW_COLS = ["hasVideo", "videoPlatform", "videoSchema", "videoSchemaGap", "videoNote", "richResultsUrl"]

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
# Site chrome: videos here are site-wide promos, not part of the article.
CHROME_TAGS = {"nav", "footer", "aside"}
VIDEO_OBJECT_RE = re.compile(r'"@?type"\s*:\s*(?:\[[^\]]*)?"(?:https?://schema\.org/)?VideoObject"')


def is_video_object(node):
    """True if a JSON-LD tree (or an Apify detected item) holds a VideoObject anywhere."""
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
        self.chrome = self.content = 0
        self.headers = []   # per open <header>: whether it counted as chrome
        self.ld = None      # text of the JSON-LD script being read

    def add(self, name):
        if not self.chrome and name not in self.platforms:
            self.platforms.append(name)

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag in CHROME_TAGS:
            self.chrome += 1
        elif tag in ("article", "main"):
            self.content += 1
        elif tag == "header":
            # A <header> outside the article is the site header; inside it, the post's own header.
            self.headers.append(self.content == 0)
            self.chrome += self.headers[-1]
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
        # Autoplaying, muted, looping clips with no controls are background or GIF-style, not videos.
        if tag == "video" and not ({"autoplay", "muted", "loop"} <= a.keys() and "controls" not in a):
            self.add("html5")

    def handle_endtag(self, tag):
        if tag in CHROME_TAGS:
            self.chrome = max(0, self.chrome - 1)
        elif tag in ("article", "main"):
            self.content = max(0, self.content - 1)
        elif tag == "header" and self.headers:
            self.chrome = max(0, self.chrome - self.headers.pop())
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


def article_urls(path):
    _, rows = read_rows(path)
    seen = []
    for r in rows:
        u = (r.get("articleUrl") or "").strip()
        if u.startswith("http") and u not in seen:
            seen.append(u)
    return seen


def short_error(msg):
    msg = msg or "did not load"
    m = re.search(r"net::ERR_[A-Z_]+|Timeout \d+ms exceeded", msg)
    return m.group(0) if m else msg.strip().splitlines()[0][:150]


async def render_all(urls, workers, timeout):
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig

    base = dict(cache_mode=CacheMode.BYPASS, page_timeout=45000, scan_full_page=True, scroll_delay=0.2, verbose=False)
    fast = CrawlerRunConfig(wait_until="domcontentloaded", delay_before_return_html=3, **base)
    # Players that add VideoObject by script can be slow to start when several pages render at
    # once, so a video with no VideoObject is rendered again, alone and slowly, before it counts.
    slow = CrawlerRunConfig(wait_until="load", delay_before_return_html=10, **base)
    browser = BrowserConfig(headless=True, verbose=False, extra_args=["--no-sandbox", "--disable-dev-shm-usage"])
    out = {}

    async with AsyncWebCrawler(config=browser) as crawler:
        async def one(url, cfg, sem, label=""):
            """Renders one page and returns its video_check row."""
            async with sem:
                t, row = time.time(), dict(articleUrl=url, hasVideo="unknown", videoPlatform="", pageVideoObject="", error="")
                try:
                    r = await asyncio.wait_for(crawler.arun(url, config=cfg), timeout)
                    if not r.success or (r.status_code or 200) >= 400:
                        row["error"] = f"HTTP {r.status_code}" if r.status_code else short_error(r.error_message)
                    else:
                        plats, vo = scan(r.html or "")
                        row.update(hasVideo="yes" if plats else "no", videoPlatform=", ".join(plats),
                                   pageVideoObject="yes" if vo else "no")
                except asyncio.TimeoutError:
                    row["error"] = f"timed out after {timeout}s"
                except Exception as e:  # one bad page must not stop the batch
                    row["error"] = short_error(f"{type(e).__name__}: {e}")
                print(f"{label}{url}: video {row['hasVideo']} {row['videoPlatform']} "
                      f"{'VideoObject ' if row['pageVideoObject'] == 'yes' else ''}{time.time() - t:.0f}s {row['error']}", flush=True)
                return row

        sem = asyncio.Semaphore(workers)
        for row in await asyncio.gather(*(one(u, fast, sem) for u in urls)):
            out[row["articleUrl"]] = row
        again = [u for u in urls if out[u]["hasVideo"] == "yes" and out[u]["pageVideoObject"] == "no"]
        if again:
            print(f"\nRechecking {len(again)} video pages with no VideoObject, slowly:", flush=True)
            sem = asyncio.Semaphore(min(2, workers))
            # A recheck can only add a VideoObject it finds; it never drops the video from the first pass.
            for row in await asyncio.gather(*(one(u, slow, sem, "recheck ") for u in again)):
                if row["pageVideoObject"] == "yes":
                    out[row["articleUrl"]]["pageVideoObject"] = "yes"
    return [out[u] for u in urls]


def api(path, body=None, token=""):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def run_actor(url, token):
    """Starts one actor run and waits for it. Returns the dataset id, or '' on failure."""
    try:
        run = api(f"/acts/{ACTOR}/runs?waitForFinish=60&maxTotalChargeUsd=0.05", {"url": url}, token)["data"]
        for _ in range(3):  # Apify waits 60 seconds at most per request
            if run["status"] not in ("READY", "RUNNING"):
                break
            run = api(f"/actor-runs/{run['id']}?waitForFinish=60", token=token)["data"]
        print(f"apify {run['status']}: {url}", flush=True)
        return run["defaultDatasetId"] if run["status"] == "SUCCEEDED" else ""
    except (urllib.error.URLError, KeyError, ValueError) as e:
        print(f"apify failed: {url}: {e}", flush=True)
        return ""


def detect(args):
    urls = article_urls(args.csv)
    os.makedirs(args.out_dir, exist_ok=True)
    rows = asyncio.run(render_all(urls, args.workers, args.timeout))
    write_rows(os.path.join(args.out_dir, "video_check.csv"),
               ["articleUrl", "hasVideo", "videoPlatform", "pageVideoObject", "error"], rows)
    todo = [r["articleUrl"] for r in rows if r["hasVideo"] == "yes"]
    write_rows(os.path.join(args.out_dir, "apify_todo.csv"), ["articleUrl"], [{"articleUrl": u} for u in todo])

    failed = [r for r in rows if r["hasVideo"] == "unknown"]
    print(f"\nRendered {len(rows)} articles: {len(todo)} with a video, "
          f"{sum(r['hasVideo'] == 'no' for r in rows)} without, {len(failed)} did not load.")
    for r in failed:
        print(f"  {r['articleUrl']}: {r['error']}")

    token = os.environ.get("APIFY_TOKEN", "").strip()
    runs_file = os.path.join(args.out_dir, "apify_runs.csv")
    if not todo:
        write_rows(runs_file, ["articleUrl", "datasetId"], [])
    elif token:
        with ThreadPoolExecutor(args.workers) as pool:
            ids = list(pool.map(lambda u: run_actor(u, token), todo))
        write_rows(runs_file, ["articleUrl", "datasetId"],
                   [dict(articleUrl=u, datasetId=i) for u, i in zip(todo, ids) if i])
        print(f"Apify: {sum(bool(i) for i in ids)} of {len(todo)} checked. Now run: video_schema.py merge")
    else:
        print(f"No APIFY_TOKEN. Run {ACTOR.replace('~', '/')} through the Apify MCP for the {len(todo)} URLs in "
              f"apify_todo.csv, write apify_runs.csv (articleUrl,datasetId), then run: video_schema.py merge")


def apify_result(dataset_id, token):
    """Returns (status, has VideoObject, rich results URL, problem) for one actor run.
    status is "ok", "blocked" (the actor could not load the page) or "error" (no usable result)."""
    try:
        items = api(f"/datasets/{dataset_id}/items?format=json&clean=true", token=token)
    except (urllib.error.URLError, ValueError) as e:
        return "error", False, "", f"could not read Apify dataset {dataset_id}: {e}"
    if not items:
        return "error", False, "", "Apify returned no result"
    it = items[0]
    rich = it.get("google_web_ui_url", "")
    if it.get("http_status") != 200 or it.get("crawl_status") != "Successful":
        return "blocked", False, rich, f"Apify could not load the page (HTTP {it.get('http_status')}, {it.get('crawl_status')})"
    return "ok", is_video_object(it.get("detected_items") or []), rich, ""


def merge(args):
    token = os.environ.get("APIFY_TOKEN", "").strip()
    check_file = os.path.join(args.out_dir, "video_check.csv")
    if not os.path.exists(check_file):
        sys.exit(f"{check_file} is missing. Run video_schema.py detect first.")
    checks = {r["articleUrl"]: r for r in read_rows(check_file)[1]}
    runs_file = os.path.join(args.out_dir, "apify_runs.csv")
    runs = {r["articleUrl"]: r["datasetId"].strip() for r in read_rows(runs_file)[1]
            if r.get("datasetId", "").strip()} if os.path.exists(runs_file) else {}
    apify = {u: apify_result(d, token) for u, d in runs.items()}

    cols, rows = read_rows(args.csv)
    cols += [c for c in NEW_COLS if c not in cols]
    counts = {}
    for row in rows:
        url = (row.get("articleUrl") or "").strip()
        vc = checks.get(url)
        if not vc:
            row.update({c: "" for c in NEW_COLS})
            continue
        has, plats = vc["hasVideo"], vc["videoPlatform"]
        rendered = vc["pageVideoObject"] == "yes"
        status, found, rich, problem = apify.get(url, ("", False, "", "Apify not run on this URL"))
        notes = []
        if has == "unknown":
            schema, gap = "", "unknown"
            notes.append(f"page did not load for the video check ({vc['error']})")
        elif has == "no":
            schema, gap = ("TRUE" if rendered else "FALSE"), "no"
            notes.append("no video on the page, so Apify was skipped")
        elif status in ("", "error") and not rendered:
            schema, gap = "", "unknown"
            notes.append(problem)
        else:
            # "blocked" falls back to the rendered page, which is what Google sees once it renders.
            schema = "TRUE" if found or rendered else "FALSE"
            gap = "no" if schema == "TRUE" else "yes"
            if status != "ok":
                notes.append(problem + "; schema read from the rendered page")
            elif rendered and not found:
                notes.append(f"VideoObject is added by script ({plats}): Apify reads raw HTML and missed it, Google renders it")
            if gap == "yes":
                notes.append(f"{plats} video with no VideoObject schema")
        row.update(hasVideo=has, videoPlatform=plats, videoSchema=schema, videoSchemaGap=gap,
                   videoNote="; ".join(notes), richResultsUrl=rich or (RICH_TEST + quote(url, safe="")))
        counts[gap] = counts.get(gap, 0) + 1
    write_rows(args.csv, cols, rows)

    print(f"Updated {args.csv}: videoSchemaGap yes {counts.get('yes', 0)}, no {counts.get('no', 0)}, "
          f"unknown {counts.get('unknown', 0)}.")
    for row in rows:
        if row.get("videoSchemaGap") in ("yes", "unknown"):
            print(f"  {row['videoSchemaGap']:7} {row.get('webDomain', '')}: {row['videoNote']}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("detect", help="render each articleUrl, find videos, run Apify if APIFY_TOKEN is set")
    d.add_argument("csv")
    d.add_argument("out_dir")
    d.add_argument("--workers", type=int, default=4, help="pages rendered at once")
    d.add_argument("--timeout", type=int, default=90, help="seconds per page")
    m = sub.add_parser("merge", help="read the Apify results and add the video columns to the CSV")
    m.add_argument("csv")
    m.add_argument("out_dir")
    args = ap.parse_args()
    detect(args) if args.cmd == "detect" else merge(args)


if __name__ == "__main__":
    main()
