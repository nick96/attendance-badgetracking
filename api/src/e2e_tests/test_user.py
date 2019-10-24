import requests


def test_admins_get_users(base_url, admin_token):
    rv = requests.get(
        f"{base_url}/user", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert rv.status_code == 200
    assert isinstance(rv.json(), list)


def test_users_get_users(base_url, user_token):
    rv = requests.get(
        f"{base_url}/user", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert rv.status_code == 401


def test_user_get_self(base_url, user_token, user_id):
    rv = requests.get(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert rv.status_code == 200
    assert "id" in rv.json() and rv.json()["id"] == user_id
    assert "first_name" in rv.json()
    assert "last_name" in rv.json()
    assert "password" not in rv.json()
    assert "email" in rv.json()
    assert "roles" in rv.json()
    assert isinstance(rv.json()["roles"], list)


def test_admin_get_user(base_url, admin_token, user_id):
    rv = requests.get(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert rv.status_code == 200
    assert "id" in rv.json()
    assert rv.json()["id"] == user_id
    assert "first_name" in rv.json()
    assert "last_name" in rv.json()
    assert "password" not in rv.json()
    assert "email" in rv.json()


def test_user_get_user(base_url, user2_token, user_id):
    rv = requests.get(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert rv.status_code == 401


def test_admin_update_user(base_url, admin_token, user_id):
    rv = requests.get(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert rv.status_code == 200
    updated_user = {
        "first_name": f"{rv.json()['first_name']} updated",
        "last_name": rv.json()["last_name"],
        "email": rv.json()["email"],
    }
    rv = requests.put(
        f"{base_url}/user/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=updated_user,
    )
    assert rv.status_code == 200
    assert rv.json()["first_name"] == updated_user["first_name"]
    assert rv.json()["last_name"] == updated_user["last_name"]
    assert rv.json()["email"] == updated_user["email"]

    requests.get(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert rv.status_code == 200
    assert rv.json()["first_name"] == updated_user["first_name"]
    assert rv.json()["last_name"] == updated_user["last_name"]
    assert rv.json()["email"] == updated_user["email"]


def test_user_update_self(base_url, user_token, user_id):
    rv = requests.get(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert rv.status_code == 200
    updated_user = {
        "first_name": f"{rv.json()['first_name']} updated",
        "last_name": rv.json()["last_name"],
        "email": rv.json()["email"],
    }
    rv = requests.put(
        f"{base_url}/user/{user_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json=updated_user,
    )
    assert rv.status_code == 200
    assert rv.json()["first_name"] == updated_user["first_name"]
    assert rv.json()["last_name"] == updated_user["last_name"]
    assert rv.json()["email"] == updated_user["email"]

    requests.get(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert rv.status_code == 200
    assert rv.json()["first_name"] == updated_user["first_name"]
    assert rv.json()["last_name"] == updated_user["last_name"]
    assert rv.json()["email"] == updated_user["email"]


def test_user_update_user(base_url, user_token, user2_token, user_id):
    rv = requests.get(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert rv.status_code == 200
    updated_user = {
        "first_name": f"{rv.json()['first_name']} updated",
        "last_name": rv.json()["last_name"],
        "email": rv.json()["email"],
    }
    rv = requests.put(
        f"{base_url}/user/{user_id}",
        headers={"Authorization": f"Bearer {user2_token}"},
        json=updated_user,
    )
    assert rv.status_code == 401


def test_admin_delete_user(base_url, admin_token, user_id):
    rv = requests.delete(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert rv.status_code == 200
    rv = requests.get(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert rv.status_code == 404


def test_user_delete_self(base_url, user_token, user_id):
    rv = requests.delete(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert rv.status_code == 200
    rv = requests.get(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert rv.status_code == 404


def test_user_delete_user(base_url, user2_token, user_token, user_id):
    rv = requests.delete(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert rv.status_code == 401
    rv = requests.get(
        f"{base_url}/user/{user_id}", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert rv.status_code == 200
