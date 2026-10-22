# WitnessOS Evidence Grades

**Status:** normative
**Version:** 1.3, published 2026-10-22 (1.2 published 2026-10-21, 1.1 published 2026-10-13, 1.0 published 2026-10-04)
**Canonical at:** this document

WitnessOS defined this ladder in 2026-06. It is the ladder the product uses. This is its
canonical statement. Where another surface states it differently this document wins and that
surface is a defect to fix.

Version 1.1 removed one ambiguity in the E3 row. Version 1.2 states how a verifier establishes
that the party behind E3 is someone other than the deployment, and lists what does not establish
it. Version 1.3 aligns the normative wording with the hardened implementation released as
WitnessOS Gateway v0.1.0 and witnessos-verifier v0.3.5, following
MOP-WITNESSOS-EVIDENCE-GRADE-AUDIT-001: the E3 row states the chain a verifier appraises, the E4
row no longer carries a custody requirement, and retention is named only as an attribute. The
rungs, their names and their prerequisites are otherwise unchanged.

## 1. What a grade is

A grade answers exactly one question:

> What has actually been proven about this statement?

It is a conclusion a verifier reaches from evidence the verifier can check for itself. It is
never a description a producer writes about itself.

Two consequences follow. Both are enforced rather than merely intended:

- **A grade is output, never input.** A record that carries a `grade` field is not thereby
  graded. The field is recorded as an attempt and ignored. Trust is what the verifier
  concludes, not what the record asserts.
- **A grade measures the strength of the evidence, not the outcome of the action.** An E4
  receipt can legitimately report a failed action, an unknown outcome or a confirmed effect.
  The grade says how well the claim is supported. It says nothing about whether the claim is
  good news.

## 2. The ladder

Every receipt carries exactly one grade, drawn from this closed set of five rungs.

| Grade | Name | What it proves | What is required to reach it |
|---|---|---|---|
| **E0** | Declared | An agent claims it acted. Nothing independent stands behind the claim. | Nothing. This is the floor and the honest answer when only a claim exists. |
| **E1** | Observed | An independent party witnessed the action. Gaps remain possible. | Instrumentation outside the acting agent, plus a trust decision that identifies who the instrumentation speaks for. |
| **E2** | Enforced | The action was authorised and routed through an enforcement point and policy was applied by something other than the acting agent. | A route the agent cannot bypass, plus a recorded policy decision against the specific action. |
| **E3** | Corroborated | The destination confirmed the outcome, and the verifier can show the confirmation belongs to this action. | An executed action, a provider attestation signed under a key the verifier trusts, a provider record that identifies the effect, a binding between that record and this action, substantive provider facts rather than a restatement of the request, and no reuse of a provider record already spent on another action. |
| **E4** | Anchored | Legitimate E3 corroborated evidence, plus an external timestamp and a Merkle checkpoint that a third party can verify offline. | Everything E3 requires, plus an external timestamp from a trust service whose certificate path authenticates against a trust anchor the verifier supplies, revocation checked at the timestamp's generation time, and a Merkle inclusion proof. No access to the producer's storage and no trust in the producer's clock. |

Use the name with the rung. The names are **Declared, Observed, Enforced, Corroborated,
Anchored**. A bare letter is not a definition and a bare adjective is not one either.

E3 rests on a party that is not the deployment. A state probe the deployment runs and reports
is the deployment's own account of itself, so it reaches no rung above the one its other
evidence already supports. The disqualifiers are published so that a reader can check them
rather than take this paragraph on trust:
[what makes a party independent](https://github.com/narko4u/evidence-record-spec/blob/main/VERIFIABILITY-OVERVIEW.md#what-makes-a-party-independent).

## 3. The ladder is nested and it fails closed

A rung is never awarded on a foundation that did not hold.

- E4 presupposes E1 through E3. An anchor proves that a record existed in a given form at a
  given time. It does not prove that the record is accurate, so it cannot carry a rung whose
  own prerequisites are missing.
- A component that cannot be demonstrated **caps** the grade at the highest rung whose
  prerequisites genuinely hold. It never inflates the grade.
- If a caller demands a grade that cannot be shown, verification **fails**. It does not warn
  and it does not round up.

### 3.1 What a verifier can conclude on its own, and what it cannot

Added 2026-10-21 after the evidence-grade audit. This subsection describes the reference
verifier; it does not weaken anything above. Where a requirement cannot be established from a
bundle alone, the verifier caps the grade and states the reason.

| Rung | What the reference verifier tests | What it still needs from outside the bundle |
|---|---|---|
| E1 | That at least one event was recorded by something other than the acting agent, and that every event carries a valid signature under a key the bundle publishes. This is a check on the record's shape, not on who wrote it. | A trust decision naming who the instrumentation speaks for. The reference verifier has no such input yet, so it reports E1 as observed-in-the-record and says plainly that the observer's identity was not authenticated. |
| E2 | That a policy decision and an authorisation both precede the action in the same case, in addition to chain, ledger, manifest and batch integrity. | That the enforcement point is genuinely non-bypassable. That is a property of the gateway's execution path, not of a file. |
| E3 | That a provider attestation is signed by a key the operator provisions under `provider_keys` in the verifier's trust policy (or `WITNESSOS_PROVIDER_KEYS_FILE` for standalone CLI use), that the key is not one of the bundle's own signing keys, that it follows an executed action in the same case, that the provider record it names is bound to this action and carries substantive provider facts, and that the record has not already been spent on a different action. | An independently obtained provider key. A key inside the bundle proves signature consistency, never identity. |
| E4 | E3 plus Merkle inclusion and an RFC 3161 timestamp verified against an operator-supplied trust anchor, with revocation checked at generation time. | Nothing further. Anchoring never substitutes for E3. Retention is reported separately and is not part of this test. |

Two consequences are worth stating plainly, because both were once assumed rather than
checked:

- **An event type is not evidence.** A record that writes `provider.confirmed` has asserted
  that a provider confirmed something. The assertion is recorded and it moves no grade until a
  key the operator trusts signs it and binds it to this action.
- **Naming a party is not corroboration.** Naming a provider, a peer or an engine in a payload
  proves that a string was written. Independence is decided by key custody and by what the key
  signed, never by the number of names that agree.

### 3.2 What does not establish that the other party is who it claims

Added in version 1.2. Each of these has been read as provider identity on some surface at some
point, and none of them is:

- a **provider name** written in a payload
- a **provider event type**, such as `provider.confirmed` or `provider.acknowledged`
- a **bundled key**, including one published in the same record's `keys.json`
- **producer metadata**, including operation ids, receipt hashes and timestamps the producer wrote
- a **producer custody declaration**, including a field that says `EXTERNAL`
- a **basis engine name**, including ours

Identity comes from one place only: a verifier or operator trust route that exists outside the
producer's evidence and that the producer cannot write. The reference verifier reads provider keys
from its own trust policy file. Where it has none, it reports the failure and caps the record.

The two consequences are absolute, and no combination of the items above changes either:

- **No authenticated identity means no E3.** An acknowledgement whose signer cannot be tied to a
  party outside the deployment is the deployment's own account of itself.
- **No E3 means no E4.** Anchoring proves that a record existed in a given form at a given time.
  It cannot supply a corroboration the record never had.

This is the position WitnessOS publishes about its own deployment: **the released platform,
WitnessOS Gateway v0.1.0 with witnessos-verifier v0.3.5, supports hardened E4 Anchored evidence
when the required independent corroboration and authenticated external anchoring conditions are
satisfied.** Historical demonstration receipts issued before the hardened model remain at the
grade the current verifier establishes, which for the project's published demonstration record is
E2 Enforced. Nothing here asserts that every governed action reaches E4: the grade is what the
verifier concludes from the evidence in front of it, and a missing prerequisite caps it.

## 4. Properties are not rungs

Some facts about a record are real and worth reporting. They are still not grades. They are
carried as named properties and they never move the grade.

| Property | What it establishes | Why it is not a rung |
|---|---|---|
| `self_signed` | A key carried inside a record signed that record. | Proves integrity and possession of that key. Proves nothing about who holds it, so the statement stays at E0. |
| `identity_route` | The route by which a verifier bound a key to a subject. | The binding is a trust decision made outside the record. Reported as a property. It is what lets E1 be earned. |
| `retained_by` | An independent custodian holds a copy of the snapshot. | Proves the record still exists. It was never proof that the record is more true. |
| revocation state | Whether the signing certificate was valid at the relevant time. | Informs whether an E4 timestamp can be trusted. It is not a rung of its own. |

**Retention is an attribute, never a rung.** There is no rung for custody. A custodian can
demonstrate that evidence still exists. That is not corroboration and it is not anchoring.
Where a policy requires retention, that is a requirement the policy sets and it is reported as
such. It is not a grade and a deployment that does not involve a custodian is not thereby a
lower grade.

## 5. The ladder closes at E4

E4 Anchored is the highest grade WitnessOS issues. Nothing we publish asserts a rung above it.

An unrecognised or out of range value in a grade field is a **failure**. It is not a new rung
and it is not a hint that a higher one exists. An implementation that reads an unexpected value
and treats it as better than E4 has a defect. An implementation that invents a rung has broken
the contract.

## 6. Retired vocabulary

Earlier drafts and derivatives of them used different words for some of these rungs. Those
words are retired. They must not be used as vocabulary again on any surface. Where one of them
appears, name the rung instead.

| Retired word | What it means now |
|---|---|
| claim only | E0 Declared. Meaning unchanged. |
| self attested | E0 Declared, plus the `self_signed` property. It was previously read as E1. |
| issuer verified | E1 Observed, plus the `identity_route` property. It was previously read as E2. |
| anchored | E4 Anchored. The word is fine as the rung name itself. |
| retained | Not a grade. Carried as the `retained_by` property. It was previously read as a top rung. |

## 7. What this ladder does not claim

- It does not claim a grade above E4 and no WitnessOS surface asserts one.
- It does not claim that anchoring makes a record immutable. Anchoring proves that a record
  existed in a given form at a given time and that it has not changed since. It is a claim
  about the record, not about the storage media holding it.
- It does not claim that corroboration means success. See section 1.
- It does not claim to be settled by a standards body. It is the WitnessOS definition,
  published so that others can cite it, implement it and check it.

## 8. How to cite

Cite this document rather than a README table, so that the citation pins to a version and a
path:

> WitnessOS evidence grades, E0 Declared through E4 Anchored, version 1.3,
> Empire Labs Pty Ltd,
> https://github.com/narko4u/witnessos/blob/main/EVIDENCE-GRADES.md

## 8.1 Revision notes

- v1.3, 2026-10-22: aligned normative wording with Gateway v0.1.0 and verifier v0.3.5 following
  MOP-WITNESSOS-EVIDENCE-GRADE-AUDIT-001. E3 states the chain a verifier appraises, E4 states
  authenticated anchoring and drops the custody requirement, and retention is named only as an
  attribute.

## 9. Related documents

- [SPEC.md](SPEC.md) section 2. The frozen specification's statement of the same ladder,
  unchanged since the v1.0 freeze.
- [ALPHA_STATUS.md](ALPHA_STATUS.md). Current issuance constraints.
- WitnessOS Gateway v0.1.0 (release notes available to partners under NDA) and
  [witnessos-verifier v0.3.5](https://github.com/narko4u/witnessos-verifier/releases/tag/v0.3.5),
  the aligned release that implements this version.
- [README.md](README.md). The product-facing summary.

---

Part of the [WitnessOS](https://github.com/narko4u/witnessos) family,
[Empire Labs Pty Ltd](https://www.empirelabs.com.au)
