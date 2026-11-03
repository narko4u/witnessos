"""Compare two corpora.

    python3 corpus_diff.py corpus/v1/corpus.tsv corpus/corpus.tsv
    python3 corpus_diff.py corpus.v1.tsv corpus.tsv

Prints added, removed and changed vectors by case id, with the old and the new
expected bytes. A revision that cannot be summarised by this script is a revision
nobody can review.
"""

import io
import sys


def load(path):
    with io.open(path, encoding="utf-8") as fh:
        lines = [l for l in fh.read().split("\n") if l.strip()]
    header, rows = lines[0], lines[1:]
    return {row.split("\t")[0]: row.split("\t") for row in rows}


def unesc(text):
    out, i = [], 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and i + 1 < len(text) and text[i + 1] in ("n", "t", "\\"):
            out.append({"n": "\n", "t": "\t", "\\": "\\"}[text[i + 1]])
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__.strip())
    old_path, new_path = sys.argv[1], sys.argv[2]
    old, new = load(old_path), load(new_path)

    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = [cid for cid in sorted(set(old) & set(new)) if old[cid] != new[cid]]

    print(f"old {old_path}: {len(old)} cases")
    print(f"new {new_path}: {len(new)} cases")
    print(f"added {len(added)}  removed {len(removed)}  changed {len(changed)}")

    for cid in added:
        print(f"  + {cid} [{new[cid][1]}] op {new[cid][2]} {unesc(new[cid][3])!r} -> {unesc(new[cid][4])!r}")
    for cid in removed:
        print(f"  - {cid} [{old[cid][1]}] op {old[cid][2]} {unesc(old[cid][3])!r} -> {unesc(old[cid][4])!r}")
    for cid in changed:
        print(f"  ~ {cid} [{new[cid][1]}] op {new[cid][2]} {unesc(new[cid][3])!r}")
        print(f"      old {unesc(old[cid][4])!r}")
        print(f"      new {unesc(new[cid][4])!r}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
