# Feature 001: User Registration and Login
## 06. Database Changes

### Purpose

This document defines the database changes required to support user registration, login, password verification, and authenticated user access.

The goal is to create a clean user storage model that works with SQLite during development and can later migrate to PostgreSQL with minimal changes.

---

## 1. Database Scope for Feature 001

This feature introduces one primary table:

```text
users
```

The `users` table stores account identity and authentication-related information.

This feature does not yet include:

- Roles and permissions
- Password reset
- Email verification
- Login history
- Refresh token storage
- Multi-factor authentication
- User profile details

Those can be added in later features.

---

## 2. Table: users

### Table Name

```text
users
```

### Purpose

Stores registered application users and their authentication credentials.

---

## 3. Proposed Columns

| Column | Type | Nullable | Unique | Default | Description |
|---|---|---:|---:|---|---|
| id | Integer | No | Yes / PK | Auto increment | Internal user identifier |
| email | String | No | Yes | None | User login email |
| hashed_password | String | No | No | None | Securely hashed password |
| is_active | Boolean | No | No | True | Whether user account is active |
| created_at | DateTime | No | No | Current timestamp | Record creation time |
| updated_at | DateTime | No | No | Current timestamp | Last update time |

---

## 4. SQLAlchemy Model Draft

```python
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
```

---

## 5. Constraints

### Primary Key

```text
users.id
```

### Unique Constraint

```text
users.email
```

The email field must be unique because it is used as the login identifier.

### Required Fields

The following fields are required:

```text
email
hashed_password
is_active
created_at
updated_at
```

---

## 6. Indexes

Recommended indexes:

```text
users.id
users.email
```

Reason:

- `id` is used for direct user lookup.
- `email` is used during registration duplicate checks and login.

---

## 7. Password Storage Rule

The database must never store a plain text password.

The application should receive:

```text
password
```

But the database should store only:

```text
hashed_password
```

Example:

```text
Input password: MyPassword123
Stored value: bcrypt/argon2 hash string
```

---

## 8. SQLite to PostgreSQL Readiness

The first implementation will use SQLite.

However, the model should be written in a way that can later support PostgreSQL.

Guidelines:

- Avoid SQLite-specific field types.
- Use SQLAlchemy ORM models.
- Use Alembic migrations when schema evolution begins.
- Avoid raw SQL unless necessary.
- Keep database URL configurable through environment settings.

---

## 9. Migration Plan

For initial development, one of two approaches may be used:

### Option A: Development-Only Auto Create

Use:

```python
Base.metadata.create_all(bind=engine)
```

This is acceptable for early learning and simple local development.

### Option B: Alembic Migration

Preferred for production-style development.

Migration should create:

```text
users table
unique index on email
index on id
```

Recommended direction:

- Use `create_all()` only for early local setup.
- Introduce Alembic before adding multiple features.

---

## 10. Repository Operations Required

The `UserRepository` should support:

```text
create_user
get_user_by_id
get_user_by_email
email_exists
```

Example responsibilities:

| Repository Method | Purpose |
|---|---|
| create_user | Insert new user record |
| get_user_by_email | Find user during login or duplicate check |
| get_user_by_id | Find authenticated user |
| email_exists | Check duplicate registration |

---

## 11. Data Validation Boundary

Database validation should enforce:

- Required fields
- Unique email
- Data type constraints

Application/Pydantic validation should enforce:

- Valid email format
- Password length
- Password confirmation if used
- Password complexity if required

---

## 12. Out of Scope for This Feature

The following database structures are intentionally excluded:

```text
roles
permissions
refresh_tokens
password_reset_tokens
email_verification_tokens
user_profiles
audit_logs
login_attempts
```

These can be introduced in later features.

---

## 13. Database Sign-Off Checklist

Before signing off this database design:

- [ ] `users` table is defined.
- [ ] `email` is unique and indexed.
- [ ] `hashed_password` is required.
- [ ] Plain text password is never stored.
- [ ] `is_active` exists for account status.
- [ ] `created_at` and `updated_at` exist.
- [ ] Design works with SQLite.
- [ ] Design can later migrate to PostgreSQL.
- [ ] Repository methods are clearly identified.
