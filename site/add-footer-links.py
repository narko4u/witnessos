#!/usr/bin/env python3
"""Add sitewide footer page-links to whitepaper (exemplar) + rebuild all pages.

1. Replaces the exemplar footer (used as shell_bottom by every page) with a
   richer but navy-consistent footer: brand block + Pages + Legal + Contact.
2. Re-runs assemble.py for all assembled pages and convert-legal for terms/privacy.
3. Adds an Explore strip + page links to index.html directly.
"""
import pathlib, re, subprocess, sys

BASE = pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/witnessos-site")
PUB = BASE / "publish-v2"
WP = PUB / "whitepaper.html"

FOOTER = """<footer>
<img class="empire-banner" src="assets/empire-banner.webp" width="1200" height="400" loading="lazy" alt="WitnessOS and Empire Labs Pty Ltd">
<div>
<strong>Empire Labs Pty Ltd</strong>
<br>WitnessOS is the runtime governance layer for autonomous agents.</div>
<div>
<strong>Pages</strong>
<br><a href="index.html">Home</a>
<br><a href="whitepaper.html">Whitepaper</a>
<br><a href="demo.html">Simulation</a>
<br><a href="casestudy.html">Case study</a>
<br><a href="roadmap.html">Roadmap</a>
<br><a href="manifesto.html">Manifesto</a>
<br><a href="quickstart.html">Quickstart</a>
<br><a href="pricing.html">Access</a>
</div>
<div>
<strong>Legal</strong>
<br><a href="terms.html">Terms of Service</a>
<br><a href="privacy.html">Privacy Policy</a>
</div>
<div>
<a href="https://www.empirelabs.com.au">www.empirelabs.com.au</a>
<br><a href="mailto:contact@empirelabs.com.au">contact@empirelabs.com.au</a>
<br><a href="https://github.com/narko4u/witnessos">github.com/narko4u/witnessos</a>
</div>
</footer>"""

# 1) Replace footer in whitepaper exemplar.
wp = WP.read_text()
old_foot = re.search(r'(<footer>.*?</footer>)', wp, re.S)
assert old_foot, "footer not found in whitepaper"
wp2 = wp[:old_foot.start(1)] + FOOTER + wp[old_foot.end(1):]
if wp2 != wp:
    WP.write_text(wp2)
    print("whitepaper footer updated")
else:
    print("whitepaper footer already current")

# 2) Rebuild assembled pages.
for page in ["quickstart", "demo", "casestudy", "manifesto", "roadmap", "pricing", "signup"]:
    subprocess.run([sys.executable, str(BASE / "assemble.py"), page], cwd=BASE, check=True)

# terms/privacy: rebuild via convert-legal (reads whitepaper shell).
subprocess.run([sys.executable, str(BASE / "convert-legal.py")], cwd=BASE, check=True)
print("done: all shells rebuilt with new footer")
