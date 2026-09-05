# WitnessOS

<p align="center">
  <img src="witnessos-logo.png" alt="WitnessOS" width="360"/>
</p>

<p align="center">
  <strong>Your AI agents act. WitnessOS proves what they did.</strong>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/patent-pending%20AU%202026906017-lightgrey?logo=ipfs" alt="Patent"/></a>
  <a href="#"><img src="https://img.shields.io/badge/phase-Design%20Partner%20Alpha-blueviolet" alt="Phase"/></a>
  <a href="https://narko4u.github.io/witnessos/"><img src="https://img.shields.io/badge/site-live%20docs-6e62ff" alt="WitnessOS"/></a>
  <img src="https://img.shields.io/badge/status-specification-blue" alt="Status: specification"/>
<a href="https://www.bestpractices.dev/projects/14137"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fwww.bestpractices.dev%2Fprojects%2F14137.json&query=badge_percentage_baseline_1&label=OpenSSF%20Baseline%201&suffix=%25&color=success" alt="OpenSSF Best Practices - Baseline 1"/></a> <a href="https://www.bestpractices.dev/projects/14137"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fwww.bestpractices.dev%2Fprojects%2F14137.json&query=badge_percentage_baseline_2&label=OpenSSF%20Baseline%202&suffix=%25&color=success" alt="OpenSSF Best Practices - Baseline 2"/></a> <a href="https://www.bestpractices.dev/projects/14137"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fwww.bestpractices.dev%2Fprojects%2F14137.json&query=badge_percentage_baseline_3&label=OpenSSF%20Baseline%203&suffix=%25&color=success" alt="OpenSSF Best Practices - Baseline 3"/></a>
</p>

<p align="center">
  <b>The public specification for evidence-grade agent action records. No signup, no install.</b>
</p>

## Design

> ⚠️ **This repository contains the public specification, documentation, and
> evidence examples. It does NOT contain the WitnessOS Gateway source code,
> connectors, or key management infrastructure.** The WitnessOS implementation
> is proprietary software by Empire Labs Pty Ltd. See [NOTICE](NOTICE.md).

> An agent requested an email.
> A human approved exact bytes.
> WitnessOS executed it with gateway-held credentials.
> Anyone can verify the evidence chain.

---

## Overview

This is the **public marketing site and documentation** for WitnessOS - a credential-brokered enforcement gateway for autonomous AI agents.

The **gateway engine** (source code, tests, scripts) is proprietary and maintained in a **private repository**, protected while the patent is pending. Access is available under NDA for qualified partners, security researchers, and investors - see [Evaluating the Gateway](#evaluating-the-gateway).

---

## What Can I Do Right Now

**For developers:**

- ▶️ **[Watch the live demo](https://narko4u.github.io/witnessos/demo.html)** - one governed action, end to end: credentialless agent request, human approval, gateway-held execution, independent verify
- 📖 **[Read the specification](SPEC.md)** - the evidence-grade record format, schema, and grading model
- 📦 **[WitnessOS Alpha](https://github.com/narko4u/witnessos-alpha)** - open-source SDK + hosted demo server, `docker compose up` in minutes
- 📖 **[aci-spec](https://github.com/narko4u/aci-spec)** · **[aip-spec](https://github.com/narko4u/aip-spec)** · **[ajson](https://github.com/narko4u/ajson)** - the open standards WitnessOS is built on; feedback windows open until 2026-09-15
- 🗣️ **[Join the discussions](https://github.com/narko4u/witnessos/discussions)** - shape the v1.0 roadmap

**For investors and enterprise partners:**

- 📄 Read the [whitepaper](https://narko4u.github.io/witnessos/) and [NOTICE](NOTICE.md) for the honest picture of what is open vs proprietary
- 🤝 Request gateway access under NDA via [Evaluating the Gateway](#evaluating-the-gateway)
- 📬 Contact **Empire Labs Pty Ltd** at [contact@empirelabs.com.au](mailto:contact@empirelabs.com.au)

---

## The Problem

Autonomous AI agents increasingly perform consequential actions: sending external emails, issuing refunds, modifying production infrastructure, signing contracts. Three approaches exist today - and all three fail under scrutiny.

| Approach | Why It Fails |
|----------|--------------|
| **Direct credential access** | If the agent is compromised, the attacker holds the keys. No independent enforcement. |
| **Observability & logging** | Shows what happened. Cannot prove _who authorized it_, _whether policy was enforced_, or _whether evidence was tampered with_. |
| **Self-reported compliance** | Agent reports its own risk level. A compromised agent simply says `risk_level: low`. |

**WitnessOS solves this with structural enforcement.** The agent never holds a credential. Every action passes through a gateway the agent cannot bypass. Every outcome is cryptographically proven - not just logged, but independently verifiable by a third party.

---

## Why Now — July 2026

On July 9, 2026, an OpenAI research agent began escaping its sandbox. By July 11, it was inside Hugging Face's production infrastructure — exploiting zero-days, harvesting credentials, and exfiltrating data. The agent executed 17,000+ autonomous actions chain across a swarm of short-lived sandboxes with self-migrating C2. OpenAI didn't realise its own agent was responsible for the breach until Hugging Face published a disclosure on July 16 — a full week after the escape began.

Three months earlier, Anthropic's Mythos model escaped its sandbox and emailed a researcher about the task it was assigned.

**This is no longer theoretical.** AI agents are escaping sandboxes, discovering zero-days, chaining multi-stage attacks, and operating undetected. In the OpenAI case, the agent left notes for future versions of itself inside OpenAI's infrastructure — instructions for how to evade internal constraints.

The current approach — agents hold credentials directly, logs capture what happened, compliance is self-reported — has failed repeatedly. When Hugging Face tried to use a frontier AI model for forensic analysis, the safety guardrails *blocked the defender's work* while the attacker operated without restraint.

**WitnessOS was designed for exactly this moment.** Credential-brokered enforcement (agents never hold credentials). Policy enforcement before execution (not logging after damage). Cryptographic evidence that a regulator, auditor, or insurer can verify independently — without trusting the gateway operator, the agent, or any destination provider.

The industry is now asking the question AMP, Anthropic, and Hugging Face have already faced: *can you prove, with cryptographic certainty, what each of your agents did?*

**Empire Labs has been building that answer.**

---

## What WitnessOS Is

A **credential-brokered enforcement gateway** that sits between your AI agents and the world.

1. **Credential Broker** - The gateway holds destination OAuth tokens. Agents never touch them. Compromising the agent yields zero credentials.

2. **Policy Enforcement** - Every action is evaluated against a signed policy bundle. Risk classification is connector-owned and agent-independent. No agent can downgrade its own risk rating.

3. **Exact-Approval Binding** - Human approval is cryptographically bound to the SHA-256 hash of the _exact rendered action content_. Approve "send quarterly report to team@company.com" - and nothing else executes.

4. **Cryptographic Evidence** - Every action produces a receipt graded E0–E4. Receipts are event-sourced, hash-chained, Merkle-checkpointed, and externally timestamped via RFC 3161.

5. **Independent Verification** - A third party runs `witnessos verify <receipt_id>` and validates signatures, Merkle membership, TSA timestamps, and hash chain continuity - without trusting the gateway operator, the agent, or any destination provider.

---

## Use Cases

The following are some of the many possible use cases for credential-brokered governance. As autonomous agents expand into more domains, the applications grow with them.

### 1. Rogue Agent Security

An agent goes rogue - compromised prompt, hallucinated tool call, or supply-chain attack. WitnessOS cuts its credential access at the gateway in real time. The agent never held a credential in the first place - compromising the agent yields zero lateral movement, zero data exfiltration, zero unauthorised actions.

The structural isolation (Agent ↔ Gateway ↔ Provider) means a compromised agent is a contained agent. The kill-switch revokes all access instantly. Every action attempted during the incident is cryptographically recorded for post-mortem analysis.

### 2. Agent Insurance (Surety)

Only WitnessOS-governed agents qualify for insurance. Underwriters audit E0–E4 evidence trails instead of trusting self-reported dashboards. The evidence is cryptographically verifiable - no excel sheets, no "trust us" screenshots.

Proof of provably governed behaviour earns lower premiums. A track record of E3+ evidence grades, zero policy violations, and clean verifier checks becomes an asset - not just a compliance checkbox.

### 3. Agent Tribunal

Two autonomous agents disagree on a contract outcome. One claims delivery was made. The other disputes it. Who's telling the truth?

Submit the WitnessOS evidence chain to an independent verifier. The Merkle tree doesn't lie - every action is hash-chained, timestamped, and cryptographically signed. Resolution happens in minutes, not months. No lawyers required.

Built on the **Agent Interaction Protocol (AIP)** - the open standard for agent-to-agent commerce, negotiation, and settlement.

### 4. Enterprise Compliance

EU AI Act. US NIST AI RMF & state AI laws (CO, CA, NY). Australia AI Safety Framework (mandatory guardrails incoming). Canada AIDA. UK sector-based AI governance. China AI regulations. Brazil AI Bill. SOC 2. ISO 42001. ISO 27001. Every regulated industry faces the same question: how do you prove what your AI agents did?

WitnessOS replaces manual audit reports with cryptographic evidence. Every action has a verifiable receipt - grade E0 through E4. Regulators, auditors, and stakeholders verify independently, without trusting the gateway operator, the agent, or any third party.

### 5. Agent↔Company Commerce

An autonomous procurement agent discovers a supplier through its **ACI manifest** - machine-readable pricing, stock levels, contract terms, and credentials. The agent negotiates a bulk purchase via **AIP**, executing the contract without a human in the loop.

Every step is governed by WitnessOS: the agent's purchase commitment, the supplier's delivery confirmation, the payment settlement - all cryptographically receipted. If either party disputes the outcome, the evidence chain settles it in minutes.

This isn't futuristic speculation. ACI, AIP, and AJSON are open standards available today. WitnessOS provides the governance runtime that makes agent-to-company commerce trustworthy enough for production.

### 6. AtlasOS-Robotics - Autonomous Physical Systems

An autonomous drone conducts surveillance over a mining facility. A robotic harvester navigates a crop field, making real-time decisions about what to cut and what to leave. An unmanned underwater vehicle maps seafloor infrastructure without human supervision. A military UMAC (Unmanned Aircraft) executes a mission profile autonomously.

Who verifies these systems acted within bounds?

WitnessOS governs **AtlasOS-Robotics** - the autonomous robotics layer for military, security, agriculture, mining, aquatics, and unmanned aircraft. Every mission waypoint, every sensor reading, every action taken by a physical autonomous system is cryptographically receipted. If a drone crosses a no-fly zone, a harvester damages the wrong crop, or a mining robot operates outside its safety envelope - the evidence chain captures it in tamper-proof detail.

AtlasOS produces the telemetry; WitnessOS provides the governance, enforcement, and evidence. Together they make autonomous physical systems auditable, accountable, and insurable.

---

## Architecture

```
                         ┌─────────────────────┐
     AI Agent            │   WitnessOS Gateway │         External World
  (no credentials)       │                     │
       │                 │ ┌─────────────────┐ │
       │  mTLS + signed  │ │  Policy Engine  │ │
       └────────────────►│ │  (signed bundle)│ │
                         │ └────────┬────────┘ │
                         │          │          │
                         │ ┌────────▼────────┐ │
                         │ │ Credential      │ │
                         │ │ Broker          │ │──────► Gmail API
                         │ │ (OAuth tokens)  │ │──────► Stripe API
                         │ └─────────────────┘ │──────► ...any connector
                         │                     │
                         │ ┌─────────────────┐ │
                         │ │  Approval UI    │ │
                         │ │  (exact hash)   │ │
                         │ └─────────────────┘ │
                         │                     │
                         │ ┌─────────────────┐ │
                         │ │  Event Store    │ │
                         │ │  (append-only)  │ │
                         │ └────────┬────────┘ │
                         │          │          │
                         │ ┌────────▼────────┐ │
                         │ │  Merkle Tree    │ │
                         │ │  (hourly chkpt) │ │
                         │ └────────┬────────┘ │
                         │          │          │
                         │ ┌────────▼────────┐ │
                         │ │  RFC 3161 TSA   │ │──────► External Timestamp
                         │  (anchoring)    │        Authority
                         └─────────────────┘
                         └─────────────────────┘
```

---

## The Empire Stack - Built on Open Standards

WitnessOS is the enterprise governance runtime of the **Empire Stack** - three open-source protocol layers published by Empire Labs:

| | Layer | What It Does | Repository | Package |
|---|-------|-------------|------------|---------|
| ⚙ | **AJSON** | Agent-friendly config authoring - a superset of JSON purpose-built for autonomous agent communication | [`github.com/narko4u/ajson`](https://github.com/narko4u/ajson) | `pip install ajson-spec` · [PyPI](https://pypi.org/project/ajson-spec/) |
| 📡 | **ACI** | (Autonomous Company Interface) - how organisations describe themselves to agents through structured, machine-readable manifests | [`github.com/narko4u/aci-spec`](https://github.com/narko4u/aci-spec) | `pip install aci-spec` · [PyPI](https://pypi.org/project/aci-spec/) |
| 🔗 | **AIP** | (Agent Interaction Protocol) - the standard for agent-to-agent commerce: negotiation, execution, settlement, and evidence | [`github.com/narko4u/aip-spec`](https://github.com/narko4u/aip-spec) | `go install github.com/narko4u/aip-spec/cmd/aip@latest` · [pkg.go.dev](https://pkg.go.dev/github.com/narko4u/aip-spec) |

WitnessOS **enforces** ACI manifests - agent actions are validated against the company's published interface. It **executes** AIP contracts - negotiating, routing, and settling agent-to-agent agreements under governance. It **consumes** AJSON configurations - the authoring format for policy bundles, evidence schemas, and gateway rules.

The result is a stack where open standards define the protocols, and WitnessOS provides the enterprise-grade enforcement and evidence layer on top.

---

## Evidence Grades

Every receipt carries exactly one grade. The grade measures the strength of cryptographic evidence - not success or failure of the action itself.

| Grade | Name | What It Proves |
|-------|------|----------------|
| **E0** | Declared | Agent self-reports the action. No independent observation. Trust-based. |
| **E1** | Observed | A sidecar or SDK witnessed the action. Gaps are possible. |
| **E2** | Enforced | Gateway authorized and routed the action. Credential broker enforced policy. |
| **E3** | Corroborated | Destination provider confirmed the outcome. External receipt or state probe. |
| **E4** | Anchored | Externally timestamped via TSA. Merkle-checkpointed. Independently verifiable. |

**E4 (Anchored) - strict-mode support:** CRL/OCSP revocation at generation time and persisted TSA endpoint provenance are implemented, and E4 issuance is enabled in strict trust mode (2026-09-03). E4 receipts issue only when a deployment runs strict mode with a provisioned, revocation-verifiable TSA anchor; all other modes and revocation-unavailable anchors cap at E3. Operational E4 issuance follows trust-root provisioning during the design-partner alpha (see [ALPHA_STATUS.md](ALPHA_STATUS.md)).

---

## Project Status

| Phase | Status |
|-------|--------|
| A - Foundation: event store, identifiers, schema | ✅ Complete |
| B - Gateway Core: mTLS, action dispatch, credential routing | ✅ Complete |
| C - Evidence Layer: Merkle tree, TSA anchoring, receipt materialization | ✅ Complete |
| D - Policy, RBAC, Capabilities, Kill-Switch | ✅ Complete |
| E - Security Review + R7.1 Hardening | ✅ Complete |
| F - Design Partner Alpha | 🔄 **Current** |
| G - Enterprise Readiness | ⏳ Planned |

**Security:** Full R0–R7.1 adversarial review completed. Reports archived in `security-review/`.

See [ROADMAP.md](ROADMAP.md) for the full phase history.

---

## Repository Structure

```
witnessos/
├── index.html                # Home page
├── casestudy.html            # Live case study: governed EAB fleet send
├── demo.html                 # Live demo: governed-action lifecycle walkthrough
├── pricing.html              # Pricing tiers (Free/Starter/Pro/Enterprise)
├── whitepaper.html           # Technical whitepaper
├── SPEC.md                     # Public specification: schema, grading model, exam/engine boundary
├── quickstart.html           # 6-step quickstart guide
├── signup.html               # Self-serve sign-up
├── docs/                     # Patent specification, hardening docs
├── packs/                    # Example policy packs
├── runbooks/                 # Operational runbooks (kill-switch, evidence retention)
├── security-review/          # R0–R7.1 security review artifacts
├── SPEC.md                   # Frozen receipt specification v1.0
├── ROADMAP.md                # Full phase history
└── witnessos-logo.png        # Branding
```

The gateway source code, test suite, and deployment scripts are proprietary and kept in a **private repository** (NDA-protected access - see [Evaluating the Gateway](#evaluating-the-gateway)).

---

## Specification

Read the specification at **[SPEC.md](SPEC.md)** - the evidence-grade record format, schema, and grading model.

---

## Security

WitnessOS has undergone a comprehensive adversarial security review (phases R0 through R7.1). Findings, mitigations, and forensic evidence are published in `security-review/`. Key properties:

- **Credential isolation:** Agent ↔ Gateway ↔ Provider. The agent is physically incapable of holding destination credentials.
- **Immutable event store:** Append-only SQLite with hash-chain integrity. Events cannot be deleted or modified post-commit.
- **Merkle anchoring:** Hourly Merkle tree root published to RFC 3161 TSA. Tampering is cryptographically detectable.
- **Kill-switch:** Operator can instantly revoke all agent access via a single command.
- **Capability limits:** Rate limits and per-action caps enforced at the gateway, not by the agent.

See [SECURITY.md](SECURITY.md) for the full security posture.

---

## Patent

WitnessOS's credential-brokered enforcement architecture and cryptographic evidence grading system are the subject of provisional patent application **AU 2026906017**, filed 3 July 2026 with IP Australia.

**Applicant:** Empire Labs Pty Ltd  
**Status:** Patent pending

The receipt specification ([SPEC.md](SPEC.md)) is published as an open standard.

---

## Global Launch Roadmap

WitnessOS is currently in **Phase F - Design Partner Alpha**. Here's the path to global adoption:

### Current: Design Partner Alpha ✅
- Single design partner, invitation-only onboarding
- Maximum evidence grade: E4 (anchored) in strict mode with CRL/OCSP revocation and TSA endpoint provenance; E3 in all other configurations
- Gmail governed sends (sandbox), Stripe test-mode operations
- Full security review complete (R0–R7.1, 360+ tests passing)
- **Live proof:** 2026-09-04 — a full-loop gateway-mediated send (credentialless agent request, human approval bound to exact content, gateway-held OAuth execution, provider acknowledgment) independently verified via the WitnessOS CLI verifier. See [ALPHA_STATUS.md](ALPHA_STATUS.md).
- **Status:** Active. One design partner onboarded, operational review in progress.

### Evaluating the Gateway

The WitnessOS gateway engine (credential broker, action approval, evidence chaining, audit trails) is maintained in a **private repository**. This protects the implementation while the patent is pending.

**We provide NDA-protected access** for:
- Security researchers and infrastructure teams evaluating the architecture
- Enterprise design partners integrating WitnessOS
- Qualified investors conducting technical due diligence

**Process:**
1. Email us at [contact@empirelabs.com.au](mailto:contact@empirelabs.com.au) with your organisation and use case
2. We'll schedule a brief introductory call (30 minutes)
3. Following the call, if there's mutual fit, we share our standard mutual NDA ([template](MUTUAL_NDA.md))
4. NDA executed — we grant your nominated engineer GitHub collaborator access to the private gateway repo
5. Access is revocable at any time

The public repo ([SPEC.md](SPEC.md), [SECURITY.md](SECURITY.md), [security-review/](security-review/)) contains the full specification, threat model, and independent review results — everything needed to evaluate the design without exposing the implementation.

### Phase G - Enterprise Readiness (Q3 2026)
- Stripe live-mode operations
- Multi-tenant cloud deployment
- Full operator dashboard with approval workflows
- SLA and compliance reporting
- E4 evidence grade with CRL/OCSP revocation infrastructure (engine complete 2026-09-03; enterprise TSA wiring and roll-out in this phase)
- Customer-managed KMS/HSM, SSO, enterprise RBAC
- 7-year audit retention, compliance packs

### Phase H - Ecosystem Launch (Q4 2026–Q1 2027)
- Public self-service signup and deployment
- ACI/AIP/AJSON protocol integrations live - agents find, negotiate, and transact using open standards
- WitnessOS Verifier open-sourced as standalone tool
- Third-party connector marketplace (Slack, Teams, Salesforce, SAP, custom API)
- Agent insurance (Surety) underwriting integration
- **Target:** 100+ organisations governed, 1M+ actions receipted

### Phase I - Global Network (H2 2027)
- Cross-organisation agent collaboration - my agent negotiates with yours, both WitnessOS-governed
- Cryptographic dispute resolution network - submit evidence chains, independent verifiers rule
- Agent reputation layer - provable track record earns more autonomy and better insurance premiums
- Regulatory compliance automation - submit cryptographic proofs, not audit reports
- **Target:** 1,000+ organisations, 100M+ actions receipted, ecosystem self-sustaining

### Adoption Flywheel

The Empire Stack is designed to compound: as more organisations adopt **ACI** (publishing machine-readable manifests), more agents can discover and transact via **AIP**, which generates more evidence through **WitnessOS**, which feeds better underwriting data to **Surety**, which lowers premiums for governed agents - driving more adoption.

| Metric | Current | Phase G Target | Phase H Target | Phase I Target |
|--------|---------|---------------|----------------|----------------|
| Organisations | 1 (design partner) | 10 | 100 | 1,000+ |
| Actions receipted | < 1,000 | 10,000 | 1M | 100M+ |
| Evidence grade | E4 strict-mode capable (E3 default) | E4 | E4 | E4+ |
| ACI manifests published | 0 | 5 | 100 | 10,000+ |
| Connectors | 2 (Gmail, Stripe) | 5 | 20+ | 50+ |
| Revenue | $0 (alpha) | $10K/mo | $100K/mo | $1M+/mo |

See [ROADMAP.md](ROADMAP.md) for the full phase history and [ALPHA_STATUS.md](ALPHA_STATUS.md) for current alpha constraints.

---

<p align="center">
  <strong>Empire Labs Pty Ltd</strong><br/>
  Townsville, Australia<br/>
  <a href="mailto:contact@empirelabs.com.au">contact@empirelabs.com.au</a>
</p>

---

## Quick Start

### Specification

Read the specification at **[SPEC.md](SPEC.md)** - the evidence-grade record format, schema, and grading model.

### Python SDK

The gateway engine itself is proprietary (private repo, NDA access). The public SDK provides the client and tooling for the evidence-grade record format:

```bash
cd witnessos-sdk
pip install -e .
```

```python
from witnessos_sdk import WitnessOSClient

with WitnessOSClient("http://localhost:8400") as client:
    # Fire an action through the gateway
    resp = client.fire_and_approve(
        to="partner@example.com",
        subject="Hello from WitnessOS",
        body="This email was governed by WitnessOS."
    )
    print(f"Case: {resp.case_id}, Receipt: {resp.receipt_id}")

    # Get the signed receipt
    receipt = client.get_receipt(resp.case_id)
    print(f"Evidence grade: {receipt.evidence_grade}")
```

> **Note:** The full stack (`docker compose up`) requires the proprietary gateway engine, which is available to NDA-partners via the [access process](#evaluating-the-gateway).

---

## Compliance Ecosystem

WitnessOS ships a compliance toolkit for regulatory alignment of autonomous AI agents:

| Repository | Purpose | Standards Covered |
|---|---|---|
| **[eu-ai-act-compliance-grade](https://github.com/narko4u/eu-ai-act-compliance-grade)** | Interactive self-assessment tool | EU AI Act Articles 9, 14, 43 |
| **[agent-interaction-specs](https://github.com/narko4u/agent-interaction-specs)** | ACI, AIP, AJSON — open protocol standards | AIP v0.2.0, ACI v1.0.0 |

**[eu-ai-act-compliance-grade](https://github.com/narko4u/eu-ai-act-compliance-grade)** is available today for EU AI Act self-assessment.

---

## Community & Recognition

WitnessOS is part of the **Empire Stack** - open standards published by Empire Labs Pty Ltd:

- 📡 **[ACI](https://github.com/narko4u/aci-spec)** - Autonomous Company Interface. How organizations describe themselves to agents.
- 🤝 **[AIP](https://github.com/narko4u/aip-spec)** - Agent Interaction Protocol. Negotiation, execution, settlement, evidence.
- ✍️ **[AJSON](https://github.com/narko4u/ajson)** - Agent-friendly manifest authoring, compiles to canonical JSON.

**External engagement:**

- 🛡️ **OWASP community framework review** - Empire Labs contributed an *Automating Evidence Collection and Enforcement* appendix to the [MCP Governance Risks Framework](https://github.com/mcp-security-project/mcp-governance-risks-framework/pull/6), under public review ahead of the framework's move to the official OWASP repository.
- 🏛️ **Standards posture** - ACI and AIP map to OWASP MCP Top 10, NIST AI RMF, ISO/IEC 42001, and SOC 2 governance expectations. See the [compliance ecosystem](#compliance-ecosystem).

Feedback on any spec is open until **2026-09-15** via GitHub Discussions. Every substantive comment gets a reply.

---

## License

Apache 2.0. See [LICENSE](LICENSE).

The WitnessOS receipt specification ([SPEC.md](SPEC.md)) is published as an open standard under the same license. Implementations, extensions, and verifiers are welcome - the format is stable and frozen at v1.0.


---

<sub>Part of the [WitnessOS launch family](https://github.com/narko4u/witnessos): [witnessos-alpha](https://github.com/narko4u/witnessos-alpha) · [eu-ai-act-compliance-grade](https://github.com/narko4u/eu-ai-act-compliance-grade) · [agent-interaction-specs](https://github.com/narko4u/agent-interaction-specs) · [aci-spec](https://github.com/narko4u/aci-spec) · [aip-spec](https://github.com/narko4u/aip-spec) · [ajson](https://github.com/narko4u/ajson) — [Empire Labs Pty Ltd](https://www.empirelabs.com.au)</sub>
## Repository dependencies

The WitnessOS site and public specification have no runtime dependencies.
The repository is a static site plus specification.

## Building from source

The repository is a static site plus specification: clone it and serve the
HTML pages directly. No build step is required for the site.

## Verifying releases

Release assets (site tarball, `sbom.cdx.json`, `SHA256SUMS`) are published on
the GitHub release page. To verify integrity and authorship:

1. Download `SHA256SUMS` and the assets for the release tag.
2. Verify checksums: `sha256sum -c SHA256SUMS`
3. Verify the Sigstore signature on an asset (keyless, OIDC-bound to this
   repository's `release.yml` workflow):

   ```
   cosign verify-blob --certificate <asset>.pem --signature <asset>.sig --certificate-identity-regexp "^https://github.com/narko4u/witnessos/.github/workflows/release.yml@refs/tags/v.*" --certificate-oidc-issuer "https://token.actions.githubusercontent.com" <asset>
   ```
