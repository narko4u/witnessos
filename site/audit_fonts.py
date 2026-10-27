#!/usr/bin/env python3
"""Audit every font-size the site actually ships.

Reads dist/*.html (the deploy dir), pulls every <style> block and every inline
style attribute, and prints each font-size declaration with its resolved pixel
value so we can see what sits below the floor.
"""
import re, pathlib, sys

BASE = pathlib.Path(__file__).resolve().parent
DIST = BASE / "dist"

def resolved_px(raw: str):
    v = raw.strip()
    m = re.match(r'^(-?[\d.]+)px$', v)
    if m:
        return float(m.group(1))
    m = re.match(r'^(-?[\d.]+)rem$', v)
    if m:
        return float(m.group(1)) * 16
    m = re.match(r'^(-?[\d.]+)em$', v)
    if m:
        return float(m.group(1)) * 16  # rough: relative to a 16px context
    if v.startswith("clamp("):
        nums = re.findall(r'(\d+(?:\.\d+)?)px', v)
        if nums:
            return min(float(n) for n in nums)
    if v.endswith("%"):
        return None
    return None

rows = []
for page in sorted(DIST.glob("*.html")):
    html = page.read_text(encoding="utf-8")
    # <style> blocks
    for block in re.findall(r'<style[^>]*>(.*?)</style>', html, re.S):
        for sel, decls in re.findall(r'([^{}]+)\{([^{}]*)\}', block):
            for v in re.findall(r'font-size\s*:\s*([^;}]+)', decls):
                rows.append((page.name, "css", " ".join(sel.split())[:60], v.strip(), resolved_px(v)))
    # inline attributes
    for attr in re.findall(r'style="([^"]*)"', html):
        for v in re.findall(r'font-size\s*:\s*([^;"]+)', attr):
            rows.append((page.name, "inline", "-", v.strip(), resolved_px(v)))
    # JS-generated markup (fallback text sizes inside strings)
    for v in re.findall(r"font-size:\s*(\.?\d*(?:\.\d+)?(?:px|rem|em))", html):
        pass

seen = {}
for page, kind, sel, raw, px in rows:
    seen.setdefault((raw, px), []).append(f"{page}:{kind}:{sel}")

print(f"{'raw':>10}  {'px':>6}  where")
print("-" * 100)
for (raw, px), where in sorted(seen.items(), key=lambda kv: (kv[0][1] is None, kv[0][1] or 0)):
    locs = where[:3]
    extra = f" (+{len(where)-3} more)" if len(where) > 3 else ""
    print(f"{raw:>10}  {('' if px is None else format(px, '.1f')):>6}  {', '.join(locs)}{extra}")

print()
print("=== BELOW 20px ===")
below = [k for k in seen if k[1] is not None and k[1] < 20]
for raw, px in sorted(below, key=lambda k: k[1]):
    print(f"{px:>6.1f}px  {raw:>10}  {len(seen[(raw,px)])} occurrence(s)")
print(f"distinct sub-20px values: {len(below)}")
