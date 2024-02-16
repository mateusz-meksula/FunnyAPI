from typing import Annotated, Any, TypeAlias

from fastapi import Depends
from mysql.connector.aio import connect
from mysql.connector.aio.cursor import MySQLCursorDict

from funnyapi.core.config import Config

config = Config()


class Cursor(MySQLCursorDict):
    async def fetchone(self) -> dict[str, Any] | None:
        return await super().fetchone()

    async def fetchall(self) -> list[dict[str, Any]]:
        return await super().fetchall()  # type: ignore


async def get_connection():
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


CursorD: TypeAlias = Annotated[Cursor, Depends(get_cursor)]
