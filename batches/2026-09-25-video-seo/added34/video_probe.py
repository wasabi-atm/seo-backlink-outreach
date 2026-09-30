"""Close look at chosen homepages: VideoObject details, player settings, and what a play button opens.

    python video_probe.py video/probe.json domain [domain ...]

Per domain, one render with a normal phone Chrome user agent and Google's tall 412x8000 viewport,
no scrolling or clicking (a stand-in for Googlebot where the site blocks the spoofed Googlebot user
agent with a 403), which records:
  - every VideoObject in the page's own JSON-LD or microdata (name, duration, embedUrl, contentUrl)
  - attributes of wistia-player, wistia_embed, mux-player and vidyard elements, and of every <video>
  - the HTML around each <video controls> and each play/watch button
Then a desktop render that clicks each visible play/watch button (never links to other pages) and
lists the video requests and player iframes that appear after the click.
"""
import asyncio, json, re, sys, time

PHONE = ("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36")
DESKTOP = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
MEDIA = re.compile(r"\.(mp4|webm|m3u8|mov)(\?|$)|vimeo\.com|youtube\.com/(embed|watch)|wistia|vidyard|stream\.mux\.com|loom\.com|brightcove|hubspotvideo|jwplayer", re.I)

LOOK = r"""() => {
  const vos = [];
  const walk = (n, path) => { if (Array.isArray(n)) n.forEach(x => walk(x, path)); else if (n && typeof n === 'object') {
      const t = [].concat(n['@type'] || []);
      if (t.some(x => String(x).endsWith('VideoObject'))) vos.push({name: n.name, duration: n.duration, embedUrl: n.embedUrl, contentUrl: n.contentUrl, uploadDate: n.uploadDate, thumb: [].concat(n.thumbnailUrl || [])[0]});
      Object.values(n).forEach(x => walk(x, path)); } };
  const ldScripts = [...document.querySelectorAll('script[type*="ld+json" i]')];
  const ldWhere = [];
  for (const s of ldScripts) { try { const before = vos.length; walk(JSON.parse(s.textContent), ''); if (vos.length > before) ldWhere.push((s.parentElement ? s.parentElement.tagName + '.' + (s.parentElement.className || '').toString().slice(0, 60) : '') + ' id=' + (s.id || '')); } catch (e) {} }
  const micro = [...document.querySelectorAll('[itemtype*="VideoObject"]')].map(e => e.outerHTML.slice(0, 300));
  const attrs = el => [...el.attributes].map(a => a.name + '=' + a.value.slice(0, 80)).join(' ');
  const players = [...document.querySelectorAll('wistia-player,[class*="wistia_embed"],mux-player,[class*="vidyard"],lite-youtube,lite-vimeo')].slice(0, 25)
      .map(e => ({tag: e.tagName.toLowerCase(), attrs: attrs(e).slice(0, 400), w: e.offsetWidth, h: e.offsetHeight}));
  const videos = [...document.querySelectorAll('video')].slice(0, 25).map(v => ({attrs: attrs(v).slice(0, 300), controls: v.controls, w: v.offsetWidth, h: v.offsetHeight,
      parent: (v.closest('section,div[class]') || v.parentElement).outerHTML.replace(/\s+/g, ' ').slice(0, 500)}));
  const plays = [];
  for (const el of document.querySelectorAll('button,a,[role=button]')) {
    const t = ((el.getAttribute('aria-label') || '') + ' ' + (el.innerText || '')).replace(/\s+/g, ' ').trim();
    if (/\bplay\b|watch|see .{1,25} in action|video|tour/i.test(t) && t.length < 100 && !el.closest('nav,footer,aside'))
      plays.push({text: t.slice(0, 90), href: el.getAttribute('href') || '', w: el.offsetWidth, html: el.outerHTML.replace(/\s+/g, ' ').slice(0, 300)});
  }
  return {title: document.title, url: location.href, videoObjects: vos, ldWhere, micro, players, videos, plays: plays.slice(0, 30)};
}"""


async def google_like(browser, domain):
    ctx = await browser.new_context(user_agent=PHONE, viewport={"width": 412, "height": 8000}, is_mobile=True, has_touch=True)
    page, out = await ctx.new_page(), {}
    try:
        r = await page.goto("https://" + domain, wait_until="domcontentloaded", timeout=45000)
        out["status"] = r.status if r else None
        try:
            await page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        await page.wait_for_timeout(8000)
        out.update(await page.evaluate(LOOK))
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {str(e)[:150]}"
    await ctx.close()
    return out


async def click_plays(browser, domain):
    ctx = await browser.new_context(user_agent=DESKTOP, viewport={"width": 1440, "height": 900})
    page, clicks = await ctx.new_page(), []
    seen = []
    page.on("request", lambda req: seen.append(req.url) if MEDIA.search(req.url) else None)
    try:
        await page.goto("https://" + domain, wait_until="domcontentloaded", timeout=45000)
        try:
            await page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        await page.wait_for_timeout(4000)
        loc = page.locator("button, [role=button], a[href^='#'], a:not([href])").filter(
            has_text=re.compile(r"\bplay\b|watch (the )?video|see .{1,25} in action|video tour|watch video", re.I))
        n = min(await loc.count(), 6)
        for i in range(n):
            el = loc.nth(i)
            try:
                if not await el.is_visible():
                    await el.scroll_into_view_if_needed(timeout=3000)
                if not await el.is_visible():
                    continue
                txt = (await el.inner_text()).strip()[:80]
                before = len(seen)
                await el.click(timeout=5000)
                await page.wait_for_timeout(5000)
                frames = await page.evaluate("""() => [...document.querySelectorAll('iframe')].filter(f => f.offsetWidth > 50)
                    .map(f => (f.src || '').slice(0, 160)).filter(s => /vimeo|youtube|wistia|vidyard|mux|loom|brightcove|hubspot/i.test(s))""")
                vids = await page.evaluate("""() => [...document.querySelectorAll('video')].filter(v => v.offsetWidth > 50 && (!v.paused || v.controls))
                    .map(v => ({src: (v.currentSrc || '').slice(0, 140), controls: v.controls, muted: v.muted, dur: isFinite(v.duration) ? Math.round(v.duration) : null}))""")
                clicks.append({"button": txt, "newRequests": list(dict.fromkeys(u[:160] for u in seen[before:]))[:12],
                               "iframesAfter": frames, "playingOrControlsVideos": vids})
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(1000)
            except Exception as e:
                clicks.append({"button": f"#{i}", "error": f"{type(e).__name__}: {str(e)[:120]}"})
    except Exception as e:
        clicks.append({"error": f"{type(e).__name__}: {str(e)[:150]}"})
    await ctx.close()
    return clicks


async def main(out_path, domains):
    from playwright.async_api import async_playwright

    res, sem = {}, asyncio.Semaphore(4)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])

        async def one(d):
            async with sem:
                t = time.time()
                res[d] = {"googleLike": await google_like(browser, d), "clicks": await click_plays(browser, d)}
                g = res[d]["googleLike"]
                print(f"{d}: {g.get('status')} VideoObjects {len(g.get('videoObjects', []))} clicks {len(res[d]['clicks'])} {time.time() - t:.0f}s", flush=True)

        await asyncio.gather(*(one(d) for d in domains))
        await browser.close()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({d: res[d] for d in domains}, f, indent=1)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2:]))
