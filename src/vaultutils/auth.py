import time
import webbrowser
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import Any, List, Optional
from playwright.sync_api import sync_playwright  # type: ignore
from hvac import Client, exceptions  # type: ignore
from vaultutils.utils import _extract_auth_url_params, _get_oidc_client_token
from vaultutils.config import Config

SELF_CLOSING_PAGE = """
<!doctype html>
<html>
<head>
<script>
// Closes IE, Edge, Chrome, Brave
window.onload = function load() {
  window.open("", "_self", "");
  window.close();
};
</script>
</head>
<body>
  <p>Authentication successful, you can close the browser now.</p>
  <script>
    // Needed for Firefox security
    setTimeout(function() {
          window.close()
    }, 5000);
  </script>
</body>
</html>
"""

# Global variable to store the token
global_token: Optional[str] = None

def get_stored_token() -> Optional[str]:
    global global_token
    return global_token

def store_token(token: str) -> None:
    global global_token
    global_token = token

def validate_token(client: Client, token: str) -> bool:
    client.token = token
    return client.is_authenticated()

def get_oidc_token(client: Client, oidc_callback_port: int = 8250) -> str:
    host = Config.VAULT_SERVER_HOST
    oidc_redirect_uri = f"http://{host}:{oidc_callback_port}/oidc/callback"

    try:
        auth_url_response = client.auth.oidc.oidc_authorization_url_request(
            role="default",
            redirect_uri=oidc_redirect_uri,
        )
        auth_url = auth_url_response.get("data", {}).get("auth_url", "")
        if not auth_url:
            raise ValueError("Authorization URL is empty")
    except Exception as error:
        raise ValueError(f"Error while getting OIDC authorization URL: {error}")

    print(f"Authorization URL: {auth_url}")

    auth_url_nonce, auth_url_state = _extract_auth_url_params(auth_url)

    trusted_uris = Config.NETWORK_NEGOTIATE_AUTH_TRUSTED_URIS
    delegation_uris = Config.NETWORK_NEGOTIATE_AUTH_DELEGATION_URIS

    token_holder: List[Any] = []

    server_thread = Thread(target=lambda: _start_local_http_server(oidc_callback_port, token_holder))
    server_thread.start()

    if Config.VAULT_OIDC_HEADLESS:
        time.sleep(3)
        with sync_playwright() as playwright:
            browser = playwright.firefox.launch(
                headless=True,
                firefox_user_prefs={
                    "network.negotiate-auth.trusted-uris": trusted_uris,
                    "network.negotiate-auth.delegation-uris": delegation_uris,
                }
            )
            page = browser.new_page()
            page.goto(auth_url)
            browser.close()
    else:
        webbrowser.open(auth_url)

    server_thread.join()

    if not token_holder:
        raise ValueError("OIDC token not received")

    token = token_holder[0]
    return _get_oidc_client_token(client, token, auth_url_nonce, auth_url_state)

def _start_local_http_server(oidc_callback_port: int, token_holder: List[Any]) -> None:
    class HttpServ(HTTPServer):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self.token = None

    class AuthHandler(BaseHTTPRequestHandler):
        token: str = ""
        def do_GET(self) :  # noqa: N802
            params = urllib.parse.parse_qs(self.path.split("?")[1])
            self.server.token = params["code"][0]
            token_holder.append(self.server.token)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str.encode(SELF_CLOSING_PAGE))

    server_address = ("", oidc_callback_port)
    httpd = HttpServ(server_address, AuthHandler)
    print(f"Starting local HTTP server at {server_address}")
    httpd.handle_request()

def login_vault(client: Client) -> None:
    if not client.url:
        raise KeyError("Vault URL not defined for vault client")

    token = get_stored_token()
    if token and validate_token(client, token):
        print("Using stored token for authentication.")
        return

    auth_method = Config.get_auth_method()

    if auth_method == "oidc":
        token = get_oidc_token(client)
        client.token = token
    elif auth_method == "token":
        client.token = Config.VAULT_TOKEN
    elif auth_method == "approle":
        client.auth.approle.login(role_id=Config.VAULT_ROLE_ID, secret_id=Config.VAULT_SECRET_ID)
    else:
        raise ValueError("No valid authentication method found.")

    if not client.is_authenticated():
        raise exceptions.VaultError("Vault authentication failed")

    store_token(client.token)
