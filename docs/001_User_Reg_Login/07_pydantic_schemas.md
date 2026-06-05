# Feature 001: User Registration and Login
## 07. Pydantic Schemas

### Purpose

This document defines the Pydantic schemas required for user registration, login, token response, and authenticated user response.

Schemas define the API contract between client and backend. They should validate incoming data and control what data is returned to the client.

---

## 1. Schema Design Principles

For this feature, schemas should follow these rules:

- Request schemas validate user input.
- Response schemas hide sensitive fields.
- Password should appear only in request schemas.
- `hashed_password` should never appear in API responses.
- Token response should use a clear format.
- Schemas should be reusable across routers and tests.

---

## 2. Required Schema Files

Recommended file structure:

```text
app/
  schemas/
    auth.py
    user.py
```

Alternative for small projects:

```text
app/
  schemas/
    auth_schema.py
    user_schema.py
```

Preferred naming for this project:

```text
auth.py
user.py
```

---

## 3. User Registration Request Schema

### Schema Name

```text
UserRegisterRequest
```

### Purpose

Validates data submitted when a new user registers.

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| email | EmailStr | Yes | User email address |
| password | str | Yes | Plain password submitted by user |

### Draft

```python
from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
```

### Notes

The password is accepted in plain text only at the request boundary. It must be hashed in the service layer before being stored.

---

## 4. User Login Request Schema

### Schema Name

```text
UserLoginRequest
```

### Purpose

Validates login credentials.

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| email | EmailStr | Yes | Registered user email |
| password | str | Yes | Submitted password |

### Draft

```python
from pydantic import BaseModel, EmailStr, Field


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)
```

### Notes

For login, password complexity does not need to be revalidated. The system only needs to verify whether the submitted password matches the stored hash.

---

## 5. User Response Schema

### Schema Name

```text
UserResponse
```

### Purpose

Defines safe user data returned from the API.

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| id | int | Yes | User ID |
| email | EmailStr | Yes | User email |
| is_active | bool | Yes | Account status |

### Draft for Pydantic v2

```python
from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
```

### Draft for Pydantic v1

```python
from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
```

### Preferred Version

Use the Pydantic version already installed in the project.

For modern FastAPI projects, Pydantic v2 is preferred unless the project has a reason to stay on v1.

---

## 6. Token Response Schema

### Schema Name

```text
TokenResponse
```

### Purpose

Defines the response returned after successful login.

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| access_token | str | Yes | JWT access token |
| token_type | str | Yes | Usually `bearer` |

### Draft

```python
from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

---

## 7. Authenticated User Response

The `/me` endpoint can reuse:

```text
UserResponse
```

Example:

```python
@router.get("/me", response_model=UserResponse)
```

This avoids creating unnecessary duplicate schemas.

---

## 8. Optional Error Response Schema

FastAPI can return error responses using `HTTPException`.

An optional shared error schema can be created later:

```python
class ErrorResponse(BaseModel):
    detail: str
```

This is useful for documentation, but not required for the first implementation.

---

## 9. Password Validation Rules

Minimum recommended registration password rule:

```text
minimum length: 8
maximum length: 128
```

Optional future rules:

- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

For Feature 001, keep password validation simple unless stricter security requirements are added.

---

## 10. Schema Responsibility Boundaries

| Schema | Responsibility |
|---|---|
| UserRegisterRequest | Validate registration input |
| UserLoginRequest | Validate login input |
| UserResponse | Return safe user information |
| TokenResponse | Return authentication token |

---

## 11. Fields That Must Not Be Returned

The following fields must never be returned in public API responses:

```text
password
hashed_password
```

Even though `hashed_password` is not the raw password, it is still sensitive and must remain internal.

---

## 12. Example Request and Response Contracts

### Register Request

```json
{
  "email": "new.user@example.com",
  "password": "StrongPassword123"
}
```

### Register Response

```json
{
  "id": 1,
  "email": "new.user@example.com",
  "is_active": true
}
```

### Login Request

```json
{
  "email": "new.user@example.com",
  "password": "StrongPassword123"
}
```

### Login Response

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

### Me Response

```json
{
  "id": 1,
  "email": "new.user@example.com",
  "is_active": true
}
```

---

## 13. Pydantic Schema Sign-Off Checklist

Before signing off this schema design:

- [ ] Registration request schema exists.
- [ ] Login request schema exists.
- [ ] User response schema exists.
- [ ] Token response schema exists.
- [ ] Email uses `EmailStr`.
- [ ] Password has basic length validation.
- [ ] `hashed_password` is never exposed.
- [ ] `/me` can reuse `UserResponse`.
- [ ] Schema version matches installed Pydantic version.
