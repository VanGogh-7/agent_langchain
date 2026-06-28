# FastAPI Learning Library

A complete learning project for building a real FastAPI web service. The app lets users register, log in, and manage their own books or learning resources.

This is intended for learning web service fundamentals, not production deployment. It still uses common project boundaries: routes, services, repositories, schemas, database models, authentication helpers, tests, and a small frontend.

## What This Demonstrates

- FastAPI application setup and routing
- Pydantic request and response models
- SQLAlchemy 2.x ORM models and sessions
- SQLite persistence
- JWT login with protected routes
- Password hashing with bcrypt
- Dependency injection for database sessions and current users
- Layered code organization
- Plain HTML, CSS, and JavaScript calling an API with `fetch()`
- Basic tests with `pytest` and `TestClient`

## Project Structure

```text
fastapi_learning_library/
  backend/app/main.py              FastAPI app factory, CORS, routers, startup
  backend/app/core/                Settings, security, shared HTTP errors
  backend/app/db/                  SQLAlchemy engine, sessions, ORM models
  backend/app/schemas/             Pydantic validation and serialization
  backend/app/repositories/        Database query functions
  backend/app/services/            Business rules
  backend/app/api/deps.py          FastAPI dependencies
  backend/app/api/routes/          HTTP route handlers
  backend/tests/                   pytest tests
  frontend/                        Plain browser UI
```

## Request Flow

An HTTP request enters a route in `backend/app/api/routes/`. The route validates input with a schema from `backend/app/schemas/`, then calls a service in `backend/app/services/`. The service enforces business rules and delegates database work to a repository in `backend/app/repositories/`. Repositories use a SQLAlchemy `Session` provided by `backend/app/api/deps.py`.

## Routing

The app is created in `backend/app/main.py` and includes these routers:

- `GET /api/health`
- `/api/auth`
- `/api/resources`

Tables are created automatically during startup with `Base.metadata.create_all()` so the project is easy to run while learning.

## Authentication

Users register with a username, email, and password. Passwords are hashed with bcrypt through Passlib. Login verifies the password and returns a JWT access token. Protected endpoints require:

```text
Authorization: Bearer <token>
```

The `get_current_user` dependency decodes the token, loads the user from the database, and rejects invalid or expired tokens with `401 Unauthorized`.

## Database Access

The project uses SQLite by default:

```text
sqlite:///./app.db
```

SQLAlchemy models live in `backend/app/db/models.py`. Database sessions are created in `backend/app/db/database.py` and injected into routes through FastAPI dependencies.

## Frontend

The frontend is plain HTML, CSS, and vanilla JavaScript. It demonstrates registration, login, token storage in `localStorage`, current user display, resource creation, listing, search, status filtering, deletion, and logout.

The JavaScript API base URL is:

```js
http://127.0.0.1:8000/api
```

If your backend is running on another port, append an `api` query parameter when opening the frontend:

```text
http://127.0.0.1:8080?api=http://127.0.0.1:8001/api
```

## Install

From the project directory:

```bash
cd fastapi_learning_library
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configure

Create a local `.env` file:

```bash
cp .env.example .env
```

Then edit `JWT_SECRET_KEY` to a local development secret. Do not commit `.env`.

## Run Backend

Run from `fastapi_learning_library/backend` so `app` is importable:

```bash
cd fastapi_learning_library/backend
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Open Frontend

Option 1: open the file directly in your browser:

```text
fastapi_learning_library/frontend/index.html
```

Option 2: serve it with Python:

```bash
cd fastapi_learning_library/frontend
python -m http.server 8080
```

Then open:

```text
http://127.0.0.1:8080
```

## Run Tests

Run tests from `fastapi_learning_library/backend`:

```bash
pytest
```

Tests use an in-memory SQLite database and override the app database dependency.

## Example API Requests

Health check:

```bash
curl http://127.0.0.1:8000/api/health
```

Register:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"password123"}'
```

Login:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"password123"}'
```

Create a resource:

```bash
TOKEN="paste-token-here"
curl -X POST http://127.0.0.1:8000/api/resources \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"FastAPI Docs","author":"FastAPI","category":"web","status":"reading","rating":5,"notes":"Study dependencies and routing."}'
```

List resources:

```bash
curl http://127.0.0.1:8000/api/resources \
  -H "Authorization: Bearer $TOKEN"
```

Search and filter:

```bash
curl "http://127.0.0.1:8000/api/resources?q=FastAPI&status=reading" \
  -H "Authorization: Bearer $TOKEN"
```

Delete:

```bash
curl -X DELETE http://127.0.0.1:8000/api/resources/1 \
  -H "Authorization: Bearer $TOKEN"
```
