# BENCHMARK PLAN 01 - Test and tag register (acceptance contract)

Candidate: target 01. Status: BUILD CANDIDATE (84/100).
Rule applied: no implementation begins before this specification is fixed (MOP section 9). Any change after the first measurement run is versioned, not edited.

## What is being claimed

The claim to test is narrow and falsifiable:

> A technician records the same test-and-tag round on the Empire engine in materially less time than on the incumbent, the records survive a no-signal day with zero loss and the resulting evidence can be verified by a third party without trusting the application that produced it.

Price is explicitly not the claim. TagVault lists A$49/mo solo and A$99/mo for five users, which is cheap. Undercutting it is not a defensible position for a company of Empire's size and any plan that rests on being A$10 cheaper should be rejected at this gate.

## Metrics

| ID | Metric | Incumbent value | Empire target | Measurement class |
|---|---|---|---|---|
| T1 | Median time per item, scan to committed record (seconds) | to be measured on trial | 40% lower | E3 when measured |
| T2 | P95 time per item (seconds) | to be measured | 40% lower | E3 |
| T3 | Records lost across a 4-hour no-signal round | claimed offline, unmeasured | zero loss, reconciled | E2 |
| T4 | Evidence pack generation for 500 items (P50 / P95 seconds) | PDF export, unmeasured | under 5s / under 12s | E3 |
| T5 | Third-party verification of an evidence pack | not offered | verifiable offline from the pack alone | E2 |
| T6 | Due-date correctness on 200 synthetic cases | configured, not audited | 200/200 | E3 |
| T7 | Import fidelity from a competitor CSV | n/a | 100% of rows, zero manual edits | E2 |
| T8 | Cost per 1,000 items tested, per month, 5 technicians | A$99 licence plus labour | stated as a computed comparison, not asserted | E3 |
| T9 | Time from download to first completed test | "weeks, not months" (EXTAG), signup (TagVault) | under 10 minutes | E2 |

## Baseline method

1. Purchase or start a legitimate trial of TagVault (A$49 tier) and request an EXTAG demonstration. Trials are permitted under MOP section 2; any spend is a separate approval item.
2. Record the incumbent at version and date, on the same hardware, with the same synthetic site.
3. Do not test against a straw man: use the cheapest credible incumbent for the time and cost rows and the enterprise one for the deployment and evidence rows.

## Test protocol

- Site: one synthetic site of 120 items across four locations, matching the dataset generator in eval/dataset.
- Operators: two, one familiar with test and tag, one new to it.
- Rounds: three per operator per system, alternating order to remove learning effects.
- Each round: scan or select 40 items, commit a result, ten include a deliberate fail, three are untagged, one is a duplicate scan.
- No-signal condition: rounds 2 and 3 for the Empire engine run with the network interface disabled for the duration.
- Instrumentation: timestamp at scan event and at commit, recorded by the harness, not by the operator.

## Dataset

Synthetic, generated. Fields: item_id, description, site, location, class, last_test_date, interval_months, result, measured_values, tag_payload. No customer data is used at any point. The generator and its seed are committed so the dataset is reproducible.

The interval values are supplied by the operator or test business, not asserted by the tool. The tool does not determine compliance and must say so, exactly as the incumbents do.

## Due-date correctness cases (T6)

Includes: interval boundaries, month-end dates, leap year, a fail followed by a repair and retest, an item moved between sites mid-cycle, an item with no prior test, an item with a corrupted tag payload and a duplicate asset id. Each case has an expected date computed by hand and recorded in the vector file. Judgement lives in the vector, not in the tool.

## Evidence pack (T4, T5)

Pack contains: the register rows, the test events, a manifest, a SHA-256 digest of the payload and a detached signature. Verification is a separate script that reads only the pack. It must succeed offline, on a machine that has never run the product and must fail loudly on a single flipped byte.

## Pass criteria

- At least three of T1, T3, T5, T6, T9 show a material advantage, where material means 25% or better on a timed metric or a binary capability the incumbent does not have.
- No metric materially worse than the incumbent (10% tolerance on timed metrics, none on correctness).
- T6 must be 200/200. A single miss is a fail, because the whole product is a date calculation.
- T5 must verify offline and must detect tampering.

## Stop rule

Stop building at the point where the pass criteria are met. Do not add dashboards, maps, Power BI, invoicing, franchise portals or lifting registers before there is a paying customer for the first register (MOP sections 20 and 22).

## Recording requirements

Every run writes a JSON record: software version, commit, model version if any, hardware, OS, test set hash, timestamp, configuration, operator id and result hash. Results live in eval/results with the raw timings, not just the summary.
