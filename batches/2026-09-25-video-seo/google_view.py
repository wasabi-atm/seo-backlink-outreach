"""Classifies what Google can see for each homepage, from the Apify Playwright run
(video_v2/google_view.json: every VideoObject in the page and in each iframe, rendered from Apify's
cloud, so Vimeo loads; from Indonesia the ISP blocks player.vimeo.com).

    python google_view.py

Writes video_v2/google_view.csv: webDomain, googleVerdict, googleVideoObjects, videoPlayers.
googleVerdict:
  real video schema  a VideoObject for a real video (a clickable player). The gap claim is wrong.
  hero only          the only VideoObjects are background or hero clips (Vimeo background=1, a
                     "hero"/"background"/"loop" name, or 20 seconds or shorter). Per the user's
                     rule (25 Sep, Netacea), a hero clip's schema does not count: the gap stands.
  none               no VideoObject anywhere Google can see: the gap stands.
  not loaded         the page did not load in the run.
"""
import csv, json, re

HERO_NAME = re.compile(r"hero|background|\bbg\b|bg[_-]|loop|banner|header|ambient", re.I)


def seconds(iso):
    m = re.match(r"P(?:T)?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?", iso or "")
    if not m or not any(m.groups()):
        return None
    h, mi, s = (float(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def is_hero(vo, frame_url):
    secs = seconds(vo.get("duration"))
    return ("background=1" in frame_url or "background=1" in (vo.get("embedUrl") or "")
            or bool(HERO_NAME.search(vo.get("name") or "")) or (secs is not None and secs <= 20))


def main():
    items = json.load(open("video_v2/google_view.json"))
    by = {}
    for it in items:
        d = it.get("domain") or ""
        if d and (d not in by or it.get("frames")):
            by[d] = it
    doms = [r["webDomain"] for r in csv.DictReader(open("video_v2/all178.csv"))]
    out = []
    for d in doms:
        it = by.get(d)
        if not it:
            out.append(dict(webDomain=d, googleVerdict="not loaded", googleVideoObjects="", videoPlayers=""))
            continue
        vos, real = [], False
        for f in it.get("frames", []):
            where = "page" if f.get("main") else re.sub(r"^https?://([^/?]+).*", r"\1 iframe", f.get("frameUrl", ""))
            for vo in f.get("vo", []):
                hero = is_hero(vo, f.get("frameUrl", ""))
                real = real or not hero
                vos.append(f"{vo.get('name') or '(no name)'} [{where}, {vo.get('duration') or 'no duration'}{', hero' if hero else ''}]")
            if f.get("micro"):
                real = True
                vos.append(f"microdata VideoObject [{where}]")
        verdict = "real video schema" if real else ("hero only" if vos else "none")
        players = "; ".join((p.get("src") or "data-src: " + p.get("dataSrc", ""))[:120] for p in it.get("players", []))
        out.append(dict(webDomain=d, googleVerdict=verdict, googleVideoObjects="; ".join(vos), videoPlayers=players))
    with open("video_v2/google_view.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["webDomain", "googleVerdict", "googleVideoObjects", "videoPlayers"])
        w.writeheader()
        w.writerows(out)
    counts = {}
    for r in out:
        counts[r["googleVerdict"]] = counts.get(r["googleVerdict"], 0) + 1
    print(counts)
    for r in out:
        if r["googleVerdict"] in ("real video schema", "hero only"):
            print(f"  {r['googleVerdict']:17} {r['webDomain']}: {r['googleVideoObjects'][:150]}")


if __name__ == "__main__":
    main()
