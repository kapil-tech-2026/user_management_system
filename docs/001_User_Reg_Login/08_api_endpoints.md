# Feature 001: User Registration and Login
## 08. API Endpoints

### Purpose

This document defines the API endpoint contract for user registration, login, and authenticated user lookup.

The goal is to finalize the HTTP interface before implementation so that routing, schemas, services, repositories, and tests all follow the same contract.

---

## 1. Endpoint Summary

| Method | Endpoint | Auth Required | Purpose |
|---|---|---:|---|
| POST | `/api/v1/auth/register` | No | Register a new user |
| POST | `/api/v1/auth/login` | No | Authenticate user and return token |
| GET | `/api/v1/auth/me` | Yes | Return current authenticated user |

---

## 2. Base Route

All authentication endpoints should be grouped under:

```text
/api/v1/auth
```

Recommended router setup:

```python
router = APIRouter(prefix="/auth", tags=["Auth"])
```

In `main.py` or API router aggregator:

```python
app.include_router(auth_router, prefix="/api/v1")
```

---

## 3. Endpoint 1: Register User

### Method and Path

```text
POST /api/v1/auth/register
```

### Purpose

Creates a new user account.

### Authentication Required

```text
No
```

### Request Body

Schema:

```text
UserRegisterRequest
```

Example:

```json
{
  "email": "new.user@example.com",
  "password": "StrongPassword123"
}
```

### Success Response

Status code:

```text
201 Created
```

Schema:

```text
UserResponse
```

Example:

```json
{
  "id": 1,
  "email": "new.user@example.com",
  "is_active": true
}
```

### Error Responses

| Status Code | Scenario |
|---:|---|
| 400 or 409 | Email already registered |
| 422 | Invalid request body |
| 500 | Unexpected server error |

### Business Rules

- Email must be unique.
- Password must be hashed before database insert.
- Response must not include password or hashed password.
- New user should default to active unless business rule says otherwise.

---

## 4. Endpoint 2: Login User

### Method and Path

```text
POST /api/v1/auth/login
```

### Purpose

Authenticates a registered user and returns an access token.

### Authentication Required

```text
No
```

### Request Body

Schema:

```text
UserLoginRequest
```

Example:

```json
{
  "email": "new.user@example.com",
  "password": "StrongPassword123"
}
```

### Success Response

Status code:

```text
200 OK
```

Schema:

```text
TokenResponse
```

Example:

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

### Error Responses

| Status Code | Scenario |
|---:|---|
| 401 | Invalid email or password |
| 403 | User account is inactive |
| 422 | Invalid request body |
| 500 | Unexpected server error |

### Business Rules

- Login should not reveal whether email or password was incorrect.
- Invalid credentials should return a generic message.
- Inactive users should not receive tokens.
- Token payload should include enough data to identify the user, usually user ID or subject.

Recommended generic error:

```json
{
  "detail": "Invalid credentials"
}
```

---

## 5. Endpoint 3: Get Current User

### Method and Path

```text
GET /api/v1/auth/me
```

### Purpose

Returns the currently authenticated user.

### Authentication Required

```text
Yes
```

### Request Header

```text
Authorization: Bearer <access_token>
```

### Request Body

```text
None
```

### Success Response

Status code:

```text
200 OK
```

Schema:

```text
UserResponse
```

Example:

```json
{
  "id": 1,
  "email": "new.user@example.com",
  "is_active": true
}
```

### Error Responses

| Status Code | Scenario |
|---:|---|
| 401 | Missing token |
| 401 | Invalid token |
| 401 | Expired token |
| 404 | User from token no longer exists |
| 403 | User account is inactive |

### Business Rules

- Endpoint must require a valid bearer token.
- Token must be decoded and validated.
- User must still exist in the database.
- Response must not expose sensitive fields.

---

## 6. Endpoint Routing File

Recommended file:

```text
app/api/v1/routers/auth.py
```

Expected router functions:

```text
register_user
login_user
get_current_user
```

Example structure:

```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    pass


@router.post("/login", response_model=TokenResponse)
def login_user(payload: UserLoginRequest, db: Session = Depends(get_db)):
    pass


@router.get("/me", response_model=UserResponse)
def get_current_user():
    pass
```

---

## 7. Status Code Decision

Recommended status codes:

| Action | Status |
|---|---:|
| Successful registration | 201 |
| Successful login | 200 |
| Successful current-user lookup | 200 |
| Duplicate email | 409 preferred, 400 acceptable |
| Invalid credentials | 401 |
| Missing/invalid token | 401 |
| Inactive user | 403 |
| Validation error | 422 |

Preferred duplicate email status:

```text
409 Conflict
```

Reason:

The request conflicts with an existing resource.

---

## 8. Authentication Token Contract

Token type:

```text
Bearer
```

Response field:

```text
access_token
```

Header usage:

```text
Authorization: Bearer <access_token>
```

Recommended token payload:

```json
{
  "sub": "1",
  "exp": "token_expiry_timestamp"
}
```

Where:

```text
sub = user id as string
exp = expiration time
```

---

## 9. API Test Cases

The following endpoint tests should be created.

### Registration Tests

```text
POST /api/v1/auth/register
- returns 201 for valid new user
- returns 409 for duplicate email
- returns 422 for invalid email
- returns 422 for missing password
- does not return password or hashed_password
```

### Login Tests

```text
POST /api/v1/auth/login
- returns 200 for valid credentials
- returns access_token and token_type
- returns 401 for wrong password
- returns 401 for unknown email
- does not reveal whether email exists
```

### Current User Tests

```text
GET /api/v1/auth/me
- returns 200 with valid token
- returns 401 without token
- returns 401 with invalid token
- returns 401 with expired token
- does not return sensitive fields
```

---

## 10. API Sign-Off Checklist

Before signing off this API design:

- [ ] Base path is `/api/v1/auth`.
- [ ] Register endpoint is finalized.
- [ ] Login endpoint is finalized.
- [ ] Current user endpoint is finalized.
- [ ] Request schemas are assigned.
- [ ] Response schemas are assigned.
- [ ] Status codes are defined.
- [ ] Error cases are defined.
- [ ] Auth requirement is clear for each endpoint.
- [ ] Test cases are identified.
- [ ] Sensitive fields are not exposed.
