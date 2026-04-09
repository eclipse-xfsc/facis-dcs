"""Contract workflow steps for negotiation, adjustment, and approval slices."""

import os
import re

from behave import given, then, when

from support.api_client import (
    contract_approve_url,
    contract_create_url,
    contract_negotiate_url,
    contract_reject_url,
    contract_retrieve_by_id_url,
    contract_submit_url,
    contract_update_url,
    contract_verify_url,
    get_with_headers,
    post_json,
    put_json,
    template_approve_url,
    template_create_url,
    template_submit_url,
    template_verify_url,
)
from support.keycloak_client import (
    admin_token,
    assign_client_role,
    ensure_client,
    ensure_client_role,
    ensure_user,
    user_token,
)


def _headers_for_role(context, role: str) -> dict:
    client_id = os.getenv("BDD_KEYCLOAK_CLIENT_ID", "digital-contracting-service")
    role_safe = re.sub(r"[^A-Za-z0-9]+", "-", role.lower()).strip("-")
    username = f"bdd-{role_safe}"
    password = os.getenv("BDD_KEYCLOAK_TEST_USER_PASSWORD", "bdd-pass-123")
    adm = admin_token()
    client_uuid = ensure_client(adm, client_id)
    role_repr = ensure_client_role(adm, client_uuid, role)
    user_id = ensure_user(adm, username, password)
    assign_client_role(adm, user_id, client_uuid, role_repr)
    token = user_token(client_id, username, password)
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _username_for_role(role: str) -> str:
    role_safe = re.sub(r"[^A-Za-z0-9]+", "-", role.lower()).strip("-")
    return f"bdd-{role_safe}"


def _ensure_store(context, name, value):
    if not hasattr(context, name) or getattr(context, name) is None:
        setattr(context, name, value)


def _template_submit_payload(context, did: str, updated_at: str) -> dict:
    _headers_for_role(context, "Template Reviewer")
    _headers_for_role(context, "Template Approver")
    return {
        "did": did,
        "updated_at": updated_at,
        "reviewers": [_username_for_role("Template Reviewer")],
        "approver": _username_for_role("Template Approver"),
    }


def _template_reviewer_submit_payload(context, did: str, updated_at: str) -> dict:
    _headers_for_role(context, "Template Approver")
    return {
        "did": did,
        "updated_at": updated_at,
        "approver": _username_for_role("Template Approver"),
        "forward_to": "approval",
    }


def _contract_submit_payload(context, did: str, updated_at: str) -> dict:
    _headers_for_role(context, "Contract Reviewer")
    _headers_for_role(context, "Contract Approver")
    return {
        "did": did,
        "updated_at": updated_at,
        "reviewers": [_username_for_role("Contract Reviewer")],
        "approver": _username_for_role("Contract Approver"),
    }


def _contract_reviewer_submit_payload(context, did: str, updated_at: str) -> dict:
    _headers_for_role(context, "Contract Approver")
    return {
        "did": did,
        "updated_at": updated_at,
        "forward_to": "approval",
        "approver": _username_for_role("Contract Approver"),
    }


def _create_approved_template_for_contract(context):
    creator_h = _headers_for_role(context, "Template Creator")
    create_resp = post_json(
        context,
        template_create_url(context),
        {
            "template_type": "FRAME_CONTRACT",
            "name": "BDD Contract Source Template",
            "description": "BDD template for contract workflows",
            "template_data": {"title": "BDD Template", "clauses": [{"id": "c1", "text": "Base clause"}]},
        },
        headers=creator_h,
    )
    assert create_resp.status_code == 200, create_resp.text
    t_did = create_resp.json().get("did")

    retrieve_resp = get_with_headers(context, f"{context.base_url}/template/retrieve/{t_did}", headers=creator_h)
    assert retrieve_resp.status_code == 200, retrieve_resp.text
    updated_at = retrieve_resp.json().get("updated_at")

    submit_resp = post_json(
        context,
        template_submit_url(context),
        _template_submit_payload(context, t_did, updated_at),
        headers=creator_h,
    )
    assert submit_resp.status_code == 200, submit_resp.text

    reviewer_h = _headers_for_role(context, "Template Reviewer")
    retrieve_resp = get_with_headers(context, f"{context.base_url}/template/retrieve/{t_did}", headers=reviewer_h)
    updated_at = retrieve_resp.json().get("updated_at")

    verify_resp = post_json(
        context,
        template_verify_url(context),
        {"did": t_did, "updated_at": updated_at},
        headers=reviewer_h,
    )
    assert verify_resp.status_code == 200, verify_resp.text

    retrieve_resp = get_with_headers(context, f"{context.base_url}/template/retrieve/{t_did}", headers=reviewer_h)
    updated_at = retrieve_resp.json().get("updated_at")

    review_submit_resp = post_json(
        context,
        template_submit_url(context),
        _template_reviewer_submit_payload(context, t_did, updated_at),
        headers=reviewer_h,
    )
    assert review_submit_resp.status_code == 200, review_submit_resp.text

    approver_h = _headers_for_role(context, "Template Approver")
    retrieve_resp = get_with_headers(context, f"{context.base_url}/template/retrieve/{t_did}", headers=approver_h)
    updated_at = retrieve_resp.json().get("updated_at")
    approve_resp = post_json(
        context,
        template_approve_url(context),
        {"did": t_did, "updated_at": updated_at},
        headers=approver_h,
    )
    assert approve_resp.status_code == 200, approve_resp.text
    return t_did


def _create_contract_in_draft(context, contract_name: str):
    t_did = _create_approved_template_for_contract(context)
    creator_h = _headers_for_role(context, "Contract Creator")
    create_resp = post_json(context, contract_create_url(context), {"did": t_did}, headers=creator_h)
    assert create_resp.status_code == 200, create_resp.text
    c_did = create_resp.json().get("did")
    retrieve_resp = get_with_headers(context, contract_retrieve_by_id_url(context, c_did), headers=creator_h)
    assert retrieve_resp.status_code == 200, retrieve_resp.text
    updated_at = retrieve_resp.json().get("updated_at")

    _ensure_store(context, "contract_dids", {})
    _ensure_store(context, "contract_updated_at", {})
    _ensure_store(context, "contract_seed_headers", {})
    context.contract_dids[contract_name] = c_did
    context.contract_updated_at[contract_name] = updated_at
    context.contract_seed_headers[contract_name] = creator_h


def _contract_data(context, contract_name: str):
    did = context.contract_dids[contract_name]
    updated_at = context.contract_updated_at[contract_name]
    return did, updated_at


def _refresh_contract(context, contract_name: str):
    did = context.contract_dids[contract_name]
    headers = None
    if hasattr(context, "contract_seed_headers"):
        headers = context.contract_seed_headers.get(contract_name)
    resp = get_with_headers(context, contract_retrieve_by_id_url(context, did), headers=headers)
    assert resp.status_code == 200, resp.text
    context.contract_updated_at[contract_name] = resp.json().get("updated_at")
    return resp.json()


def _prepare_contract_under_review(context, contract_name: str):
    did, updated_at = _contract_data(context, contract_name)
    creator_h = context.contract_seed_headers[contract_name]
    submit_to_negotiation = post_json(
        context,
        contract_submit_url(context),
        _contract_submit_payload(context, did, updated_at),
        headers=creator_h,
    )
    assert submit_to_negotiation.status_code == 200, submit_to_negotiation.text
    _refresh_contract(context, contract_name)

    # Backend workflow transitions Draft -> Negotiation on first submit,
    # then Negotiation -> Submitted on a second creator submit.
    did, updated_at = _contract_data(context, contract_name)
    submit_to_submitted = post_json(
        context,
        contract_submit_url(context),
        _contract_submit_payload(context, did, updated_at),
        headers=creator_h,
    )
    assert submit_to_submitted.status_code == 200, submit_to_submitted.text
    _refresh_contract(context, contract_name)


def _prepare_contract_pending_approval(context, contract_name: str):
    did, _ = _contract_data(context, contract_name)
    _prepare_contract_under_review(context, contract_name)

    reviewer_h = _headers_for_role(context, "Contract Reviewer")
    retrieve = get_with_headers(context, contract_retrieve_by_id_url(context, did), headers=reviewer_h)
    assert retrieve.status_code == 200, retrieve.text
    updated_at = retrieve.json().get("updated_at")

    verify = post_json(
        context,
        contract_verify_url(context),
        {"did": did, "updated_at": updated_at},
        headers=reviewer_h,
    )
    assert verify.status_code == 200, verify.text

    retrieve = get_with_headers(context, contract_retrieve_by_id_url(context, did), headers=reviewer_h)
    assert retrieve.status_code == 200, retrieve.text
    updated_at = retrieve.json().get("updated_at")

    review_submit = post_json(
        context,
        contract_submit_url(context),
        _contract_reviewer_submit_payload(context, did, updated_at),
        headers=reviewer_h,
    )
    assert review_submit.status_code == 200, review_submit.text
    _refresh_contract(context, contract_name)


@given('contract "{name}" is in "Draft" status')
def step_given_contract_draft(context, name):
    _create_contract_in_draft(context, name)


@given('contract "{name}" is in "Under Review" status')
def step_given_contract_under_review(context, name):
    _create_contract_in_draft(context, name)
    _prepare_contract_under_review(context, name)


@given('contract "{name}" is pending approval')
def step_given_contract_pending_approval(context, name):
    _create_contract_in_draft(context, name)
    _prepare_contract_pending_approval(context, name)


@given('contract "{name}" requires my approval')
def step_given_contract_requires_my_approval(context, name):
    step_given_contract_pending_approval(context, name)


@given('contract "{name}" is open for negotiation')
def step_given_contract_open_for_negotiation(context, name):
    _create_contract_in_draft(context, name)


@given('contract "{name}" negotiation is complete')
def step_given_contract_negotiation_complete(context, name):
    _create_contract_in_draft(context, name)


@when('I open contract "{name}" for negotiation')
def step_when_open_for_negotiation(context, name):
    did, _ = _contract_data(context, name)
    context.requests_response = get_with_headers(context, contract_retrieve_by_id_url(context, did))


@when('I adjust clause "{clause}" with new text')
def step_when_adjust_clause(context, clause):
    name = "Service Agreement"
    did, updated_at = _contract_data(context, name)
    payload = {
        "did": did,
        "updated_at": updated_at,
        "contract_data": {
            "edited_clause": clause,
            "text": f"Updated by BDD for {clause}",
        },
    }
    context.requests_response = put_json(context, contract_update_url(context), payload)
    if context.requests_response.status_code == 200:
        _refresh_contract(context, name)


@when('I attempt to adjust clause "{clause}"')
def step_when_attempt_adjust_clause(context, clause):
    step_when_adjust_clause(context, clause)


@when('I initiate the approval process for contract "{name}"')
def step_when_initiate_approval(context, name):
    did, updated_at = _contract_data(context, name)
    context.requests_response = post_json(
        context,
        contract_submit_url(context),
        _contract_submit_payload(context, did, updated_at),
    )
    if context.requests_response.status_code == 200:
        _refresh_contract(context, name)


@when('I approve contract "{name}"')
def step_when_approve_contract(context, name):
    did, updated_at = _contract_data(context, name)
    context.requests_response = post_json(context, contract_approve_url(context), {"did": did, "updated_at": updated_at})
    if context.requests_response.status_code == 200:
        _refresh_contract(context, name)


@when('I reject contract "{name}" with reason "{reason}"')
def step_when_reject_contract(context, name, reason):
    did, updated_at = _contract_data(context, name)
    context.requests_response = post_json(
        context,
        contract_reject_url(context),
        {"did": did, "updated_at": updated_at, "reason": reason},
    )


@when('I access the approval interface for contract "{name}"')
def step_when_access_approval_interface(context, name):
    did, _ = _contract_data(context, name)
    context.requests_response = get_with_headers(context, contract_retrieve_by_id_url(context, did))


@when('I submit contract "{name}" for review')
def step_when_submit_contract_for_review(context, name):
    did, updated_at = _contract_data(context, name)
    context.requests_response = post_json(
        context,
        contract_submit_url(context),
        _contract_submit_payload(context, did, updated_at),
    )
    if context.requests_response.status_code == 200:
        _refresh_contract(context, name)


@when('I attempt to add a comment to contract "{name}"')
def step_when_attempt_comment_contract(context, name):
    did, updated_at = _contract_data(context, name)
    context.requests_response = post_json(
        context,
        contract_negotiate_url(context),
        {
            "did": did,
            "updated_at": updated_at,
            "negotiated_by": "bdd-observer",
            "change_request": "comment attempt",
        },
    )


@when('I attempt to approve contract "{name}"')
def step_when_attempt_approve_contract(context, name):
    step_when_approve_contract(context, name)
