#!/usr/bin/env python3
"""Prove the local build is what https://witnessos.com.au is actually serving.

The host rewrites internal links into extensionless pretty URLs at the edge, and while
doing so it re-serialises the anchors it touches: attributes come out single-quoted and in
a different order, and a stray space before `>` is dropped. None of that is a content
difference, so the comparison is made on a canonical form:

  * internal links mapped back to <name>.html and `/` to index.html
  * attributes parsed, sorted by name and re-rendered as name="value"
  * whitespace before a tag close removed

Anything that survives that is a real difference between the build and the live page, so a
pass here means the deployed site came from this tree.

Usage:
    python3 build_and_verify.py
    python3 verify_live_equivalence.py [--dist dist] [--snapshot DIR] [--base https://...]

Exit status is 0 only when every page still in dist/ matches production after
canonicalisation.
"""
import argparse
import hashlib
import pathlib
import re
import subprocess
import sys
import tempfile

VOID_SKIP = {"meta", "link", "br", "img", "hr", "input", "source", "area", "base", "col",
             "embed", "param", "track", "wbr"}
ATTR = re.compile(r"([a-zA-Z_:][-a-zA-Z0-9_:.]*)(?:\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s\"'>]+))?")


def _canon_tag(match, stems):
    raw = match.group(0)
    inner = raw[1:-1].strip()
    if inner.startswith("/"):
        return "</%s>" % inner[1:].strip().lower()
    self_close = inner.endswith("/")
    if self_close:
        inner = inner[:-1].rstrip()
    name_match = re.match(r"([a-zA-Z][-a-zA-Z0-9]*)", inner)
    if not name_match:
        return raw
    name = name_match.group(1).lower()
    attrs = []
    for am in ATTR.finditer(inner[name_match.end():]):
        key = am.group(1).lower()
        val = am.group(2)
        if val is None:
            attrs.append((key, ""))
            continue
        if val[:1] in "\"'":
            val = val[1:-1]
        if key == "href":
            if val == "/":
                val = "index.html"
            else:
                stem = val.lstrip("/")
                if "/" not in stem and stem in stems:
                    val = "%s.html" % stem
        attrs.append((key, val.replace('"', "&quot;")))
    attrs.sort()
    rendered = " ".join('%s="%s"' % (k, v) for k, v in attrs)
    out = "<%s%s" % (name, (" " + rendered) if rendered else "")
    return out + (" />" if self_close else ">")


def canon(html, stems):
    return re.sub(r"<[^>]+>", lambda m: _canon_tag(m, stems), html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dist", default="dist")
    ap.add_argument("--snapshot", default=None)
    ap.add_argument("--base", default="https://witnessos.com.au")
    args = ap.parse_args()

    dist = pathlib.Path(args.dist)
    if not dist.is_dir():
        raise SystemExit("no build directory at %s: run build_and_verify.py first" % dist)
    snap = pathlib.Path(args.snapshot) if args.snapshot else pathlib.Path(
        tempfile.mkdtemp(prefix="witnessos-live-"))
    snap.mkdir(parents=True, exist_ok=True)

    pages = sorted(p.name for p in dist.glob("*.html"))
    stems = {p[:-5] for p in pages}
    rows, problems = [], []

    for name in pages:
        local = (dist / name).read_text(encoding="utf-8")
        cached = snap / name
        if not cached.exists():
            proc = subprocess.run(
                ["curl", "-sSL", "--max-time", "30", "-o", str(cached), "-w", "%{http_code}",
                 "%s/%s" % (args.base, name)], capture_output=True, text=True)
            if proc.stdout.strip() != "200":
                problems.append((name, "live HTTP %s" % proc.stdout.strip()))
                continue
        live = cached.read_text(encoding="utf-8")
        a, b = canon(local, stems), canon(live, stems)
        rows.append((name, a == b, len(local), len(live), a))
        if a != b:
            al, bl = a.splitlines(), b.splitlines()
            first = next((i for i, (x, y) in enumerate(zip(al, bl)) if x != y),
                         min(len(al), len(bl)))
            detail = ""
            if first < min(len(al), len(bl)):
                detail = "\n      build: %s\n      live : %s" % (al[first][:150], bl[first][:150])
            problems.append((name, "first difference at canonical line %d%s" % (first + 1, detail)))

    for name, ok, lb, ll, a in rows:
        print("%-22s %-5s build=%6d live=%6d canon=%6d" % (name, "MATCH" if ok else "DIFF", lb, ll, len(a)))
    matched = sum(1 for r in rows if r[1])
    print("\npages=%d matched=%d" % (len(rows), matched))
    if problems:
        print("differences:")
        for name, why in problems:
            print("  %-22s %s" % (name, why))
        return 1

    digest = hashlib.sha256()
    for name, *_ in sorted(rows):
        digest.update(canon((dist / name).read_text(encoding="utf-8"), stems).encode())
    print("canonical build digest %s" % digest.hexdigest())
    print("VERDICT: this build is what %s is serving" % args.base)
    return 0


if __name__ == "__main__":
    sys.exit(main())
