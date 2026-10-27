#!/usr/bin/env python3
"""Render the site pages to PNG for review. Desktop width, full page."""
import pathlib
from playwright.sync_api import sync_playwright

BASE = pathlib.Path("/mnt/c/VaultSentinel/witnessos-site")
PUB = BASE / "publish-v2"
OUT = BASE / "preview"
OUT.mkdir(exist_ok=True)

PAGES = ["index", "passport", "products", "instructions", "pricing", "demo",
         "casestudy", "manifesto", "roadmap", "signup", "terms", "privacy"]

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
    for name in PAGES:
        f = PUB / f"{name}.html"
        page.goto(f.as_uri())
        page.wait_for_timeout(600)
        h = page.evaluate("document.body.scrollHeight")
        # hero crop (for the phone) + full page (for detail)
        page.screenshot(path=str(OUT / f"{name}-hero.png"), clip={"x": 0, "y": 0, "width": 1280, "height": min(1150, h)})
        page.screenshot(path=str(OUT / f"{name}-full.png"), full_page=True)
        print(f"{name:14} height={h:>6}px  ->  {name}-hero.png, {name}-full.png")
    b.close()
print("\nwritten to", OUT)
