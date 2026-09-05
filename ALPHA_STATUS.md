# WitnessOS - Alpha Status

**Current phase:** F - Design Partner Alpha
**Maximum evidence grade:** E4 (strict mode; E3 default in all other configurations)
**Design partners:** One at a time, invitation-only

---

## What's Available

- Gateway enforcement with credential broker (Gmail + Stripe test mode)
- Policy engine with human approval workflow
- Action permits with JTI redemption and DPoP binding
- Event-sourced lifecycle with all 11 event types
- Hash-chained receipts with Merkle checkpointing
- RFC 3161 TSA external anchoring (E4 anchored receipts issuing live since 2026-09-05)
- Independent CLI verifier (`witnessos verify`)
- RBAC with separation of duties
- Kill-switch and financial caps
- Docker deployment (non-root, read-only rootfs)

## What's NOT Available During Alpha

- **Self-service deployment** - Alpha partners are onboarded directly by Empire Labs.
- **Live financial transactions** - Stripe operations use test mode only.
- **Multi-tenant SaaS** - Single-tenant deployment per design partner.
- **Enterprise features** - SSO, customer-managed KMS, 7-year retention, SLA.

## Design Partner Alpha

Current Alpha operates under these constraints:

- **One design partner at a time** - 2-4 week operational review before expanding
- **Invitation-only** - No self-service signup
- **Gmail governed sends** - Sandbox/test mode only
- **Stripe test-mode operations** - No live money movement
- **Gateway enforcement** - applies only to actions routed through WitnessOS-held credentials

## Evidence Grade Precision

- **E3 (Corroborated):** Destination provider acknowledged the action. This means Gmail API accepted the send - it does NOT independently prove delivery, inbox placement, or read status.
- **Stripe operations:** Test mode only during Alpha. Does not constitute proof of a live financial transaction.
- **E4 (Anchored):** Strict-mode issuance is live (2026-09-05) with CRL/OCSP revocation at generation time and persisted TSA endpoint provenance. E4 anchored receipts issue against a provisioned, revocation-verifiable TSA trust root; each receipt exports as a bundle (TSA token plus signed case-head commitment) that a third party can re-verify offline with zero trust in the operator. Deployments without strict mode or a revocation-verifiable anchor cap at E3. Independent review proceeds through the design-partner alpha.

## Contact

Design Partner inquiries: contact@empirelabs.com.au — we provide NDA-protected access to the production gateway codebase for qualified evaluations (see README.md).

Security disclosures: contact@empirelabs.com.au (see SECURITY.md)
