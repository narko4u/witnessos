---
title: "The Evidence Ladder, E0 to E4: A Field Guide for Teams Running AI Agents"
published: false
description: "A practical guide to the WitnessOS evidence ladder: what each grade from E0 to E4 actually proves, how a receipt earns its grade, and how to verify an E4 anchored receipt yourself with standard tooling."
tags: [ai, security, devops, tutorial]
series: false
cover_image: https://narko4u.github.io/witnessos/witnessos-logo.png
---

# The Evidence Ladder, E0 to E4: A Field Guide

In the previous post we made the case that dashboards are not audit trails. This one is the practical field guide: what each evidence grade means, how a receipt earns its grade, and how you can verify an E4 receipt yourself with standard tooling. No vendor login required.

## The ladder at a glance

Every governed agent action in WitnessOS produces a receipt carrying exactly one grade. The grade describes what the evidence can support, nothing more:

| Grade | Name | What it proves |
|-------|------|----------------|
| E0 | Declared | The action was recorded as a declared event. Trust-based. |
| E1 | Observed | A sidecar or SDK witnessed the action. Gaps are possible. |
| E2 | Enforced | A gateway authorised and routed the action under policy. |
| E3 | Corroborated | The destination provider confirmed the outcome. |
| E4 | Anchored | E3 plus an independent RFC 3161 timestamp, revocation checked, and a Merkle inclusion proof, all verifiable offline. Anchoring is one requirement of E4, not a substitute for corroboration. |

The ladder has a strict rule: **grades are earned, never claimed**. If a proof gate cannot be satisfied, the grade is capped down. A deployment that cannot reach an independent timestamp authority tops out at E3 no matter what the vendor's marketing says.

## What each grade looks like in practice

**E0 - Declared.** The agent's self-report lands in a log. Useful for debugging, worthless for accountability. Most agent platforms live here.

**E1 - Observed.** A sidecar process or SDK recorded the event independently of the agent's own memory. Better, but the observer often sits on the same host as the agent, so gaps are possible.

**E2 - Enforced.** This is the inflection point. The action did not just get logged, it got routed through a gateway that applied policy before execution. The gateway is a credential broker: the agent never holds the destination credential directly. Policy, approval, and audit hooks sit between the request and the execution. This is where governance stops being decorative.

**E3 - Corroborated.** The destination provider confirms the outcome. The email service confirms the message was sent. The payment provider confirms the charge. External receipts or state probes corroborate what the gateway believed happened.

**E4 - Anchored.** E4 presupposes E3: it needs a party other than the deployment to have confirmed the outcome. Given that, the case-head commitment is sent to an RFC 3161 Time Stamping Authority. The TSA returns a signed token proving the record existed at a specific moment, and the TSA's certificate chain is checked for revocation at issuance time. The result is a bundle: TSA token plus signed commitment, exportable and verifiable by anyone, offline, with zero trust in the operator.

## How an E4 receipt is built

The order of operations matters, so here is the sequence:

1. **Policy first.** The proposed action is checked against the organisation's allowlist and policy pack before anything executes. No allowlist match, no execution, no receipt above the enforcement floor.
2. **Execution through the broker.** The agent requests, the gateway executes with the held credential, and every hook fires along the way.
3. **Hash chaining.** Every event links to the previous one, so altering any link breaks the visible chain.
4. **Independent timestamp.** The commitment is sealed by an RFC 3161 TSA, not by the operator's own clock.
5. **Revocation check.** The TSA certificate chain is validated at generation time, not assumed valid forever.
6. **Exportable bundle.** TSA token plus signed case-head commitment. Verification runs on the verifier's own machine, from the bundle alone.

## Verify it yourself

The honest test of any evidence system is whether a third party can check it without the vendor. Our public repository ships the schema, the grade model, and a working demo:

- Public repo: [github.com/narko4u/witnessos](https://github.com/narko4u/witnessos)
- Interactive demo: [narko4u.github.io/witnessos/demo.html](https://narko4u.github.io/witnessos/demo.html)

The demo walks one governed action end to end: credentialless agent request, human approval, gateway-held execution, independent verification. No signup, no install.

## Choosing your target grade

Different actions deserve different evidence. A low-risk internal note might be fine at E1. Anything that spends money, touches customer data, or changes production state should target E3 or E4. The rule of thumb: the more irreversible the action, the higher the grade you need to prove it.

If you are evaluating a platform, ask what grade it can actually produce in your configuration, not what its marketing collateral claims. Then ask to see the receipt and verify it yourself. If the vendor cannot hand you a bundle that verifies offline, you do not have an audit trail yet.

---

*WitnessOS is the runtime governance layer for autonomous agents: deterministic policy, governed approval, and cryptographic evidence graded E0 to E4. Built by Empire Labs Pty Ltd.*

*Read the specification: [github.com/narko4u/witnessos](https://github.com/narko4u/witnessos)*

*Enterprise evaluation: [contact@empirelabs.com.au](mailto:contact@empirelabs.com.au)*

*Website: [witnessos.com.au](https://witnessos.com.au)*

---

*Security Division, Empire Labs Pty Ltd*
*[www.empirelabs.com.au](https://www.empirelabs.com.au)*
