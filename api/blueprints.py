from flask import request, g
from passlib.hash import argon2

from api.database import db, app
from api.decorators import requires_authn, requires_authz
from api.exceptions import (
    UserExistsException,
    AuthorizationException,
    AuthenticationException,
)
from api.schemas import UserRequestSchema, UserResponseSchema, LoginRequestSchema
from api.service import add_user, get_user_by_email, new_jwt, get_all_users

db.create_all()


@app.route("/user", methods=["GET"])
@requires_authz(roles=["admin"])
def get_users():
    """Get all users."""
    return UserResponseSchema(many=True).dumps(get_all_users())


@app.route("/user/<int:id>")
@requires_authn
def get_user_by_id(user_id: int):
    if g.user.id != user_id and not g.user.is_admin():
        app.logger.warn(
            f"User {g.user.id} tried to access {user_id} but was denied due to not having admin privileges"
        )
        raise AuthorizationException(
            f"User {g.user.email} does not have sufficient authorisation"
        )
    found_user = get_user_by_id(g.user.id)
    return UserResponseSchema().dumps(found_user)


@app.route("/user", methods=["POST"])
def create_user():
    """Create a new user."""
    req = UserRequestSchema().loads(request.get_data())

    try:
        created_user = add_user(**req)
    except UserExistsException as err:
        return {"message": str(err)}, 400

    if not create_user:
        app.logger.error(
            f"User with email {req['email']} was not found, even though they were just created"
        )
        return 500
    return UserResponseSchema().dumps(created_user), 201


@app.route("/login")
def login():
    """Exchange credentials for a JWT."""
    req = LoginRequestSchema().loads(request.get_data())
    user = get_user_by_email(req.email)
    if not user:
        app.logger.info(f"Could not find user with email {user.email}")
        raise AuthenticationException(f"Email {user.email} or password incorrect")

    if not argon2.verify(req.password, user.password):
        app.logger.info(f"User {user.id}'s password is incorrect")
        raise AuthenticationException(f"Email {user.email} or password incorrect")

    return new_jwt(user)
