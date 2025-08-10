from http import HTTPStatus
from unittest.mock import MagicMock, patch  # noqa: F401

import pytest  # type: ignore

from vaultutils.server import app as flask_app  # type: ignore
from vaultutils.server import start_server, stop_server


@pytest.fixture
def app():
    return flask_app


@pytest.fixture
def client(app):
    app.testing = True
    with app.test_client() as client:
        yield client


def test_start_server(mocker):
    mock_run = mocker.patch("vaultutils.server.app.run")
    start_server()
    mock_run.assert_called_once_with(host="localhost", port=8001)


def test_stop_server(mocker):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = HTTPStatus.OK
    stop_server()
    mock_post.assert_called_once_with("http://localhost:8001/shutdown", timeout=10)


def test_authenticate(mocker, client):
    mocker.patch("vaultutils.auth.login_vault")
    mocker.patch("vaultutils.controllers.vault_controller.Client")

    response = client.post("/authenticate")
    assert response.status_code == HTTPStatus.OK
    assert "token" in response.get_json()


def test_fetch_secret(mocker, client):
    mocker.patch("vaultutils.auth.login_vault")
    mocker.patch(
        "vaultutils.controllers.vault_controller.vault_secret_fetcher.fetch_secret",
        return_value={"key": "value"},
    )

    response = client.post(
        "/fetch-secret", json={"path": "path/to/secret", "key": "key"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {"secret": {"key": "value"}}


def test_shutdown():
    # The shutdown endpoient can not be tested as it terminates the current process and
    # does not return anything
    pass
