import functools

from flask import session, make_response

from src.controllers.auth import AuthenticationController


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if "access_token" not in session or not AuthenticationController.verify_token(
            session["access_token"]
        ):
            return make_response("", 403)
        else:
            return view(*args, **kwargs)

    return wrapped_view
