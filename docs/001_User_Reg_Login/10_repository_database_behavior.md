# Feature 001: User Registration and Login
## 10. Repository / Database Behavior

### Purpose

This document defines the repository and database behavior required for user registration, login, and authenticated user lookup.

The repository layer should isolate database query logic from the service layer.

---

## 1. Repository Layer Role

The repository layer should answer this question:

```text
How does the application read from and write to the database?
```

It should not decide business rules such as whether a duplicate email should return a 409 response. It should only perform database operations and return results.

---

## 2. Recommended File

```text
app/repositories/user_repository.py
```

---

## 3. Main Repository Class

Recommended class:

```python
class UserRepository:
    ...
```

Recommended initialization:

```python
class UserRepository:
    def __init__(self, db: Session):
        self.db = db
```

This keeps the SQLAlchemy session inside the repository.

---

## 4. Required Repository Methods

```text
create_user
get_user_by_id
get_user_by_email
email_exists
```

Optional methods for future features:

```text
update_user
deactivate_user
delete_user
list_users
```

---

## 5. Method: create_user

### Purpose

Insert a new user into the database.

### Inputs

```text
email
hashed_password
is_active
```

### Output

```text
Created User model
```

### Behavior

```text
1. Create User ORM object.
2. Add user to database session.
3. Commit transaction.
4. Refresh object.
5. Return created user.
```

### Draft

```python
def create_user(self, email: str, hashed_password: str, is_active: bool = True) -> User:
    user = User(
        email=email,
        hashed_password=hashed_password,
        is_active=is_active,
    )

    self.db.add(user)
    self.db.commit()
    self.db.refresh(user)

    return user
```

### Notes

The repository assumes the password is already hashed before this method is called.

---

## 6. Method: get_user_by_email

### Purpose

Find a user by email.

### Inputs

```text
email
```

### Output

```text
User model or None
```

### Behavior

```text
1. Query users table by email.
2. Return first matching user.
3. Return None if no user exists.
```

### Draft

```python
def get_user_by_email(self, email: str) -> User | None:
    return (
        self.db.query(User)
        .filter(User.email == email)
        .first()
    )
```

### Used By

```text
register_user
authenticate_user
email_exists
```

---

## 7. Method: get_user_by_id

### Purpose

Find a user by internal ID.

### Inputs

```text
user_id
```

### Output

```text
User model or None
```

### Draft

```python
def get_user_by_id(self, user_id: int) -> User | None:
    return (
        self.db.query(User)
        .filter(User.id == user_id)
        .first()
    )
```

### Used By

```text
get_current_user
future profile endpoints
future authorization checks
```

---

## 8. Method: email_exists

### Purpose

Check whether an email already exists.

### Inputs

```text
email
```

### Output

```text
bool
```

### Draft

```python
def email_exists(self, email: str) -> bool:
    return self.get_user_by_email(email) is not None
```

### Notes

This method is convenient but optional because the service can also call `get_user_by_email()` directly.

---

## 9. Transaction Behavior

For Feature 001:

| Operation | Commit Needed? | Notes |
|---|---:|---|
| Create user | Yes | Inserts new row |
| Get user by email | No | Read-only |
| Get user by ID | No | Read-only |
| Email exists | No | Read-only |

---

## 10. Database Session Dependency

Recommended file:

```text
app/db/database.py
```

Recommended dependency:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Routers should receive the session through FastAPI dependency injection.

---

## 11. Repository Usage Flow

### Registration

```text
AuthService.register_user()
↓
UserRepository.get_user_by_email()
↓
UserRepository.create_user()
```

### Login

```text
AuthService.authenticate_user()
↓
UserRepository.get_user_by_email()
```

### Current User

```text
AuthService.get_current_user()
↓
UserRepository.get_user_by_id()
```

---

## 12. Repository Should Not Do

The repository should not:

- Hash passwords.
- Verify passwords.
- Create JWT tokens.
- Raise HTTP exceptions.
- Know API endpoint paths.
- Return Pydantic response schemas.
- Decide business-level error messages.
- Perform request validation.

---

## 13. Database Error Handling

Possible database errors:

```text
Unique constraint violation on email
Database connection error
Commit failure
Invalid transaction state
```

The service or router should handle expected errors gracefully.

Even if duplicate email is checked before insert, the database unique constraint is still required because two requests could arrive at nearly the same time.

---

## 14. SQLite Behavior Notes

SQLite is acceptable for learning and local development.

Important notes:

- SQLite has limited concurrency compared to PostgreSQL.
- Use SQLAlchemy abstractions to keep the code portable.
- Avoid SQLite-specific raw SQL.
- Keep database URL in configuration.
- Use a separate test database during tests.

---

## 15. PostgreSQL Readiness Notes

To prepare for PostgreSQL later:

- Keep SQLAlchemy models database-agnostic.
- Use environment-based `DATABASE_URL`.
- Avoid hardcoded SQLite paths inside business logic.
- Use Alembic migrations before production-style deployment.
- Avoid relying on SQLite-specific behavior.

---

## 16. Repository Test Cases

Repository-level tests may include:

```text
create_user saves a user
get_user_by_email returns existing user
get_user_by_email returns None for unknown email
get_user_by_id returns existing user
get_user_by_id returns None for unknown ID
email_exists returns True for existing email
email_exists returns False for unknown email
```

---

## 17. Repository Sign-Off Checklist

Before signing off repository/database behavior:

- [ ] `UserRepository` is defined.
- [ ] `create_user` behavior is defined.
- [ ] `get_user_by_email` behavior is defined.
- [ ] `get_user_by_id` behavior is defined.
- [ ] `email_exists` behavior is defined.
- [ ] Repository uses SQLAlchemy session.
- [ ] Repository does not contain business logic.
- [ ] Repository does not raise HTTP exceptions.
- [ ] Database session dependency is defined.
- [ ] SQLite and PostgreSQL portability is considered.
- [ ] Unique email protection is enforced at database level.
