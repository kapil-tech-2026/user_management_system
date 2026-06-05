from app.models.user import User


def test_register_user_success(client) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "password123"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "email": "user@example.com",
        "is_active": True,
        "role": "user",
    }


def test_reject_duplicate_email(client, registered_user) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "password123"},
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


def test_reject_invalid_email(client) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "not-an-email", "password": "password123"},
    )

    assert response.status_code == 422


def test_reject_short_password(client) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "short"},
    )

    assert response.status_code == 422


def test_stored_password_is_hashed(client, db_session) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "password123"},
    )

    assert response.status_code == 201

    stored_user = db_session.query(User).filter(User.email == "user@example.com").one()
    assert stored_user.hashed_password != "password123"
    assert stored_user.hashed_password
    assert stored_user.role == "user"


def test_register_response_does_not_expose_sensitive_fields(client) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "password123"},
    )

    assert response.status_code == 201
    body = response.json()
    assert "password" not in body
    assert "hashed_password" not in body


def test_public_registration_cannot_self_assign_admin(client) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "admin-try@example.com",
            "password": "password123",
            "role": "admin",
        },
    )

    assert response.status_code == 201
    assert response.json()["role"] == "user"
