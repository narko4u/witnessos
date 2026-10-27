# EU AI Act — Article 14 (Human Oversight)
## E0-E4 Evidence Templates

**Regulation:** EU AI Act, Article 14 — Human Oversight for high-risk AI systems
**Enforcement:** August 2, 2026
**Context:** Article 14 requires that high-risk AI systems are designed with human oversight mechanisms. For autonomous AI agents, this means: (a) humans must be able to oversee agent decisions, (b) humans must be able to intervene or stop the agent, (c) the system must support "stop button" functionality, and (d) oversight must be proportionate to the risk. WitnessOS's exact-approval binding provides the strongest possible human oversight — per-action approval with cryptographic content binding.

---

## E0 — Raw Oversight Log

**Purpose:** Raw log of oversight events — approvals, rejections, interventions, and overrides.

### Template

```json
[
  {
    "evidence_grade": "E0",
    "oversight_event_type": "human_approval",
    "action_id": "act_c3d4e5f6",
    "agent_id": "agent-executor-01",
    "human_id": "human-eddie",
    "approval_content_hash": "sha256:approved-hash",
    "decision": "APPROVED",
    "timestamp": "2026-07-28T14:30:00.000Z",
    "response_time_ms": 2500
  },
  {
    "evidence_grade": "E0",
    "oversight_event_type": "human_intervention",
    "action_id": "act_d4e5f6a7",
    "agent_id": "agent-executor-01",
    "human_id": "human-eddie",
    "intervention_type": "REJECT_AND_BLOCK",
    "reason": "Unusual file write path detected",
    "timestamp": "2026-07-28T14:35:00.000Z",
    "response_time_ms": 1800
  }
]
```

### Article 14 Mapping

| Article 14 Requirement | E0 Coverage |
|---|---|
| Art 14(1) — Human oversight measures | Raw log provides the oversight audit trail |
| Art 14(3)(a) — Understanding system capabilities | Oversight log shows real human-agent interaction patterns |
| Art 14(3)(c) — Ability to override | Log records all interventions and overrides |
| Art 14(4)(b) — Operational constraints | Human rejections show constraint application |

---

## E1 — Signed Oversight Record

**Purpose:** Each oversight event is gateway-signed, providing non-repudiable proof of human involvement.

### Template

```json
{
  "evidence_grade": "E1",
  "gateway_id": "wgos-gw-01",
  "gateway_signature": "ed25519:gateway-sig",
  "oversight_event_type": "human_approval",
  "action_id": "act_c3d4e5f6",
  "agent_id": "agent-executor-01",
  "human": {
    "human_id": "human-eddie",
    "human_identity_proof": "mTLS-client-cert-eddie-workstation",
    "human_identity_verified_by": "gateway-identity-broker"
  },
  "approval": {
    "approval_content_hash": "sha256:exact-content-hash",
    "approval_method": "EXACT_HASH_BINDING",
    "approval_binding": "human-sees-exact-content-before-approving",
    "approval_window_ms": 2500,
    "approval_timestamp": "2026-07-28T14:30:00.000Z"
  },
  "policy_evaluation": {
    "policy_bundle_id": "pb-2026-07-v3",
    "oversight_required": true,
    "oversight_level": "per_action_approval",
    "risk_tier": "HIGH"
  }
}
```

### Article 14 Mapping

| Article 14 Requirement | E1 Coverage |
|---|---|
| Art 14(2) — Proportionality of oversight | Signed records show the risk tier and corresponding oversight level applied |
| Art 14(3)(a) — Human understanding | Approval window confirms human had time to review |
| Art 14(3)(b) — Autonomy boundaries | Signed policy evaluation shows oversight was required for this action |

---

## E2 — Chain-Bound Oversight Sequence

**Purpose:** Oversight events are linked into the same hash chain as actions, proving that oversight happened in the correct sequence — approval before execution, intervention after detection.

### Template

```json
{
  "evidence_grade": "E2",
  "chain_id": "chain-agent-executor-2026-07-28",
  "chain_link": "chain-hash:e2-oversight-7f83b165",
  "prev_link_hash": "chain-hash:e2-action-8a9b7c6d",
  "next_link_hash": "chain-hash:e2-action-b1c2d3e4",
  "oversight_position": "BETWEEN_ACTION_46_AND_ACTION_47",
  "oversight_type": "human_approval",
  "action_before_oversight": {
    "action_id": "act_b2c3d4e5",
    "action_hash": "sha256:action-46-content",
    "completed": true,
    "evidence_generated": true
  },
  "oversight_event": {
    "human_id": "human-eddie",
    "decision": "APPROVED",
    "content_hash_approved": "sha256:action-47-content",
    "timestamp": "2026-07-28T14:30:00.000Z"
  },
  "action_after_oversight": {
    "action_id": "act_c3d4e5f6",
    "action_hash": "sha256:action-47-content-executed",
    "execution_hash_matches_approval": true,
    "completed": true
  },
  "sequence_integrity": "INTACT — approval precedes execution, content hash matches"
}
```

### Article 14 Mapping

| Article 14 Requirement | E2 Coverage |
|---|---|
| Art 14(1) — Measures enable effective oversight | Chain proves oversight happened at the correct point in the sequence |
| Art 14(3)(c) — Ability to override or stop | Intervention events are chain-bound, proving they actually interrupted the sequence |
| Art 14(4)(a) — Stop button or similar | Chain shows: intervention event → no subsequent actions until human re-authorizes |

---

## E3 — Multi-Verified Oversight Proof

**Purpose:** Multiple independent verifiers confirm that human oversight was genuine — not fabricated by the gateway operator.

### Template

```json
{
  "evidence_grade": "E3",
  "oversight_receipt_id": "receipt-e3-oversight-f7a8b9c0",
  "verifiers": [
    {
      "verifier_id": "verifier-alpha",
      "confirmed_facts": [
        "Human identity eddie was authenticated via mTLS at 2026-07-28T14:29:57Z",
        "Approval hash matches action execution hash",
        "Oversight event is chain-bound between action 46 and action 47"
      ],
      "verification": "PASS"
    },
    {
      "verifier_id": "verifier-beta",
      "confirmed_facts": [
        "Oversight timestamp (14:30:00) within 3 seconds of action timestamp (14:30:03)",
        "No evidence of retrospective oversight injection",
        "Human identity certificate chain validates to trusted CA"
      ],
      "verification": "PASS"
    }
  ],
  "consensus": {
    "genuine_human_oversight": true,
    "retrospective_injection": false,
    "forgery_risk": "NEGLIGIBLE"
  }
}
```

### Article 14 Mapping

| Article 14 Requirement | E3 Coverage |
|---|---|
| Art 14(3) — Effective human oversight | Multi-verifier consensus proves oversight was genuine, not fabricated |
| Art 14(4)(a) — Stop button | Verifiers confirm intervention events are authentic and cannot be forged |

---

## E4 — Cross-Certified Oversight Certificate

**Purpose:** Highest-grade certificate proving ongoing human oversight across all agent operations for a given period. Suitable for Article 43 conformity assessment.

### Template

```json
{
  "evidence_grade": "E4",
  "certificate_id": "e4-oversight-2026-07-28",
  "period": "2026-07-28T00:00:00Z to 2026-07-28T23:59:59Z",
  "aggregate_metrics": {
    "total_actions": 2847,
    "human_approved": 287,
    "human_rejected": 12,
    "policy_auto_approved": 2548,
    "human_interventions": 3,
    "mean_approval_time_ms": 2200,
    "max_approval_time_ms": 15000,
    "emergency_stops_triggered": 0
  },
  "oversight_ratio": {
    "high_risk_actions_requiring_oversight": 299,
    "high_risk_actions_with_oversight": 299,
    "compliance_rate": 1.0
  },
  "compliance_assertions": {
    "eu_ai_act_article_14_1": "PASS — Human oversight measures implemented and evidenced",
    "eu_ai_act_article_14_3_a": "PASS — Humans understand system through per-action content review",
    "eu_ai_act_article_14_3_b": "PASS — Human can decide not to use agent for specific actions",
    "eu_ai_act_article_14_3_c": "PASS — Human can override, stop, or intervene on every action",
    "eu_ai_act_article_14_4_a": "PASS — Stop button equivalent: no action executes without current approval"
  },
  "signature": "ed25519:e4-oversight-signature",
  "rfc3161_timestamps": ["timestamp-token-data"]
}
```

---

## Quick Reference: Evidence Grade → Article 14 Coverage

| Grade | What It Proves | Art 14(1) | Art 14(3) | Art 14(4) | Use Case |
|---|---|---|---|---|---|
| **E0** | Oversight events occurred | ✅ source | ✅ source | ✅ source | Internal audit, SIEM |
| **E1** | Oversight was gateway-signed | ✅ direct | ✅ direct | ❌ | Human oversight records |
| **E2** | Oversight happened in correct sequence | ✅ | ✅ direct | ✅ direct | Risk management docs |
| **E3** | Oversight was independently verified | ✅ | ✅ | ✅ | Conformity assessment |
| **E4** | Continuous compliant oversight certified | ✅ | ✅ | ✅ | Regulatory submission |
