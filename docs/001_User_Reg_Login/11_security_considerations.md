# Feature 001: User Registration and Login
## 11. Security Considerations

### Purpose

This document defines the minimum security requirements for implementing user registration, login, password handling, and token-based authentication.

Authentication features are security-sensitive. Even in a learning project, the design should avoid unsafe habits.

---

## 1. Security Scope for Feature 001

This feature includes:

```text
user registration
password hashing
login credential verification
JWT access token creation
protected current-user endpoint
```

This feature does not yet include:

```text
refresh tokens
password reset
email verification
multi-factor authentication
account lockout
rate limiting
audit logging
role-based access control
```

Those can be introduced in later features.

---

## 2. Password Storage

### Rule

Plain text passwords must never be stored.

The system should only store:

```text
hashed_password
```

### Required Behavior

```text
1. User submits plain password.
2. Service receives password.
3. Service hashes password.
4. Repository stores only hashed password.
5. Plain password is discarded after request processing.
```

---

## 3. Password Hashing

Recommended libraries:

```text
passlib with bcrypt
or
pwdlib / bcrypt-based implementation
```

Expected utility functions:

```python
def hash_password(password: str) -> str:
    ...

def verify_password(plain_password: str, hashed_password: str) -> bool:
    ...
```

Recommended file:

```text
app/core/security.py
```

---

## 4. Password Validation

Minimum requirement for Feature 001:

```text
minimum length: 8
maximum length: 128
```

Optional future rules:

```text
uppercase character
lowercase character
number
special character
password breach checks
password history
```

For the first version, avoid overcomplicating password rules unless the product requires it.

---

## 5. Login Error Message

The login endpoint should not reveal whether the email exists.

Avoid:

```json
{
  "detail": "Email does not exist"
}
```

Avoid:

```json
{
  "detail": "Password is incorrect"
}
```

Use:

```json
{
  "detail": "Invalid credentials"
}
```

Reason:

Revealing whether an email exists can help attackers enumerate registered accounts.

---

## 6. Token Type

Use bearer token authentication.

Client sends:

```text
Authorization: Bearer <access_token>
```

API returns:

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

---

## 7. JWT Payload

Recommended access token payload:

```json
{
  "sub": "user_id",
  "exp": "expiration_timestamp"
}
```

Rules:

- `sub` should identify the user.
- `exp` should define token expiration.
- Do not store password or sensitive personal data in the token.
- Keep token payload minimal.

---

## 8. Token Expiration

Access tokens should expire.

Recommended starting value:

```text
30 minutes
```

Configurable setting:

```text
ACCESS_TOKEN_EXPIRE_MINUTES
```

This should be defined in environment/config settings, not hardcoded across the application.

---

## 9. Secret Key Management

JWT signing requires a secret key.

Rules:

- Do not hardcode production secrets in source code.
- Do not commit `.env` files to GitHub.
- Use environment variables for secrets.
- Provide `.env.example` without real secrets.

Recommended config names:

```text
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```

Example `.env.example`:

```text
SECRET_KEY=replace-with-secure-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 10. Sensitive Fields

The API must never return:

```text
password
hashed_password
```

Sensitive fields should not appear in:

```text
registration response
login response
/me response
error response
logs
test snapshots
```

---

## 11. Protected Endpoint Requirement

The endpoint below must require a valid token:

```text
GET /api/v1/auth/me
```

Required behavior:

```text
missing token -> 401
invalid token -> 401
expired token -> 401
inactive user -> 403
valid token -> 200
```

---

## 12. Account Active Status

The `users` table includes:

```text
is_active
```

Rules:

- Inactive users should not be allowed to log in.
- Inactive users should not be allowed to access `/me`.
- Inactive behavior should return `403 Forbidden`.

---

## 13. Duplicate Email Protection

Duplicate email protection should exist in both:

```text
service layer
database constraint
```

Reason:

The service layer provides a clean user-facing error.

The database constraint protects data integrity under concurrent requests.

---

## 14. CORS

If this backend will be used by a frontend application later, CORS should be configured carefully.

For local development:

```text
http://localhost:3000
http://localhost:5173
```

Avoid allowing all origins in production.

---

## 15. Logging

Do not log:

```text
plain passwords
hashed passwords
access tokens
authorization headers
secret keys
```

Safe logs may include:

```text
registration attempt status
login success/failure status
user ID after authentication
high-level error messages
```

---

## 16. Rate Limiting

Rate limiting is out of scope for Feature 001 implementation but should be considered later.

Important future endpoints for rate limiting:

```text
POST /api/v1/auth/login
POST /api/v1/auth/register
POST /api/v1/auth/password-reset
```

---

## 17. Security Testing Requirements

Security-related test cases should verify:

```text
password is hashed
plain password is not stored
hashed_password is not returned
wrong password returns 401
unknown email returns 401
login error message is generic
/me requires token
invalid token is rejected
```

---

## 18. Security Sign-Off Checklist

Before signing off this feature:

- [ ] Plain text password is never stored.
- [ ] Password is hashed before database insert.
- [ ] Password verification uses secure hash comparison.
- [ ] Login error does not reveal whether email exists.
- [ ] JWT contains minimal payload.
- [ ] JWT includes expiration.
- [ ] Secret key comes from configuration.
- [ ] `.env` is not committed.
- [ ] `hashed_password` is never returned.
- [ ] `/me` requires bearer token.
- [ ] Inactive users are blocked.
- [ ] Duplicate email is protected by service and database.
