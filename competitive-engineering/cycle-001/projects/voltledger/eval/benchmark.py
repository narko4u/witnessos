#!/usr/bin/env python3
"""VOLTLEDGER evaluation harness - T4, T5, T6 and G-series gates.

Runs the deterministic core, scores it against vectors.json, builds an evidence
pack and proves tamper detection. Everything this file reports is measured in
this process; anything that cannot be measured yet is reported as BLOCKED
rather than estimated.

Usage:
    python3 benchmark.py [--items 120] [--pack-items 500]

Outputs:
    dataset/assets.csv          deterministic synthetic register
    results/<timestamp>.json    full run record
Exit code 0 only when every gate passes.
"""

import argparse
import calendar
import csv
import hashlib
import hmac
import json
import os
import platform
import random
import secrets
import sys
import time
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET = os.path.join(ROOT, "dataset")
RESULTS = os.path.join(ROOT, "results")
HARDWARE = f"{platform.system()} {platform.release()} {platform.machine()}"
SOFTWARE = "voltledger-eval 0.1.0"

SITES = ["maroochydore-depot", "noosa-holiday-park", "caboolture-yard", "strathpine-office"]
CLASSES = ["portable-appliance", "power-tool", "extension-lead", "power-board", "rcd"]
# Interval values in this synthetic set are what a test business has decided for
# its own site classes. The tool does not decide compliance; it applies the
# operator's interval. Real deployments load intervals from the customer.
INTERVALS = {"portable-appliance": 12, "power-tool": 3, "extension-lead": 6,
             "power-board": 12, "rcd": 6}


def add_months(d: date, months: int) -> date:
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def classify(as_of: date, next_due, window_days: int, result: str) -> str:
    if result == "fail":
        return "retest_required"
    if result == "untested" or next_due is None:
        return "untested"
    if as_of > next_due:
        return "overdue"
    if (next_due - as_of).days <= window_days:
        return "due_soon"
    return "current"


def generate_assets(count: int, seed: int = 20261103) -> list:
    rng = random.Random(seed)
    rows = []
    for i in range(count):
        cls = rng.choice(CLASSES)
        # Realistic spread: most items sit inside their cycle, a tail is overdue.
        span = int(INTERVALS[cls] * 30.4 * rng.uniform(0.15, 1.45))
        last = date(2026, 11, 3) - timedelta(days=rng.randint(0, max(1, span)))
        rows.append({
            "item_id": f"AU-{1000 + i}",
            "description": f"{cls} unit {i}",
            "site": rng.choice(SITES),
            "location": f"bay-{rng.randint(1, 9)}",
            "class": cls,
            "last_test": last.isoformat(),
            "interval_months": INTERVALS[cls],
            "result": rng.choice(["pass"] * 9 + ["fail"]),
            "tag_payload": f"https://tags.example/{1000 + i}",
        })
    return rows


def write_assets(rows: list) -> str:
    path = os.path.join(DATASET, "assets.csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return path


def run_vectors():
    with open(os.path.join(DATASET, "vectors.json"), encoding="utf-8") as fh:
        vectors = json.load(fh)
    fails = []

    for v in vectors["due_date_vectors"]:
        got = add_months(date.fromisoformat(v["last_test"]), v["interval_months"]).isoformat()
        if got != v["expected"]:
            fails.append({"vector": v["id"], "case": v["case"], "want": v["expected"], "got": got})

    for v in vectors["status_vectors"]:
        nxt = date.fromisoformat(v["next_due"]) if v["next_due"] else None
        got = classify(date.fromisoformat(v["as_of"]), nxt, v["window_days"], v["result"])
        if got != v["expected_status"]:
            fails.append({"vector": v["id"], "case": v["case"],
                          "want": v["expected_status"], "got": got})

    return len(vectors["due_date_vectors"]) + len(vectors["status_vectors"]), fails


def import_register(rows: list) -> dict:
    """Reject bad rows loudly. Silence here becomes a wrong certificate later."""
    seen, accepted, rejected = set(), [], []
    for r in rows:
        if r["item_id"] in seen:
            rejected.append({"row": r["item_id"], "reason": "duplicate asset id"})
            continue
        if int(r["interval_months"]) <= 0:
            rejected.append({"row": r["item_id"], "reason": "interval_months must be positive"})
            continue
        if not r.get("tag_payload"):
            rejected.append({"row": r["item_id"], "reason": "missing tag payload"})
            continue
        seen.add(r["item_id"])
        accepted.append(r)
    return {"accepted": accepted, "rejected": rejected}


def build_register(items: list, as_of: date, window_days: int = 30) -> list:
    out = []
    for r in items:
        nxt = add_months(date.fromisoformat(r["last_test"]), int(r["interval_months"]))
        out.append({**r, "next_due": nxt.isoformat(),
                    "status": classify(as_of, nxt, window_days, r["result"])})
    return out


def seal(payload: dict) -> tuple:
    """Digest every record, chain the digests, sign the chain.

    A real deployment signs with an asymmetric key anchored outside the product
    and stamps the result into the WitnessOS evidence layer. This harness uses
    an HMAC run key so the verification path is exercised honestly offline.
    """
    key = secrets.token_bytes(32)
    prev = b"\x00" * 32
    chain = []
    for rec in payload["records"]:
        body = json.dumps(rec, sort_keys=True, separators=(",", ":")).encode()
        digest = hashlib.sha256(prev + body).digest()
        chain.append(digest.hex())
        prev = digest
    head = hashlib.sha256(b"".join(bytes.fromhex(c) for c in chain)).hexdigest()
    mac = hmac.new(key, head.encode(), hashlib.sha256).hexdigest()
    return {"chain": chain, "head": head, "mac": mac}, key


def verify(pack: dict, key: bytes) -> bool:
    payload, seal_ = pack["payload"], pack["seal"]
    prev = b"\x00" * 32
    for rec, claimed in zip(payload["records"], seal_["chain"]):
        body = json.dumps(rec, sort_keys=True, separators=(",", ":")).encode()
        digest = hashlib.sha256(prev + body).hexdigest()
        if digest != claimed:
            return False
        prev = bytes.fromhex(digest)
    head = hashlib.sha256(b"".join(bytes.fromhex(c) for c in seal_["chain"])).hexdigest()
    if head != seal_["head"]:
        return False
    return hmac.compare_digest(hmac.new(key, head.encode(), hashlib.sha256).hexdigest(), seal_["mac"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", type=int, default=120)
    ap.add_argument("--pack-items", type=int, default=500)
    args = ap.parse_args()
    os.makedirs(RESULTS, exist_ok=True)

    started = time.time()
    gate = {}

    # T6: due-date and status correctness against hand-computed vectors.
    total, fails = run_vectors()
    gate["T6_vectors"] = {"cases": total, "failures": fails, "pass": not fails}

    # Synthetic register and integrity import rules.
    rows = generate_assets(args.items)
    csv_path = write_assets(rows)
    dirty = rows + [dict(rows[0]), {**rows[1], "item_id": "AU-BAD1", "interval_months": 0}]
    imported = import_register(dirty)
    reasons = sorted(r["reason"] for r in imported["rejected"])
    gate["I01_duplicate_and_bad_rows"] = {
        "rejected": imported["rejected"],
        "pass": len(imported["rejected"]) == 2 and reasons == ["duplicate asset id",
                                                               "interval_months must be positive"],
    }

    register = build_register(imported["accepted"], date(2026, 11, 3))
    counts = {}
    for r in register:
        counts[r["status"]] = counts.get(r["status"], 0) + 1

    # T4: evidence pack generation for a realistic round size.
    big = build_register(imported["accepted"] * (args.pack_items // max(1, len(imported["accepted"])) + 1),
                         date(2026, 11, 3))[:args.pack_items]
    timings = []
    pack = None
    for _ in range(5):
        t0 = time.perf_counter()
        payload = {"register": "synthetic", "as_of": "2026-11-03", "records": big}
        seal_, key = seal(payload)
        pack = {"payload": payload, "seal": seal_}
        timings.append((time.perf_counter() - t0) * 1000)
    timings.sort()
    gate["T4_pack_build_ms"] = {"p50": round(timings[2], 2), "max": round(timings[-1], 2),
                                "records": len(big), "pass": timings[-1] < 12000}

    # T5: verification works offline and detects a single flipped byte.
    ok_clean = verify(pack, key)
    tampered = json.loads(json.dumps(pack))
    tampered["payload"]["records"][17]["result"] = "pass" if big[17]["result"] != "pass" else "fail"
    ok_tampered = verify(tampered, key)
    wrong_key = verify(pack, secrets.token_bytes(32))
    gate["T5_evidence"] = {"verifies_clean": ok_clean, "detects_tamper": not ok_tampered,
                           "rejects_wrong_key": not wrong_key,
                           "pass": ok_clean and not ok_tampered and not wrong_key}

    # T6/T1/T8 that cannot be measured yet are declared, not estimated.
    gate["T1_T2_per_item_time"] = {"status": "BLOCKED",
                                   "reason": "requires the capture app and human operators; not built in this cycle"}
    gate["T3_offline_loss"] = {"status": "BLOCKED", "reason": "requires device with radio disabled"}
    gate["T8_cost_per_1000"] = {"status": "BLOCKED",
                                "reason": "needs measured labour time; published licence prices alone cannot produce it"}
    gate["T9_first_test_minutes"] = {"status": "BLOCKED", "reason": "requires packaged build"}

    dataset_hash = hashlib.sha256(open(csv_path, "rb").read()).hexdigest()
    record = {
        "software": SOFTWARE,
        "hardware": HARDWARE,
        "python": sys.version.split()[0],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "dataset": csv_path,
        "dataset_sha256": dataset_hash,
        "register_status_counts": counts,
        "gates": gate,
        "elapsed_s": round(time.time() - started, 3),
        "evidence_pack_head": pack["seal"]["head"],
    }
    out = os.path.join(RESULTS, time.strftime("run-%Y%m%dT%H%M%S.json"))
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)

    print(f"register: {len(register)} items  {counts}")
    print(f"T6 vectors: {total - len(fails)}/{total}")
    print(f"T4 pack: {len(big)} records p50 {gate['T4_pack_build_ms']['p50']}ms max {gate['T4_pack_build_ms']['max']}ms")
    print(f"T5 verify={ok_clean} tamper_detected={not ok_tampered} wrong_key_rejected={not wrong_key}")
    print(f"BLOCKED (declared, not estimated): T1/T2, T3, T8, T9")
    print(f"results: {out}")

    hard = [gate["T6_vectors"]["pass"], gate["T5_evidence"]["pass"],
            gate["T4_pack_build_ms"]["pass"], gate["I01_duplicate_and_bad_rows"]["pass"]]
    return 0 if all(hard) else 1


if __name__ == "__main__":
    sys.exit(main())
