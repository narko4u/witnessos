# EU AI Act — Article 9 (Risk Management System)
## E0-E4 Evidence Templates

**Regulation:** EU AI Act, Article 9 — Risk Management System for high-risk AI systems
**Enforcement:** August 2, 2026
**Context:** Autonomous AI agents are not explicitly mentioned in the Act, but Article 9's requirement for "continuous iterative risk management throughout the entire lifecycle" applies to any high-risk system. WitnessOS evidence receipts satisfy Article 9's documentation and verification requirements.

---

## E0 — Raw Event Log (Internal Audit Trail)

**Purpose:** Raw, unprocessed log of all agent actions. Serves as the foundation for higher evidence grades.

### Template

```json
[
  {
    "evidence_grade": "E0",
    "gateway_id": "wgos-gw-01",
    "action_id": "act_a1b2c3d4",
    "timestamp": "2026-07-28T14:30:00.000Z",
    "agent_id": "agent-porgie-01",
    "action_type": "tool_call",
    "tool": "github_api",
    "payload_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "policy_check": "PASS",
    "schema_validation": "PASS",
    "duration_ms": 234
  }
]
```

### Article 9 Mapping

| Article 9 Requirement | E0 Coverage |
|---|---|
| Art 9(2)(a) — Identification of known and foreseeable risks | Raw log provides the data source for risk identification patterns |
| Art 9(2)(b) — Estimation and evaluation of risks | Action frequency, failure rates, and policy violations can be computed from E0 aggregates |
| Art 9(2)(c) — Evaluation of residual risks | Post-mitigation action patterns compared to pre-mitigation baselines |
| Art 9(3) — Testing procedures | Test action logs show system behavior under controlled conditions |
| Art 9(4) — Continuous iterative risk management | Streaming E0 log provides real-time risk posture data |

### CLI Generation

```bash
witnessos compliance --standard eu-ai-act --article 9 --evidence e0 --from 2026-07-01 --to 2026-07-28
```

---

## E1 — Signed Event Record (Evidence of Human Oversight — Art 14)

**Purpose:** Each action record is signed by the gateway, providing tamper evidence and binding the record to a specific gateway instance.

### Template

```json
{
  "evidence_grade": "E1",
  "gateway_id": "wgos-gw-01",
  "gateway_key_fingerprint": "ed25519:abc123def456",
  "signature": "MEUCIQDOkC...8qNc7M=",
  "signing_timestamp": "2026-07-28T14:30:00.000Z",
  "chain_reference": "chain-hash:e1-a1b2c3d4",
  "action": {
    "action_id": "act_a1b2c3d4",
    "agent_id": "agent-porgie-01",
    "type": "tool_call",
    "tool": "github_api",
    "endpoint": "/repos/narko4u/witnessos/issues",
    "parameters": {
      "title": "Security audit finding",
      "labels": ["security", "automated"]
    },
    "parameters_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
  },
  "approval": {
    "approver_id": "human-eddie",
    "approval_hash": "sha256:approved-content-hash",
    "approval_timestamp": "2026-07-28T14:29:55.000Z",
    "approval_method": "exact_hash_binding"
  },
  "policy_evaluation": {
    "policy_bundle_id": "pb-2026-07-v3",
    "policy_decision": "ALLOW",
    "matched_rules": ["rbac-agent-developer-role", "github-write-allowed"],
    "evaluation_duration_ms": 12
  }
}
```

### Article 9 Mapping

| Article 9 Requirement | E1 Coverage |
|---|---|
| Art 9(2)(c) — Residual risk evaluation | Signed records show actual vs. expected risk mitigations took effect |
| Art 9(3) — Testing procedures | Signed test records provide non-repudiable evidence of testing |
| Art 9(5) — Risk management documentation | Signed log entries satisfy Art 9(5)'s documentation maintenance requirement |

### CLI Generation

```bash
witnessos compliance --standard eu-ai-act --article 9 --evidence e1 --action-id act_a1b2c3d4
```

---

## E2 — Hash-Chained Action Sequence (Risk Management Evidence — Art 9)

**Purpose:** Actions are linked into a hash chain where each receipt references the previous one. This provides tamper-evident ordering of all actions and enables full sequence reconstruction.

### Template

```json
{
  "evidence_grade": "E2",
  "chain_id": "chain-agent-porgie-2026-07-28",
  "chain_length": 47,
  "chain_anchor": "chain-hash:e1-a1b2c3d4",
  "this_link": "chain-hash:e2-7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
  "prev_link_hash": "chain-hash:e2-8a9b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f",
  "merkle_proof": {
    "tree_root": "merkle:2026-07-28T14:00-batch",
    "tree_height": 6,
    "leaf_index": 42,
    "sibling_hashes": [
      "sha256:hash-1",
      "sha256:hash-2",
      "sha256:hash-3",
      "sha256:hash-4",
      "sha256:hash-5",
      "sha256:hash-6"
    ]
  },
  "action": {
    "action_id": "act_b2c3d4e5",
    "agent_id": "agent-porgie-01",
    "type": "tool_call",
    "tool": "slack_api",
    "parameters_hash": "sha256:action-content-hash",
    "sequence_position": 47
  },
  "context_boundary": {
    "server_transition": false,
    "active_contexts": ["github-monitoring", "slack-notifications"],
    "context_transfer_permitted": true
  },
  "toxic_flow_check": {
    "sequence_pattern": "read-read-write",
    "cumulative_risk_score": 0.3,
    "threshold_breached": false,
    "pattern_matched": false
  },
  "timestamp": "2026-07-28T14:30:05.000Z",
  "signature": "ed25519:chain-signature"
}
```

### Article 9 Mapping

| Article 9 Requirement | E2 Coverage |
|---|---|
| Art 9(2)(a) — Risk identification | Hash chain enables reconstruction of agent behavior patterns for risk identification |
| Art 9(2)(b) — Risk estimation | Sequence analysis provides frequency, ordering, and dependency data for risk quantification |
| Art 9(4) — Continuous iterative risk management | Each new chain link provides real-time risk posture update |
| Art 9(6) — Risk management system update | Chain versioning shows when risk management measures were updated and their effect on subsequent actions |
| Art 9(7) — Post-market monitoring | Full chain reconstruction enables post-hoc risk analysis after deployment |

### CLI Generation

```bash
witnessos compliance --standard eu-ai-act --article 9 --evidence e2 --chain chain-agent-porgie-2026-07-28
```

---

## E3 — Multi-Agent Verified Receipt (System-Level Conformity — Art 43)

**Purpose:** Evidence receipts are cross-verified by multiple independent gateways or verification nodes. Provides system-level assurance that no single gateway can forge, alter, or suppress evidence.

### Template

```json
{
  "evidence_grade": "E3",
  "receipt_id": "receipt-e3-f7a8b9c0",
  "verification_round": 3,
  "participating_verifiers": [
    {
      "verifier_id": "verifier-alpha",
      "verification_result": "CONFIRMED",
      "verifier_signature": "ed25519:verifier-alpha-sig"
    },
    {
      "verifier_id": "verifier-beta",
      "verification_result": "CONFIRMED",
      "verifier_signature": "ed25519:verifier-beta-sig"
    },
    {
      "verifier_id": "verifier-gamma",
      "verification_result": "CONFIRMED",
      "verifier_signature": "ed25519:verifier-gamma-sig"
    }
  ],
  "threshold_met": true,
  "threshold_required": 2,
  "chain_verified": {
    "chain_id": "chain-agent-porgie-2026-07-28",
    "chain_integrity": "INTACT",
    "chain_length": 47,
    "first_link_timestamp": "2026-07-28T08:00:00.000Z",
    "last_link_timestamp": "2026-07-28T14:30:05.000Z"
  },
  "policy_bundle_verified": {
    "bundle_id": "pb-2026-07-v3",
    "bundle_integrity": "INTACT",
    "bundle_signing_key": "ed25519:policy-signing-key",
    "bundle_valid_from": "2026-07-01T00:00:00Z",
    "bundle_valid_to": "2026-07-31T23:59:59Z"
  },
  "consensus": {
    "status": "PASS",
    "violations_found": 0,
    "warnings": []
  }
}
```

### Article 9 Mapping

| Article 9 Requirement | E3 Coverage |
|---|---|
| Art 9(6) — Effectiveness of risk management measures | Cross-verified evidence proves measures were enforced correctly |
| Art 9(7) — Post-market monitoring | Independent verification of all post-deployment actions |
| Art 9(8) — Significant incident reporting | Cross-verified evidence provides authoritative incident timeline |

### Article 43 Mapping

| Article 43 Requirement | E3 Coverage |
|---|---|
| Art 43(1) — Conformity assessment procedure | Multi-verified evidence chain serves as the audit record for conformity assessment |
| Art 43(2) — Notified body involvement | Third-party verifiers can confirm evidence integrity without trust |
| Art 43(4) — Technical documentation | Cross-verified receipts form the evidentiary foundation for technical documentation |

### CLI Generation

```bash
witnessos compliance --standard eu-ai-act --article 43 --evidence e3 --chain chain-agent-porgie-2026-07-28
```

---

## E4 — Cross-Certified Evidence Chain (Full Conformity Assessment — Art 43)

**Purpose:** The highest evidence grade. Multiple independent verification nodes cross-certify the entire evidence chain. Merkle-checkpointed, RFC 3161 timestamped, Ed25519 signed. Suitable for regulatory submission, dispute resolution, and insurance underwriting.

### Template

```json
{
  "evidence_grade": "E4",
  "certificate_id": "e4-cert-2026-07-28-porgie",
  "certification_authority": "WitnessOS Certification Authority",
  "certificate_chain": [
    "ca-root-cert.pem",
    "ca-intermediate-cert.pem",
    "gateway-01-cert.pem"
  ],
  "merkle_tree": {
    "tree_root": "merkle:2026-07-28-daily-batch",
    "tree_size": 2847,
    "tree_height": 12,
    "last_updated": "2026-07-28T23:59:59.000Z"
  },
  "rfc3161_timestamps": [
    {
      "timestamp_authority": "freetsa.org",
      "timestamp": "2026-07-28T23:59:59.000Z",
      "timestamp_token": "MIIGVD...token-data"
    }
  ],
  "aggregate_summary": {
    "total_actions": 2847,
    "total_agents": 2,
    "total_gateways": 1,
    "time_period": "2026-07-28T00:00:00Z to 2026-07-28T23:59:59Z",
    "policy_violations": 0,
    "approval_rate": 1.0,
    "schema_validation_failures": 3,
    "sequence_violations": 0
  },
  "compliance_assertions": {
    "eu_ai_act_article_9": "PASS",
    "eu_ai_act_article_14": "PASS",
    "eu_ai_act_article_43": "PASS",
    "nsa_mcp_guidance": "PASS",
    "iso_42001_aligned": "PARTIAL"
  },
  "auditor_notes": "Full compliance evidence chain verifiable without trust. All 2847 actions have hash-chained, merkle-checkpointed, timestamped evidence receipts. 3 schema validation failures occurred due to malformed input from external trigger — all were correctly rejected by gateway policy. No unauthorized actions, no credential leaks, no policy violations.",
  "signature": "ed25519:e4-certification-signature"
}
```

### Article 43 Mapping

| Article 43 Requirement | E4 Coverage |
|---|---|
| Art 43(1) — Conformity assessment procedure | Complete evidence chain meets the "appropriate conformity assessment procedure" requirement |
| Art 43(2) — Notified body engagement | E4 certificate can be submitted directly to Notified Body without additional trust assumptions |
| Art 43(3) — Ongoing compliance | Daily E4 certificates demonstrate continuous compliance |
| Art 43(4) — Technical documentation annex | E4 certificate serves as the foundational annex to technical documentation |
| Art 43(5) — CE marking eligibility | Achieving E4 is a prerequisite for CE marking under the Act |

### CLI Generation

```bash
witnessos compliance --standard eu-ai-act --evidence e4 --date 2026-07-28 --output pdf
witnessos compliance --standard eu-ai-act --evidence e4 --date 2026-07-28 --output json
```

---

## Quick Reference: Evidence Grade → Article Coverage

| Grade | Verification | Trust Model | Art 9 | Art 14 | Art 43 | Use Case |
|---|---|---|---|---|---|---|
| **E0** | None (raw log) | Gateway only | ✅ source | ✅ source | ❌ | Internal debugging, SIEM feed |
| **E1** | Gateway-signed | Gateway + key | ✅ direct | ✅ direct | ❌ | Human oversight records, audit trail |
| **E2** | Hash-chained | Chain integrity | ✅ direct | ✅ | ✅ source | Risk management documentation |
| **E3** | Multi-verifier | Consensus | ✅ | ✅ | ✅ direct | Conformity assessment, system audit |
| **E4** | Cross-certified + timestamped | Zero-trust | ✅ | ✅ | ✅ direct | Regulatory submission, insurance |
