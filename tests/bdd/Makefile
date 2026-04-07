SHELL := /bin/bash -eu -o pipefail

PYTHON ?= python3
VENV_PATH ?= .venv
BDD_EXECUTOR_REPO ?= https://github.com/eclipse-xfsc/bdd-executor.git
BDD_EXECUTOR_PATH ?= .tmp/bdd-executor
FEATURES_PATH ?= ../../features
TAGS ?= @executable
ARG_BDD ?=
K8S_NAMESPACE ?= default
HELM_RELEASE ?= dcs
DCS_SERVICE ?= $(HELM_RELEASE)-digital-contracting-service
DCS_DEPLOYMENT ?= $(DCS_SERVICE)
LOCAL_FORWARD_PORT ?= 18991
SERVICE_PORT ?= 8991
DCS_API_BASE_PATH ?= /digital-contracting-service/api
ENABLE_KEYCLOAK_PORT_FORWARD ?= false
KEYCLOAK_SERVICE ?= $(HELM_RELEASE)-keycloak
KEYCLOAK_DEPLOYMENT ?= $(KEYCLOAK_SERVICE)
KEYCLOAK_SERVICE_PORT ?= 8080
KEYCLOAK_LOCAL_FORWARD_PORT ?= 18080
BDD_KEYCLOAK_REALM ?= master
HELM_CHART_PATH ?= ../../deployment
HELM_TIMEOUT ?= 20m

KIND_CLUSTER_NAME ?= dcs-bdd
KIND_WAIT ?= 120s
DOCKER_IMAGE_REPOSITORY ?= digital-contracting-service
DOCKER_IMAGE_TAG ?= bdd
DOCKER_IMAGE ?= $(DOCKER_IMAGE_REPOSITORY):$(DOCKER_IMAGE_TAG)
KIND_NAMESPACE ?= dcs-bdd
KIND_HELM_VALUES ?=
KIND_HELM_SET ?=
LOCAL_BIN ?= .tmp/bin
KIND_VERSION ?= v0.23.0
KIND_BIN ?= $(LOCAL_BIN)/kind
KUBECTL_VERSION ?= v1.30.2
KUBECTL_BIN ?= $(LOCAL_BIN)/kubectl
HELM_VERSION ?= v3.15.2
HELM_BIN ?= $(LOCAL_BIN)/helm
BDD_RUNNER_SCRIPT ?= scripts/run_bdd_helm.sh

.PHONY: setup_dev run_bdd_dev run_bdd_all run_bdd_helm_dev run_bdd_helm_all ensure_kind ensure_kubectl ensure_helm ensure_k8s_tools kind_create kind_delete kind_load_image kind_deploy kind_uninstall run_bdd_kind_dev run_bdd_kind_all run_bdd_kind_ci build_dcs_image clean help

help:
	@echo "make setup_dev    # Create venv and install bdd-executor"
	@echo "make run_bdd_dev  # Run tagged executable BDD scenarios"
	@echo "make run_bdd_all  # Run all BDD scenarios"
	@echo "make run_bdd_helm_dev # Port-forward Helm service and run tagged scenarios"
	@echo "make run_bdd_helm_all # Port-forward Helm service and run all scenarios"
	@echo "make run_bdd_kind_dev # Build ephemeral kind+Helm stack and run tagged scenarios"
	@echo "make run_bdd_kind_all # Build ephemeral kind+Helm stack and run all scenarios"
	@echo "make ensure_kind     # Install local kind binary when missing"
	@echo "make ensure_k8s_tools # Install local kubectl/helm binaries when missing"
	@echo "make kind_delete     # Delete kind cluster used for BDD"
	@echo "make clean        # Remove local test artifacts"

$(BDD_EXECUTOR_PATH):
	mkdir -p .tmp
	if [[ ! -d "$(BDD_EXECUTOR_PATH)/.git" ]]; then \
		git clone --depth 1 "$(BDD_EXECUTOR_REPO)" "$(BDD_EXECUTOR_PATH)"; \
	fi

setup_dev: $(BDD_EXECUTOR_PATH)
	@if [[ -f "$(VENV_PATH)/bin/pip" ]] && ! "$(VENV_PATH)/bin/pip" --version >/dev/null 2>&1; then \
		echo "Existing virtualenv at $(VENV_PATH) is not usable in this environment; recreating"; \
		rm -rf "$(VENV_PATH)"; \
	fi
	@if [[ ! -f "$(VENV_PATH)/bin/activate" ]]; then \
		$(PYTHON) -m venv "$(VENV_PATH)"; \
	fi
	"$(VENV_PATH)/bin/pip" install --upgrade pip wheel
	"$(VENV_PATH)/bin/pip" install -e "$(BDD_EXECUTOR_PATH)[dev]"

run_bdd_dev: setup_dev
	source "$(VENV_PATH)/bin/activate" && \
	mkdir -p .reports/junit && \
	behave "$(FEATURES_PATH)" -t "$(TAGS)" --junit --junit-directory .reports/junit $(ARG_BDD)

run_bdd_all: setup_dev
	source "$(VENV_PATH)/bin/activate" && \
	mkdir -p .reports/junit && \
	behave "$(FEATURES_PATH)" --junit --junit-directory .reports/junit $(ARG_BDD)

run_bdd_helm_dev: setup_dev ensure_k8s_tools
	@VENV_PATH="$(VENV_PATH)" \
		FEATURES_PATH="$(FEATURES_PATH)" \
		KUBECTL_BIN="$(KUBECTL_BIN)" \
		K8S_NAMESPACE="$(K8S_NAMESPACE)" \
		DCS_DEPLOYMENT="$(DCS_DEPLOYMENT)" \
		DCS_SERVICE="$(DCS_SERVICE)" \
		LOCAL_FORWARD_PORT="$(LOCAL_FORWARD_PORT)" \
		SERVICE_PORT="$(SERVICE_PORT)" \
		DCS_API_BASE_PATH="$(DCS_API_BASE_PATH)" \
		KEYCLOAK_SERVICE="$(KEYCLOAK_SERVICE)" \
		KEYCLOAK_DEPLOYMENT="$(KEYCLOAK_DEPLOYMENT)" \
		KEYCLOAK_LOCAL_FORWARD_PORT="$(KEYCLOAK_LOCAL_FORWARD_PORT)" \
		KEYCLOAK_SERVICE_PORT="$(KEYCLOAK_SERVICE_PORT)" \
		BDD_KEYCLOAK_REALM="$(BDD_KEYCLOAK_REALM)" \
		ENABLE_KEYCLOAK_PORT_FORWARD="$(ENABLE_KEYCLOAK_PORT_FORWARD)" \
		BDD_RUN_MODE=dev \
		TAGS="$(TAGS)" \
		ARG_BDD="$(ARG_BDD)" \
		bash "$(BDD_RUNNER_SCRIPT)"

run_bdd_helm_all: setup_dev ensure_k8s_tools
	@VENV_PATH="$(VENV_PATH)" \
		FEATURES_PATH="$(FEATURES_PATH)" \
		KUBECTL_BIN="$(KUBECTL_BIN)" \
		K8S_NAMESPACE="$(K8S_NAMESPACE)" \
		DCS_DEPLOYMENT="$(DCS_DEPLOYMENT)" \
		DCS_SERVICE="$(DCS_SERVICE)" \
		LOCAL_FORWARD_PORT="$(LOCAL_FORWARD_PORT)" \
		SERVICE_PORT="$(SERVICE_PORT)" \
		DCS_API_BASE_PATH="$(DCS_API_BASE_PATH)" \
		KEYCLOAK_SERVICE="$(KEYCLOAK_SERVICE)" \
		KEYCLOAK_DEPLOYMENT="$(KEYCLOAK_DEPLOYMENT)" \
		KEYCLOAK_LOCAL_FORWARD_PORT="$(KEYCLOAK_LOCAL_FORWARD_PORT)" \
		KEYCLOAK_SERVICE_PORT="$(KEYCLOAK_SERVICE_PORT)" \
		BDD_KEYCLOAK_REALM="$(BDD_KEYCLOAK_REALM)" \
		ENABLE_KEYCLOAK_PORT_FORWARD="$(ENABLE_KEYCLOAK_PORT_FORWARD)" \
		BDD_RUN_MODE=all \
		ARG_BDD="$(ARG_BDD)" \
		bash "$(BDD_RUNNER_SCRIPT)"

build_dcs_image:
	@docker build -f ../../backend/Dockerfile -t "$(DOCKER_IMAGE)" ../..

ensure_kind:
	@mkdir -p "$(LOCAL_BIN)"
	@if [[ -x "$(KIND_BIN)" ]]; then \
		echo "Using cached kind binary: $(KIND_BIN)"; \
	elif command -v kind >/dev/null 2>&1; then \
		echo "Using system kind: $$(command -v kind)"; \
		ln -sf "$$(command -v kind)" "$(KIND_BIN)"; \
	else \
		if ! command -v curl >/dev/null 2>&1; then \
			echo "curl is required to download kind"; \
			exit 1; \
		fi; \
		OS="$$(uname | tr '[:upper:]' '[:lower:]')"; \
		ARCH_RAW="$$(uname -m)"; \
		case "$$ARCH_RAW" in \
			x86_64) ARCH=amd64 ;; \
			aarch64|arm64) ARCH=arm64 ;; \
			*) echo "Unsupported architecture for kind: $$ARCH_RAW"; exit 1 ;; \
		esac; \
		URL="https://kind.sigs.k8s.io/dl/$(KIND_VERSION)/kind-$$OS-$$ARCH"; \
		echo "Downloading kind $(KIND_VERSION) from $$URL"; \
		curl -fsSL "$$URL" -o "$(KIND_BIN)"; \
		chmod +x "$(KIND_BIN)"; \
	fi

ensure_kubectl:
	@mkdir -p "$(LOCAL_BIN)"
	@if [[ -x "$(KUBECTL_BIN)" ]]; then \
		echo "Using cached kubectl binary: $(KUBECTL_BIN)"; \
	elif command -v kubectl >/dev/null 2>&1; then \
		echo "Using system kubectl: $$(command -v kubectl)"; \
		ln -sf "$$(command -v kubectl)" "$(KUBECTL_BIN)"; \
	else \
		if ! command -v curl >/dev/null 2>&1; then \
			echo "curl is required to download kubectl"; \
			exit 1; \
		fi; \
		OS="$$(uname | tr '[:upper:]' '[:lower:]')"; \
		ARCH_RAW="$$(uname -m)"; \
		case "$$ARCH_RAW" in \
			x86_64) ARCH=amd64 ;; \
			aarch64|arm64) ARCH=arm64 ;; \
			*) echo "Unsupported architecture for kubectl: $$ARCH_RAW"; exit 1 ;; \
		esac; \
		URL="https://dl.k8s.io/release/$(KUBECTL_VERSION)/bin/$$OS/$$ARCH/kubectl"; \
		echo "Downloading kubectl $(KUBECTL_VERSION) from $$URL"; \
		curl -fsSL "$$URL" -o "$(KUBECTL_BIN)"; \
		chmod +x "$(KUBECTL_BIN)"; \
	fi

ensure_helm:
	@mkdir -p "$(LOCAL_BIN)" .tmp
	@if [[ -x "$(HELM_BIN)" ]]; then \
		echo "Using cached helm binary: $(HELM_BIN)"; \
	elif command -v helm >/dev/null 2>&1; then \
		echo "Using system helm: $$(command -v helm)"; \
		ln -sf "$$(command -v helm)" "$(HELM_BIN)"; \
	else \
		if ! command -v curl >/dev/null 2>&1; then \
			echo "curl is required to download helm"; \
			exit 1; \
		fi; \
		OS="$$(uname | tr '[:upper:]' '[:lower:]')"; \
		ARCH_RAW="$$(uname -m)"; \
		case "$$ARCH_RAW" in \
			x86_64) ARCH=amd64 ;; \
			aarch64|arm64) ARCH=arm64 ;; \
			*) echo "Unsupported architecture for helm: $$ARCH_RAW"; exit 1 ;; \
		esac; \
		ARCHIVE="helm-$(HELM_VERSION)-$$OS-$$ARCH.tar.gz"; \
		URL="https://get.helm.sh/$$ARCHIVE"; \
		echo "Downloading helm $(HELM_VERSION) from $$URL"; \
		curl -fsSL "$$URL" -o ".tmp/$$ARCHIVE"; \
		tar -xzf ".tmp/$$ARCHIVE" -C .tmp; \
		cp ".tmp/$$OS-$$ARCH/helm" "$(HELM_BIN)"; \
		chmod +x "$(HELM_BIN)"; \
	fi

ensure_k8s_tools: ensure_kubectl ensure_helm

kind_create: ensure_kind ensure_k8s_tools
	@if ! "$(KIND_BIN)" get clusters | grep -qx "$(KIND_CLUSTER_NAME)"; then \
		"$(KIND_BIN)" create cluster --name "$(KIND_CLUSTER_NAME)" --wait "$(KIND_WAIT)"; \
	else \
		echo "kind cluster $(KIND_CLUSTER_NAME) already exists"; \
	fi

kind_delete: ensure_kind
	@if "$(KIND_BIN)" get clusters | grep -qx "$(KIND_CLUSTER_NAME)"; then \
		"$(KIND_BIN)" delete cluster --name "$(KIND_CLUSTER_NAME)"; \
	else \
		echo "kind cluster $(KIND_CLUSTER_NAME) does not exist"; \
	fi

kind_load_image: kind_create
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "docker is required to load $(DOCKER_IMAGE) into kind"; \
		exit 1; \
	fi
	@docker image inspect "$(DOCKER_IMAGE)" >/dev/null 2>&1 || (echo "Missing local image $(DOCKER_IMAGE). Build it first." && exit 1)
	@"$(KIND_BIN)" load docker-image "$(DOCKER_IMAGE)" --name "$(KIND_CLUSTER_NAME)"

kind_deploy: kind_load_image
	@"$(HELM_BIN)" dependency build "$(HELM_CHART_PATH)"
	@if ! "$(HELM_BIN)" upgrade --install "$(HELM_RELEASE)" "$(HELM_CHART_PATH)" \
		--namespace "$(KIND_NAMESPACE)" \
		--create-namespace \
		--wait \
		--timeout "$(HELM_TIMEOUT)" \
		--set image.repository="$(DOCKER_IMAGE_REPOSITORY)" \
		--set image.tag="$(DOCKER_IMAGE_TAG)" \
		--set postgresql.enabled=true \
		--set keycloak.enabled=true \
		--set keycloak.extraEnvVars[0].name=KC_HOSTNAME \
		--set keycloak.extraEnvVars[0].value="$(HELM_RELEASE)-keycloak" \
		--set keycloak.extraEnvVars[1].name=KC_HOSTNAME_PORT \
		--set keycloak.extraEnvVars[1].value="8080" \
		--set keycloak.extraEnvVars[2].name=KC_HOSTNAME_STRICT \
		--set keycloak.extraEnvVars[2].value="false" \
		--set nats.enabled=true \
		--set oidc.issuerURL="http://$(HELM_RELEASE)-keycloak:8080/realms/master" \
		--set oidc.clientID="digital-contracting-service" \
		--set route.basePath="/digital-contracting-service" \
		$(KIND_HELM_VALUES) \
		$(KIND_HELM_SET); then \
		echo "=== PODS ==="; \
		"$(KUBECTL_BIN)" get pods -n "$(KIND_NAMESPACE)" -o wide || true; \
		echo "=== DEPLOYMENTS ==="; \
		"$(KUBECTL_BIN)" get deployments -n "$(KIND_NAMESPACE)" || true; \
		echo "=== EVENTS ==="; \
		"$(KUBECTL_BIN)" get events -n "$(KIND_NAMESPACE)" --sort-by=.lastTimestamp || true; \
		echo "=== DCS LOGS ==="; \
		"$(KUBECTL_BIN)" logs deployment/$(DCS_DEPLOYMENT) -n "$(KIND_NAMESPACE)" --tail=200 || true; \
		echo "=== KEYCLOAK LOGS ==="; \
		"$(KUBECTL_BIN)" logs deployment/$(HELM_RELEASE)-keycloak -n "$(KIND_NAMESPACE)" --tail=200 || true; \
		exit 1; \
	fi

kind_uninstall:
	@"$(HELM_BIN)" uninstall "$(HELM_RELEASE)" --namespace "$(KIND_NAMESPACE)" >/dev/null 2>&1 || true

run_bdd_kind_dev: kind_deploy
	@$(MAKE) run_bdd_helm_dev \
		K8S_NAMESPACE="$(KIND_NAMESPACE)" \
		HELM_RELEASE="$(HELM_RELEASE)" \
		ENABLE_KEYCLOAK_PORT_FORWARD=true

run_bdd_kind_all: kind_deploy
	@$(MAKE) run_bdd_helm_all \
		K8S_NAMESPACE="$(KIND_NAMESPACE)" \
		HELM_RELEASE="$(HELM_RELEASE)" \
		ENABLE_KEYCLOAK_PORT_FORWARD=true

run_bdd_kind_ci: build_dcs_image run_bdd_kind_dev

clean:
	rm -rf "$(VENV_PATH)" .tmp .reports
