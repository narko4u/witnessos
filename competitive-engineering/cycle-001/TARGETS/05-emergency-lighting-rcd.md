# TARGET 05 - Emergency lighting and RCD test records

Dossier date: 2026-11-03. Third register on the target 01 engine.

## Product and company

- Capability: record of emergency lighting and exit sign discharge tests and residual current device (RCD) trip tests, with intervals, measured values, pass or fail and an evidence pack.
- Providers examined: TagVault (offers an emergency lighting test log and RCD test records alongside its appliance register), Clevermode (appliance-centric, adjacent only) and the market default: paper logbooks and a Word template.
- Category: electrical compliance record keeping, building safety.

## Customer

Electricians who already do test and tag rounds, facility managers of commercial buildings and strata and property managers who need the record for insurance and audits. Crucially, this is the same buyer as target 01 buying a second obligation from the same person on the same visit.

## Pricing

| Provider | Price | Evidence |
|---|---|---|
| TagVault | A$49/mo solo, A$99/mo teams to 5, with emergency lighting and RCD records included | E1, vendor pricing and feature sections |
| Paper logbook | Zero licence | E0 |

## Core capability

For each fitting: identify it, record the test type (duration, duration-and-measure or a measured value such as trip time and current), apply the interval, compare the measurement to the pass band, then produce the register and the certificate evidence.

## Strongest incumbent features

- TagVault: treats the records as first-class register entries rather than a form, includes them at no extra tier and bundles the client evidence pack.
- Incumbents generally: mobile capture beats the clipboard.

## Weakest incumbent features

- Emergency lighting is usually modelled as one more appliance with a note field, so measured values have no schema and cannot be trended.
- Discharge tests are time-based events that happen while the technician is doing something else; none of the tools handles a partially completed round well.
- RCD results include numeric measurements (trip time, trip current); capturing numbers as free text destroys the audit value.
- No incumbent produces a per-fitting history that a building auditor can verify independently.

## Deployment architecture

Cloud SaaS, mobile capture, same as target 01.

## API and interoperability

Same as target 01: CSV out at best, no public API.

## Open-source competitors

None found.

## Build complexity

Low. Schema work for measured values plus a pass-band evaluator plus the existing round workflow. Roughly one week on the target 01 engine.

## Switching difficulty

Low. CSV of fixture id, location, test date, test type, measured value, result.

## Revenue opportunity

Incremental revenue on the same account. It also strengthens the target 01 pitch: one app for every electrical obligation on the site, one evidence pack for the client, one price. That is a defensible bundle that a single-purpose appliance app cannot match.

## Why it scored 73

- Revenue 12/20: attached revenue, rarely a standalone purchase.
- Build 12/15: reuse.
- Differentiation 13/20: measured-value schema and pass bands, better than a note field.
- Migration 7/10: trivial import.
- Weakness 7/10: free-text measurements, no independent verification.
- Reuse 9/10: highest reuse in the cycle.
- Support 4/5: deterministic.
- IP risk 9/10: standards are publicly purchasable; the technician supplies pass criteria and intervals.

## Rejection conditions

Reject as a standalone product; ship only as a register on the target 01 engine and only after the first register has a paying customer.
