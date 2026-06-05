# Feature 001: User Registration and Login
## 12. Test Cases

### Purpose

This document defines the test cases required before signing off Feature 001.

Testing should confirm that registration, login, token authentication, database behavior, validation, and security requirements work as expected.

---

## 1. Testing Scope

Feature 001 should include tests for:

```text
registration
login
current authenticated user endpoint
service layer behavior
repository/database behavior
security behavior
validation behavior
```

---

## 2. Test Structure

```text
tests/
  conftest.py
  test_auth_register.py
  test_auth_login.py
  test_auth_me.py
  test_user_repository.py
  test_auth_service.py
```

---

## 3. Test Database Strategy

Use a separate test database.

For SQLite testing:

```text
sqlite:///./test.db
```

The test setup should:

```text
1. Create test database tables.
2. Override FastAPI database dependency.
3. Run each test with clean data.
4. Drop or clean tables after tests.
```

---

## 4. Required Fixtures

Recommended fixtures:

```text
test_db
client
created_user
auth_token
auth_headers
```

Example responsibilities:

| Fixture | Purpose |
|---|---|
| test_db | Provides isolated database session |
| client | Provides FastAPI TestClient |
| created_user | Creates reusable test user |
| auth_token | Creates valid JWT for test user |
| auth_headers | Returns Authorization header |

---

## 5. Registration Endpoint Tests

### Test 1: Register User Successfully

```text
Given a valid email and valid password
When POST /api/v1/auth/register is called
Then the response status should be 201
And response should include id, email, is_active
And response should not include password or hashed_password
```

Expected status:

```text
201 Created
```

---

### Test 2: Reject Duplicate Email

```text
Given a user already exists
When another registration request uses the same email
Then the response should return conflict error
```

Expected status:

```text
409 Conflict
```

Acceptable alternative:

```text
400 Bad Request
```

Preferred:

```text
409 Conflict
```

---

### Test 3: Reject Invalid Email

```text
Given an invalid email format
When registration is submitted
Then validation should fail
```

Expected status:

```text
422 Unprocessable Entity
```

---

### Test 4: Reject Missing Password

```text
Given a registration request without password
When registration is submitted
Then validation should fail
```

Expected status:

```text
422 Unprocessable Entity
```

---

### Test 5: Reject Short Password

```text
Given a password shorter than minimum length
When registration is submitted
Then validation should fail
```

Expected status:

```text
422 Unprocessable Entity
```

---

### Test 6: Confirm Password Is Hashed

```text
Given a successful registration
When the user is retrieved from the database
Then stored hashed_password should not equal plain password
```

Expected result:

```text
stored hashed_password != submitted password
```

---

## 6. Login Endpoint Tests

### Test 1: Login Successfully

```text
Given a registered user
When valid credentials are submitted
Then response should return access_token and token_type
```

Expected status:

```text
200 OK
```

Expected response:

```json
{
  "access_token": "some_token",
  "token_type": "bearer"
}
```

---

### Test 2: Reject Wrong Password

```text
Given a registered user
When wrong password is submitted
Then login should fail
```

Expected status:

```text
401 Unauthorized
```

Expected message:

```text
Invalid credentials
```

---

### Test 3: Reject Unknown Email

```text
Given an email that does not exist
When login is submitted
Then login should fail
```

Expected status:

```text
401 Unauthorized
```

Expected message:

```text
Invalid credentials
```

---

### Test 4: Do Not Reveal Whether Email Exists

```text
Given wrong password for existing user
And unknown email for non-existing user
When both login requests fail
Then both should return the same generic error message
```

Expected message:

```text
Invalid credentials
```

---

### Test 5: Reject Inactive User Login

```text
Given a registered but inactive user
When valid credentials are submitted
Then login should fail
```

Expected status:

```text
403 Forbidden
```

---

## 7. Current User Endpoint Tests

### Test 1: Return Current User With Valid Token

```text
Given a valid authenticated user token
When GET /api/v1/auth/me is called
Then the endpoint should return current user data
```

Expected status:

```text
200 OK
```

Expected response fields:

```text
id
email
is_active
```

---

### Test 2: Reject Missing Token

```text
Given no Authorization header
When GET /api/v1/auth/me is called
Then the request should fail
```

Expected status:

```text
401 Unauthorized
```

---

### Test 3: Reject Invalid Token

```text
Given an invalid token
When GET /api/v1/auth/me is called
Then the request should fail
```

Expected status:

```text
401 Unauthorized
```

---

### Test 4: Reject Expired Token

```text
Given an expired token
When GET /api/v1/auth/me is called
Then the request should fail
```

Expected status:

```text
401 Unauthorized
```

---

### Test 5: Do Not Return Sensitive Fields

```text
Given a valid token
When GET /api/v1/auth/me is called
Then response should not include password or hashed_password
```

Expected result:

```text
password not in response
hashed_password not in response
```

---

## 8. Repository Tests

### Test 1: Create User

```text
Given valid user data with hashed password
When UserRepository.create_user is called
Then user should be saved in the database
```

---

### Test 2: Get User by Email

```text
Given an existing user
When UserRepository.get_user_by_email is called
Then the correct user should be returned
```

---

### Test 3: Unknown Email Returns None

```text
Given an email not in the database
When UserRepository.get_user_by_email is called
Then None should be returned
```

---

### Test 4: Get User by ID

```text
Given an existing user
When UserRepository.get_user_by_id is called
Then the correct user should be returned
```

---

### Test 5: Email Exists

```text
Given an existing email
When UserRepository.email_exists is called
Then True should be returned
```

---

## 9. Service Layer Tests

### Test 1: Register User Hashes Password

```text
Given registration input
When AuthService.register_user is called
Then the created user should contain a hashed password
```

---

### Test 2: Register User Rejects Duplicate Email

```text
Given an existing email
When AuthService.register_user is called with same email
Then DuplicateEmailError should be raised
```

---

### Test 3: Authenticate User Accepts Valid Credentials

```text
Given a registered user
When AuthService.authenticate_user is called with valid credentials
Then user should be returned
```

---

### Test 4: Authenticate User Rejects Invalid Credentials

```text
Given invalid credentials
When AuthService.authenticate_user is called
Then InvalidCredentialsError should be raised
```

---

### Test 5: Authenticate User Rejects Inactive User

```text
Given inactive user
When AuthService.authenticate_user is called
Then InactiveUserError should be raised
```

---

## 10. Security Tests

Required security checks:

```text
plain password is never stored
hashed_password is not returned in register response
hashed_password is not returned in /me response
login failure message is generic
invalid token is rejected
expired token is rejected
inactive users cannot log in
inactive users cannot access /me
```

---

## 11. Minimum Test Set for First Sign-Off

If time is limited, the minimum test set should include:

```text
1. Register user successfully
2. Reject duplicate email
3. Password is hashed
4. Login successfully
5. Reject wrong password
6. Reject unknown email
7. /me works with valid token
8. /me rejects missing token
9. Sensitive fields are not returned
```

Do not sign off the feature without these tests.

---

## 12. Suggested Test Command

Use:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

For one file:

```bash
pytest tests/test_auth_register.py -v
```

---

## 13. Test Sign-Off Checklist

Before signing off Feature 001:

- [ ] Registration success test passes.
- [ ] Duplicate email test passes.
- [ ] Invalid email test passes.
- [ ] Short password test passes.
- [ ] Password hashing test passes.
- [ ] Login success test passes.
- [ ] Wrong password test passes.
- [ ] Unknown email test passes.
- [ ] Generic login error test passes.
- [ ] `/me` with valid token test passes.
- [ ] `/me` without token test passes.
- [ ] `/me` with invalid token test passes.
- [ ] Sensitive fields are not exposed.
- [ ] Repository tests pass.
- [ ] Service tests pass.
- [ ] Full `pytest` run passes.
