def test_login_successfully(client, registered_user) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_reject_wrong_password(client, registered_user) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "wrongpass"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_reject_unknown_email(client) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "missing@example.com", "password": "password123"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_wrong_password_and_unknown_email_share_generic_error(client, registered_user) -> None:
    wrong_password_response = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "wrongpass"},
    )
    unknown_email_response = client.post(
        "/api/v1/auth/login",
        json={"email": "missing@example.com", "password": "password123"},
    )

    assert wrong_password_response.status_code == 401
    assert unknown_email_response.status_code == 401
    assert wrong_password_response.json() == {"detail": "Invalid credentials"}
    assert unknown_email_response.json() == {"detail": "Invalid credentials"}
