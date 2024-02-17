import os
import sqlite3

import aiosqlite
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

os.environ["MYSQL_HOST"] = "test"
os.environ["MYSQL_USER"] = "test"
os.environ["MYSQL_PASSWORD"] = "test"

from funnyapi.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    connection = sqlite3.connect("testfunnyapi.db")
    cursor = connection.cursor()

    cursor.execute(
        """\
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(60) NOT NULL,
    is_admin INTEGER DEFAULT 0,
    is_banned INTEGER DEFAULT 0
);
    """
    )
    cursor.execute(
        """\
CREATE TABLE IF NOT EXISTS joke (
    joke_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title VARCHAR(20) NOT NULL,
    body VARCHAR(500) NOT NULL,
    likes_count INTEGER NOT NULL DEFAULT 0,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
    """
    )
    cursor.execute(
        """\
CREATE TABLE IF NOT EXISTS category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20) UNIQUE NOT NULL
);
    """
    )
    cursor.execute(
        """\
CREATE TABLE IF NOT EXISTS joke_category (
    joke_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (joke_id, category_id),
    FOREIGN KEY (joke_id) REFERENCES joke(joke_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

"""
    )

    connection.commit()
    cursor.close()
    connection.close()

    yield

    os.remove("testfunnyapi.db")


@pytest.fixture(name="client")
def client_fixture():
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(name="cursor", scope="function")
async def cursor_fixture():
    connection = await aiosqlite.connect("testfunnyapi.db")
    cursor = await connection.cursor()
    yield cursor
    await connection.commit()
    await cursor.close()
    await connection.close()
