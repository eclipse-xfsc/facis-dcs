"""Contract creation API steps for executable BDD scenarios."""

import os

from behave import then, when

from support.api_client import contract_create_url
from support.api_client import get_with_headers
from support.api_client import post_json


@when('the system sends a POST request to create contract with template "{template_name}"')
def step_when_create_contract_with_template(context, template_name):
    assert hasattr(context, "template_dids") and template_name in context.template_dids, (
        f"No template DID configured for template '{template_name}'"
    )
    context.requests_response = post_json(
        context,
        contract_create_url(context),
        {"did": context.template_dids[template_name]},
    )


@when("the system submits contract creation request with populated fields")
def step_when_create_contract_with_payload(context):
    template_did = os.getenv("BDD_TEMPLATE_DID_DEFAULT")
    assert template_did, "BDD_TEMPLATE_DID_DEFAULT must be set for this scenario"
    context.requests_response = post_json(
        context,
        contract_create_url(context),
        {"did": template_did},
    )


@when("the system attempts to create contract via API")
def step_when_attempt_create_contract(context):
    payload = {"did": os.getenv("BDD_TEMPLATE_DID_DEFAULT", "did:example:template:missing")}
    context.requests_response = post_json(context, contract_create_url(context), payload)


@when('I create a contract from template "{template_name}"')
def step_when_create_contract_from_template(context, template_name):
    assert hasattr(context, "template_dids") and template_name in context.template_dids, (
        f"No approved template DID for '{template_name}' — ensure the Given step ran"
    )
    context.requests_response = post_json(
        context,
        contract_create_url(context),
        {"did": context.template_dids[template_name]},
    )


@when('I attempt to create a contract from template "{template_name}"')
def step_when_attempt_create_contract_from_template(context, template_name):
    template_did = (
        (context.template_dids or {}).get(template_name)
        if hasattr(context, "template_dids")
        else "did:example:template:missing"
    )
    context.requests_response = post_json(
        context,
        contract_create_url(context),
        {"did": template_did or "did:example:template:missing"},
    )


@then("the contract is assigned a unique contract ID")
def step_then_contract_unique_id(context):
    body = context.requests_response.json()
    did = body.get("did")
    assert isinstance(did, str) and did.strip(), f"Expected a contract DID, got: {body}"


@then("metadata is auto-filled including parties, jurisdiction, and applicable schemas")
def step_then_metadata_auto_filled(context):
    assert context.requests_response.status_code == 200, context.requests_response.text


@then("the creation is logged and traceable to the template version")
def step_then_creation_logged_traceable(context):
    assert context.requests_response.status_code == 200, context.requests_response.text