from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from shrink_it.users.models import User
from shrink_it.auth.security import verify_password


def test_register_user_success(client: TestClient, db_session: Session):
    password = "KotRyszard123!"

    response = client.post(
        "/auth/register",
        json={
            "first_name": "Jan",
            "last_name": "Kowalski",
            "email": "jan.kowalski@example.com",
            "password": password,
            "phone_number": "+48123123123",
        },
    )

    assert response.status_code == 201
    responde_data = response.json()

    assert responde_data["first_name"] == "Jan"
    assert responde_data["last_name"] == "Kowalski"
    assert responde_data["email"] == "jan.kowalski@example.com"
    assert responde_data["phone_number"] == "+48123123123"
    assert responde_data["is_active"] is True
    assert responde_data["is_admin"] is False

    assert "password" not in responde_data

    user = db_session.scalar(
        select(User).where(User.email == "jan.kowalski@example.com")
    )

    assert user is not None
    assert user.password != password
    assert verify_password(password, user.password)


def test_register_user_with_existing_email(client: TestClient):

    user = {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "email": "jan.kowalski@example.com",
        "password": "KotRyszard123!",
        "phone_number": "+48123123123",
    }

    response = client.post("/auth/register", json=user)

    assert response.status_code == 201

    second_response = client.post("/auth/register", json=user)

    assert second_response.status_code == 409


def test_register_user_with_invalid_email(client: TestClient):

    user = {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "email": "jan.kowalski.example.com",
        "password": "KotRyszard123!",
        "phone_number": "+48123123123",
    }

    response = client.post("/auth/register", json=user)

    assert response.status_code == 422


def test_register_user_with_missing_field(client: TestClient):

    user = {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "email": "jan.kowalski.example.com",
        "phone_number": "+48123123123",
    }

    response = client.post("/auth/register", json=user)

    assert response.status_code == 422


def test_login_success(client: TestClient):

    user = {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "email": "jan.kowalski@example.com",
        "password": "KotRyszard123!",
        "phone_number": "+48123123123",
    }

    register_response = client.post("/auth/register", json=user)

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login", data={"username": user["email"], "password": user["password"]}
    )

    assert login_response.status_code == 200

    login_response_body = login_response.json()

    assert "access_token" in login_response_body
    assert login_response_body["token_type"] == "bearer"


def test_login_with_incorrect_password(client: TestClient):

    user = {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "email": "jan.kowalski@example.com",
        "password": "KotRyszard123!",
        "phone_number": "+48123123123",
    }

    register_response = client.post("/auth/register", json=user)

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login", data={"username": user["email"], "password": "ABCabc123!"}
    )

    assert login_response.status_code == 401
    assert "access_token" not in login_response.json()
