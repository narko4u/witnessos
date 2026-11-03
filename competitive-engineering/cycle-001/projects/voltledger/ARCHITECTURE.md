# VoltLedger architecture

PWA-first, Rust core, no server in the pilot. The standard this follows is `../../ARCHITECTURE-STANDARD.md`.

## Layout

```
apps/capture/
    index.html              screen, Android-first, 412px reference width
    app.js                  wiring: IndexedDB, rendering, camera, import/export
    core.js                 JS implementation of the core, fallback and oracle
    wasm-core.js            bridge to the Rust core, with the load-time parity gate
    core.wasm               voltledger-core compiled for wasm32-unknown-unknown
    sw.js                   shell cache, versioned
    manifest.webmanifest    installable, standalone, no store listing
apps/capture/wire.js       the wire protocol in plain JavaScript, fallback engine
core-rs/
    src/lib.rs              rules, reconciliation, CSV, evidence, WASM ABI
    src/lib.rs  (mod wire)  dispatch(op, input) - the one path native and WASM both use
    src/sha256.rs           content digest, no dependencies, NIST vectors as tests
    src/tester_import/      adapter boundary: mod, generic_csv, validation, normalisation
    src/bin/import_report.rs  the import as a program, JSON out
eval/
    benchmark.py            Python harness, independent oracle, unchanged
    oracle.py               second Python implementation, authored the 200 cases
    gate.py                 one command, five legs, exit code is the answer
    tester_import_gate.py   drives the real binary over the fixtures
    tests/core.test.mjs     Node suite over core.js
    tests/corpus.test.mjs   Node suite over wire.js, 200 cases
    e2e/run_e2e.py          browser gate: parity, durability, offline, export
    e2e/corpus_gate.py      browser gate: 200 cases through the WASM core
    vectors/corpus/         the frozen 200-case corpus and its digest
    vectors.json            hand-computed expectations, authored before the code
```

Full parity contract in `PARITY.md`, import boundary in `TESTER-IMPORT.md`.

## Why the core is Rust

The record is the product. If the phone and the console ever compute two different next-due dates from the same test, the contractor's register is worthless in an audit. One implementation compiled to both places removes that class of failure; a second implementation in JavaScript would recreate it.

The WASM parity gate runs on every load. If the Rust core and the hand-computed vectors disagree, the interface falls back to `core.js` and says so, rather than writing records with an unverified engine.

## Data path

1. Operator scans or types a tag. The class comes from the register, not the dropdown default.
2. Pass or fail is committed to IndexedDB in a single transaction that also advances the device sequence counter. The button only settles after the transaction completes.
3. The view is derived: reconcile all operations, take the latest per item, compute the due date from the class.
4. Export produces CSV from the derived state. Import validates the whole file before any row is stored.

Nothing leaves the device unless the operator exports. There is no account, no sync endpoint and no telemetry in the pilot.

## Reconciliation rules

- A duplicate operation id applies once, whatever order it arrives in.
- The latest tested date wins; ties break on device id then sequence, so two phones offline on the same day cannot produce two answers.
- A same-day disagreement is reported as a conflict, never merged away.
- Days are counted from the record, never typed by hand and month arithmetic clamps to the last day of the target month.

## Growth path

The pilot ships as a PWA with no store dependency. The same Rust core then compiles to a Tauri or native Android binary when tester integration or deployment evidence justifies it, without a rewrite. Tester import already sits behind a profile boundary in `src/tester_import/`, so a new tester is a profile entry and a fixture, not an architecture change. Moving it into its own `empire-import` crate is mechanical when a second product needs it.
