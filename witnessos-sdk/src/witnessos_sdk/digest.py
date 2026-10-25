"""Canonical mission digest, as published by WitnessOS Foundation v1.0.1.

The Gateway recomputes a digest over the mission it received and refuses the
request when it differs from the one the caller declared. That refusal is correct
and it is not a policy decision: it means the caller serialised a different object.
Before v1.0.1 the rule was undocumented and the refusal arrived as a deny with no
reason, so the first integrator debugged a governance system when the fault was a
JSON encoder.

Use this function instead of reimplementing the rule. The rule is generic: it
belongs to the Foundation contract, not to any one mission model, so any consumer
mapping its own action into a GovernedAction hashes it the same way.

The rule, stated once:

* preimage is exactly ``{intent, steps, capability_profile, robot_class}``
* JSON with no spaces, sorted keys, ASCII-escaped non-ASCII
* UTF-8 bytes of that string
* SHA-256
* rendered as ``sha256:<64 lowercase hex>``

Nothing else is hashed. ``mission_id``, risk assessments, metadata, timestamps,
agent identity and any wrapper document are outside the preimage.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable, Mapping

DIGEST_RULE = "witnessos.foundation.digest.v1"
DIGEST_ALGORITHM = "sha256"
DIGEST_FIELDS = ("intent", "steps", "capability_profile", "robot_class")

__all__ = [
    "DIGEST_ALGORITHM",
    "DIGEST_FIELDS",
    "DIGEST_RULE",
    "canonical_mission_bytes",
    "canonical_mission_digest",
    "canonical_mission_preimage",
]


def canonical_mission_preimage(
    intent: str,
    steps: Iterable[Mapping[str, Any]],
    capability_profile: Mapping[str, Any] | None,
    robot_class: str,
) -> dict[str, Any]:
    """The four fields that are hashed, in the Gateway's own shape.

    ``capability_profile`` is optional here only because an empty profile is a
    legitimate value; pass ``{}`` or ``None`` and it becomes ``{}``, which is what
    the Gateway hashes when it receives no profile. Passing ``None`` is not a
    default for a missing field: ``robot_class`` has no default at all, because a
    consumer that guesses it gets a mismatch the Gateway reports as a deny.
    """
    return {
        "intent": intent,
        "steps": list(steps),
        "capability_profile": dict(capability_profile or {}),
        "robot_class": robot_class,
    }


def canonical_mission_bytes(
    intent: str,
    steps: Iterable[Mapping[str, Any]],
    capability_profile: Mapping[str, Any] | None,
    robot_class: str,
) -> bytes:
    """The exact bytes the Gateway hashes."""
    preimage = canonical_mission_preimage(intent, steps, capability_profile, robot_class)
    return json.dumps(
        preimage,
        separators=(",", ":"),
        sort_keys=True,
        ensure_ascii=True,
    ).encode("utf-8")


def canonical_mission_digest(
    intent: str,
    steps: Iterable[Mapping[str, Any]],
    capability_profile: Mapping[str, Any] | None,
    robot_class: str,
) -> str:
    """The ``sha256:`` digest a mission request must declare.

    Example (see the published integration doc for the worked example):

    >>> canonical_mission_digest(
    ...     intent="Survey grid A and hold on completion",
    ...     steps=[{"action": "survey", "parameters": {"zone": "A", "altitude_m": 25}}],
    ...     capability_profile={"has_camera": True},
    ...     robot_class="field_marker",
    ... )
    'sha256:d5166d48c699a12df1736d3885665d5dcec492e189dc25c20450aa73ce563a1c'
    """
    return f"{DIGEST_ALGORITHM}:" + hashlib.sha256(
        canonical_mission_bytes(intent, steps, capability_profile, robot_class)
    ).hexdigest()
