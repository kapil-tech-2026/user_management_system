def test_me_works_with_valid_token(client, access_token) -> None:
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "user@example.com",
        "is_active": True,
        "role": "user",
    }


def test_me_rejects_missing_token(client) -> None:
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_me_rejects_invalid_token(client) -> None:
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_me_response_does_not_expose_sensitive_fields(client, access_token) -> None:
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "password" not in body
    assert "hashed_password" not in body
    assert body["role"] == "user"
