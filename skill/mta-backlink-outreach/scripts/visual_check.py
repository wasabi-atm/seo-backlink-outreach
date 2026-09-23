"""Visual check for backlink candidates, built on webscreenshotter.

    python visual_check.py candidates.csv shots/ [--workers 4] [--timeout 150]

For every webDomain in the CSV it saves shots/<domain>.png, the first screen as a
16:9 image (1440x810), and writes shots/signals.csv with SEO-farm signals from the
homepage.

Setup (once): pip install webscreenshotter "selenium<4.10" webdriver-manager pillow
The selenium pin matters: webscreenshotter passes the driver path positionally,
which Selenium 4.10+ removed. Google Chrome must be installed.
"""
import argparse, csv, multiprocessing as mp, os, re, shutil, sys, time

AD_NETS = ["googlesyndication", "adsbygoogle", "taboola", "outbrain", "ezoic", "mediavine", "propellerads", "adsterra"]
FARM_WORDS = ["write for us", "guest post", "sponsored post", "submit a guest", "link insertion", "casino", "betting", "cbd", "payday"]
WIDTH, HEIGHT = 1440, 900   # browser window; the saved shot is cropped to 16:9
SHOT_W, SHOT_H = 1440, 810


def clean_domain(d):
    d = d.strip().lower()
    d = re.sub(r"^https?://", "", d).split("/")[0]
    return d[4:] if d.startswith("www.") else d


def _shoot(url, tmp):
    # Runs in a child process so a hung page can be killed.
    import contextlib, io
    from webscreenshotter import take_screenshot
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        take_screenshot(url, height=HEIGHT, width=WIDTH, directory=tmp, file_suffix="s_", stitch=False)


def shoot(url, out_dir, key, timeout):
    """Returns '' on success, else an error string."""
    tmp = os.path.join(out_dir, "_" + key)
    shutil.rmtree(tmp, ignore_errors=True)
    p = mp.Process(target=_shoot, args=(url, tmp))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate(); p.join(5)
        shutil.rmtree(tmp, ignore_errors=True)
        return "timeout after %ss" % timeout
    first = os.path.join(tmp, "s_1.png")
    if not os.path.exists(first):
        shutil.rmtree(tmp, ignore_errors=True)
        return "webscreenshotter produced no images"
    from PIL import Image
    im = Image.open(first).convert("RGB")
    # Scale to 1440 wide, then crop the top to 16:9. Pad if the window came out short.
    im = im.resize((SHOT_W, max(1, round(im.height * SHOT_W / im.width))))
    canvas = Image.new("RGB", (SHOT_W, SHOT_H), "white")
    canvas.paste(im.crop((0, 0, SHOT_W, min(im.height, SHOT_H))), (0, 0))
    canvas.save(os.path.join(out_dir, key + ".png"))
    shutil.rmtree(tmp, ignore_errors=True)
    return ""


def signals(url, key):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    s = {"webDomain": key, "loaded": False, "title": "", "adNetworks": "", "farmWords": "",
         "externalLinksHome": 0, "wordsHome": 0, "hasBlog": False, "shotError": ""}
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=%d,%d" % (WIDTH, HEIGHT))
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
        driver.set_page_load_timeout(30)
        driver.get(url)
        time.sleep(2.5)
        s["loaded"], s["title"] = True, (driver.title or "")[:120]
        html = driver.page_source.lower()
        text = driver.execute_script("return document.body ? document.body.innerText : ''").lower()
        s["adNetworks"] = ";".join(a for a in AD_NETS if a in html)
        s["farmWords"] = ";".join(w for w in FARM_WORDS if w in text)
        s["wordsHome"] = len(text.split())
        links = driver.execute_script("return Array.from(document.querySelectorAll('a[href]')).map(e => e.href)")
        s["externalLinksHome"] = len({l for l in links if l.startswith("http") and key not in l})
        s["hasBlog"] = any(re.search(r"/(blog|resources|insights|articles|news|guides)(/|$)", l) for l in links)
    except Exception as e:
        s["title"] = "ERROR: " + str(e).splitlines()[0][:100]
    finally:
        if driver:
            driver.quit()
    return s


def check(args):
    key, out_dir, timeout = args
    url = "https://" + key
    err = shoot(url, out_dir, key, timeout)
    s = signals(url, key)
    s["shotError"] = err
    print(f"{key}: {'loaded' if s['loaded'] else 'FAILED'}{'  shot: ' + err if err else ''}", flush=True)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path"); ap.add_argument("out_dir")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=150, help="seconds per site for screenshots")
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    # Install the driver once up front so parallel workers don't race on the download.
    from webdriver_manager.chrome import ChromeDriverManager
    ChromeDriverManager().install()
    rows = list(csv.DictReader(open(a.csv_path, newline="", encoding="utf-8-sig")))
    keys = list(dict.fromkeys(clean_domain(r["webDomain"]) for r in rows if r.get("webDomain", "").strip()))
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(a.workers) as ex:
        out = list(ex.map(check, [(k, a.out_dir, a.timeout) for k in keys]))
    with open(os.path.join(a.out_dir, "signals.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)
    failed = [s["webDomain"] for s in out if s["shotError"]]
    print(f"\n{len(out) - len(failed)}/{len(out)} screenshotted. signals: {os.path.join(a.out_dir, 'signals.csv')}")
    if failed:
        print("No screenshots (use the fallback in the skill): " + ", ".join(failed))


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    sys.exit(main())
