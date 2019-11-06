from typing import List

from sqlalchemy import Table
from sqlalchemy.orm import relationship

from .extensions import db

# Join table to users and roles.
_users_x_roles = Table(
    "users_x_roles",
    db.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
    extend_existing=True,
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    roles = relationship("Role", secondary=_users_x_roles)

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        roles=[],
    ):
        super().__init__(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            roles=roles,
        )

    def is_admin(self) -> bool:
        return self.has_role("admin")

    def has_role(self, role: str) -> bool:
        usr = User.query.filter_by(email=self.email).first()
        return role in [role.name for role in usr.roles]


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    users = relationship("User", secondary=_users_x_roles)

    def __init__(self, name: str, users: List[User]):
        super().__init__(name=name, users=users)
