from unittest.mock import MagicMock, patch  # noqa: F401

import pytest  # type: ignore
from click.testing import CliRunner  # type: ignore

from vaultutils.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_setup(runner: CliRunner, mocker) -> None:
    mock_subprocess = mocker.patch("vaultutils.cli.subprocess.run")
    result = runner.invoke(cli, ["setup"])
    assert result.exit_code == 0
    mock_subprocess.assert_called_once_with(["playwright", "install"], check=True)


def test_start(runner: CliRunner, mocker) -> None:
    mock_server = mocker.patch("vaultutils.cli.start_server")
    result = runner.invoke(cli, ["start"])
    assert result.exit_code == 0
    mock_server.assert_called_once()


def test_stop(runner: CliRunner, mocker) -> None:
    mock_server = mocker.patch("vaultutils.cli.stop_server")
    result = runner.invoke(cli, ["stop"])
    assert result.exit_code == 0
    mock_server.assert_called_once()


def test_fetch_secret(runner: CliRunner, mocker) -> None:
    mock_client = mocker.patch("vaultutils.cli.client")
    mock_client.fetch_secret.return_value = {"key": "value"}

    # Capture the result and print it for debugging
    result = runner.invoke(cli, ["fetch-secret", "path/to/secret", "key"])

    # Check for exit code and output
    assert result.exit_code == 0, (
        f"Unexpected exit code: {result.exit_code}, output: {result.output}"
    )
    assert "key" in result.output
    assert "value" in result.output


def test_authenticate(runner: CliRunner, mocker) -> None:
    mock_client = mocker.patch("vaultutils.cli.client")
    mock_client.authenticate.return_value = "test_token"
    result = runner.invoke(cli, ["authenticate"])
    assert result.exit_code == 0
    assert "Authenticated successfully" in result.output
    assert "test_token" in result.output
