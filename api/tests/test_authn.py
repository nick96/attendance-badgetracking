import jwt
from passlib.hash import argon2
from flask import url_for

from api.models import User
from api.schemas import UserResponseSchema
from api.tests.utils import register_user


class TestAuthn:
    def test_register_user(self, client, db):
        resp = register_user(client)

        assert resp.status_code == 201

        registered_user = UserResponseSchema().loads(resp.data)

        usr = db.session.query(User).filter_by(id=registered_user["id"]).first()
        assert usr
        assert argon2.verify("password", usr.password)

    def test_register_already_registered_user(self, client):
        register_user(client)
        resp = register_user(client)

        assert resp.status_code == 400

    def test_login_successful(self, app, client):
        register_user(client)
        resp = client.post(
            url_for("auth.login"),
            json={"email": "example@example.com", "password": "password"},
        )
        assert resp.status_code == 200
        assert "token" in resp.json
        assert jwt.decode(
            resp.json["token"],
            app.config["JWT_SECRET"],
            algorithms=app.config["JWT_ALGOS"],
        )

    def test_login_no_exist(self, client):
        resp = client.post(
            url_for("auth.login"),
            json={"email": "example@example.com", "password": "password"},
        )
        assert resp.status_code == 403
        assert "token" not in resp.json

    def test_login_wrong_password(self, client):
        register_user(client)
        resp = client.post(
            url_for("auth.login"),
            json={"email": "example@example.com", "password": "password1"},
        )
        assert resp.status_code == 403
        assert "token" not in resp.json
