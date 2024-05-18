# Project-specific variables
PROJECT_NAME=vaultutils
VERSION=0.0.1
WHEEL_FILE=dist/$(PROJECT_NAME)-$(VERSION)-py3-none-any.whl

# Define environment variables with default values if not set
VAULT_URL ?= http://localhost:8200
VAULT_MOUNT_POINT ?= secret
VAULT_AUTH_METHOD ?= oidc
VAULT_OIDC_HEADLESS ?= true
VAULT_OIDC_AUTH ?= true
VAULT_ROLE_ID ?= your-role-id
VAULT_SECRET_ID ?= your-secret-id
VAULT_TOKEN ?= your-vault-token
VAULT_SERVER_HOST ?= localhost
VAULT_SERVER_PORT ?= 8001
NETWORK_NEGOTIATE_AUTH_TRUSTED_URIS ?= .myorg.com
NETWORK_NEGOTIATE_AUTH_DELEGATION_URIS ?= .myorg.com

export VAULT_URL
export VAULT_MOUNT_POINT
export VAULT_AUTH_METHOD
export VAULT_OIDC_HEADLESS
export VAULT_OIDC_AUTH
export VAULT_ROLE_ID
export VAULT_SECRET_ID
export VAULT_TOKEN
export VAULT_SERVER_HOST
export VAULT_SERVER_PORT
export NETWORK_NEGOTIATE_AUTH_TRUSTED_URIS
export NETWORK_NEGOTIATE_AUTH_DELEGATION_URIS

MAKE_TESTS ?= ""
MAKE_PYTEST_ARGS ?=

# Targets
.PHONY: auth setup start fetch clean build install uninstall full stop test

test:
	pytest --capture=tee-sys ${MAKE_PYTEST_ARGS} ${MAKE_TESTS}

setup:
	@echo "Setting up the project..."
	@vaultutils setup

start:
	@echo "Starting the Vault Manager server..."
	@vaultutils start

auth:
	@echo "Authenticating the Vault server..."
	@vaultutils authenticate

fetch:
	@echo "Fetching secret from Vault..."
	@vaultutils fetch-secret your-path your-key

clean:
	@echo "Cleaning up build artifacts..."
	@hatch clean
	@rm -rf dist/
	@rm -rf build/
	@rm -rf $(PROJECT_NAME).egg-info

build: clean
	@echo "Building the project..."
	@hatch build

uninstall:
	@echo "Uninstalling the project..."
	@pip uninstall -y $(PROJECT_NAME)

install: build
	@echo "Installing the project from wheel..."
	@VERSION=$$(hatch version); \
	WHEEL_FILE=dist/$(PROJECT_NAME)-$$VERSION-py3-none-any.whl; \
	pip install $$WHEEL_FILE

stop:
	@echo "Stopping the Vault Manager server..."
	@vaultutils stop

full: uninstall build install setup start
	@echo "Full process completed successfully."
