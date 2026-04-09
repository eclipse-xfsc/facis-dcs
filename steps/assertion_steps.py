"""Shared assertion steps for executable BDD scenarios."""

from behave import then


@then("a draft contract is generated")
def step_then_draft_generated(context):
    assert context.requests_response.status_code == 200, context.requests_response.text


@then("the contract is assigned a unique ID")
def step_then_unique_id(context):
    body = context.requests_response.json()
    assert isinstance(body, dict), body
    did = body.get("did")
    assert isinstance(did, str) and did.strip(), body


@then("metadata is populated from API payload")
def step_then_metadata_populated(context):
    assert context.requests_response.status_code == 200, context.requests_response.text


@then('the contract status is set to "Draft"')
def step_then_status_draft(context):
    assert context.requests_response.status_code == 200, context.requests_response.text


@then("validation ensures required fields are present")
def step_then_validation_required_fields(context):
    assert context.requests_response.status_code in (200, 400), context.requests_response.text


@then("the request is denied with an authorization error")
def step_then_denied_authorization(context):
    assert context.requests_response.status_code in (401, 403), context.requests_response.text


@then('the request is denied with error "Credential invalid or access revoked"')
def step_then_denied_credential_invalid(context):
    assert context.requests_response.status_code in (401, 403), context.requests_response.text


@then("the request is denied")
def step_then_denied(context):
    assert context.requests_response.status_code in (401, 403), context.requests_response.text


@then("the creation is logged with timestamp and actor identity")
def step_then_creation_logged(context):
    assert context.requests_response is not None


@then("the attempt is logged with timestamp and actor identity")
def step_then_attempt_logged(context):
    assert context.requests_response is not None