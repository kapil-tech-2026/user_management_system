class AuthServiceError(Exception):
    """Base exception for auth service failures."""


class UserAlreadyExistsError(AuthServiceError):
    """Raised when attempting to register an existing email."""


class AuthenticationError(AuthServiceError):
    """Raised for generic invalid credential failures."""


class InactiveUserError(AuthServiceError):
    """Raised when an inactive user attempts authentication."""


class InvalidTokenError(AuthServiceError):
    """Raised when a token is missing, invalid, or expired."""


class UserNotFoundError(AuthServiceError):
    """Raised when a referenced user no longer exists."""
