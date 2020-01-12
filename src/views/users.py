from flask import Blueprint, session, request, make_response
from flask.cli import with_appcontext
import click

from src.controllers.auth import AuthenticationController

bp = Blueprint("users", __name__, url_prefix="/users")


@click.command("add-user")
@click.argument("username")
@click.argument("password")
@with_appcontext
def add_user(username, password):
    AuthenticationController.add_user(username, password)


@bp.route("/login", methods=["POST"])
def login():
    user_credential = request.get_json()
    if (
        AuthenticationController.verify_user(
            user_credential["username"], user_credential["password"]
        )
        is False
    ):
        return make_response("", 403)

    session["access_token"] = AuthenticationController.issue_token(
        user_credential["username"], 60 * 60 * 24  # 1 day
    )
    return make_response("", 200)


@bp.route("/logout", methods=["POST"])
def logout():
    session["access_token"] = ""
    return make_response("", 200)


def init_add_user(app):
    app.cli.add_command(add_user)
