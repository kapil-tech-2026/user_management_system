import pytest

from app.core.security import decode_access_token, verify_password
from app.services.exceptions import (
    AuthenticationError,
    AuthorizationError,
    InvalidTokenError,
    UserAlreadyExistsError,
)


def test_register_user_returns_created_user(auth_service) -> None:
    user = auth_service.register_user("user@example.com", "password123")

    assert user.id == 1
    assert user.email == "user@example.com"
    assert user.is_active is True
    assert user.role == "user"


def test_register_user_hashes_password_before_storage(auth_service, user_repository) -> None:
    user = auth_service.register_user("user@example.com", "password123")
    stored_user = user_repository.get_user_by_id(user.id)

    assert stored_user is not None
    assert stored_user.hashed_password != "password123"
    assert verify_password("password123", stored_user.hashed_password) is True


def test_register_user_rejects_duplicate_email(auth_service) -> None:
    auth_service.register_user("user@example.com", "password123")

    with pytest.raises(UserAlreadyExistsError):
        auth_service.register_user("user@example.com", "password123")


def test_authenticate_user_success(auth_service) -> None:
    created_user = auth_service.register_user("user@example.com", "password123")

    authenticated_user = auth_service.authenticate_user(
        "user@example.com",
        "password123",
    )

    assert authenticated_user.id == created_user.id


def test_authenticate_user_rejects_wrong_password(auth_service) -> None:
    auth_service.register_user("user@example.com", "password123")

    with pytest.raises(AuthenticationError) as wrong_password_error:
        auth_service.authenticate_user("user@example.com", "wrongpass")

    assert str(wrong_password_error.value) == "Invalid credentials"


def test_authenticate_user_rejects_unknown_email(auth_service) -> None:
    with pytest.raises(AuthenticationError) as unknown_email_error:
        auth_service.authenticate_user("missing@example.com", "password123")

    assert str(unknown_email_error.value) == "Invalid credentials"


def test_create_login_token_uses_user_id_subject(auth_service) -> None:
    user = auth_service.register_user("user@example.com", "password123")

    token = auth_service.create_login_token(user)
    payload = decode_access_token(token)

    assert payload["sub"] == str(user.id)
    assert "exp" in payload
    assert "role" not in payload


def test_get_current_user_returns_user_for_valid_token(auth_service) -> None:
    created_user = auth_service.register_user("user@example.com", "password123")
    token = auth_service.create_login_token(created_user)

    current_user = auth_service.get_current_user(token)

    assert current_user.id == created_user.id


def test_get_current_user_rejects_invalid_token(auth_service) -> None:
    with pytest.raises(InvalidTokenError):
        auth_service.get_current_user("invalid-token")


def test_require_admin_user_allows_admin(auth_service, user_repository) -> None:
    admin_user = user_repository.create_user(
        email="admin@example.com",
        hashed_password="hashed-value",
        role="admin",
    )

    allowed_user = auth_service.require_admin_user(admin_user)

    assert allowed_user.role == "admin"


def test_require_admin_user_rejects_non_admin(auth_service) -> None:
    user = auth_service.register_user("user@example.com", "password123")

    with pytest.raises(AuthorizationError):
        auth_service.require_admin_user(user)
