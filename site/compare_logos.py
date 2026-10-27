#!/usr/bin/env python3
"""Did the font floor change any logo or image? Compare HEAD~1 vs now.

Pulls the pre-font-floor pages out of git (HEAD~1) and measures every image,
svg and logo/brand element on both builds, so the new exempt list (titles,
subtitles, logos, images, tables) can be honoured with evidence.
"""
import pathlib, subprocess
from playwright.sync_api import sync_playwright

BASE = pathlib.Path(__file__).resolve().parent
TMP = pathlib.Path("/tmp/fontfloor-pre")
TMP.mkdir(exist_ok=True)

PAGES = ["index", "passport", "products", "instructions", "pricing", "demo",
         "casestudy", "manifesto", "roadmap", "signup", "terms", "privacy"]

for p in PAGES:
    out = subprocess.run(["git", "show", f"HEAD~1:publish-v2/{p}.html"],
                         cwd=BASE, capture_output=True, text=True)
    if out.returncode == 0:
        (TMP / f"{p}.html").write_text(out.stdout)

JS = """() => {
  const out = [];
  const sel = 'img, svg, .logo, .logo-stage, .brand, [class*="brand"], [class*="logo"]';
  for (const el of document.querySelectorAll(sel)) {
    const r = el.getBoundingClientRect();
    if (r.width < 1) continue;
    const cs = getComputedStyle(el);
    out.push([el.tagName.toLowerCase(), (el.className || '').toString().slice(0, 32),
              Math.round(r.width) + 'x' + Math.round(r.height), cs.fontSize,
              (el.textContent || '').trim().slice(0, 30).replace(/\\s+/g, ' ')]);
  }
  return out;
}"""

def measure(browser, path):
    pg = browser.new_page(viewport={"width": 1440, "height": 1000})
    pg.goto(path.as_uri())
    pg.wait_for_timeout(250)
    rows = pg.evaluate(JS)
    pg.close()
    return rows

with sync_playwright() as pw:
    b = pw.chromium.launch()
    diffs = 0
    for p in PAGES:
        base = measure(b, TMP / f"{p}.html")
        now = measure(b, BASE / "dist" / f"{p}.html")
        by_key = lambda rows: {(r[0], r[1], r[4]): (r[2], r[3]) for r in rows}
        bmap, nmap = by_key(base), by_key(now)
        def box_change(was, isnow):
            a = [int(v) for v in was[0].split("x")]
            b = [int(v) for v in isnow[0].split("x")]
            return abs(a[0] - b[0]) > 1 or abs(a[1] - b[1]) > 1
        def meaningful(k, was, isnow):
            # What matters for a logo/image is its rendered BOX. The inherited
            # font-size on an <img> or logo <a> renders no text at all.
            if k[0] in ("img", "svg", "a", "picture"):
                return box_change(was, isnow)
            return was != isnow
        changed = [(k, bmap[k], nmap[k]) for k in bmap
                   if k in nmap and meaningful(k, bmap[k], nmap[k])]
        added = [k for k in nmap if k not in bmap]
        for k, was, isnow in changed:
            print(f"CHANGED {p:12} <{k[0]} class=\"{k[1]}\"> {k[2][:26]:28} {was} -> {isnow}")
            diffs += 1
        for k in added:
            print(f"ADDED   {p:12} <{k[0]} class=\"{k[1]}\"> {k[2][:26]:28} {nmap[k]}")
            diffs += 1
    b.close()
    print()
    print("logo/image elements changed by the floor raise:", diffs if diffs else "none")
