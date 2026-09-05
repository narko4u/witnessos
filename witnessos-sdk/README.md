# WitnessOS Python SDK

A Python SDK for interacting with the WitnessOS enforcement gateway.

```python
from witnessos_sdk import WitnessOSClient, GmailSendRequest

with WitnessOSClient("http://localhost:8400") as client:
    # Check health
    print(client.health())

    # Send an email (permissive mode auto-dispatches)
    resp = client.send_email(GmailSendRequest(
        to="partner@example.com",
        subject="Hello from SDK",
        body="This is a WitnessOS-governed email.",
    ))
    print(f"Case: {resp.case_id}, Status: {resp.status}")

    # In strict mode: fire → approve
    # client.set_policy("strict")
    # resp = client.send_email(...)
    # if resp.status == "approval_required":
    #     dispatch = client.approve(resp.case_id)
    #     print(f"Dispatched: {dispatch.receipt_id}")

    # Get full signed receipt
    receipt = client.get_receipt(resp.case_id)
    print(f"Evidence grade: {receipt.evidence_grade}")

    # Get Merkle chain
    chain = client.get_chain(resp.case_id)
    print(f"Chain root: {chain.root[:40]}...")
```

## Installation

```bash
pip install witnessos-sdk
```

Or from source:
```bash
cd witnessos-sdk
pip install -e .
```

## API

| Method | Description |
|--------|-------------|
| `health()` | Check gateway status + policy mode |
| `set_policy(mode)` | Switch strict/permissive |
| `send_email(req)` | Request gmail.send action |
| `refund(req)` | Request stripe.refund action |
| `approve(case_id)` | Approve + dispatch pending action |
| `deny(case_id)` | Deny pending action |
| `list_cases()` | All cases with status |
| `get_case(case_id)` | Single case detail + events |
| `get_chain(case_id)` | Merkle chain visualisation |
| `get_receipt(case_id)` | Full signed receipt |
| `fire_and_approve(to, subject, body)` | Two-step convenience |
| `wait_for_approval(case_id)` | Poll until resolved |
| `reset()` | Reset demo server state |

## Requirements

- Python 3.10+
- httpx
- pydantic 2+
