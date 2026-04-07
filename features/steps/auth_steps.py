"""Authentication and scenario setup steps for executable BDD scenarios."""

import os
import re

from behave import given

from support.keycloak_client import admin_token
from support.keycloak_client import assign_client_role
from support.keycloak_client import ensure_client
from support.keycloak_client import ensure_client_role
from support.keycloak_client import ensure_user
from support.keycloak_client import user_token
from support.template_utils import template_env_key


@given('I am authenticated with role "{role}"')
def step_given_authenticated_with_role(context, role):
    client_id = os.getenv("BDD_KEYCLOAK_CLIENT_ID", "digital-contracting-service")
    role_safe = re.sub(r"[^A-Za-z0-9]+", "-", role.lower()).strip("-")
    username = f"bdd-{role_safe}"
    password = os.getenv("BDD_KEYCLOAK_TEST_USER_PASSWORD", "bdd-pass-123")

    admin_access_token = admin_token()
    client_uuid = ensure_client(admin_access_token, client_id)
    role_repr = ensure_client_role(admin_access_token, client_uuid, role)
    user_id = ensure_user(admin_access_token, username, password)
    assign_client_role(admin_access_token, user_id, client_uuid, role_repr)

    token = user_token(client_id, username, password)
    context.headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


@given("a system service is authenticated via API")
def step_given_authenticated_service(context):
    token = os.getenv("BDD_DCS_TOKEN")
    assert token, "BDD_DCS_TOKEN must be set for authenticated API scenarios"
    context.headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


@given("a system service provides an invalid API key")
def step_given_invalid_api_key(context):
    context.headers = {
        "Authorization": "Bearer invalid-token",
        "Content-Type": "application/json",
    }


@given('template "{template_name}" is available')
def step_given_template_available(context, template_name):
    env_key = template_env_key(template_name)
    template_did = os.getenv(env_key)
    assert template_did, f"Missing template DID env var: {env_key}"
    if not hasattr(context, "template_dids"):
        context.template_dids = {}
    context.template_dids[template_name] = template_did


@given("the service provides contract data in the request payload")
def step_given_payload_data(context):
    context.contract_payload_extra = {"source": "bdd"}