import logging
from http import HTTPStatus

import requests  # type: ignore
from flask import Flask  # type: ignore

from vaultutils.config import Config
from vaultutils.views.vault_view import vault_blueprint

app = Flask(__name__)
app.register_blueprint(vault_blueprint)

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")


def start_server() -> None:
    host = Config.VAULT_SERVER_HOST
    port = Config.VAULT_SERVER_PORT
    app.run(host=host, port=port)


def stop_server() -> None:
    host = Config.VAULT_SERVER_HOST
    port = Config.VAULT_SERVER_PORT
    try:
        response = requests.post(f"http://{host}:{port}/shutdown")
        if response.status_code == HTTPStatus.OK:
            logging.info("Server shutdown successfully.")
    except requests.exceptions.RequestException as e:
        logging.info(f"Error stopping the server: {e}")


if __name__ == "__main__":
    start_server()
