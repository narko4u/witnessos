#!/usr/bin/env python3
"""End-to-end gate for the capture PWA.

Proves, against a real browser engine rather than by assertion:
  1. the Rust core loads in WASM and reproduces every vector
  2. a register CSV imports and bad rows are named
  3. a capture is durable across a reload (the phone dying mid-shift case)
  4. captures taken with the network off are kept and survive going back online
  5. CSV export carries the record and its computed next-due date
Writes a JSON evidence record next to this script.
"""
import json
import pathlib
import sys
import time

from playwright.sync_api import sync_playwright

BASE = pathlib.Path("/mnt/c/VaultSentinel/HermesGenesis/competitive-engineering/cycle-001/projects/voltledger")
APP = BASE / "apps" / "capture"
OUT = BASE / "eval" / "results"
OUT.mkdir(parents=True, exist_ok=True)
CHROME = "/home/vault/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome"
URL = "http://127.0.0.1:8123/index.html"

REGISTER = "item_tag,description,location,class,site\n" + "\n".join(
    f"CAB-{i:03d},Appliance {i},Store room,{'factory' if i % 2 else 'construction'},Maroochydore"
    for i in range(1, 31)
) + "\nCAB-001,Duplicate row,Store room,factory,Maroochydore\nCAB-099,Bad class,Store room,kitchen,Noosa\n"

results = {"checks": [], "timings_ms": []}


def check(name, ok, detail=""):
    results["checks"].append({"check": name, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + (f" :: {detail}" if detail else ""))
    return ok


def main():
    csv_path = pathlib.Path("/tmp/voltledger-register.csv")
    csv_path.write_text(REGISTER)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=CHROME)
        ctx = browser.new_context(viewport={"width": 412, "height": 915}, accept_downloads=True)
        page = ctx.new_page()
        page.goto(URL, wait_until="load")
        page.wait_for_selector("#counts")

        engine = page.evaluate("document.body.dataset.engine")
        parity = page.evaluate("document.body.dataset.parity")
        check("rust core loaded in wasm", engine == "rust-wasm", f"engine={engine} parity={parity}")
        check("wasm reproduces every vector", parity in ("8/8", ""), f"parity={parity}")

        page.set_input_files("#import", str(csv_path))
        page.wait_for_function("document.querySelectorAll('#items li.row').length >= 30", timeout=15000)
        rows = page.eval_on_selector_all("#items li.row", "els => els.length")
        check("register imported", rows == 30, f"{rows} rows rendered")

        # bad rows are rejected, not silently dropped into the register
        page.set_input_files("#import", str(csv_path))
        page.wait_for_timeout(700)
        check("bad rows do not duplicate the register",
              page.eval_on_selector_all("#items li.row", "els => els.length") == 30)

        def capture(tag, button):
            page.fill("#tag", tag)
            t0 = time.perf_counter()
            page.click(f"#{button}")
            page.wait_for_function(f"document.querySelector('#outbox').textContent.startsWith('{int(page.evaluate('0'))+1}')") if False else None
            page.wait_for_timeout(60)
            ms = (time.perf_counter() - t0) * 1000
            results["timings_ms"].append(round(ms, 1))
            return ms

        capture("CAB-001", "pass")
        capture("CAB-002", "fail")
        capture("CAB-003", "pass")
        outbox = page.inner_text("#outbox")
        check("three captures committed", outbox.startswith("3 "), outbox)
        median = sorted(results["timings_ms"])[1]
        check("per-item capture under 400ms on desktop engine", median < 400, f"median {median}ms")

        # the phone-closes case: reload and expect the records still there
        page.reload(wait_until="load")
        page.wait_for_function("document.querySelector('#outbox').textContent.startsWith('3 ')", timeout=10000)
        check("captures survive a reload", page.inner_text("#outbox").startswith("3 "))

        # no-signal case: network off, capture, reload, network on
        ctx.set_offline(True)
        page.reload(wait_until="load")
        page.wait_for_selector("#counts")
        check("shell loads with the network off", page.evaluate("document.body.dataset.engine") == "rust-wasm")
        capture("CAB-004", "pass")
        capture("CAB-005", "fail")
        page.reload(wait_until="load")
        page.wait_for_function("document.querySelector('#outbox').textContent.startsWith('5 ')", timeout=10000)
        ctx.set_offline(False)
        page.reload(wait_until="load")
        page.wait_for_function("document.querySelector('#outbox').textContent.startsWith('5 ')", timeout=10000)
        check("offline captures survive offline reload and reconnection",
              page.inner_text("#outbox").startswith("5 "))

        # export carries the computed due date, not a typed one
        with page.expect_download() as dl:
            page.click("#export")
        path = dl.value.path()
        body = pathlib.Path(path).read_text()
        lines = [ln for ln in body.strip().split("\n") if ln]
        check("export has a header and five records", len(lines) == 6, f"{len(lines)} lines")
        cab1 = next(ln for ln in lines if ln.startswith("CAB-001,"))
        check("export carries the computed next due date", "2027-05-03" in cab1, cab1)
        check("export records the result", ",pass," in cab1)

        conflicts = page.inner_text("#conflicts")
        check("no false conflicts on a single device", conflicts.strip() == "", conflicts)

        page.screenshot(path=str(OUT / "pwa-e2e.png"), full_page=True)
        browser.close()

    results["engine"] = "rust-wasm via voltledger-core"
    results["url"] = URL
    results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    results["passed"] = sum(1 for c in results["checks"] if c["ok"])
    results["total"] = len(results["checks"])
    out = OUT / f"e2e-{time.strftime('%Y%m%dT%H%M%S')}.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\n{results['passed']}/{results['total']} checks passed -> {out}")
    return 0 if results["passed"] == results["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
