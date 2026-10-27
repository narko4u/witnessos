"""Replace the site footer with the Empire Labs banner plate plus a live link bar.

The banner artwork keeps its own chevron frame: the baked-in labels were painted out
(inpaint-footer-text.py) and a real anchor row is positioned inside the frame, so the
footer looks exactly like the supplied artwork but every item is a working link.

Below 700px the frame is too small to hold legible text, so the artwork is cropped
above the frame and the links become a stacked list under it.

Run from the repo root. Idempotent: every rule starting with `footer.empire` is
dropped and re-inserted, so it is safe to re-run. Generated pages read their footer
from _navy-exemplar.html, which this also edits.
"""
import pathlib
import re
import sys

FILES = [
    "_navy-exemplar.html",
    "publish-v2/index.html",
    "publish-v2/privacy.html",
    "publish-v2/terms.html",
]

# The old footer styling, still present in files not yet touched by this script.
LEGACY_CSS = """footer{padding:30px 0;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:22px;flex-wrap:wrap;color:var(--muted);font-size:var(--floor)}
footer .empire-banner{width:100%;height:auto;object-fit:contain;border-radius:8px;border:1px solid var(--line)}
footer a{color:var(--text)}"""

NEW_CSS = """footer.empire{padding:0 0 34px;display:block;color:var(--muted)}
footer.empire .empire__plate{position:relative;container-type:inline-size;display:block}
footer.empire .empire__art{display:block;width:100%;height:auto;object-fit:contain;border:1px solid var(--line);border-radius:8px}
footer.empire .empire__bar{position:absolute;left:4.4%;right:4.9%;top:75.4%;height:12.7%;display:flex;align-items:center;justify-content:flex-end;font-size:1.09cqw;line-height:1}
footer.empire .empire__bar > *{position:relative;padding:0 0.55em;white-space:nowrap}
footer.empire .empire__bar > * + *::before{content:"";position:absolute;left:0;top:50%;width:1px;height:1.05em;margin-top:-0.52em;background:rgba(85,199,255,.38)}
footer.empire .empire__legal{color:#cfe0f0}
footer.empire .empire__bar a{color:var(--accent)}
footer.empire .empire__bar a:hover,footer.empire .empire__bar a:focus-visible{color:#fff}
@media(max-width:1120px){footer.empire .empire__art{aspect-ratio:1280/322;object-fit:cover;object-position:top}
footer.empire .empire__bar{position:relative;left:auto;right:auto;top:auto;height:auto;margin-top:16px;flex-wrap:wrap;justify-content:flex-start;font-size:12.5px;line-height:1.5;padding:16px 0 0}
footer.empire .empire__bar::before{content:"";position:absolute;left:0;right:0;top:0;height:1px;background:linear-gradient(90deg,rgba(85,199,255,0),rgba(85,199,255,.85) 5%,rgba(163,227,255,.95) 50%,rgba(85,199,255,.85) 95%,rgba(85,199,255,0));box-shadow:0 0 9px rgba(85,199,255,.45)}
footer.empire .empire__legal{opacity:.8;letter-spacing:.08em;padding-bottom:4px}
footer.empire .empire__bar > *{flex:1 0 100%;padding:2px 0}
footer.empire .empire__bar > * + *::before{display:none}}"""

FOOTER = """<footer class="empire">
<div class="empire__plate">
<img class="empire__art" src="assets/empire-footer.webp" width="1280" height="455" loading="lazy" alt="Empire Labs Pty Ltd and WitnessOS. WitnessOS is the runtime governance layer for autonomous agents.">
<div class="empire__bar">
<span class="empire__legal">Legal:</span>
<a href="terms.html">Terms of Service</a>
<a href="privacy.html">Privacy Policy</a>
<a href="https://www.empirelabs.com.au">www.empirelabs.com.au</a>
<a href="mailto:contact@empirelabs.com.au">contact@empirelabs.com.au</a>
<a href="https://github.com/narko4u/witnessos">github.com/narko4u/witnessos</a>
</div>
</div>
</footer>"""

FOOTER_RE = re.compile(r"<footer[^>]*>.*?</footer>", re.S)


def rewrite_css(text: str) -> tuple[str, bool]:
    if LEGACY_CSS in text:
        text = text.replace(LEGACY_CSS, NEW_CSS)
        return text, True

    lines = text.split("\n")
    kept, first = [], None
    for line in lines:
        if line.startswith("footer.empire") or line.startswith("@media(max-width:1120px){footer.empire"):
            if first is None:
                first = len(kept)
            continue
        kept.append(line)
    if first is None:
        return text, False
    kept[first:first] = NEW_CSS.split("\n")
    return "\n".join(kept), True


def main() -> int:
    failures = 0
    for rel in FILES:
        path = pathlib.Path(rel)
        text = path.read_text()
        before = text
        text, changed = rewrite_css(text)
        if not changed:
            print(f"FAIL {rel}: no footer CSS found to replace")
            failures += 1
            continue
        if not FOOTER_RE.search(text):
            print(f"FAIL {rel}: no <footer> block")
            failures += 1
            continue
        text = FOOTER_RE.sub(lambda _m: FOOTER, text, count=1)
        if text != before:
            path.write_text(text)
            print(f"ok   {rel}")
        else:
            print(f"skip {rel} (unchanged)")
    print(f"failures: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
