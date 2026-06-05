from app.core.security import (
    JWTError,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.exceptions import (
    AuthenticationError,
    AuthorizationError,
    InactiveUserError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register_user(self, email: str, password: str) -> User:
        if self.user_repository.email_exists(email):
            raise UserAlreadyExistsError("A user with this email already exists.")

        hashed_password = hash_password(password)
        return self.user_repository.create_user(
            email=email,
            hashed_password=hashed_password,
            role="user",
        )

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repository.get_user_by_email(email)

        if user is None or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid credentials")

        if not user.is_active:
            raise InactiveUserError("Inactive user")

        return user

    def create_login_token(self, user: User) -> str:
        return create_access_token({"sub": str(user.id)})

    def get_current_user(self, token: str | None) -> User:
        if not token:
            raise InvalidTokenError("Missing token")

        try:
            payload = decode_access_token(token)
        except JWTError as exc:
            raise InvalidTokenError("Invalid or expired token") from exc

        subject = payload.get("sub")
        if subject is None:
            raise InvalidTokenError("Invalid token subject")

        try:
            user_id = int(subject)
        except (TypeError, ValueError) as exc:
            raise InvalidTokenError("Invalid token subject") from exc

        user = self.user_repository.get_user_by_id(user_id)
        if user is None:
            raise UserNotFoundError("User not found")

        if not user.is_active:
            raise InactiveUserError("Inactive user")

        return user

    def require_admin_user(self, user: User) -> User:
        if user.role != "admin":
            raise AuthorizationError("Admin role required")

        return user
