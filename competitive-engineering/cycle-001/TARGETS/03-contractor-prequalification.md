# TARGET 03 - Contractor prequalification and site compliance (Australia)

Dossier date: 2026-11-03.

## Product and company

- Capability: prove that every contractor, worker and subcontractor on a site holds current licences, insurance, inductions and competencies, before they are allowed to work.
- Providers examined: ComplyFlow (complyflow.com, Australian, ISO 27001), Altora (altora.com, contractor management module), plus spreadsheet and email chasing.
- Category: WHS and workforce compliance.

## Customer

Head contractors, site owners, facility managers, local government and utilities. The buyer is the WHS or compliance manager; the users are contractors who resent the portal and site supervisors who need a yes or no at the gate.

## Pricing

| Provider | Price | Evidence |
|---|---|---|
| ComplyFlow | Worker licence AU$35 per worker per year, one licence covers that worker across all clients; AI-reviewed company prequalification AU$100 per year; Starter free for 5 users and 5 sites; additional seats from AU$2.92/month; enterprise quoted | E1, vendor pricing page |
| Altora | Contractor management module A$169 per month | E1, vendor pricing page |
| Spreadsheet and email | Zero licence, unbounded chasing labour | E0 |

## Core capability

Collect documents once, verify them against requirements, watch expiry and grant or deny site access. Everything else (inductions, visitor sign-in, permits, inspections) is an adjacent module sold to the same buyer.

## Strongest incumbent features

- ComplyFlow: one worker licence across all clients (a genuinely good model), AI-reviewed prequalification, REST API and MCP published for integrators, ISO 27001, Australian hosting, free starter tier, live access app for site sign-in.
- Altora: simple per-site module pricing, self-service contractor portal, induction and check-in modules.

## Weakest incumbent features

- The per-worker licence model is widely misunderstood; the vendor devotes an FAQ to explaining it [E1, vendor pricing FAQ]. Confusion at the pricing page is a conversion tax.
- Verification is document collection. A PDF of a certificate is accepted on trust; the platform records that someone uploaded it, not that the certificate is genuine or current [E0 inference].
- Expiry chasing still runs on email and portal reminders; the contractor ignores both.
- Both platforms require the contractor to log into a portal they use for six different clients, each with a different system.
- Migration between platforms is painful because worker history and document approval decisions are not exported in a portable form.

## Deployment architecture

Cloud SaaS, Australian hosted at ComplyFlow, multi-tenant, mobile apps for site access and inspections. ComplyFlow publishes an offline-capable inspections app, which shows they know the connectivity problem exists.

## API and interoperability

ComplyFlow publishes REST API and MCP connectors [E1]. Altora integrates with induction and check-in modules; no public API found this cycle. This matters: ComplyFlow is the more open incumbent, so our differentiation cannot be "API", it has to be verification quality and cost.

## Open-source competitors

None credible. The category depends on trust and workflow, not code.

## Build complexity

Medium-high. The document verification logic, expiry rules and the permission model are tractable; the hard part is the trust surface (do we verify the certificate against the issuing body or only record its presence) and the multi-party workflow. Estimated 6 to 10 weeks for a credible core.

## Switching difficulty

Medium. Company and worker records export as spreadsheets from both incumbents on request; the switching cost is re-verifying documents and re-inducing contractors. That is why a migration assistant with bulk document intake and automatic re-verification is a real wedge.

## Revenue opportunity

Per-worker pricing scales with headcount, which means large sites pay real money and small sites pay almost nothing. A site appliance priced per site (A$2,400 to A$9,600 a year) with unlimited workers undercuts large deployments while raising margin. The buyer is conservative and procurement-heavy, so first revenue is slower than target 01.

## Why it scored 73

- Revenue 17/20: high-value category, but long sales cycles.
- Build 10/15: verification and multi-party workflow.
- Differentiation 14/20: local verification with signed receipts beats document collection; cost model beats per-worker licensing.
- Migration 7/10: exportable, but re-verification work.
- Weakness 7/10: portal fatigue, expiry chasing, pricing confusion.
- Reuse 8/10: same evidence and document primitives.
- Support 2/5: multi-party support is expensive and the contractor user is hostile.
- IP risk 8/10: worker data is sensitive; privacy obligations must be handled properly.

## Rejection conditions

Reject if the first five buyers treat prequalification as a commodity already bundled into their WHS platform or if certificate verification against issuing bodies proves legally unavailable. The second is the differentiation, so losing it collapses the case to price competition.
