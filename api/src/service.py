import datetime
from typing import List, Iterator

import jwt
from flask import current_app
from passlib.hash import argon2

from api.exceptions import (
    UserExistsException,
    RoleExistsException,
    RoleNotFoundException,
    AuthorizationException,
    UserNotFoundException,
)
from api.extensions import db
from api.models import User, Role


def get_user_by_id(user_id: int) -> User:
    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise UserNotFoundException(user_id=user_id)
    return user


def get_user_by_email(email: str) -> User:
    user = User.query.filter_by(email=email).first()
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
    if User.query.filter_by(email=email).scalar():
        raise UserExistsException(email=email)
    roles = [get_role_by_name(role_name) for role_name in role_names]
    password = argon2.hash(password)
    db.session.add(User(first_name, last_name, email, password, roles))
    db.session.commit()
    return User.query.filter_by(email=email).first()


def get_all_users() -> Iterator[User]:
    return User.query.all()


def update_user(
    updating_user: User,
    update_user_id: int,
    first_name: str,
    last_name: str,
    email: str,
    password: str = None,
    role_names: List[str] = None,
) -> User:
    if not updating_user.is_admin() and updating_user.id != update_user_id:
        raise AuthorizationException(f"User cannot update user {update_user_id}")

    if not updating_user.is_admin() and role_names is not None:
        raise AuthorizationException(f"User cannot update their roles")

    user = get_user_by_id(update_user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    if password:
        user.password = argon2.hash(password)
    if role_names is not None:
        user.roles = [get_role_by_name(role_name) for role_name in role_names]

    db.session.commit()
    return User.query.filter_by(id=update_user_id).first()


def delete_user(deleting_user: User, delete_user_id: int) -> User:
    if not deleting_user.is_admin() and deleting_user.id != delete_user_id:
        raise AuthorizationException(f"User cannot delete user {delete_user_id}")
    deleted_user = get_user_by_id(delete_user_id)
    db.session.delete(deleted_user)
    db.session.commit()
    return deleted_user


def add_role(name: str, user_emails: List[str] = [], user_ids: List[int] = []) -> Role:
    if Role.query.filter_by(name=name).scalar():
        raise RoleExistsException(name)
    users = [get_user_by_email(email) for email in user_emails] + [
        get_user_by_id(user_id) for user_id in user_ids
    ]
    db.session.add(Role(name, users))
    db.session.commit()
    return Role.query.filter_by(name=name).first()


def get_role_by_name(name: str) -> Role:
    role = Role.query.filter_by(name=name).first()
    if not role:
        raise RoleNotFoundException(name=name)
    return role


def new_jwt(user: User, app=current_app) -> str:
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
    return jwt.decode(
        token, app.config["JWT_SECRET"], algorithms=app.config["JWT_ALGOS"]
    )
