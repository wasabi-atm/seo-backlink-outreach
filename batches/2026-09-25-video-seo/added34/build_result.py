"""Builds video_result.csv for the 34 added companies.

    python build_result.py

Reads targets.csv, video/video_check.csv (video_schema.py detect + recheck), video/players.csv
(video_schema.py players), video/rrt.csv (rrt_check.py), video/inventory.csv (video_inventory.py)
and applies the decisions below, which come from video/inventory.json, video/probe.json
(video_probe.py), video/click_check.json (video_click_check.py) and the click and audio checks run
on 30 Sep 2026.

Google's Rich Results Test did not run (it redirected to a Google sign-in page on the first test),
so every decision rests on local renders. The user's rules still apply: a silent autoplay or muted
loop is not a video, and schema that exists only for such a loop does not count (videoSchemaGap
check when that loop is the only video and Google would see a VideoObject for it).
"""
import csv
from urllib.parse import quote

RICH_TEST = "https://search.google.com/test/rich-results?url="
COLS = ["companyName", "webDomain", "homepageUrl", "richResultsTestUrl", "hasVideo", "videoPlatform", "videoSchema",
        "videoSchemaGap", "videoNote", "rrtResult", "playersAtLoad", "vimeoAtLoad", "userVideo", "agreesWithUser"]

# domain: (hasVideo, videoPlatform, videoSchema, videoSchemaGap, videoNote, agreesWithUser)
D = {
    "hubspot.com": ("no", "none (silent self-hosted clips)", "FALSE", "no",
        "The only videos are three silent product animation clips (8, 15 and 12 seconds, no audio track) that rotate in the hero, and the Play video buttons replay the same clips in a pop-up player, so there is no real video and no VideoObject.",
        "no: the user counted the hero clips, but they are short silent animations and the pop-up player only replays them"),
    "salesforce.com": ("unknown", "", "unknown", "unknown",
        "The homepage returned 403 Access Denied to every local render (Googlebot and normal Chrome), so its video and schema could not be checked.",
        "unverified: the page could not be loaded to check the user's No"),
    "notion.so": ("no", "none (silent self-hosted loop)", "FALSE", "no",
        "The only video is a silent 11-second autoplay hero loop from ctfassets with no controls, so there is no real video, and the page has no VideoObject.",
        "no: the hero video is a silent autoplay loop, which does not count"),
    "asana.com": ("no", "", "FALSE", "no",
        "No video tag or player on the homepage; See Asana in action links out to /demo/main-video.",
        "yes"),
    "monday.com": ("no", "none (silent self-hosted loops)", "FALSE", "no",
        "The only videos are muted autoplay loops of 15 to 17 seconds with no controls (Cloudinary), so there is no real video, and the page has no VideoObject.",
        "no: the hero and section videos are muted autoplay loops, which do not count"),
    "airtable.com": ("no", "none (silent self-hosted loops)", "FALSE", "no",
        "The only videos are muted autoplay background loops with a pause button and no controls (Sanity CDN), so there is no real video, and the page has no VideoObject.",
        "no: the hero and section videos are muted autoplay loops, which do not count"),
    "linear.app": ("no", "", "FALSE", "no",
        "No video tag, player or video URL on the homepage.",
        "yes"),
    "intercom.com": ("no", "", "FALSE", "no",
        "No video tag, player or video URL on the homepage.",
        "yes"),
    "zendesk.com": ("no", "", "FALSE", "no",
        "No video tag, player or video URL on the homepage.",
        "n/a (user unsure): no video found"),
    "freshworks.com": ("no", "none (Wistia background loops)", "FALSE", "check",
        "Every Wistia embed is a background player (controls hidden, autoplay, loop, 17 to 26 seconds), and Wistia's script adds a VideoObject for one of them (FW_EX Home page_ITSM_T1_V2, a 20-second loop) to the page head at load, so Google would likely show a Video item for a loop only; check before using the video lines.",
        "no: the Wistia embeds are background loops with the controls hidden, not playable videos"),
    "pipedrive.com": ("no", "", "FALSE", "no",
        "No video tag or player on the homepage; Watch demo links out to /en/demo.",
        "yes"),
    "close.com": ("no", "none (silent self-hosted loops)", "FALSE", "no",
        "The only videos are the muted 5-second Hero_Chloe loop and a 20-second Orb loop with no controls or audio, so there is no real video, and the page has no VideoObject.",
        "no: the hero and Orb videos are silent loops, which do not count"),
    "outreach.io": ("yes", "wistia", "TRUE", "no",
        "outreach.io redirects to outreach.ai/home, which has a Wistia pop-up video (Outreach: The Agentic AI Platform for Revenue Teams, 2:30) plus two animation clips, and Wistia's script puts a VideoObject for all three in the page head at load, so the real video has schema.",
        "no: there is a real Wistia video (2:30) behind a play button on the homepage"),
    "gong.io": ("yes", "wistia (loads on click)", "FALSE", "yes",
        "The Anthropic customer story tile plays a 2:35 Wistia video (Anthropic: Customer Case Study) that only loads when clicked, and nothing on the page gives it a VideoObject.",
        "no: the Anthropic customer story tile plays a 2:35 Wistia video"),
    "clari.com": ("no", "", "FALSE", "no",
        "No video tag, player or video URL on the homepage.",
        "yes"),
    "apollo.io": ("no", "none (silent self-hosted loop)", "FALSE", "no",
        "The only video is a silent 22-second autoplay hero loop (.webm) with no controls, so there is no real video, and the page has no VideoObject.",
        "no: the hero video is a silent autoplay loop, which does not count"),
    "klaviyo.com": ("no", "none (Vimeo-hosted loops)", "FALSE", "check",
        "The only videos are three Vimeo-hosted product loops (set to loop, two play on hover) drawn by Vimeo's player script, which the local ISP blocks, so if Google renders them as Vimeo players it would show Video items for loops only; check before using the video lines.",
        "yes"),
    "braze.com": ("no", "", "FALSE", "no",
        "No video tag, player or video URL on the homepage.",
        "yes"),
    "customer.io": ("no", "", "FALSE", "no",
        "No video tag, player or video URL on the homepage.",
        "yes"),
    "iterable.com": ("no", "", "FALSE", "no",
        "No video tag, player or video URL on the homepage.",
        "yes"),
    "semrush.com": ("no", "none (silent self-hosted loops)", "FALSE", "no",
        "The only videos are silent 26 to 35-second product loops (muted, looping, no controls, no audio track), so there is no real video, and the page has no VideoObject.",
        "yes"),
    "ahrefs.com": ("yes", "wistia (demo pop-up, loads on click)", "FALSE", "yes",
        "The hero and product .mp4s are silent loops, but the Watch demos button opens seven Wistia product demos (77 seconds to 4:10, for example Ahrefs Brand Radar) that load only on click, and the page has no VideoObject.",
        "yes (the real videos are the Wistia demos behind Watch demos; the hero and product .mp4s are silent loops)"),
    "vanta.com": ("no", "", "FALSE", "no",
        "No video tag or player on the homepage; Watch now links to a webinar page.",
        "n/a (user unsure): no video found"),
    "drata.com": ("yes", "vimeo", "TRUE", "no",
        "The homepage has a 50-second Vimeo video (AI Agent Governance Limited Availability) behind a play button, and the page's own JSON-LD carries a VideoObject for it, so it has schema.",
        "n/a (user unsure): there is a real Vimeo video with its own VideoObject"),
    "wiz.io": ("yes", "mux", "FALSE", "yes",
        "The customer carousel has Mux clips of named customer executives (CISOs and others) speaking (11 to 31 seconds, muted by default with an unmute button and sound), and the page has no VideoObject.",
        "yes"),
    "crowdstrike.com": ("yes", "vidyard", "FALSE", "yes",
        "Three Vidyard customer testimonial videos sit behind Click to launch Video buttons, and Vidyard adds no VideoObject and the page has none.",
        "yes"),
    "okta.com": ("no", "none (Vidyard background loops)", "FALSE", "no",
        "The only videos are Vidyard background loops (type/background, with a pause button) and Watch now links to the Oktane page, so there is no real video, and Vidyard carries no VideoObject.",
        "n/a (user unsure): only Vidyard background loops"),
    "datadoghq.com": ("yes", "html5 (Vimeo-hosted MP4 in a pop-up player)", "FALSE", "yes",
        "The product .mp4s are muted loops, but a pop-up player with controls holds the Datadog platform video tour (a Vimeo-hosted 1080p MP4, not a Vimeo player), and the page has no VideoObject.",
        "yes (the real video is the pop-up platform tour; the product .mp4s are silent loops)"),
    "newrelic.com": ("no", "none (Wistia product loops)", "FALSE", "check",
        "The only videos are six muted, looping Wistia product clips of 11 to 29 seconds (o11y_toolkit_*), and Wistia's script adds a VideoObject for each to the page head at load, so Google would likely show Video items for loops only; check before using the video lines.",
        "yes"),
    "hashicorp.com": ("no", "", "FALSE", "no",
        "No video tag, player or video URL on the homepage.",
        "yes"),
    "ramp.com": ("yes", "wistia (loads on click)", "FALSE", "yes",
        "The hero is a silent 13-second loop, but two Watch Video tiles open Wistia videos on click (Stack by Ramp, 67 seconds, and the Perplexity customer story, 99 seconds), and the page has no VideoObject.",
        "yes (the real videos are the two Wistia tiles; the hero .webm is a silent loop)"),
    "brex.com": ("yes", "html5 (self-hosted MP4, loads on click)", "FALSE", "yes",
        "See Brex in action plays a 73-second self-hosted MP4 with sound and controls that loads only on click, and the page has no VideoObject.",
        "yes"),
    "deel.com": ("yes", "html5 (self-hosted MP4, custom play button)", "TRUE", "no",
        "The customer story section has real self-hosted videos with sound (Revolut 1:45, Cocoroco 1:28) behind custom play buttons, and the page's own JSON-LD lists a VideoObject for each customer story video, so they have schema.",
        "no: the customer story section has real videos with sound (1:45 and 1:28)"),
    "rippling.com": ("yes", "wistia (loads on click)", "FALSE", "yes",
        "The Play video 1:00 button opens a 60-second Wistia video (Rippling AI Sizzle) that loads only on click, and the page has no VideoObject.",
        "n/a (user unsure): there is a real 60-second Wistia video"),
}


def rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def dom(d):
    d = d.strip().lower()
    return d[4:] if d.startswith("www.") else d


players = {r["webDomain"]: r for r in rows("video/players.csv")}
rrt = {r["webDomain"]: r for r in rows("video/rrt.csv")}
gstatus = {r["webDomain"]: r["status"] for r in rows("video/inventory.csv") if r["render"] == "google"}
out = []
for t in rows("targets.csv"):
    d = dom(t["webDomain"])
    has, plat, schema, gap, note, agree = D[d]
    p, r = players.get(d, {}), rrt.get(d, {})
    vimeo = p.get("vimeoVerdict") or p.get("error", "")
    if gstatus.get(d) not in ("200", ""):
        vimeo += f" (not a real check: the page answered HTTP {gstatus[d]} to the Googlebot user agent)"
    rrt_result = (r["rrtNote"] if r["rrtNote"].startswith("not run") else "not run: " + r["rrtNote"]) if r.get("rrtStatus") == "blocked" else \
        (f"{r.get('rrtTypes') or 'no items'}; Videos valid {r.get('rrtVideoValid') or 0}, invalid {r.get('rrtVideoInvalid') or 0}"
         + (f" ({r['rrtVideoNames']})" if r.get("rrtVideoNames") else "")) if r.get("rrtStatus") == "ok" else f"error: {r.get('rrtNote', '')}"
    out.append(dict(companyName=t["companyName"], webDomain=d, homepageUrl=t["url"],
                    richResultsTestUrl=RICH_TEST + quote(t["url"], safe=""), hasVideo=has, videoPlatform=plat,
                    videoSchema=schema, videoSchemaGap=gap, videoNote=note, rrtResult=rrt_result,
                    playersAtLoad=p.get("players", "") or "none", vimeoAtLoad=vimeo, userVideo=t["userVideo"],
                    agreesWithUser=agree))
with open("video_result.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(out)
count = lambda k, v: sum(r[k] == v for r in out)
print(f"{len(out)} rows; hasVideo yes {count('hasVideo', 'yes')}, no {count('hasVideo', 'no')}, unknown {count('hasVideo', 'unknown')}; "
      f"videoSchemaGap yes {count('videoSchemaGap', 'yes')}, no {count('videoSchemaGap', 'no')}, check {count('videoSchemaGap', 'check')}, "
      f"unknown {count('videoSchemaGap', 'unknown')}")
