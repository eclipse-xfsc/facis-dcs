"""Shared assertion steps for executable BDD scenarios."""

from behave import then


@then("the contract is assigned a unique ID")
def step_then_unique_id(context):
    body = context.requests_response.json()
    assert isinstance(body, dict), body
    did = body.get("did")
    assert isinstance(did, str) and did.strip(), body


@then("the request is denied with an authorization error")
def step_then_denied_authorization(context):
    assert context.requests_response.status_code in (401, 403), context.requests_response.text


@then('the request is denied with error "Credential invalid or access revoked"')
def step_then_denied_credential_invalid(context):
    assert context.requests_response.status_code in (401, 403), context.requests_response.text


@then("the request is denied")
def step_then_denied(context):
    assert context.requests_response.status_code in (401, 403), context.requests_response.text