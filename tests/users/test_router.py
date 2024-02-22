from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    request_data = {
        "username": "user123",
        "password": "test_PASSword123!!",
    }
    r = client.post("/user/create", json=request_data)
    user = r.json()

    assert r.status_code == 201
    assert user["username"] == "user123"
    assert user["is_admin"] is False
    assert user["is_banned"] is False
