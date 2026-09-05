"""Data models for the WitnessOS SDK - typed request/response objects."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """Supported action types in WitnessOS."""

    EMAIL = "email"
    REFUND = "refund"


class PolicyMode(str, Enum):
    """Demo policy enforcement modes."""

    STRICT = "strict"
    PERMISSIVE = "permissive"


class GmailSendRequest(BaseModel):
    """Request to send an email through the WitnessOS gateway."""

    agent_id: str = Field(default="sdk-client", description="Agent identity")
    sender: str = Field(default="sender@example.com", description="Sender email address (override in your config)")
    to: str = Field(..., description="Recipient(s), comma-separated")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body text")
    cc: Optional[str] = Field(default=None, description="CC recipients")
    bcc: Optional[str] = Field(default=None, description="BCC recipients")


class GmailSendResponse(BaseModel):
    """Response from requesting an email send through WitnessOS."""

    case_id: str
    status: str
    message: Optional[str] = None
    preview: Optional[str] = None
    mime_sha256: Optional[str] = None
    action_hash: Optional[str] = None
    expires_at: Optional[str] = None
    receipt_id: Optional[str] = None
    provider_operation_id: Optional[str] = None


class RefundRequest(BaseModel):
    """Request to process a refund through the WitnessOS gateway."""

    agent_id: str = Field(default="sdk-client", description="Agent identity")
    payment_intent: str = Field(..., description="Payment intent or charge ID")
    amount: float = Field(..., description="Refund amount")
    currency: str = Field(default="usd", description="Currency code")
    reason: Optional[str] = Field(default=None, description="Refund reason")
    idempotency_key: Optional[str] = Field(default=None, description="Idempotency key")


class RefundResponse(BaseModel):
    """Response from requesting a refund through WitnessOS."""

    case_id: str
    status: str
    message: Optional[str] = None
    action_hash: Optional[str] = None
    expires_at: Optional[str] = None
    receipt_id: Optional[str] = None
    provider_operation_id: Optional[str] = None


class DispatchResponse(BaseModel):
    """Response after approval and dispatch of an action."""

    case_id: str
    status: str
    receipt_id: Optional[str] = None
    provider_operation_id: Optional[str] = None
    chain_commitment: Optional[dict[str, Any]] = None
    action_hash: Optional[str] = None


class CaseSummary(BaseModel):
    """Summary of a single case in the audit view."""

    case_id: str
    action_type: str = ""
    queue_status: str = ""
    case_status: Optional[str] = None
    approver: Optional[str] = None
    approver_note: Optional[str] = None
    chain_commitment: Optional[dict[str, Any]] = None
    events: Optional[list[dict[str, Any]]] = None


class CasesResponse(BaseModel):
    """List of all cases from the audit endpoint."""

    cases: list[CaseSummary]
    total: Optional[int] = None
    pending: Optional[int] = None
    approved: Optional[int] = None
    completed: Optional[int] = None


class ChainData(BaseModel):
    """Merkle chain data for a case."""

    case_id: str
    leaf_count: int
    root: str
    leaves: list[str]
    levels: list[dict[str, Any]]
    proof: list[dict[str, Any]]


class ReceiptData(BaseModel):
    """Full signed receipt for a case."""

    receipt_id: str
    case_id: str
    status: Optional[str] = None
    evidence_grade: Optional[str] = None
    actor: Optional[dict[str, Any]] = None
    policy: Optional[dict[str, Any]] = None
    action: Optional[dict[str, Any]] = None
    outcome: Optional[dict[str, Any]] = None
    integrity: Optional[dict[str, Any]] = None
    timing: Optional[dict[str, Any]] = None
    chain_commitment: Optional[dict[str, Any]] = None
