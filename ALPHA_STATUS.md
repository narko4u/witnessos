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
- RFC 3161 TSA external anchoring with offline re-verification (E4-capable verification. Current production receipts: E2 pending independent provider corroboration.)
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

- **E3 (Corroborated):** A party other than the deployment, whose identity a verifier establishes from its own trust input, confirmed the outcome. A gateway record of a provider acknowledgement is not that on its own: it is the deployment's own account, so current production receipts cap at E2 Enforced.
- **Stripe operations:** Test mode only during Alpha. Does not constitute proof of a live financial transaction.
- **E4 (Anchored):** WitnessOS supports E4 Anchored evidence and independently verifies RFC 3161 timestamping and Merkle inclusion proofs. Current production receipts remain E2 Enforced until independently authenticated provider/counterparty corroboration is available. The capability is built and verified: strict-mode anchoring with CRL/OCSP revocation at generation time and persisted TSA endpoint provenance, exported as a bundle (TSA token plus signed case-head commitment) that a third party re-verifies offline with zero trust in the operator. Anchoring does not, on its own, establish E4: it presupposes Corroborated evidence, and E3/E4 production issuance is gated on independent provider corroboration. Independent review proceeds through the design-partner alpha.

## Contact

Design Partner inquiries: contact@empirelabs.com.au — we provide NDA-protected access to the production gateway codebase for qualified evaluations (see README.md).

Security disclosures: contact@empirelabs.com.au (see SECURITY.md)
