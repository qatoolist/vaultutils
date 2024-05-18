import pytest   # type: ignore
from vaultutils.client import VaultManagerClient

@pytest.fixture
def client():
    return VaultManagerClient()

def test_setup(mocker):
    mock_subprocess = mocker.patch("vaultutils.client.subprocess.run")
    client = VaultManagerClient()
    client.setup()
    mock_subprocess.assert_called_once_with(["playwright", "install"], check=True)

def test_start(mocker, client):
    mock_start_server = mocker.patch("vaultutils.client.start_server")
    client.start()
    mock_start_server.assert_called_once()

def test_stop(mocker, client):
    mock_stop_server = mocker.patch("vaultutils.client.stop_server")
    client.stop()
    mock_stop_server.assert_called_once()

def test_authenticate(mocker, client):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"token": "test_token"}

    token = client.authenticate()
    assert token == "test_token"
    mock_post.assert_called_once_with("http://localhost:8001/authenticate")

def test_fetch_secret(mocker, client):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"secret": {"key": "value"}}

    secret = client.fetch_secret("path/to/secret", "key")
    assert secret == {"secret": {"key": "value"}}
    mock_post.assert_called_once_with("http://localhost:8001/fetch-secret", json={"path": "path/to/secret", "key": "key"})
