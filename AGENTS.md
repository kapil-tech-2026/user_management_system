# AGENTS.md

## Project Context

This repository is a backend learning and implementation project focused on building production-style FastAPI features one feature at a time.

Current active feature:

```text
Feature 001: User Registration and Login
```

The backend should follow a real sprint-style workflow:

```text
requirements -> design -> implementation -> tests -> fixes -> review -> sign-off
```

---

## Primary Tech Stack

Use the following stack unless the repository already clearly uses a different standard:

```text
FastAPI
SQLAlchemy ORM
SQLite for local development
PostgreSQL-ready design
Pydantic
Pytest
JWT authentication
Password hashing
```

---

## Architecture Rules

Follow a layered FastAPI architecture:

```text
router -> schema -> service -> repository -> model -> database
```

Each layer has a clear responsibility.

### Router Layer

Location:

```text
app/api/
app/api/v1/
app/api/v1/routers/
```

Responsibilities:

```text
HTTP request and response handling
status codes
FastAPI dependencies
route definitions
converting service errors to HTTP errors
```

Router files should not contain:

```text
raw SQL queries
direct password hashing logic
large business workflows
database transaction details
```

---

### Schema Layer

Location:

```text
app/schemas/
```

Responsibilities:

```text
Pydantic request validation
Pydantic response models
API contract definitions
safe output shaping
```

Rules:

```text
Never expose password.
Never expose hashed_password.
Use EmailStr for email fields.
Use ORM-compatible response schemas.
Use the Pydantic version already used in the repository.
```

---

### Service Layer

Location:

```text
app/services/
```

Responsibilities:

```text
business logic
registration flow
login flow
password hashing coordination
password verification coordination
token creation coordination
active/inactive user checks
```

Service files should not contain:

```text
route decorators
raw SQL
FastAPI Request or Response objects
database table definitions
```

---

### Repository Layer

Location:

```text
app/repositories/
```

Responsibilities:

```text
database read/write operations
SQLAlchemy queries
database persistence behavior
```

Repository files should not contain:

```text
password hashing
JWT creation
HTTPException unless already established by project convention
Pydantic response shaping
business decision logic
```

---

### Model Layer

Location:

```text
app/models/
```

Responsibilities:

```text
SQLAlchemy ORM models
database table mappings
database constraints
indexes
relationships
```

---

### Database Layer

Location:

```text
app/db/
```

Responsibilities:

```text
database engine
session factory
base model declaration
database dependency
```

Keep database configuration portable between SQLite and PostgreSQL.

---

### Core Layer

Location:

```text
app/core/
```

Responsibilities:

```text
application settings
security utilities
password hashing helpers
JWT helpers
shared configuration
```

Do not hardcode real secrets.

---

## Feature 001 Required Endpoints

Implement the following endpoints:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

---

## Feature 001 Expected Behavior

### Register

Endpoint:

```text
POST /api/v1/auth/register
```

Expected behavior:

```text
Create a new user.
Validate email and password.
Reject duplicate email.
Hash password before storage.
Return safe user response.
Do not return password or hashed_password.
```

Preferred success status:

```text
201 Created
```

Preferred duplicate email status:

```text
409 Conflict
```

---

### Login

Endpoint:

```text
POST /api/v1/auth/login
```

Expected behavior:

```text
Authenticate with email and password.
Return JWT access token.
Return token_type as bearer.
Reject wrong password.
Reject unknown email.
Use the same generic error for wrong password and unknown email.
Do not reveal whether the email exists.
```

Preferred invalid credentials status:

```text
401 Unauthorized
```

Preferred error message:

```json
{
  "detail": "Invalid credentials"
}
```

---

### Current User

Endpoint:

```text
GET /api/v1/auth/me
```

Expected behavior:

```text
Require Authorization: Bearer <token>.
Decode and validate token.
Return current authenticated user.
Reject missing token.
Reject invalid token.
Reject expired token.
Reject inactive user.
Do not return password or hashed_password.
```

---

## Feature 001 Database Requirements

Create a `users` table/model with:

```text
id
email
hashed_password
is_active
created_at
updated_at
```

Rules:

```text
email must be unique
email should be indexed
hashed_password is required
plain password must never be stored
is_active should default to true
created_at and updated_at should be included
```

---

## Feature 001 Schema Requirements

Required request/response schemas:

```text
UserRegisterRequest
UserLoginRequest
UserResponse
TokenResponse
```

Expected fields:

```text
UserRegisterRequest:
- email: EmailStr
- password: str, min length 8, max length 128

UserLoginRequest:
- email: EmailStr
- password: str

UserResponse:
- id: int
- email: EmailStr
- is_active: bool

TokenResponse:
- access_token: str
- token_type: str = "bearer"
```

---

## Feature 001 Repository Requirements

Create a user repository with:

```text
create_user
get_user_by_id
get_user_by_email
email_exists
```

Repository rules:

```text
Use SQLAlchemy session.
Return ORM models or None.
Keep transaction behavior explicit.
Do not hash passwords.
Do not create tokens.
Do not return Pydantic response objects.
```

---

## Feature 001 Service Requirements

Create an auth service with:

```text
register_user
authenticate_user
create_login_token
get_current_user
```

Service rules:

```text
Check duplicate email before creating user.
Hash password before calling repository create method.
Verify password during login.
Use generic invalid credentials behavior.
Reject inactive users.
Create access token with user ID as subject.
Decode token for current-user lookup.
```

---

## Security Requirements

Authentication code is security-sensitive.

Follow these rules:

```text
Never store plain text passwords.
Never return hashed_password in API responses.
Never log plain passwords.
Never log access tokens.
Never commit real secrets.
Never create a real .env file with actual secrets.
Use .env.example for placeholder values only.
```

JWT requirements:

```text
Use a configurable SECRET_KEY.
Use a configurable ALGORITHM.
Use a configurable ACCESS_TOKEN_EXPIRE_MINUTES.
Include sub in token payload.
Include exp in token payload.
Keep token payload minimal.
Do not include password, hashed_password, or sensitive data in token payload.
```

Password requirements:

```text
Use secure hashing.
Provide hash_password().
Provide verify_password().
Do not implement homemade password hashing.
```

---

## Testing Requirements

Use pytest.

Tests should not use the development database.

Use a separate test database and override the database dependency when needed.

Minimum required tests for Feature 001:

```text
register user successfully
reject duplicate email
reject invalid email
reject short password
confirm stored password is hashed
login successfully
reject wrong password
reject unknown email
confirm wrong password and unknown email return same generic error
/me works with valid token
/me rejects missing token
/me rejects invalid token
/me does not expose password or hashed_password
register response does not expose password or hashed_password
```

Do not delete or weaken tests to make the suite pass.

---

## Common Commands

Use the repository's existing commands if they are documented.

If no project-specific commands exist, use these defaults:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_auth_register.py -v
```

Run the FastAPI app locally only if needed:

```bash
uvicorn app.main:app --reload
```

---

## Dependency Management Rules

Before adding dependencies:

```text
Inspect pyproject.toml, requirements.txt, or other package files.
Use the repository's existing dependency management approach.
Do not introduce a second package manager unless necessary.
```

Likely dependencies for Feature 001 may include:

```text
email-validator
python-jose[cryptography]
passlib[bcrypt]
pydantic-settings
```

Only add what the project actually needs.

---

## Implementation Workflow for Codex

Before editing files:

```text
1. Inspect the repository.
2. Identify existing conventions.
3. Summarize current structure.
4. Create a short implementation plan.
5. State assumptions.
```

While editing:

```text
Keep changes focused.
Do not rewrite unrelated files.
Do not change endpoint paths unless required by existing conventions.
Prefer readable code over clever code.
Use type hints where practical.
Preserve existing working tests.
```

After editing:

```text
Run tests.
Fix failing tests.
Run tests again.
Summarize files changed.
Summarize behavior implemented.
Summarize test results.
List any remaining risks or TODOs.
```

---

## Review and Sign-Off Rules

Feature 001 is not complete until:

```text
all required endpoints exist
all required schemas exist
user model exists
repository layer exists
service layer exists
security utilities exist
password hashing works
JWT login works
/me authentication works
sensitive fields are not exposed
test database is isolated
full pytest suite passes
no unrelated rewrites were introduced
no real secrets were committed
```

---

## Human Review Checklist

After Codex completes implementation, verify:

```text
Did the code follow router/schema/service/repository/model/database separation?
Did Codex adapt to the existing repo instead of blindly replacing it?
Are secrets externalized?
Is .env excluded from commits?
Is .env.example safe?
Is password hashing handled only in service/security utilities?
Is hashed_password hidden from all responses?
Do login failures avoid email enumeration?
Are tests meaningful?
Did pytest pass?
```

---

## Future Feature Rule

For future features, reuse the same sprint process:

```text
1. Feature name
2. Business goal
3. Functional requirements
4. Non-functional requirements
5. Acceptance criteria
6. Database changes
7. Pydantic schemas
8. API endpoints
9. Service-layer behavior
10. Repository/database behavior
11. Security considerations
12. Test cases
13. Codex implementation prompt
14. Build result
15. Test result
16. Fix/update notes
17. Sign-off decision
```

Update this file only when a rule should apply repeatedly across the repository.
