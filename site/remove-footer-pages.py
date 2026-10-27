#!/usr/bin/env python3
"""Remove the Pages column from every footer (Eddie 2026-09-07).

The column:
<div>
<strong>Pages</strong>
<br><a href="index.html">Home</a>
<br><a href="demo.html">Simulation</a>
<br><a href="casestudy.html">Case study</a>
<br><a href="manifesto.html">Manifesto</a>
<br><a href="roadmap.html">Roadmap</a>
<br><a href="signup.html">Request access</a>
</div>

Top nav already carries these links on every page, so the footer column is
redundant. Applied to all publish-v2 pages + the build exemplar.
"""
import pathlib, re

BASE = pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/witnessos-site")
PUB = BASE / "publish-v2"

pages_col = re.compile(
    r'\s*<div>\s*<strong>Pages</strong>.*?</div>', re.S)

targets = ["index", "demo", "casestudy", "manifesto", "roadmap", "terms", "privacy", "signup"]

for name in targets:
    p = PUB / f"{name}.html"
    s = p.read_text(errors="replace")
    s2, n = pages_col.subn("", s, count=1)
    assert n == 1, f"{name}: expected exactly one Pages column, got {n}"
    # tidy the double blank line the removal leaves
    s2 = s2.replace("</footer>\n\n</div>", "</footer>\n</div>")
    s2 = s2.replace("</div>\n\n\n<div>", "</div>\n<div>")
    p.write_text(s2)
    print(f"{name}.html: Pages column removed")

# keep the exemplar in sync so future rebuilds don't resurrect it
ex = BASE / "_navy-exemplar.html"
s = ex.read_text()
s2, n = pages_col.subn("", s, count=1)
assert n == 1, f"exemplar: expected exactly one Pages column, got {n}"
ex.write_text(s2)
print("_navy-exemplar.html: Pages column removed")
