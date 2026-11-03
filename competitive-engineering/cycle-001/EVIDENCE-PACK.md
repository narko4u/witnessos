# CYCLE-001 Evidence Pack: VoltLedger

Compiled 2026-11-03 under MOP-EMPIRE-COMPETITIVE-ENGINEERING-001. Authority: Eddie. Orchestrator: Sovereign.
Spend to date: A$0 of the A$49 authorised. No subscription, hardware or service cost incurred.

## 1. Verdict

**PILOT BUILD: GO. PRODUCTION: NO-GO, evidence gate open.**

The engineering is proven and reproducible. The commercial claim is not. Nothing in this pack upgrades the purchase-reason hypothesis above E0, because the buyer research has been invited and not yet answered and the incumbent trial is blocked on a bot check that only a human may pass.

That is not a reason to stop building. It is a reason to refuse to call it validated.

## 2. What was built

Architecture per the Empire AI Language Standard (see `../ARCHITECTURE-STANDARD.md`): Rust core, browser interface, Python harness retained unchanged as an independent oracle.

| Component | Path | Language | State |
|---|---|---|---|
| Deterministic core | `projects/voltledger/core-rs/src/lib.rs` | Rust, zero dependencies | Compiles, tests pass |
| Browser core | `apps/capture/core.wasm` | Rust to wasm32-unknown-unknown | Loading and verifying on every page load |
| Capture interface | `apps/capture/` | Browser stack, TypeScript target | Installable PWA, offline, IndexedDB |
| Evaluation oracle | `eval/benchmark.py` | Python, standard library only | Unchanged, still green |
| Browser gate | `eval/e2e/run_e2e.py` | Python plus Playwright | 13 checks, all passing |
| JS parity suite | `eval/tests/core.test.mjs` | Node test runner | 11 of 11 |
| Parity corpus | `eval/vectors/corpus/corpus.tsv` | 200 frozen cases, hashed | Regenerated only by `derive_corpus.py` |
| Parity gate | `eval/gate.py` | Python, all legs | One command, five legs |
| Tester import | `core-rs/src/tester_import/` | Rust, profile as data | Three generic profiles, no brand |
| Import report | `core-rs/src/bin/import_report.rs` | Rust binary, JSON out | Run as a program, not only as a test |

## 3. Executed evidence

Every line below is a command that ran, not a claim about code that exists.

| Gate | Command | Result |
|---|---|---|
| Oracle harness | `python3 eval/benchmark.py` | exit 0, 18/18 vectors, run 20261103T191626 |
| Rust core | `cargo test` | exit 0 |
| JS core | `node --test eval/tests/core.test.mjs` | 11 tests, 11 pass, 0 fail |
| WASM build | `cargo build --release --target wasm32-unknown-unknown` | artifact 40KB class, copied to `apps/capture/core.wasm` |
| Browser end to end | `python3 eval/e2e/run_e2e.py` | **13/13 checks pass** |
| Four-way parity | `python3 eval/gate.py` | **200/200 cases** in oracle, native Rust, JavaScript and the browser running Rust/WASM |
| Tester import | `cargo test --test tester_import` | 8 tests, 8 pass |
| Import report | `python3 eval/tester_import_gate.py` | **31 checks, 0 failed**, digest verified against `hashlib` |
| Formatting | `typography.py --fix` over all Markdown | exit 0 |

The browser gate covers, in a real Chromium against the served app:

1. The Rust core loads and reproduces every hand-computed vector in the browser. Parity is displayed in the interface and falls back to the JS core with a visible warning if it ever fails.
2. Duplicate asset ids and non-positive intervals are rejected by name.
3. A captured result survives a full page reload.
4. Results captured with the network disabled survive reconnect and reconciliation produces the correct next-due date.
5. CSV export carries the record, the computed due date and the class.

Measured core performance, 500 records: 3.93ms p50, 4.89ms max for a full evidence pack build and verify.

### What the 200 cases do and do not prove

200 frozen cases cover interval boundaries, leap years, month ends, every register
state and both status edges, zero and negative intervals, duplicate ids, malformed
dates, missing fields, class changes, operator override, imported history,
reconciliation collisions, offline records, conflicting edits and export/re-import
parity. The expected bytes came from a separate Python oracle, anchored by twenty
literal answers worked out by hand, so a shared mistake has to survive four
independent reproductions to pass.

What it does not prove: that the register is right for a real site or that an
operator can use it. Those need the incumbent baseline and the interviews.

### The tester import boundary

A tester export is read by a profile, which is data, not code. Three generic
profiles exist; no tester brand is named anywhere, because naming one before a real
export has been exercised would be a compatibility claim we cannot support. Raw rows
are retained verbatim and normalised readings are stored separately, so an auditor
can always see what the instrument actually printed. Nothing is coerced: `>999`
stays text, `03/11/2026` under an ISO profile is a rejected row with a reason and
an empty cell is an absent value rather than a default.

## 4. A defect the gate caught

The first end-to-end run failed one check: a factory item exported as `construction`. The capture screen was taking the class from the dropdown's default rather than from the register, so the first option silently overwrote the truth for every item.

This is precisely the failure mode that makes a register useless in an audit and it was invisible to the unit tests because they never went through the interface. Fixed at `apps/capture/app.js` so the tag drives the class and an operator override is still recorded; re-ran the gate to 13/13.

Recorded because a gate that has never failed is a gate that has never been tested.

## 5. Commercial evidence, honestly graded

| Item | Grade | Basis |
|---|---|---|
| Incumbent prices: TagVault A$49/mo solo, A$99/mo to 5; Clevermode A$220/yr; PlanetSafe A$2.10-3.50/item plus A$120 per visit; EXTAG quote only | E1 | Vendor-published pages, read 2026-11-03 |
| TagVault has no tester import, two-tap workflow, end-of-day CSV | E1 | Vendor's own material |
| Our per-item speed advantage | **BLOCKED** | Needs the incumbent in hand and two operators |
| Our offline duration advantage | **BLOCKED** | Proven durable in browser, not measured over a working day |
| Buyers value independently verifiable records | **E0** | Hypothesis. No contractor has answered yet |
| Willingness to pay A$59 / A$149 | **E0** | Untested |

Outbound executed today, all approved:

| Action | State |
|---|---|
| Five Queensland contractor research invitations | **SENT**, Sent ids 512-516: Dawson Electric (Woolloongabba), JLT Services (Capalaba), Level Up Electrical (Brendale), Bright Sparks (Sunshine Coast), MightyWatt (Balmoral Ridge) |
| EXTAG demonstration request | **SENT** to info@extag.com.au, asked for setup time, offline behaviour, evidence output and price for three users |
| TagVault trial | **BLOCKED**, Cloudflare Turnstile on the Clerk sign-up. Not circumvented |

The invitation asks whether a record has ever been questioned. It does not suggest one has. Every respondent who says "never" is recorded as a negative result and two or more negatives out of five collapses the differentiation claim and forces a re-score.

## 6. The one thing only Eddie can do

TagVault sign-up is gated by Cloudflare Turnstile. I will not defeat a bot check, so the trial needs a human click. The form is already filled and the profile is warm:

```
cd /home/vault/.hermes/cache/scratch/ce001/tagvault
/usr/bin/python3 signup.py
```

That opens a browser at the TagVault sign-up with contact@empirelabs.com.au pre-filled and the generated password held in `cred.txt` at mode 0600. Click the Turnstile checkbox and submit, then tell me and I will run the full baseline protocol in `COMPETITOR-BENCHMARK.md` against the live trial: setup time, import/export, per-item workflow, offline behaviour, report output, tester integration, migration friction.

Same for any contractor who replies: I run the 11 questions in `../INTERVIEW-PROTOCOL.md`, verbatim and record negatives as results.

## 7. Fixed decision rules, unchanged by today's work

- Two or more of five contractors report a real record challenge with time lost: the evidence claim survives, differentiation holds.
- One or none: re-score VoltLedger with differentiation reduced, find an advantage the interviews actually demonstrate or demote it. No rationalising.
- Three or more report losing records to connectivity: offline durability becomes the lead claim, since it is measurable in a demo.
- Production remains NO-GO until incumbent baseline and buyer evidence are both in hand.

## 8. Cost ledger

| Item | Cost |
|---|---|
| Rust toolchain, wasm target, Playwright, Node | A$0, already installed |
| Synthetic dataset generation | A$0 |
| Web research and extraction | A$0 |
| Email outreach, six messages | A$0 |
| **Total against the A$49 cap** | **A$0** |
