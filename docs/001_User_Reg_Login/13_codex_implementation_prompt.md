# Feature 001: User Registration and Login
## 13. Step-by-Step Codex Implementation Prompt

### Purpose

This document provides a step-by-step implementation prompt that can be given to Codex to build **Feature 001: User Registration and Login** in a production-style FastAPI backend.

The prompt is designed to make Codex follow the same feature-development process used in the planning documents:

```text
1. Understand existing project
2. Confirm target architecture
3. Implement database/model layer
4. Implement Pydantic schemas
5. Implement repository layer
6. Implement service layer
7. Implement security utilities
8. Implement API router
9. Add tests
10. Run tests
11. Fix issues
12. Provide implementation summary
```

---

## 1. Feature Context for Codex

### Feature Name

```text
Feature 001: User Registration and Login
```

### Backend Stack

```text
FastAPI
SQLite for local development
SQLAlchemy ORM
Pydantic
Pytest
JWT-based authentication
Password hashing
```

### Architecture Style

The backend should follow a layered FastAPI architecture:

```text
router -> schema -> service -> repository -> model -> database
```

### Main Goal

Implement a complete user registration and login feature with:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

---

## 2. Recommended Repository Context Files

Before implementation, Codex should inspect these files if they exist:

```text
README.md
AGENTS.md
pyproject.toml
requirements.txt
.env.example
app/main.py
app/db/database.py
app/db/base.py
app/models/
app/schemas/
app/repositories/
app/services/
app/api/
tests/
```

If any required folder does not exist, Codex should create it using the structure defined below.

---

## 3. Target Project Structure

Codex should implement or update the project toward this structure:

```text
app/
  main.py

  core/
    config.py
    security.py

  db/
    database.py
    base.py

  models/
    user.py

  schemas/
    auth.py
    user.py

  repositories/
    user_repository.py

  services/
    auth_service.py

  api/
    v1/
      api.py
      routers/
        auth.py

tests/
  conftest.py
  test_auth_register.py
  test_auth_login.py
  test_auth_me.py
  test_user_repository.py
  test_auth_service.py
```

If the repository already has a different but clean structure, Codex should adapt to the existing structure instead of blindly replacing it.

---

# 4. Master Codex Prompt

Copy and paste the following prompt into Codex.

---

## Codex Prompt

```text
You are working on a FastAPI backend project.

Your task is to implement Feature 001: User Registration and Login.

Follow a professional backend sprint workflow:
1. Inspect the existing repository structure.
2. Identify the current FastAPI entrypoint, database setup, dependency pattern, test setup, and package management.
3. Create a short implementation plan before editing files.
4. Implement the feature using layered architecture.
5. Add tests.
6. Run tests.
7. Fix any failing tests.
8. Provide a final summary of files changed, tests run, and remaining notes.

Feature requirements:

Functional requirements:
- A user can register with email and password.
- Email must be unique.
- Password must be hashed before storage.
- A user can log in with valid email and password.
- Invalid login must return a generic invalid credentials error.
- Successful login must return an access token and token type.
- A protected /me endpoint must return the current authenticated user.
- The API must not expose password or hashed_password in responses.

Non-functional requirements:
- Use FastAPI.
- Use SQLAlchemy ORM.
- Use SQLite for local development, but keep the design portable to PostgreSQL.
- Use Pydantic schemas for request and response validation.
- Use repository and service layers.
- Use pytest for tests.
- Keep code modular and readable.
- Do not hardcode secrets in source code.
- Do not commit or create a real .env file with secrets.
- Use .env.example for placeholder configuration only.

Required endpoints:
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me

Expected endpoint behavior:

1. POST /api/v1/auth/register
Request:
{
  "email": "new.user@example.com",
  "password": "StrongPassword123"
}

Success:
- Status code: 201
- Response body:
{
  "id": 1,
  "email": "new.user@example.com",
  "is_active": true
}

Failure:
- Duplicate email: 409 Conflict preferred
- Invalid request body: 422

2. POST /api/v1/auth/login
Request:
{
  "email": "new.user@example.com",
  "password": "StrongPassword123"
}

Success:
- Status code: 200
- Response body:
{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}

Failure:
- Wrong password: 401
- Unknown email: 401
- Use the same generic error message for both:
{
  "detail": "Invalid credentials"
}

3. GET /api/v1/auth/me
Header:
Authorization: Bearer <access_token>

Success:
- Status code: 200
- Response body:
{
  "id": 1,
  "email": "new.user@example.com",
  "is_active": true
}

Failure:
- Missing token: 401
- Invalid token: 401
- Expired token: 401
- Inactive user: 403

Database requirements:
- Create a users table/model.
- Fields:
  - id: integer primary key
  - email: string, unique, indexed, required
  - hashed_password: string, required
  - is_active: boolean, default true
  - created_at: datetime
  - updated_at: datetime
- Do not store plain text passwords.
- Enforce unique email at the database level.

Pydantic schema requirements:
- UserRegisterRequest
  - email: EmailStr
  - password: str, min length 8, max length 128
- UserLoginRequest
  - email: EmailStr
  - password: str
- UserResponse
  - id: int
  - email: EmailStr
  - is_active: bool
  - ORM-compatible config
- TokenResponse
  - access_token: str
  - token_type: str = "bearer"

Repository requirements:
Create a user repository with methods:
- create_user
- get_user_by_id
- get_user_by_email
- email_exists

Repository rules:
- Repository should contain database query logic.
- Repository should not hash passwords.
- Repository should not create JWT tokens.
- Repository should not raise FastAPI HTTPException unless the existing project convention already does that.

Service requirements:
Create an auth service with behavior for:
- register_user
- authenticate_user
- create_login_token
- get_current_user

Service rules:
- Service should contain business logic.
- Service should hash passwords before creating users.
- Service should verify passwords during login.
- Service should create JWT access tokens.
- Service should check inactive users.
- Service should avoid revealing whether login failed because of email or password.

Security requirements:
- Use secure password hashing.
- Add security helper functions:
  - hash_password
  - verify_password
  - create_access_token
  - decode_access_token or equivalent
- JWT payload should include:
  - sub: user ID as string
  - exp: expiration timestamp
- Do not include password, hashed_password, or sensitive personal data in the token.
- Secret key, algorithm, and expiry should come from config.
- Provide safe defaults for local development only if appropriate.
- Add .env.example if missing.

Testing requirements:
Add tests for the following minimum cases:
1. Register user successfully.
2. Reject duplicate email.
3. Reject invalid email.
4. Reject short password.
5. Confirm stored password is hashed.
6. Login successfully.
7. Reject wrong password.
8. Reject unknown email.
9. Confirm wrong password and unknown email return the same generic error.
10. /me works with a valid token.
11. /me rejects missing token.
12. /me rejects invalid token.
13. /me response does not expose password or hashed_password.
14. Register response does not expose password or hashed_password.

Testing rules:
- Use pytest.
- Use FastAPI TestClient or the existing test client pattern.
- Use a separate test database.
- Override the database dependency for tests if needed.
- Tests must not use the development database.
- Run the full test suite before final response.

Implementation rules:
- Do not rewrite unrelated parts of the project.
- Do not change public endpoint paths unless the existing project has a clear versioning convention.
- Preserve existing working tests.
- Keep changes small and focused.
- Prefer readable code over clever code.
- Use type hints where practical.
- Add comments only where they clarify non-obvious behavior.
- Do not expose secret values.
- Do not create a real .env file with real secrets.

Deliverables:
- Updated FastAPI app with auth endpoints.
- SQLAlchemy user model.
- Pydantic schemas.
- User repository.
- Auth service.
- Security utilities.
- Tests.
- Updated .env.example if needed.
- Final implementation summary.

Before editing, show:
- Existing structure found.
- Implementation plan.
- Any assumptions.

After editing, show:
- Files created/modified.
- Tests run.
- Test results.
- Any remaining risks or TODOs.

Start by inspecting the repository and creating an implementation plan.
```

---

# 5. Step-by-Step Codex Execution Plan

The master prompt above can be used once. However, for stronger control, the implementation can also be split into smaller Codex tasks.

---

## Step 1: Repository Inspection Prompt

### Prompt

```text
Inspect this FastAPI repository and summarize the current backend structure.

Focus on:
- app entrypoint
- database setup
- SQLAlchemy setup
- Pydantic version
- existing routers
- existing dependency injection pattern
- current test setup
- package/dependency management
- whether AGENTS.md exists

Do not edit files yet.

Return:
1. Current structure summary
2. Gaps for Feature 001: User Registration and Login
3. Recommended implementation plan
4. Any assumptions
```

### Expected Outcome

Codex should return:

```text
- Current project structure summary
- Existing files that can be reused
- Missing files/folders
- Dependency gaps
- Test setup status
- Clear implementation plan
```

### Sign-Off Before Next Step

Proceed only when the plan is reasonable and does not propose unrelated rewrites.

---

## Step 2: Database and Model Prompt

### Prompt

```text
Implement the database/model foundation for Feature 001.

Tasks:
1. Ensure SQLAlchemy database setup exists.
2. Create or update app/db/database.py.
3. Create or update app/db/base.py.
4. Create app/models/user.py.
5. Define a User model with:
   - id
   - email
   - hashed_password
   - is_active
   - created_at
   - updated_at
6. Ensure email is unique and indexed.
7. Keep SQLite compatibility and PostgreSQL readiness.
8. Do not implement routes yet.
9. Do not implement login yet.

After changes, show:
- Files changed
- Model fields created
- Any assumptions
```

### Expected Outcome

Codex should create or update:

```text
app/db/database.py
app/db/base.py
app/models/user.py
```

The project should now have a valid SQLAlchemy `User` model.

---

## Step 3: Pydantic Schema Prompt

### Prompt

```text
Implement Pydantic schemas for Feature 001.

Create or update:
- app/schemas/auth.py
- app/schemas/user.py

Required schemas:
1. UserRegisterRequest
   - email: EmailStr
   - password: str with min_length=8 and max_length=128

2. UserLoginRequest
   - email: EmailStr
   - password: str

3. UserResponse
   - id: int
   - email: EmailStr
   - is_active: bool
   - compatible with ORM model serialization

4. TokenResponse
   - access_token: str
   - token_type: str default "bearer"

Rules:
- Do not expose password or hashed_password in response schemas.
- Use the Pydantic version already used in the project.
- Do not implement routes yet.

After changes, show:
- Files changed
- Schemas created
- Pydantic version assumptions
```

### Expected Outcome

Codex should create safe request and response schemas without exposing sensitive fields.

---

## Step 4: Security Utility Prompt

### Prompt

```text
Implement security utilities for Feature 001.

Create or update:
- app/core/config.py
- app/core/security.py

Required behavior:
1. Load SECRET_KEY, ALGORITHM, and ACCESS_TOKEN_EXPIRE_MINUTES from config.
2. Provide safe local-development defaults only if the project convention allows it.
3. Do not create or commit a real .env file.
4. Add or update .env.example with placeholder values if missing.
5. Implement:
   - hash_password(password: str) -> str
   - verify_password(plain_password: str, hashed_password: str) -> bool
   - create_access_token(data: dict, expires_delta: optional) -> str
   - decode_access_token(token: str) -> dict or equivalent
6. JWT should include an expiration.
7. JWT subject should use the user ID as a string.
8. Do not put password or hashed_password in token payload.

After changes, show:
- Files changed
- Security helpers created
- Dependency additions needed
- Config variables added
```

### Expected Outcome

Codex should implement reusable security helpers for password hashing and JWT token handling.

Expected files:

```text
app/core/config.py
app/core/security.py
.env.example
```

Possible dependency additions:

```text
python-jose[cryptography]
passlib[bcrypt]
pydantic-settings
email-validator
```

Codex should adapt dependency names to the project’s existing dependency management.

---

## Step 5: Repository Prompt

### Prompt

```text
Implement the user repository for Feature 001.

Create or update:
- app/repositories/user_repository.py

Required methods:
1. create_user(email: str, hashed_password: str, is_active: bool = True)
2. get_user_by_id(user_id: int)
3. get_user_by_email(email: str)
4. email_exists(email: str)

Rules:
- Repository should use SQLAlchemy session.
- Repository should only contain database operations.
- Repository should not hash passwords.
- Repository should not verify passwords.
- Repository should not create JWT tokens.
- Repository should not expose HTTP-specific behavior.
- Repository should not return Pydantic schemas.

After changes, show:
- Files changed
- Methods implemented
- Any transaction behavior
```

### Expected Outcome

Codex should create a clean database-access layer used by the service layer.

---

## Step 6: Service Layer Prompt

### Prompt

```text
Implement the auth service for Feature 001.

Create or update:
- app/services/auth_service.py

Required behavior:
1. register_user
   - Check duplicate email.
   - Hash password.
   - Create user through UserRepository.
   - Return created user.

2. authenticate_user
   - Find user by email.
   - Verify password.
   - Return generic invalid credentials behavior for unknown email and wrong password.
   - Reject inactive users.

3. create_login_token
   - Create access token using user ID as subject.

4. get_current_user
   - Decode token.
   - Extract user ID from token subject.
   - Retrieve user.
   - Reject missing, invalid, expired, or unknown users.
   - Reject inactive users.

Rules:
- Service contains business logic.
- Service should not define FastAPI routes.
- Service should not contain raw SQL.
- Keep error handling clean.
- Use project conventions for exceptions.
- If custom exceptions are helpful, add them in a clean location.

After changes, show:
- Files changed
- Service methods implemented
- Error-handling approach
```

### Expected Outcome

Codex should create the core business logic for registration, login, token creation, and current-user lookup.

---

## Step 7: API Router Prompt

### Prompt

```text
Implement the authentication API router for Feature 001.

Create or update:
- app/api/v1/routers/auth.py
- app/api/v1/api.py if the project uses a router aggregator
- app/main.py if needed to include the router

Required endpoints:
1. POST /api/v1/auth/register
2. POST /api/v1/auth/login
3. GET /api/v1/auth/me

Endpoint behavior:
- Register:
  - request model: UserRegisterRequest
  - response model: UserResponse
  - status: 201
  - duplicate email: 409 preferred

- Login:
  - request model: UserLoginRequest
  - response model: TokenResponse
  - status: 200
  - invalid credentials: 401 with generic message

- Me:
  - requires bearer token
  - response model: UserResponse
  - missing/invalid token: 401
  - inactive user: 403

Rules:
- Router handles HTTP-specific behavior.
- Router should call service layer.
- Router should not directly query the database except through service/repository pattern.
- Do not expose password or hashed_password.

After changes, show:
- Routes added
- Files changed
- How router is included in the app
```

### Expected Outcome

Codex should expose working API endpoints under:

```text
/api/v1/auth
```

---

## Step 8: Test Implementation Prompt

### Prompt

```text
Add tests for Feature 001.

Create or update:
- tests/conftest.py
- tests/test_auth_register.py
- tests/test_auth_login.py
- tests/test_auth_me.py
- tests/test_user_repository.py
- tests/test_auth_service.py

If the repository uses a simpler test structure, adapt to it without reducing coverage.

Required tests:
1. Register user successfully.
2. Reject duplicate email.
3. Reject invalid email.
4. Reject short password.
5. Confirm stored password is hashed.
6. Login successfully.
7. Reject wrong password.
8. Reject unknown email.
9. Confirm wrong password and unknown email return the same generic error.
10. /me works with a valid token.
11. /me rejects missing token.
12. /me rejects invalid token.
13. /me response does not expose password or hashed_password.
14. Register response does not expose password or hashed_password.

Testing rules:
- Use pytest.
- Use FastAPI TestClient unless the project already uses another pattern.
- Use a separate test database.
- Override the database dependency for tests if needed.
- Tests must not use the development database.
- Keep tests deterministic.
- Do not depend on external services.

After changes, show:
- Test files created/modified
- Test database strategy
- How to run tests
```

### Expected Outcome

Codex should create meaningful test coverage for endpoint, service, repository, and security behavior.

---

## Step 9: Test Run and Fix Prompt

### Prompt

```text
Run the full test suite.

Command:
pytest -v

If tests fail:
1. Read the failure messages.
2. Fix the implementation or tests appropriately.
3. Re-run the failing tests.
4. Re-run the full test suite.

Do not ignore failing tests.
Do not delete tests to make the suite pass.
Do not weaken security tests.

Return:
- Commands run
- Test results
- Fixes applied
- Any remaining failures
```

### Expected Outcome

Codex should run tests, fix issues, and report final passing status.

---

## Step 10: Final Review Prompt

### Prompt

```text
Review the completed Feature 001 implementation.

Check:
1. Endpoint paths are correct.
2. Password is hashed before storage.
3. Plain password is never stored.
4. hashed_password is never returned.
5. Duplicate email is handled.
6. Login error is generic.
7. JWT contains minimal payload.
8. /me requires bearer token.
9. Tests cover registration, login, /me, repository, service, and security behavior.
10. The implementation follows the router/schema/service/repository/model/database architecture.
11. No unrelated code was rewritten.
12. No real secrets were committed.

Return:
- Final review checklist
- Files changed
- Tests run
- Final sign-off recommendation
- Remaining TODOs, if any
```

### Expected Outcome

Codex should provide a final implementation summary suitable for sprint sign-off.

---

# 6. Expected Final Implementation Outcome

After Codex completes the feature, the backend should have:

## Application Behavior

```text
User can register.
User can log in.
User receives a bearer access token.
User can access /me with a valid token.
Invalid login fails safely.
Protected endpoint rejects missing or invalid token.
```

## API Endpoints

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

## Data Layer

```text
users table exists
email is unique
password is stored only as hashed_password
is_active is available
created_at and updated_at exist
```

## Code Layers

```text
router layer exists
schema layer exists
service layer exists
repository layer exists
model layer exists
database session dependency exists
security utilities exist
```

## Test Coverage

The feature should have passing tests for:

```text
registration
duplicate email
validation errors
password hashing
login success
login failure
generic login error
authenticated /me
missing token
invalid token
sensitive field exclusion
repository behavior
service behavior
```

## Security Outcome

The implementation should confirm:

```text
plain password is never stored
hashed_password is never returned
JWT expires
JWT payload is minimal
secret configuration is externalized
.env is not committed
```

---

# 7. Sprint Sign-Off Criteria

Feature 001 is ready for sign-off only when:

```text
[ ] All required endpoints exist.
[ ] All required schemas exist.
[ ] User model exists.
[ ] Repository layer exists.
[ ] Service layer exists.
[ ] Security utilities exist.
[ ] Password hashing works.
[ ] Login token generation works.
[ ] /me authentication works.
[ ] API responses do not expose sensitive fields.
[ ] Test database is isolated.
[ ] Full pytest suite passes.
[ ] Codex final summary includes files changed and tests run.
[ ] No unrelated rewrites were introduced.
[ ] No real secrets were committed.
```

---

# 8. Recommended Human Review Checklist

After Codex finishes, manually review:

```text
1. Did Codex follow the existing project structure?
2. Did it introduce unnecessary complexity?
3. Did it hardcode secrets?
4. Did it expose hashed_password anywhere?
5. Did it use the development database in tests?
6. Did it skip any required test?
7. Did it return 401 for both unknown email and wrong password?
8. Did it use 409 or a clear equivalent for duplicate email?
9. Did it keep router, service, repository, and model responsibilities separate?
10. Did it run pytest successfully?
```

---

# 9. Suggested Commit Message

```text
feat(auth): implement user registration and login
```

Suggested commit body:

```text
- add user model and database support
- add auth and user schemas
- add user repository
- add auth service
- add password hashing and JWT utilities
- add auth router for register, login, and me endpoints
- add tests for registration, login, token auth, and security behavior
```

---

# 10. Notes for Future Features

This Codex prompt structure can be reused for future backend features by changing:

```text
feature name
business rules
database changes
schemas
endpoints
service behavior
repository behavior
security requirements
test cases
```

For future features, keep the same sprint cycle:

```text
requirements -> design -> implementation prompt -> build -> test -> fix -> sign-off
```
