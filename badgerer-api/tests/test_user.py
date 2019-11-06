from flask import url_for
from werkzeug import Client

from badgerer_api.models import User
from badgerer_api.schemas import UserResponseSchema, UserRequestSchema

from .utils import register_user, login_user


class TestUser:
    def test_get_user_self(self, app, client: Client):
        register_resp = register_user(client)
        login_resp = login_user(client)
        resp = client.get(
            url_for("user.get_user_by_id", user_id=register_resp.json["id"]),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
        )
        assert resp.status_code == 200
        UserResponseSchema().loads(resp.data)

    def test_get_user_no_exist(self, app, client):
        login_resp = login_user(
            client,
            email=app.config["ADMIN_EMAIL"],
            password=app.config["ADMIN_PASSWORD"],
        )
        resp = client.get(
            url_for("user.get_user_by_id", user_id=100),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
        )
        assert resp.status_code == 404

    def test_get_user_admin(self, app, client):
        register_resp = register_user(client)
        login_resp = login_user(
            client,
            email=app.config["ADMIN_EMAIL"],
            password=app.config["ADMIN_PASSWORD"],
        )
        resp = client.get(
            url_for("user.get_user_by_id", user_id=register_resp.json["id"]),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
        )
        assert resp.status_code == 200
        UserResponseSchema().loads(resp.data)

    def test_get_user_other(self, client):
        register_resp = register_user(client)
        register_user(client, email="example2@example.com")
        login_resp = login_user(client, email="example2@example.com")
        resp = client.get(
            url_for("user.get_user_by_id", user_id=register_resp.json["id"]),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
        )
        assert resp.status_code == 401

    def test_update_user_self(self, db, client):
        register_resp = register_user(client)
        login_resp = login_user(client)

        user = (
            db.session.query(User)
            .filter_by(id=register_resp.json["id"])
            .first()
        )
        user.first_name = "updated_first_name"
        req = UserRequestSchema().dump(user)
        req.pop("password")
        resp = client.put(
            url_for("user.update_user", user_id=user.id),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
            json=req,
        )
        assert resp.status_code == 200
        updated_user_resp = UserResponseSchema().loads(resp.data)
        assert updated_user_resp["first_name"] == user.first_name

    def test_update_user_admin(self, app, db, client):
        register_resp = register_user(client)
        login_resp = login_user(
            client,
            email=app.config["ADMIN_EMAIL"],
            password=app.config["ADMIN_PASSWORD"],
        )

        user = (
            db.session.query(User)
            .filter_by(id=register_resp.json["id"])
            .first()
        )
        user.first_name = "updated_first_name"
        req = UserRequestSchema().dump(user)
        req.pop("password")
        resp = client.put(
            url_for("user.update_user", user_id=user.id),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
            json=req,
        )
        assert resp.status_code == 200
        updated_user_resp = UserResponseSchema().loads(resp.data)
        assert updated_user_resp["first_name"] == user.first_name

    def test_update_user_other(self, db, client):
        register_resp = register_user(client)
        register_user(client, email="example2@example.com")
        login_resp = login_user(
            client, email="example2@example.com", password="password"
        )

        user = (
            db.session.query(User)
            .filter_by(id=register_resp.json["id"])
            .first()
        )
        user.first_name = "updated_first_name"
        req = UserRequestSchema().dump(user)
        req.pop("password")
        resp = client.put(
            url_for("user.update_user", user_id=user.id),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
            json=req,
        )
        assert resp.status_code == 401

    def test_delete_user_self(self, db, client):
        register_resp = register_user(client)
        login_resp = login_user(client)

        resp = client.delete(
            url_for("user.update_user", user_id=register_resp.json["id"]),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
        )
        assert resp.status_code == 200
        UserResponseSchema().loads(resp.data)
        assert (
            db.session.query(User)
            .filter_by(id=register_resp.json["id"])
            .scalar()
            is None
        )

    def test_delete_user_admin(self, db, app, client):
        register_resp = register_user(client)
        login_resp = login_user(
            client,
            email=app.config["ADMIN_EMAIL"],
            password=app.config["ADMIN_PASSWORD"],
        )

        resp = client.delete(
            url_for("user.update_user", user_id=register_resp.json["id"]),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
        )
        assert resp.status_code == 200
        UserResponseSchema().loads(resp.data)
        assert (
            db.session.query(User)
            .filter_by(id=register_resp.json["id"])
            .scalar()
            is None
        )

    def test_delete_user_other(self, client):
        register_resp = register_user(client)
        register_user(client, email="example2@example.com")
        login_resp = login_user(
            client, email="example2@example.com", password="password"
        )
        resp = client.delete(
            url_for("user.update_user", user_id=register_resp.json["id"]),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
        )
        assert resp.status_code == 401

    def test_admin_get_all(self, app, client):
        register_user(client)
        login_resp = login_user(
            client,
            email=app.config["ADMIN_EMAIL"],
            password=app.config["ADMIN_PASSWORD"],
        )
        resp = client.get(
            url_for("user.get_users"),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
        )
        assert resp.status_code == 200

    def test_user_get_all(self, client: Client):
        register_user(client)
        login_resp = login_user(client)
        resp = client.get(
            url_for("user.get_users"),
            headers={"Authorization": f"Bearer {login_resp.json['token']}"},
        )
        assert resp.status_code == 401
