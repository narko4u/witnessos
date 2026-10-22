# WitnessOS - Alpha Status

**Current phase:** F - Design Partner Alpha
**Maximum evidence grade:** E4 Anchored (strict mode; E3 default in all other configurations)
**Design partners:** One at a time, invitation-only

---

## What's Available

- Gateway enforcement with credential broker (Gmail + Stripe test mode)
- Policy engine with human approval workflow
- Action permits with JTI redemption and DPoP binding
- Event-sourced lifecycle with all 11 event types
- Hash-chained receipts with Merkle checkpointing
- Hardened E3 corroboration path and RFC 3161 external anchoring with offline re-verification, released as Gateway v0.1.0 with witnessos-verifier v0.3.5
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

- **E3 (Corroborated):** A party other than the deployment, whose identity a verifier establishes from its own trust input, confirmed the outcome. The verifier appraises an executed action, a provider attestation signed under a trusted key, a provider record that identifies the effect, a binding between that record and this action, substantive provider facts, and no reuse of that record on another action. A provider event type on its own is not corroboration: a gateway record of an acknowledgement it wrote itself is the deployment's own account, and it caps at E2 Enforced.
- **Hardened E4 is supported** by Gateway v0.1.0 and witnessos-verifier v0.3.5 when the required independent corroboration and authenticated anchoring conditions are satisfied.
- **Historical demonstration receipts** issued before the hardened model remain E2 where that is what the current verifier establishes.
- **Stripe operations:** Test mode only during Alpha. Does not constitute proof of a live financial transaction.
- **E4 (Anchored):** E4 presupposes legitimate E3 corroborated evidence and adds independently authenticated external anchoring. The implementation authenticates the timestamp's certificate path against a trust anchor the verifier supplies, checks revocation at generation time, and carries Merkle inclusion, exported as a bundle (TSA token plus signed case-head commitment) that a third party re-verifies offline with zero trust in the operator. Anchoring is not a substitute for corroboration, and an unrecognised grade value is a failure rather than a new rung. Retention and custody are reported as attributes: a deployment may verify them, leave them unverified or require them by policy, and none of that lifts E3 to E4. Independent review proceeds through the design-partner alpha.

## Contact

Design Partner inquiries: contact@empirelabs.com.au — we provide NDA-protected access to the production gateway codebase for qualified evaluations (see README.md).

Security disclosures: contact@empirelabs.com.au (see SECURITY.md)
