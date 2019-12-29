from flask import Blueprint, session, request, make_response

from src.controllers.auth import AuthenticationController, AuthorizationController

bp = Blueprint("users", __name__, url_prefix="/users")


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

    session["access_token"] = AuthorizationController.issue_token(
        user_credential["username"]
    )
    return make_response("", 200)

