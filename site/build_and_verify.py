#!/usr/bin/env python3
"""Build every navy page, then verify it: forbidden strings, tag balance,
internal links, copy hygiene. Writes dist/ for deploy. Read-only on the theme."""
import base64, hashlib, pathlib, re, shutil, subprocess, sys

BASE = pathlib.Path(__file__).resolve().parent
PUB = BASE / "publish-v2"
BODIES = BASE / "_bodies"
DIST = BASE / "dist"

PAGES = ["passport", "products", "instructions", "pricing", "demo", "casestudy",
         "manifesto", "roadmap", "signup", "pqc", "conformance"]

FORBIDDEN = ["6e62ff", "Source Sans", "api.witnessos.dev", "witnessos-compliance",
             "Sovereign, Co-founder", "demo@witnessos", "\u2122", "\u2014"]

print("=== BUILD ===")
for p in PAGES:
    r = subprocess.run([sys.executable, str(BASE / "assemble.py"), p],
                       capture_output=True, text=True, cwd=BASE)
    print((r.stdout or r.stderr).strip())

print()
print("=== VERIFY ===")
pages = sorted(PUB.glob("*.html"))
present = {f.name for f in pages}
fail = 0
for f in pages:
    s = f.read_text()
    probs = []
    for bad in FORBIDDEN:
        if bad in s:
            probs.append(f"forbidden string: {bad!r}")
    if s.count("<section") != s.count("</section>"):
        probs.append(f"section imbalance {s.count('<section')}/{s.count('</section>')}")
    if s.count("<div") != s.count("</div>"):
        probs.append(f"div imbalance {s.count('<div')}/{s.count('</div>')}")
    # internal links must resolve
    for href in set(re.findall(r'href="([^"#?:]+\.html)(?:#[^"]*)?"', s)):
        if href not in present:
            probs.append(f"dead internal link: {href}")
    # visible copy hygiene: strip tags + scripts before checking for @ and dashes
    body = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", body)
    stray_at = [a.rstrip(".") for a in re.findall(r"[\w.+-]+@[\w.-]+", text)
                if a.rstrip(".") not in ("contact@empirelabs.com.au",)]
    if stray_at:
        probs.append(f"unapproved email in copy: {stray_at[:2]}")
    if "\u2014" in text:
        probs.append("em dash in visible copy")
    if re.search(r"\bE5\b", text):
        probs.append("E5 referenced")
    status = "OK " if not probs else "FAIL"
    if probs:
        fail += 1
    print(f"{status} {f.name:22} {len(s):>7} chars  {'; '.join(probs[:3])}")

print()
print(f"pages checked: {len(pages)}  failures: {fail}")

print()
print("=== INDEX nav + internal links (homepage) ===")
idx = PUB / "index.html"
if idx.exists():
    si = idx.read_text()
    m = re.search(r'<nav aria-label="Main navigation">.*?</nav>', si, re.S)
    print("nav:", re.sub(r"\s+", " ", m.group(0))[:400] if m else "NO NAV")
    links = sorted(set(re.findall(r'href="([^"#?:]+\.html)', si)))
    print("internal links:", links)
    anchors = sorted(set(re.findall(r'href="(#[a-z-]+)"', si)))
    print("section anchors:", anchors)

print()
print("=== DIST (deploy dir) ===")
if DIST.exists():
    shutil.rmtree(DIST)
shutil.copytree(PUB, DIST, ignore=shutil.ignore_patterns("_bodies"))
n = len(list(DIST.rglob("*")))
print(f"dist refreshed: {n} entries, {sum(f.stat().st_size for f in DIST.rglob('*') if f.is_file())/1024:.0f} KB")

# --- traffic beacon -----------------------------------------------------------------
# Instrumentation is installed at build time, never hand-edited into a page, so a
# rebuild always reproduces it and a page can never drift out of coverage.
print()
print("=== TRAFFIC BEACON ===")
BEACON_SRC = BASE / "static-src" / "beacon.js"
BEACON_TAG = '<script src="/beacon.js" defer></script>'
if not BEACON_SRC.exists():
    print(f"FAIL beacon source missing: {BEACON_SRC}")
    fail += 1
else:
    shutil.copyfile(BEACON_SRC, DIST / "beacon.js")
    tagged = 0
    total = 0
    for f in sorted(DIST.rglob("*.html")):
        total += 1
        s = f.read_text()
        if BEACON_TAG in s:
            tagged += 1
            continue
        if "</body>" not in s:
            print(f"FAIL no </body> to attach the beacon in {f.name}")
            fail += 1
            continue
        f.write_text(s.replace("</body>", BEACON_TAG + "\n</body>", 1))
        tagged += 1
    print(f"beacon on {tagged}/{total} pages, served from /beacon.js")
    if tagged != total:
        print("FAIL beacon coverage is not complete")
        fail += 1

    # Tag genuine conversion actions only. Cross-page navigation gets no tag,
    # because moving between our own pages is not a conversion and tagging it
    # would turn the CTA numbers into noise.
    MAILTO_RE = re.compile(r'<a\b([^>]*?href="mailto:[^"]*"[^>]*?)>')

    def _tag_cta(m):
        attrs = m.group(1)
        if "data-cta=" in attrs:
            return m.group(0)
        subj = re.search(r'subject=([^"&]*)', attrs)
        slug = "contact"
        if subj:
            raw = subj.group(1).lower().replace("%20", " ")
            slug = re.sub(r"[^a-z0-9]+", "-", raw).strip("-")[:40] or "contact"
        return f'<a data-cta="cta:email:{slug}"{attrs}>'

    ctas = 0
    for f in sorted(DIST.rglob("*.html")):
        s = f.read_text()
        new = MAILTO_RE.sub(_tag_cta, s)
        if new != s:
            f.write_text(new)
            ctas += len(MAILTO_RE.findall(s))
    print(f"conversion anchors tagged: {ctas}")

# --- content security policy ---------------------------------------------------------
# The policy in netlify.toml names every inline script by its SHA-256 hash, so a page
# that gains, loses or edits one of those blocks would be refused by the browser with
# nothing else to show for it. The hashes are recomputed from the built pages here and
# compared against the policy, which turns that silent breakage into a build failure.
print()
print("=== CONTENT SECURITY POLICY ===")
NETLIFY_TOML = BASE / "netlify.toml"
csp_hashes = set()
for f in sorted(DIST.rglob("*.html")):
    for m in re.finditer(r"<script>(.*?)</script>", f.read_text(), re.S):
        digest = hashlib.sha256(m.group(1).encode()).digest()
        csp_hashes.add("sha256-" + base64.b64encode(digest).decode())

if not NETLIFY_TOML.exists():
    print("FAIL netlify.toml missing, so no policy is delivered")
    fail += 1
else:
    toml_text = NETLIFY_TOML.read_text()
    declared = set(re.findall(r"'(sha256-[A-Za-z0-9+/=]+)'", toml_text))
    missing = sorted(csp_hashes - declared)
    extra = sorted(declared - csp_hashes)
    for h in missing:
        print(f"FAIL inline script not named in the policy: {h}")
        fail += 1
    for h in extra:
        print(f"FAIL policy names a hash no page carries: {h}")
        fail += 1
    if not missing and not extra:
        print(f"policy pins {len(csp_hashes)} inline script hash(es), all present")
    for need in ("content-security-policy", "default-src 'self'", "frame-ancestors 'none'",
                 "base-uri 'self'", "object-src 'none'"):
        if need not in toml_text.lower():
            print(f"FAIL policy is missing {need!r}")
            fail += 1

print()
print(f"TOTAL FAILURES: {fail}")
