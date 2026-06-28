from fastapi.testclient import TestClient


def register_and_login(client: TestClient, username: str = "reader") -> str:
    client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "password123",
        },
    )
    login_response = client.post(
        "/api/auth/login",
        json={"username": username, "password": "password123"},
    )
    return str(login_response.json()["access_token"])


def test_authenticated_user_can_create_resource(client: TestClient) -> None:
    token = register_and_login(client)

    response = client.post(
        "/api/resources",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "FastAPI Tutorial",
            "author": "FastAPI Docs",
            "category": "web",
            "status": "reading",
            "rating": 5,
            "notes": "Learn routing, dependencies, and schemas.",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "FastAPI Tutorial"
    assert data["status"] == "reading"


def test_authenticated_user_can_list_resources(client: TestClient) -> None:
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post(
        "/api/resources",
        headers=headers,
        json={"title": "SQLAlchemy Guide", "category": "database"},
    )

    response = client.get("/api/resources", headers=headers)

    assert response.status_code == 200
    resources = response.json()
    assert len(resources) == 1
    assert resources[0]["title"] == "SQLAlchemy Guide"


def test_unauthenticated_user_cannot_access_resources(client: TestClient) -> None:
    response = client.get("/api/resources")

    assert response.status_code == 401
