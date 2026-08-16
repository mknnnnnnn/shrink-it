# Shrink it

[![Python Tests](https://github.com/mknnnnnnn/shrink-it/actions/workflows/ci.yml/badge.svg)](https://github.com/mknnnnnnn/shrink-it/actions/workflows/ci.yml)

Shrink it is a backend URL shortener built with FastAPI, PostgreSQL, and Docker.

It supports custom aliases, QR code generation, link expiration, click limits, and user authentication.

## Features

- Shortens long URLs
- Redirects short links to original URLs
- Supports custom short aliases
- Supports link expiration
- Supports one-time links
- Stores data in PostgreSQL
- Tracks click counts
- Supports maximum click limits
- Supports user accounts

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Docker
- Docker Compose
- Pytest
- GitHub Actions

## Overview

### Short links

Each long URL can be converted into a shorter code:

```txt
https://example.com
```
can become:
```txt
http://localhost:8000/example-short-code
```

### Custom aliases
Users can provide custom aliases instead of using randomly generated short code.

### Link expiration
Admins can set an expiration date for links. Links will be no longer available after expiration.

### One-time links
Admins can create one-time links by setting maximum click limit to one.

### Maximum click limits
Admins can set the maximum number of allowed clicks. After reaching the limit, the link is no longer available.

## API Methods

### URL API

Most URL endpoints require authentication. 
The `/{short_code}` endpoint is public and redirects to the original URL.
Changing the maximum click limit and expiration date requires admin permissions.

| Method | Endpoint | Required role | Description |
|---|---|---|---|
| `GET` | `/{short_code}` | Public | Redirect to the original URL |
| `GET` | `/urls` | User | Get all URLs available for the authenticated user |
| `POST` | `/urls` | User | Create a new short URL |
| `GET` | `/urls/qr` | User | Generate a QR code for a URL |
| `PATCH` | `/urls/{id}/deactivate` | User | Deactivate a URL |
| `PATCH` | `/urls/{id}/activate` | User | Activate a URL |
| `DELETE` | `/urls/{id}` | User | Delete a URL |
| `PATCH` | `/urls/{id}/max-clicks/{limit}` | Admin | Change the maximum click limit for a URL |
| `PATCH` | `/urls/{id}/expire-date/{expire_date}` | Admin | Change the expiration date for a URL |

### Users API

Most user management endpoints require admin permissions. Authenticated users can change their own password.

| Method | Endpoint | Required role | Description |
|---|---|---|---|
| `PATCH` | `/users/me/password` | User | Change the authenticated user's password |
| `PATCH` | `/users/{id}` | Admin | Update user details |
| `GET` | `/users` | Admin | Get all users |
| `GET` | `/users/{id}` | Admin | Get user details by ID |
| `DELETE` | `/users/{id}/delete` | Admin | Delete a user |
| `PATCH` | `/users/{id}/active-status/{status}` | Admin | Change user active status |
| `PATCH` | `/users/{id}/admin-status/{status}` | Admin | Change user admin status |

### Authentication API

Authentication is handled with OAuth2 password flow and JWT bearer tokens.

| Method | Endpoint | Required role | Description |
|---|---|---|---|
| `POST` | `/auth/register` | Public | Register a new user |
| `POST` | `/auth/login` | Public | Log in user and return a bearer token |

In Swagger UI, users can authenticate by clicking the **Authorize** button and providing their username and password.

## Data Validation

Request validation is handled with Pydantic. It includes:

- valid email addresses,
- valid original URLs,
- first and last names between 1 and 20 characters,
- passwords with a minimum length of 8 characters,
- optional international phone numbers,
- custom short codes between 3 and 10 characters,
- alphanumeric custom short codes,
- separate schemas for registration, login, updates and responses.

Invalid request data returns a `422 Unprocessable Entity` response.

## Error Handling

| Status | Meaning |
|---|---|
| `400 Bad Request` | URL is inactive or already active |
| `401 Unauthorized` | Credentials or authentication token are invalid |
| `403 Forbidden` | User does not have permission or the click limit has been reached |
| `404 Not Found` | User or URL does not exist |
| `409 Conflict` | Email, phone number or custom short code already exists |
| `410 Gone` | URL has expired |
| `422 Unprocessable Entity` | Request validation failed |
| `500 Internal Server Error` | Short-code generation failed |

Database integrity errors are handled with transaction rollback.

## Setup - Docker Compose

Clone the repository:
```bash
git clone https://github.com/mknnnnnnn/shrink-it
cd shrink-it
```
Create an `.env` file:
```bash
cp .env.example .env
```

Start the application:
```bash
docker compose up -d db
docker compose run --rm api alembic upgrade head
docker compose up -d
```

### Usage

Open Swagger in your browser:
```text
http://localhost:8000/docs
```

Stop the application:
```bash
docker compose down
```

Remove the database volume:
```bash
docker compose down -v
```

## Tests

The project includes automated tests written with `pytest`. 

Tests, linting, formatting checks, and coverage are automatically executed with GitHub Actions on every push and pull request.

Run tests locally with:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

Check code quality:
```bash
ruff check . --ignore=B008
ruff format --check .
```