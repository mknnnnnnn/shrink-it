# Shrink it

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
| `GET` | `/urls` | User | Get all URLs available for the authenticated user |
| `POST` | `/urls` | User | Create a new short URL |
| `GET` | `/urls/qr` | User | Generate a QR code for a URL |
| `GET` | `/{short_code}` | Public | Redirect to the original URL |
| `PATCH` | `/urls/{id}/deactivate` | User | Deactivate a URL |
| `PATCH` | `/urls/{id}/activate` | User | Activate a URL |
| `DELETE` | `/urls/{id}` | User | Delete a URL |
| `PATCH` | `/urls/{id}/max-clicks/{limit}` | Admin | Change the maximum click limit for a URL |
| `PATCH` | `/urls/{id}/expire-date/{expire_date}` | Admin | Change the expiration date for a URL |

### Users API

All user management endpoints require admin permissions.

| Method | Endpoint | Required role | Description |
|---|---|---|---|
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
