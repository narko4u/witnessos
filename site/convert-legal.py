#!/usr/bin/env python3
"""Convert purple legal/prose pages (terms, privacy) to the navy theme.

Strategy: take the completed navy whitepaper exemplar as the shell source,
extract its <head>+<style> and nav/footer, then translate the purple page's
document body (class vocabulary -> navy vocabulary) and splice.
"""
import re, pathlib
import sys
sys.path.insert(0, str(pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/witnessos-site")))
from navybuild import build_nav

PUB = pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/publish-v2")

# ---------- 1. Load navy shell from the verified exemplar (not whitepaper.html) ----------
ex = (pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/witnessos-site") / "_navy-exemplar.html").read_text()

# head incl. opening <body><div class="wrap"><header...>...</header><main id="top"> ... <logo-stage...>
m_head = re.search(r'(<!DOCTYPE html>.*?<body>\s*<div class="wrap">.*?</header>\s*<main id="top">\s*<a class="logo-stage".*?</a>)', ex, re.S)
shell_top = m_head.group(1)

# footer from exemplar: capture from </main> through </html> so closure tags are kept
m_foot = re.search(r'(</main>\s*<footer>.*?</html>)', ex, re.S)
shell_bottom = m_foot.group(1)

# current nav label + page title come per-file; adjust via replace later.
# ---------- 2. Class translation for legal prose ----------
TRANS = [
    (r'class="legal-hero[^"]*"', ''),                       # hero wrapper
    (r'class="code-label"[^>]*style="[^"]*"[^>]*>', 'class="eyebrow" style="display:block;margin-bottom:12px">'),
    (r'class="display-large"', ''),                          # h1 uses core navy h1
    (r'class="meta"', 'class="value"'),
    (r'class="section-heading"', ''),                        # h2 core style
    (r'class="sub-heading"', ''),                            # h3 -> navy .prose h3
    (r'class="body-text"', ''),                              # p -> navy .prose p
    (r'class="definition-term"', 'style="color:var(--text)"'),
    (r'class="recital"', 'style="margin:22px 0;padding:16px 20px;border-left:3px solid var(--accent);background:var(--panel);border-radius:0 8px 8px 0;color:#d5e2ef"'),
    (r'class="highlight-box"', 'style="margin:16px 0;padding:16px 18px;border:1px solid var(--line);border-radius:8px;background:var(--panel)"'),
    (r'class="last-updated"', 'class="value"'),
    (r'class="document"', 'class="prose" style="max-width:780px;margin:0 auto"'),
    (r'class="container"', 'class="wrap"'),
]

def translate_body(purple_html):
    s = purple_html
    # drop purple <nav>...</nav> and <footer>...</footer>
    s = re.sub(r'<nav>.*?</nav>', '', s, flags=re.S)
    s = re.sub(r'<footer>.*?</footer>', '', s, flags=re.S)
    # drop <!doctype...><head>...</head><body ...>
    s = re.sub(r'<!DOCTYPE html>.*?<body>', '', s, flags=re.S)
    s = re.sub(r'</body>\s*</html>', '', s, flags=re.S)
    for pat, rep in TRANS:
        s = re.sub(pat, rep, s)
    # strip inline purple color styles referencing vars we no longer define
    s = re.sub(r'style="color:var\(--color-primary[^"]*"[^>]*>', '>', s)
    s = re.sub(r'style="[^"]*--color-primary[^"]*"', '', s)
    # logo references: purple uses witnessos-logo.png; navy uses assets/witnessos-logo.webp
    s = s.replace('src="witnessos-logo.png"', 'src="assets/witnessos-logo.webp"')
    s = s.replace('href="witnessos-logo.png"', 'href="assets/witnessos-logo.webp"')
    return s.strip()

def build(page):
    purple = (pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/publish-v1") / f"{page}.html").read_text()
    title_m = re.search(r'<title>(.*?)</title>', purple, re.S)
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', purple)
    title = title_m.group(1).strip() if title_m else f"WitnessOS | {page}"
    desc = desc_m.group(1) if desc_m else ""
    body = translate_body(purple)
    # --- build head title/desc into exemplar-derived top ---
    top = shell_top
    top = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', top, flags=re.S)
    top = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{desc}"', top, count=1)
    # canonical/og url
    top = top.replace('https://witnessos.com.au/whitepaper.html', f'https://witnessos.com.au/{page}.html')
    # nav: page-link nav from navybuild, current page marked
    top = re.sub(r'<nav aria-label="Main navigation">.*?</nav>',
                 lambda m: build_nav(f"{page}.html", page.capitalize()),
                 top, count=1, flags=re.S)
    # nav: mark this page current
    html = top + "\n" + body + "\n" + shell_bottom
    (PUB / f"{page}.html").write_text(html)
    print(f"wrote {PUB / f'{page}.html'} ({len(html)} chars)")

if __name__ == "__main__":
    for p in ("terms", "privacy"):
        build(p)
