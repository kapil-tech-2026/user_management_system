# Feature 001: Functional Requirements

## Overview

Functional requirements define what the registration and login feature must do from the perspective of users, API behavior, and backend processing.

## Registration Requirements

### FR-001: Register a New User

The system shall allow a new user to register using an email address and password.

Minimum required input:

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
```

Expected behavior:

- Validate the email format.
- Validate that the password is present.
- Check that the email is not already registered.
- Hash the password before saving.
- Create a new user record in the database.
- Return a response that does not include the password or password hash.

---

### FR-002: Enforce Unique Email

The system shall reject registration if the email is already associated with an existing user account.

Expected behavior:

- Return a clear error response.
- Do not create a duplicate user record.
- Preserve the existing user record unchanged.

Recommended status code:

```text
409 Conflict
```

Alternative acceptable status code:

```text
400 Bad Request
```

---

### FR-003: Store Hashed Password Only

The system shall never store plain-text passwords.

Expected behavior:

- Convert the provided password into a secure hash.
- Store only the hashed password in the database.
- Never return the hash in an API response.

---

### FR-004: Return Registered User Information

After successful registration, the system shall return basic user information.

Example response:

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true
}
```

Response must not include:

```text
password
hashed_password
```

---

## Login Requirements

### FR-005: Authenticate Existing User

The system shall allow an existing user to log in using email and password.

Minimum required input:

```json
{
  "email": "user@example.com",
  "password": "StrongPassword123"
}
```

Expected behavior:

- Locate the user by email.
- Verify the submitted password against the stored hash.
- Return an access token if credentials are valid.
- Reject the request if credentials are invalid.

---

### FR-006: Reject Invalid Login Credentials

The system shall reject login attempts when:

- The email does not exist.
- The password is incorrect.
- The user account is inactive.

Recommended status code:

```text
401 Unauthorized
```

Recommended response:

```json
{
  "detail": "Invalid email or password"
}
```

The response should not reveal whether the email or password was incorrect.

---

### FR-007: Return Access Token on Successful Login

After successful login, the system shall return an access token.

Example response:

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

---

## Authenticated User Requirements

### FR-008: Get Current Authenticated User

The system shall provide a protected endpoint that returns the currently authenticated user's information.

Endpoint candidate:

```text
GET /api/v1/auth/me
```

Expected behavior:

- Require a valid bearer token.
- Decode and validate the token.
- Retrieve the user from the database.
- Return the authenticated user's public information.

Example response:

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true
}
```

---

### FR-009: Reject Requests Without Token

The system shall reject access to protected endpoints when no token is provided.

Recommended status code:

```text
401 Unauthorized
```

---

### FR-010: Reject Requests With Invalid Token

The system shall reject access to protected endpoints when the token is invalid, expired, malformed, or refers to a user that no longer exists.

Recommended status code:

```text
401 Unauthorized
```

---

## User Data Requirements

### FR-011: User Record Fields

The system shall create and maintain a user record with at least the following fields:

```text
id
email
hashed_password
is_active
created_at
updated_at
```

---

### FR-012: Default User Status

Newly registered users shall be active by default unless future business rules define email verification or admin approval.

Initial default:

```text
is_active = true
```

---

## Error Handling Requirements

### FR-013: Return Consistent Error Responses

The system shall return clear and consistent error responses for validation, duplicate registration, invalid login, and unauthorized access.

Example:

```json
{
  "detail": "Invalid email or password"
}
```

---

## Testing Requirements

### FR-014: Automated Registration Tests

The system shall include automated tests for:

- Successful registration
- Duplicate email rejection
- Invalid email rejection
- Missing password rejection
- Password not returned in response
- Password stored as hash

---

### FR-015: Automated Login Tests

The system shall include automated tests for:

- Successful login
- Invalid password rejection
- Unknown email rejection
- Access token returned on success

---

### FR-016: Automated Protected Endpoint Tests

The system shall include automated tests for:

- Access `/me` with valid token
- Reject `/me` without token
- Reject `/me` with invalid token
