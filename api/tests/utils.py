from flask import url_for, Response
from werkzeug import Client


def register_user(
    client: Client,
    first_name: str = "first_name",
    last_name: str = "last_name",
    email: str = "example@example.com",
    password: str = "password",
) -> Response:
    return client.post(
        url_for("user.create_user"),
        json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        },
    )


def login_user(
    client: Client, email: str = "example@example.com", password: str = "password"
) -> Response:
    return client.post(
        url_for("auth.login"), json={"email": email, "password": password}
    )
