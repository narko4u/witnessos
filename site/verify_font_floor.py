#!/usr/bin/env python3
"""Prove the font floor holds on every built page.

Loads each dist page in Chromium, walks every element that renders text, and
reports anything below the floor. Headings (h1-h6) and table cells are exempt by
instruction (titles, subtitles, tables keep their own sizes). Also reports the
size of the kernel line itself and any horizontal overflow.
"""
import pathlib, sys, json
from playwright.sync_api import sync_playwright

BASE = pathlib.Path(__file__).resolve().parent
DIST = BASE / "dist"

JS = r"""
() => {
  const floor = getComputedStyle(document.documentElement).getPropertyValue('--floor').trim();
  const rows = [];
  const seen = new Set();
  document.querySelectorAll('body *').forEach(el => {
    // only elements that directly render text
    const txt = Array.from(el.childNodes)
      .filter(n => n.nodeType === 3)
      .map(n => n.textContent.trim()).join(' ').trim();
    if (!txt) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    const size = parseFloat(cs.fontSize);
    const tag = el.tagName.toLowerCase();
    const cls = (el.className && typeof el.className === 'string') ? el.className : '';
    // Exempt: headings (titles/subtitles), table cells, and logos/images --
    // including everything inside a logo lockup, e.g. the console wordmark's
    // inner <span> (Eddie 2026-09-17).
    const inLogo = !!el.closest('img, svg, picture, [class*="brand"], [class*="logo"]');
    const exempt = ['h1','h2','h3','h4','h5','h6','th','td','thead','tbody','table','caption'].includes(tag)
      || inLogo;
    let sel = tag + (cls ? '.' + cls.trim().split(' ').filter(Boolean).join('.') : '');
    rows.push({sel: sel.slice(0, 70), size: size, exempt: exempt, text: txt.slice(0, 48)});
    seen.add(size);
  });
  const below = rows.filter(r => r.size < parseFloat(floor) - 0.01);
  const violations = below.filter(r => !r.exempt);
  const overflows = [];
  document.querySelectorAll('body *').forEach(el => {
    if (el.scrollWidth > el.clientWidth + 2 && el.clientWidth > 0) {
      const cs = getComputedStyle(el);
      if (cs.overflowX === 'visible' || cs.overflowX === 'hidden') {
        overflows.push(el.tagName.toLowerCase() + '.' + (typeof el.className === 'string' ? el.className.trim().split(/\s+/)[0] : '') + ' sw=' + el.scrollWidth + ' cw=' + el.clientWidth);
      }
    }
  });
  const kernel = document.querySelector('.lead');
  return {
    floor: floor,
    docOverflow: document.documentElement.scrollWidth - window.innerWidth,
    minSize: rows.length ? Math.min(...rows.map(r => r.size)) : null,
    distinct: [...new Set(rows.map(r => r.size))].sort((a, b) => a - b),
    violations: violations.slice(0, 12),
    nViolations: violations.length,
    exemptBelow: [...new Set(below.filter(r => r.exempt).map(r => r.sel + ' @' + r.size + 'px'))].slice(0, 8),
    kernelSize: kernel ? parseFloat(getComputedStyle(kernel).fontSize) : null,
    overflows: [...new Set(overflows)].slice(0, 6),
  };
}
"""

def main():
    pages = sorted(DIST.glob("*.html"))
    viewports = [(1440, 900, "desktop"), (390, 844, "mobile")]
    bad = 0
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w, h, label in viewports:
            print(f"================ {label} {w}x{h} ================")
            pg = b.new_page(viewport={"width": w, "height": h})
            for f in pages:
                pg.goto(f.as_uri())
                pg.wait_for_timeout(250)
                r = pg.evaluate(JS)
                flag = "OK  " if r["nViolations"] == 0 else "FAIL"
                if r["nViolations"]:
                    bad += 1
                print(f"{flag} {f.name:20} floor={r['floor']:>4}  min={r['minSize']:<5} "
                      f"kernel={r['kernelSize']}  below-floor(non-heading/table)={r['nViolations']}  "
                      f"doc-overflow={r['docOverflow']}px")
                for v in r["violations"]:
                    print(f"        ↓ {v['size']}px  {v['sel']}  \"{v['text']}\"")
                if r["overflows"]:
                    print(f"        overflow: {'; '.join(r['overflows'])}")
                if label == "desktop" and f.name == "index.html":
                    print(f"        all distinct sizes: {r['distinct']}")
                if label == "desktop":
                    print(f"        exempt-but-below: {r['exemptBelow']}")
            pg.close()
        b.close()
    print()
    print(f"pages with non-exempt text below the floor: {bad}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
