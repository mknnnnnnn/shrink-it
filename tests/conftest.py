import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from shrink_it.database import Base, get_db
from shrink_it.main import app

TEST_URL = "sqlite://"

test_engine = create_engine(
    TEST_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestSessionLocal = sessionmaker(bind=test_engine, autoflush=False)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session):
    def override_db_session():
        yield db_session

    app.dependency_overrides[get_db] = override_db_session

    with TestClient(app) as client_test:
        yield client_test

    app.dependency_overrides.clear()


@pytest.fixture
def login(client):

    user = {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "email": "jan.kowalski@example.com",
        "password": "KotRyszard123!",
        "phone_number": "+48123123123",
    }

    register = client.post("/auth/register", json=user)

    assert register.status_code == 201

    assert register.json()["first_name"] == user["first_name"]
    assert register.json()["last_name"] == user["last_name"]
    assert register.json()["email"] == user["email"]
    assert register.json()["phone_number"] == user["phone_number"]

    assert register.json()["is_active"] is True
    assert register.json()["is_admin"] is False

    assert "password" not in register.json()

    login = client.post(
        "/auth/login", data={"username": user["email"], "password": user["password"]}
    )

    assert login.status_code == 200

    assert "access_token" in login.json()
    assert login.json()["token_type"] == "bearer"

    return login.json()
