from funnyapi.core.database import Cursor
from funnyapi.users.database import User, UserRepository
from funnyapi.users.schemas import UserCreate


class UserService:
    user_repo: UserRepository

    def __init__(self, cursor: Cursor) -> None:
        self.user_repo = UserRepository(cursor)

    async def create_user(self, user: UserCreate) -> User:
        username_taken = await self.user_repo.get_by_username(user.username) is not None
        if username_taken:
            raise ValueError
        # TODO add password hashing
        await self.user_repo.add(user.username, user.password)
        new_user = await self.user_repo.get_by_username(user.username)
        return new_user  # type: ignore
