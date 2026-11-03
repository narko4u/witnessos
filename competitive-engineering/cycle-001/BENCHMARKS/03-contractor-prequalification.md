# BENCHMARK PLAN 03 - Contractor prequalification and site compliance

Candidate: target 03. Status: RESEARCH (73/100).

## Claim to test

> A site can verify that a contractor's documents are genuine and current, not merely uploaded, at lower cost per worker than per-worker licensing and the gate decision works with no network.

The honest risk is in the first clause. If "verify" only means "record that a PDF exists", we are ComplyFlow with a different price and the candidate should be rejected. The benchmark therefore tests verification quality first and speed second.

## Metrics

| ID | Metric | Baseline | Empire target |
|---|---|---|---|
| C1 | Share of submitted documents checked against the issuing body or a signed source, not just uploaded (%) | vendor workflow: upload and manual review | measurement of what is achievable, then a target |
| C2 | Time to review 100 documents against requirements (minutes) | trial | 50% lower |
| C3 | Contractor time to submit a compliant pack (minutes) | trial | 50% lower, no new account required |
| C4 | Gate decision latency, cached (ms) and offline | live lookup | under 200ms, offline capable |
| C5 | Annual cost at 150 workers | ComplyFlow AU$35/worker/yr = A$5,250 plus AU$100 prequalification; Altora A$169/mo module | flat per-site price stated in A$ |
| C6 | Exportability of worker and approval history on exit | vendor-dependent | full export, portable format |
| C7 | False-clear rate: expired or invalid document admitted | not published | zero on the test set |

## Protocol

Build a synthetic contractor set of 25 companies and 150 workers, with 40 seeded defects: expired insurance, wrong entity name, missing induction, mismatched licence class, a forged certificate, a superseded certificate version and a duplicate worker across two companies. Run the set through each system as a reviewer and count clearances. C7 is measured against the seeded truth.

## Pass criteria

C7 must be zero. If the incumbents also achieve zero on this set, the differentiation claim is dead and the candidate drops to WATCH. C5 must show a real cost reduction at 150 workers against per-worker licensing. C2 and C3 are secondary.

## Legal and privacy gate

Worker documents include personal information. Storage, retention and cross-border handling must be settled before any pilot and the design must allow the customer to hold the data themselves. This is a pre-build gate, not a post-build cleanup.

## Stop rule

Do not build the induction, permit, visitor or inspection modules. Prequalification and gate access only. The rest is how ComplyFlow became a suite.
