# EU AI Act Evidence Templates — E0-E4 Mapping

**Regulation:** EU AI Act 2024/1689 — High-Risk AI System Obligations
**Enforcement Date:** August 2, 2026 (Articles 9, 14, 43)
**Repository:** `narko4u/witnessos-compliance`
**Mapped by:** Porgie, July 28, 2026

---

## Quick Reference: E0-E4 Evidence Grades

| Grade | Name | What It Captures | Verifiable By |
|---|---|---|---|
| **E0** | Action Intent | Agent's request + policy decision + reason | Gateway signature |
| **E1** | Action Outcome | What actually happened at the destination | Destination response + gateway confirmation |
| **E2** | Cryptographic Proof | Hash-chained receipt with Merkle checkpoint | Independent verifier (`witnessos verify`) |
| **E3** | Approval Binding | Human approval bound to exact action hash | Gateway + operator identity |
| **E4** | Third-Party Witness | External time authority (RFC 3161) + independent observer | TSA + third-party verifier |

---

## Article 9 — Risk Management System

### Requirement
> "A risk management system shall be established, implemented, documented and maintained in relation to high-risk AI systems throughout their lifecycle."

### WitnessOS Evidence Template

| Article 9 Obligation | WitnessOS Evidence | Minimum Grade | Sample Receipt |
|---|---|---|---|
| 9(2)(a): Identify known risks | Policy bundle defines risk classes per action type | E1 | `witnessos policy evaluate --risk external_email` |
| 9(2)(b): Estimate risks under intended use | Gateway logs every action, build risk profile over time | E2 | Hash-chained daily risk summaries |
| 9(2)(c): Evaluate risks from incidents | Approval events log denied actions + reason | E1 | `witnessos events --type denied --since 30d` |
| 9(2)(d): Adopt risk management measures | Policy updates are signed, timestamped, auditable | E2 | `witnessos policy diff --at 2026-01-01 vs 2026-08-01` |
| 9(5): Testing procedures | All gateway changes validated against 232-test suite | E0 | Test run receipts with pass-fail evidence |

**Compliance statement:** WitnessOS provides continuous, cryptographically-verifiable evidence of risk management activity for every governed agent action.

---

## Article 14 — Human Oversight

### Requirement
> "High-risk AI systems shall be designed and developed in such a way that natural persons can effectively oversee them."

### WitnessOS Evidence Template

| Article 14 Obligation | WitnessOS Implementation | Evidence Grade | Receipt Template |
|---|---|---|---|
| 14(1): Human oversight throughout use | Every action goes through a human—every decision matches a policy rule | E1 | Per-action receipt |
| 14(2): Prevent or minimize risks | High-risk actions require explicit human approval before execution | E3 | Approval-bound receipt (SHA-256 content binding) |
| 14(4)(a): Understand capabilities/limitations | Policy bundle describes exactly what agent CAN do | E0 | `witnessos policy list` |
| 14(4)(b): Monitoring | Ongoing action logs—real-time, immutable, verifiable | E2 | Merkle-checkpointed transaction log |
| 14(4)(c): Interpret output correctly | Every approval shows exact action content + destination + parameters | E3 | Human-readable approval screen |
| 14(4)(d): Disregard, override, stop | Any action denied → blocked at gateway + receipt captured | E1 | Denied action receipt |
| 14.3: Human-over-the-loop monitoring | Continuous monitoring via gateway health dashboard + approval queue | E2 | Approval queue depth + stale approval timer |

---

## Article 43 — Conformity Assessment

### Requirement
> "High-risk AI systems shall undergo the relevant conformity assessment procedure before they are placed on the market."

### WitnessOS Evidence Template

| Article 43 Obligation | Resolution Evidence | Grade | How To Generate |
|---|---|---|---|
| 43.1: Internal control based conformity | Certified policy bundle + test suite passes form internal control evidence | E2 | `witnessos policy certify --scope internal_control` |
| 43.2: Technical documentation requirements | Every receipt, every approval, every credential grant logged | E0-E4 | Full receipt export |
| 43.3: Documentation available for 10 years | Merkle-checked + RFC 3161 timestamping = forever verifiable | E4 | `witnessos audit-pack --period 2026-2027` |
| 43.4: Post-market monitoring | Continuous receipt generation + verification | E2 | `witnessos verify --continuous` |

**Compliance statement:** Article 43 conformity assessment is continuous, not episodic. Every governed action generates evidence. A regulator can run `witnessos verify` and receive a full, independently verifiable evidence trail for any period.

---

## E0-E4 → Compliance Use Cases

| Use Case | Evidence Grade Needed | WitnessOS Capability |
|---|---|---|
| Load-carrying demonstration | E2 | `witnessos compliance eu-ai-act --report demo` |
| Annual audit | E4 | Complete evidence pack with RFC 3161 third-party timestamps |
| Breach investigation | E3 | Every action, every approval, every denial, hash-chained |
| Insurance claim (agent caused damage) | E2-E4 | Independently verifiable by insurer without trusting operator |
| Design audit | E1 | Approval records + automated test results |

---

## Next Compliance Step

1. Build `cli/compliance.py` — CLI that generates these evidence templates
2. Add Article 13 chain (transparency) 
3. Add CSV export for EU technical documentation supplements
4. Wire into WitnessOS Gateway health endpoint

---

*Generated by Compliance Pack — `templates/eu-ai-act/evidence-templates.md`*