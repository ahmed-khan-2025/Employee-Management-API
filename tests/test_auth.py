def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["username"] == "john"
    assert data["role"] == "user"
    assert "id" in data


def test_register_duplicate_user(client):
    first = client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "password123",
        },
    )

    assert first.status_code == 201

    second = client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "password123",
        },
    )

    assert second.status_code == 409


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "john",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data is not None
    assert "access_token" in data


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "password123",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "john",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_login_unknown_user(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "unknown",
            "password": "password123",
        },
    )

    assert response.status_code == 401


def test_me_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_me_with_token(client, admin_token):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["username"] == "admin"
    assert data["role"] == "admin"


def test_me_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401