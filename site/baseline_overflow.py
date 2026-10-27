#!/usr/bin/env python3
"""Baseline vs now: horizontal overflow per page per width.

Extracts the committed (pre-font-floor) pages from git HEAD into a temp dir and
compares document overflow against the current build, so any layout regression
from raising the type can be told apart from a pre-existing one.
"""
import pathlib, subprocess, sys
from playwright.sync_api import sync_playwright

BASE = pathlib.Path(__file__).resolve().parent
TMP = pathlib.Path("/tmp/fontfloor-baseline")
TMP.mkdir(exist_ok=True)

PAGES = ["index", "passport", "products", "instructions", "pricing", "demo",
         "casestudy", "manifesto", "roadmap", "signup", "terms", "privacy"]
WIDTHS = [1440, 1024, 768, 390]

for p in PAGES:
    out = subprocess.run(["git", "show", f"HEAD:publish-v2/{p}.html"],
                         cwd=BASE, capture_output=True, text=True)
    if out.returncode == 0:
        (TMP / f"{p}.html").write_text(out.stdout)

JS = "() => document.documentElement.scrollWidth - window.innerWidth"

with sync_playwright() as pw:
    b = pw.chromium.launch()
    print(f"{'page':14} " + "".join(f"{w:>16}" for w in WIDTHS))
    print(f"{'':14} " + "".join(f"{'base -> now':>16}" for w in WIDTHS))
    regressions = []
    for p in PAGES:
        row = []
        for w in WIDTHS:
            vals = {}
            for label, path in (("base", TMP / f"{p}.html"), ("now", BASE / "dist" / f"{p}.html")):
                if not path.exists():
                    vals[label] = None
                    continue
                pg = b.new_page(viewport={"width": w, "height": 900})
                pg.goto(path.as_uri())
                pg.wait_for_timeout(200)
                vals[label] = pg.evaluate(JS)
                pg.close()
            row.append(f"{vals['base']} -> {vals['now']}")
            if vals["now"] and vals["now"] > 0 and (not vals["base"] or vals["base"] == 0):
                regressions.append((p, w, vals["base"], vals["now"]))
        print(f"{p:14} " + "".join(f"{c:>16}" for c in row))
    b.close()

print()
print("NEW overflow (clean before, overflowing now):", regressions or "none")
