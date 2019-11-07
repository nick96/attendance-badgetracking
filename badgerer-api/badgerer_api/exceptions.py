"""Application specific exceptions."""

from flask import request
from typing import Optional


class UserExistsException(Exception):
    """Exception thrown when the user already exist."""

    def __init__(self, email: str):
        """Create a new exception for the already existing email."""
        super().__init__(f"User with email {email} already exists")


class RoleExistsException(Exception):
    """Exception thrown when the role already exists."""

    def __init__(self, name: str):
        """Create new exception for the already existing role."""
        super().__init__(f"Role with name {name} already exists")


class RoleNotFoundException(Exception):
    """Exception thrown when the role is not found."""

    def __init__(
        self, name: Optional[str] = None, role_id: Optional[int] = None
    ):
        """Create a new exception for the unfound role.

        Roles can be retrieved by their ID or name, this constructor accounts
        for both.

        """
        if role_id is not None:
            super().__init__(f"Role with ID {role_id} not found")
        elif name is not None:
            super().__init__(f"Role with name {name} not found")
        else:
            raise ValueError("name or role_id parameters must be provided.")


class AuthenticationException(Exception):
    """Exception thrown when authentication fails."""

    def __init__(self, message):
        """Create new AuthenticationException."""
        super().__init__(message)


class AuthorizationException(Exception):
    """Exception thrown when authorization fails."""

    def __init__(self, message):
        """Create a new AuthorizationException."""
        super().__init__(message)


class UserNotFoundException(Exception):
    """Exception thrown then the user is not found."""

    def __init__(
        self,
        email: Optional[str] = None,
        user_id: Optional[int] = None,
        status_code=404,
    ):
        """Create a user not found exception.

        This exceptions can be raised in two contexts. When we're trying to
        retrieve a user from an authenticated request and when the user is
        logging in. In the first context, we want to return a 404 Not Found,
        however in the second on we want to return a 403 Forbidden because the
        login is incorrect.

        :param email: Email of the unfound user, this should not be used with user_id
        :param user_id: ID of the unfound user, this should not be used with email
        :param status_code: Status code that should be returned to the user, defaults to 404

        """
        self.status_code = status_code
        if user_id is not None:
            super().__init__(f"No user with ID {user_id} was found")
        elif email is not None:
            super().__init__(f"No user with email {email} was found")
        else:
            raise ValueError("user_id or email parameters must be provided")


def validation_error_handler(app, error):
    """Handle validation errors."""
    app.logger.warning(f"Invalid request body: {request.get_data()}")
    return {"message": "Validation error", "errors": error.messages}, 400


def authn_exception_handler(app, error):
    """Handle authentication exceptions."""
    app.logger.warning(f"Authentication exception: {str(error)}")
    return {"message": "Authentication error", "error": str(error)}, 403


def authz_exception_handler(app, error):
    """Handle authorization exceptions."""
    app.logger.warning(f"Authorization exception: {str(error)}")
    return {"message": "Authorization error", "error": str(error)}, 401


def user_exists_exception_handler(app, error):
    """Handle exceptions thrown when the user already exists."""
    app.logger.warning(f"User already exists: {str(error)}")
    return {"message": "User already exists", "error": str(error)}, 400


def role_exists_exception_handler(app, error):
    """Handle exceptions thrown when the role already exists."""
    app.logger.warning(f"User already exists: {str(error)}")
    return {"message": "Role already exists", "error": str(error)}, 400


def user_not_found_exception_handler(app, error):
    """Handle exceptions thrown when the user is not found."""
    app.logger.warning(f"Could not find user: {str(error)}")
    expected_msg = {"message": "User not found", "error": str(error)}
    return expected_msg, error.status_code


def role_not_found_exception_handler(app, error):
    """Handle exceptions thrown when the roles is not found."""
    app.logger.warning(f"Could not find role: {str(error)}")
    return {"message": "Role not found", "error": str(error)}, 404
