# Login System API

A portfolio-ready FastAPI backend project focused on building authentication and authorization features with a clean layered architecture.

This repository is being developed feature by feature in a sprint-style workflow:

`requirements -> design -> implementation -> tests -> fixes -> review -> sign-off`

The current implementation includes secure user registration, JWT-based login, authenticated user lookup, a health check endpoint, and the start of role-based access control support.

## Why This Project

I built this project to practice production-style backend development rather than only shipping endpoints quickly. The focus is on:

- Clear separation of concerns
- Secure authentication flows
- Test-first thinking
- Maintainable project structure
- PostgreSQL-ready backend design while keeping local setup simple with SQLite

## Features

### Implemented

- User registration with email validation
- Secure password hashing with `passlib` and `bcrypt`
- Duplicate email protection
- JWT access token login
- Authenticated `/me` endpoint
- Generic login error handling to avoid email enumeration
- Inactive user checks
- Health check endpoint
- Default user role assignment
- Isolated pytest database setup

### In Progress / Planned

- Expanded role-based access control
- Additional authorization rules
- More production-oriented API hardening

## Tech Stack

- FastAPI
- SQLAlchemy ORM
- Pydantic v2
- SQLite for local development
- PostgreSQL-ready configuration
- JWT with `python-jose`
- Password hashing with `passlib[bcrypt]`
- Pytest
- HTTPX / FastAPI TestClient for API tests

## Project Structure

The codebase follows a layered FastAPI architecture:

```text
app/
|-- api/            # Routers, dependencies, HTTP layer
|-- core/           # Settings, security, shared configuration
|-- db/             # Engine, sessions, base, DB initialization
|-- models/         # SQLAlchemy ORM models
|-- repositories/   # Database access logic
|-- schemas/        # Pydantic request/response models
`-- services/       # Business logic
```

Request flow:

```text
router -> schema -> service -> repository -> model -> database
```

## Current API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/api/v1/auth/register` | Register a new user |
| `POST` | `/api/v1/auth/login` | Authenticate and receive a JWT |
| `GET` | `/api/v1/auth/me` | Return the currently authenticated user |
| `GET` | `/api/v1/health` | Simple health check |

## Authentication Flow

### Register

- Accepts email and password
- Validates input with Pydantic
- Hashes the password before persistence
- Stores users with a default `user` role
- Returns a safe response without password fields

### Login

- Accepts email and password
- Verifies the hashed password
- Returns a JWT access token
- Uses a generic `Invalid credentials` message for both unknown email and wrong password

### Current User

- Requires `Authorization: Bearer <token>`
- Decodes and validates the JWT
- Loads the authenticated user from the database
- Rejects invalid, missing, expired, or inactive-user cases

## Security Notes

- Plain text passwords are never stored
- Passwords and `hashed_password` are never exposed in API responses
- JWT settings are configurable through environment variables
- `.env.example` contains placeholders only
- Token payloads are minimal and use `sub` for the user identifier

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd login_system
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your environment file

Use `.env.example` as a reference and create a local `.env` with your own development values.

Example variables:

```env
APP_NAME=Login System API
API_V1_PREFIX=/api/v1
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-dev-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

Docs will be available at:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Running Tests

Run the full test suite with:

```bash
pytest -v
```

The tests use an isolated in-memory SQLite database and do not rely on the development database file.

## Example Requests

### Register

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Get Current User

```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

## Design Notes

- Local development uses SQLite for simplicity
- The application structure is ready to move toward PostgreSQL-backed environments
- Repository and service layers make future growth easier as features expand
- Feature planning documents are tracked in the [`docs/`](docs/) folder

## Portfolio Highlights

- Built with a maintainable backend architecture instead of a single-file prototype
- Uses secure password hashing and token-based authentication
- Includes meaningful automated tests around validation, security, and auth behavior
- Documents feature work in a structured sprint format

## Roadmap

- Add richer RBAC capabilities
- Expand authorization checks by role
- Add database migrations
- Add Docker support
- Add CI for automated test runs
- Extend the API with more user management workflows

## License

This project is available for learning, review, and portfolio use.
