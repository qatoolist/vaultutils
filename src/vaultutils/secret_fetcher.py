from typing import Any, Optional

from cachetools import TTLCache
from hvac import Client  # type: ignore

from vaultutils.auth import login_vault
from vaultutils.config import Config
from vaultutils.utils import singleton


@singleton
class VaultSecretFetcher:
    """
    A class to fetch secrets from Vault and cache them using an in-memory cache.
    """

    def __init__(self):
        """
        Initialize the VaultSecretFetcher.
        """
        self.client = Client(url=Config.VAULT_URL)
        self.mount_point = Config.VAULT_MOUNT_POINT
        self.cache = TTLCache(
            maxsize=100, ttl=300
        )  # Cache with max size 100 and TTL 300 seconds

    def fetch_secret(self, path: str, key: Optional[str] = None) -> Any:
        """
        Fetch a secret from Vault.

        Args:
            path (str): The path of the secret.
            key (Optional[str]): The specific key within the secret.

        Returns:
            Any: The secret value.

        Raises:
            KeyError: If the key is not found in the secret.
        """
        if path not in self.cache:
            login_vault(self.client)
            self.cache[path] = self._fetch_secret_from_vault(path)

        secrets = self.cache[path]

        if key:
            if key in secrets:
                return secrets[key]
            else:
                err_msg: str = f"Key {key} not found in path {path}"
                raise KeyError(err_msg)
        else:
            return secrets

    def _fetch_secret_from_vault(self, path: str) -> dict:
        """
        Fetch a secret from Vault directly.

        Args:
            path (str): The path of the secret.

        Returns:
            dict: The secret data.
        """
        data = self.client.secrets.kv.read_secret_version(
            path=path, mount_point=self.mount_point
        )
        return data["data"]["data"]
