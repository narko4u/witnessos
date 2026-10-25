"""
Caller authentication for signed Gateway requests.

The Gateway's consumer ingress is a local-host Unix domain socket. Identity has
two halves and both are checked:

* the operating-system peer credential on the socket decides *who* the operator
  is, so the operator id a caller signs must be the account it connects from;
* an HMAC envelope over the request proves the caller holds the shared secret.

The envelope canonical string is colon delimited and signed with HMAC-SHA256:

``protocol:method:path:caller_id:operator_id:request_id:timestamp:body_hash``

``body_hash`` is ``sha256:<hex>`` over the exact request body bytes, and a GET
with no body hashes the empty string. A request older than the replay window, or
one whose request id has been seen before, is refused by the Gateway.

This module exists so a consumer does not have to reimplement the envelope from
prose. It is the same rule the Gateway applies when it rebuilds the envelope
from the request.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import time
from typing import Optional

PROTOCOL_VERSION = "1"
REPLAY_WINDOW_SECONDS = 300


def body_digest(body: bytes) -> str:
    """Return the declared body hash for a request body (``sha256:<hex>``)."""
    return "sha256:" + hashlib.sha256(body).hexdigest()


def request_id() -> str:
    """Return a fresh request id."""
    return secrets.token_hex(16)


def canonical_envelope(
    method: str,
    path: str,
    caller_id: str,
    operator_id: str,
    request_id_value: str,
    timestamp: int,
    body_hash: str,
    protocol_version: str = PROTOCOL_VERSION,
) -> str:
    """Return the exact string the Gateway signs and verifies."""
    return (
        f"{protocol_version}:{method}:{path}:{caller_id}:{operator_id}:"
        f"{request_id_value}:{timestamp}:{body_hash}"
    )


def signature(payload: str, secret: str) -> str:
    """Return the hex HMAC-SHA256 of the canonical envelope."""
    return hmac.new(
        secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def sign_request(
    method: str,
    path: str,
    body: bytes,
    *,
    caller_id: str,
    operator_id: str,
    secret: str,
    request_id_value: Optional[str] = None,
    timestamp: Optional[int] = None,
) -> dict[str, str]:
    """Build the headers for one authenticated request.

    ``operator_id`` must be the account that opens the socket: the Gateway
    derives it from the peer credential and signs over the derived value, so a
    caller that signs a different name produces a signature that cannot verify.
    """
    rid = request_id_value or request_id()
    ts = int(time.time()) if timestamp is None else int(timestamp)
    digest = body_digest(body)
    envelope = canonical_envelope(
        method=method.upper(),
        path=path,
        caller_id=caller_id,
        operator_id=operator_id,
        request_id_value=rid,
        timestamp=ts,
        body_hash=digest,
    )
    return {
        "X-WitnessOS-Signature": signature(envelope, secret),
        "X-WitnessOS-Caller": caller_id,
        "X-WitnessOS-Request-Id": rid,
        "X-WitnessOS-Timestamp": str(ts),
        "X-WitnessOS-Body-Hash": digest,
        "Content-Type": "application/json",
    }
