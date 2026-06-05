# Feature 001: Non-Functional Requirements

## Overview

Non-functional requirements define the expected quality, security, maintainability, reliability, and development standards for the registration and login feature.

## Security Requirements

### NFR-001: Password Security

Passwords must never be stored in plain text.

Requirements:

- Use a secure password hashing algorithm.
- Store only `hashed_password` in the database.
- Never expose `hashed_password` in API responses.
- Never log raw passwords.

Recommended implementation area:

```text
app/core/security.py
```

---

### NFR-002: Token Security

Authentication tokens must be generated using a server-side secret and an expiration policy.

Requirements:

- Token must include enough information to identify the user.
- Token must have an expiration time.
- Token secret must be read from configuration or environment variables.
- Token validation must happen before protected endpoints return data.

---

### NFR-003: Login Error Safety

Login failure messages should not reveal whether the email exists.

Preferred error message:

```json
{
  "detail": "Invalid email or password"
}
```

Avoid:

```json
{
  "detail": "Email not found"
}
```

Reason: revealing which emails are registered can create account enumeration risk.

---

## Architecture Requirements

### NFR-004: Layered FastAPI Structure

The implementation must follow a layered backend structure.

Required layers:

```text
Router
Schema
Service
Repository
Model
Database
Core utilities
Tests
```

Route handlers should remain thin. Business logic should not be written directly inside routers.

---

### NFR-005: Separation of Concerns

Each layer must have a clear responsibility.

```text
Router        -> HTTP behavior
Schema        -> validation and serialization
Service       -> business logic
Repository    -> database operations
Model         -> SQLAlchemy table mapping
Core          -> config, hashing, token utilities
```

This improves testability and keeps future features maintainable.

---

### NFR-006: PostgreSQL-Ready Design

The application will use SQLite during early development but should be designed so PostgreSQL can be introduced later with minimal changes.

Requirements:

- Use SQLAlchemy ORM.
- Avoid raw SQLite-specific SQL where possible.
- Keep database URL configurable.
- Use standard column types that translate well to PostgreSQL.
- Keep future Alembic migration support in mind.

---

## Validation Requirements

### NFR-007: Request Validation

Input validation should be handled through Pydantic schemas.

Requirements:

- Email must be validated as an email address.
- Password must be required.
- Request models should reject invalid data before service logic runs.

---

### NFR-008: Response Safety

Response schemas must control what fields are returned to the client.

Requirements:

- User response must include public fields only.
- Password fields must be excluded from response schemas.
- Internal database fields should not leak accidentally.

---

## Reliability Requirements

### NFR-009: Predictable Status Codes

The API should return consistent HTTP status codes.

Recommended status codes:

```text
201 Created        -> successful registration
200 OK             -> successful login
401 Unauthorized   -> invalid login or missing/invalid token
409 Conflict       -> duplicate email registration
422 Unprocessable  -> request validation failure
```

---

### NFR-010: Transaction Safety

Database operations should commit only when the operation is valid.

Requirements:

- Do not create a user if validation fails.
- Do not create a duplicate user.
- Roll back failed database operations when necessary.

---

## Testability Requirements

### NFR-011: Automated Test Coverage

The feature must include automated tests for both success and failure cases.

Minimum test categories:

```text
Registration tests
Login tests
Protected endpoint tests
Repository/service behavior tests where appropriate
```

---

### NFR-012: Test Database Isolation

Tests should not use the production or development database directly.

Requirements:

- Use a separate test database.
- Reset test data between tests or test sessions.
- Override FastAPI database dependencies during tests if needed.

---

## Maintainability Requirements

### NFR-013: Consistent Naming

Files, classes, functions, and schemas should follow clear naming conventions.

Examples:

```text
User
UserCreate
UserRead
UserRepository
AuthService
register_user
authenticate_user
```

---

### NFR-014: Minimal Route Logic

Routers should call service functions instead of directly handling database queries or password logic.

Avoid this pattern:

```text
router -> database query -> hash password -> commit
```

Preferred pattern:

```text
router -> service -> repository -> database
```

---

### NFR-015: Configurable Settings

Security-sensitive and environment-specific values should be configurable.

Examples:

```text
DATABASE_URL
SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES
ALGORITHM
```

These should not be hardcoded directly inside route files.

---

## Performance Requirements

### NFR-016: Reasonable Authentication Response Time

Registration and login should complete within a reasonable response time for normal usage.

This feature does not require advanced optimization, but it should avoid unnecessary repeated database queries.

---

## Documentation Requirements

### NFR-017: Feature Documentation

The feature should include planning and implementation documentation sufficient for another developer to understand:

- What the feature does
- What endpoints exist
- What database tables are involved
- What tests prove the feature works
- What is out of scope

---

## Sign-Off Quality Bar

The feature should not be signed off until:

- All acceptance criteria pass.
- All automated tests pass.
- Passwords are confirmed to be hashed.
- Password fields are not returned in API responses.
- Protected endpoints reject unauthenticated requests.
- Project structure remains clean and layered.
