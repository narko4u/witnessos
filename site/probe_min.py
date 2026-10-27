#!/usr/bin/env python3
"""Show exactly which elements sit below the floor on one page (no exemptions applied)."""
import sys, pathlib
from playwright.sync_api import sync_playwright

BASE = pathlib.Path(__file__).resolve().parent
page_name = sys.argv[1] if len(sys.argv) > 1 else "instructions"
width = int(sys.argv[2]) if len(sys.argv) > 2 else 390

JS = """() => {
  const out = [];
  for (const el of document.querySelectorAll('*')) {
    const t = (el.textContent || '').trim();
    if (!t) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const fs = parseFloat(cs.fontSize);
    if (fs < 18) {
      let inTable = !!el.closest('table');
      out.push([fs, el.tagName.toLowerCase(), (el.className || '').toString().slice(0, 40),
                inTable ? 'IN-TABLE' : '', t.slice(0, 60).replace(/\\s+/g, ' ')]);
    }
  }
  return out.sort((a, b) => a[0] - b[0]);
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": width, "height": 900})
    pg.goto((BASE / "dist" / f"{page_name}.html").as_uri())
    pg.wait_for_timeout(300)
    for fs, tag, cls, tbl, txt in pg.evaluate(JS):
        print(f"{fs:>5}px  <{tag} class=\"{cls}\"> {tbl:9} {txt}")
    b.close()
