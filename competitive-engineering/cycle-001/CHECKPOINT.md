# CYCLE-001 checkpoint

Accepted by Eddie on 2026-11-03.

    baseline commit   8638bd9
    tag               CE001-VOLTLEDGER-PRE-VALIDATION
    verdict           PILOT BUILD GO / PRODUCTION NO-GO
    corpus            v1, 200 cases, sha256 40c4afe56db5150a1d6ec003d34847c68a15302ede38129c15d5d74574fc4a3e

The tag is a documentation marker, not a release. No version number is assigned.

## What the checkpoint proves

Executed at the commit, not asserted from the code:

| Gate | Result |
|---|---|
| Corpus freeze check | v1 digest and case count match `MANIFEST.json` |
| Four-way parity | 200 of 200 cases in the Python oracle, native Rust, JavaScript and the browser running Rust/WASM |
| Tester import | 8 Rust tests, 31 report checks, digest verified against `hashlib` |
| Browser UX | 13 of 13 checks in Chromium |
| Python harness | exit 0, 18 of 18 legacy vectors, 500-record pack about 3 ms p50 |
| Typography | exit 0, no em dashes, no comma before and or or |

## What the checkpoint does not prove

- That a contractor will pay, that contractors experience the record problem or
  that the register matches a real site.
- Any speed or offline advantage against an incumbent, which was never measured.
- That a branded tester file imports, because no branded tester file exists yet.

## Scope lock

No new product surface until an external gate moves. Not built and not to be
started:

- dashboards, account management, billing, cloud hosting
- native Android packaging, Bluetooth or USB tester integration
- branded tester adapters, reporting embellishments, marketing site
- customer-specific features, operator UI for the import layer

Reason: the engine is no longer the open question. Whether contractors pay for a
problem they actually experience is.

## External gates open

| Gate | Owner | State |
|---|---|---|
| TagVault trial baseline | Eddie clicks Turnstile, then Sovereign runs the frozen contract | Blocked on the click |
| Five contractor interviews | Responders | Invitations sent 2026-11-03, no replies |
| First real tester export | Any operator | Not obtained |
| EXTAG baseline information | EXTAG | Demo request sent, no reply |

Decision rule held unchanged: two or more of five reporting a genuine record or
evidence challenge keeps the differentiation alive. Zero or one fails it and forces
a re-score or a pivot. Unexpected pain reported by respondents is recorded as a
result and can replace the thesis.

## Next decision

Not another engineering gate. It is GO TO FIELD PILOT, PIVOT or KILL, taken when
one of the external gates resolves.
