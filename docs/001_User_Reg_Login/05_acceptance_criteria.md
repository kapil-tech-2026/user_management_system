# Feature 001: Acceptance Criteria

## Overview

Acceptance criteria define the specific conditions that must be true before Feature 001 can be considered complete and ready for sign-off.

These criteria should guide implementation, testing, code review, and final approval.

---

## Registration Acceptance Criteria

### AC-001: Successful User Registration

**Given** a user provides a valid email and password  
**When** the user submits a registration request  
**Then** the system creates a new user record  
**And** the response returns public user information  
**And** the response does not include password or hashed password fields.

Expected endpoint:

```text
POST /api/v1/auth/register
```

Expected status code:

```text
201 Created
```

Expected response example:

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true
}
```

---

### AC-002: Duplicate Email Rejection

**Given** a user account already exists with a specific email  
**When** another registration request is submitted with the same email  
**Then** the system rejects the request  
**And** no duplicate user record is created.

Recommended status code:

```text
409 Conflict
```

Expected response example:

```json
{
  "detail": "Email is already registered"
}
```

---

### AC-003: Invalid Email Rejection

**Given** a registration request contains an invalid email format  
**When** the request is submitted  
**Then** the system rejects the request during validation.

Expected status code:

```text
422 Unprocessable Entity
```

---

### AC-004: Missing Password Rejection

**Given** a registration request does not include a password  
**When** the request is submitted  
**Then** the system rejects the request during validation.

Expected status code:

```text
422 Unprocessable Entity
```

---

### AC-005: Password Is Hashed Before Storage

**Given** a user registers with a valid password  
**When** the user record is saved to the database  
**Then** the stored password value is a hash  
**And** the stored value is not equal to the submitted plain-text password.

Verification requirement:

```text
Database hashed_password != original password
```

---

## Login Acceptance Criteria

### AC-006: Successful Login

**Given** a registered active user exists  
**And** the user submits the correct email and password  
**When** the login request is submitted  
**Then** the system authenticates the user  
**And** returns a bearer access token.

Expected endpoint:

```text
POST /api/v1/auth/login
```

Expected status code:

```text
200 OK
```

Expected response example:

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

---

### AC-007: Wrong Password Rejection

**Given** a registered user exists  
**And** the submitted password is incorrect  
**When** the login request is submitted  
**Then** the system rejects the login attempt.

Expected status code:

```text
401 Unauthorized
```

Expected response example:

```json
{
  "detail": "Invalid email or password"
}
```

---

### AC-008: Unknown Email Rejection

**Given** no user exists with the submitted email  
**When** the login request is submitted  
**Then** the system rejects the login attempt.

Expected status code:

```text
401 Unauthorized
```

Expected response example:

```json
{
  "detail": "Invalid email or password"
}
```

The response should not reveal that the email does not exist.

---

## Protected Endpoint Acceptance Criteria

### AC-009: Authenticated User Can Access `/me`

**Given** a user has logged in successfully  
**And** the user has a valid bearer token  
**When** the user requests the current-user endpoint  
**Then** the system returns the authenticated user's public information.

Expected endpoint:

```text
GET /api/v1/auth/me
```

Expected status code:

```text
200 OK
```

Expected response example:

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true
}
```

---

### AC-010: Missing Token Rejection

**Given** a request is made to a protected endpoint without a bearer token  
**When** the request is submitted  
**Then** the system rejects the request.

Expected status code:

```text
401 Unauthorized
```

---

### AC-011: Invalid Token Rejection

**Given** a request is made with an invalid, malformed, or expired token  
**When** the request is submitted to a protected endpoint  
**Then** the system rejects the request.

Expected status code:

```text
401 Unauthorized
```

---

## Architecture Acceptance Criteria

### AC-012: Layered Backend Structure Is Followed

**Given** the feature is implemented  
**When** the code is reviewed  
**Then** the code follows the agreed layered architecture.

Expected structure:

```text
app/api/v1/routers/auth.py
app/schemas/auth.py
app/schemas/user.py
app/services/auth_service.py
app/repositories/user_repository.py
app/models/user.py
app/core/security.py
app/db/database.py
tests/
```

---

### AC-013: Router Does Not Contain Business Logic

**Given** the auth router is reviewed  
**When** route handlers are inspected  
**Then** they should primarily handle request/response behavior  
**And** delegate business logic to the service layer.

---

### AC-014: Repository Handles Database Access

**Given** the user repository is reviewed  
**When** database operations are inspected  
**Then** user lookup and user creation queries are handled in the repository layer.

---

## Testing Acceptance Criteria

### AC-015: Registration Tests Pass

Automated tests must verify:

- Successful registration
- Duplicate email rejection
- Invalid email rejection
- Missing password rejection
- Password is not returned in response
- Password is stored as a hash

---

### AC-016: Login Tests Pass

Automated tests must verify:

- Successful login
- Wrong password rejection
- Unknown email rejection
- Access token is returned on success

---

### AC-017: Protected Endpoint Tests Pass

Automated tests must verify:

- `/me` works with a valid token
- `/me` rejects missing token
- `/me` rejects invalid token

---

## Final Sign-Off Checklist

Feature 001 can be signed off only when all of the following are true:

```text
[ ] Registration endpoint works
[ ] Duplicate email is rejected
[ ] Login endpoint works
[ ] Invalid login is rejected
[ ] Access token is returned on successful login
[ ] Protected endpoint works with valid token
[ ] Protected endpoint rejects missing token
[ ] Protected endpoint rejects invalid token
[ ] Password is hashed in the database
[ ] Password is never returned in API response
[ ] Code follows router/schema/service/repository/model structure
[ ] Automated tests pass
[ ] Feature documentation is updated
```
