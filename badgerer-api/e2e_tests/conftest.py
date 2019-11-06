import os

import pytest
import requests


def get_token(base_url: str, user: str, password: str) -> str:
    rv = requests.post(
        f"{base_url}/login",
        json={"email": user, "password": password},
        headers={"User-Agent": "Pytest setup/teardown"},
    )
    assert rv.status_code == 200, rv.content.decode("utf8")
    assert "token" in rv.json()
    return rv.json()["token"]


def get_user_id(base_url: str, admin_token: str, email: str) -> int:
    rv = requests.get(
        f"{base_url}/user",
        headers={
            "Authorization": f"Bearer {admin_token}",
            "User-Agent": "Pytest setup/teardown",
        },
    )
    assert rv.status_code == 200
    return [user["id"] for user in rv.json() if user["email"] == email][0]


@pytest.fixture
def base_url():
    return os.environ.get("BASE_URL", "http://localhost:5000")


@pytest.fixture
def admin_user():
    return os.environ.get("ADMIN_USER", "admin@admin.com")


@pytest.fixture
def admin_password():
    return os.environ.get("ADMIN_PASS", "admin")


@pytest.fixture
def admin_token(base_url, admin_user, admin_password):
    return get_token(base_url, admin_user, admin_password)


@pytest.fixture
def user():
    return "test_user@example.com"


@pytest.fixture
def password():
    return "password"


@pytest.fixture
def user_token(base_url, user, password):
    return get_token(base_url, user, password)


@pytest.fixture
def user_id(base_url, admin_token, user):
    return get_user_id(base_url, admin_token, user)


@pytest.fixture
def user2():
    return "test_user2@example.com"


@pytest.fixture
def user2_token(base_url, user2, password):
    return get_token(base_url, user2, password)


@pytest.fixture
def user2_id(base_url, admin_token, user2):
    return get_user_id(base_url, admin_token, user2)


@pytest.fixture(autouse=True)
def before_after_test(base_url, admin_token, user, user2, password):
    # Create users
    rv = requests.post(
        f"{base_url}/user",
        json={
            "first_name": "test",
            "last_name": "user",
            "email": user,
            "password": password,
        },
        headers={"User-Agent": "Pytest setup/teardown"},
    )
    rv = requests.post(
        f"{base_url}/user",
        json={
            "first_name": "test",
            "last_name": "user",
            "email": user2,
            "password": password,
        },
        headers={"User-Agent": "Pytest setup/teardown"},
    )

    yield
    # Clean up users
    rv = requests.get(
        f"{base_url}/user",
        headers={
            "Authorization": f"Bearer {admin_token}",
            "User-Agent": "Pytest setup/teardown",
        },
    )
    assert rv.status_code == 200
    users = [user for user in rv.json() if user["email"] in (user, user2)]
    for select_user in users:
        rv = requests.delete(
            f"{base_url}/user/{select_user['id']}",
            headers={
                "Authorization": f"Bearer {admin_token}",
                "User-Agent": "Pytest setup/teardown",
            },
        )
        assert rv.status_code == 200


def pytest_configure(config):
    base_url = os.environ.get("BASE_URL", "http://localhost:5000")
    admin_user = os.environ.get("ADMIN_USER", "admin@admin.com")
    admin_password = os.environ.get("ADMIN_PASS", "admin")
    admin_token = get_token(base_url, admin_user, admin_password)
    rv = requests.get(
        f"{base_url}/user",
        headers={
            "Authorization": f"Bearer {admin_token}",
            "User-Agent": "Pytest setup/teardown",
        },
    )
    assert rv.status_code == 200
    users = [
        user
        for user in rv.json()
        if user["email"] in ("test_user@example.com", "test_user2@example.com")
    ]
    for select_user in users:
        rv = requests.delete(
            f"{base_url}/user/{select_user['id']}",
            headers={
                "Authorization": f"Bearer {admin_token}",
                "User-Agent": "Pytest setup/teardown",
            },
        )
        assert rv.status_code == 200
