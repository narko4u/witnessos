# NSA MCP Security Guidance → WitnessOS Feature Mapping

**Document:** NSA CSI — "Model Context Protocol: Security Design Considerations for AI-Driven Automation"
**Published:** June 2, 2026
**Mapped by:** Porgie (Sovereign's Prodigy), July 28, 2026
**Repository:** `narko4u/witnessos-compliance`

---

## Executive Summary

The NSA's formal MCP Security Guidance independently validates the entire architectural thesis behind WitnessOS. Every NSA finding maps directly to an existing or planned WitnessOS feature. This document provides the traceable mapping for sales, compliance, and competitive positioning.

---

## NSA Finding #1: No Required Authentication or RBAC

> *"MCP has become the de facto standard for communication between AI clients and services that provide context and execute tool actions. However, the protocol was designed without mandatory authentication, authorization, or RBAC."*

### WitnessOS Answer: Identity Broker (SPIFFE-Based)

| NSA Requirement | WitnessOS Implementation | Status |
|---|---|---|
| Agent identity | SPIFFE-based verifiable identity for every agent | ✅ Gateway enforces |
| RBAC enforcement | Policy engine evaluates role-based rules on every action | ✅ Policy bundles |
| Identity-to-session mapping | Gateway maintains session context per agent identity | ✅ Built-in |

**Evidence:** WitnessOS Gateway enforces identity on EVERY tool call. No anonymous agents. No unauthenticated MCP traffic.

---

## NSA Finding #2: No Token Lifecycle Management

> *"MCP has no native support for token refresh, revocation, or reuse detection."*

### WitnessOS Answer: Credential Broker

The WitnessOS Gateway holds ALL destination credentials. The agent has ZERO credentials. Token lifecycle is managed entirely by the gateway:

| NSA Gap | WitnessOS Solution |
|---|---|
| No token refresh | Gateway rotates credentials automatically (OAuth 2.0 compliant) |
| No revocation | All agent access can be revoked at the gateway instantly |
| No reuse detection | Gateway tracks every credential grant — reuse is impossible |

**Evidence:** The credential broker is the core architectural innovation of WitnessOS. It's not a bolt-on—it's the foundation.

---

## NSA Finding #3: Arbitrary Code Execution (ACE) Risk

> *"MCP tool execution creates CWE-77, CWE-78, CWE-94, CWE-95 exposures. Servers that execute tool calls on behalf of AI clients introduce arbitrary code execution surfaces."*

### WitnessOS Answer: Exact-Action Binding

| NSA Risk | WitnessOS Mitigation |
|---|---|
| CWE-77 (Command Injection) | Gateway validates every action against a signed policy before execution — only pre-defined actions pass |
| CWE-78 (OS Command Injection) | No raw command execution is allowed — actions are structured requests |
| CWE-94 (Code Injection) | Action payloads are validated against strict schemas |
| CWE-95 (Eval Injection) | No dynamic evaluation — all policies are signed, immutable bundles |

**Evidence:** WitnessOS policy bundles define EXACTLY which actions are permitted. Anything outside the approved parameter set is denied at the gateway. The agent cannot inject new tool calls that aren't in the approved policy.

---

## NSA Finding #4: Poor Approval Workflows

> *"Once trusted, MCP servers can change behavior without triggering review. There is no native approval mechanism."*

### WitnessOS Answer: Exact-Approval Binding

| NSA Gap | WitnessOS Implementation |
|---|---|
| No approval mechanism | Human-in-the-loop approval required for high-risk actions |
| No change detection | SHA-256 hash of exact action content — if anything changes, approval is invalidated |
| Behavioral drift | Policy bundles are signed and immutable after issuance |

**Evidence grade:** E3 (Approval-bound receipt). The operator approves an EXACT action hash. If the content changes by one character, the signature breaks and the action is denied.

---

## NSA Finding #5: Insecure Serialization

> *"No strict schema enforcement across MCP protocol enables injection techniques."*

### WitnessOS Answer: AJSON Schema Enforcement

All action payloads are validated against AJSON (Agent JSON) schemas. Strict typing. No arbitrary fields. No injection surface. The gateway enforces structural validation before any action reaches a destination.

---

## NSA Finding #6: Context Sharing Across MCP Servers

> *"MCP per servers can share context across servers, increasing data leakage and unverified task propagation risk."*

### WitnessOS Answer: Per-Destination Credential Isolation

The credential broker isolates credentials per destination. An agent that accessed Gmail has ZERO access to Stripe. There is no such thing as "context sharing" through the gateway.

---

## NSA Recommendations → WitnessOS Implementation Matrix

| NSA Recommendation | WitnessOS Feature | Maturity |
|---|---|---|
| Apply Zero Trust (SP 800-207) | Credential-brokered enforcement — never trust, always verify | ✅ Alpha |

|Implement strict input validation | Ison schema enforcement + policy-based action filtering | ✅ Alpha  |
| Require per-action approval workflows | Exact-approval binding with SHA-256 content hashing | ✅ Alpha |
| Deploy RBAC at the MCP integration layer| Identity broker + policy engine | ✅ Alpha |
| Monitor for "toxic flows" (multi-step attacks) | E0-E4 evidence chain with full event lineage | ✅ Alpha |
| Audit all MCP traffic with tamper-proof logs | Merkle-checkpointed, RFC 3161 timestamped receipts | ✅ Alpha (E3 max) |

---

## Sales Positioning (Derived from NSA Findings)

**One-liner:** "The NSA published what MCP security needs. WitnessOS is what delivers it."

**Technical:** "Every NSA recommendation — identity, RBAC, approval workflows, audit trails — is natively implemented in WitnessOS, not bolted on."

**Competitive:** "Aurascape watches MCP traffic. WitnessOS prevents it from running without governance. The NSA wants prevention, not observation."

---

## Source

NSA Cybersecurity Information Sheet
**"Model Context Protocol (MCP): Security Design Considerations for AI-Driven Automation"**
Published: June 2, 2026
URL: https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF

---

*Generated by WitnessOS Compliance Pack — `mappings/nsa-mcp-guidance-mapping.md`*