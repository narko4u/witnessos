# TARGET 04 - Lifting and height-safety equipment registers

Dossier date: 2026-11-03. This is the same commercial core as target 01 on a second register, which is why it scored 74 and why it is cheap to reach.

## Product and company

- Capability: register of lifting gear and height-safety equipment (slings, chains, shackles, harnesses, lanyards, hoists) with inspection intervals, competent-person results, next-due dates and evidence for the site auditor.
- Providers examined: EXTAG (lifting register module on the same platform as its test and tag product), Asset Konnect (asset and CMMS platform, Australia, published annual plans).
- Category: asset compliance, high-risk equipment.

## Customer

Lifting equipment suppliers and hire companies, crane and rigging contractors, mine sites, construction head contractors and any site where a lifting register is audited. The person who pays is the same operations or WHS manager as target 01 and often the same company already runs test and tag.

## Pricing

| Provider | Price | Evidence |
|---|---|---|
| EXTAG | No published price; sold as an implementation on a shared platform | E1 |
| Asset Konnect | Professional A$1,990 per year, Enterprise A$3,990 per year, Nonprofit Lite A$690 per year | E1, vendor plans page |
| Paper register and tag system | Zero licence, unbounded labour, fails at audit | E0 |

## Core capability

Item identity, inspection interval, competent-person result, next due, evidence pack. Identical to target 01 with a different item taxonomy and a different interval source.

## Strongest incumbent features

- EXTAG: one platform across test and tag, lifting, scaffolding and inspections; NFC/QR tagging; map view; Power BI reporting.
- Asset Konnect: transparent annual pricing, CMMS breadth, compliance reporting, Australian support.

## Weakest incumbent features

- The register is a module in a platform sold by implementation, so the small rigging company that needs only the register cannot buy it.
- Annual platform pricing (A$1,990 to A$3,990) is a hard decision for a five-person business.
- Same evidence weakness as target 01: the output is a report, not a verifiable record.
- Lifting equipment moves between sites and between owners; none of the tools handles transfer of custody with evidence.

## Deployment architecture

Cloud SaaS, mobile capture, tagging hardware optional.

## API and interoperability

No public API found for either provider this cycle. Both import from spreadsheet by project.

## Open-source competitors

None found specific to Australian lifting registers.

## Build complexity

Low, because it is target 01's engine with a different configuration: item classes, interval rules supplied by the licensed inspector and a custody-transfer event. Marginal build cost over target 01 is roughly one week.

## Switching difficulty

Low. Same CSV shape as target 01: item id, description, class, site, inspection date, result, next due, inspector.

## Revenue opportunity

Smaller population than test and tag, but higher value per customer and frequently the same customer. The strategic value is incremental: it raises revenue per account without a second sale and it blocks a competitor from owning the register category around our first product.

## Why it scored 74

- Revenue 12/20: narrower population, higher per-account value.
- Build 12/15: reuse of target 01.
- Differentiation 14/20: custody transfer with evidence, flat price, offline.
- Migration 7/10: same CSV shape.
- Weakness 7/10: implementation-only sales, annual platform pricing.
- Reuse 9/10: the clearest reuse case in the cycle.
- Support 4/5: deterministic.
- IP risk 9/10: no proprietary code; the applicable standards are publicly purchasable and the inspector supplies the intervals.

## Rejection conditions

Reject as a standalone product. It should ship as a second register on the target 01 engine and only if target 01 reaches its first paying customer.
