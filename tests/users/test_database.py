import sqlite3

import pytest
from aiosqlite import Cursor

from funnyapi.users.database import UserRepository

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(name="user_repo", scope="function")
def user_repo_fixture(cursor):
    repo = UserRepository(cursor)

    yield repo


@pytest.fixture(scope="module", autouse=True)
def fill_database():
    connection = sqlite3.connect("testfunnyapi.db")
    cursor = connection.cursor()

    cursor.execute(
        """\
INSERT INTO user (username, password_hash)
VALUES
    ('test01', 'hash01'),
    ('test02', 'hash02'),
    ('test03', 'hash03'),
    ('test04', 'hash04'),
    ('test05', 'hash05')
;
"""
    )
    connection.commit()
    cursor.close()
    connection.close()
    yield


@pytest.mark.asyncio
async def test_user_add(user_repo: UserRepository, cursor: Cursor):
    await user_repo.add("test_user", "test_hashed_password")

    await cursor.execute("SELECT * FROM user WHERE username = 'test_user'")
    data = await cursor.fetchone()

    assert data is not None
    assert len(data) == 5
    assert isinstance(data[0], int)
    assert "test_user" in data
    assert "test_hashed_password" in data


@pytest.mark.asyncio
async def test_user_get(user_repo: UserRepository):
    user = await user_repo.get(1)

    assert user is not None
    assert user[0] == 1  # type: ignore
    assert "test01" in user
    assert "hash01" in user


@pytest.mark.asyncio
async def test_user_get_non_existing(user_repo: UserRepository):
    user = await user_repo.get(1000)

    assert user is None


@pytest.mark.asyncio
async def test_user_get_all(user_repo: UserRepository):
    users = await user_repo.get_all()

    assert users is not None
    assert len(users) >= 5

    user = users[0]
    assert user[0] == 1  # type: ignore


@pytest.mark.asyncio
async def test_user_modify(user_repo: UserRepository, cursor: Cursor):
    await cursor.execute("SELECT is_banned FROM user WHERE user_id = 1")
    data = await cursor.fetchone()
    assert data is not None
    assert data[0] == 0

    await user_repo.modify(1, is_banned=True)

    await cursor.execute("SELECT is_banned FROM user WHERE user_id = 1")
    data = await cursor.fetchone()
    assert data is not None
    assert data[0] == 1


@pytest.mark.asyncio
async def test_user_delete(user_repo: UserRepository, cursor: Cursor):
    await cursor.execute("SELECT * FROM user WHERE user_id = 1")
    data = await cursor.fetchone()
    assert data is not None

    await user_repo.delete(1)

    await cursor.execute("SELECT * FROM user WHERE user_id = 1")
    data = await cursor.fetchone()
    assert data is None
