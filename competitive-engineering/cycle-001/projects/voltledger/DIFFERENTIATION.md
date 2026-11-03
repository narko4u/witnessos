# DIFFERENTIATION.md - VoltLedger

The rule from MOP section 30: the answer cannot be "because we built one too" and it must be measurable.

## What we are not claiming

- Not cheaper. TagVault is A$49 per month and Clevermode is A$220 a year. A price fight with a small Australian vendor is a fight we should refuse.
- Not broader. EXTAG already sells test and tag, lifting, safety and inspections on one platform with Power BI reporting. Matching that is a two-year detour.
- Not more compliant. No software confers compliance and every incumbent says so correctly.

## Claim 1: readings import instead of being typed

Hypothesis, currently E0. One incumbent states on its own site that it does not connect to a tester and relies on two-tap entry plus end-of-day CSV import. If that is the state of the market, the seconds are in transcription and the errors are in transcription.

- Measured by: T1 and T2 in COMPETITOR-BENCHMARK.md, on the same hardware with two operators and alternating rounds.
- Falsified if: median time per item is within 25% of the incumbent. Then speed is not the wedge and the pitch must rest on Claim 2 alone.

## Claim 2: the evidence can be checked without trusting us

Currently E2 for the mechanism, not E3 or E4 for the customer outcome. The harness verifies a 500-record pack offline, detects a single flipped byte and rejects a wrong key, in under 5ms at p50. No incumbent examined in this cycle advertises a tamper-evident record, only a PDF pack.

Why a buyer cares: the record exists to satisfy a client, an auditor or an insurer. A PDF proves what the software printed. A signed pack proves what was recorded and fails if anything is altered afterwards.

- Measured by: T5, plus a third-party verification test where someone who has never installed the product verifies a pack on their own machine.
- Falsified if: buyers say their clients accept the existing PDF and never challenge it. That is a real possibility and the first five interviews must test it directly.

## Claim 3: a full day with no signal and no loss

Hypothesis, E0 until the device test runs. One incumbent claims offline recording with later sync. We claim the same thing plus reconciliation the operator can see and we can prove loss equals zero because the queue is a file on the device, not a promise.

- Measured by: T3, four hours with the radio off, then reconcile and count.
- Falsified if: records are lost or duplicated on reconnect.

## Claim 4: one engine, three registers

Internal advantage, not a customer claim yet. Test and tag, lifting and emergency lighting are the same data model with different item classes and interval sources. This is why the second and third products cost about a week each and why a single-purpose competitor has to build three times.

- Measured by: build cost of register two after register one ships, recorded in the KPI table.
- Falsified if: register two needs more than two weeks of work.

## Claim 5: the data stays with the business

Design fact, verifiable: one database file per business, capture with no network, no telemetry of customer data by default and an export that is the whole register in CSV. For a contractor whose client list is the equity in the business, this is a different conversation from a cloud portal.

- Measured by: inspection of the shipped build and by the export test in T7.

## The one-sentence position

> Every record you hand a client can be checked by them without trusting your software and the round still works in a basement with no signal.

## What would make us lose

- The two cheapest incumbents add tester import and signed evidence in the same quarter. Possible: both are small and both are close to the problem.
- Buyers do not care about verifiable evidence because nobody has ever challenged their PDF. Then this is a feature nobody pays for and the candidate drops to WATCH.
- Tester manufacturers lock their import formats behind partner agreements and we cannot read the instruments the customers actually own.
