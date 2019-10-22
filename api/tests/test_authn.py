import datetime

import flask
import jwt
import pytest
from passlib.hash import argon2
from flask import url_for

from api.decorators import check_authn
from api.exceptions import AuthenticationException, UserNotFoundException
from api.models import User
from api.schemas import UserResponseSchema
from api.tests.utils import register_user


class TestAuthn:
    def test_register_user(self, client, db):
        resp = register_user(client)

        assert resp.status_code == 201, resp.json["message"]

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
        assert resp.status_code == 200, resp.json["message"]
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

    @pytest.mark.xfail()
    def test_check_authn_no_header(self, mocker, app):
        mock_request = mocker.patch.object(flask, "request")
        mock_request.headers.get.return_value = dict()
        with pytest.raises(
            AuthenticationException,
            match="Request does not contain an 'Authorization' header",
        ), app.app_context():
            assert check_authn(mock_request)

    def test_check_authn_invalid_jwt(self, mocker, app):
        mock_request = mocker.patch.object(flask, "request")
        mock_request.headers.get.return_value = "Bearer token"
        with pytest.raises(
            AuthenticationException, match="Could not decode token: .*"
        ), app.app_context():
            assert check_authn(mock_request)

    def test_check_authn_no_exist(self, mocker, app):
        mock_request = mocker.patch.object(flask, "request")
        token = jwt.encode(
            {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(seconds=app.config["JWT_EXP_SEC"]),
                "sub": "no_exist@example.com",
                "fnm": "first_name",
                "lnm": "last_name",
            },
            app.config["JWT_SECRET"],
        ).decode("utf8")
        mock_request.headers.get.return_value = f"Bearer {token}"
        with pytest.raises(
            UserNotFoundException,
            match="No user with email no_exist@example.com was found",
        ), app.app_context():
            assert check_authn(mock_request)

    def test_check_authn_ok(self, client, mocker, app):
        register_user(client)
        mock_request = mocker.patch.object(flask, "request")
        token = jwt.encode(
            {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(seconds=app.config["JWT_EXP_SEC"]),
                "sub": "example@example.com",
                "fnm": "first_name",
                "lnm": "last_name",
            },
            app.config["JWT_SECRET"],
        ).decode("utf8")
        mock_request.headers.get.return_value = f"Bearer {token}"
        with app.app_context():
            check_authn(mock_request)
