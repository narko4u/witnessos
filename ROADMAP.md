# WitnessOS - Roadmap

## Current Status
**Phase E Complete** - Security review, R7.1 hardening, OpenSSL boundary, crash safety, Docker deployment, 360 tests passing. **Phase F (Design Partner Alpha)** is the current phase - single partner, invitation-only, E4 evidence grade in strict mode (E3 default in all other configurations). **Live proof 2026-09-04:** first full-loop gateway-mediated send (human-approved, provider-acknowledged) independently verified via the WitnessOS CLI verifier.

---

## Roadmap

### Phase A - Foundation ✅
- [x] Receipt spec frozen (SPEC.md v1.0)
- [x] Canonical JSON library (RFC 8785 serialisation)
- [x] Event store - append-only, SQLite + Merkle tree engine
- [x] Key generation and management (Ed25519 keypairs, key registry)
- [x] CLI verifier: `witnessos verify <receipt_id>`

### Phase B - Gateway Core ✅
- [x] FastAPI gateway skeleton with mTLS
- [x] Credential Broker - Gmail OAuth, `gmail.send` scope, agent never holds credentials
- [x] Action Permit issuance and JTI redemption ledger
- [x] Policy Engine - approval_required for external_email risk class
- [x] Approval UI - exact action diff, scope, expiry, approve/deny
- [x] Gmail connector - send endpoint, response capture

### Phase C - Evidence Layer ✅
- [x] Lifecycle event recording - all 11 event types
- [x] Receipt generation from event stream (derived view)
- [x] Hash chaining and Merkle checkpointing
- [x] RFC 3161 external timestamping (TSA anchoring)
- [x] WORM anchor - customer S3/GCS, optional

### Phase D - Policy, RBAC, Caps, Kill-Switch ✅
- [x] Policy taxonomy - pack-based rules with action bindings
- [x] Persistent approval queue - event-sourced with expiry
- [x] Tenant isolation - first-class scoping, non-overridable
- [x] RBAC and Separation of Duties - role-based access with SoD enforcement
- [x] Atomic cap reservations - monthly financial caps with SQLite atomicity
- [x] Kill-switch semantics - emergency connector disable, webhook-safe
- [x] Acceptance gate - full E2E pipeline verifiable

### Phase E - Security Review + R7.1 Hardening ✅
- [x] R0: Credential exposure remediation
- [x] R1: Deployment security (Docker, non-root, read-only rootfs)
- [x] R2: Concurrency claim race fix (C-01 - proven at 50-thread)
- [x] R3: Deny-by-default RBAC + self-approval bypass fix
- [x] R4: Gateway approve URL unpredictability + nonce replay protection
- [x] R5: Queue transition validation + caps currency
- [x] R6: Archive hygiene, forensic quarantine, delivery manifest
- [x] R7.1: OpenSSL ts-verify boundary hardening, CMS §5.4 fix, algorithm enforcement, E4 structural disable (superseded - re-enabled 2026-09-03 with revocation + provenance gates), Docker digest pinning, crash boundary proofs (Gmail + Stripe)
- [x] Test suite: 360 passed, 1 skipped, 0 failures
- [x] Reviewer brief, test procedures, closeout template
- [x] Disposable deployment script, credential rotation/destroy script
- [ ] Independent security review execution (reviewer)
- [ ] Deployed E0 acceptance tests in live environment

### Phase F - Design Partner Alpha (Current)
- [x] 1 Design Partner onboarded - 2–4 week operational review before expanding
- [x] Gmail governed sends (sandbox/test mode)
- [x] Stripe test-mode refund operations
- [ ] Incident and support channel
- [x] Operator dashboard - approval screen, read-only
- [ ] Operators 2–3 added after operational review passes
- [x] Maximum evidence grade: E4 (strict mode) - CRL/OCSP revocation at genTime plus persisted provenance landed 2026-09-03; E3 remains the default in all other configurations

### Phase G - Enterprise Readiness
- [ ] Stripe live mode
- [ ] Multi-tenant cloud deployment
- [ ] Full operator dashboard
- [ ] SLA and compliance reporting
- [ ] E4 at enterprise scale - production TSA wiring and roll-out (engine strict-mode capability landed 2026-09-03)
- [ ] Customer-managed KMS/HSM
- [ ] SSO, enterprise RBAC
- [ ] 7-year retention, audit packs

---

**Current deliverable:** Design Partner Alpha (Phase F). Invitation-only.
**Not yet available:** Self-service deployment, enterprise readiness, live financial controls, multi-tenant SaaS.

For Design Partner inquiries: contact@empirelabs.com.au

---

## Compliance Pack Roadmap

Parallel to the gateway roadmap, the compliance toolkit ships independently:

| Milestone | Repository | Status |
|---|---|---|
| EU AI Act evidence templates (Article 9, 14, 43) | [eu-ai-act-compliance-grade](https://github.com/narko4u/eu-ai-act-compliance-grade) | ✅ Complete |
| Docker/Kubernetes deployment pack | Compliance toolkit | 🔄 In Progress |
| Design Partner kit (Phase 5C) | Compliance toolkit | ⏳ Planned |
| Design Partner outreach (10 companies) | Phase 6A | ⏳ Planned |
| Revenue ops (GumRoad, Stripe) | Phase 6B | ⏳ Planned |
