import sqlite3

import pytest
from fastapi.testclient import TestClient
from passlib.hash import pbkdf2_sha256


@pytest.fixture(scope="module", autouse=True)
def create_test_user():
    connection = sqlite3.connect("testfunnyapi.db")
    cursor = connection.cursor()

    cursor.execute(
        f"""\
INSERT INTO user (username, password_hash)
VALUES
    ('existing', {pbkdf2_sha256.hash('test_hash')!r})
;
"""
    )
    connection.commit()
    cursor.close()
    connection.close()
    yield


def test_create_user(client: TestClient):
    request_data = {
        "username": "user123",
        "password1": "test_PASSword123!!",
        "password2": "test_PASSword123!!",
    }
    r = client.post("/user/create", json=request_data)
    user = r.json()

    assert r.status_code == 201
    assert user["username"] == "user123"
    assert user["is_admin"] is False
    assert user["is_banned"] is False


def test_create_user_password_dont_match(client: TestClient):
    request_data = {
        "username": "user123",
        "password1": "test_PASSword123!!",
        "password2": "TEST_PASSword123!!",
    }
    r = client.post("/user/create", json=request_data)
    assert r.status_code == 422


def test_create_user_missing_password(client: TestClient):
    request_data = {
        "username": "user123",
        "password1": "test_PASSword123!!",
    }
    r = client.post("/user/create", json=request_data)
    assert r.status_code == 422


def test_create_user_username_taken(client: TestClient):
    request_data = {
        "username": "existing",
        "password1": "test_PASSword123!!",
        "password2": "test_PASSword123!!",
    }
    r = client.post("/user/create", json=request_data)
    data = r.json()

    assert r.status_code == 409
    assert data["detail"] == "Username already taken."


def test_token(client: TestClient):
    form_data = {
        "username": "existing",
        "password": "test_hash",
    }
    r = client.post("/user/token", data=form_data)
    data = r.json()

    assert r.status_code == 200
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"


def test_token_invalid_username(client: TestClient):
    form_data = {
        "username": "invalid",
        "password": "test_hash",
    }
    r = client.post("/user/token", data=form_data)

    assert r.status_code == 400


def test_token_invalid_password(client: TestClient):
    form_data = {
        "username": "existing",
        "password": "test_hash_123",
    }
    r = client.post("/user/token", data=form_data)

    assert r.status_code == 400


def test_token_invalid_data(client: TestClient):
    form_data = {"invalid": "yes"}
    r = client.post("/user/token", data=form_data)

    assert r.status_code == 422


def test_can_access_auth_required_endpoint(client: TestClient):
    form_data = {
        "username": "existing",
        "password": "test_hash",
    }
    r = client.post("/user/token", data=form_data)
    data = r.json()
    token = data["access_token"]

    r = client.get("/user/me", headers={"Authorization": f"Bearer {token}"})
    data = r.json()
    assert r.status_code == 200
    assert "user_id" in data
    assert "username" in data
    assert "is_admin" in data
    assert "is_banned" in data
    assert "created" in data
