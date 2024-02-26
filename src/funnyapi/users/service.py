from typing import cast

from fastapi import HTTPException, status

from funnyapi.core.database import Cursor
from funnyapi.users.database import User, UserRepository
from funnyapi.users.schemas import UserCreate
from funnyapi.users.utils import get_password_hash


class UserService:
    user_repo: UserRepository

    def __init__(self, cursor: Cursor) -> None:
        self.user_repo = UserRepository(cursor)

    async def create_user(self, user: UserCreate) -> User:
        username_taken = await self.user_repo.get_by_username(user.username) is not None

        if username_taken:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken.",
            )

        password_hash = get_password_hash(user.password1)
        await self.user_repo.add(user.username, password_hash)
        new_user = await self.user_repo.get_by_username(user.username)

        return cast(User, new_user)
