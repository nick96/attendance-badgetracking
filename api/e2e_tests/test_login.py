import requests


def test_admin_login(base_url, admin_user, admin_password):
    rv = requests.post(
        f"{base_url}/login", json={"email": admin_user, "password": admin_password}
    )
    assert rv.status_code == 200
    assert list(rv.json().keys()) == ["token"]


def test_user_login(base_url, user, password):
    rv = requests.post(f"{base_url}/login", json={"email": user, "password": password})
    assert rv.status_code == 200
    assert list(rv.json().keys()) == ["token"]
