"""Lists every video on each homepage, to tell real players from silent hero loops.

    python video_inventory.py targets.csv video/ [--workers 4]

Two renders per homepage, with local Playwright Chromium:
  google   Googlebot smartphone user agent, 412x8000 viewport, no scrolling or clicking (what Google sees)
  desktop  normal desktop Chrome, 1440x900, scrolled to the bottom in steps (anything lazy-loaded)

For each render it records the HTTP status and title (to spot bot-block pages), every <video> tag
(controls, autoplay, muted, loop, visible size, duration, whether it sits in nav/footer/aside),
player iframes and player markers (Wistia, Vidyard, YouTube, Vimeo, Loom, Brightcove, lite-youtube),
video URLs mentioned anywhere in the HTML (modal players), "play/watch video" buttons, and every
schema.org @type in the page's own JSON-LD and microdata. Writes video/inventory.json and
video/inventory.csv (one row per site and render).
"""
import argparse, asyncio, csv, json, os, re, time

GOOGLEBOT = ("Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) "
             "Chrome/128.0.6613.119 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
DESKTOP = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
           "Chrome/140.0.0.0 Safari/537.36")

JS = r"""() => {
  const chrome = el => !!el.closest('nav,footer,aside');
  const vis = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 1 && r.height > 1 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity !== 0; };
  const videos = [...document.querySelectorAll('video')].map(v => {
    const srcs = [v.currentSrc || v.getAttribute('src') || '', ...[...v.querySelectorAll('source')].map(s => s.getAttribute('src') || '')].filter(Boolean);
    const r = v.getBoundingClientRect();
    return {src: (srcs[0] || '').slice(0, 180), controls: v.hasAttribute('controls') || v.controls,
      autoplay: v.hasAttribute('autoplay') || v.autoplay, muted: v.muted || v.hasAttribute('muted'), loop: v.loop,
      w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top + scrollY), visible: vis(v),
      duration: isFinite(v.duration) ? Math.round(v.duration) : null, chrome: chrome(v),
      poster: (v.getAttribute('poster') || '').slice(0, 120), cls: (v.className && v.className.baseVal === undefined ? v.className : '').slice(0, 80)};
  });
  const PLAYER = /vimeo|youtube|youtu\.be|wistia|vidyard|loom\.com|brightcove|hubspotvideo|jwplayer|mux\.com|dailymotion|vidalytics|videoask|synthesia|storylane|navattic|arcade\.software|supademo/i;
  const iframes = [...document.querySelectorAll('iframe')].map(f => ({src: (f.getAttribute('src') || f.getAttribute('data-src') || '').slice(0, 180),
      w: f.offsetWidth, h: f.offsetHeight, chrome: chrome(f)})).filter(f => PLAYER.test(f.src));
  const markers = [];
  for (const el of document.querySelectorAll('lite-youtube,lite-vimeo,wistia-player,mux-player,video-js,[class*="wistia_embed"],[class*="wistia_async"],[class*="vidyard-player"],[data-vidyard],[data-wistia-id],[data-youtube-id],[data-video-id],[data-video-url],[data-video],[data-vimeo-id]')) {
    const attrs = [...el.attributes].filter(a => /src|video|wistia|vidyard|youtube|vimeo|class/i.test(a.name)).map(a => a.name + '=' + a.value.slice(0, 90)).join(' ');
    markers.push({tag: el.tagName.toLowerCase(), attrs: attrs.slice(0, 260), visible: vis(el), chrome: chrome(el)});
  }
  const html = document.documentElement.outerHTML;
  const urls = new Set();
  for (const m of html.matchAll(/(?:https?:)?\/\/[^"'\s<>()\\]+?\.(?:mp4|webm|m3u8|mov)(?:\?[^"'\s<>()\\]*)?/gi)) urls.add(m[0].slice(0, 160));
  for (const m of html.matchAll(/(?:https?:)?\/\/(?:www\.)?(?:youtube\.com\/(?:embed|watch|shorts)[^"'\s<>\\]*|youtu\.be\/[\w-]+|(?:player\.)?vimeo\.com\/(?:video\/)?\d+[^"'\s<>\\]*|fast\.wistia\.(?:com|net)\/[^"'\s<>\\]+|[\w.-]*wistia\.com\/medias\/\w+|(?:play|embed)\.vidyard\.com\/[^"'\s<>\\]+|www\.loom\.com\/(?:share|embed)\/\w+)/gi)) urls.add(m[0].slice(0, 160));
  const plays = [];
  for (const el of document.querySelectorAll('button,a,[role=button],[aria-label]')) {
    const t = ((el.getAttribute('aria-label') || '') + ' ' + (el.innerText || '')).replace(/\s+/g, ' ').trim();
    if (/\bplay\b|watch (the |our )?(video|demo|now|film|story|keynote)|see .{1,25} in action|video/i.test(t) && t.length < 90 && !chrome(el))
      plays.push({text: t.slice(0, 80), href: (el.getAttribute('href') || '').slice(0, 100), visible: vis(el)});
  }
  const ld = [...document.querySelectorAll('script[type*="ld+json" i]')].map(s => s.textContent || '');
  const types = new Set();
  const walk = n => { if (Array.isArray(n)) n.forEach(walk); else if (n && typeof n === 'object') {
      for (const k of ['@type', 'type']) if (n[k]) (Array.isArray(n[k]) ? n[k] : [n[k]]).forEach(t => typeof t === 'string' && types.add(t.split('/').pop()));
      Object.values(n).forEach(walk); } };
  for (const t of ld) { try { walk(JSON.parse(t)); } catch (e) { for (const m of t.matchAll(/"@type"\s*:\s*"([^"]+)"/g)) types.add(m[1] + '?'); } }
  for (const e of document.querySelectorAll('[itemtype]')) types.add('micro:' + e.getAttribute('itemtype').split('/').pop());
  return {title: document.title.slice(0, 120), finalUrl: location.href, videos, iframes, markers: markers.slice(0, 30),
          urls: [...urls].slice(0, 40), plays: plays.slice(0, 25), types: [...types], bodyLen: (document.body.innerText || '').length};
}"""


def clean_domain(d):
    d = re.sub(r"^https?://", "", d.strip().lower()).split("/")[0]
    return d[4:] if d.startswith("www.") else d


async def render(browser, url, mode):
    if mode == "google":
        ctx = await browser.new_context(user_agent=GOOGLEBOT, viewport={"width": 412, "height": 8000}, is_mobile=True, has_touch=True)
    else:
        ctx = await browser.new_context(user_agent=DESKTOP, viewport={"width": 1440, "height": 900})
    page, out = await ctx.new_page(), {"status": None, "error": ""}
    try:
        resp = await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        out["status"] = resp.status if resp else None
        try:
            await page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        await page.wait_for_timeout(6000)
        if mode == "desktop":
            for _ in range(30):
                done = await page.evaluate("() => { window.scrollBy(0, 700); return innerHeight + scrollY >= document.body.scrollHeight - 5; }")
                await page.wait_for_timeout(350)
                if done:
                    break
            await page.wait_for_timeout(4000)
        out.update(await page.evaluate(JS))
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {str(e).splitlines()[0][:150]}"
    finally:
        await ctx.close()
    return out


def summarise(d):
    vids = d.get("videos", [])
    real = [v for v in vids if v["controls"] and not v["chrome"]]
    loops = [v for v in vids if not v["controls"] and not v["chrome"]]
    return {
        "status": d.get("status"), "title": d.get("title", ""), "error": d.get("error", ""),
        "videoTags": len(vids), "controlsVideos": len(real), "controlsVisible": sum(v["visible"] for v in real),
        "silentLoops": len(loops), "loopDurations": ",".join(str(v["duration"]) for v in loops if v["duration"] is not None),
        "iframes": "; ".join(f"{f['src']} ({f['w']}x{f['h']}{', chrome' if f['chrome'] else ''})" for f in d.get("iframes", [])),
        "markers": "; ".join(f"{m['tag']} {m['attrs'][:120]}{' (hidden)' if not m['visible'] else ''}" for m in d.get("markers", []))[:600],
        "platformUrls": "; ".join(u for u in d.get("urls", []) if not re.search(r"\.(mp4|webm|m3u8|mov)", u, re.I))[:600],
        "playButtons": "; ".join(f"{p['text']}{' -> ' + p['href'] if p['href'] else ''}{'' if p['visible'] else ' (hidden)'}" for p in d.get("plays", []))[:600],
        "schemaTypes": ", ".join(sorted(d.get("types", []))),
    }


async def main(args):
    from playwright.async_api import async_playwright

    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        targets = [(clean_domain(r["webDomain"]), (r.get("url") or "").strip()) for r in csv.DictReader(f)]
    sem, res = asyncio.Semaphore(args.workers), {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage", "--autoplay-policy=no-user-gesture-required"])

        async def one(domain, url):
            async with sem:
                t = time.time()
                res[domain] = {m: await render(browser, url or "https://" + domain, m) for m in ("google", "desktop")}
                g, dsk = summarise(res[domain]["google"]), summarise(res[domain]["desktop"])
                print(f"{domain}: google {g['status']} controls {g['controlsVideos']} loops {g['silentLoops']} iframes [{g['iframes'][:80]}] "
                      f"| desktop {dsk['status']} controls {dsk['controlsVideos']} loops {dsk['silentLoops']} {time.time() - t:.0f}s", flush=True)

        await asyncio.gather(*(one(d, u) for d, u in targets))
        await browser.close()
    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, "inventory.json"), "w", encoding="utf-8") as f:
        json.dump({d: res[d] for d, _ in targets}, f, indent=1)
    rows = [dict(webDomain=d, render=m, **summarise(res[d][m])) for d, _ in targets for m in ("google", "desktop")]
    with open(os.path.join(args.out_dir, "inventory.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {args.out_dir}/inventory.json and inventory.csv")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("out_dir")
    ap.add_argument("--workers", type=int, default=4)
    asyncio.run(main(ap.parse_args()))
