"""Live Google Rich Results Test (RRT) check, one homepage at a time.

    python rrt_check.py targets.csv video/rrt.csv [--pause 25]

Opens https://search.google.com/test/rich-results?url=<homepage> in Chromium (headed), waits up to
150s for the test to finish, reads the detected item types from the results page, opens the Videos
entry if there is one to read its valid/invalid counts and item names, saves a screenshot to
rrt_shots/<domain>.png and writes one row per site to rrt.csv
(webDomain, rrtStatus ok/blocked/error, rrtTypes, rrtVideoValid, rrtVideoInvalid, rrtVideoNames, rrtNote).

Hard stop: if Google shows a CAPTCHA, reCAPTCHA, an "unusual traffic" page or a sign-in page, the
run stops at once, and that site and every site after it are written as rrtStatus=blocked. Nothing
tries to solve, bypass or get round it.

Run on 30 Sep 2026: the first test (freshworks.com) redirected straight to accounts.google.com
("Sign in to continue to Google Search Console"), so the step stopped there and all 34 rows are
blocked. Because Google never showed a results page, the result parser below (read_results) has
not been exercised against the live page yet; check its output against the screenshots the first
time it runs.
"""
import argparse, asyncio, csv, os, re, sys, time
from urllib.parse import quote

RICH_TEST = "https://search.google.com/test/rich-results?url="
COLS = ["webDomain", "rrtStatus", "rrtTypes", "rrtVideoValid", "rrtVideoInvalid", "rrtVideoNames", "rrtNote"]
WALL_URL = re.compile(r"accounts\.google\.com|google\.com/sorry|/recaptcha/", re.I)
WALL_TEXT = re.compile(r"unusual traffic|not a robot|recaptcha|captcha|to continue to Google Search Console|Couldn.t sign you in", re.I)
DONE_TEXT = re.compile(r"valid items? detected|No items detected|not eligible for rich results|Test results|Page not eligible", re.I)


def clean_domain(d):
    d = re.sub(r"^https?://", "", d.strip().lower()).split("/")[0]
    return d[4:] if d.startswith("www.") else d


async def wall(page):
    if WALL_URL.search(page.url):
        return f"redirected to {page.url.split('?')[0]}"
    try:
        txt = await page.evaluate("document.body ? document.body.innerText : ''")
    except Exception:
        return ""  # mid-navigation; checked again on the next poll
    m = WALL_TEXT.search(txt)
    return f"page shows '{m.group(0)}'" if m else ""


async def read_results(page):
    """Detected types with counts, plus the Videos detail. Untested against a live results page."""
    txt = await page.evaluate("document.body.innerText")
    types = []
    for m in re.finditer(r"^\s*([A-Z][A-Za-z ]{2,40})\s*\n\s*(\d+)\s+valid items? detected", txt, re.M):
        types.append(f"{m.group(1).strip()} ({m.group(2)})")
    valid = invalid = ""
    names = []
    videos = page.get_by_text(re.compile(r"^Videos?$")).first
    if await videos.count():
        await videos.click()
        await page.wait_for_timeout(3000)
        detail = await page.evaluate("document.body.innerText")
        mv = re.search(r"(\d+)\s+valid items?", detail)
        mi = re.search(r"(\d+)\s+invalid items?", detail)
        valid, invalid = (mv.group(1) if mv else "0"), (mi.group(1) if mi else "0")
        names = re.findall(r"^\s*name\s*\n?\s*(.+)$", detail, re.M)[:10]
    return txt, types, valid, invalid, names


async def main(args):
    from playwright.async_api import async_playwright

    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        targets = [(clean_domain(r["webDomain"]), (r.get("url") or "").strip() or "https://" + clean_domain(r["webDomain"]))
                   for r in csv.DictReader(f)]
    shots = os.path.join(os.path.dirname(os.path.abspath(args.csv)), "rrt_shots")
    os.makedirs(shots, exist_ok=True)
    rows, stopped = [], ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 1000}, locale="en-US")
        for i, (domain, url) in enumerate(targets):
            row = dict(webDomain=domain, rrtStatus="blocked", rrtTypes="", rrtVideoValid="", rrtVideoInvalid="",
                       rrtVideoNames="", rrtNote="")
            if stopped:
                row["rrtNote"] = f"not run: the RRT step stopped earlier ({stopped})"
                rows.append(row)
                continue
            page, t = await ctx.new_page(), time.time()
            try:
                await page.goto(RICH_TEST + quote(url, safe="") + "&hl=en", wait_until="domcontentloaded", timeout=60000)
                result = ""
                while time.time() - t < 150:
                    await page.wait_for_timeout(5000)
                    w = await wall(page)
                    if w:
                        stopped = f"{domain}: {w}"
                        row["rrtNote"] = f"Google showed a wall ({w}); RRT step stopped"
                        break
                    try:
                        if DONE_TEXT.search(await page.evaluate("document.body.innerText")):
                            result = "done"
                            break
                    except Exception:
                        pass
                if not stopped:
                    await page.wait_for_timeout(3000)
                    if result:
                        txt, types, valid, invalid, names = await read_results(page)
                        row.update(rrtStatus="ok", rrtTypes=", ".join(types) or ("none" if "No items detected" in txt else ""),
                                   rrtVideoValid=valid, rrtVideoInvalid=invalid, rrtVideoNames=" | ".join(names))
                    else:
                        row.update(rrtStatus="error", rrtNote="test did not finish within 150s")
                await page.screenshot(path=os.path.join(shots, domain + ".png"))
            except Exception as e:
                row.update(rrtStatus="error", rrtNote=f"{type(e).__name__}: {str(e).splitlines()[0][:150]}")
            finally:
                await page.close()
            print(f"rrt {domain}: {row['rrtStatus']} {row['rrtTypes']} {row['rrtNote']} {time.time() - t:.0f}s", flush=True)
            rows.append(row)
            if not stopped and i < len(targets) - 1:
                await asyncio.sleep(args.pause)
        await browser.close()
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {args.out}" + (f"; stopped at {stopped}" if stopped else ""))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("out")
    ap.add_argument("--pause", type=int, default=25, help="seconds between tests")
    asyncio.run(main(ap.parse_args()))
