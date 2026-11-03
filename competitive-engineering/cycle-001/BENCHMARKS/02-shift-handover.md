# BENCHMARK PLAN 02 - Shift handover and issue chasing

Candidate: target 02. Status: RESEARCH (78/100). Benchmark is written now so that the research question is measurable, not because a build is authorised.

## Claim to test

> A shift lead can produce a complete handover in less time than on paper and in less time than on a per-seat CMMS, every open item leaves the shift with an owner and a due date and an item closes only against evidence.

The second and third clauses are the ones that matter. The vendor comparison used in this cycle states that follow-up between shifts and closure on evidence are the least implemented capabilities in the field [E1, third-party vendor guide, 2026-11-02]. If that is true, it is the differentiation and it is testable by reading each incumbent's own workflow rather than by benchmarking speed.

## Metrics

| ID | Metric | Baseline source | Empire target |
|---|---|---|---|
| H1 | Time for a shift lead to complete a handover, 20 events (minutes) | paper, MaintainX trial, Turnover trial | 50% lower than the best incumbent |
| H2 | Share of open items carrying an owner and a due date (%) | vendor workflow inspection | 100% enforced by the model |
| H3 | Share of items closed with linked evidence (%) | vendor workflow inspection | 100% or the item stays open |
| H4 | Floor operation with no network, full shift | vendor documentation | full function, sync on reconnect, zero loss |
| H5 | Annual cost at 30 users | MaintainX US$20-65/user/mo; Turnover US$15/user/mo founding rate | flat per-plant price, stated in A$ |
| H6 | Time from install to first handover on the plant network (minutes) | quoted implementations | under 60 minutes |
| H7 | Recurring fault findability: retrieve last month's same-fault history (seconds) | trial | under 10 seconds |

## Baseline method

Trial MaintainX (free tier) and Turnover and request demonstrations from Opralog and Shiftconnector for the regulated rows. Record versions and dates. Where a vendor publishes no price, record "quote only" and do not invent a figure.

## Protocol

One synthetic plant, 40 machines, three shifts, 25 open items seeded across five categories. Three shift leads run a handover each, in alternating order. Evidence closure is tested by attempting to close an item with a note only, which must be refused.

## Pass criteria

H2 and H3 must be 100% by construction or the product is not different. H1 must beat the best incumbent by 25%. H4 must survive a full shift with the network down. If only speed wins and the closure model does not, the candidate drops to WATCH.

## Stop rule

Do not build a CMMS. Do not build machine-data integration. Handover and chasing only. If a plant wants maintenance work orders, that is MaintainX's job and not our wedge.

## Open question to settle before build

Whether a local appliance is acceptable on plant networks at all. Three site visits answer it better than any document and no build should start until it is answered.
