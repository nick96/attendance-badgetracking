from marshmallow import ValidationError
from flask import request, current_app


class UserExistsException(Exception):
    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists")


class RoleExistsException(Exception):
    def __init__(self, name: str):
        super().__init__(f"Role with name {name} already exists")


class RoleNotFoundException(Exception):
    def __init__(self, name: str = "", role_id: int = 0):
        if role_id > 0:
            super().__init__(f"Role with ID {role_id} not found")
        else:
            super().__init__(f"Role with name {name} not found")


class AuthenticationException(Exception):
    def __init__(self, message):
        super().__init__(message)


class AuthorizationException(Exception):
    def __init__(self, message):
        super().__init__(message)


class UserNotFoundException(Exception):
    def __init__(self, email: str = "", user_id: int = 0):
        if user_id > 0:
            super().__init__(f"Not user with ID {user_id} was found")
        else:
            super().__init__(f"Not user with email {email} was found")


def validation_error_handler(app, error):
    app.logger.warning(f"Invalid request body: {request.get_data()}")
    return {"message": "Validation error", "errors": error.messages}, 400


def authn_exception_handler(app, error):
    app.logger.warning(f"Authentication exception: {str(error)}")
    return {"message": "Authentication error", "error": str(error)}, 403


def authz_exception_handler(app, error):
    app.logger.warning(f"Authorization exception: {str(error)}")
    return {"message": "Authorization error", "error": str(error)}, 401


def user_exists_exception_handler(app, error):
    app.logger.warning(f"User already exists: {str(error)}")
    return {"message": "User already exists", "error": str(error)}, 400


def role_exists_exception_handler(app, error):
    app.logger.warning(f"User already exists: {str(error)}")
    return {"message": "Role already exists", "error": str(error)}, 400
