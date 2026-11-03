"""One command, every leg.

    python3 eval/gate.py

Legs:

  freeze      corpus.tsv against the frozen manifest digest and case count
  oracle      the Python oracle against the frozen corpus (integrity: the oracle
              authored the corpus, so this only proves the file on disk is the
              file that was authored)
  rust        the corpus through `wire::dispatch`, the same function WASM calls
  js          the corpus through the plain-JavaScript wire
  browser     the corpus through the page in Chromium, which must be running the
              Rust core as WebAssembly
  import      the tester-import fixtures through the real binary

Every leg is required. A leg that cannot run is a failure, not a skip.
"""

import os
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
CORE = os.path.join(PROJECT, "core-rs")
CAPTURE = os.path.join(PROJECT, "apps", "capture")
sys.path.insert(0, HERE)

import oracle  # noqa: E402

PORT = 8134


def quiet_server(directory):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

        def log_message(self, format, *args):  # noqa: A002 - matches the parent signature
            pass

    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def load_corpus():
    path = os.path.join(HERE, "vectors", "corpus", "corpus.tsv")
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()

    def unescape(text):
        out, i = [], 0
        while i < len(text):
            ch = text[i]
            if ch != "\\":
                out.append(ch)
                i += 1
                continue
            nxt = text[i + 1] if i + 1 < len(text) else ""
            if nxt in ("n", "t", "\\"):
                out.append({"n": "\n", "t": "\t", "\\": "\\"}[nxt])
                i += 2
            else:
                out.append(ch)
                i += 1
        return "".join(out)

    cases = []
    for line in raw.split("\n")[1:]:
        if not line.strip():
            continue
        case_id, category, op, payload, expected = line.split("\t")
        want = unescape(expected)
        cases.append((case_id, category, int(op), unescape(payload), "" if want == "<empty>" else want))
    return cases


def leg_freeze():
    """The corpus is acceptance evidence: it must match the frozen manifest."""
    import hashlib
    import json

    corpus = os.path.join(HERE, "vectors", "corpus", "corpus.tsv")
    manifest_path = os.path.join(HERE, "vectors", "corpus", "MANIFEST.json")
    with open(corpus, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)
    cases = len(load_corpus())
    ok = digest == manifest["sha256"] and cases == manifest["cases"]
    if not ok:
        print(f"    digest {digest} vs manifest {manifest['sha256']}")
        print(f"    cases {cases} vs manifest {manifest['cases']}")
    return ok, f"v{manifest['version']} {manifest['sha256'][:16]}... {cases} cases"


def leg_oracle():
    cases = load_corpus()
    bad = [c for c in cases if oracle.dispatch(c[2], c[3]) != c[4]]
    for case_id, _cat, op, payload, want in bad[:5]:
        print(f"    {case_id} op {op} {payload!r}: expected {want!r}, got {oracle.dispatch(op, payload)!r}")
    return len(bad) == 0, f"{len(cases) - len(bad)}/{len(cases)} cases"


def run(cmd, cwd, label):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"    {label} exited {proc.returncode}")
        for line in (proc.stdout + proc.stderr).splitlines()[-12:]:
            print(f"    | {line}")
    return proc


def leg_rust():
    proc = run(["cargo", "test", "--quiet", "--test", "corpus"], CORE, "cargo test --test corpus")
    ok = proc.returncode == 0
    return ok, "200/200 cases" if ok else "failed"


def leg_js():
    proc = run(
        ["node", "--test", "tests/corpus.test.mjs"],
        HERE,
        "node --test tests/corpus.test.mjs",
    )
    ok = proc.returncode == 0
    return ok, "200/200 cases" if ok else "failed"


def leg_browser():
    server = quiet_server(CAPTURE)
    try:
        url = f"http://127.0.0.1:{PORT}/index.html"
        proc = run([sys.executable, os.path.join(HERE, "e2e", "corpus_gate.py"), "--url", url], PROJECT, "corpus_gate.py")
    finally:
        server.shutdown()
    ok = proc.returncode == 0
    engine = ""
    for line in proc.stdout.splitlines():
        if line.startswith("engine"):
            engine = line.split(None, 1)[1]
    return ok, f"200/200 through {engine or 'unknown engine'}" if ok else "failed"


def leg_import():
    a = run(["cargo", "test", "--quiet", "--test", "tester_import"], CORE, "cargo test --test tester_import")
    b = run([sys.executable, os.path.join(HERE, "tester_import_gate.py")], PROJECT, "tester_import_gate.py")
    ok = a.returncode == 0 and b.returncode == 0
    checks = ""
    for line in b.stdout.splitlines():
        if line.startswith("checks"):
            checks = line
    return ok, checks or "failed"


def main():
    legs = [
        ("freeze", leg_freeze),
        ("oracle", leg_oracle),
        ("rust", leg_rust),
        ("js", leg_js),
        ("browser", leg_browser),
        ("import", leg_import),
    ]
    print("VoltLedger gate")
    print()
    results = []
    for name, fn in legs:
        print(f"  {name} ...")
        ok, detail = fn()
        results.append((name, ok, detail))
        print(f"  {'PASS' if ok else 'FAIL'}  {name:8s} {detail}")
    failed = [name for name, ok, _ in results if not ok]
    print()
    if failed:
        print(f"GATE FAILED: {', '.join(failed)}")
        return 1
    print("GATE PASSED: oracle, native Rust, JavaScript and the browser agree on all 200 cases,")
    print("and the tester import refuses what it cannot verify.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
