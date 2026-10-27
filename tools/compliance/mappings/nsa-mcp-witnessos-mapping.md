# NSA MCP Security Guidance → WitnessOS Feature Mapping

**Source:** NSA CSI "Model Context Protocol: Security Design Considerations for AI-Driven Automation" (June 2, 2026)
**Document:** [media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF](https://media.defense.gov/2026/Jun/02/2003943289/-1/-1/0/CSI_MCP_SECURITY.PDF)
**Mapped:** July 28, 2026

---

## Executive Summary

The NSA's MCP Security Guidance identifies **8 critical security gaps** in the Model Context Protocol and makes **5 overarching recommendations**. WitnessOS's credential-brokered architecture satisfies **all 8 gap remediations** and **all 5 recommendations** — structurally, not observationally. No other product in the AI agent governance space can make this claim.

---

## NSA Finding → WitnessOS Feature Mapping

### F1: MCP Reverses Familiar Interaction Pattern

| | |
|---|---|
| **NSA Finding** | MCP servers both *query AND execute* actions for clients — unlike traditional API servers which only respond to queries. This inverted pattern creates new attack paths where a compromised or malicious server can execute arbitrary actions on the client's behalf. |
| **NSA CWE Ref** | N/A (architectural pattern finding) |
| **WitnessOS Feature** | **Credential-Brokered Gateway** |
| **How It Satisfies** | WitnessOS Gateway brokers ALL credentials between agents and tools. The agent never holds keys to any destination. Even if an MCP server is compromised or malicious, it cannot execute arbitrary actions because: (a) it has no credentials to authenticate with downstream services, and (b) every action is bound to a specific approval with a SHA-256 content hash. The inverted pattern is structurally contained — the gateway is the only entity with authority to execute, and it enforces policy on every call. |
| **Evidence Grade** | E2 — hash-chained action sequence proving gateway mediation on every call |
| **Verification** | Third-party verifier confirms: no tool call in the chain was possible without gateway signature |

---

### F2: Arbitrary Code Execution (ACE)

| | |
|---|---|
| **NSA Finding** | MCP servers can receive and execute arbitrary code from clients. References CWE-77 (Command Injection), CWE-78 (OS Command Injection), CWE-94 (Code Injection), CWE-95 (Eval Injection). |
| **WitnessOS Feature** | **Exact-Approval Binding + Schema Enforcement** |
| **How It Satisfies** | WitnessOS's exact-approval binding requires a human to approve the *exact* SHA-256 hash of every action before execution. The approval is bound to the precise content of the action — not a class of actions, not a template. If the action content changes (even by one character), the hash changes, and the approval is invalidated. Additionally, the ACI (Agent Configuration Interface) manifest defines strict schemas for every tool call, preventing malformed or malicious payloads from reaching the execution boundary. |
| **Evidence Grade** | E1 — signed event record showing approved hash matches executed hash |
| **Verification** | `witnessos verify <receipt_id>` confirms hash match between approved and executed action |

---

### F3: No Required Authentication or RBAC

| | |
|---|---|
| **NSA Finding** | MCP has no required authentication mechanism. Session-to-identity mapping is optional, meaning any agent can impersonate any other agent. No role-based access control exists at the protocol level. |
| **WitnessOS Feature** | **mTLS Authentication + Identity Registry + Policy Engine** |
| **How It Satisfies** | WitnessOS Gateway requires mTLS (mutual TLS) for every agent connection. Each agent has a unique X.509 identity bound to its ACI manifest. The Policy Engine enforces role-based access control (RBAC) at the gateway — not at the protocol level. Agents are mapped to roles via signed policy bundles (OPA/Rego). The gateway rejects any request without a valid identity, and identity-to-role mapping is checked on every action. No agent can impersonate another because the cryptographic identity is bound to the mTLS session. |
| **Evidence Grade** | E2 — hash-chained action sequence with identity assertions at each link |
| **Verification** | Independent verifier checks: (1) mTLS certificate chain, (2) identity-to-policy mapping, (3) role authorization for each action |

---

### F4: No Token Lifecycle Management

| | |
|---|---|
| **NSA Finding** | MCP has no support for token lifecycle management — refresh, revocation, or reuse protocols are absent from the specification. Once a token is granted, it has no expiration mechanism. |
| **WitnessOS Feature** | **Credential Vault with Token Lifecycle** |
| **How It Satisfies** | WitnessOS Gateway holds ALL destination credentials in an encrypted vault. The gateway manages token lifecycle: (a) **refresh** — tokens are rotated automatically based on policy, (b) **revocation** — the gateway can revoke ALL agent access in real-time via a single policy update, and the agent has no cached credentials to fall back on because it never held them, (c) **reuse prevention** — each credential grant is single-use bound to the specific action, preventing token replay. The agent cannot store, cache, or reuse tokens because tokens never reach the agent. |
| **Evidence Grade** | E3 — multi-agent verified receipt including token lifecycle events |
| **Verification** | Verifier confirms: credential vault logs show token issue → use → revocation cycle with no agent-side caching |

---

### F5: Poor Approval Workflows

| | |
|---|---|
| **NSA Finding** | Once an MCP server is trusted, it can change its behavior (tool definitions, resource access patterns) without triggering a new approval workflow. The trust model is binary and static. |
| **WitnessOS Feature** | **Exact-Approval Binding + Policy Versioning** |
| **How It Satisfies** | WitnessOS does not have binary "trusted/not-trusted" — every action requires its own approval bound to the SHA-256 hash of the exact content. If a tool's behavior changes (new parameters, modified schema), the hash of any subsequent action changes, and the old approval is invalid. Additionally, the Policy Engine supports versioned policy bundles: any change to tool definitions, access patterns, or resource scopes requires a new signed policy. The system detects drift between the registered tool schema and the current schema on every call. |
| **Evidence Grade** | E1 — signed event record showing approval hash binding |
| **Verification** | Verifier checks: tool schema version on approval ↔ tool schema version on execution must match |

---

### F6: Insecure Serialization

| | |
|---|---|
| **NSA Finding** | MCP uses JSON-based serialization without strict schema enforcement, enabling injection techniques and malformed payload attacks. |
| **WitnessOS Feature** | **AJSON Schema Enforcement + Input Validation** |
| **How It Satisfies** | WitnessOS uses AJSON (Agent JSON — a superset of JSON with strict schema enforcement) for all inter-agent communication. AJSON enforces: (a) required/optional field validation, (b) type constraints on every parameter, (c) regex and format validation on string fields, (d) max length and range constraints on numeric fields, (e) rejection of unknown fields (no extra-properties). Malformed payloads are rejected at the gateway before reaching any execution boundary. The ACI manifest defines the exact schema for every tool and resource. |
| **Evidence Grade** | E0 — raw event log showing schema validation pass/fail for each payload |
| **Verification** | Verifier replays payload against AJSON schema; rejection proves enforcement |

---

### F7: Context Sharing Across MCP Servers

| | |
|---|---|
| **NSA Finding** | Context is shared across MCP servers in a multi-server architecture, increasing data leakage risk and enabling unverified task propagation. An action in Server A can seed an action in Server B without review. |
| **WitnessOS Feature** | **Per-Action Isolation + Context Boundary Enforcement** |
| **How It Satisfies** | WitnessOS Gateway enforces per-action isolation boundaries. Each tool call is an isolated transaction with its own: (a) credential grant, (b) approval hash, (c) evidence receipt, (d) context boundary. Context does NOT flow between servers unless explicitly configured in the ACI manifest as a "context pass-through" — and even then, the pass-through is: (i) declared in advance, (ii) signed into policy, (iii) logged as a context-transfer event in the evidence chain. Unplanned context sharing is structurally impossible because the gateway mediates every call and enforces per-action isolation. |
| **Evidence Grade** | E2 — hash-chained action sequence showing context boundaries at each server transition |
| **Verification** | Verifier checks: no evidence receipt references context from a different server unless a context-transfer event exists in the chain |

---

### F8: Toxic Flows (Multi-Step Attacks)

| | |
|---|---|
| **NSA Finding** | Multi-step attacks where no single call is malicious but the sequence produces a harmful outcome. Toxic flows are invisible to conventional per-call monitoring because each individual call appears benign. |
| **WitnessOS Feature** | **Evidence Chain Analysis (E3+) + Policy Sequence Enforcement** |
| **How It Satisfies** | WitnessOS's hash-chained evidence receipts (E2+) make the full action sequence visible and verifiable. The gateway enforces **sequence policies** — not just per-action policies. A sequence policy can specify: (a) ordering constraints (Step B must follow Step A), (b) context constraints (if action reads data from Server A, it cannot write to Server B), (c) cumulative-risk thresholds (if 3 "read" actions in 10 minutes, trigger human approval on 4th). Because every action produces a cryptographically linked receipt, toxic flows are detectable at the pattern level — not just the call level. The gateways Policy Engine evaluates the full sequence chain against sequence policies on every new action. |
| **Evidence Grade** | E3 — multi-agent verified receipt enabling cross-agent flow analysis |
| **Verification** | Verifier runs sequence policy against the full evidence chain; any toxic flow pattern triggers a policy violation report |

---

## NSA Recommendations → WitnessOS Feature Map

| NSA Recommendation | WitnessOS Feature | Implementation Mechanism |
|---|---|---|
| **Apply Zero Trust (SP 800-207)** | Credential-brokered enforcement | No agent is trusted by default. Every action requires: identity verification (mTLS) → policy evaluation (OPA/Rego) → approval binding (SHA-256) → evidence generation (E0-E4). The agent has zero implicit trust and zero stored credentials. |
| **Strict Input Validation & Schema Enforcement** | AJSON + ACI manifest validation | Every tool call payload is validated against the ACI schema at the gateway. Malformed, oversized, or unexpected-field payloads are rejected before reaching any execution boundary. |
| **Per-Action Approval Workflows** | Exact-Approval Binding | Every action requires a human-approved SHA-256 hash of its exact content. No batch approvals. No wildcard approvals. No template approvals. Every action is individually bound to its precise content. |
| **RBAC at MCP Integration Layer** | Identity Registry + Policy Engine | Agents are cryptographically identified (mTLS), mapped to roles (ACI manifest), and authorized per-action (OPA/Rego policy). The gateway enforces RBAC at the MCP boundary — not at the application layer. |
| **Monitor for Toxic Flows** | Evidence Chain Analysis (E3-E4) | The hash-chained evidence trail enables cross-call pattern analysis. Sequence policies detect multi-step attacks no single call reveals. Verifiable by third parties without gateway access. |

---

## Compliance Evidence Map

| NSA Requirement | WitnessOS Evidence Grade | CLI Command |
|---|---|---|
| Agent identity verification | E2 | `witnessos compliance --standard nsa-mcp --report identity` |
| Credential lifecycle management | E3 | `witnessos compliance --standard nsa-mcp --report credentials` |
| Per-action approval audit | E1 | `witnessos compliance --standard nsa-mcp --report approvals` |
| Input validation enforcement | E0 | `witnessos compliance --standard nsa-mcp --report validation` |
| Toxic flow detection | E3 | `witnessos compliance --standard nsa-mcp --report toxic-flows` |
| Context boundary enforcement | E2 | `witnessos compliance --standard nsa-mcp --report context` |
| Policy version control | E1 | `witnessos compliance --standard nsa-mcp --report policy-audit` |
| Full compliance summary | E4 | `witnessos compliance --standard nsa-mcp --output pdf` |

---

## Market Positioning (Derived)

The NSA guidance validates the WitnessOS architecture in a way no marketing copy can match. Recommended positioning:

> **"The NSA says MCP needs credential governance, per-action approval, and audit trails. WitnessOS delivers all three — structurally, not observationally."**

Or for regulated buyers:

> **"When the U.S. intelligence community publishes guidance on AI agent security, your governance platform should be the one they're describing. WitnessOS is."**
