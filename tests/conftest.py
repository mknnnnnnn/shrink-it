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
