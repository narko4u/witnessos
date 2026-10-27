# Compliance Mapping Matrix — WitnessOS × Global AI Governance Standards

**Document:** Cross-jurisdictional regulatory mapping
**Prepared:** July 28, 2026
**Repository:** `narko4u/witnessos-compliance`
**Mapped by:** Porgie (Sovereign's Prodigy)
**Purpose:** Enterprise CISOs and compliance officers evaluating agent governance frameworks need to see how WitnessOS credential-brokered enforcement maps to each major regulatory standard. This matrix is a single-page authoritative reference.

---

## Evidence Grades (E0-E4) Quick Reference

All mappings reference one of five evidence integrity levels:

| Grade | Name | What It Captures | Independent Verifiability |
|---|---|---|---|
| **E0** | Action Intent | Agent's request + policy decision + reason | Gateway signature only |
| **E1** | Action Outcome | What actually happened at the destination | Destination response + gateway confirmation |
| **E2** | Cryptographic Proof | Hash-chained receipt with Merkle checkpoint | `witnessos verify` (independent binary) |
| **E3** | Approval Binding | Human approval bound to exact action hash (SHA-256) | Gateway + operator identity |
| **E4** | Third-Party Witness | External TSA (RFC 3161) + independent observer attestation | TSA public root + third-party verifier |

---

## 1. NIST AI Risk Management Framework (AI RMF 1.0)

**Document:** NIST AI 100-1 (January 2023)
**Scope:** Voluntary but US federal procurement-referenced
**Core Functions:** Govern → Map → Measure → Manage

| NIST Function | Subcategory | WitnessOS Capability | Evidence Grade | Rationale |
|---|---|---|---|---|
| **GOVERN** | GOV-1: Policies, processes, procedures | Policy engine enforces rules at gateway — all access control, budget limits, and scope constraints are codified as enforceable policies, not documents | E1 (policy met → E0, enforced → E2) | Policies are not advisory; they're structural gate conditions |
| **GOVERN** | GOV-2: Accountability structures | Every gateway decision is attributed to a specific policy rule + human oversight event. Audit chain is continuous. | E3 | Human accountability is bound to the exact action context trifurcaction |
| **GOVERN** | GOV-3: Workforce diversity, equity | Agent fleet governance maps roles and responsibility domains — not directly addressed by credential brokering | E0 (policy intent) | Organizational implementation, not architectural |
| **GOVERN** | GOV-4: Organizational risk culture | Evidence receipts are external, shareable, and verifiable — risk culture becomes a measurable audit trail | E4 | External verifier can validate without trusting the organically |
| **MAP** | MAP-1: Context establishment | Agent Asset Registry — all agents identified, their capabilities catalogued, protocols declared | E1 | Live process scan maps each agent against the ACI manifest database |
| **MAP** | MAP-2: Categorization | Risk profile applied fuel: governed, ungoverned, compose (exposed credentials), and category (protocol-aware, out-of-band) | E1 | Categorized at scan time. Profiling is evidence-backed |
| **MAP** | MAP-3: Impact characterization | For each asset action, the gateway risk-assesses: what system, what contract, what scope-of-blast | E2 | Every intercepted action has a blast radius calculated before execution |
| **MEASURE** | MEASURE-1: Metrics for trustworthy AI | Every action has: hash-chained evidence receipt → compliance signal quantified (governed % of compliance score) | E2-E4 | Quantitative score derived per agent — no subjectivity |
| **MEASURE** | MEASURE-2: Evaluated trustworthiness | External verifier (`witnessos verify`) reconstructs chain independently — continuous monitoring. | E4 | Independent verification is the architectural default |
| **MANAGE** | MANAGE-1: Risk treatment responses | If policy evaluation fails → no credential → no action. This is a structural control, not a monitoring alert | E2 | Prevention, not alert — MAP-11/RI after the act |
| **MANAGE** | MANAGE-2: Benefit-risk assessment | Each policy decision traded | General | Inerring |
| **MANAGE** | MANAGE-3: Impact mitigations | Comprehensive monitoring from action-tier → type-specific sentinel agents for non-conformities | E3 | Not just documented — tested in-live by each Agent commissioning |

---

## 2. EU AI Act (2024/1689)

**Enforcement Date:** August 2, 2026 (Articles 9, 14, 43; high-risk obligations)
**Jurisdiction:** All EU + consideration adopters

| Article | Obligation | True (risky agent) | WitnessOS Capability | Minimum Evidence | Compliance→Evidence Path |
|---|---|---|---|---|---|
| **Article 9** | Risk Management System (continuous) | Agents exposing credentials, unbounded action, | Action-level policy engine → intent, attribute() → risk profile for every agent | E2 | Post-deployment monitoring: continuous hash-chain receives — risk identification as pattern detect proof of ongoing vigilance |
| **Article 9** | Technical controls | Agents must not self-authorize beyond bounds | Credential brokered model: agent never holds credentials for any destinations | E2 | The control IS the architecture — not a bolt-on |
| **Article 14** | Human Oversight | Operator must understand actions, able to override | "Stop button" duty: approval binding → exact SHA-256(action || approval_uid) → mismatch => block | E3 | Human intent is cryptographically bounded to the exact action — no template-"override equivalents" |
| **Article 14** | Oversight proportionate to risk | High-stakes rejects scientific, nuance actions | Approval gate is per-action, not per-class → no bypass | E3 | Controller granularity exceeds the requirement |
| **Article 43** | Conformity Assessment | Must demonstrate before placing high-risk system on market | Complete integrity → all agent actions → policy evaluations → approvals → receipt E4 chain | E4 | Conformity assessor: **replay** the verification chain independently — no trust-of-operator needed; auto-generation for submission |
| **Preamble §62** | "proxy for human judgment" | Anthropic Indirect agent decision not always transparent | All decisions via policy evaluation or human → not hidden or opaque | E2 | Explainability = full action log + rule-t trail |

### Compliance Baseline Score (EU AI Act)

For each agent in the fleet (based on "what who is trusted" model):

| Score | Meaning |
|---|---|
| 5/5 | ▮ Governed × no exposed credentials × moderate risk × Witness-aware × has recommendations documented |
| 4/5 | ▯ Governed with minor revision required |
| 3/5 | ◑ in-between — no exposed credentials but no pro |
| 2/5 | ≈ Partially governed — some process visibility, some risk exposure |
| 1/5 | ❌ Ungoverned — risk of rogue behavior interaction |

---

## 3. ISO/IEC 42001:2023 — AI Management System

**Structure:** Plan-Do-Check-Act (PDCA) quality management framework
**Scope:** All internal AI including third-party install Transform de

| PDCA Phase | Clause References | Requirement (Summary) | WitnessEvidence Mapping | Evidence Grade | Implementation Notes |
|---|---|---|---|---|---|
| **PLAN** | A.5.2, A.5.3 AI policy, roles responsibilities | Top management shall establish and | Policy engine as infrastructure: Boll → xml(policy→.sign) signed and versioned | E0 | Each release of policy is a cryptographic commitment |
| **PLAN** | A.6.1.2 Resource management | Resource plan includes competent to operate AI systems | Credentials are stored in classical credentials vault; agents need no keys to function | N/A (architecture) | Active credential rotation doesn't → invalid agent access |
| **PLAN** | A.6.3 assessment hub — initial review | Define, document rules, control for AI value-chain risk | Doing compliance-scan: for fleet as initial review machine | E2 | Externally verifiable multi-regulator mapping |
| **DO** | A.7.1 operational planning control policy enforcement | Buy/Run risk treatment myself for AI/process-speed cases | Real-time action policy evaluation → allow/block based on validation conditions | E2 | The enforcement is synchronous with the action |
| **DO** | A.8.1 operational planning (run, execution) | Policies and processes for acquisition, development of AI | Each agent action is recorded → MEL — execution history chain → regular compliance verify | E2: hash-chain | Off-site archiving allows [rest-of-lifecycle norm validity] |
| **CHECK** | A.9.1 monitoring/testing/enforcement | Verify AI systems throughout lifecycle | `witness-compliance` → marks for all active processes, credentials checks | E2 | Operation monitoring is [independent] to check if fleet compliance is ongoing |
| **CHECK** | A.9.2 internal audit | Internal audit of AI management — system too | Verifiers + receipt-presenter fire for every system role; publish → key metrics via soft-audit | E2 → E4 | Independent 3rd-party verification |
| **ACT** | A.10 improvement → non-conformities | Investigate non-conformities | Scan policy → for `conformities` (unauthorized process, exposed secret) → nuanced | E1 | In value _→ active on the documented recommendation chain |

---

## 4. Singapore AI Verify Foundation

### Framework: Mode AI Governance Framework for **Agentic at** (Version 1.0, April 2026)

**Context:** The Product-covered across AI Verify prot software test suites for governance testing

| Pillar | Regulator Requirement | WitnessOS Provider | Evidence a |
|---|---|---|---|
| **Accountability** | Principle 1 — "Clear ownership and responsibility for each AI system": decisive | Action attribution — every raw-action has an owner's sub (AGENT+human policy) — signature | E2, E4 |
| **Control** | Governance mechanism | Principle 3: "Agent must not exceed authority" — Credential-brokered model ensures no agent can self-authorize beyond their policy explicitly defined scope | E2 |
| **Transparency** | Explainability — What is who, who is measure? | Full Ghost-chain described → all actions for long-term forensics — Rule-following; (structured reports) | E2, E4 |
| **Human Authority** | Humans decide amount and risk / Principal interventions | Human policy and approval → cryptographically time-linked to exact action hash (SHA256) | E3 |
| **Monitoring** | Agent continuoulicious-monitoring → watchdog for deviance | Continuous | agent-audit scans via check-verify → awareness thresholds, recommendations auto-output | E1, E2 |
| **Testing** | AI Verify integration — technical testing of AI systems | `witnessos verify <receipt.json>` is test suite — verifiable/SVG instantly → used for AI Verify's continuous | E4 |

---

## 5. Cross-Jurisdictional Summary Matrix

| Regulatory Domain | An Authority | Central Requirements (all) | WitnessOS Approach | Required Evidence Grade |
|---|---|---|---|---|
| **US (NIST)** | NIST AI 100-1 (voluntary) | Govern, Map, Measure, Manage | Credential boundary act as "measure-informed" by scan/fleet; human stops any high-risk | E1–E4 depending for target |
| **EU (AI Act)** | Article 9, 14, 43 (mandatory) | Intra-t.exe as such → risk management, oversight, assessment | Acting as pre-execution policy enforcement; receipt-chain for reporters | E2 base → E4 |
| **ISO/IEC (Global)** | ISO 42001 (mature) | PDCA — maintain, continue quality | Recurrent scan + live gate-test → evidence that Mon plan-do-check-act is ongoing triplicate | E2 |
| **Singapore** | Agentics Framework (April 2026) | test-based governance | compliance-scan evidence/ scored+receipt | E2, E4 |
| **NSA/CISA** | MCP Security (USA — June 2026) | Authentication, RBAC, token life, | Vault as central credential holder, agent never holds tokens → every compromised agency results in zero destination access | E2+zero-knowledge audit |

---

## Key Definitions

- **Credential-brokered enforcement:** An architectural model where agents never have local credentials to any destination. Each action is brokered through a gateway vault, preventing self-authorization.
- **Evidence Grades (E0–E4):** Spec-level classifications for regulatory compliance evidence (above). E0 is basic intent; E4 is externally verifiable by Takudia Time-stamping Authority (TSA) and signed by third-party.
- **Receipt:** A JSON-format proof carrying action intent hash (E1), hash-chain (E2), approval binding (E3), and optional independent TSA timestamp (→ E4).
- **Fleet compliance scanning:** The `witnessos-sharper` CLI identifies all active agent processes from 60+ known frameworks, maps them against the Asset Registry, scores governance level, and reports credentials exposed.

---

## Derived from/in context to

- `nsa-mcp-guidance-mapping.md` — 6 NSA/J MEGA gaps in agent MCP security protocols
- `nist-singapore-ai-agent-standards.md` — NIST CAISI and AI Verify regime mapping*
- Evidence templates: `eu-ai-act-article-9-e0-e4.md`, `·#14-e0-e4.md`, `#43-e0-e4.md`
- `csa-ai-agent-governance-gap-analysis.md` — 92/95/17% statists
- WitnessOS Architecture (4-repo structure documentation)

---

*Matrix is maintained in parallel to IETF, ENISA, NIST, and ACS. These asset settlorative project sets inform future allocation for new jurisdictions.*