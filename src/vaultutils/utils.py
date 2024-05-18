import urllib.parse
from hvac import Client  # type: ignore
from functools import wraps
from typing import Any, Dict, TypeVar

def _extract_auth_url_params(auth_url: str) -> tuple[str, str]:
    """
    Extract nonce and state from the authorization URL.

    Args:
        auth_url (str): The authorization URL.

    Returns:
        tuple[str, str]: The nonce and state values.
    """
    try:
        query_string = auth_url.split("?")[1]
        params = urllib.parse.parse_qs(query_string)
        auth_url_nonce = params["nonce"][0]
        auth_url_state = params["state"][0]
        return auth_url_nonce, auth_url_state
    except (IndexError, KeyError) as e:
        raise ValueError(f"Error parsing authorization URL: {auth_url}") from e

def _get_oidc_client_token(vault_client: Client, code: str, nonce: str, state: str) -> str:
    """
    Get OIDC client token from Vault using the authorization code.

    Args:
        vault_client (Client): Vault client.
        code (str): Authorization code.
        nonce (str): Nonce value.
        state (str): State value.

    Returns:
        str: The client token.
    """
    auth_result = vault_client.auth.oidc.oidc_callback(
        code=code,
        path="oidc",
        nonce=nonce,
        state=state,
    )
    client_token = auth_result["auth"]["client_token"]
    return client_token

T = TypeVar("T")

def singleton(cls: T) -> T:
    """
    Decorator to enforce singleton pattern on a class.
    """
    instances: Dict[T, T] = {}

    @wraps(cls)  # type: ignore
    def get_instance(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)  # type: ignore
        return instances[cls]

    return get_instance  # type: ignore
