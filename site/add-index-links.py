#!/usr/bin/env python3
"""Add outbound hyperlinks to index.html (navy landing page stays first page).

In the SAME theme/vocabulary (no new design system): inserts an "Explore the
full site" section using .cap-grid/.cap components, and expands the footer with
page links exactly matching the subpage footer.

The rest of index.html is untouched: same <style>, same sections, same order.
"""
import pathlib, re

BASE = pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/witnessos-site")
IDX = BASE / "publish-v2" / "index.html"
s = IDX.read_text()

# 1) Explore section placed after the FAQ section, before the final CTA.
explore = """<section id="explore">
<div class="eyebrow">Explore the full site</div>
<h2>Summary to substance</h2>
<p class="copy">The landing page is the one-minute summary. Each page below goes deeper, in the same governed-proof story.</p>
<div class="cap-grid">
<article class="cap">
<code>WHITEPAPER</code>
<h3><a href="whitepaper.html">Security architecture</a></h3>
<p>Policy enforcement, audit integrity, deployment and the compliance framework.</p>
</article>
<article class="cap">
<code>SIMULATION</code>
<h3><a href="demo.html">Interactive simulation</a></h3>
<p>Fire governed actions in your browser and inspect signed E0-E4 receipts.</p>
</article>
<article class="cap">
<code>CASE STUDY</code>
<h3><a href="casestudy.html">Governing 9 agents</a></h3>
<p>How Empire Labs governs its own autonomous fleet with WitnessOS.</p>
</article>
<article class="cap">
<code>MANIFESTO</code>
<h3><a href="manifesto.html">Why proof matters</a></h3>
<p>The case for governed autonomy over blind trust.</p>
</article>
<article class="cap">
<code>ROADMAP</code>
<h3><a href="roadmap.html">Shipped and next</a></h3>
<p>E4-capable anchored evidence today: anchoring implemented and independently verified. Current production receipts are E2 pending independent provider corroboration, with the connector layer and trust network ahead.</p>
</article>
<article class="cap">
<code>ACCESS</code>
<h3><a href="pricing.html">Evaluate and deploy</a></h3>
<p>Free browser simulation, design-partner early access, enterprise deployments.</p>
</article>
</div>
</section>
"""

faq_end = re.search(r'(<section class="faq" id="faq">.*?</section>)(\n<section class="cta">)', s, re.S)
assert faq_end, "FAQ section boundary not found"
s = s[:faq_end.start(2)] + explore + s[faq_end.start(2):]

# 2) Footer page links (same block as subpages).
footer = """<footer>
<img class="empire-banner" src="assets/empire-banner.webp" width="1200" height="400" loading="lazy" alt="WitnessOS and Empire Labs Pty Ltd">
<div>
<strong>Empire Labs Pty Ltd</strong>
<br>WitnessOS is the runtime governance layer for autonomous agents.</div>
<div>
<strong>Pages</strong>
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
old_footer = re.search(r'(<footer>.*?</footer>)', s, re.S)
assert old_footer, "index footer not found"
s = s[:old_footer.start(1)] + footer + s[old_footer.end(1):]

IDX.write_text(s)
print(f"index.html updated ({len(s)} chars)")
