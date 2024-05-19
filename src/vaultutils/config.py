import os


class Config:
    VAULT_URL = os.getenv("VAULT_URL", "http://localhost:8200")
    VAULT_MOUNT_POINT = os.getenv("VAULT_MOUNT_POINT", "secret")
    VAULT_OIDC_HEADLESS = os.getenv("VAULT_OIDC_HEADLESS", "false").lower() == "true"
    VAULT_OIDC_AUTH = os.getenv("VAULT_OIDC_AUTH", "true").lower() == "true"
    VAULT_ROLE_ID = os.getenv("VAULT_ROLE_ID")
    VAULT_SECRET_ID = os.getenv("VAULT_SECRET_ID")
    VAULT_TOKEN = os.getenv("VAULT_TOKEN")
    VAULT_SERVER_HOST = os.getenv("VAULT_SERVER_HOST", "localhost")
    VAULT_SERVER_PORT = int(os.getenv("VAULT_SERVER_PORT", "8001"))
    NETWORK_NEGOTIATE_AUTH_TRUSTED_URIS = os.getenv(
        "NETWORK_NEGOTIATE_AUTH_TRUSTED_URIS", ".myorg.com"
    )
    NETWORK_NEGOTIATE_AUTH_DELEGATION_URIS = os.getenv(
        "NETWORK_NEGOTIATE_AUTH_DELEGATION_URIS", ".myorg.com"
    )
    VAULT_AUTH_METHOD = os.getenv("VAULT_AUTH_METHOD")

    @classmethod
    def get_auth_method(cls):
        if cls.VAULT_AUTH_METHOD:
            return cls.VAULT_AUTH_METHOD
        if cls.VAULT_TOKEN:
            return "token"
        elif cls.VAULT_ROLE_ID and cls.VAULT_SECRET_ID:
            return "approle"
        elif cls.VAULT_OIDC_AUTH or cls.VAULT_OIDC_HEADLESS:
            return "oidc"
        else:
            err_msg: str = "No valid authentication method found. Please set the appropriate environment variables."
            raise ValueError(err_msg)
