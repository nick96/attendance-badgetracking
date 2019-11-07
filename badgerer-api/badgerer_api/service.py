"""Service layer.

This provides a way for the controllers to interact with the persistence layer
in an abstracted manner.

"""

import datetime
from typing import Iterator, List

import jwt
from badgerer_api.exceptions import (
    AuthorizationException,
    RoleExistsException,
    RoleNotFoundException,
    UserExistsException,
    UserNotFoundException,
)
from badgerer_api.extensions import db
from badgerer_api.models import Role, User
from flask import current_app
from passlib.hash import argon2  # type: ignore


def get_user_by_id(user_id: int) -> User:
    """Get a user by their ID.

    :para user_id: ID of the user to get
    """
    user: User = User.query.filter_by(id=user_id).first()
    if not user:
        raise UserNotFoundException(user_id=user_id)
    return user


def get_user_by_email(email: str) -> User:
    """Get a user by their email.

    :param email: Email to retrieve the user by
    """
    user: User = User.query.filter_by(email=email).first()
    if not user:
        raise UserNotFoundException(email=email)
    return user


def add_user(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    role_names: List[str] = [],
) -> User:
    """Create a new user."""
    if User.query.filter_by(email=email).scalar():
        raise UserExistsException(email=email)
    roles = [get_role_by_name(role_name) for role_name in role_names]
    password = argon2.hash(password)
    db.session.add(User(first_name, last_name, email, password, roles))
    db.session.commit()
    created_user: User = User.query.filter_by(email=email).first()
    return created_user


def get_all_users() -> Iterator[User]:
    """Get all the users in the database."""
    users: Iterator[User] = User.query.all()
    return users


def update_user(
    updating_user: User,
    update_user_id: int,
    first_name: str,
    last_name: str,
    email: str,
    password: str = None,
    role_names: List[str] = None,
) -> User:
    """Update a user."""
    if not updating_user.is_admin() and updating_user.id != update_user_id:
        raise AuthorizationException(
            f"User cannot update user {update_user_id}"
        )

    if not updating_user.is_admin() and role_names is not None:
        raise AuthorizationException(f"User cannot update their roles")

    user = get_user_by_id(update_user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    if password:
        user.password = argon2.hash(password)
    if role_names is not None:
        user.roles = [
            get_role_by_name(role_name) for role_name in role_names
        ]  # type: ignore

    db.session.commit()
    updated_user: User = User.query.filter_by(id=update_user_id).first()
    return updated_user


def delete_user(deleting_user: User, delete_user_id: int) -> User:
    """Delete a user."""
    if not deleting_user.is_admin() and deleting_user.id != delete_user_id:
        raise AuthorizationException(
            f"User cannot delete user {delete_user_id}"
        )
    deleted_user = get_user_by_id(delete_user_id)
    db.session.delete(deleted_user)
    db.session.commit()
    return deleted_user


def add_role(
    name: str, user_emails: List[str] = [], user_ids: List[int] = []
) -> Role:
    """Add a role to user."""
    if Role.query.filter_by(name=name).scalar():
        raise RoleExistsException(name)
    users = [get_user_by_email(email) for email in user_emails] + [
        get_user_by_id(user_id) for user_id in user_ids
    ]
    db.session.add(Role(name, users))
    db.session.commit()
    added_role: Role = Role.query.filter_by(name=name).first()
    return added_role


def get_role_by_name(name: str) -> Role:
    """Retrieve a role by its name."""
    role: Role = Role.query.filter_by(name=name).first()
    if not role:
        raise RoleNotFoundException(name=name)
    return role


def new_jwt(user: User, app=current_app) -> str:
    """Create and return a new JWT."""
    return jwt.encode(
        {
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(seconds=app.config["JWT_EXP_SEC"]),
            "sub": user.email,
            "fnm": user.first_name,
            "lnm": user.last_name,
        },
        app.config["JWT_SECRET"],
    ).decode("utf8")


def validate_jwt(token: str, app=current_app) -> dict:
    """Validate a JWT."""
    return jwt.decode(
        token, app.config["JWT_SECRET"], algorithms=app.config["JWT_ALGOS"]
    )
