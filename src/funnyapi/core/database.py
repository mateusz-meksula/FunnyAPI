from typing import Any

from mysql.connector.aio import connect
from mysql.connector.aio.cursor import MySQLCursorDict

from funnyapi.core.config import Config


class Cursor(MySQLCursorDict):
    async def fetchone(self) -> Any | None:
        return await super().fetchone()

    async def fetchall(self) -> list[Any]:
        return await super().fetchall()


async def get_connection():
    config = Config()
    return await connect(
        host=config.db_host,
        user=config.db_user,
        password=config.db_password,
        database=config.db_name,
    )


async def get_cursor():
    connection = await get_connection()
    cursor = await connection.cursor(dictionary=True)
    yield cursor
    await connection.commit()
    await cursor.close()
    await connection.close()
