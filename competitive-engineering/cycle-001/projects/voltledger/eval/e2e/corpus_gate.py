"""Browser gate for the 200-case corpus.

Loads the real capture page in Chromium, confirms the page is running the Rust
core compiled to WebAssembly (not the JavaScript fallback), then pushes all 200
cases through the page's own wire entry point and compares the strings the
browser produced against the frozen corpus.

Any disagreement fails the gate. There is no tolerance list.

    python3 corpus_gate.py [--url http://127.0.0.1:8123/index.html]
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
EVAL = os.path.dirname(HERE)
CORPUS = os.path.join(EVAL, "vectors", "corpus", "corpus.tsv")
RESULTS = os.path.join(EVAL, "results")
CHROME = "/home/vault/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome"


def unescape(text):
    out, i = [], 0
    while i < len(text):
        ch = text[i]
        if ch != "\\":
            out.append(ch)
            i += 1
            continue
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if nxt == "n":
            out.append("\n")
            i += 2
        elif nxt == "t":
            out.append("\t")
            i += 2
        elif nxt == "\\":
            out.append("\\")
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def load_cases():
    with open(CORPUS, encoding="utf-8") as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    cases = []
    for line in raw.split("\n")[1:]:
        if not line.strip():
            continue
        case_id, category, op, payload, expected = line.split("\t")
        want = unescape(expected)
        cases.append(
            {
                "case_id": case_id,
                "category": category,
                "op": int(op),
                "payload": unescape(payload),
                "expected": "" if want == "<empty>" else want,
            }
        )
    return cases, sha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8123/index.html")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    cases, sha = load_cases()
    if len(cases) != 200:
        raise SystemExit(f"corpus has {len(cases)} cases, expected 200")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=True, executable_path=CHROME, args=["--no-sandbox"]
        )
        page = browser.new_page()
        page.goto(args.url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_function("() => window.__volt !== undefined", timeout=20000)
        engine = page.evaluate("() => window.__volt.engine()")

        results = page.evaluate(
            """(cases) => cases.map((c) => {
                try { return window.__volt.run(c.op, c.payload); }
                catch (err) { return `THREW ${err.message}`; }
            })""",
            cases,
        )
        version = browser.version
        browser.close()

    failures = []
    by_category = {}
    for case, got in zip(cases, results):
        cat = by_category.setdefault(case["category"], {"cases": 0, "failed": 0})
        cat["cases"] += 1
        if got != case["expected"]:
            cat["failed"] += 1
            failures.append(
                {
                    "case_id": case["case_id"],
                    "category": case["category"],
                    "op": case["op"],
                    "payload": case["payload"],
                    "expected": case["expected"],
                    "got": got,
                }
            )

    record = {
        "gate": "corpus-200-browser",
        "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "url": args.url,
        "browser": f"chromium {version}",
        "engine": engine,
        "corpus_sha256": sha,
        "cases": len(cases),
        "passed": len(cases) - len(failures),
        "failed": len(failures),
        "by_category": by_category,
        "failures": failures[:20],
    }
    os.makedirs(RESULTS, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out = os.path.join(RESULTS, f"corpus-{stamp}.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"engine   {engine}")
    print(f"corpus   {sha}")
    print(f"cases    {len(cases)}  passed {record['passed']}  failed {record['failed']}")
    for cat in sorted(by_category):
        row = by_category[cat]
        mark = "ok  " if row["failed"] == 0 else "FAIL"
        print(f"  {mark} {cat:24s} {row['cases']:3d} cases, {row['failed']} failed")
    for f in failures[:10]:
        print(f"\n{f['case_id']} [{f['category']}] op {f['op']}")
        print(f"  payload  {f['payload']!r}")
        print(f"  expected {f['expected']!r}")
        print(f"  got      {f['got']!r}")
    print(f"\nrecord   {out}")

    if engine != "rust-wasm":
        print(f"\nGATE FAILED: the page is running {engine}, not the Rust core")
        return 1
    if failures:
        print(f"\nGATE FAILED: {len(failures)} of {len(cases)} browser results disagree")
        return 1
    print("\nGATE PASSED: browser, WASM and the frozen corpus agree on 200 of 200")
    return 0


if __name__ == "__main__":
    sys.exit(main())
