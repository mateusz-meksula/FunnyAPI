from typing import cast

from fastapi import HTTPException, status

from funnyapi.core.config import Config
from funnyapi.core.database import Cursor
from funnyapi.users.database import User, UserRepository
from funnyapi.users.schemas import UserCreate
from funnyapi.users.utils import (
    AuthenticationError,
    create_jwt_token,
    get_password_hash,
    verify_password,
)


class UserService:
    user_repo: UserRepository

    def __init__(self, cursor: Cursor, config: Config) -> None:
        self.user_repo = UserRepository(cursor)
        self.config = config

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

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repo.get_by_username(username)
        if user is None:
            raise AuthenticationError

        is_password_correct = verify_password(password, user["password_hash"])
        if not is_password_correct:
            raise AuthenticationError

        return user

    def get_jwt_token(self, user: User) -> str:
        payload = {"sub": str(user["user_id"])}
        return create_jwt_token(
            payload=payload,
            key=self.config.jwt_secret_key,
            algorithm=self.config.jwt_algorithm,
        )
