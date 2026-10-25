"""WitnessOS Python SDK - enforce, audit, and verify AI agent actions."""

__version__ = "0.1.1"


from .client import WitnessOSClient
from .contract import (
    CONTRACT_VERSION,
    AuthorityState,
    Decision,
    ExecutionState,
    FoundationCase,
    GradeStatus,
)
from .digest import (
    DIGEST_ALGORITHM,
    DIGEST_FIELDS,
    DIGEST_RULE,
    canonical_mission_bytes,
    canonical_mission_digest,
    canonical_mission_preimage,
)
from .models import (
    ActionType,
    CaseSummary,
    ChainData,
    DispatchResponse,
    GmailSendRequest,
    GmailSendResponse,
    PolicyMode,
    ReceiptData,
    RefundRequest,
    RefundResponse,
)

__all__ = [
    "WitnessOSClient",
    "CONTRACT_VERSION",
    "DIGEST_ALGORITHM",
    "DIGEST_FIELDS",
    "DIGEST_RULE",
    "canonical_mission_bytes",
    "canonical_mission_digest",
    "canonical_mission_preimage",
    "FoundationCase",
    "Decision",
    "AuthorityState",
    "ExecutionState",
    "GradeStatus",
    "GmailSendRequest",
    "GmailSendResponse",
    "RefundRequest",
    "RefundResponse",
    "DispatchResponse",
    "CaseSummary",
    "ChainData",
    "ReceiptData",
    "ActionType",
    "PolicyMode",
]
