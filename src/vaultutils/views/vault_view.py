from flask import Blueprint  # type: ignore

from vaultutils.controllers.vault_controller import VaultController

vault_blueprint = Blueprint("vault", __name__)

vault_blueprint.add_url_rule(
    "/authenticate", view_func=VaultController.authenticate, methods=["POST"]
)
vault_blueprint.add_url_rule(
    "/fetch-secret", view_func=VaultController.fetch_secret, methods=["POST"]
)
vault_blueprint.add_url_rule(
    "/shutdown", view_func=VaultController.shutdown, methods=["POST"]
)
