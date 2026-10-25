"""The published canonical digest examples, pinned in the SDK.

These four values are published in the Foundation v1.0.1 integration doc. They were
generated from the Gateway implementation, and they are asserted here so the public
helper and the engine cannot drift apart without a test failing.
"""

import hashlib
import json

import pytest

from witnessos_sdk.digest import (
    DIGEST_FIELDS,
    canonical_mission_bytes,
    canonical_mission_digest,
    canonical_mission_preimage,
)

EXAMPLE = {
    "intent": "Survey grid A and hold on completion",
    "steps": [{"action": "survey", "parameters": {"zone": "A", "altitude_m": 25}}],
    "capability_profile": {"has_camera": True},
    "robot_class": "field_marker",
}

EXAMPLE_CANONICAL = (
    '{"capability_profile":{"has_camera":true},'
    '"intent":"Survey grid A and hold on completion",'
    '"robot_class":"field_marker",'
    '"steps":[{"action":"survey","parameters":{"altitude_m":25,"zone":"A"}}]}'
)
EXAMPLE_DIGEST = "sha256:d5166d48c699a12df1736d3885665d5dcec492e189dc25c20450aa73ce563a1c"

UNICODE_DIGEST = "sha256:e0ea516d13de799633687b25486e86f13cb332c06c533b692b0c68be732ed5a1"
EXTRA_FIELD_DIGEST = "sha256:09a086fe4f2f004efdad7b2e7c2b3f91c5e5ff9482b590175cb1b95adf56314c"


def test_published_canonical_bytes():
    assert canonical_mission_bytes(
        intent=EXAMPLE["intent"],
        steps=EXAMPLE["steps"],
        capability_profile=EXAMPLE["capability_profile"],
        robot_class=EXAMPLE["robot_class"],
    ) == EXAMPLE_CANONICAL.encode("utf-8")


def test_published_digest():
    assert canonical_mission_digest(
        intent=EXAMPLE["intent"],
        steps=EXAMPLE["steps"],
        capability_profile=EXAMPLE["capability_profile"],
        robot_class=EXAMPLE["robot_class"],
    ) == EXAMPLE_DIGEST


def test_non_ascii_is_escaped_not_raw_utf8():
    digest = canonical_mission_digest(
        intent="Survey café grid",
        steps=[{"action": "survey", "parameters": {"zone": "A"}}],
        capability_profile={},
        robot_class="generic",
    )
    assert digest == UNICODE_DIGEST
    canonical = canonical_mission_bytes(
        intent="Survey café grid",
        steps=[{"action": "survey", "parameters": {"zone": "A"}}],
        capability_profile={},
        robot_class="generic",
    )
    assert b"\\u00e9" in canonical
    assert "é".encode("utf-8") not in canonical


def test_mission_id_is_outside_the_preimage():
    preimage = canonical_mission_preimage(
        intent=EXAMPLE["intent"],
        steps=EXAMPLE["steps"],
        capability_profile=EXAMPLE["capability_profile"],
        robot_class=EXAMPLE["robot_class"],
    )
    assert tuple(sorted(preimage)) == tuple(sorted(DIGEST_FIELDS))
    assert "mission_id" not in preimage


def test_hashing_the_mission_id_is_the_documented_negative_example():
    payload = {
        "capability_profile": EXAMPLE["capability_profile"],
        "intent": EXAMPLE["intent"],
        "mission_id": "atlas-e2-ref-001",
        "robot_class": EXAMPLE["robot_class"],
        "steps": EXAMPLE["steps"],
    }
    wrong = "sha256:" + hashlib.sha256(
        json.dumps(payload, separators=(",", ":"), sort_keys=True, ensure_ascii=True).encode()
    ).hexdigest()
    assert wrong == EXTRA_FIELD_DIGEST
    assert wrong != EXAMPLE_DIGEST


def test_robot_class_has_no_default():
    with pytest.raises(TypeError):
        canonical_mission_digest(
            intent=EXAMPLE["intent"],
            steps=EXAMPLE["steps"],
            capability_profile=EXAMPLE["capability_profile"],
        )


def test_empty_capability_profile_is_an_empty_object_not_null():
    preimage = canonical_mission_preimage(
        intent="x", steps=[], capability_profile=None, robot_class="generic"
    )
    assert preimage["capability_profile"] == {}
    assert canonical_mission_bytes(
        intent="x", steps=[], capability_profile=None, robot_class="generic"
    ) == b'{"capability_profile":{},"intent":"x","robot_class":"generic","steps":[]}'
