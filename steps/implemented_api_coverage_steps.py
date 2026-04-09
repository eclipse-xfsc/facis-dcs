"""Generic steps to cover currently implemented API endpoints."""

from datetime import datetime, timezone

import requests
from behave import then, when


def _now_rfc3339() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _payload_for_key(payload_key: str) -> dict | None:
    now = _now_rfc3339()
    payloads = {
        "none": None,
        "template_create": {
            "template_type": "FRAME_CONTRACT",
            "name": "BDD Coverage Template",
            "description": "Coverage request",
            "template_data": {"title": "coverage"},
        },
        "template_submit": {
            "did": "did:example:template:1",
            "updated_at": now,
            "reviewers": ["reviewer@example.org"],
            "approver": "approver@example.org",
        },
        "template_update": {
            "did": "did:example:template:1",
            "updated_at": now,
            "template_data": {"title": "updated"},
        },
        "template_update_manage": {
            "did": "did:example:template:1",
            "updated_at": now,
            "state": "DRAFT",
            "template_data": {"title": "managed"},
        },
        "template_verify": {
            "did": "did:example:template:1",
            "updated_at": now,
        },
        "template_approve": {
            "did": "did:example:template:1",
            "updated_at": now,
        },
        "template_reject": {
            "did": "did:example:template:1",
            "updated_at": now,
            "reason": "coverage",
        },
        "template_register": {
            "did": "did:example:template:1",
            "updated_at": now,
        },
        "template_archive": {
            "did": "did:example:template:1",
            "updated_at": now,
        },
        "contract_create": {
            "did": "did:example:template:1",
        },
        "contract_update": {
            "did": "did:example:contract:1",
            "updated_at": now,
            "contract_data": {"title": "updated"},
        },
        "contract_submit": {
            "did": "did:example:contract:1",
            "updated_at": now,
            "reviewers": ["reviewer@example.org"],
            "approver": "approver@example.org",
        },
        "contract_negotiate": {
            "did": "did:example:contract:1",
            "updated_at": now,
            "negotiated_by": "negotiator@example.org",
            "change_request": {"field": "value"},
        },
        "contract_respond": {
            "id": "neg-1",
            "action_flag": "ACCEPTING",
            "responded_by": "reviewer@example.org",
        },
        "contract_verify": {
            "did": "did:example:contract:1",
            "updated_at": now,
        },
        "contract_approve": {
            "did": "did:example:contract:1",
            "updated_at": now,
        },
        "contract_reject": {
            "did": "did:example:contract:1",
            "updated_at": now,
            "reason": "coverage",
        },
        "contract_store": {
            "did": "did:example:contract:1",
            "updated_at": now,
        },
        "contract_terminate": {
            "did": "did:example:contract:1",
            "updated_at": now,
        },
        "contract_audit": {
            "did": "did:example:contract:1",
            "updated_at": now,
        },
    }
    assert payload_key in payloads, f"Unknown payload key: {payload_key}"
    return payloads[payload_key]


@when('the system sends "{http_method}" request to protected endpoint "{endpoint}" with payload "{payload_key}"')
def step_when_protected_request(context, http_method, endpoint, payload_key):
    payload = _payload_for_key(payload_key)
    url = f"{context.base_url}{endpoint}"
    headers = getattr(context, "headers", {}).copy()
    headers.setdefault("Content-Type", "application/json")
    context.requests_response = requests.request(
        method=http_method,
        url=url,
        headers=headers,
        json=payload,
        timeout=context.http_timeout_seconds,
    )


@when('the system sends "{http_method}" request to public endpoint "{endpoint}"')
def step_when_public_request(context, http_method, endpoint):
    url = f"{context.base_url}{endpoint}"
    context.requests_response = requests.request(
        method=http_method,
        url=url,
        timeout=context.http_timeout_seconds,
    )


@then("the response status is 200")
def step_then_status_200(context):
    assert context.requests_response.status_code == 200, context.requests_response.text


@then('the response JSON includes "{field_name}"')
def step_then_json_field_present(context, field_name):
    body = context.requests_response.json()
    assert field_name in body, body
