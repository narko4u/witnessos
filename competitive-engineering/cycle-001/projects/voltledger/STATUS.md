# STATUS.md - VoltLedger

Updated 2026-11-03, after the parity and tester-import stage. Internal working name, uncleared until trademark and domain search.

## Stage

Pilot-ready artefact, unvalidated commercially. Production decision NO-GO pending buyer evidence and the incumbent baseline. See `../../EVIDENCE-PACK.md`.

## Done

- Candidate selected from a 25-candidate register at 84/100.
- Acceptance contract fixed before implementation, as MOP section 9 requires.
- Python oracle harness executed: exit 0, 18/18 legacy vectors, 500-record pack 3.93ms p50.
- Rust `voltledger-core` written to the Empire AI Language Standard, zero dependencies, `cargo test` exit 0.
- Compiled to `apps/capture/core.wasm`, loaded in the browser, with a visible JS fallback.
- Installable offline PWA: IndexedDB, durable across reload and reconnect, deterministic reconciliation, CSV import validation and export.
- Browser UX gate `eval/e2e/run_e2e.py`: 13 of 13 checks in Chromium.
- **200-case corpus frozen and hashed. All four runtimes agree on all 200 cases**: Python oracle, native Rust, JavaScript and the browser running the Rust core as WebAssembly. `python3 eval/gate.py` runs every leg.
- **Tester import layer built as an adapter boundary**: three generic profiles, raw rows retained verbatim, normalised readings stored separately, every rejection named with its line and reason, SHA-256 of the original bytes in the report. Eight Rust tests and a 31-check binary gate.
- Class-capture defect found by the browser gate and fixed at source.
- Six external messages sent: five contractor research invitations, one EXTAG demonstration request.

## Not done and deliberately

- No native Android build. The PWA ships first; Tauri or native only when tester deployment evidence justifies it.
- No tester brand adapter and no Bluetooth or USB capture. Those names appear only after a real export has been exercised.
- No tested `tester import` button in the capture screen. The layer is complete and proven as a program; wiring it into the operator flow is the next rung and needs a real export to design against.
- No measured incumbent baseline. TagVault sign-up is behind Cloudflare Turnstile and needs a human click.
- No contractor answer yet. Invitations sent 2026-11-03.
- No deployment documentation, demo, pilot agreement or trademark search.

## Blockers

| Blocker | Owner | Consequence if unresolved |
|---|---|---|
| Turnstile click on the TagVault sign-up | Eddie | No measured incumbent baseline |
| Contractor replies to five invitations | Responders | Purchasing claim stays at E0 |
| Two operators with phones, four hours | Eddie | T1 and T2 cannot be measured |
| One real tester export from any brand | Any operator | No brand adapter can be built honestly |

## Next three actions, in order

1. Run the baseline protocol against the TagVault trial the moment it exists, into `COMPETITOR-BENCHMARK.md` section 3.
2. Interview every responder with `../../INTERVIEW-PROTOCOL.md`, verbatim, negatives recorded.
3. With two operators, run T1 and T2 on real hardware, then decide GO or PIVOT on the numbers.

## Honest position

The deterministic core is proven, the four runtimes agree and the import layer
refuses what it cannot verify. Every commercial claim about speed and about buyers
valuing verifiable evidence is still unproven. Say it that way until the numbers
exist.
