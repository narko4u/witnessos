# COMMERCIAL.md - VoltLedger

The six questions from MOP section 22, answered before any further engineering.

## Buyer

Primary: the owner of an Australian electrical contracting business with 2 to 6 technicians that runs test and tag rounds as recurring revenue. They buy software personally, decide in a week and pay by card.
Secondary: an in-house facilities or maintenance team with a few hundred to a few thousand items across sites. Slower sale, larger contract.

## Problem

Two problems and the second is the one that gets paid for:

1. The round is recorded by hand from a tester display, which is slow and produces transcription errors.
2. When a client, insurer or auditor questions a record, the contractor produces a PDF that proves nothing except that the software printed it.

## Existing spend

| Option | Annual cost to a 2-technician business | Evidence |
|---|---|---|
| TagVault solo | A$588 | E1, vendor page |
| Clevermode | A$220 including GST plus tester and printer kit | E1, vendor page |
| EXTAG | quoted, implementation based | E1, vendor page |
| Paper and spreadsheet | zero licence, unbounded labour, weakest evidence | E0 |

## Offer

A local-first register that imports the readings, works with no signal and produces an evidence pack the client can verify without installing anything. Flat price, no per-client fees, whole register exports as CSV at any time.

## Price

Hypothesis, not validated:

| Tier | Price | Included |
|---|---|---|
| Solo | A$59/mo | one technician, unlimited items, client evidence packs |
| Team | A$149/mo | up to 5 technicians, same features, shared register |
| Business | A$1,290/yr | unlimited technicians, priority support, migration done for them |

This is 20% to 50% above TagVault's A$49 and A$99 tiers. The premium buys tester import and verifiable evidence. If neither of those proves valuable in interviews, the price must fall to A$49 or below and the case weakens to a commodity fight we should not enter.

## Migration

1. Export the current register as CSV.
2. Import with column mapping, seven fields, tested as gate T7.
3. Keep the tags already on the equipment, matching on asset id.
4. Run one round in parallel and compare counts.

Target: under 30 minutes and we do the first import for them. No lock-in to argue about, because the export is the same shape as the import.

## Proof

- Executed today: the due engine is correct on 18 hand-computed cases, the evidence pack verifies offline, a single flipped byte fails it and a wrong key is rejected.
- To be executed: per-item time against an incumbent on the same hardware and a no-signal day with zero loss.
- To be executed with a customer: one real round on their own devices, counted against their paper or their current app.

## Honest unit economics

A two-technician business running 1,500 items a month at A$2.50 per item bills about A$3,750 a month for the work (published per-item rates are A$2.10 to A$3.50 plus a call-out, E1). Typing readings at 20 seconds per item is roughly 8.3 hours a month. At 8 seconds via import it is 3.3 hours. The saving is about 5 hours, roughly A$300 at A$60 per hour loaded cost and that is an assumption, not a measurement.

Against that, our premium over the cheapest incumbent is A$50 a month. The labour case therefore stands up, but thinly and it is not the reason someone switches. The reason is the evidence and one disputed client claim or one failed audit costs more than a year of any of these tools. That claim is E0 until a customer tells us it happened to them.

At 100 paying businesses on a blended A$70 a month, revenue is about A$84,000 a year. At 250 businesses it is about A$210,000. Cost to serve is close to zero because the product runs on the customer's device. The constraint is distribution, not capacity, which is why the first customer type is the one Empire can reach without paid media.

## Customer validation plan

MOP section 23 requires five qualified prospects, three demonstrations and one paid pilot before another feature set is built.

1. Identify 20 Queensland electrical contractors who advertise test and tag.
2. Approach five, one at a time, with a single ask: a 30-minute demonstration at their office with their own register export.
3. Run three demonstrations.
4. Convert one to a paid pilot at A$500 for 30 days, refundable, with the benchmark run on their own equipment.
5. Record what they say about evidence, specifically whether a client has ever challenged a record.

Approval required before any contact: outbound to prospects is not permitted without Eddie's word (revenue-initiative boundaries).

## Risks

| Risk | Effect | Mitigation |
|---|---|---|
| Evidence is a feature nobody pays for | Differentiation collapses to price | Interview five buyers before building the app |
| Cheapest incumbent adds tester import | Speed claim weakens | Lead with evidence, keep import as table stakes |
| Tester import formats blocked | Core workflow broken | Support CSV from the instrument's own software and manual entry |
| Standard citation misused | Legal exposure | Never embed interval tables, always state the tool does not determine compliance |
| Working name conflicts | Rebrand cost | Trademark search before any public use |
| Incumbent bundles a free tier | Price pressure | Stay on the evidence and offline claims, not on price |
