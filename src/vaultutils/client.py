import subprocess
from http import HTTPStatus
from typing import Any, Optional

import requests

from vaultutils.server import start_server, stop_server


class VaultManagerClient:
    def __init__(self, host: str = "localhost", port: int = 8001) -> None:
        self.base_url = f"http://{host}:{port}"

    def setup(self) -> None:
        """Setup Playwright."""
        subprocess.run(["playwright", "install"], check=True)

    def start(self) -> None:
        """Start the Vault Manager server."""
        start_server()

    def stop(self) -> None:
        """Stop the Vault Manager server."""
        stop_server()

    def authenticate(self) -> str:
        """Authenticate with Vault using environment variables."""
        response = requests.post(f"{self.base_url}/authenticate", timeout=10)
        if response.status_code == HTTPStatus.OK:
            return response.json()["token"]
        else:
            err_msg: str = (
                f"Error during authentication: {response.status_code} - {response.text}"
            )
            raise Exception(err_msg)

    def fetch_secret(self, path: str, key: Optional[str] = None) -> dict[str, Any]:
        """Fetch a secret from Vault."""
        response = requests.post(
            f"{self.base_url}/fetch-secret", json={"path": path, "key": key}, timeout=10
        )
        return response.json()
