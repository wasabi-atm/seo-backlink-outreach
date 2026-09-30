"""Clicks the play controls on a few homepages (desktop Chrome, headless) and records what plays.

    python video_click_check.py video/click_check.json

For each site it clicks the given selector(s), waits, then lists player iframes, playing or
controls <video> tags (with duration and whether any audio was decoded after 4s of playback), and
the video requests the click caused. Also prints the HTML around given text (context lookups).
Only play buttons are clicked; nothing is submitted.
"""
import asyncio, json, re, sys

DESKTOP = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
MEDIA = re.compile(r"\.(mp4|webm|m3u8|mov)(\?|$)|vimeo\.com|youtube\.com/(embed|watch)|wistia|vidyard|stream\.mux\.com|loom\.com|brightcove", re.I)
SITES = {
    "rippling.com": {"click": ["a:has-text('Play video')"]},
    "crowdstrike.com": {"click": ["button[aria-label='Click to launch Video'] >> visible=true"]},
    "deel.com": {"click": ["button[aria-label='Play video'] >> visible=true"]},
    "ahrefs.com": {"click": ["button:has-text('Watch demos')"]},
    "hubspot.com": {"click": ["button.wtm-evfc__play-btn >> visible=true"]},
    "brex.com": {"click": ["button[data-testid=playButton] >> visible=true"]},
    "datadoghq.com": {"click": ["text=Datadog Video Tour", "a:has-text('Video Tour'), button:has-text('Video Tour')"]},
    "wiz.io": {"context": ["mux-player", "testimonial", "Watch"]},
    "klaviyo.com": {"context": ["vimeo.com/1223678585", "vimeo.com/1223222038"]},
    "gong.io": {"context": ["5lqgv3qxc8", "wistia.net/embed/iframe/"]},
    "freshworks.com": {"context": ["wistia-player"]},
}
STATE = """() => ({
  iframes: [...document.querySelectorAll('iframe')].filter(f => f.offsetWidth > 50).map(f => (f.src || '').slice(0, 160))
     .filter(s => /vimeo|youtube|wistia|vidyard|mux|loom|brightcove/i.test(s)),
  videos: [...document.querySelectorAll('video')].filter(v => v.offsetWidth > 50 && (!v.paused || v.controls)).map(v => ({
     src: (v.currentSrc || '').slice(0, 140), controls: v.controls, muted: v.muted, paused: v.paused,
     dur: isFinite(v.duration) ? Math.round(v.duration) : null, audioBytes: v.webkitAudioDecodedByteCount}))
})"""


async def main(out):
    from playwright.async_api import async_playwright
    res = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--autoplay-policy=no-user-gesture-required"])
        for d, cfg in SITES.items():
            ctx = await browser.new_context(user_agent=DESKTOP, viewport={"width": 1440, "height": 900})
            page, seen, r = await ctx.new_page(), [], {"clicks": [], "context": {}}
            page.on("request", lambda req: seen.append(req.url) if MEDIA.search(req.url) else None)
            try:
                await page.goto("https://" + d, wait_until="domcontentloaded", timeout=45000)
                try:
                    await page.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    pass
                await page.wait_for_timeout(4000)
                html = await page.content()
                for t in cfg.get("context", []):
                    r["context"][t] = [html[max(0, m.start() - 250): m.start() + 350].replace("\n", " ") for m in re.finditer(re.escape(t), html)][:4]
                for sel in cfg.get("click", []):
                    loc = page.locator(sel)
                    if not await loc.count():
                        r["clicks"].append({"sel": sel, "found": 0})
                        continue
                    el = loc.first
                    before = len(seen)
                    try:
                        await el.scroll_into_view_if_needed(timeout=5000)
                        await el.click(timeout=8000)
                    except Exception as e:
                        r["clicks"].append({"sel": sel, "error": str(e)[:150]})
                        continue
                    await page.wait_for_timeout(2000)
                    # unmute and play anything that is now showing, then measure decoded audio
                    await page.evaluate("() => document.querySelectorAll('video').forEach(v => { if (v.offsetWidth > 50 && (v.controls || !v.paused)) { v.muted = false; v.play().catch(() => {}); } })")
                    await page.wait_for_timeout(5000)
                    st = await page.evaluate(STATE)
                    r["clicks"].append({"sel": sel, "found": await loc.count(), "requests": list(dict.fromkeys(u[:150] for u in seen[before:]))[:10], **st})
                    break
            except Exception as e:
                r["error"] = str(e)[:200]
            await ctx.close()
            res[d] = r
            print(d, json.dumps(r)[:1500], "\n", flush=True)
        await browser.close()
    json.dump(res, open(out, "w"), indent=1)

asyncio.run(main(sys.argv[1]))
