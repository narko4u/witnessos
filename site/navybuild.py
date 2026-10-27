#!/usr/bin/env python3
"""Navy shell builder — reuse the verified exemplar's head/style/footer.

Usage (from another script or interactive):
    from navybuild import navy_shell, build_nav
    top, bottom = navy_shell(title, desc, active_label, canonical, extra_css="...")

Nav policy (Eddie 2026-09-07): page links, not section anchors.
  Homepage (index.html): Simulation | Case study | Manifesto | Roadmap |
  Request access | [Book an assessment button]
  Subpages: Home | Simulation | Case study | Manifesto | Roadmap | Request
  access | [Book an assessment button], with the current page marked
  aria-current. Legal pages (terms/privacy) append their own current entry.
"""
import re, pathlib

BASE = pathlib.Path(__file__).resolve().parent
PUB = BASE / "publish-v2"
EXEMPLAR = BASE / "_navy-exemplar.html"
CTA = "mailto:contact@empirelabs.com.au?subject=WitnessOS%20Assessment"

# Main site pages shown in the nav (label, canonical file).
# Nav policy (Eddie 2026-09-07): page links, not section anchors.
# Commercial pages lead and the passport sits beside them because it is the
# developer on-ramp. Simulation follows; Roadmap, Casestudy, Manifesto and
# Signup are reached from the landing page, footer and CTAs, keeping the nav at
# five links plus the CTA button so it holds at 980px.
NAV_PAGES = [
    ("Products", "products.html"),
    ("Passport", "passport.html"),
    ("Instructions", "instructions.html"),
    ("Conformance", "conformance.html"),
    ("Pricing", "pricing.html"),
    ("Post-quantum", "pqc.html"),
]

# Pages reachable but out of the nav (footer Pages column keeps them linked).
# Pages reached from another page instead of the nav. conformance earned a nav slot
# on Eddie's call (2026-10-18); standards is a stand-alone page reached by URL and
# sitemap (nothing links it today), so a ninth nav link would wrap the strip for it.
SUPPRESS_SELF_ENTRY = {"standards.html"}

FOOTER_PAGES = [
    ("Products", "products.html"),
    ("Instructions", "instructions.html"),
    ("Post-quantum", "pqc.html"),
    ("Simulation", "demo.html"),
    ("Case study", "casestudy.html"),
    ("Manifesto", "manifesto.html"),
    ("Pricing", "pricing.html"),
    ("Conformance evidence", "conformance.html"),
    ("Roadmap", "roadmap.html"),
    ("Request access", "signup.html"),
]

def build_nav(canonical, label):
    """Return the <nav> block for a subpage; canonical/label mark the current page."""
    parts = ['<nav aria-label="Main navigation">']
    parts.append(f'<a href="index.html">Home</a>')
    for nav_label, nav_file in NAV_PAGES:
        if nav_file == canonical:
            parts.append(f'<a href="{nav_file}" aria-current="page">{nav_label}</a>')
        else:
            parts.append(f'<a href="{nav_file}">{nav_label}</a>')
    # legal pages (not in NAV_PAGES): append own current entry.
    # Pages that are reached from another page instead of the nav set SUPPRESS_SELF_ENTRY,
    # because an eighth link wraps the strip at 1280px.
    if canonical not in [f for _, f in NAV_PAGES] and canonical not in SUPPRESS_SELF_ENTRY:
        parts.append(f'<a href="{canonical}" aria-current="page">{label}</a>')
    parts.append(f'<a class="button" href="{CTA}">Book an assessment</a>')
    parts.append('</nav>')
    return "\n".join(parts)

def navy_shell(title, desc, active_label="Simulation", canonical="demo.html", extra_css=None):
    """Return (top, bottom) html fragments in the navy theme.

    top: doctype..logo-stage; body content goes between top and bottom.
    active_label: nav text for the current page.
    extra_css: optional extra <style> rules injected before the closing </style>.
    """
    ex = EXEMPLAR.read_text()

    # Everything through the logo-stage close.
    m_top = re.search(
        r'(<!DOCTYPE html>.*?<main id="top">\s*<a class="logo-stage".*?</a>)',
        ex, re.S)
    top = m_top.group(1)

    # Everything from </main> to </html> (footer + closers).
    m_bot = re.search(r'(</main>.*?</html>)', ex, re.S)
    bottom = m_bot.group(1)

    # Patch title + description + canonical/og + twitter.
    top = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', top, flags=re.S)
    top = re.sub(r'<meta name="description" content="[^"]*"',
                 f'<meta name="description" content="{desc}"', top, count=1)
    top = re.sub(r'property="og:title" content="[^"]*"',
                 f'property="og:title" content="{title}"', top)
    top = re.sub(r'name="twitter:title" content="[^"]*"',
                 f'name="twitter:title" content="{title}"', top)
    top = re.sub(r'property="og:description" content="[^"]*"',
                 f'property="og:description" content="{desc}"', top)
    top = re.sub(r'name="twitter:description" content="[^"]*"',
                 f'name="twitter:description" content="{desc}"', top)
    top = top.replace('https://witnessos.com.au/whitepaper.html',
                      f'https://witnessos.com.au/{canonical}')

    # Nav: replace the entire old <nav> block with the page-link nav.
    top = re.sub(r'<nav aria-label="Main navigation">.*?</nav>',
                 lambda m: build_nav(canonical, active_label), top, count=1, flags=re.S)

    # Inject extra CSS before the final </style> (the exemplar has one style block).
    if extra_css:
        top = re.sub(r'</style>', extra_css + '\n</style>', top, count=1)
    return top, bottom
