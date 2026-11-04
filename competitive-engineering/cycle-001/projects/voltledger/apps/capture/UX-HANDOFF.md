# VoltLedger Mobile PWA — Senti UI build v1

**Scope:** Electrician-facing UI / brand layer on top of the pre-existing VoltLedger capture PWA.

**Branch:** `senti/voltledger-mobile-pwa-v1` (isolated from the frozen `ce001-voltledger` checkpoint).
**Status:** DESIGN/IMPLEMENTATION CHECKPOINT. **NOT field-certified, deployed or production-authorised.**

## Implemented in this branch

- Dark/gold VoltLedger dashboard with live on-device asset, attention and saved-record counters. No invented sample data.
- Large equipment scanning/capture action, accessible form inputs, PASS/FAIL controls and clear offline status.
- On-site registration of a genuinely new tag in the existing IndexedDB `items` store, without CSV pre-processing.
- Environment class requires explicit selection for new assets. Existing tags restore the class from the register.
- Failed electrical tests are displayed as **FAILED**, not misrepresented as OK based on a future due date.
- Register search by tag, description or location; import existing assets, export results, download CSV template.
- PWA manifest, service worker caching the updated UI files, install hint, brand app icon SVG.
- Camera error fallback to manual entry; camera loop stops after the scanner is closed.
- CSV text escaped during DOM rendering to prevent HTML injection through register fields.
- Browser test probe published only after engine/parity state is recorded.
- QR delivery generator (`make_install_qr.py`) creates SVG + printable install card **only from a real approved HTTPS URL**; no live URL invented.

## What is unchanged

`core-rs/`, `core.wasm`, `core.js`, `wasm-core.js`, `wire.js`, corpus and existing Python oracle/evidence. PWA business rules, due-date calculations and reconciliation remain owned by the established Rust/JS engine.

## Engineer acceptance gates — to be run by Sovereign

1. **Function:** `python3 eval/gate.py` must pass all six legs. Browser MUST report `rust-wasm`; never let JS fallback masquerade as a Rust pass.
2. **Legacy UX:** `eval/e2e/run_e2e.py` must still pass, including CSV import, 3 captures, reload, offline capture and export. Preserve pre-existing run records.
3. **New UI:** Browser tests at 360 px, 412 px and 1440 px — no horizontal overflow, clear PASS/FAIL states, readable labels, nav anchors, search, install guidance, keyboard focus and actual dates/status, including failed results.
4. **New asset:** Start from empty IndexedDB; manually add tag, environment, description; record PASS then FAIL; reload offline; verify persistence and accurate visible status. Reject duplicate tags and blank description/class.
5. **Security:** Verify untrusted CSV text cannot inject HTML or execute script; ensure generated CSV values are safe in spreadsheet viewers (formula injection review).
6. **QR/PWA:** Verify install on Android from *approved* HTTPS or localhost test address; test service worker cache and WASM loading completely offline after first installation. Provide real, non-fabricated install URL before generating QR.
7. **OEM:** Keep supplier branding and integrations out of the claim until an agreement and a real export are tested. White-label reskin can be added after evidence.

## Install QR generation (after an approved HTTPS preview exists)

```sh
python3 -m pip install qrcode
python3 make_install_qr.py https://approved-host.example/voltledger/
```

The URL above is **illustrative only**, not a deployment. The script outputs `voltledger-install.svg` and `voltledger-install.html`. Validate the QR against the actual deployed origin on a second phone before distribution.

## Known limitations

- Product has not been tested in this ChatGPT session on a real Android phone or with a branded tester; full browser gates are pending an execution environment with the repo and Chromium.
- Generic five-column asset-register CSV import is present. Real tester output adapter remains gated on an authentic sample and permissions.
- Local device records are **not** automatically uploaded or synchronised. Clearing browser data can erase records; operational data retention/backup flow needs field validation.
- SVG-only PWA icon may require 192/512 PNG and maskable variants for consistent install prompts; add these before Android pilot sign-off.
- The displayed interval classifications are established prototype rules, not a verified declaration of suitability for every AS/NZS situation.
- No production release, billing, app-store installation, manufacturer connection, or public customer distribution is authorised by this branch.

## Product handoff

Senti: UX, layout, visual hierarchy and product-facing copy.  
Sovereign: gate execution, any core changes, real hardware tests, packaging, approved HTTPS pilot release and integration.
