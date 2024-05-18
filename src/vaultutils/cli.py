import click  # type: ignore
import subprocess
from typing import Optional
from vaultutils.server import start_server, stop_server
from vaultutils.client import VaultManagerClient

client = VaultManagerClient()

@click.group()
def cli() -> None:
    """CLI group for Vault Manager commands."""
    pass

@cli.command()
def setup() -> None:
    """Setup Playwright."""
    subprocess.run(["playwright", "install"], check=True)

@cli.command()
def start() -> None:
    """Start the Vault Manager server."""
    start_server()

@cli.command()
def stop() -> None:
    """Stop the Vault Manager server."""
    stop_server()

@cli.command()
@click.argument("path")
@click.argument("key", required=False)
def fetch_secret(path: str, key: Optional[str]) -> None:
    """Fetch a secret from Vault."""
    try:
        secret = client.fetch_secret(path, key)
        click.echo(secret)
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
def authenticate() -> None:
    """Authenticate with Vault using environment variables."""
    try:
        token = client.authenticate()
        click.echo(f"Authenticated successfully. Token: {token}")
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == "__main__":
    cli()
