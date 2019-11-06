from flask import Blueprint
from flask import request, g, current_app
from passlib.hash import argon2  # type: ignore
from badgerer_api import service
from badgerer_api.decorators import requires_authn, requires_authz
from badgerer_api.exceptions import (
    AuthorizationException,
    AuthenticationException,
    UserNotFoundException,
)
from badgerer_api.schemas import (
    UserRequestSchema,
    UserResponseSchema,
    LoginRequestSchema,
)

user_blueprint = Blueprint("user", __name__)
auth_blueprint = Blueprint("auth", __name__)


@user_blueprint.route("/user", methods=["GET"])
@requires_authz(roles=["admin"])
def get_users():
    """Get all users."""
    return UserResponseSchema(many=True).dumps(service.get_all_users())


@user_blueprint.route("/user/<int:user_id>")
@requires_authn()
def get_user_by_id(user_id: int):
    if g.user.id != user_id and not g.user.is_admin():
        current_app.logger.warning(
            f"User {g.user.id} tried to access {user_id} but was denied"
            + " due to not having admin privileges"
        )
        raise AuthorizationException(
            f"User {g.user.email} does not have sufficient authorisation"
        )
    found_user = service.get_user_by_id(user_id)
    current_app.logger.info(f"Found user {found_user}")
    return UserResponseSchema().dump(found_user)


@user_blueprint.route("/user", methods=["POST"])
def create_user():
    """Create a new user."""
    req = UserRequestSchema().loads(request.get_data())
    created_user = service.add_user(**req)

    if not create_user:
        current_app.logger.error(
            f"User with email {req['email']} was not found, even though they"
            + " were just created"
        )
        return 500
    current_app.logger.info(f"Created user {created_user}")
    return UserResponseSchema().dump(created_user), 201


@user_blueprint.route("/user/<int:user_id>", methods=["PUT"])
@requires_authn()
def update_user(user_id: int):
    req = UserRequestSchema().load(request.get_json())
    updated_user = service.update_user(
        updating_user=g.user, update_user_id=user_id, **req
    )
    current_app.logger.info(f"Updated user {updated_user}")
    return UserResponseSchema().dump(updated_user)


@user_blueprint.route("/user/<int:user_id>", methods=["DELETE"])
@requires_authn()
def delete_user(user_id: int):
    deleted_user = service.delete_user(
        deleting_user=g.user, delete_user_id=user_id
    )
    current_app.logger.info(f"Deleted user {deleted_user}")
    return UserResponseSchema().dump(deleted_user)


@auth_blueprint.route("/login", methods=["POST"])
def login():
    """Exchange credentials for a JWT."""
    req = LoginRequestSchema().loads(request.get_data())
    try:
        user = service.get_user_by_email(req["email"])
    except UserNotFoundException as err:
        err.status_code = 403
        raise err
    if not user:
        current_app.logger.info(
            f"Could not find user with email {req['email']}"
        )
        raise AuthenticationException("Email or password incorrect")

    if not argon2.verify(req["password"], user.password):
        current_app.logger.info(f"User {user.id}'s password is incorrect")
        raise AuthenticationException("Email or password incorrect")

    current_app.logger.info(f"Creating token for user {user}")
    return {"token": service.new_jwt(user)}
