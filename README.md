# vaultutils

<p align="center"><img src="/logo/vaultutils.png" alt="vaultutils. logo"></p>

[![PyPI - Version](https://img.shields.io/pypi/v/vaultutils.svg)](https://pypi.org/project/vaultutils)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vaultutils.svg)](https://pypi.org/project/vaultutils)

`vaultutils` is a Python package designed for efficient Vault authentication and secret fetching. It provides a flexible and powerful way to interact with HashiCorp Vault, supporting various authentication methods including OIDC, token-based, and AppRole authentication. The package also includes a built-in Flask server for managing Vault secrets and a CLI for easy interaction.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [CLI](#cli)
  - [Client](#client)
- [API Endpoints](#api-endpoints)
- [Development](#development)
  - [Testing](#testing)
- [Releasing](#releasing)
- [License](#license)

## Installation

You can install the `vaultutils` package using `pip`:

```bash
pip install vaultutils
```

## Configuration

`vaultutils` relies on environment variables for configuration. The following variables can be set to customize the behavior of the package:

- `VAULT_URL`: The URL of the Vault server (default: `http://localhost:8200`).
- `VAULT_MOUNT_POINT`: The mount point of the secrets engine (default: `secret`).
- `VAULT_OIDC_HEADLESS`: Enable headless OIDC authentication (default: `false`).
- `VAULT_OIDC_AUTH`: Enable OIDC authentication (default: `true`).
- `VAULT_ROLE_ID`: The AppRole role ID.
- `VAULT_SECRET_ID`: The AppRole secret ID.
- `VAULT_TOKEN`: The Vault token for token-based authentication.
- `VAULT_SERVER_HOST`: The host for the Flask server (default: `localhost`).
- `VAULT_SERVER_PORT`: The port for the Flask server (default: `8001`).
- `NETWORK_NEGOTIATE_AUTH_TRUSTED_URIS`: Trusted URIs for network negotiate auth (default: `.myorg.com`).
- `NETWORK_NEGOTIATE_AUTH_DELEGATION_URIS`: Delegation URIs for network negotiate auth (default: `.myorg.com`).
- `VAULT_AUTH_METHOD`: Explicitly specify the authentication method (`oidc`, `token`, `approle`).

## Usage

### CLI

The `vaultutils` package provides a command-line interface for easy interaction with Vault. The CLI supports various commands such as `setup`, `start`, `stop`, `fetch_secret`, and `authenticate`.

#### Setup

To install the necessary dependencies for headless browser automation:

```bash
vaultutils setup
```

#### Start the Server

To start the Flask server:

```bash
vaultutils start
```

#### Stop the Server

To stop the Flask server:

```bash
vaultutils stop
```

#### Authenticate with Vault

To authenticate with Vault:

```bash
vaultutils authenticate
```

#### Fetch a Secret

To fetch a secret from Vault:

```bash
vaultutils fetch_secret <path> [key]
```

### Client

The `VaultManagerClient` class allows you to interact with the Vault server programmatically.

```python
from vaultutils.client import VaultManagerClient

client = VaultManagerClient()

# Setup Playwright
client.setup()

# Start the server
client.start()

# Authenticate with Vault
token = client.authenticate()

# Fetch a secret
secret = client.fetch_secret("secret/path", "secret_key")

# Stop the server
client.stop()
```

## API Endpoints

The Flask server provides several endpoints for managing Vault secrets.

- `POST /authenticate`: Authenticate with Vault using environment variables.
- `POST /fetch-secret`: Fetch a secret from Vault. Requires JSON payload with `path` and optional `key`.
- `POST /shutdown`: Shutdown the Flask server.

## Development

### Makefile

A `Makefile` is provided to simplify development tasks.

### Testing

The `vaultutils` package includes a comprehensive set of unit tests using `pytest`. To run the tests:

1. Install the development dependencies:

```bash
make full
```

2. Run the tests using `pytest`:

```bash
make test
```

### Releasing

The project uses calendar-based version tags in the form `v<dd.mm.yy>.<n>` where `n` is the release number for the day. To
cut a new release:

```bash
make release
```

This command updates the version, creates a tag and pushes it to GitHub. A
workflow then builds the project and uploads the artifacts to PyPI using the
repository's `PYPI_TOKEN` secret.

## License

`vaultutils` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
