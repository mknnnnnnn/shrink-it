from fastapi.testclient import TestClient


def test_create_url(client: TestClient, login: dict):
    url = {
        "original_url": "https://www.example.com/",
        "short_code": "abcd123",
    }

    token = login["access_token"]

    response = client.post(
        "/urls",
        json=url,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["original_url"] == url["original_url"]
    assert data["short_code"] == url["short_code"]
    assert "created_at" in data
    assert data["expires_at"] is None
    assert data["click_count"] == 0
    assert data["click_max"] is None
    assert data["is_active"] is True


def test_create_url_without_auth(client: TestClient):

    url = {
        "original_url": "https://www.example.com/",
        "short_code": "abcd123",
    }

    response = client.post("/urls", json=url, headers={"Authorization": "Bearer token"})

    assert response.status_code == 401


def test_create_url_with_invalid_url(client: TestClient, login: dict):

    url = {"original_url": "www.example.com", "short_code": "abc123"}

    token = login["access_token"]

    response = client.post(
        "/urls", json=url, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422


def test_create_url_with_invalid_short_code(client: TestClient, login: dict):

    url = {"original_url": "https://www.example.com/", "short_code": "a"}

    token = login["access_token"]

    response = client.post(
        "/urls", json=url, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422


def test_create_url_duplicate_short_code(client: TestClient, login: dict):

    url = {"original_url": "https://www.example.com/", "short_code": "abc123"}

    token = login["access_token"]

    response = client.post(
        "/urls", json=url, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201

    second_response = client.post(
        "/urls", json=url, headers={"Authorization": f"Bearer {token}"}
    )

    assert second_response.status_code == 409


def test_get_url(client: TestClient, login: dict):

    url = {"original_url": "https://www.example.com/", "short_code": "abc123"}

    token = login["access_token"]

    response = client.post(
        "/urls", json=url, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201

    response = client.get("/urls", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["original_url"] == url["original_url"]
    assert data[0]["short_code"] == url["short_code"]


def test_redict_url(client: TestClient, login: dict):

    token = login["access_token"]

    url = {"original_url": "https://www.example.com/", "short_code": "abc123"}

    response = client.post(
        "/urls", json=url, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201

    redict = client.get(f"/{url['short_code']}", follow_redirects=False)
    assert redict.status_code in (302, 307)
    assert redict.headers["location"] == url["original_url"]
