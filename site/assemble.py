#!/usr/bin/env python3
"""Assemble a navy page from shell (navybuild) + body fragment + optional page css.

Body fragments live in publish-v2/_bodies/<page>.body.html and contain ONLY the
content between the logo-stage and the footer (i.e. the <section> elements).
Optional page css at publish-v2/_bodies/<page>.css is injected into <head>.

Usage:
    python3 assemble.py pricing
Writes publish-v2/<page>.html
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from navybuild import navy_shell, PUB

BASE = pathlib.Path(__file__).resolve().parent
BODIES = BASE / "_bodies"

PAGES = {
    "passport": dict(title="WitnessOS | Passport",
        desc="Signed identity and scoped authority for autonomous agents. Issue locally, verify offline, fail closed by default.",
        label="Passport", canonical="passport.html"),
    "products": dict(title="WitnessOS | Products",
        desc="The WitnessOS family: verifiable identity and scoped authority for agents, independent verification of evidence bundles and declared-versus-observed MCP checks.",
        label="Products", canonical="products.html"),
    "instructions": dict(title="WitnessOS | Instructions",
        desc="Install and run the WitnessOS tools: verify offline, prove inclusion in an anchored receipt and check what an MCP server declares against what it does.",
        label="Instructions", canonical="instructions.html"),
    "pricing": dict(title="WitnessOS | Pricing",
        desc="Open-source tools are free. Assessments, audits, conformance mapping and adapter builds are priced per engagement. The engine is released to design partners.",
        label="Pricing", canonical="pricing.html"),
    "pqc": dict(title="WitnessOS | Post-Quantum Readiness",
        desc="Cryptographic inventory and an ISM-2073 transition plan for Australian government systems. A signed CBOM you can verify without trusting us.",
        label="Post-quantum", canonical="pqc.html"),
    "demo": dict(title="WitnessOS | Interactive Simulation",
        desc="Run the WitnessOS governed-action simulation in your browser. E0-E4 evidence grades, policy decisions, and signed receipts - fully client-side.",
        label="Simulation", canonical="demo.html"),
    "casestudy": dict(title="WitnessOS | Case Study",
        desc="How Empire Labs deploys WitnessOS as the operating layer for governed agent action - policy enforcement and RFC 3161 anchored evidence.",
        label="Case Study", canonical="casestudy.html"),
    "manifesto": dict(title="WitnessOS | Manifesto",
        desc="The WitnessOS manifesto: why autonomous agents need cryptographic proof at the action layer, not trust at the model layer.",
        label="Manifesto", canonical="manifesto.html"),
    "roadmap": dict(title="WitnessOS | Roadmap",
        desc="WitnessOS roadmap: hardened E4 evidence in WitnessOS Gateway v0.1.0 and witnessos-verifier v0.3.5. E4 requires legitimate E3 corroborated evidence plus independently authenticated external anchoring. Early-access engagements scaling to self-serve.",
        label="Roadmap", canonical="roadmap.html"),
    "signup": dict(title="WitnessOS | Request Early Access",
        desc="Request early access to the WitnessOS gateway engine. Design-partner deployments under NDA with direct engineering support.",
        label="Request Access", canonical="signup.html"),
    "standards": dict(title="WitnessOS | WitnessOS and Flinders",
        desc="Flinders is the engagement programme that defines what evidence must exist for AI assurance in Australia. WitnessOS is the product that produces it. The definition comes first.",
        label="WitnessOS and Flinders", canonical="standards.html"),
    "conformance": dict(title="WitnessOS | What a conformance record cannot establish",
        desc="A conformance record can prove it was not altered. It cannot prove the party who produced it was independent. The five limits, and the one independent check that survives them.",
        label="Conformance evidence", canonical="conformance.html"),
}

def main(page):
    meta = PAGES[page]
    body = (BODIES / f"{page}.body.html").read_text()
    css_path = BODIES / f"{page}.css"
    extra = css_path.read_text() if css_path.exists() else None
    top, bottom = navy_shell(meta["title"], meta["desc"], active_label=meta["label"],
                             canonical=meta["canonical"], extra_css=extra)
    out = top + "\n" + body + "\n" + bottom
    (PUB / f"{page}.html").write_text(out)
    print(f"wrote {PUB / f'{page}.html'} ({len(out)} chars)")

if __name__ == "__main__":
    main(sys.argv[1])
