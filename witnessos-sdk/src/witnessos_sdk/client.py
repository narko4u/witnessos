"""
WitnessOS Python SDK Client.

Connects to a WitnessOS gateway via HTTP and provides a typed, ergonomic API
for requesting actions, managing approvals, and retrieving evidence.
"""

import json
import time
from typing import Any, Optional
from urllib.parse import urljoin

import httpx

from .models import (
    CaseSummary,
    CasesResponse,
    ChainData,
    DispatchResponse,
    GmailSendRequest,
    GmailSendResponse,
    PolicyMode,
    ReceiptData,
    RefundRequest,
    RefundResponse,
)


class WitnessOSClient:
    """Client for the WitnessOS gateway API.

    Connects to a WitnessOS demo server or production gateway over HTTP.

    Args:
        base_url: Base URL of the WitnessOS server (e.g. http://localhost:8400)
        timeout: HTTP request timeout in seconds (default: 30)
    """

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(timeout=httpx.Timeout(timeout))
        self._url = lambda path: urljoin(f"{self.base_url}/", path.lstrip("/"))

    # ── Health & Policy ───────────────────────────────────────────────────

    def health(self) -> dict[str, Any]:
        """Check gateway health and current policy mode."""
        resp = self._client.get(self._url("/demo/health"))
        resp.raise_for_status()
        return resp.json()

    def set_policy(self, mode: str) -> dict[str, Any]:
        """Switch policy enforcement mode (strict or permissive)."""
        resp = self._client.post(
            self._url(f"/demo/policy/{mode}")
        )
        resp.raise_for_status()
        return resp.json()

    # ── Actions ───────────────────────────────────────────────────────────

    def send_email(self, request: GmailSendRequest) -> GmailSendResponse:
        """Request to send an email through the WitnessOS gateway.

        In permissive mode, the email is auto-dispatched.
        In strict mode, returns approval_required - use approve() to proceed.
        """
        payload = {
            "action_type": "email",
            "sender": request.sender,
            "to": request.to,
            "subject": request.subject,
            "body": request.body,
            "agent_id": request.agent_id,
        }
        if request.cc:
            payload["cc"] = request.cc
        if request.bcc:
            payload["bcc"] = request.bcc

        resp = self._client.post(
            self._url("/demo/action"),
            json=payload,
        )
        resp.raise_for_status()
        return GmailSendResponse(**resp.json())

    def refund(self, request: RefundRequest) -> RefundResponse:
        """Request a refund through the WitnessOS gateway.

        In permissive mode, the refund is auto-dispatched.
        In strict mode, returns approval_required.
        """
        payload = {
            "action_type": "refund",
            "payment_intent": request.payment_intent,
            "amount": request.amount,
            "currency": request.currency,
            "agent_id": request.agent_id,
        }
        if request.reason:
            payload["reason"] = request.reason
        if request.idempotency_key:
            payload["idempotency_key"] = request.idempotency_key

        resp = self._client.post(
            self._url("/demo/action"),
            json=payload,
        )
        resp.raise_for_status()
        return RefundResponse(**resp.json())

    # ── Approvals ─────────────────────────────────────────────────────────

    def approve(self, case_id: str, note: str = "") -> DispatchResponse:
        """Approve a pending action. The gateway dispatches it immediately.

        Returns the dispatch result including receipt_id and chain commitment.
        """
        resp = self._client.post(
            self._url(f"/demo/approve/{case_id}"),
            json={"note": note},
        )
        resp.raise_for_status()
        return DispatchResponse(**resp.json())

    def deny(self, case_id: str, note: str = "") -> dict[str, Any]:
        """Deny a pending approval."""
        resp = self._client.post(
            self._url(f"/demo/deny/{case_id}"),
            json={"note": note},
        )
        resp.raise_for_status()
        return resp.json()

    # ── Evidence & Audit ──────────────────────────────────────────────────

    def list_cases(self) -> CasesResponse:
        """List all cases with queue status and event counts."""
        resp = self._client.get(self._url("/demo/cases"))
        resp.raise_for_status()
        data = resp.json()
        cases = [CaseSummary(**c) for c in data.pop("cases", [])]
        return CasesResponse(cases=cases, **data)

    def get_case(self, case_id: str) -> CaseSummary:
        """Get full details for a single case including all events."""
        resp = self._client.get(self._url(f"/demo/cases/{case_id}"))
        resp.raise_for_status()
        return CaseSummary(**resp.json())

    def get_chain(self, case_id: str) -> ChainData:
        """Get Merkle chain data for a completed case."""
        resp = self._client.get(self._url(f"/demo/chain/{case_id}"))
        resp.raise_for_status()
        return ChainData(**resp.json())

    def get_receipt(self, case_id: str) -> ReceiptData:
        """Get the full signed receipt for a completed case."""
        resp = self._client.get(self._url(f"/demo/receipt/{case_id}"))
        resp.raise_for_status()
        return ReceiptData(**resp.json())

    # ── Wait Helpers ──────────────────────────────────────────────────────

    def wait_for_approval(
        self,
        case_id: str,
        timeout: float = 30.0,
        poll_interval: float = 1.0,
    ) -> CaseSummary:
        """Poll a case until it leaves 'pending' status.

        Useful when waiting for human-in-the-loop approval.

        Args:
            case_id: The case to monitor.
            timeout: Max seconds to wait.
            poll_interval: Seconds between polls.

        Returns:
            The case summary with final status.

        Raises:
            TimeoutError: If the case doesn't resolve within timeout.
        """
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            case = self.get_case(case_id)
            if case.queue_status not in ("pending",):
                return case
            time.sleep(poll_interval)
        raise TimeoutError(
            f"Case {case_id} still pending after {timeout}s"
        )

    def fire_and_approve(
        self,
        to: str,
        subject: str,
        body: str,
        sender: str = "sender@example.com",
        agent_id: str = "sdk-client",
    ) -> DispatchResponse:
        """Convenience: request an email, then immediately approve it.

        Two-step pattern for strict mode: request_send → approve.
        Returns the final dispatch response.
        """
        req = GmailSendRequest(
            agent_id=agent_id,
            sender=sender,
            to=to,
            subject=subject,
            body=body,
        )
        resp = self.send_email(req)
        if resp.status == "approval_required":
            return self.approve(resp.case_id)
        # Already dispatched (permissive mode)
        return DispatchResponse(
            case_id=resp.case_id,
            status=resp.status or "dispatched",
            receipt_id=resp.receipt_id,
            provider_operation_id=resp.provider_operation_id,
            action_hash=resp.action_hash,
        )

    def reset(self) -> dict[str, Any]:
        """Reset the demo server - purge all data."""
        resp = self._client.post(self._url("/demo/reset"))
        resp.raise_for_status()
        return resp.json()

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._client.close()

    def __enter__(self) -> "WitnessOSClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
