# Empire Competitive Engineering Programme

MOP-EMPIRE-COMPETITIVE-ENGINEERING-001, owned by Empire Labs Pty Ltd, orchestrated by Sovereign.

Builds follow the Empire AI Language Standard in `ARCHITECTURE-STANDARD.md`: Python-first for research and evaluation, Rust-first for production and edge runtime, TypeScript-first for web interfaces, with any deviation documented rather than assumed.
Cycle 001 has run through the benchmark stage: candidate selected, contract fixed, pilot artefact built and gated, commercial evidence still open. Read `cycle-001/EVIDENCE-PACK.md` first, then `cycle-001/RECOMMENDATION.md`.

## What this directory is

A repeatable machine, not a report. Each cycle leaves behind scored candidates, dossiers, acceptance contracts and, where a candidate survives, an executable measurement harness. The point is that cycle 002 takes less effort than cycle 001 and cycle 010 takes less again.

## Layout

```
competitive-engineering/
  README.md                 this file, the operating manual
  tools/
    score.py                rubric scoring and band assignment, computed not hand-summed
  cycle-001/
    CANDIDATES-25.md        register, rubric breakdown, threshold decisions
    scores.json             the sub-scores score.py consumes
    TARGETS/                five competitor dossiers
    BENCHMARKS/             three acceptance contracts
    RECOMMENDATION.md       stage 6 output, the GO / NO-GO
    STATUS.md               stage position, KPI counters, corrections
    projects/voltledger/    the recommended candidate and its harness
```

When a candidate becomes a real build it graduates to `projects/<name>/` at the repository root with the section 28 file set. `projects/voltledger/` sits here for now because it is still at the benchmark stage.

## The operating loop

Observe, specify, benchmark, rebuild, differentiate, prove, productise, sell. In practice:

1. **Hunt.** Fill the register to at least 25 candidates with evidence of real demand: a published price, a named buyer, a visible complaint. A product that is merely interesting does not enter.
2. **Score.** Sub-scores in `scores.json`, totals from `tools/score.py`. Never hand-sum, because the register and the ranking drift apart within two cycles when you do.
3. **Band.** 80 and above is a build candidate. 65 to 79 is research. 50 to 64 is watch. Below 50 is rejected with the reason kept.
4. **Dossier the top five.** Product, company, customer, price with an evidence class, strongest and weakest features, deployment, API, open-source alternatives, build complexity, switching difficulty, revenue, rejection condition.
5. **Contract the top three.** No code before the acceptance contract exists. Metrics, thresholds, protocol, dataset, pass criteria, stop rule.
6. **Recommend one.** Fill the section 42 block. A ranking is not a build approval.
7. **Prove by execution.** A harness that exits 0 on real gates. Blocked metrics are declared BLOCKED, never estimated.
8. **Validate commercially.** Five prospects, three demonstrations, one paid pilot. Nothing else gets built until that happens.

## Rules that are not negotiable

- **Functionality, not implementation.** Public documentation, published prices, published behaviour, legitimate trials, open-source under compatible licences. No proprietary code, no leaked material, no copied assets, no competitor trademark as an Empire asset. Provenance recorded per project.
- **Evidence classes on every claim.** E0 opinion, E1 public claim, E2 reproduced test, E3 repeatable benchmark, E4 independent or customer evidence. Marketing may only lean on E3 and E4.
- **Price evidence in the register is E1 unless trialled.** The register states which.
- **Blocked is a status, not a gap to fill with a number.** The VoltLedger harness prints four BLOCKED metrics rather than guessing them.
- **Stop at the minimum demonstrable advantage.** Then sell. Feature drift is the named failure mode in the MOP and it is how a three-week build becomes a three-quarter detour.
- **Rejection is a result.** Two candidates were rejected on strategy this cycle and that saved more time than the recommendation earned.
- **Typography gate before any doc leaves the building.**

## Reusable primitives and their status

| Primitive | Status after cycle 001 |
|---|---|
| Rubric scorer | built, tools/score.py |
| Evidence pack with chain, head digest and signature check | built and executed, projects/voltledger/eval/benchmark.py |
| Synthetic register generator with seeded reproducibility | built |
| Date and interval engine with vector-based judgement | built, 18 vectors |
| Benchmark record schema, versions and hashes | built, eval/results |
| Dossier template | established across five dossiers |
| Acceptance contract template | established across three contracts |
| Migration via CSV with column mapping | specified, not built |
| Local runtime packaging | not started |

The next candidate that needs an evidence chain, a synthetic dataset or a vector-scored rule engine starts from these instead of from zero. That is the compounding the MOP asks for.

## KPI table, all cycles

| KPI | 001 |
|---|---|
| Candidates researched | 25 |
| Dossiers | 5 |
| Contracts | 3 |
| Recommended builds | 1 |
| Gates executed | 6 |
| Cash spent | A$0 |
| Paid pilots | 0 |
| MRR | A$0 |

## Next cycle

Cycle 002 opens when the first baseline is measured. Queue: shift handover for discrete manufacturing at 78 and a second register on the VoltLedger engine at roughly one week of marginal work.
