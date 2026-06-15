from fastapi.testclient import TestClient
from pathlib import Path
from sqlalchemy import select
import sys

PATH = Path(__file__).resolve().parents[1]
MAIN_PATH = PATH / "src"
sys.path.append(str(MAIN_PATH))

from shrink_it.users.models import User
from shrink_it.database import SessionLocal
from shrink_it.auth.security import hash_password
from shrink_it.main import app

client = TestClient(app)


def test_users_get_with_no_auth():
    response = client.get("/users")

    assert response.status_code == 401


def test_users_get_wtih_admin_auth():
    db = None
    admin_email = "admin@test.com"
    admin_password = "admin"

    try:
        db = SessionLocal()

        statement = select(User).where(User.email == admin_email)
        db_admin = db.scalar(statement)

        if db_admin:
            db.delete(db_admin)
            db.commit()

        db_admin = User(
            first_name="admin",
            last_name="admin",
            email=admin_email,
            password=hash_password(admin_password),
            is_admin=True,
        )

        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)

        response = client.post(
            "/auth/login", data={"username": admin_email, "password": admin_password}
        )

        assert response.status_code == 200

        token = response.json()["access_token"]

        response = client.get("/users", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    finally:
        if db is not None:
            try:
                statement = select(User).where(User.email == admin_email)

                db_admin = db.scalar(statement)

                if db_admin:
                    db.delete(db_admin)
                    db.commit()
            finally:
                db.close()
