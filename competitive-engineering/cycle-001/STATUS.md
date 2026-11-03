# CYCLE-001 STATUS

Updated 2026-11-03, benchmark stage executed. Programme: MOP-EMPIRE-COMPETITIVE-ENGINEERING-001. Technical baseline accepted by Eddie on 2026-11-03, see `CHECKPOINT.md` and the tag `CE001-VOLTLEDGER-PRE-VALIDATION`.

## Stage position

| Stage | Requirement | State |
|---|---|---|
| 1 | 25 candidates identified | COMPLETE |
| 2 | All 25 scored on the section 7 rubric | COMPLETE |
| 3 | Top 10 selected | COMPLETE |
| 4 | Dossiers for top 5 | COMPLETE |
| 5 | Benchmark plans for top 3 | COMPLETE |
| 6 | One candidate recommended | COMPLETE, VoltLedger 84/100 |
| 7 | Measured baseline against incumbents | PARTIAL. Published evidence captured at E1, trial blocked on Turnstile |
| 8 | Customer validation, five prospects | INVITED, five sent, no reply yet |
| 9 | Pilot artefact built against the locked capture target | COMPLETE, 13/13 browser gate |
| 9a | 200-case deterministic corpus, four-way parity | COMPLETE, 200/200 in oracle, Rust, JavaScript and the browser |
| 9b | Tester CSV import as an adapter boundary | COMPLETE, 8 Rust tests plus 31-check binary gate, no brand claimed |
| 10 | T1 and T2 on real hardware | BLOCKED, needs two operators and the incumbent in hand |

## Artefacts

| Path | What it is |
|---|---|
| CANDIDATES-25.md | Register, rubric breakdown and threshold decisions |
| TARGETS/01 to 05 | Competitor dossiers for the top five |
| BENCHMARKS/01 to 03 | Acceptance contracts for the top three |
| RECOMMENDATION.md | Stage 6 recommendation with the GO / NO-GO |
| EVIDENCE-PACK.md | Consolidated benchmark-stage evidence and the production verdict |
| INTERVIEW-PROTOCOL.md | Eleven questions, capture sheet, decision rules fixed in advance |
| ../ARCHITECTURE-STANDARD.md | Empire AI Language Standard, standing rule |
| projects/voltledger/ | Spec, differentiation, provenance, commercial case, architecture, status |
| projects/voltledger/core-rs/ | Rust core, zero dependencies, compiled to WASM |
| projects/voltledger/apps/capture/ | Installable offline PWA |
| projects/voltledger/eval/ | Python oracle, vectors, Node suite, browser gate, run records |

## Executed evidence this cycle

Oracle harness run 20261103T191626, exit 0, dataset SHA-256 bab3222f1f32372b54defe7289307c26e38672c87b86bdc2aa9e53ef0f777f39:
18 of 18 vectors, 500-record pack 3.93ms p50 / 4.89ms max, offline verification pass, tamper detection pass, wrong-key rejection pass, import rejection pass.

Benchmark stage additionally executed:

| Gate | Result |
|---|---|
| `cargo test` in core-rs | exit 0 |
| `node --test eval/tests/core.test.mjs` | 11 of 11 pass |
| `eval/e2e/run_e2e.py` in Chromium | 13 of 13 checks pass |
| WASM parity in the browser | every vector reproduced by the Rust core |
| `eval/gate.py` (oracle, Rust, JavaScript, browser) | **200 of 200 cases agree, no tolerance** |
| `cargo test --test tester_import` | 8 tests, 8 pass |
| `eval/tester_import_gate.py` | 31 checks, 0 failed, digest checked against `hashlib` |
| Typography gate over all Markdown | exit 0 |

Metrics still declared BLOCKED rather than estimated: per-item time against the incumbent, offline loss over a working day, cost per 1,000 items, first-test time and the whole commercial layer.

## Corrections made and kept visible

- Candidate 04 scores 74 on the rubric breakdown, not the 73 first written. Both are in the register with the correction noted.
- Two status vectors were wrong on first drafting (S01 expected current for an item due today, S04 and S05 had window arithmetic off by a day). They were corrected before the first execution and the harness now passes all 18. Recorded here because a vector set that is silently edited after a run is worthless.
- The capture screen took the class from the dropdown default instead of the register, so a factory item exported as construction. Found by the browser gate, fixed at source, gate re-run to 13/13.
- The 200-case corpus found real disagreements on first run, on import row order and on expanded-year date formatting and it exposed a negative interval that the unsigned window type could not express at all. Each was fixed in the runtime that was wrong and the expectation was not moved. `PARITY.md` records them.

## Commercial state, graded

- Incumbent prices and capability gaps: **E1**, vendor-published, read 2026-11-03.
- The claim that buyers value independently verifiable records: **E0**, hypothesis. Invitations sent, nothing answered.
- Willingness to pay A$59 / A$149: **E0**, untested.
- Spend: **A$0** of the A$49 cap.

## KPI counters (section 39)

| KPI | Cycle 001 |
|---|---|
| Candidates researched | 25 |
| Candidates rejected outright | 2 strategic (07, 22/23 cluster) |
| Candidates to WATCH | 11 |
| Dossiers written | 5 |
| Benchmark plans written | 3 |
| Prototypes built | 1 (VoltLedger pilot PWA, Rust core) |
| Benchmark gates executed | 200 of 200 four-way parity cases, 13 of 13 browser checks, 11 of 11 JS, 18 of 18 legacy vectors, 8 of 8 import tests, 31 of 31 import report checks, Rust suite green |
| Time to pilot artefact | under one day of build, unvalidated |
| Build cost | A$0 cash |
| Paid pilots | 0 |
| MRR / ARR | A$0 |
| Reuse achieved | 3 registers mapped to 1 engine, core designed for the EmpireCore crate split |
| Support hours | 0 |

## Next cycle trigger

Cycle 002 begins when five contractor interviews are answered or the incumbent baseline is measured, whichever lands first, not on a calendar date. Two candidates are queued for it: shift handover for discrete manufacturing and a second register on the VoltLedger engine.
