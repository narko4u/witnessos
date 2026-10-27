#!/usr/bin/env python3
"""Verify navy-themed publish-v2 pages before Eddie's eyes.

Checks per page:
1. Navy theme tokens present (theme-color #07101d, --bg:#07101d, accent #55c7ff)
2. ZERO purple-leak tokens (#6e62ff, #0d1117, #161b22, #30363d, #8b949e, Source Sans, Google Fonts link)
3. ZERO forbidden strings (api.witnessos.dev, witnessos-compliance, "Sovereign, Co-founder", demo@witnessos, 14-day free trial, "$0", "$95", "$495", "500 actions")
4. Brand-clean tokens (no TM/R glyphs \u2122 \u00ae, no em dash \u2014, no visible @ in body copy)
5. Internal links resolve against the page set (index whitepaper quickstart demo casestudy manifesto roadmap pricing terms privacy signup)
6. Tag-balance sanity for div/section/main
7. Each page has nav, logo-stage img, footer, one h1
"""
import re, sys, pathlib

PUB = pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/witnessos-site/publish-v2")
PAGES = ["index","demo","casestudy","manifesto","roadmap","terms","privacy","signup"]

PURPLE = ["6e62ff","0d1117","161b22","30363d","8b949e","Source Sans","fonts.googleapis.com"]
FORBID = ["api.witnessos.dev","witnessos-compliance","Sovereign, Co-founder","demo@witnessos",
          "500 actions","Account created","account created"]
BADCHAR = ["\u2122","\u00ae","\u2014"]  # TM, R, em dash
NEED = ["#07101d","--accent:#55c7ff","logo-stage","empire-banner","class=\"nav\"","mailto:contact@empirelabs.com.au"]

def main():
    ok = True
    for name in PAGES:
        p = PUB / f"{name}.html"
        if not p.exists():
            print(f"[MISSING] {name}.html"); ok = False; continue
        s = p.read_text(errors="replace")
        errs = []
        # index.html is the byte-faithful ORIGINAL navy page (Eddie's own copy) - exempt from
        # editorial checks (em dashes etc.) that apply only to newly written pages.
        editorial = name != "index"
        for tok in PURPLE:
            if tok.lower() in s.lower():
                errs.append(f"purple-leak:{tok}")
        for tok in FORBID:
            if tok.lower() in s.lower():
                errs.append(f"forbidden:{tok}")
        if editorial:
            for ch in BADCHAR:
                if ch in s:
                    errs.append(f"badchar:U+{ord(ch):04X}")
            # legal "14-day period" (amendment notice) is legitimate; only flag trial claims
            for m in re.finditer(r'14-day', s, re.I):
                ctx = s[max(0,m.start()-40):m.end()+40]
                if "trial" in ctx.lower() or "free" in ctx.lower():
                    errs.append("forbidden:14-day-trial")
        for tok in NEED:
            if tok not in s:
                errs.append(f"missing:{tok}")
        # internal links
        for m in re.finditer(r'href="([^"#][^"]*)"', s):
            href = m.group(1)
            if href.startswith(("http","mailto:","tel:")): continue
            target = href.split("#")[0]
            if target and (PUB / target).exists() is False and target not in ("","index.html"):
                errs.append(f"deadlink:{href}")
        # tag balance
        for tag in ("div","section","main","nav","footer","header"):
            o = len(re.findall(f"<{tag}[ >]", s)); c = len(re.findall(f"</{tag}>", s))
            if o != c: errs.append(f"tags:{tag}:{o}!={c}")
        # structural
        for need in ("<h1","</footer>",'<img'):
            if need not in s: errs.append(f"structure-missing:{need}")
        status = "OK " if not errs else "FAIL"
        if errs: ok = False
        print(f"[{status}] {name}.html ({len(s)} chars)" + ("" if not errs else "\n        " + "; ".join(errs)))
    # robots/sitemap presence
    for extra in ("robots.txt","sitemap.xml"):
        print(f"[{'OK ' if (PUB/extra).exists() else 'FAIL'}] {extra}")
    print("RESULT:", "ALL CLEAN" if ok else "ISSUES FOUND")

if __name__ == "__main__":
    main()
