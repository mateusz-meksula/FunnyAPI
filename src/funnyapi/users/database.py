from typing import TypedDict

from pypika import Query, Table

from funnyapi.core.database import Cursor


class User(TypedDict):
    user_id: int
    username: str
    password_hash: str
    is_admin: bool
    is_banned: bool


class UserRepository:
    def __init__(self, cursor: Cursor) -> None:
        self.cursor = cursor
        self.user_table = Table("user")

    async def add(self, username: str, password_hash: str) -> None:
        q = (
            Query.into(self.user_table)
            .columns("username", "password_hash")
            .insert(username, password_hash)
        )
        await self.cursor.execute(q.get_sql())

    async def get(self, user_id: int) -> User | None:
        q = (
            Query.from_(self.user_table)
            .select("*")
            .where(self.user_table.user_id == user_id)
        )
        await self.cursor.execute(q.get_sql())
        return await self.cursor.fetchone()

    async def get_all(self) -> list[User]:
        q = Query.from_(self.user_table).select("*")
        await self.cursor.execute(q.get_sql())
        return await self.cursor.fetchall()

    async def modify(self, user_id: int, *, is_banned: bool) -> None:
        q = (
            Query.update(self.user_table)
            .set(self.user_table.is_banned, is_banned)
            .where(self.user_table.user_id == user_id)
        )
        await self.cursor.execute(q.get_sql())

    async def delete(self, user_id: int) -> None:
        q = (
            Query.from_(self.user_table)
            .delete()
            .where(self.user_table.user_id == user_id)
        )
        await self.cursor.execute(q.get_sql())
