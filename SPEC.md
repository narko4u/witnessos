# WitnessOS - Frozen Specification v1.0

> **Status note (2026-09-03):** Evidence grades are no longer capped at E3 - E4 strict-mode issuance is enabled (E3 remains the default in non-strict configurations). Normative E1-E4 definitions below are unchanged from the v1.0 freeze. See [ALPHA_STATUS.md](ALPHA_STATUS.md) for current constraints.

**Status:** FROZEN - Build Reference  
**Date:** 2026-06-26  
**Owner:** Empire Labs Pty Ltd  
**Author:** Empire Labs Pty Ltd

---

## 0. Product Definition

WitnessOS is the **credential-brokered enforcement and evidence layer for consequential agent actions.**

It is not observability. It is not compliance theater. It is not a dashboard. It is not "AI logs."

WitnessOS enforces authorised high-risk agent actions and produces cryptographically verifiable receipts showing:
- Who authorised the action
- What policy applied
- What was executed
- What the destination confirmed
- The evidence grade behind that claim

**Core claim:** Designed to support audits, incident investigations, and compliance evidence.

**Category:** Enforced, verifiable proof of consequential AI actions.

**Launch wedge:** The enforcement and receipt gateway for MCP and API write actions - starting with Gmail send.

---

## 1. Architecture

### 1.1 Gateway Mode (The Product)

Gateway Mode is enforcement + evidence. It is structurally unavoidable for protected actions.

```
Agent
  │
  │ mTLS + signed action request
  ▼
WitnessOS Gateway
  │
  ├──► Policy Engine (evaluates against policy bundle)
  │      ├── Connector registry determines risk_class
  │      ├── Policy evaluated → decision (allow/deny/approval_required)
  │      └── If approval required → Approval UI
  │
  ├──► Credential Broker (holds destination OAuth credentials)
  │      └── Agent NEVER receives destination credential
  │
  ├──► Issues Action Permit (bound to canonical action hash)
  │
  ├──► Routes action to Destination
  │      └── Gateway is the only principal able to execute
  │
  ├──► Records lifecycle events (append-only)
  │
  ├──► Checkpoints to Merkle tree (hourly)
  │
  └──► External anchor (RFC 3161 TSA)
```

**Rule:** The agent never receives destination credentials. The gateway holds the only OAuth grant - narrowest practical scope (e.g., `gmail.send`, not full mailbox).

### 1.2 Sidecar Mode (Telemetry Only)

Async observation. E1 evidence at best. Can miss events, crash, be disabled, or be bypassed. Useful for debugging and investigation. Not evidence. Not marketed as proof.

### 1.3 Native Enforcement Mode (Internal APIs / MCP Servers)

For WitnessOS-controlled MCP servers and internal APIs:

```
Agent → Destination (with Action Permit)
Destination → WitnessOS Verifier (validates permit before executing)
```

Requires destination to install WitnessOS verifier SDK. Valid for controlled MCP servers using OAuth authorization model.

---

## 2. Evidence Grades

Every receipt carries exactly one grade. No ambiguity.

| Grade | Name | Meaning | Required |
|-------|------|---------|----------|
| E0 | Declared | Agent claims it acted. No independent observation. | Trust |
| E1 | Observed | SDK/sidecar saw the action. Gaps possible. | Agent instrumentation |
| E2 | Enforced | WitnessOS authorised and routed through gateway. | Gateway + policy evaluation |
| E3 | Corroborated | Destination returned verifiable confirmation. | Provider receipt or state probe |
| E4 | Anchored | Receipt chain externally timestamped and checkpointed. | TSA + Merkle root published |

**Evidence grade measures strength of evidence, not business success.** An E4 receipt can legitimately show `provider_failed`, `unknown`, or `effect_confirmed`.

**Dashboard language:** Never "immutable." Always: "E4 - Gateway-enforced, provider-confirmed, externally anchored."

---

## 3. Receipt Lifecycle - Event-Sourced

### 3.1 Principle

Do not mutate a receipt from `requested` to `confirmed`. Create an **immutable Action Case** containing signed lifecycle events.

### 3.2 Lifecycle Events

```
action.requested     - Agent requests action; canonical request hash recorded
policy.evaluated     - Policy bundle evaluated; decision recorded
approval.granted     - Human approval granted (if required); scope + expiry recorded
dispatch.started     - Gateway dispatches action to destination
provider.acknowledged - Destination confirms receipt of action
provider.outcome_unknown - Gateway lost response; destination status ambiguous
reconciliation_pending  - Awaiting outcome resolution
provider.confirmed   - Destination confirms success
provider.failed      - Destination confirms failure
outcome.reconciled   - Outcome resolved (possibly from idempotent retry or manual check)
anchor.completed     - Receipt chain externally anchored (E4)
```

### 3.3 Derived Receipt View

`receipt_status` is a calculated view from immutable events - not a mutable source record.

```
StatusDerivation:
  requested         → action.requested exists
  policy_evaluated  → policy.evaluated exists
  approval_pending  → policy.evaluated + approval required + no approval.granted
  approved          → approval.granted exists + not expired
  dispatched        → dispatch.started exists
  acknowledged      → provider.acknowledged exists
  unknown           → dispatch.started + no provider response + timeout
  confirmed         → provider.confirmed exists
  failed            → provider.failed exists
  reconciled        → outcome.reconciled exists
  anchored          → anchor.completed exists
```

### 3.4 Unknown as First-Class Outcome

Never infer failure because the gateway didn't receive a response.

```
dispatch.started
provider_outcome_unknown  ← explicitly recorded
reconciliation_pending
```

**Gmail:** Ambiguous network failure → no automatic re-send. Manual or provider-state reconciliation required. Duplicate outbound emails are worse than a visible "unknown" state.

**Stripe:** Retain idempotency key. Reconcile safely using Stripe's idempotency support for POST operations. Same key → no duplicate side effects.

---

## 4. Receipt Format - Canonical JSON (RFC 8785)

All JSON is canonicalised per RFC 8785 before hashing or signing. Same data always produces same hash.

### 4.1 Full Receipt Schema

```json
{
  "receipt_version": "1.0",
  "receipt_id": "wos_20260626_a1b2c3d4",
  "evidence_grade": "E3",
  "receipt_status": "confirmed",
  "case_id": "wos_case_abc123",

  "actor": {
    "agent_id": "spiffe://example.org/prod/sales-agent",
    "workload_identity": "x509:fingerprint:sha256:...",
    "agent_build_hash": "sha256:...",
    "framework": "example-agent-framework",
    "framework_version": "1.0",
    "model": "example-model-1",
    "runtime_env_hash": "sha256:...",
    "signing_key_id": "key_2026_q3"
  },

  "delegation": {
    "human_principal": "admin@example.com",
    "approval_id": "wos_approval_abc123",
    "approval_scope_hash": "sha256:...",
    "approval_expires_at": "2026-06-26T15:00:00Z"
  },

  "action": {
    "canonical_request_hash": "sha256:...",
    "target_system": "gmail",
    "target_resource": "send_message",
    "idempotency_key": "wos_idem_xyz789",
    "risk_class": "external_email",
    "permit_jti": "wos_permit_def456"
  },

  "policy": {
    "decision": "allow",
    "policy_bundle_hash": "sha256:...",
    "policy_engine_version": "1.0.0",
    "rule_id": "ext_email_requires_approval"
  },

  "outcome": {
    "stage": "provider_confirmed",
    "confirmation_method": "api_response",
    "independently_verifiable": false,
    "provider_operation_id": "gmail_msg_abc123",
    "provider_receipt_hash": "sha256:...",
    "state_probe_hash": "sha256:...",
    "raw_evidence_blob_hash": "sha256:..."
  },

  "timing": {
    "observed_at": "2026-06-26T14:32:17.000Z",
    "anchored_at": "2026-06-26T15:00:03.000Z",
    "anchor_status": "anchored"
  },

  "integrity": {
    "previous_receipt_hash": "sha256:...",
    "merkle_checkpoint": "sha256:...",
    "timestamp_token": "rfc3161:base64...",
    "signing_key_id": "key_2026_q3",
    "signature": "ed25519:base64..."
  },

  "privacy": {
    "capture_profile": "restricted-redacted-v1",
    "encrypted_blob_refs": ["s3://witnessos-evidence/enc/abc123"],
    "redacted_fields": ["email_body", "recipient_address"]
  }
}
```

### 4.2 Provider-Evidence Taxonomy

`confirmation_method` values:

| Value | Meaning | Example |
|-------|---------|---------|
| `api_response` | Destination API returned success response. Not independently verifiable without destination trust. | Gmail send 200 OK |
| `signed_webhook` | Destination sent cryptographically signed webhook confirming outcome. | Stripe signed webhook |
| `provider_api_reconciliation` | Outcome confirmed by querying provider API after action. | Polling Stripe for charge status |
| `public_ledger_reference` | Action recorded on public blockchain or similar. Independently verifiable. | ETH tx hash |
| `manual_attestation` | Human confirmed outcome. Weakest form. | Operator checked and attested |

`independently_verifiable`: Boolean. Can a third party verify this outcome without trusting WitnessOS or the destination provider?

### 4.3 Gmail v0 Outcome Language

"Authorised, gateway-executed, Gmail API accepted."  
Not "delivered." Not "opened." Not "read."

---

## 5. Action Permits (Capability Tokens)

### 5.1 Design

Action Permits are NOT generic JWTs. They are single-use, tightly-bound capability tokens.

### 5.2 Required Fields

```
jti            - unique token identifier (UUIDv7)
sub            - agent identity (spiffe://...)
aud            - exact destination endpoint
tenant_id      - tenant scope
action_hash    - canonical SHA-256 of the authorised action
target_method  - HTTP method or RPC method
target_path    - exact API path
risk_class     - from connector registry
iat            - issued-at timestamp
nbf            - not-before timestamp
exp            - expiry (60-second TTL from iat)
cnf            - DPoP key confirmation (JWK thumbprint of agent's auth key)
```

### 5.3 Replay Resistance

- `jti` tracked in one-time redemption ledger; any reuse denied
- DPoP proof required: agent signs (method, URL, permit hash) with its auth key
- mTLS binding: agent's TLS client certificate must match the key in `cnf`
- Deny any reused `jti` - even within TTL window
- `action_hash` binding prevents permit reuse for a different action

### 5.4 Strict Mode (Enterprise)

For payments, infrastructure changes, or large refunds:

No `dispatch.started` until:
1. Approval event durably committed to customer-controlled evidence store
2. Pre-dispatch action hash durably committed to customer-controlled evidence store
3. `anchor_status` reflects these commitments before dispatch

This prevents: approve → dispatch → crash before evidence written → no proof approval happened.

---

## 6. Key Architecture

No key performs two jobs.

| Key | Purpose | Rotation | Storage |
|-----|---------|----------|---------|
| Agent Auth Key | mTLS + DPoP binding; proves agent identity | Quarterly | Agent runtime |
| Receipt Ledger Signing Key | Signs receipts and Merkle checkpoints | Quarterly | WitnessOS Gateway (HSM-backed) |
| Policy Bundle Signing Key | Signs policy bundles for integrity verification | Per policy update | Policy management service |
| Approval Signing Key | Signs human approval events | Per approval session | Approval UI / session-bound |
| Destination OAuth Credential | Authorises gateway to act on destination | Per OAuth grant | Credential Broker (encrypted) |
| Customer KMS Key (Enterprise) | Encrypts evidence blobs; customer-controlled | Customer-managed | Customer KMS / HSM |

### 6.1 Key Rotation

- All signing keys have declared lifespans
- Key rotation events are themselves receipts
- Revocation receipts published when keys retired
- Verifier must validate key was active at receipt timestamp

---

## 7. External Anchoring - Trust Architecture

### 7.1 Anchor Stack

1. Per-receipt hash chaining (`previous_receipt_hash`)
2. Hourly Merkle root computation
3. RFC 3161 timestamp token from trusted TSA
4. Merkle root + timestamp → customer-controlled WORM storage (S3 Object Lock, GCS retention)
5. Optional: public transparency log (hashes only - never content)
6. Enterprise: customer-managed KMS/HSM keys for signing
7. Key rotation and revocation receipts

### 7.2 Verification Chain

A verifier independently checks:
1. Ed25519 signature on receipt ✓
2. Receipt position in Merkle tree ✓
3. Merkle root timestamped by TSA ✓
4. TSA timestamp ≥ receipt `observed_at` (allows clock skew window) ✓
5. No gaps in hash chain ✓
6. Signing key was active at receipt timestamp ✓

### 7.3 E4 Timing Semantics

```
"timing": {
  "observed_at": "2026-06-26T14:32:17Z",     // WitnessOS observation
  "anchored_at": "2026-06-26T15:00:03Z",      // TSA-provided latest-existence boundary
  "anchor_status": "anchored"                  // anchored | anchor_pending
}
```

- `observed_at` = WitnessOS system observation time
- `anchored_at` = externally proven latest-existence boundary (from TSA)
- Until hourly checkpoint completes: `anchor_pending` → receipt is E3, not E4
- RFC 3161 proves hash existed no later than TSA timestamp
- It does NOT independently prove the action occurred at `observed_at`

### 7.4 Strict Mode (E4+)

No action dispatch until approval + pre-dispatch action hash durably committed to customer-controlled evidence store. This is the version enterprises will pay for.

---

## 8. Privacy Model

### 8.1 Capture Profiles

| Profile | Command Type | Arguments | Output | PII/Sensitive |
|---------|-------------|-----------|--------|---------------|
| `full` | Plaintext | Plaintext | Plaintext | Unredacted |
| `restricted` | Plaintext | HMAC'd | Hashed | Redacted |
| `restricted-redacted-v1` | Type only | HMAC'd | Hashed | Stripped |
| `minimal` | Type only | Hashed | None | Stripped |

**Default:** `restricted-redacted-v1`.

### 8.2 HMAC for Sensitive Values

Do NOT plain-SHA-256 email addresses, account IDs, or small payload values in restricted modes. Attackers can brute-force low-entropy hashes.

- Use tenant-scoped keyed HMAC (HMAC-SHA-256) for privacy fields
- Retain canonical SHA-256 hashes for integrity commitments (separate field)
- HMAC key is tenant-specific, rotated on tenant offboarding

### 8.3 Encrypted Evidence Blobs

- Full evidence blobs encrypted with customer-controlled KMS key
- WitnessOS never holds plaintext for restricted profiles
- `encrypted_blob_refs` points to customer-decryptable storage locations

### 8.4 Data Ownership

> "WitnessOS creates customer-owned evidence. Aggregated benchmark data is strictly opt-in, privacy-preserving, and never required for product operation."

No "data moat." No training on customer actions. No hoarding sensitive records.

---

## 9. Connector Registry & Risk Classification

### 9.1 Principle

Risk classification is connector-owned. Never trust an agent-provided `risk_level`.

### 9.2 Registry Schema

```json
{
  "connector_id": "gmail_send_v1",
  "target_system": "gmail",
  "target_resource": "send_message",
  "risk_class": "external_email",
  "risk_level": "high",
  "default_policy": "approval_required",
  "credential_scope": "https://www.googleapis.com/auth/gmail.send",
  "idempotency_support": false,
  "reconciliation_method": "manual"
}
```

### 9.3 Write Classes (MVP Launch Order)

| # | Class | Risk | Start |
|---|-------|------|-------|
| 1 | External communication | High | Gmail send |
| 2 | Modify business records | High/Medium | Stripe refund or HubSpot update |
| 3 | Spend or commit value | Critical | Stripe payment |

### 9.4 Native Enforcement Eligible

Only internal APIs and MCP servers that install WitnessOS verifier SDK use Native Enforcement Mode. Third-party SaaS (Gmail, Stripe, HubSpot) always uses Gateway + Credential Broker Mode.

---

## 10. MVP v0 - What Ships

### 10.1 Definition

**One high-risk action, one framework, one verifier.**

### 10.2 Scope

1. **Gateway** - FastAPI, mTLS, credential broker holding Gmail OAuth token
2. **Connector** - Gmail send (`gmail.send` scope only, not full mailbox)
3. **Policy Engine** - One policy: human approval required for `external_email` risk class
4. **Approval UI** - Exact action diff, expiry, scope, max value, one-click approve/deny
5. **Event-Sourced Ledger** - Immutable lifecycle events, append-only
6. **Receipt Chain** - Ed25519 signing, hash chaining, canonical JSON (RFC 8785)
7. **CLI Verifier** - `witnessos verify <receipt_id>` - independent verification
8. **External Anchoring** - Hourly Merkle roots + RFC 3161 TSA timestamps
9. **Action Permits** - Single-use, DPoP-bound, jti redemption ledger
10. **Privacy** - `restricted-redacted-v1` capture profile, HMAC for sensitive fields
11. **Red-Team Suite** - 10 tests (see §11), all must pass before publish
12. **Failure Mode** - Fail closed for high-risk actions

### 10.3 What v0 Does NOT Build

- Dashboard (CLI only) - `witnessos status`, `witnessos inspect`, `witnessos verify`
- Multi-tenant cloud vault (local SQLite + WORM anchor only)
- Sidecar mode (gateway only)
- Terminal governance
- Integrations beyond Gmail send
- Enterprise SSO, RBAC, KMS
- Stripe connector (second after v0 launch)
- Public transparency log

---

## 11. Red-Team Suite

All 10 tests must pass before publishing the launch blog.

| # | Attack | Test | Expected Result |
|---|--------|------|-----------------|
| 1 | Direct API bypass | Agent attempts Gmail send without Action Permit | Gateway rejects; no action executes |
| 2 | Expired approval replay | Replay previously valid approval | Permit redemption ledger detects; denies |
| 3 | Modified SQLite database | Manually edit a receipt row in local store | `witnessos verify` detects hash chain break |
| 4 | Deleted receipts | Delete receipt from local store | `witnessos verify` flags gap in chain |
| 5 | Clock rollback | Set system clock back; create receipt | TSA timestamp reveals inconsistency |
| 6 | Stolen agent credential | Sign with different agent's auth key | DPoP binding or mTLS mismatch; gateway rejects |
| 7 | Policy changed after approval | Approve under policy v1, execute under v2 | `policy_bundle_hash` mismatch; verifier detects |
| 8 | Gateway outage | Kill gateway during action execution | Fail closed - no action executes; no unlogged actions |
| 9 | Destination succeeds but response lost | Gmail sends; WitnessOS never receives confirmation | Receipt shows `provider_outcome_unknown`; reconciliation pending |
| 10 | Destination fails after dispatch | Receipt claims success; Gmail actually returned error | Reconciliation detects `provider_failed`; receipt updated |

---

## 12. Pricing

| Tier | Price | Includes |
|------|-------|----------|
| **OSS** | Free | Gateway, local vault, verifier, basic policies, MIT license |
| **Cloud Team** | $500/mo | Hosted verification, alerts, 90-day retention, 50K receipts/mo |
| **Enterprise** | $2,500/mo | SSO, customer KMS, 7-year retention, private deployment, audit packs, 500K receipts/mo |
| **Regulated** | Custom | Legal hold, data residency, dedicated tenant, custom connectors, BAA, SLA |

**Explicitly removed:**
- "SOC 2 report" as tier feature → Empire Labs becomes SOC 2 compliant as a company; customers don't buy SOC 2 reports as a feature
- "Insurer-ready" → replaced with "structured evidence export" until actual insurer partnerships exist
- Usage-aware pricing: receipt volume, storage, retention, anchoring, and connectors drive cost

---

## 13. Strategic Positioning

### 13.1 Core Category

> **Enforced, verifiable proof of consequential AI actions.**

This survives OpenAI tracing, Datadog, LangSmith, IAM vendors, and generic audit logging because those products can show activity - WitnessOS must prove authority, enforcement, execution, outcome, and integrity.

### 13.2 Moat

**Not:** "We invented JSON receipts."

**Is:** "Auditors, insurers, customers, and destination systems trust WitnessOS evidence grades and verification tooling."

Strategy:
- Publish this receipt specification openly (RFC-style)
- Compatible with emerging audit-trail work (IETF draft where sensible)
- Own `wos.*` extension namespace
- Ship conformance tests and test vectors
- Open-source the verifier
- Commercial moat: managed verification network, policy packs, provider connectors, audit workflows, evidence export

### 13.3 The Big Fish

| # | Acquirer | Rationale | Range |
|---|----------|-----------|-------|
| 1 | Microsoft | Copilot agents everywhere. Needs independent trust layer. | $1B-$3B |
| 2 | Datadog | Next-gen observability = agent evidence. | $500M-$1.5B |
| 3 | Palo Alto Networks | Agent actions = new attack surface. | $500M-$1B |
| 4 | Google | Gemini + Workspace agents. Slow but strategic. | $800M-$2B |
| 5 | Vanta/Drata | Compliance automation for AI era. | $300M-$800M |
| 6 | Palantir | Defense/intel needs non-negotiable accountability. | $500M-$1.5B |
| 7 | ServiceNow | Workflow automation audit trail. | $400M-$1B |

### 13.4 Launch Story

> "An agent requests to send an external email. WitnessOS evaluates policy, requires approval, executes using gateway-held credentials, records every immutable lifecycle event, and produces a receipt any third party can verify."

---

## 14. Build Order

### Phase A - Foundation (Week 1)
1. Receipt spec frozen (this document)
2. Canonical JSON library (RFC 8785 serialisation)
3. Event store (append-only, SQLite-based index + Merkle tree engine)
4. Key generation and management (Ed25519 keypairs, key registry)
5. CLI verifier: `witnessos verify <receipt_id>`

### Phase B - Gateway Core (Week 1-2)
6. FastAPI gateway skeleton with mTLS
7. Credential Broker (Gmail OAuth, `gmail.send` scope)
8. Action Permit issuance and redemption ledger
9. Policy Engine (one rule: `external_email` → approval required)
10. Approval UI (simple web UI: diff, scope, expiry, approve/deny)
11. Gmail connector (send endpoint, response capture)

### Phase C - Evidence Layer (Week 2)
12. Lifecycle event recording (all 11 event types)
13. Receipt generation from event stream
14. Hash chaining and Merkle checkpointing
15. RFC 3161 external timestamping
16. WORM anchor (customer S3/GCS, optional)

### Phase D - Red-Team & Ship (Week 2-3)
17. Red-team suite (all 10 tests)
18. First-party dogfood integration
19. Launch blog and GitHub repo
20. Receipt spec RFC published

---

## 15. Non-Negotiables (Locked)

1. **Credential Broker pattern** - agents never receive destination OAuth tokens
2. **Event-sourced lifecycle** - immutable events, not mutable receipts
3. **Evidence grades** - E0 through E4 on every receipt
4. **Action Permits** - jti, DPoP, one-time redemption, action_hash binding
5. **Split keys** - no key performs two jobs
6. **Privacy by default** - `restricted-redacted-v1`, HMAC for sensitive values
7. **Connector-owned risk classification** - never trust agent-provided `risk_level`
8. **Unknown as first-class outcome** - never infer failure from silence
9. **Fail closed** - gateway outage = no action, not unlogged action
10. **Red-team suite** - all 10 tests pass before blog publish
11. **RFC 8785 canonical JSON** - before any hashing or signing
12. **External anchoring** - RFC 3161 TSA + Merkle checkpoints for E4

---

**Spec frozen. Build begins from this document.**
