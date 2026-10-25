"""Pins the caller-auth envelope that the Gateway verifies.

The envelope is a protocol, not an implementation detail: a consumer that builds
it differently gets its requests refused. These vectors are fixed so a change to
the helper cannot silently drift away from the Gateway.
"""

import hashlib
import hmac

from witnessos_sdk.auth import (
    PROTOCOL_VERSION,
    body_digest,
    canonical_envelope,
    sign_request,
    signature,
)

SECRET = "test-secret-do-not-use"
REQUEST_ID = "0123456789abcdef0123456789abcdef"
TIMESTAMP = 1700000000
PATH = "/v1/foundation/cases/wos_example"


def test_protocol_version_is_one():
    assert PROTOCOL_VERSION == "1"


def test_body_digest_matches_sha256_framing():
    assert body_digest(b"") == (
        "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    assert body_digest(b'{"a":1}') == (
        "sha256:015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862"
    )


def test_canonical_envelope_shape():
    env = canonical_envelope(
        method="GET",
        path=PATH,
        caller_id="atlas",
        operator_id="vault",
        request_id_value=REQUEST_ID,
        timestamp=TIMESTAMP,
        body_hash=body_digest(b""),
    )
    assert env == (
        f"1:GET:{PATH}:atlas:vault:{REQUEST_ID}:{TIMESTAMP}:"
        "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    )
    assert env.count(":") == 8


def test_signature_is_hmac_sha256_over_the_envelope():
    headers = sign_request(
        "GET",
        PATH,
        b"",
        caller_id="atlas",
        operator_id="vault",
        secret=SECRET,
        request_id_value=REQUEST_ID,
        timestamp=TIMESTAMP,
    )
    env = canonical_envelope(
        method="GET",
        path=PATH,
        caller_id="atlas",
        operator_id="vault",
        request_id_value=REQUEST_ID,
        timestamp=TIMESTAMP,
        body_hash=body_digest(b""),
    )
    expected = hmac.new(
        SECRET.encode(), env.encode(), hashlib.sha256
    ).hexdigest()
    assert headers["X-WitnessOS-Signature"] == expected
    assert headers["X-WitnessOS-Caller"] == "atlas"
    assert headers["X-WitnessOS-Request-Id"] == REQUEST_ID
    assert headers["X-WitnessOS-Timestamp"] == str(TIMESTAMP)
    assert headers["X-WitnessOS-Body-Hash"] == body_digest(b"")


def test_signature_helper_is_deterministic():
    assert signature("a:b:c", SECRET) == signature("a:b:c", SECRET)
    assert signature("a:b:c", SECRET) != signature("a:b:d", SECRET)


def test_fresh_request_ids_differ():
    a = sign_request(
        "GET", PATH, b"", caller_id="atlas", operator_id="vault", secret=SECRET
    )
    b = sign_request(
        "GET", PATH, b"", caller_id="atlas", operator_id="vault", secret=SECRET
    )
    assert a["X-WitnessOS-Request-Id"] != b["X-WitnessOS-Request-Id"]
