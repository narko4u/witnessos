# WitnessOS Evidence Grades

**Status:** normative
**Version:** 1.0, published 2026-10-04
**Canonical at:** this document

WitnessOS defined this ladder in 2026-06. It is the ladder the product uses. This is its
canonical statement. Where another surface states it differently this document wins and that
surface is a defect to fix.

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
| **E3** | Corroborated | The destination confirmed the outcome. | A provider response or a state probe that speaks to the outcome rather than to the request. |
| **E4** | Anchored | The record carries an external timestamp and a Merkle checkpoint. A third party can verify both offline. | An external timestamp from a trust service, a Merkle inclusion proof and verification against a trust anchor the verifier supplies, with no access to the producer's storage and no trust in the producer's clock. |

Use the name with the rung. The names are **Declared, Observed, Enforced, Corroborated,
Anchored**. A bare letter is not a definition and a bare adjective is not one either.

## 3. The ladder is nested and it fails closed

A rung is never awarded on a foundation that did not hold.

- E4 presupposes E1 through E3. An anchor proves that a record existed in a given form at a
  given time. It does not prove that the record is accurate, so it cannot carry a rung whose
  own prerequisites are missing.
- A component that cannot be demonstrated **caps** the grade at the highest rung whose
  prerequisites genuinely hold. It never inflates the grade.
- If a caller demands a grade that cannot be shown, verification **fails**. It does not warn
  and it does not round up.

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

> WitnessOS evidence grades, E0 Declared through E4 Anchored, version 1.0,
> Empire Labs Pty Ltd,
> https://github.com/narko4u/witnessos/blob/main/EVIDENCE-GRADES.md

## 9. Related documents

- [SPEC.md](SPEC.md) section 2. The frozen specification's statement of the same ladder,
  unchanged since the v1.0 freeze.
- [ALPHA_STATUS.md](ALPHA_STATUS.md). Current issuance constraints.
- [README.md](README.md). The product-facing summary.

---

Part of the [WitnessOS](https://github.com/narko4u/witnessos) family,
[Empire Labs Pty Ltd](https://www.empirelabs.com.au)
