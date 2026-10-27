#!/usr/bin/env python3
"""Element-level screenshots so the raised type can be eyeballed where it matters."""
import pathlib
from playwright.sync_api import sync_playwright

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / "preview"
OUT.mkdir(exist_ok=True)

SHOTS = [
    ("demo", ".demo-shell", "demo-console.png"),
    ("index", ".receipt", "index-receipt.png"),
    ("index", ".cap", "index-caps.png"),
    ("pricing", ".plans", "pricing-plans.png"),
    ("casestudy", ".metrics", "casestudy-metrics.png"),
    ("instructions", ".prose pre", "instructions-pre.png"),
]

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 1000})
    for page, sel, out in SHOTS:
        pg.goto((BASE / "dist" / f"{page}.html").as_uri())
        pg.wait_for_timeout(300)
        el = pg.query_selector(sel)
        if not el:
            print(f"MISS {page} {sel}")
            continue
        el.scroll_into_view_if_needed()
        pg.wait_for_timeout(150)
        el.screenshot(path=str(OUT / out))
        box = el.bounding_box()
        print(f"OK   {page} {sel:16} -> {out}  {int(box['width'])}x{int(box['height'])}")
    b.close()
