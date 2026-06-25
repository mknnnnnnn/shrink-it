from fastapi.testclient import TestClient
from pathlib import Path
from sqlalchemy import select
import sys

PATH = Path(__file__).resolve().parents[1]
SRC_PATH = PATH / "src"
sys.path.append(str(SRC_PATH))

from shrink_it.main import app
from shrink_it.database import SessionLocal
from shrink_it.urls.models import URL


def test_create_url_with_no_auth():
    orginal_url = "example@example.com"
    short_code = "QWERTY"

    try:
        db = SessionLocal()

        statement = select(URL).where(URL.original_url == orginal_url)
        db_url = db.scalar(statement)

        if db_url:
            db.delete(db_url)
            db.commit()

        client = TestClient(app)

        response = client.post(
            "/urls", data={"orginal_url": orginal_url, "short_code": short_code}
        )

        assert response.status_code == 401
    finally:
        if db is not None:
            try:
                statement = select(URL).where(URL.original_url == orginal_url)

                db_url = db.scalar(statement)

                if db_url:
                    db.delete(db_url)
                    db.commit()
            finally:
                db.close()
