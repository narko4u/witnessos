# EU AI Act — Article 43 (Conformity Assessment)
## E0-E4 Evidence Templates

**Regulation:** EU AI Act, Article 43 — Conformity Assessment for high-risk AI systems
**Enforcement:** August 2, 2026
**Context:** Article 43 requires providers of high-risk AI systems to undergo a conformity assessment procedure before placing the system on the market. For autonomous AI agents, this means demonstrating that the governance and oversight framework meets Articles 8-15 requirements. WitnessOS evidence receipts provide the verifiable audit trail necessary for Article 43 compliance.

---

## E0 — Raw Conformity Data Feed

**Purpose:** Raw, unfiltered stream of all data that feeds into the conformity assessment. Includes action logs, policy evaluations, oversight events, and system configuration snapshots.

### Template

```json
{
  "evidence_grade": "E0",
  "data_category": "conformity_raw",
  "collection_period": {
    "start": "2026-07-01T00:00:00Z",
    "end": "2026-07-28T23:59:59Z"
  },
  "datasets": [
    {
      "name": "action_log",
      "record_count": 82347,
      "size_bytes": 16469400
    },
    {
      "name": "policy_evaluations",
      "record_count": 6745,
      "size_bytes": 1349000
    },
    {
      "name": "oversight_events",
      "record_count": 1245,
      "size_bytes": 249000
    },
    {
      "name": "schema_validations",
      "record_count": 82347,
      "size_bytes": 823470
    },
    {
      "name": "system_configurations",
      "record_count": 12,
      "size_bytes": 120000
    }
  ],
  "data_integrity": {
    "total_records": 172696,
    "total_hash": "sha256:aggregate-data-hash",
    "gap_detection": "NO_GAPS_FOUND"
  }
}
```

### Article 43 Mapping

| Article 43 Requirement | E0 Coverage |
|---|---|
| Art 43(1) — Conformity assessment obligation | Raw data is the foundation for any conformity assessment procedure |
| Art 43(4) — Technical documentation | Raw logs are the source data for technical documentation preparation |
| Art 43(5) — CE marking | Raw data supports the CE marking declaration |

---

## E1 — Signed Conformity Records

**Purpose:** Gateway-signed conformity records provide non-repudiable evidence of system configuration and policy state at specific points in time.

### Template

```json
{
  "evidence_grade": "E1",
  "record_type": "system_configuration_snapshot",
  "gateway_id": "wgos-gw-01",
  "gateway_signature": "ed25519:gateway-sig",
  "snapshot_timestamp": "2026-07-28T00:00:00.000Z",
  "system_state": {
    "witnessos_gateway_version": "v0.2.3-alpha",
    "policy_bundle_id": "pb-2026-07-v3",
    "policy_bundle_hash": "sha256:policy-bundle-hash",
    "policy_bundle_valid_from": "2026-07-01T00:00:00Z",
    "policy_bundle_valid_to": "2026-07-31T23:59:59Z",
    "aci_manifests_registered": 2,
    "agent_identities_registered": 2,
    "credential_vault_version": "v1.1.0",
    "evidence_store_uptime": "99.97%",
    "merkle_tree_anchor": "merkle:2026-07-28-daily-batch"
  },
  "conformity_status": {
    "article_9_risk_management": "ACTIVE",
    "article_14_human_oversight": "ACTIVE",
    "article_15_accuracy": "MONITORING"
  }
}
```

### Article 43 Mapping

| Article 43 Requirement | E1 Coverage |
|---|---|
| Art 43(1) — Assessment procedure | Signed configuration snapshots provide verifiable system state at assessment time |
| Art 43(4)(a) — System description | Signed snapshot describes the system architecture at a point in time |
| Art 43(4)(e) — Change management | Multiple signed snapshots show system evolution over the lifecycle |

---

## E2 — Chain-Bound Conformity Timeline

**Purpose:** Conformity events, configuration changes, and policy updates are hash-chained to prove the sequence of system evolution over time.

### Template

```json
{
  "evidence_grade": "E2",
  "chain_id": "chain-conformity-witnessos-2026",
  "chain_length": 28,
  "significant_events": [
    {
      "chain_position": 1,
      "timestamp": "2026-07-01T09:00:00Z",
      "event_type": "policy_bundle_activation",
      "bundle_id": "pb-2026-07-v1",
      "description": "Initial policy bundle for EU AI Act compliance"
    },
    {
      "chain_position": 12,
      "timestamp": "2026-07-15T14:30:00Z",
      "event_type": "policy_update",
      "bundle_id": "pb-2026-07-v2",
      "description": "Updated RBAC rules for developer role — restricted write access"
    },
    {
      "chain_position": 19,
      "timestamp": "2026-07-22T10:00:00Z",
      "event_type": "agent_registration",
      "agent_id": "agent-porgie-01",
      "aci_manifest_hash": "sha256:aci-manifest-hash",
      "description": "New agent registered with ACI manifest v1.0"
    },
    {
      "chain_position": 25,
      "timestamp": "2026-07-28T00:00:00Z",
      "event_type": "conformity_snapshot",
      "description": "End-of-period conformity snapshot"
    }
  ],
  "chain_integrity": "INTACT — all 28 links verified"
}
```

### Article 43 Mapping

| Article 43 Requirement | E2 Coverage |
|---|---|
| Art 43(2) — Notified body assessment | Chain provides complete timeline of system changes for notified body review |
| Art 43(3) — Ongoing compliance | Chain continuity proves unbroken compliance monitoring |
| Art 43(4)(e) — Change management | Every configuration change is chain-bound and auditable |

---

## E3 — Multi-Verified Conformity Receipt

**Purpose:** Multiple independent verifiers confirm the entire conformity evidence stack — policies, agent identities, oversight, action logs — is authentic and complete.

### Template

```json
{
  "evidence_grade": "E3",
  "conformity_receipt_id": "receipt-e3-conformity-2026-07-28",
  "verification_date": "2026-07-28T23:59:59Z",
  "verified_components": [
    {
      "component": "policy_bundle",
      "bundle_id": "pb-2026-07-v3",
      "verifiers": ["verifier-alpha", "verifier-beta"],
      "result": "AUTHENTIC — bundle hash matches, signing key validates"
    },
    {
      "component": "evidence_chains",
      "chain_ids": ["chain-agent-executor-01", "chain-agent-porgie-01"],
      "verifiers": ["verifier-alpha", "verifier-gamma"],
      "result": "INTACT — all links verified, no gaps, no forgeries"
    },
    {
      "component": "oversight_records",
      "period": "2026-07-01 to 2026-07-28",
      "verifiers": ["verifier-beta", "verifier-gamma"],
      "result": "GENUINE — all oversight events authenticated"
    },
    {
      "component": "credential_vault_audit",
      "period": "2026-07-01 to 2026-07-28",
      "verifiers": ["verifier-alpha", "verifier-gamma"],
      "result": "CLEAN — no unauthorized access, no credential leaks"
    }
  ],
  "overall_result": "PASS"
}
```

### Article 43 Mapping

| Article 43 Requirement | E3 Coverage |
|---|---|
| Art 43(1) — Assessment procedure | Multi-verified receipt can be submitted as part of the conformity assessment |
| Art 43(2) — Notified body | Notified body can use E3 receipt as starting point, reducing assessment cost |
| Art 43(3) — Ongoing compliance | Regular E3 receipts demonstrate continuous conformity |

---

## E4 — Cross-Certified Conformity Certificate

**Purpose:** The definitive compliance certificate for EU AI Act Article 43 conformity assessment. Cross-certified by multiple independent verification nodes, timestamped, and suitable for CE marking.

### Template

```json
{
  "evidence_grade": "E4",
  "certificate_id": "e4-conformity-witnessos-2026-07-28",
  "certification_type": "EU_AI_ACT_ARTICLE_43_CONFORMITY",
  "system_under_assessment": {
    "system_name": "WitnessOS Gateway",
    "system_version": "v0.2.3-alpha",
    "system_provider": "Empire Labs Pty Ltd",
    "system_classification": "High-risk AI system (Article 6 + Annex III)"
  },
  "assessment_period": {
    "start": "2026-07-01T00:00:00Z",
    "end": "2026-07-28T23:59:59Z"
  },
  "conformity_declarations": {
    "article_8_compliance_measures": "PASS",
    "article_9_risk_management": "PASS",
    "article_10_data_governance": "N/A — not a training system",
    "article_11_technical_documentation": "PASS — E4 certificate serves as documentation foundation",
    "article_12_record_keeping": "PASS — E0-E4 evidence store with 99.97% uptime",
    "article_13_transparency": "PASS — ACI manifests provide agent transparency",
    "article_14_human_oversight": "PASS — per-action hash-bound approval",
    "article_15_accuracy_and_robustness": "IN_PROGRESS — baseline established"
  },
  "merkle_checkpoint": {
    "checkpoint_id": "merkle:2026-07-28-conformity",
    "root_hash": "merkle:conformity-root-hash",
    "tree_size": 172696,
    "last_updated": "2026-07-28T23:59:59Z"
  },
  "certification_authority": {
    "authority_name": "WitnessOS Certification Authority (self-certified)",
    "authority_key": "ed25519:ca-public-key",
    "certificate_chain": [
      "ca-root.pem",
      "ca-intermediate.pem",
      "gateway-signing.pem"
    ]
  },
  "timestamps": [
    {
      "authority": "freetsa.org",
      "timestamp": "2026-07-28T23:59:59Z",
      "included": true
    }
  ],
  "signature": "ed25519:e4-conformity-signature"
}
```

### Article 43 Mapping

| Article 43 Requirement | E4 Coverage |
|---|---|
| Art 43(1) — Full conformity | E4 certificate serves as the complete conformity assessment record |
| Art 43(2) — Notified body submission | Certificate is ready for Notified Body review |
| Art 43(3) — Ongoing monitoring | Daily E4 generations demonstrate continuous compliance |
| Art 43(5) — CE marking | E4 certificate supports CE marking declaration |
| Art 43(6) — Documentation retention | Cryptographic evidence satisfies the 10-year retention requirement |

---

## CLI Usage

```bash
# Generate conformity evidence for Article 43 assessment
witnessos compliance --standard eu-ai-act --article 43 --evidence e0 --from 2026-07-01 --to 2026-07-28
witnessos compliance --standard eu-ai-act --article 43 --evidence e1 --system-snapshot
witnessos compliance --standard eu-ai-act --article 43 --evidence e2 --chain conformity-chain
witnessos compliance --standard eu-ai-act --article 43 --evidence e3 --verifier alpha,beta,gamma
witnessos compliance --standard eu-ai-act --evidence e4 --date 2026-07-28 --output pdf
witnessos compliance --standard eu-ai-act --evidence e4 --date 2026-07-28 --output json

# Full Article 43 assessment bundle
witnessos compliance --standard eu-ai-act --report full-assessment --period 2026-07 --output pdf
```
