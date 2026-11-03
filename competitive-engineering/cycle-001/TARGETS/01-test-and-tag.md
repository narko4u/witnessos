# TARGET 01 - Australian test and tag register

Dossier date: 2026-11-03. Evidence class labels per MOP section 19.

## Product and company

- Capability: portable electrical equipment register with test results, test intervals, next-due dates, reminders and a client-facing compliance record.
- Providers examined: EXTAG (extag.com.au, Perth), TagVault (tagvault.com.au), Clevermode (clevermode.com.au), plus paper and spreadsheet.
- Category: electrical compliance record keeping, AS/NZS 3760 programme support.

## Customer

Three distinct buyers, in ascending order of budget:

1. Test-and-tag operators and electrical contractors, 1 to 10 technicians. They bill per item with a call-out: one published provider charges A$2.10 to A$3.50 per item plus a A$120 service fee per visit, ex GST [E1, PlanetSafe published rates, Aug 2026].
2. Facilities and site managers with in-house maintenance teams, hundreds to thousands of items across sites.
3. Franchise and multi-site operators who need a client portal because their clients demand compliance evidence.

## Pricing

| Provider | Price | Evidence |
|---|---|---|
| TagVault | A$49/mo solo, A$99/mo teams to 5; 14-day trial; client portal free at every tier | E1, vendor pricing section, read this cycle |
| Clevermode | A$200 + GST per year (A$220 inc GST) for the app; tester and printer kit sold with it | E1, vendor FAQ and kit page |
| EXTAG | No published price; sold as a platform implementation; "most teams up and running in weeks, not months"; unlimited users subject to fair use; sovereign hosting on request | E1, vendor page |
| Paper and spreadsheet | Zero licence, unbounded labour | E0 |

## Core capability (the commercial core)

Identify the item, apply the interval, record the result, produce the evidence, know what is due next. Everything else (maps, Power BI dashboards, contractor portals, lifting registers) is adjacency.

## Strongest incumbent features

- EXTAG: NFC, QR and barcode tagging, map view with status pins, embedded Power BI reporting, lifting and inspection registers on one platform, sovereign hosting on request.
- TagVault: two-tap record, per-client branded register, one-click evidence pack for a client WHS audit, emergency lighting and RCD records alongside appliances, CSV export promised, offline recording with sync.
- Clevermode: hardware plus software bundle, QR tag printing, branded PDF reports, local support.

## Weakest incumbent features

- TagVault states on its own site that it does not connect to a tester yet, relying on two-tap entry plus end-of-day CSV import [E1, vendor FAQ]. Readings are the most error-prone part of the job.
- Clevermode couples the register to a purchased tester and printer kit, so the software decision becomes a hardware decision [E1].
- EXTAG sells an implementation, not a signup. Deployment measured in weeks excludes the one and two-person operators who are the majority of the market [E1].
- None of the three publishes a cryptographic record of who tested what and when. The evidence pack is a PDF, which is not verifiable by the client's auditor beyond trusting the PDF [E0 inference from feature pages].
- Interval and next-due logic is configured per customer, which is correct, but it means the register's accuracy depends on the operator's setup discipline [E1].

## Deployment architecture

All three are cloud SaaS with mobile capture. TagVault claims offline capture with sync. Clevermode pairs the app to a Bluetooth tester and printer. EXTAG runs as a hosted multi-module platform with optional sovereign hosting.

## API and interoperability

- TagVault: CSV export promised as "a promise, not a roadmap item" [E1]. No documented public API found this cycle.
- EXTAG: no public API documentation found this cycle; Power BI reporting is embedded, implying an internal data layer rather than an outward API.
- Clevermode: no public API documentation found.
- No incumbent advertises an open import format beyond CSV, which is the migration wedge.

## Open-source competitors

No mature open-source test and tag register was found this cycle. Generic open-source CMMS projects (e.g. openMAINT, Gridex) handle asset schedules but not AS/NZS 3760 registers, tag printing or client evidence packs. This is a thin field, which is unusual and favourable.

## Build complexity

Low to medium. The core is a deterministic data model plus a mobile capture loop plus a report generator. The genuinely hard parts are: tester import formats, tag printing and the interval rules table, which the operator licenses and configures. Estimated 3 to 5 weeks to a credible MVP using Empire's existing local runtime and document generation.

## Switching difficulty

Low. A competitor's register exports as CSV: asset id, description, site, location, test date, result, next due. Mapping those seven fields is a 30-minute job. Printed tags stay on the equipment and do not need replacing if our app reads the same QR payload or falls back to asset id.

## Revenue opportunity

Australia has a large electrical contractor base and a standing compliance obligation. At A$49 to A$149 per business per month across a conservative 2,000 addressable operators in the first two years, the ceiling is A$2.4M ARR before adjacency. The realistic first-year target is 100 paying businesses at A$59/mo or A$70,800 ARR, with each business worth roughly A$600 to A$1,800 a year in avoided manual register work.

## Why it scored 84

- Revenue demand 15/20: proven willingness to pay at A$220 to A$588 per year per business, with a clear buyer and a service revenue line that depends on the record.
- Build feasibility 13/15: small deterministic core, Empire has the runtime, no model dependency.
- Differentiation 18/20: offline depth, tester import, verifiable evidence, flat price, zero marginal cost.
- Migration 8/10: CSV in, CSV out, tags reused.
- Competitive weakness 8/10: hardware coupling, no tester link at the cheapest rival, weeks-long deployment at the enterprise one.
- Strategic reuse 9/10: the same engine resells as lifting registers and emergency lighting records.
- Support burden 4/5: deterministic rules, few integration surfaces, but field users need hand-holding.
- IP risk 9/10: no proprietary code involved, the standard is publicly purchasable and the tool records decisions rather than certifying compliance.

## Rejection conditions

Reject this candidate if the first five prospects say their current tool is good enough and that offline capture is not a real pain or if tester import proves legally or technically blocked on all three major instruments. Either answer kills the differentiation thesis, not the product.
