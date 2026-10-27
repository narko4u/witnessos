#!/usr/bin/env python3
"""Raise every font size on witnessos.com.au to the kernel-line floor.

Eddie 2026-09-17: "WitnessOS is not an operating system for machines..." (.lead)
becomes the smallest type anywhere on the site. Anything currently smaller is
raised to that size. Titles, subtitles and tables keep their current sizes.

The floor is a CSS variable so the two breakpoints stay locked to .lead:
  desktop  --floor: 20px   (.lead is 20px)
  <=650px  --floor: 18px   (.lead is 18px)

Run with --dry to list changes without writing.
"""
import sys, pathlib

BASE = pathlib.Path(__file__).resolve().parent
PUB = BASE / "publish-v2"
BODIES = BASE / "_bodies"

HEAD_FILES = ["_NAVY_HEAD.html", "_navy-exemplar.html",
              "publish-v2/index.html", "publish-v2/terms.html", "publish-v2/privacy.html"]
SUB_FILES = ["_navy-exemplar.html", "publish-v2/terms.html", "publish-v2/privacy.html"]

# ---- base theme (every page family) -----------------------------------------
BASE_EDITS = [
    (":root{color-scheme:dark;--bg:#07101d;",
     ":root{color-scheme:dark;--floor:20px;--bg:#07101d;"),

    ('font:16px/1.65 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}',
     'font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;'
     'font-size:var(--floor);line-height:1.65}'),

    (".nav nav{display:flex;align-items:center;gap:24px;color:var(--muted);font-size:14px}",
     ".nav nav{display:flex;align-items:center;gap:24px;color:var(--muted);font-size:var(--floor)}"),

    ("background:var(--accent);color:#03111e;font-weight:750;font-size:14px}",
     "background:var(--accent);color:#03111e;font-weight:750;font-size:var(--floor)}"),

    (".eyebrow{color:var(--accent);font:700 12px/1.5 ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase}",
     ".eyebrow{color:var(--accent);font-family:ui-monospace,monospace;font-weight:700;"
     "font-size:var(--floor);line-height:1.5;letter-spacing:.14em;text-transform:uppercase}"),

    ("margin-bottom:8px;font:12px ui-monospace,monospace;color:var(--muted)}",
     "margin-bottom:8px;font-family:ui-monospace,monospace;font-size:var(--floor);color:var(--muted)}"),

    (".row{padding:11px 0;border-bottom:1px solid #1d344c;font:13px ui-monospace,monospace}",
     ".row{padding:11px 0;border-bottom:1px solid #1d344c;font-family:ui-monospace,monospace;"
     "font-size:var(--floor)}"),

    ("color:#8ea8bd;font:12px/1.75 ui-monospace,monospace;overflow-wrap:anywhere}",
     "color:#8ea8bd;font-family:ui-monospace,monospace;font-size:var(--floor);line-height:1.75;"
     "overflow-wrap:anywhere}"),

    (".receipt-foot{font:12px ui-monospace,monospace}",
     ".receipt-foot{font-family:ui-monospace,monospace;font-size:var(--floor)}"),

    (".num{font:700 12px ui-monospace,monospace;color:var(--accent)}",
     ".num{font-family:ui-monospace,monospace;font-weight:700;font-size:var(--floor);"
     "color:var(--accent)}"),

    (".rung span,.assurance span{color:var(--muted);font-size:14px}",
     ".rung span,.assurance span{color:var(--muted);font-size:var(--floor)}"),

    (".cap code{color:var(--accent);font-size:12px}",
     ".cap code{color:var(--accent);font-size:var(--floor)}"),

    (".proof strong{display:block;font-size:18px;line-height:1.25}",
     ".proof strong{display:block;font-size:var(--floor);line-height:1.25}"),

    ("flex-wrap:wrap;color:var(--muted);font-size:13px}",
     "flex-wrap:wrap;color:var(--muted);font-size:var(--floor)}"),

    ("color:var(--accent);font:700 13px/1.4 ui-monospace,monospace;letter-spacing:.02em}",
     "color:var(--accent);font-family:ui-monospace,monospace;font-weight:700;"
     "font-size:var(--floor);line-height:1.4;letter-spacing:.02em}"),

    ("color:var(--muted);font:400 13px/1.4 ui-sans-serif,system-ui,sans-serif;letter-spacing:0}",
     "color:var(--muted);font-family:ui-sans-serif,system-ui,sans-serif;font-weight:400;"
     "font-size:var(--floor);line-height:1.4;letter-spacing:0}"),

    ("@media(max-width:650px){.wrap{width:min(92%,560px)}",
     "@media(max-width:650px){:root{--floor:18px}\n.wrap{width:min(92%,560px)}"),
]

# ---- sub-page extras (prose, toc) -------------------------------------------
SUB_EDITS = [
    ("font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.9em;background:#0a1726",
     "font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:var(--floor);"
     "background:#0a1726"),

    ("font-size:13px;line-height:1.7;color:#8ea8bd}",
     "font-size:var(--floor);line-height:1.7;color:#8ea8bd}"),

    ("border-radius:999px;color:var(--muted);font-size:13px}",
     "border-radius:999px;color:var(--muted);font-size:var(--floor)}"),
]

# ---- per-page css -----------------------------------------------------------
PAGE_EDITS = {
    "_bodies/casestudy.css": [
        (".metric span{color:var(--muted);font-size:14px;line-height:1.4}",
         ".metric span{color:var(--muted);font-size:var(--floor);line-height:1.4}"),
        (".quote footer{margin-top:14px;color:var(--muted);font-size:14px;",
         ".quote footer{margin-top:14px;color:var(--muted);font-size:var(--floor);"),
    ],
    "_bodies/pricing.css": [
        (".plan .plan-desc{color:var(--muted);font-size:14px;margin-bottom:18px}",
         ".plan .plan-desc{color:var(--muted);font-size:var(--floor);margin-bottom:18px}"),
        (".plan .price-sub{color:var(--muted);font-size:13px;margin:2px 0 18px}",
         ".plan .price-sub{color:var(--muted);font-size:var(--floor);margin:2px 0 18px}"),
        ("position:relative;color:var(--muted);font-size:14px;",
         "position:relative;color:var(--muted);font-size:var(--floor);"),
        (".faq-question{font-weight:600;color:var(--text);cursor:pointer;font-size:17px}",
         ".faq-question{font-weight:600;color:var(--text);cursor:pointer;font-size:var(--floor)}"),
        (".faq-answer{display:none;margin-top:10px;color:var(--muted);font-size:15px}",
         ".faq-answer{display:none;margin-top:10px;color:var(--muted);font-size:var(--floor)}"),
    ],
    "_bodies/signup.css": [
        (".form-benefit p{margin:0;color:var(--muted);font-size:14px}",
         ".form-benefit p{margin:0;color:var(--muted);font-size:var(--floor)}"),
        (".field label{display:block;color:var(--text);font-size:13px;font-weight:700;margin-bottom:6px}",
         ".field label{display:block;color:var(--text);font-size:var(--floor);font-weight:700;"
         "margin-bottom:6px}"),
        (".field .err{display:none;color:#ff8a8a;font-size:12px;margin-top:4px}",
         ".field .err{display:none;color:#ff8a8a;font-size:var(--floor);margin-top:4px}"),
        (".form-note{color:var(--muted);font-size:12px;margin:18px 0 0}",
         ".form-note{color:var(--muted);font-size:var(--floor);margin:18px 0 0}"),
        ("color:var(--text);font:15px/1.5 Inter,ui-sans-serif,system-ui,sans-serif;resize:vertical}",
         "color:var(--text);font-family:Inter,ui-sans-serif,system-ui,sans-serif;"
         "font-size:var(--floor);line-height:1.5;resize:vertical}"),
    ],
    # The simulation console: every label, badge, chip and button to the floor.
    # Only the h2/h4 headings keep their own sizes (titles and subtitles).
    "_bodies/demo.css": [
        # `.sim-top .brand` (the console wordmark) is a LOGO -- it keeps its own
        # size and must NOT be raised (Eddie 2026-09-17: titles, subtitles,
        # logos, images and tables are exempt from the floor).
        ("border-radius:20px;font-size:.72rem;", "border-radius:20px;font-size:var(--floor);"),
        ("padding:10px 14px;font-size:13px;", "padding:10px 14px;font-size:var(--floor);"),
        (".demo-shell .sidebar-section h3{font-size:.68rem;",
         ".demo-shell .sidebar-section h3{font-size:var(--floor);"),
        ("padding:6px 12px;font-size:.72rem;", "padding:6px 12px;font-size:var(--floor);"),
        (".demo-shell .mode-desc{font-size:.72rem;", ".demo-shell .mode-desc{font-size:var(--floor);"),
        ("border-radius:6px;font-size:.78rem;", "border-radius:6px;font-size:var(--floor);"),
        ("color:var(--text-heading);font-size:.75rem;font-family:ui-monospace",
         "color:var(--text-heading);font-size:var(--floor);font-family:ui-monospace"),
        ("monospace;font-size:.72rem;color:var(--text-heading);font-weight:500}",
         "monospace;font-size:var(--floor);color:var(--text-heading);font-weight:500}"),
        (".demo-shell .case-item .ci-type{font-size:.65rem;",
         ".demo-shell .case-item .ci-type{font-size:var(--floor);"),
        (".demo-shell .case-item .ci-meta{font-size:.68rem;",
         ".demo-shell .case-item .ci-meta{font-size:var(--floor);"),
        ("border-radius:3px;font-size:.65rem;font-weight:500}", "border-radius:3px;"
         "font-size:var(--floor);font-weight:500}"),
        (".demo-shell .ci-actions button{padding:3px 10px;font-size:.68rem;",
         ".demo-shell .ci-actions button{padding:3px 10px;font-size:var(--floor);"),
        (".demo-shell .empty-state p{color:var(--text-dim);font-size:.85rem;",
         ".demo-shell .empty-state p{color:var(--text-dim);font-size:var(--floor);"),
        (".demo-shell .detail-header .dh-meta{font-size:.75rem;",
         ".demo-shell .detail-header .dh-meta{font-size:var(--floor);"),
        (".demo-shell .tl-content .tl-type{font-size:.72rem;",
         ".demo-shell .tl-content .tl-type{font-size:var(--floor);"),
        (".demo-shell .tl-content .tl-detail{font-size:.72rem;",
         ".demo-shell .tl-content .tl-detail{font-size:var(--floor);"),
        (".demo-shell .tl-content .tl-time{font-size:.65rem;",
         ".demo-shell .tl-content .tl-time{font-size:var(--floor);"),
        ("font-size:.58rem;color:var(--text-dim);max-width:160px;",
         "font-size:var(--floor);color:var(--text-dim);max-width:160px;"),
        (".demo-shell .chain-arrow{color:var(--text-dim);font-size:.6rem}",
         ".demo-shell .chain-arrow{color:var(--text-dim);font-size:var(--floor)}"),
        ("monospace;font-size:.68rem;color:var(--text-body);overflow-x:auto;",
         "monospace;font-size:var(--floor);color:var(--text-body);overflow-x:auto;"),
        ("border-radius:6px;font-size:.72rem;background:var(--bg-card)",
         "border-radius:6px;font-size:var(--floor);background:var(--bg-card)"),
        ("padding:8px 16px;font-size:.75rem;font-weight:500;",
         "padding:8px 16px;font-size:var(--floor);font-weight:500;"),
    ],
    # JS-rendered empty/error strings inside the console
    "_bodies/demo.body.html": [
        ("font-size: .78rem", "font-size: var(--floor)"),
        ("font-size:.78rem", "font-size:var(--floor)"),
    ],
}


def apply(path, edits, dry):
    p = BASE / path
    if not p.exists():
        print(f"  MISSING {path}")
        return 0
    s = p.read_text(encoding="utf-8")
    orig = s
    for old, new in edits:
        n = s.count(old)
        if n == 0:
            print(f"  ! no match in {path}: {old[:70]}...")
            continue
        s = s.replace(old, new)
        print(f"  {path}: {n}x  {old[:58]}... -> var(--floor)")
    if s != orig and not dry:
        p.write_text(s, encoding="utf-8")
    return 1 if s != orig else 0


def main():
    dry = "--dry" in sys.argv
    print(f"=== font floor {'(DRY RUN)' if dry else 'APPLY'} ===")
    print("-- base theme")
    for f in HEAD_FILES:
        print(f"[{f}]")
        apply(f, BASE_EDITS, dry)
    print("-- sub-page extras")
    for f in SUB_FILES:
        print(f"[{f}]")
        apply(f, SUB_EDITS, dry)
    print("-- per-page css")
    for f, edits in PAGE_EDITS.items():
        print(f"[{f}]")
        apply(f, edits, dry)
    print()
    print("done." if not dry else "dry run complete, nothing written.")


if __name__ == "__main__":
    main()
