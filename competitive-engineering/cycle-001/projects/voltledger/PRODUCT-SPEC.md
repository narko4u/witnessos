# PRODUCT-SPEC.md - VoltLedger

Version 0.1, 2026-11-03. Working name only. No trademark search has been run, so the name is not cleared for public use.

## Purpose

A local-first register for electrical compliance testing. The operator identifies an item, applies its interval, records the result and hands the client evidence that can be checked without trusting the software.

Commercial core: input, decision, structured result. Everything else is adjacency and is out of scope until a customer pays.

## Scope, first release

1. Asset register: item id, description, site, location, class, interval in months, last test date.
2. Capture: scan a tag payload or pick the item, record result and measured values, commit.
3. Due engine: compute next due from the operator's interval, classify current, due soon, overdue, retest required, untested.
4. Evidence pack: register rows plus test events, chained digests, one head digest, offline verification script.
5. Import: competitor CSV with column mapping. Export: CSV, complete, no lock-in.
6. Offline: capture and commit with no network, queue and reconcile on reconnect.

## Out of scope, first release

- Lifting, height-safety, emergency lighting and RCD registers. The same engine will take them and they are deliberately deferred until register one has a paying customer.
- Dashboards, maps, Power BI, franchise portals, invoicing.
- Tester Bluetooth pairing beyond CSV import.
- Compliance determination. The tool applies intervals the operator supplies and says so, exactly as the incumbents do.
- Any cloud account requirement for capture.

## Data model

| Entity | Fields |
|---|---|
| Site | site_id, name, address, client_id |
| Asset | item_id, description, site_id, location, class, interval_months, tag_payload, state |
| Test event | event_id, item_id, tested_at, tester_id, result, measured_values, note, device_id, app_version |
| Evidence pack | pack_id, as_of, records, chain[], head, mac or signature |

Rules that must hold and are tested:

- An asset id is unique in a register. A duplicate is rejected at import with the row named.
- `interval_months` must be positive.
- A failed result always wins over the date. A failed item is retest required even if it is not due.
- A duplicate scan inside one round is flagged, never silently overwritten.
- An item moved between sites keeps its test date and records the move.
- A corrupted tag payload is recorded as unresolved and the item is not marked tested.

## Capture loop

Unlock, last site, scan, choose one of three result buttons, enter measured values only when the class needs them, commit. Target: under 10 seconds per item for a practised user, which is roughly three taps and no typing. The tester import path exists because typing readings is where seconds and errors both come from.

## Evidence pack format

JSON with: manifest (version, pack_id, as_of, record count), records array, chain of per-record SHA-256 digests seeded from a zero block, a head digest over the chain and an HMAC or signature over the head. Verification reads only the pack and a key. A single flipped byte must fail. Verification must run on a machine that has never installed the product.

Deployment note: the shipped product must use an asymmetric key held outside the application, with the option to stamp the head into the WitnessOS evidence layer. The harness uses a run-scoped HMAC because it tests the verification path, not the key custody.

## Interfaces

- CSV in and out in the first release.
- REST with OpenAPI later, only if a customer asks. No compatibility theatre.

## Acceptance against MOP section 21

| Requirement | Status |
|---|---|
| 1 core functionality works | PARTIAL: register and due engine work, capture app not built |
| 2 automated tests pass | PASS: harness exits 0 on 4 gates |
| 3 benchmark runs reproducible | PASS: seeded dataset, hash recorded |
| 4 competitor comparison exists | PARTIAL: published baseline captured, no measured baseline |
| 5 at least one measurable advantage | BLOCKED: needs T1 measured |
| 6 dependency licences acceptable | PASS: Python standard library only |
| 7 deployment documented | NOT STARTED |
| 8 pricing hypothesis | DONE: see COMMERCIAL.md |
| 9 customer profile | DONE: see COMMERCIAL.md |
| 10 demo can be run | NO: harness is not a demo |

## Engineering constraints

- No network required for capture.
- No telemetry of customer data by default. Aggregate counts only, opt in.
- Runs on a phone browser or as a packaged app; the register must also run headless on a laptop for the office.
- One database file per business, portable, backed up as a file.
