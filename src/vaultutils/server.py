from flask import Flask # type: ignore
from vaultutils.views.vault_view import vault_blueprint
from vaultutils.config import Config

import requests # type: ignore

app = Flask(__name__)
app.register_blueprint(vault_blueprint)

def start_server()-> None:
    host = Config.VAULT_SERVER_HOST
    port = Config.VAULT_SERVER_PORT
    app.run(host=host, port=port)

def stop_server()-> None:
    host = Config.VAULT_SERVER_HOST
    port = Config.VAULT_SERVER_PORT
    try:
        response = requests.post(f"http://{host}:{port}/shutdown")
        if response.status_code == 200:
            print("Server shutdown successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error stopping the server: {e}")

if __name__ == "__main__":
    start_server()
