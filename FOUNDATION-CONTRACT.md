# WitnessOS Foundation Consumer Contract

**Contract version:** 1.0
**Status:** frozen for the Foundation v1.0.0 release candidate
**Schema:** [FOUNDATION-CONTRACT.schema.json](FOUNDATION-CONTRACT.schema.json)
**Python model:** [witnessos-sdk/src/witnessos_sdk/contract.py](witnessos-sdk/src/witnessos_sdk/contract.py)

A consumer of WitnessOS evidence needs to answer four questions without reading a
gateway database, a Merkle tree, a signing key or a trust policy:

1. what did the agent ask to do,
2. what did the authority decide,
3. what actually happened,
4. what has been proven about the record of it.

This document freezes the shape of those answers. It is versioned as a whole. The
JSON schema and the Python model are generated from the same definitions and are
part of the contract, not a convenience.

## 1. Fields

Every graded action a consumer receives carries these fields. Optional fields that
are absent and fields whose value is `UNKNOWN` mean the same thing: not established.

| Field | Type | Who states it | Meaning |
|---|---|---|---|
| `contract_version` | string | Empire Labs | `1.0` for this version. A consumer pins it and refuses an unrecognised major version. |
| `case_id` | string | gateway | Stable identifier for the governed action. The handle a consumer quotes. |
| `action_family` | string | gateway | Governed action family, for example `provider.charge`. |
| `target` | string | gateway | Provider or peer the action addresses. |
| `proposal_digest` | string | gateway | sha256 over the canonical proposal bytes. What the policy decided against. |
| `requested_at` | string | gateway | RFC 3339 UTC timestamp of the request. |
| `decision` | enum | enforcement point | `ALLOW`, `DENY`, `UNKNOWN`. |
| `authority_state` | enum | enforcement point | `GRANTED`, `DENIED`, `EXPIRED`, `UNKNOWN`. Whether a grant stood behind the action. |
| `policy_id` | string | enforcement point | Policy that produced the decision. |
| `decided_by` | string | enforcement point | Identity of the enforcement point, never the acting agent. |
| `execution_state` | enum | enforcing path or provider | `EXECUTED`, `FAILED`, `DISPATCHED`, `UNKNOWN`. A dispatch acknowledgement is not execution. |
| `sealed_batch_id` | string | gateway | The sealed batch the achieved grade belongs to. |
| `sealed_through_sequence` | integer | gateway | Last event sequence the sealed batch covers. |
| `unsealed_tail_events` | integer | gateway | Events outside the sealed batch. Non-zero does not weaken the sealed grade and is never hidden. |
| `provisional_grade` | string | gateway | Grade supported before the case is batch bound. Never final evidence. |
| `achieved_evidence_grade` | string | gateway | Grade for the sealed batch. Empty until a batch binding exists. |
| `verified_grade` | string | relying party | Grade the consumer's own verifier reached. Always empty from the gateway. |
| `grade_status` | enum | gateway | `PROVISIONAL`, `ACHIEVED`, `UNKNOWN`. |
| `grade_scope` | string | gateway and verifier | Boundary the grade describes, for example `E2 @ sealed batch <id> / through sequence 4`. |
| `grade_cap_reason` | string | gateway and verifier | The rung that stopped the ladder and the missing prerequisite, for example `capped at E2: E3: no corroboration was appraised`. |
| `receipt_id` | string | gateway | Evidence receipt for this case. |
| `provider_operation_id` | string | provider | Provider-side identifier, when a provider was involved. |

## 2. Rules a consumer may rely on

- **UNKNOWN is never a pass.** `UNKNOWN` in `decision`, `authority_state`,
  `execution_state` or `grade_status` is not authorised, not enforced, not executed
  and not graded. The reference model raises rather than let an UNKNOWN be read as
  consent.
- **The issuer never states a verified grade.** `verified_grade` is filled by the
  relying party's verifier under its own trust policy. A gateway that fills it is
  asserting the result of a check it cannot run on itself.
- **A grade without a scope is incomplete.** `grade_scope` names the boundary and
  `grade_cap_reason` names why the ladder stopped. A consumer that receives a capped
  grade without a reason has received an incomplete record.
- **The grade belongs to a snapshot.** `sealed_batch_id` and
  `sealed_through_sequence` fix which body of events the grade is about. Events in
  `unsealed_tail_events` are not covered by it.
- **No private internals.** Nothing in this contract requires access to the gateway's
  database, its Merkle tree, its keys or its trust policy. A consumer that finds
  itself needing one of those has a contract defect to report, not a workaround to
  build.
- **Anchoring is not required for E3.** An E3 bundle exports without a timestamp and
  verifies offline. E4 is E3 plus an authenticated external anchor and is the relying
  party's conclusion.

## 3. Compatibility

- **1.x** may add optional fields and new enum members that do not change the meaning
  of an existing value. A consumer must tolerate unknown fields and must treat an
  unrecognised enum member as `UNKNOWN`, never as an upgrade.
- **2.0** is required for any rename, removal, type change or a change in the meaning
  of an existing value.
- The grade ladder itself is defined in
  [EVIDENCE-GRADES.md](EVIDENCE-GRADES.md) version 1.4 and closes at E4 Anchored.
  This contract carries the ladder's output, it does not redefine it.

## 4. Minimal consumer walk-through

```python
from witnessos_sdk.contract import CONTRACT_VERSION, FoundationCase

case = FoundationCase.model_validate(payload)      # payload from the gateway or a verifier
assert case.contract_version == CONTRACT_VERSION    # pin it, do not assume it

case.refuse_if_unknown()        # an UNKNOWN is a refusal, not a maybe
if not case.is_authorised:      # GRANTED only
    return "refused"
if not case.is_verified:        # the consumer's own verifier has not run yet
    return "evidence not yet independently verified"
```

The same rule holds outside Python. A consumer in any language validates the payload
against the JSON schema, pins `contract_version`, and refuses any `UNKNOWN` before
treating an action as authorised or its evidence as verified.

## 4a. Where the projection comes from

A consumer obtains this contract object read-only:

```
GET /v1/foundation/cases/{case_id}
```

The gateway produces it from its own record, validates it against
[FOUNDATION-CONTRACT.schema.json](FOUNDATION-CONTRACT.schema.json) before
returning it and answers `404` for a case it has nothing recorded for. The SDK
method is `WitnessOSClient.get_foundation_case()`, which parses the body into
`FoundationCase`. A consumer must not import engine internals or rebuild the
projection; see [INTEGRATION-v1.0.1.md](INTEGRATION-v1.0.1.md).

---

Part of the [WitnessOS](https://github.com/narko4u/witnessos) family,
[Empire Labs Pty Ltd](https://www.empirelabs.com.au)
