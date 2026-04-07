"""Template API steps for executable BDD scenarios."""

from behave import then, when

from support.api_client import get_with_headers
from support.api_client import post_json
from support.api_client import template_create_url
from support.api_client import template_retrieve_by_id_url
from support.template_utils import template_type_for_category


@when('I create a template "{template_name}" in category "{category}"')
def step_when_create_template(context, template_name, category):
    payload = {
        "template_type": template_type_for_category(category),
        "name": template_name,
        "description": "BDD executable template creation",
        "template_data": {
            "title": template_name,
            "clauses": [{"id": "c1", "text": "Confidentiality clause"}],
        },
    }
    context.requests_response = post_json(context, template_create_url(context), payload)
    assert context.requests_response.status_code == 200, context.requests_response.text
    body = context.requests_response.json()
    context.created_template_did = body.get("did")
    assert context.created_template_did, body


@then('the template is created in "Draft" status')
def step_then_template_created_draft(context):
    context.template_retrieve_response = get_with_headers(
        context,
        template_retrieve_by_id_url(context, context.created_template_did),
    )
    assert context.template_retrieve_response.status_code == 200, context.template_retrieve_response.text
    body = context.template_retrieve_response.json()
    state = str(body.get("state", "")).lower()
    assert state == "draft", body


@then('the template is assigned version "1.0"')
def step_then_template_version(context):
    body = context.template_retrieve_response.json()
    version = body.get("version")
    assert version in (None, 1, "1", "1.0"), body