"""Decorators used throughout the application."""

from functools import wraps
from typing import List

import jwt
from flask import request, g, current_app, Request

from .exceptions import AuthenticationException, AuthorizationException
from .service import get_user_by_email, validate_jwt


def check_authn(request: Request):
    """Authenticate the user based on the given request.

    The `Authorization` header should contain a bearer token which is checked
    for validity. The user is then set based on the email contained in the
    payload.

    :param request: Request to get the token from

    """
    authn = request.headers.get("Authorization")
    if not authn:
        raise AuthenticationException(
            "Request does not contain an 'Authorization' header"
        )
    current_app.logger.debug(f"Found authorization header: {authn}")
    token = authn.replace("Bearer ", "")
    current_app.logger.debug(f"Bearer token is {token}")
    try:
        payload = validate_jwt(token)
    except jwt.InvalidTokenError as err:
        raise AuthenticationException(f"Could not decode token: {str(err)}")
    current_app.logger.debug(f"Validated token with payload {payload}")
    user = get_user_by_email(payload["sub"])
    if not user:
        raise AuthenticationException(
            f"Could not find user with email {payload['sub']}"
        )
    current_app.logger.debug(f"Token is for user {user}")
    g.user = user


def check_authz(request: Request, roles: List[str]):
    """Check the user is authorized.

    First checks that the user can be correctly authenticated using the given
    request. Then checks they have the required roles.

    :param request: Request to get the token from to authenticate the user
    :param roles: Roles to check the user has the correct authorization

    """
    check_authn(request)
    user = get_user_by_email(g.user.email)
    if not user:
        raise AuthorizationException(
            f"No user with email {g.user.email} exists"
        )

    for role in roles:
        if not user.has_role(role):
            raise AuthorizationException(
                f"User {g.user.email} does not have sufficient authorisation"
            )


def requires_authn():  # noqa: D202
    """Assert a user is authenticated.

    This decorator ensure that the bearer token in the `Authorization` header
    exists and it valid. Then it adds the user's email to the `user_email`
    field to the request context (`g`) so it is accessible during the request.

    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            check_authn(request)
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def requires_authz(roles: List[str]):  # noqa: D202
    """Assert the user has the required authentication (via roles).

    Using this decorator implies authentication (`requires_auth` is called
    inside).

    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            check_authz(request, roles)
            return fn(*args, **kwargs)

        return decorator

    return wrapper
