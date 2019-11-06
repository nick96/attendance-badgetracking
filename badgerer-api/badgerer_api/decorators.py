from functools import wraps
from typing import List

import jwt
from flask import request, g, current_app, Request

from .exceptions import AuthenticationException, AuthorizationException
from .service import get_user_by_email, validate_jwt


def check_authn(request: Request):
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


def requires_authn():
    """Decorator to assert a user is authenticated.

    This decorator ensure that the bearer token in the `Authorization` header exists and it valid. Then it adds the
     user's email to the `user_email` field to the request context (`g`) so it is accessible during the request.
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            check_authn(request)
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def requires_authz(roles: List[str]):
    """Decorator to assert the user has the required authentication (via roles).

    Using this decorator implies authentication (`requires_auth` is called inside).
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            check_authz(request, roles)
            return fn(*args, **kwargs)

        return decorator

    return wrapper
