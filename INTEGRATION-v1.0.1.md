# Integration guide - Foundation v1.0.1

This guide is what a dependent product needs to integrate against WitnessOS
Foundation. It documents three things that Foundation v1.0.0 left implicit: where
the contract projection comes from, how the canonical mission digest is computed
and how a deployment is provisioned from published artefacts.

Nothing here changes the contract. [FOUNDATION-CONTRACT.md](FOUNDATION-CONTRACT.md)
remains version 1.0, the evidence ladder in
[EVIDENCE-GRADES.md](EVIDENCE-GRADES.md) is unchanged and evidence issued under
v1.0.0 verifies under v1.0.1 with the same verifier.

---

## 1. Reading the contract projection

A case's projection is served read-only:

```
GET /v1/foundation/cases/{case_id}
```

Optional query parameter `stage` is `issuance` (default) or `verification`.

```python
from witnessos_sdk import WitnessOSClient

with WitnessOSClient("http://127.0.0.1:8400") as client:
    case = client.get_foundation_case("wos_...")
    print(case.contract_version, case.decision, case.authority_state,
          case.execution_state, case.provisional_grade, case.grade_cap_reason)
    if case.refuse_if_unknown():
        ...
```

In another language, call the route and validate the body against
[FOUNDATION-CONTRACT.schema.json](FOUNDATION-CONTRACT.schema.json). The response
always carries every contract field.

What a consumer may rely on:

- `contract_version` is `1.0`. Pin it. A 1.x addition is optional fields and new
  enum members only.
- `UNKNOWN` is a value, never a blank. A fact the issuer could not establish is
  `UNKNOWN` and `UNKNOWN` is never authorised, never enforced, never
  corroborated and never verified.
- `execution_state` is `DISPATCHED` when an enforcement point acknowledged a
  dispatch and `EXECUTED` only when the effect was observed. A dispatch
  acknowledgement is not execution.
- `achieved_evidence_grade` belongs to a sealed batch and is quoted with
  `grade_scope`, for example `E2 @ sealed batch X / through sequence N`. Events
  after that boundary are counted in `unsealed_tail_events` and cannot weaken the
  sealed grade.

Failure responses:

| Condition | Status | Body |
| --- | --- | --- |
| No recorded events for the case | `404` | `{"error": "case_not_found"}` |
| Projection could not be produced or did not validate | `500` | `{"error": "contract_projection_unavailable", "detail": ...}` |

A `200` never carries a partial contract. Treat any other status as "no
projection", never as a reason to reconstruct one.

## 2. Ingress boundary

```
Gateway consumer ingress is local-host Unix Domain Socket only.
```

A valid HMAC envelope alone does not authorise a remote TCP caller. Ingress is
peer-credential based: the gateway identifies the caller through the socket and a
TCP caller presenting a correctly signed envelope is refused with
`403 caller_not_authenticated`. That is intentional for the current deployment
profile. Run the consumer on the same host as the gateway or in a container that
shares the socket. Cross-host authenticated transport belongs to a later
deployment phase.

## 3. Canonical mission digest (normative)

A mission request declares a digest and the gateway recomputes it over what it
received. A mismatch is refused, so the rule below is not advisory.

### Preimage

Exactly four fields:

```
{intent, steps, capability_profile, robot_class}
```

`mission_id`, risk assessments, metadata, timestamps, agent identity and any
wrapper document are outside the preimage.

### Canonicalisation

1. Take exactly those four fields, with the values the gateway will receive.
2. Serialise as JSON with no spaces (`separators=(",", ":")`), sorted keys
   (`sort_keys=True`) and ASCII escaping (`ensure_ascii=True`, so non-ASCII reaches
   the bytes as `\uXXXX`, never as raw UTF-8).
3. Encode that string as UTF-8. With ASCII escaping it is pure ASCII.
4. SHA-256 over those bytes.
5. Render as `sha256:` followed by 64 lowercase hex characters.

### Worked example

Input:

```json
{
  "intent": "Survey grid A and hold on completion",
  "steps": [{"action": "survey", "parameters": {"zone": "A", "altitude_m": 25}}],
  "capability_profile": {"has_camera": true},
  "robot_class": "field_marker"
}
```

Canonical string, 191 bytes:

```
{"capability_profile":{"has_camera":true},"intent":"Survey grid A and hold on completion","robot_class":"field_marker","steps":[{"action":"survey","parameters":{"altitude_m":25,"zone":"A"}}]}
```

Digest:

```
sha256:d5166d48c699a12df1736d3885665d5dcec492e189dc25c20450aa73ce563a1c
```

### Non-ASCII characters

The same shape with `intent: "Survey café grid"`:

Canonical string:

```
{"capability_profile":{},"intent":"Survey caf\u00e9 grid","robot_class":"generic","steps":[{"action":"survey","parameters":{"zone":"A"}}]}
```

Digest:

```
sha256:e0ea516d13de799633687b25486e86f13cb332c06c533b692b0c68be732ed5a1
```

A consumer that writes raw UTF-8 here produces different bytes and is refused.
This is the most common integration mistake.

### Negative example

Hashing `mission_id` as part of the object is wrong. For
`{capability_profile, intent, mission_id, robot_class, steps}` with
`mission_id = "atlas-e2-ref-001"` the digest is:

```
sha256:09a086fe4f2f004efdad7b2e7c2b3f91c5e5ff9482b590175cb1b95adf56314c
```

which is not the expected digest. A second negative: omitting `robot_class` and
hashing an empty string in its place. The gateway hashes what it received, so an
omitted field mismatches rather than defaulting.

### Use the helper, not a reimplementation

```python
from witnessos_sdk.digest import canonical_mission_digest

digest = canonical_mission_digest(
    intent="Survey grid A and hold on completion",
    steps=[{"action": "survey", "parameters": {"zone": "A", "altitude_m": 25}}],
    capability_profile={"has_camera": True},
    robot_class="field_marker",
)
```

The helper is generic: it belongs to the Foundation contract, not to any one
mission model. The examples above are its tests.

### Versioning

Foundation 1.x keeps this rule exactly as documented. A change to the serializer,
the field set, the prefix or the hash function is a breaking change and ships as a
new contract version with a new digest rule name. Adding fields to your own mission
model does not change the rule; those fields stay outside the preimage.

## 4. Provisioning a deployment

Deny-by-default is the shipped posture: a principal that is not bound cannot
approve and a deployment with no binding refuses every approval with
`rbac_not_configured_deny_by_default`. Provisioning is how you get through that
default and it is checked rather than assumed.

```
witnessos provision init \
  --data-dir /var/lib/witnessos/data \
  --keys-dir /var/lib/witnessos/keys \
  --packs-dir /var/lib/witnessos/packs \
  --approver operator-7 --tenant '*'
```

`init` does the following and fails if any step is not satisfied:

1. creates the data and key directories at mode `0700`;
2. generates a receipt signing key if none exists and reports its key id, never
   the private key;
3. installs the shipped policy packs into `--packs-dir`, records a sha256 for each
   in `<data-dir>/packs-manifest.json` and confirms the policy engine loads them;
4. binds the approver principal to the approving role for the named tenant and
   writes that binding to `<data-dir>/rbac.env` at mode `0600`;
5. proves the bound principal can approve `robot.mission.execute`;
6. proves a principal that is not bound is refused.

The binding is the environment entry the gateway reads:

```
export WITNESSOS_RBAC_ADMIN_PRINCIPALS='operator-7:*'
```

Verify at any time, including after a restore:

```
witnessos provision verify \
  --data-dir /var/lib/witnessos/data \
  --keys-dir /var/lib/witnessos/keys \
  --packs-dir /var/lib/witnessos/packs
```

`verify` reads the recorded binding rather than re-deriving one from its
arguments, checks the packs against the manifest, checks the signing key and
re-proves both directions. A pack file that no longer matches the manifest fails
verification, because the deployment would otherwise judge actions under policy
the operator never approved.

Deployment state is exactly four things and they are backed up together: the data
directory, the key directory, the packs directory and the effective environment. A
restore of one without the others is a different deployment, so run `verify` after
any restore.

## 5. What this guide does not cover

Cross-host transport, provider connectors and E3 corroboration are deployment and
product decisions, not Foundation contract surfaces. A consumer that needs any of
them is asking for a new capability, not for a looser contract.

---

Part of the [WitnessOS](https://github.com/narko4u/witnessos) family,
[Empire Labs Pty Ltd](https://www.empirelabs.com.au)
