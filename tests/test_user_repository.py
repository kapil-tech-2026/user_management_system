from app.core.security import verify_password


def test_create_user_persists_user(user_repository) -> None:
    user = user_repository.create_user(
        email="user@example.com",
        hashed_password="hashed-value",
    )

    assert user.id == 1
    assert user.email == "user@example.com"
    assert user.hashed_password == "hashed-value"
    assert user.is_active is True
    assert user.role == "user"


def test_get_user_by_id_returns_user(user_repository) -> None:
    created_user = user_repository.create_user(
        email="user@example.com",
        hashed_password="hashed-value",
    )

    fetched_user = user_repository.get_user_by_id(created_user.id)

    assert fetched_user is not None
    assert fetched_user.id == created_user.id


def test_get_user_by_email_returns_user(user_repository) -> None:
    user_repository.create_user(
        email="user@example.com",
        hashed_password="hashed-value",
    )

    fetched_user = user_repository.get_user_by_email("user@example.com")

    assert fetched_user is not None
    assert fetched_user.email == "user@example.com"


def test_email_exists_reflects_stored_user(user_repository) -> None:
    user_repository.create_user(
        email="user@example.com",
        hashed_password="hashed-value",
    )

    assert user_repository.email_exists("user@example.com") is True
    assert user_repository.email_exists("missing@example.com") is False


def test_repository_stores_hashed_password_value(auth_service, user_repository) -> None:
    created_user = auth_service.register_user("user@example.com", "password123")
    stored_user = user_repository.get_user_by_id(created_user.id)

    assert stored_user is not None
    assert stored_user.hashed_password != "password123"
    assert verify_password("password123", stored_user.hashed_password) is True
    assert stored_user.role == "user"


def test_create_user_can_persist_admin_role(user_repository) -> None:
    user = user_repository.create_user(
        email="admin@example.com",
        hashed_password="hashed-value",
        role="admin",
    )

    assert user.role == "admin"
