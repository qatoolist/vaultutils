import os
import signal
from typing import Any, Tuple
from hvac import Client  # type: ignore
from flask import jsonify, request  # type: ignore
from vaultutils.secret_fetcher import VaultSecretFetcher
from vaultutils.auth import login_vault
from vaultutils.config import Config
from threading import Lock, Thread

vault_secret_fetcher = VaultSecretFetcher()
lock = Lock()

class VaultController:
    @staticmethod
    def authenticate()-> Tuple[dict[str, Any], int]:
        client = Client(url=Config.VAULT_URL)
        if not client.url:
            return jsonify({"error": "Vault URL not defined"}), 400

        try:
            with lock:
                login_vault(client)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return jsonify({"token": client.token})

    @staticmethod
    def fetch_secret()-> Tuple[dict[str, Any], int]:
        path = request.json["path"]
        key = request.json.get("key")

        with lock:
            secret = vault_secret_fetcher.fetch_secret(path, key)

        return jsonify({"secret": secret})

    @staticmethod
    def shutdown()-> Tuple[dict[str, str], int]:
        def shutdown_server():
            func = request.environ.get("werkzeug.server.shutdown")
            if func is None:
                os.kill(os.getpid(), signal.SIGTERM)
            else:
                func()

        response = jsonify({"message": "Server shutting down..."})
        thread = Thread(target=shutdown_server)
        thread.start()
        return response
