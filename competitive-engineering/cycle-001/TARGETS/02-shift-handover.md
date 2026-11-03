# TARGET 02 - Shift handover and open-issue chasing (discrete manufacturing)

Dossier date: 2026-11-03.

## Product and company

- Capability: the record of what happened last shift, what is still open, who owns it and when it closes.
- Providers examined: Morsa (morsa.ai, vendor that also publishes the comparison guide), Turnover, MaintainX, UpKeep, Tulip and the regulated electronic shift logs: Octave Tempo (formerly Hexagon j5), Infotechnics Opralog, Eschbach Shiftconnector, Innovapptive.
- Category: manufacturing operations continuity.

## Customer

Plant managers and shift leads in discrete manufacturing, food, chemicals and utilities. The paying buyer is the plant manager or operations manager; the daily user is the shift lead, who will not attend training and will use whatever is fastest at the line.

## Pricing

Prices read on vendor pricing pages on 2 November 2026 as published in the Morsa comparison [E1, third-party published, vendor pages cited]:

| Tool | Price |
|---|---|
| MaintainX | Free plan, then US$20 to US$65 per user per month, billed yearly |
| UpKeep | US$24 to US$55 per user per month |
| Turnover | From US$75 per month for five users at founding rate (US$15/user) |
| Tulip | US$100 to US$250 per interface per month |
| Octave Tempo, Opralog, Shiftconnector, Innovapptive | Quote only |

## Core capability

Capture entries during the shift in structured sections, carry open items forward, give each an owner and due date and close on evidence. The vendor's own analysis of the field says the last two are the least implemented: follow-up between shifts and closure on evidence [E1, Morsa guide, 2026-11-02].

## Strongest incumbent features

- MaintainX and UpKeep: mature mobile apps, work-order linkage, low entry price, fast deployment.
- Opralog, Tempo, Shiftconnector: audit-grade logs for control rooms, historian integration, sign-off, regulated environments.
- Tulip: frontline app platform with machine data and AI copilot.
- Turnover: cheap, purpose-built, public price.

## Weakest incumbent features

- Quote-only pricing on every regulated log, which blocks the small and mid plant entirely.
- Per-user pricing punishes the shift population; a 60-person plant on MaintainX at US$45/user is US$2,700 a month.
- No vendor makes closure depend on evidence by default; closure is a message, not a receipt [E1, Morsa's own gap analysis].
- Cloud dependency on a factory floor with poor Wi-Fi, in an environment where the data is generated at the machine.
- Half of small and medium plants still use paper or spreadsheets, per IoT Analytics (December 2025) as cited in the Morsa guide [E1 secondary].

## Deployment architecture

Cloud SaaS with mobile apps. Tulip is an app platform with on-premise options at enterprise scale. Regulated logs are typically on-premise or private cloud with integration work.

## API and interoperability

MaintainX and UpKeep expose documented REST APIs. Turnover publishes none found this cycle. Regulated logs integrate through historians and ERP connectors, quoted per project. Migration from paper needs an import path for equipment lists and open items; nobody advertises one.

## Open-source competitors

No credible open-source shift handover product. Generic options (NocoDB, Baserow, Odoo maintenance) can be bent into a log and plants do exactly that, which is evidence of demand without a product.

## Build complexity

Medium. The data model is simple; the difficulty is the chase engine (who is waiting on whom, escalation, closure on evidence) and making entry faster than paper at the line. Local runtime on the plant network is a genuine architectural fit, not a marketing line: the plant already has a network and the data should not leave it.

## Switching difficulty

Medium-low. Open items export as CSV or are retyped; equipment lists come from an ERP export. The barrier is behavioural, not technical: the shift lead must adopt it in one shift or the tool dies.

## Revenue opportunity

Mid-market plants pay US$20 to US$65 per seat today. A local appliance priced per plant, not per seat, at A$4,800 to A$12,000 a year undercuts a 30-seat MaintainX deployment (roughly US$16,200/year at US$45) by two thirds while raising margin, because marginal cost after deployment is near zero. Ten plants is A$48,000 to A$120,000 ARR with no per-seat ceiling.

## Why it scored 78

- Revenue 16/20: proven paid category, but procurement is slower and the buyer is more conservative than a contractor.
- Build 11/15: chase engine and adoption risk.
- Differentiation 15/20: local, flat price, closure on evidence, works offline on the floor.
- Migration 7/10: CSV in, but behavioural switching is the real barrier.
- Weakness 8/10: quote-only incumbents, per-seat pricing, no evidence closure.
- Reuse 9/10: the evidence and workflow primitives are the same as target 01.
- Support 3/5: plant deployments need onsite or remote setup.
- IP risk 9/10: no proprietary code, standards not implicated.

## Rejection conditions

Reject if plant managers say the handover problem is already solved by their CMMS or if the first three sites will not allow a local appliance on the plant network. Both are plausible and both kill the deployment model rather than the idea.
