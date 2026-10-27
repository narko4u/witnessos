#!/usr/bin/env python3
"""Build witnessos-draft.html: the live navy single page + compressed sections.

Same exact theme (copy of publish-v2/index.html, byte-identical CSS), with
main points from the 11-page content set folded in as anchor sections that
only use existing components (.cap/.cap-grid/.standards/.faq-item/.actions).
"""
import pathlib, sys

SRC = pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/publish-v2/index.html")
OUT = pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/witnessos-draft.html")
html = SRC.read_text()

def rep(old, new, tag):
    global html
    n = html.count(old)
    assert n == 1, f"{tag}: expected 1 match, found {n}"
    html = html.replace(old, new)

# 1) Nav: add Access + Roadmap anchors in the same style (kept tight).
rep('<a href="#compliance">Compliance</a>',
    '<a href="#compliance">Compliance</a>\n<a href="#access">Access</a>\n<a href="#roadmap">Roadmap</a>',
    "nav anchors")

# 2) Compressed ACCESS section (pricing + signup + quickstart main points).
access = """<section id="access">
<div class="eyebrow">Access</div>
<h2>Evaluate free. Deploy with our team.</h2>
<p class="copy">Three ways in: a free browser evaluation, the design-partner programme for the proprietary gateway engine, and custom enterprise deployments. Every path runs the same evidence ladder.</p>
<div class="cap-grid">
<article class="cap">
<code>SIMULATION</code>
<h3>Free in-browser evaluation</h3>
<p>Walk the governed-action flow in your browser: policy evaluation, the E0 to E4 evidence ladder and signed receipts. No sign-up and no install.</p>
</article>
<article class="cap">
<code>EARLY ACCESS</code>
<h3>Design-partner programme</h3>
<p>Deploy the proprietary gateway engine on your own infrastructure under NDA, with direct engineering support and RFC 3161 anchored E4 evidence.</p>
</article>
<article class="cap">
<code>ENTERPRISE</code>
<h3>Custom deployments</h3>
<p>On-premises or dedicated deployments, custom policy integrations, white-label options and SLAs tailored to your estate.</p>
</article>
</div>
<div class="actions">
<a class="button" href="mailto:contact@empirelabs.com.au?subject=WitnessOS%20Assessment">Book a technical assessment</a>
<a class="button secondary" href="mailto:contact@empirelabs.com.au?subject=WitnessOS%20Enterprise%20Enquiry">Enterprise enquiry</a>
</div>
</section>
"""
rep('<section class="faq" id="faq">', access + '<section class="faq" id="faq">', "insert access before faq")

# 3) Compressed ROADMAP section (roadmap main points) after access.
roadmap = """<section id="roadmap">
<div class="eyebrow">Roadmap</div>
<h2>Shipped. Shipping. Next.</h2>
<div class="cap-grid">
<article class="cap">
<code>SHIPPED &middot; SEP 2026</code>
<h3>E4 anchored evidence</h3>
<p>Live receipts carry RFC 3161 external timestamps with revocation verified at record time, and they re-verify offline with zero trust in Empire Labs.</p>
</article>
<article class="cap">
<code>NOW</code>
<h3>Early-access engagements</h3>
<p>Design-partner deployments are scaling toward self-serve access. The SDK is open source and the receipt specification is public.</p>
</article>
<article class="cap">
<code>NEXT</code>
<h3>More governed lanes</h3>
<p>Additional email, messaging and financial-system connectors ship through the design-partner programme.</p>
</article>
</div>
<div class="standards">
<strong>Dogfooded in production.</strong> WitnessOS governs Empire Labs' own autonomous fleet: 9 agents, 1,247 actions evaluated in 30 days, 7 policy denials, 12ms median evaluation latency and zero unauthorised actions.
</div>
</section>
"""
rep('<section class="faq" id="faq">', roadmap + '<section class="faq" id="faq">', "insert roadmap before faq")

# 4) FAQ: two access questions that replace the separate pricing/signup pages.
faq_extra = """<div class="faq-item">
<h3>How do I get access to the gateway engine?</h3>
<p>The gateway engine is proprietary and released through our design-partner programme under NDA. Book an assessment and we will scope policy gates and evidence requirements for your environment.</p>
</div>
<div class="faq-item">
<h3>Is WitnessOS open source?</h3>
<p>The SDK, the receipt specification and the public documentation are open. The gateway engine is proprietary, covered by patent pending, and available to design partners under NDA.</p>
</div>
</section>
"""
rep('running the agent itself.</p>\n</div>\n</section>', 'running the agent itself.</p>\n</div>\n' + faq_extra, "faq extras")

OUT.write_text(html)
print(f"wrote {OUT} ({len(html)} chars)")
