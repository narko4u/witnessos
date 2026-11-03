# COMPETITOR-BENCHMARK.md - VoltLedger acceptance contract

Version 1.0, fixed 2026-11-03. Candidate: target 01 (score 84/100).
Measurement method: ../../BENCHMARKS/01-test-and-tag.md
Change control: any edit after the first measured baseline run creates version 1.1 with the reason recorded. Thresholds are not loosened after seeing results.

## The claim under test

> A technician records the same round in materially less time because readings import instead of being typed, the records survive a no-signal day with zero loss and the evidence pack verifies offline without trusting the application that produced it.

Price is not part of the claim. The cheapest incumbent is A$49 per month, so "cheaper" is not a defensible position and the commercial case must not be built on it.

## Baseline, as published (E1, read 2026-11-03)

| Item | TagVault | Clevermode | EXTAG |
|---|---|---|---|
| Licence | A$49/mo solo, A$99/mo to 5 users | A$200 + GST per year (A$220 inc GST) plus tester and printer kit | quote only |
| Tester connection | none yet, two-tap entry plus end-of-day CSV | paired via the kit hardware | not stated publicly |
| Offline | recording offline, sync later | app on phone, tester local | not stated publicly |
| Evidence output | branded PDF pack, one click | branded PDF reports | certificates from completed tests |
| Client portal | free at every tier | not stated | contractor access to same register |
| Deployment | signup, 14-day trial | buy kit | "weeks, not months" |
| Export | CSV, promised | not stated | not stated publicly |

No baseline row above is E2 or E3. Nothing has been trialled yet and this contract says so in writing.

## Metrics and thresholds

| ID | Metric | Threshold | Class when measured |
|---|---|---|---|
| T1 | Median seconds per item, scan to commit | 40% below the best incumbent | E3 |
| T2 | P95 seconds per item | 40% below | E3 |
| T3 | Records lost over a 4-hour no-signal round | zero, reconciled on reconnect | E2 |
| T4 | Pack build time for 500 items, P95 | under 12,000ms | E3 |
| T5 | Offline verification, tamper detection, wrong-key rejection | all three true | E2 |
| T6 | Due-date and status correctness on the full vector set | 100% | E3 |
| T7 | Competitor CSV import fidelity | 100% of rows, zero manual edits | E2 |
| T8 | Cost per 1,000 items for a 5-technician business | computed from measured times, not asserted | E3 |
| T9 | Download to first completed test | under 10 minutes | E2 |

## Executed results, run-20261103T191626

Command: `python3 eval/benchmark.py` in projects/voltledger.
Environment: Linux 6.6.87.2-microsoft-standard-WSL2 x86_64, Python recorded in the run file.
Dataset: eval/dataset/assets.csv, SHA-256 bab3222f1f32372b54defe7289307c26e38672c87b86bdc2aa9e53ef0f777f39.

| Gate | Result | Status |
|---|---|---|
| T6 vectors, 18 hand-computed cases | 18/18 | PASS (executed) |
| T4 pack build, 500 records | p50 3.93ms, max 4.89ms | PASS (executed) |
| T5 evidence verifies clean | true | PASS (executed) |
| T5 tamper detected on one flipped byte | true | PASS (executed) |
| T5 wrong key rejected | true | PASS (executed) |
| I01 duplicate id and non-positive interval rejected at import | 2 of 2 rejected, correct reasons | PASS (executed) |
| T1 and T2 per-item time | not measured | BLOCKED: no capture app |
| T3 offline loss | not measured | BLOCKED: needs a device with the radio off |
| T8 cost per 1,000 | not computed | BLOCKED: needs measured labour time |
| T9 first test time | not measured | BLOCKED: no packaged build |

What this proves: the date engine, the evidence chain and the import rules are executable and correct against hand-computed expectations and a single flipped byte is caught. What it does not prove: that a human is faster on it. That claim needs the app and two operators and it is the claim the whole commercial case rests on.

The vector set is 18 cases today. The contract calls for 200. Expanding the set is part of the build, not part of the recommendation.

## Recording requirements

Every run must write software version, hardware, OS, dataset hash, timestamp, configuration and result hash. The harness does this. A result that cannot be reproduced from its record is not evidence.

## Exit criteria for the benchmark stage

Advance to build only when T1, T3, T5 and T6 pass together. If T5 or T6 fails, stop: there is no product.
