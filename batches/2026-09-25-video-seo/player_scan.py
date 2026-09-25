"""Lists the video player iframes each homepage loads without any scrolling or clicking, the way
Google's renderer sees the page (tall phone viewport). Needed because the ISP here blocks
player.vimeo.com, so Vimeo's own VideoObject (which Google counts, see Netacea and Alpheya) never
loads locally, but the iframe URLs are still in the page.

    <repo>/.venv-crawl/bin/python player_scan.py video_v2/all178.csv video_v2/player_scan.csv [--workers 4]

vimeoVerdict per homepage (see classify):
  real vimeo player   a visible Vimeo player that is not a hero loop loads with the page: Google's
                      Rich Results Test shows Vimeo's VideoObject for it as a Video item (checked on
                      Alpheya and Tribepad), so the gap claim is wrong
  vimeo hero only     every visible Vimeo iframe is a hero loop (background=1, or autoplay and
                      muted): Google shows it as a Video item, but a hero clip's schema does not
                      count (the user's rule, from Netacea), so the gap stands if the site has a
                      real video elsewhere
  vimeo hidden only   the Vimeo player sits hidden (a closed pop-up): Google did not count Netacea's
                      hidden one, so the gap stands
  no vimeo at load    no Vimeo iframe loads until a click or scroll
"""
import argparse, asyncio, csv, re, sys, time

GB = ("Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0.6613.119 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
PLAYER = re.compile(r"vimeo|youtube|wistia|vidyard|loom\.com|brightcove|hubspotvideo|jwplayer|mux\.com|dailymotion", re.I)
JS = """() => [...document.querySelectorAll('iframe')].map(e => ({src: e.getAttribute('src') || '', lazy: e.getAttribute('loading') || '',
          w: e.offsetWidth, h: e.offsetHeight}))"""


def classify(players):
    """players: the iframe URLs as written in the players column ('<url> (WxH)' or '<url> (hidden)')."""
    vimeo = [p for p in players if "vimeo" in p]
    visible = [p for p in vimeo if "(hidden)" not in p]
    hero = lambda p: "background=1" in p or ("autoplay=1" in p and "muted=1" in p)
    if any(not hero(p) for p in visible):
        return "real vimeo player"
    if visible:
        return "vimeo hero only"
    return "vimeo hidden only" if vimeo else "no vimeo at load"


async def scan(domains, workers):
    from playwright.async_api import async_playwright
    sem, out = asyncio.Semaphore(workers), {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])

        async def one(d):
            async with sem:
                t = time.time()
                ctx = await browser.new_context(user_agent=GB, viewport={"width": 412, "height": 8000}, is_mobile=True, has_touch=True)
                page = await ctx.new_page()
                row = dict(webDomain=d, players="", vimeoVerdict="", error="")
                try:
                    await page.goto("https://" + d, wait_until="domcontentloaded", timeout=45000)
                    try:
                        await page.wait_for_load_state("networkidle", timeout=15000)
                    except Exception:
                        pass
                    await page.wait_for_timeout(5000)
                    frames = [f for f in await page.evaluate(JS) if PLAYER.search(f["src"])]
                    listed = [f["src"][:160] + (f" ({f['w']}x{f['h']})" if f["w"] else " (hidden)") for f in frames]
                    row["players"] = "; ".join(listed)
                    row["vimeoVerdict"] = classify(listed)
                except Exception as e:  # one bad page must not stop the batch
                    row["error"] = str(e).splitlines()[0][:100]
                finally:
                    await ctx.close()
                print(f"{d}: {row['vimeoVerdict'] or row['error']} {time.time() - t:.0f}s", flush=True)
                out[d] = row
        await asyncio.gather(*(one(d) for d in domains))
        await browser.close()
    return [out[d] for d in domains]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("out")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    doms = [r["webDomain"] for r in csv.DictReader(open(args.csv))]
    rows = asyncio.run(scan(doms, args.workers))
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["webDomain", "vimeoVerdict", "players", "error"])
        w.writeheader()
        w.writerows(rows)
    counts = {}
    for r in rows:
        k = r["vimeoVerdict"] or "error"
        counts[k] = counts.get(k, 0) + 1
    print(counts)


if __name__ == "__main__":
    main()
