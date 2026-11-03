# CYCLE-001, STAGE 6 - Recommended first build

Date 2026-11-03. Reports 1 to 4 of MOP section 38 are delivered by this file and the documents it references.

## Recommendation

```text
PRODUCT:                VoltLedger (working name, not trademark cleared)
CURRENT PROVIDER:       TagVault, Clevermode, EXTAG (plus paper)
CUSTOMER:               Australian electrical contractors and test and tag operators, 2 to 6 technicians
CURRENT PRICE:          TagVault A$49/mo solo and A$99/mo to 5 users; Clevermode A$220/yr inc GST plus tester kit; EXTAG quote only
CORE CAPABILITY:        Identify the item, apply the interval, record the result, produce evidence, know what is due next
CURRENT WEAKNESS:       No tester import at the cheapest platform, hardware coupling at the second, implementation-only sales at the third and no verifiable evidence at any of them
EMPIRE VERSION:         Local-first register, offline capture with reconciliation, imported readings, tamper-evident evidence pack verified offline, flat price
PRIMARY ADVANTAGE:      The record a contractor hands a client can be verified by that client without trusting the software, which no examined incumbent offers
SECONDARY ADVANTAGE:    A full day with no signal and zero loss and one engine serving three registers (test and tag, lifting, emergency lighting and RCD)
BUILD ESTIMATE:         3 to 5 weeks to a pilot-ready MVP for one register, from a standing start, standard library only
MIGRATION STRATEGY:     CSV import and export on seven fields, existing equipment tags reused, first import done for the customer inside 30 minutes
PROPOSED PRICE:         A$59/mo solo, A$149/mo to 5 technicians, A$1,290/yr per business unlimited (hypothesis, unvalidated)
FIRST CUSTOMER TYPE:    Queensland electrical contractor doing test and tag rounds, reached personally, not by paid media
OPPORTUNITY SCORE:      84/100
```

## Why this and not the others

Three of the top five candidates are the same commercial core on different registers. That is the finding that decides the cycle: one engine, three products, one buyer. Test and tag is the entry register because it has the highest revenue score, the clearest buyer and the shortest build and the other two registers then cost about a week each instead of months.

Shift handover (78) is the better long-run business: flat per-plant pricing against per-seat incumbents, a real local-appliance fit and a bigger contract value. It loses this cycle because the sale needs site visits and the chase engine is harder than the register. It stays in RESEARCH and should be the second build, not the first.

Contractor prequalification (73) has the largest contract values and the fastest cost story against per-worker licensing, but its differentiation depends on verifying documents against issuing bodies, which is a legal and partnership problem before it is an engineering one.

Agent governance (69) was excluded on strategy: WitnessOS already occupies that ground and building a second product there would compete with the Empire's own engine.

## GO / NO-GO

**Conditional GO to the benchmark stage. NO-GO to a production build today.**

The condition is specific: the advantage must be measured on a real device against a real incumbent before the capture app is built out. MOP section 42 is explicit that ranking first is not enough and the honest state of the evidence is that the deterministic core is proven while the commercial claim is not.

What has already been demonstrated by execution, not assertion:

| Evidence | Result |
|---|---|
| Due-date and status engine against hand-computed vectors | 18 of 18 |
| Evidence pack, 500 records | p50 3.93ms, max 4.89ms |
| Offline verification from the pack alone | passes |
| Tamper detection on one flipped byte | passes |
| Wrong signing key rejected | passes |
| Duplicate asset id and non-positive interval rejected at import | passes |

That is E2/E3 evidence for the mechanism. It is not evidence that a technician is faster and it is not evidence that anyone will pay.

## Approvals requested

1. Open a TagVault trial and request an EXTAG demonstration, so the baseline in COMPETITOR-BENCHMARK.md can be measured. Cost: one A$49 month at most.
2. Permission to approach five Queensland electrical contractors for a 30-minute demonstration each. No spend, no public claim, no product claim beyond what is measured.
3. A decision on the capture target: phone browser first or a packaged app. This changes the build estimate and the offline proof.

## What happens when those are answered

Week 1: measured baseline on the incumbent, expanded vector set to 200 cases, capture loop with a file-backed queue.
Week 2: T1 and T2 timed with two operators, T3 no-signal day, T7 import from a real competitor export.
Week 3 to 5: pilot build, migration tool, three demonstrations, one paid pilot at A$500 for 30 days.
Then and only then, report 6 with commercial validation results.

## Funnel record

25 candidates identified and scored. 10 advanced. 5 dossiers. 3 benchmark plans. 1 recommendation. 13 were not advanced: 2 on strategy (agent governance competes with WitnessOS, tender and quoting are covered by Oscar), 11 to WATCH on score.
