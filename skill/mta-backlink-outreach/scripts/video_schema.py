"""Video schema check for Step 2c. For each site it finds out whether the homepage has a video
and whether that video has VideoObject structured data. A video with no VideoObject
(videoSchemaGap yes) switches on the fixed opening lines of the Step 5 email.

    python video_schema.py detect  01_prospects.csv video/ [--workers 4]
    python video_schema.py apify   video/apify_todo.csv video/ [--workers 16]    (needs APIFY_TOKEN)
    python video_schema.py merge   01_prospects.csv video/
    python video_schema.py players video/apify_todo.csv video/ [--workers 6]    (Vimeo check)
    python video_schema.py recheck some.csv video/ [--workers 4]                (deep render only)

detect renders the homepage of every webDomain with crawl4ai (local Playwright Chromium, free)
and writes

  video/video_check.csv  webDomain, url, pageTitle, hasVideo (yes/no/unknown), videoPlatform,
                         pageVideoObject, iframeVideoObject, error
  video/apify_todo.csv   webDomain, url of every homepage with a video and no VideoObject in the
                         rendered page (if the render already shows one, Apify can't change the answer)

A homepage with a video but no VideoObject gets a deep render before it counts. It renders the page
the way Google does (Googlebot phone user agent, a tall viewport, no scrolling or clicking: a
VideoObject that only appears after scrolling, as on JumpCloud, is not seen by Google), waits for
the network to settle, then reads structured data in the page itself and, apart from that, in every
iframe. Google only counts the page's own markup: a VideoObject inside an
embedded player's iframe (Wistia's iframe embed has one) does not make the page eligible, so it is
recorded in iframeVideoObject and does not close the gap. recheck runs the deep render on its own.

Then the Apify actor dev00/google-rich-results-checker (raw HTML, one URL per run) checks each todo
URL. With APIFY_TOKEN set in the environment, `apify` runs them through the Apify API in parallel,
saves each full result to video/apify_raw/<domain>.json and writes video/apify_results.csv
(webDomain, videoObject TRUE/FALSE, apifyStatus ok/blocked/error, detectedTypes, richResultsUrl).
The token is only read from the environment, never written anywhere. Without a token, Claude runs
the actor through the Apify MCP and writes apify_results.csv itself.

Vimeo: a Vimeo player page carries its own VideoObject, and Google's Rich Results Test counts it for
the host page when the player is visible at load (checked on Alpheya and Tribepad, 25 Sep 2026). A
hero loop (background=1, or autoplay and muted) also shows up, but its schema does not count for
the pitch (Netacea), and a hidden player (a closed pop-up) is not counted by Google (Altruistiq).
YouTube and Vidyard embeds carry no VideoObject, and Google did not count Posit's Wistia iframe.
`players` renders each homepage the way Google does (Googlebot phone user agent, tall viewport, no
scrolling), lists the video iframes that load and writes video/players.csv with vimeoVerdict: real
vimeo player, vimeo hero only, vimeo hidden only or no vimeo at load. It reads iframe URLs only, so
it works even where the ISP blocks player.vimeo.com (Indonesia does). merge then treats a real
Vimeo player as schema present (no gap), and a hero-only page as "check".

merge adds hasVideo, videoSchema, videoSchemaGap and videoNote to the CSV in place. Rows that are
not in video_check.csv keep their values, so swaps can be checked in their own folder and merged
in later.

The actor reads the raw HTML only. Some players (Wistia, for one) add their VideoObject by
script, which Google does see, so the rendered page is checked too. A gap is only reported when
neither finds a VideoObject.

Runs in the crawl4ai venv (<repo>/.venv-crawl), the same one blog_crawl.py uses.
"""
import argparse, asyncio, csv, json, os, re, sys, time
import urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.parse import quote

ACTOR = "dev00/google-rich-results-checker"
API = "https://api.apify.com/v2"
RICH_TEST = "https://search.google.com/test/rich-results?url="
GOOGLEBOT = ("Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/128.0.6613.119 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
CHECK_COLS = ["webDomain", "url", "pageTitle", "hasVideo", "videoPlatform", "pageVideoObject", "iframeVideoObject", "error"]
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


DEEP_JS = r"""() => {
  const ld = [], types = [];
  for (const s of document.querySelectorAll('script[type*="ld+json" i]')) ld.push(s.textContent || '');
  for (const e of document.querySelectorAll('[itemtype],[typeof]'))
    types.push((e.getAttribute('itemtype') || '') + ' ' + (e.getAttribute('typeof') || ''));
  return {ld, types};
}"""


def markup_has_video_object(found):
    for text in found.get("ld", []):
        try:
            if is_video_object(json.loads(text)):
                return True
        except ValueError:
            if VIDEO_OBJECT_RE.search(text):
                return True
    return any(re.search(r"schema\.org/VideoObject\b|(^|\s)VideoObject(\s|$)", t) for t in found.get("types", []))


async def deep_all(domains, workers, timeout):
    """Returns {domain: {pageVideoObject, iframeVideoObject, error}} from a slow, thorough render."""
    from playwright.async_api import async_playwright

    sem, out = asyncio.Semaphore(workers), {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        ctx = await browser.new_context(user_agent=GOOGLEBOT, viewport={"width": 412, "height": 8000}, is_mobile=True, has_touch=True)

        async def look(page, domain):
            await page.goto("https://" + domain, wait_until="domcontentloaded", timeout=45000)
            try:
                await page.wait_for_load_state("networkidle", timeout=20000)
            except Exception:
                pass  # busy pages never go idle; carry on
            await page.wait_for_timeout(8000)  # script-added schema (Wistia) needs a few seconds
            main = markup_has_video_object(await page.main_frame.evaluate(DEEP_JS))
            inner = False
            for f in page.frames:
                if f is not page.main_frame and not inner:
                    try:
                        inner = markup_has_video_object(await f.evaluate(DEEP_JS))
                    except Exception:
                        pass  # cross-origin frames that refuse evaluation
            return main, inner

        async def one(domain):
            async with sem:
                t, row, page = time.time(), dict(pageVideoObject="", iframeVideoObject="", error=""), await ctx.new_page()
                try:
                    main, inner = await asyncio.wait_for(look(page, domain), timeout)
                    row.update(pageVideoObject="yes" if main else "no", iframeVideoObject="yes" if inner else "no")
                except asyncio.TimeoutError:
                    row["error"] = f"timed out after {timeout}s"
                except Exception as e:  # one bad page must not stop the batch
                    row["error"] = short_error(f"{type(e).__name__}: {e}")
                finally:
                    await page.close()
                print(f"deep {domain}: page VideoObject {row['pageVideoObject'] or '?'}, iframe "
                      f"{row['iframeVideoObject'] or '?'} {time.time() - t:.0f}s {row['error']}", flush=True)
                out[domain] = row

        await asyncio.gather(*(one(d) for d in domains))
        await browser.close()
    return out


async def render_all(domains, workers, timeout):
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig

    # 20 screens of scrolling is plenty for a homepage and stops endless pages from stalling a worker.
    base = dict(cache_mode=CacheMode.BYPASS, page_timeout=45000, scan_full_page=True, scroll_delay=0.2,
                max_scroll_steps=20, verbose=False)
    fast = CrawlerRunConfig(wait_until="domcontentloaded", delay_before_return_html=3, **base)
    browser = BrowserConfig(headless=True, verbose=False, extra_args=["--no-sandbox", "--disable-dev-shm-usage"])
    out = {}

    async with AsyncWebCrawler(config=browser) as crawler:
        async def one(domain, cfg, sem, label=""):
            """Renders one homepage and returns its video_check row."""
            async with sem:
                url = "https://" + domain
                t, row = time.time(), dict(webDomain=domain, url=url, pageTitle="", hasVideo="unknown",
                                           videoPlatform="", pageVideoObject="", iframeVideoObject="", error="")
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
    # Players that add VideoObject by script can be slow to start, so a video with no VideoObject
    # gets the deep render before it counts. It can only add a VideoObject; it never drops the video.
    again = [d for d in domains if out[d]["hasVideo"] == "yes" and out[d]["pageVideoObject"] == "no"]
    if again:
        print(f"\nDeep render of {len(again)} homepages with a video but no VideoObject:", flush=True)
        for d, r in (await deep_all(again, min(3, workers), 120)).items():
            if r["pageVideoObject"] == "yes":
                out[d]["pageVideoObject"] = "yes"
            out[d]["iframeVideoObject"] = r["iframeVideoObject"]
    return [out[d] for d in domains]


def detect(args):
    domains = []
    for r in read_rows(args.csv)[1]:
        d = clean_domain(r.get("webDomain") or "")
        if d and d not in domains:
            domains.append(d)
    os.makedirs(args.out_dir, exist_ok=True)
    rows = asyncio.run(render_all(domains, args.workers, args.timeout))
    write_rows(os.path.join(args.out_dir, "video_check.csv"), CHECK_COLS, rows)
    todo = [r for r in rows if r["hasVideo"] == "yes" and r["pageVideoObject"] == "no"]
    write_rows(os.path.join(args.out_dir, "apify_todo.csv"), ["webDomain", "url"], todo)

    failed = [r for r in rows if r["hasVideo"] == "unknown"]
    print(f"\nRendered {len(rows)} homepages: {sum(r['hasVideo'] == 'yes' for r in rows)} with a video "
          f"({len(todo)} of them with no VideoObject, for Apify), "
          f"{sum(r['hasVideo'] == 'no' for r in rows)} without, {len(failed)} did not load.")
    for r in failed:
        print(f"  {r['webDomain']}: {r['error']}")
    if todo:
        print(f"\nNext: video_schema.py apify {args.out_dir}/apify_todo.csv {args.out_dir} (with APIFY_TOKEN set), or "
              f"run {ACTOR} through the Apify MCP on the {len(todo)} URLs and write apify_results.csv; then merge")
    else:
        print("\nNo homepage has a video, so there is nothing for Apify. Run: video_schema.py merge")


def recheck(args):
    """Deep render of every webDomain in a CSV; updates video_check.csv in the output folder."""
    domains = list(dict.fromkeys(d for d in (clean_domain(r.get("webDomain") or "") for r in read_rows(args.csv)[1]) if d))
    os.makedirs(args.out_dir, exist_ok=True)
    check_file = os.path.join(args.out_dir, "video_check.csv")
    rows = {r["webDomain"]: r for r in read_rows(check_file)[1]} if os.path.exists(check_file) else {}
    for d, r in asyncio.run(deep_all(domains, args.workers, args.timeout)).items():
        row = rows.setdefault(d, dict(webDomain=d, url="https://" + d, hasVideo="unknown"))
        if r["error"]:
            row["error"] = row.get("error") or r["error"]
            continue
        if row.get("pageVideoObject") != "yes":
            row["pageVideoObject"] = r["pageVideoObject"]
        row["iframeVideoObject"] = r["iframeVideoObject"]
    write_rows(check_file, CHECK_COLS, rows.values())
    print(f"\nUpdated {check_file}: page VideoObject in {sum(r.get('pageVideoObject') == 'yes' for r in rows.values())}, "
          f"only in an iframe in {sum(r.get('pageVideoObject') != 'yes' and r.get('iframeVideoObject') == 'yes' for r in rows.values())}.")


PLAYER_IFRAME = re.compile(r"vimeo|youtube|wistia|vidyard|loom\.com|brightcove|hubspotvideo|jwplayer|mux\.com|dailymotion", re.I)
IFRAMES_JS = """() => [...document.querySelectorAll('iframe')].map(e => ({src: e.getAttribute('src') || '', w: e.offsetWidth, h: e.offsetHeight}))"""


def classify_vimeo(players):
    """players: '<url> (WxH)' or '<url> (hidden)' for each video iframe loaded without scrolling."""
    vimeo = [p for p in players if "vimeo" in p]
    visible = [p for p in vimeo if "(hidden)" not in p]
    hero = lambda p: "background=1" in p or ("autoplay=1" in p and "muted=1" in p)
    if any(not hero(p) for p in visible):
        return "real vimeo player"
    if visible:
        return "vimeo hero only"
    return "vimeo hidden only" if vimeo else "no vimeo at load"


async def players_all(domains, workers):
    from playwright.async_api import async_playwright

    sem, out = asyncio.Semaphore(workers), {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])

        async def one(d):
            async with sem:
                t = time.time()
                ctx = await browser.new_context(user_agent=GOOGLEBOT, viewport={"width": 412, "height": 8000}, is_mobile=True, has_touch=True)
                page, row = await ctx.new_page(), dict(webDomain=d, vimeoVerdict="", players="", error="")
                try:
                    await page.goto("https://" + d, wait_until="domcontentloaded", timeout=45000)
                    try:
                        await page.wait_for_load_state("networkidle", timeout=15000)
                    except Exception:
                        pass  # busy pages never go idle
                    await page.wait_for_timeout(5000)
                    listed = [f["src"][:160] + (f" ({f['w']}x{f['h']})" if f["w"] else " (hidden)")
                              for f in await page.evaluate(IFRAMES_JS) if PLAYER_IFRAME.search(f["src"])]
                    row.update(players="; ".join(listed), vimeoVerdict=classify_vimeo(listed))
                except Exception as e:  # one bad page must not stop the batch
                    row["error"] = short_error(f"{type(e).__name__}: {e}")
                finally:
                    await ctx.close()
                print(f"players {d}: {row['vimeoVerdict'] or row['error']} {time.time() - t:.0f}s", flush=True)
                out[d] = row

        await asyncio.gather(*(one(d) for d in domains))
        await browser.close()
    return [out[d] for d in domains]


def players(args):
    domains = list(dict.fromkeys(d for d in (clean_domain(r.get("webDomain") or "") for r in read_rows(args.csv)[1]) if d))
    os.makedirs(args.out_dir, exist_ok=True)
    rows = asyncio.run(players_all(domains, args.workers))
    path = os.path.join(args.out_dir, "players.csv")
    keep = [r for r in read_rows(path)[1] if r["webDomain"] not in domains] if os.path.exists(path) else []
    write_rows(path, ["webDomain", "vimeoVerdict", "players", "error"], keep + rows)
    counts = {}
    for r in rows:
        counts[r["vimeoVerdict"] or "error"] = counts.get(r["vimeoVerdict"] or "error", 0) + 1
    print(f"\nWrote {path}: {counts}")


def types_in(node, found):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("@type", "type"):
                for t in (v if isinstance(v, list) else [v]):
                    if isinstance(t, str):
                        found.add(t.rsplit("/", 1)[-1])
            types_in(v, found)
    elif isinstance(node, list):
        for v in node:
            types_in(v, found)
    return found


def apify_api(args):
    """Runs the actor once per URL through the Apify API, many at a time."""
    token = os.environ.get("APIFY_TOKEN", "").strip()
    if not token:
        sys.exit("APIFY_TOKEN is not set. Set it in the environment, or run the actor through the Apify MCP instead.")
    targets = {}
    for r in read_rows(args.csv)[1]:
        d = clean_domain(r.get("webDomain") or "")
        if d:
            targets.setdefault(d, (r.get("url") or "").strip() or "https://" + d)
    raw_dir = os.path.join(args.out_dir, "apify_raw")
    os.makedirs(raw_dir, exist_ok=True)
    actor = ACTOR.replace("/", "~")

    def run(item):
        domain, url = item
        row = dict(webDomain=domain, videoObject="", apifyStatus="error", detectedTypes="", richResultsUrl=RICH_TEST + quote(url, safe=""))
        req = urllib.request.Request(
            f"{API}/acts/{actor}/run-sync-get-dataset-items?memory=256&timeout=180&maxTotalChargeUsd=0.02",
            data=json.dumps({"url": url}).encode(), headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req, timeout=240) as resp:
                items = json.load(resp)
        except (urllib.error.URLError, ValueError, TimeoutError) as e:
            print(f"apify {domain}: {short_error(str(e))}", flush=True)
            return row
        with open(os.path.join(raw_dir, domain + ".json"), "w", encoding="utf-8") as f:
            json.dump(items, f, indent=1)
        if not items:
            return row
        it = items[0]
        row["richResultsUrl"] = it.get("google_web_ui_url") or row["richResultsUrl"]
        row["detectedTypes"] = ", ".join(sorted(types_in(it.get("detected_items") or [], set())))
        if it.get("http_status") == 200 and it.get("crawl_status") == "Successful":
            row.update(apifyStatus="ok", videoObject="TRUE" if is_video_object(it.get("detected_items") or []) else "FALSE")
        else:
            row["apifyStatus"] = "blocked"
        print(f"apify {domain}: {row['apifyStatus']} {row['videoObject']}", flush=True)
        return row

    with ThreadPoolExecutor(args.workers) as pool:
        results = list(pool.map(run, targets.items()))
    res_file = os.path.join(args.out_dir, "apify_results.csv")
    keep = [r for r in read_rows(res_file)[1] if clean_domain(r.get("webDomain") or "") not in targets] if os.path.exists(res_file) else []
    write_rows(res_file, ["webDomain", "videoObject", "apifyStatus", "detectedTypes", "richResultsUrl"], keep + results)
    count = lambda k, v: sum(r[k] == v for r in results)
    print(f"\nApify: {len(results)} runs, {count('videoObject', 'TRUE')} with VideoObject, {count('videoObject', 'FALSE')} without, "
          f"{count('apifyStatus', 'blocked')} blocked, {count('apifyStatus', 'error')} errors. Raw results in {raw_dir}/")


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

    players_file = os.path.join(args.out_dir, "players.csv")
    vimeo = {r["webDomain"]: r for r in read_rows(players_file)[1]} if os.path.exists(players_file) else {}

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
                v = vimeo.get(domain, {})
                if v.get("vimeoVerdict") == "real vimeo player":
                    schema, gap = "TRUE", "no"
                    notes[-1] = ("a real Vimeo player loads with the page; Vimeo's own VideoObject shows as a Video item "
                                 "in Google's Rich Results Test, so this is not a gap")
                elif v.get("vimeoVerdict") == "vimeo hero only":
                    other = [x for x in v.get("players", "").split("; ") if x and ("vimeo" not in x or "(hidden)" in x)]
                    if other or set(plats.split(", ")) - {"vimeo"}:
                        notes.append("Google sees a Video item only for a Vimeo hero loop, which does not count")
                    else:
                        gap = "check"
                        notes.append("the only video found is a Vimeo hero loop; check there is a real video before using the video lines")
                elif v.get("vimeoVerdict") == "vimeo hidden only":
                    notes.append("the Vimeo player is hidden until clicked, so Google does not see its schema")
        row.update(hasVideo=has, videoSchema=schema, videoSchemaGap=gap, videoNote="; ".join(notes))
        counts[gap] = counts.get(gap, 0) + 1
    write_rows(args.csv, cols, rows)

    print(f"Updated {args.csv}: videoSchemaGap yes {counts.get('yes', 0)}, no {counts.get('no', 0)}, "
          f"check {counts.get('check', 0)}, unknown {counts.get('unknown', 0)}.")
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
    pl = sub.add_parser("players", help="list the video iframes each homepage loads the way Google renders it (Vimeo check)")
    pl.add_argument("csv")
    pl.add_argument("out_dir")
    pl.add_argument("--workers", type=int, default=6)
    a = sub.add_parser("apify", help="run the Apify actor on each URL through the API, in parallel (needs APIFY_TOKEN)")
    a.add_argument("csv")
    a.add_argument("out_dir")
    a.add_argument("--workers", type=int, default=16, help="actor runs at once (the account allows 32)")
    r = sub.add_parser("recheck", help="deep render only: page and iframe VideoObject for every webDomain")
    r.add_argument("csv")
    r.add_argument("out_dir")
    r.add_argument("--workers", type=int, default=4)
    r.add_argument("--timeout", type=int, default=120, help="seconds per page")
    m = sub.add_parser("merge", help="combine the render and the Apify results into the CSV")
    m.add_argument("csv")
    m.add_argument("out_dir")
    args = ap.parse_args()
    {"detect": detect, "apify": apify_api, "players": players, "recheck": recheck, "merge": merge}[args.cmd](args)


if __name__ == "__main__":
    main()
