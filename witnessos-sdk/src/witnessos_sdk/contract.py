"""WitnessOS Foundation consumer contract, version 1.0.

This module is the frozen shape a consumer builds against. It carries only what a
consumer may depend on: an identifier for the case, the decision and the two states
that explain it, the sealed batch a grade belongs to and the grades themselves.
Nothing here reaches into a gateway database, a Merkle tree, a signing key or a
trust policy, because a consumer that needs those is not consuming evidence, it is
re-implementing the producer.

Two rules run through every field.

UNKNOWN is a value, not a blank. A consumer that cannot establish a fact must read
UNKNOWN, and UNKNOWN is never authorised, never enforced, never corroborated and
never verified. A missing field and an UNKNOWN field mean the same thing and neither
is a pass.

The issuer states at most an achieved grade. ``verified_grade`` is stated by the
relying party's own verifier, never by the party that produced the evidence.

Field names follow the shipped implementation rather than a parallel vocabulary, so
that a consumer reading a gateway case and a consumer reading this model see one set
of names. ``achieved_evidence_grade`` is the batch-bound grade the gateway reports;
``grade_cap_reason`` is the gateway's ``cap_reason`` and the verifier's
``grade_cap_reason``.

Version this module as a whole. A change to a field name, a type or an enum member is
a new contract version, and consumers pin ``CONTRACT_VERSION``.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

CONTRACT_VERSION = "1.0"


class Decision(str, Enum):
    """What the authority decided about the proposed action."""

    ALLOW = "ALLOW"
    DENY = "DENY"
    UNKNOWN = "UNKNOWN"


class AuthorityState(str, Enum):
    """Whether a grant stood behind the action, as far as the record shows."""

    GRANTED = "GRANTED"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"
    UNKNOWN = "UNKNOWN"


class ExecutionState(str, Enum):
    """What happened to the action once authorised.

    UNKNOWN is the honest answer for an action whose effect was never observed. A
    dispatch acknowledgement is not execution and must not be reported as it.
    """

    EXECUTED = "EXECUTED"
    FAILED = "FAILED"
    DISPATCHED = "DISPATCHED"
    UNKNOWN = "UNKNOWN"


class GradeStatus(str, Enum):
    """Which grade the issuer is reporting."""

    PROVISIONAL = "PROVISIONAL"
    ACHIEVED = "ACHIEVED"
    UNKNOWN = "UNKNOWN"


class FoundationCase(BaseModel):
    """One governed action as a consumer sees it, at contract version 1.0."""

    contract_version: str = Field(default=CONTRACT_VERSION)
    case_id: str = Field(description="Stable identifier for the governed action")

    # Proposal / request. A request is not a record of an effect.
    action_family: Optional[str] = Field(
        default=None, description="Governed action family, for example 'provider.charge'"
    )
    target: Optional[str] = Field(default=None, description="Provider or peer the action addresses")
    proposal_digest: Optional[str] = Field(
        default=None,
        description="sha256 over the canonical proposal bytes; what the policy decided against",
    )
    requested_at: Optional[str] = Field(default=None, description="RFC 3339 timestamp (UTC)")

    # Decision and the states that explain it.
    decision: Decision = Field(default=Decision.UNKNOWN)
    authority_state: AuthorityState = Field(default=AuthorityState.UNKNOWN)
    policy_id: Optional[str] = Field(default=None, description="Policy that produced the decision")
    decided_by: Optional[str] = Field(
        default=None, description="Enforcement point identity, never the acting agent"
    )
    execution_state: ExecutionState = Field(default=ExecutionState.UNKNOWN)

    # The snapshot a grade belongs to.
    sealed_batch_id: Optional[str] = Field(default=None)
    sealed_through_sequence: Optional[int] = Field(
        default=None, description="Last event sequence the sealed batch covers"
    )
    unsealed_tail_events: Optional[int] = Field(
        default=None,
        description="Events outside the sealed batch. Non-zero does not weaken the sealed grade",
    )

    # The grades, each attributed to whoever is entitled to state it.
    provisional_grade: Optional[str] = Field(
        default=None, description="Issuer, before batch binding. Never final evidence"
    )
    achieved_evidence_grade: Optional[str] = Field(
        default=None, description="Issuer, for the sealed batch. Empty until a batch binding exists"
    )
    verified_grade: Optional[str] = Field(
        default=None, description="Relying party's verifier. Always empty from the issuer"
    )
    grade_status: GradeStatus = Field(default=GradeStatus.UNKNOWN)
    grade_scope: Optional[str] = Field(
        default=None, description="Boundary the grade describes, for example 'E2 @ sealed batch X'"
    )
    grade_cap_reason: Optional[str] = Field(
        default=None,
        description="Rung that stopped the ladder and the missing prerequisite, null when uncapped",
    )

    # Evidence handles a consumer may quote.
    receipt_id: Optional[str] = Field(default=None, description="Evidence receipt for this case")
    provider_operation_id: Optional[str] = Field(
        default=None, description="Provider-side identifier, when a provider was involved"
    )

    @property
    def is_authorised(self) -> bool:
        """True only for an explicit grant. UNKNOWN and DENY both answer False."""
        return self.authority_state is AuthorityState.GRANTED

    @property
    def is_verified(self) -> bool:
        """True only when a relying party's verifier has stated a grade."""
        return bool(self.verified_grade)

    def refuse_if_unknown(self) -> None:
        """Raise rather than let an UNKNOWN be read as a pass."""
        if self.authority_state is AuthorityState.UNKNOWN:
            raise ValueError(f"case {self.case_id}: authority state is UNKNOWN")
        if self.execution_state is ExecutionState.UNKNOWN:
            raise ValueError(f"case {self.case_id}: execution state is UNKNOWN")
        if self.grade_status is GradeStatus.UNKNOWN:
            raise ValueError(f"case {self.case_id}: grade status is UNKNOWN")
