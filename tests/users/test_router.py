import sqlite3

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module", autouse=True)
def create_test_user():
    connection = sqlite3.connect("testfunnyapi.db")
    cursor = connection.cursor()

    cursor.execute(
        """\
INSERT INTO user (username, password_hash)
VALUES
    ('existing', 'test_hash')
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
