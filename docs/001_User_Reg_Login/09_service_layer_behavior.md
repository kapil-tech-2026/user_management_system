# Feature 001: User Registration and Login
## 09. Service-Layer Behavior

### Purpose

This document defines the business logic that belongs in the service layer for user registration, login, and authenticated user retrieval.

The service layer should coordinate validation, repository calls, password hashing, password verification, token creation, and business rule enforcement.

---

## 1. Service Layer Role

The service layer should answer this question:

```text
What should the application do?
```

It should not directly handle HTTP request/response details and should not contain raw database query logic.

---

## 2. Recommended File

```text
app/services/auth_service.py
```

---

## 3. Main Service Class

Recommended class:

```python
class AuthService:
    ...
```

The service can be implemented either as:

```text
Option A: Class with static methods
Option B: Class initialized with repository
Option C: Plain functions
```

Recommended for learning and clean architecture:

```text
Option B: Class initialized with repository
```

This makes the service easier to test and prepares the project for dependency injection.

---

## 4. Required Service Methods

```text
register_user
authenticate_user
create_login_token
get_current_user
```

Optional helper methods:

```text
validate_new_user_email
validate_user_is_active
```

---

## 5. Method: register_user

### Purpose

Creates a new user account.

### Inputs

```text
email
password
database session or repository instance
```

### Output

```text
User model or UserResponse-compatible object
```

### Behavior

```text
1. Normalize email if needed.
2. Check whether email already exists.
3. If email exists, raise duplicate email error.
4. Hash the plain password.
5. Create user through repository.
6. Return created user.
```

### Business Rules

- Email must be unique.
- Password must never be stored as plain text.
- Password hashing must happen before database insert.
- Created user should default to active.
- Response must not expose `hashed_password`.

### Pseudocode

```python
def register_user(payload):
    existing_user = user_repository.get_by_email(payload.email)

    if existing_user:
        raise DuplicateEmailError("Email already registered")

    hashed_password = hash_password(payload.password)

    user = user_repository.create(
        email=payload.email,
        hashed_password=hashed_password,
    )

    return user
```

---

## 6. Method: authenticate_user

### Purpose

Validates login credentials.

### Inputs

```text
email
password
```

### Output

```text
Authenticated user model
```

### Behavior

```text
1. Find user by email.
2. If user does not exist, raise invalid credentials error.
3. Verify submitted password against stored hash.
4. If password does not match, raise invalid credentials error.
5. Check whether user is active.
6. Return authenticated user.
```

### Business Rules

- Do not reveal whether email or password was incorrect.
- Use a generic error message for failed login.
- Inactive users should not be authenticated.

### Recommended Generic Error

```text
Invalid credentials
```

### Pseudocode

```python
def authenticate_user(email, password):
    user = user_repository.get_by_email(email)

    if not user:
        raise InvalidCredentialsError("Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError("Invalid credentials")

    if not user.is_active:
        raise InactiveUserError("User account is inactive")

    return user
```

---

## 7. Method: create_login_token

### Purpose

Creates an access token after successful authentication.

### Inputs

```text
user
```

### Output

```text
access token string
```

### Behavior

```text
1. Read user ID.
2. Create token payload.
3. Add expiration.
4. Sign token.
5. Return token.
```

### Recommended Token Payload

```json
{
  "sub": "user_id",
  "exp": "expiration_timestamp"
}
```

### Pseudocode

```python
def create_login_token(user):
    token_data = {"sub": str(user.id)}
    access_token = create_access_token(data=token_data)
    return access_token
```

---

## 8. Method: get_current_user

### Purpose

Returns the user associated with a valid access token.

### Inputs

```text
token
```

### Output

```text
User model
```

### Behavior

```text
1. Decode token.
2. Extract subject/user ID.
3. Validate token payload.
4. Retrieve user from repository.
5. If user does not exist, raise authentication error.
6. If user is inactive, raise authorization error.
7. Return user.
```

### Pseudocode

```python
def get_current_user(token):
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise AuthenticationError("Invalid token")

    user = user_repository.get_by_id(int(user_id))

    if not user:
        raise AuthenticationError("Invalid token")

    if not user.is_active:
        raise InactiveUserError("User account is inactive")

    return user
```

---

## 9. Error Handling Strategy

The service layer can raise custom domain exceptions.

Recommended exceptions:

```text
DuplicateEmailError
InvalidCredentialsError
InactiveUserError
InvalidTokenError
UserNotFoundError
```

The router layer should convert these into HTTP responses.

Example:

| Service Exception | HTTP Status |
|---|---:|
| DuplicateEmailError | 409 |
| InvalidCredentialsError | 401 |
| InactiveUserError | 403 |
| InvalidTokenError | 401 |
| UserNotFoundError | 404 or 401 depending on context |

---

## 10. Service Layer Should Not Do

The service layer should not:

- Directly return FastAPI `Response` objects.
- Know endpoint paths.
- Contain route decorators.
- Contain raw SQL.
- Expose password hashes.
- Store plain text passwords.
- Parse HTTP headers directly.

---

## 11. Service Dependencies

The service layer may depend on:

```text
UserRepository
password hashing utility
JWT/token utility
configuration settings
```

Recommended utility files:

```text
app/core/security.py
app/core/config.py
```

---

## 12. Example Service Flow: Registration

```text
Router receives request
↓
Pydantic validates request
↓
Router calls AuthService.register_user()
↓
Service checks duplicate email
↓
Service hashes password
↓
Service calls UserRepository.create_user()
↓
Repository saves user
↓
Service returns user
↓
Router returns UserResponse
```

---

## 13. Example Service Flow: Login

```text
Router receives request
↓
Pydantic validates request
↓
Router calls AuthService.authenticate_user()
↓
Service finds user by email
↓
Service verifies password
↓
Service checks active status
↓
Service creates access token
↓
Router returns TokenResponse
```

---

## 14. Service-Layer Sign-Off Checklist

Before signing off service-layer behavior:

- [ ] Registration business flow is defined.
- [ ] Login business flow is defined.
- [ ] Current-user flow is defined.
- [ ] Password hashing responsibility is assigned.
- [ ] Password verification responsibility is assigned.
- [ ] Token creation responsibility is assigned.
- [ ] Duplicate email behavior is defined.
- [ ] Invalid credential behavior is defined.
- [ ] Inactive user behavior is defined.
- [ ] Service layer does not contain HTTP route logic.
- [ ] Service layer does not contain raw database queries.
