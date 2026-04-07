#!/usr/bin/env bash

# DCS API root. Include API prefix if your server uses one.
# Examples:
# export BDD_DCS_BASE_URL="http://127.0.0.1:8991"
# export BDD_DCS_BASE_URL="http://127.0.0.1:8991/api"
# Helm chart default route path example:
# export BDD_DCS_BASE_URL="http://127.0.0.1:18991/digital-contracting-service/api"
export BDD_DCS_BASE_URL="http://127.0.0.1:8991"

# Optional token for positive-path scenarios.
# export BDD_DCS_TOKEN="<jwt-token>"

# Template DID used by the scenario name "Service Agreement Template".
# export BDD_TEMPLATE_DID_SERVICE_AGREEMENT_TEMPLATE="did:example:template:service-agreement"

# HTTP timeout in seconds.
export BDD_HTTP_TIMEOUT_SECONDS="20"
