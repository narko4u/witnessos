#!/usr/bin/env python3
"""Score a competitive-engineering candidate set against the MOP section 7 rubric.

Scores are computed here, never summed by hand, so the register and the ranking
cannot drift apart. Sub-scores above their cap are an error, not a typo to fix
later.

Usage:
    python3 score.py <scores.json> [--top 10]
"""

import argparse
import json
import sys

CAPS = {"rev": 20, "build": 15, "diff": 20, "migr": 10,
        "weak": 10, "reuse": 10, "support": 5, "ip": 10}


def threshold(total: int) -> str:
    if total >= 80:
        return "BUILD CANDIDATE"
    if total >= 65:
        return "RESEARCH"
    if total >= 50:
        return "WATCH"
    return "REJECT"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--top", type=int, default=10)
    args = ap.parse_args()

    with open(args.path, encoding="utf-8") as fh:
        rows = json.load(fh)

    errors = []
    for r in rows:
        for k, cap in CAPS.items():
            v = r.get(k)
            if not isinstance(v, int) or v < 0 or v > cap:
                errors.append(f"{r.get('id')}: {k}={v} outside 0..{cap}")
    if errors:
        print("rubric violations:")
        for e in errors:
            print("  " + e)
        return 1

    scored = []
    for r in rows:
        total = sum(r[k] for k in CAPS)
        scored.append((total, r["id"], r["name"], r.get("note", "")))
    scored.sort(reverse=True)

    print(f"{'#':>3} {'id':>3} {'score':>5}  {'band':<16} name")
    for i, (total, cid, name, note) in enumerate(scored, 1):
        flag = "  <- " + note if note else ""
        print(f"{i:>3} {cid:>3} {total:>5}  {threshold(total):<16} {name}{flag}")

    print()
    print(f"candidates: {len(scored)}  bands: "
          f"BUILD {sum(1 for s in scored if s[0] >= 80)}, "
          f"RESEARCH {sum(1 for s in scored if 65 <= s[0] < 80)}, "
          f"WATCH {sum(1 for s in scored if 50 <= s[0] < 65)}, "
          f"REJECT {sum(1 for s in scored if s[0] < 50)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
