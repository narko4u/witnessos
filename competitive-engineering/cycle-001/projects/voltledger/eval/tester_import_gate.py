"""Tester-import gate.

Runs the import layer as a program - `cargo run --bin import_report` - over
fixtures that look like tester exports, and checks the report an operator would
actually read: rows taken, rows refused, the line each refusal sits on, the
reason in words, the digest of the original bytes and the untouched reading.

The expectations below are written here, not read back from the Rust tests, and
the digest is recomputed with hashlib so the core's SHA-256 is checked against a
reference implementation rather than against itself.

    python3 tester_import_gate.py
"""

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
CORE = os.path.join(PROJECT, "core-rs")
FIXTURES = os.path.join(CORE, "tests", "fixtures", "tester-import")
RESULTS = os.path.join(HERE, "results")
BIN = os.path.join(CORE, "target", "debug", "import_report")

# (profile, fixture, expected)
CASES = [
    {
        "profile": "generic_csv",
        "fixture": "generic_pass.csv",
        "total_rows": 4,
        "accepted": 4,
        "rejected": [],
        "first_reading": ">999",
    },
    {
        "profile": "generic_csv",
        "fixture": "generic_rejects.csv",
        "total_rows": 7,
        "accepted": 1,
        "rejected": [
            (3, "duplicate asset id"),
            (4, "item_tag is empty"),
            (5, "bad date: 03/11/2026"),
            (6, "unknown result: MAYBE"),
            (7, "unknown class: kitchen"),
            (8, "bad date: 2026-02-30"),
        ],
    },
    {
        "profile": "generic_csv_no_header",
        "fixture": "no_header.csv",
        "total_rows": 3,
        "accepted": 3,
        "rejected": [],
        "first_reading": ">999",
        "first_line": 1,
    },
    {
        "profile": "generic_csv_day_first",
        "fixture": "dmy_dates.csv",
        "total_rows": 3,
        "accepted": 3,
        "rejected": [],
        "dates": ["2026-11-03", "2026-10-31", "2024-02-29"],
    },
    {
        # The wrong profile must refuse, not reinterpret: day-first cannot read
        # an ISO date, and the row is rejected rather than reshaped.
        "profile": "generic_csv_day_first",
        "fixture": "generic_pass.csv",
        "total_rows": 4,
        "accepted": 0,
        "rejected": [
            (2, "bad date: 2026-11-03"),
            (3, "bad date: 2026-11-03"),
            (4, "bad date: 2026-11-03"),
            (5, "bad date: 2026-10-31"),
        ],
    },
]


def build():
    proc = subprocess.run(
        ["cargo", "build", "--bin", "import_report", "--quiet"],
        cwd=CORE,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"build failed\n{proc.stdout}\n{proc.stderr}")
    if not os.path.exists(BIN):
        raise SystemExit(f"binary missing: {BIN}")


def run(profile, path):
    proc = subprocess.run(
        [BIN, "--profile", profile, "--file", path],
        capture_output=True,
        text=True,
    )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise SystemExit(f"not JSON (exit {proc.returncode}):\n{proc.stdout}\n{proc.stderr}")
    return proc.returncode, payload


def main():
    build()
    failures = []
    checks = 0
    records = []

    for case in CASES:
        path = os.path.join(FIXTURES, case["fixture"])
        code, report = run(case["profile"], path)
        label = f"{case['profile']} / {case['fixture']}"

        def check(ok, detail):
            nonlocal checks
            checks += 1
            if not ok:
                failures.append(f"{label}: {detail}")

        check(code == 0, f"exit {code}, expected 0")
        if "error" in report:
            failures.append(f"{label}: error {report['error']}")
            continue

        check(report["total_rows"] == case["total_rows"],
              f"total_rows {report['total_rows']} != {case['total_rows']}")
        check(report["accepted"] == case["accepted"],
              f"accepted {report['accepted']} != {case['accepted']}")

        got = [(r["line"], r["reason"]) for r in report["rejected"]]
        check(got == case["rejected"], f"rejected {got} != {case['rejected']}")

        with open(path, "rb") as fh:
            expected_digest = hashlib.sha256(fh.read()).hexdigest()
        check(report["file_sha256"] == expected_digest,
              f"file_sha256 {report['file_sha256']} != reference {expected_digest}")

        if case.get("first_reading"):
            readings = [r["reading"] for r in report["readings"]]
            check(readings and readings[0] == case["first_reading"],
                  f"reading preserved as text: {readings[:2]}")
        if case.get("first_line"):
            check(report["readings"][0]["line"] == case["first_line"],
                  f"first line {report['readings'][0]['line']}")
        if case.get("dates"):
            got_dates = [r["tested_at"] for r in report["readings"]]
            check(got_dates == case["dates"], f"dates {got_dates} != {case['dates']}")

        if case["fixture"] == "generic_rejects.csv":
            raw = report["rejected"][2]["raw"]
            check(raw.startswith("CAB-010,PASS,03/11/2026"), f"raw row not retained: {raw}")

        records.append(
            {
                "profile": case["profile"],
                "fixture": case["fixture"],
                "total_rows": report["total_rows"],
                "accepted": report["accepted"],
                "rejected": got,
                "file_sha256": report["file_sha256"],
            }
        )

    # An unknown adapter is refused outright, not silently mapped to a default.
    code, payload = run("adapter_metrel", os.path.join(FIXTURES, "generic_pass.csv"))
    checks += 1
    if code != 2 or "unknown adapter" not in payload.get("error", ""):
        failures.append(f"unknown adapter: exit {code}, payload {payload}")

    os.makedirs(RESULTS, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out = os.path.join(RESULTS, f"tester-import-{stamp}.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(
            {
                "gate": "tester-import",
                "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "cases": len(CASES) + 1,
                "checks": checks,
                "failed": len(failures),
                "results": records,
                "failures": failures,
            },
            fh,
            indent=2,
            ensure_ascii=False,
        )
        fh.write("\n")

    for f in failures:
        print(f"FAIL {f}")
    print(f"checks {checks}  failed {len(failures)}")
    print(f"record {out}")
    if failures:
        return 1
    print("GATE PASSED: tester import takes what it can verify and refuses the rest by name")
    return 0


if __name__ == "__main__":
    sys.exit(main())
