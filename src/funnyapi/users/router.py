from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_restful.cbv import cbv

from funnyapi.core.database import Cursor, get_cursor
from funnyapi.users.schemas import UserCreate, UserRead
from funnyapi.users.service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@cbv(router)
class UserView:
    cursor: Cursor = Depends(get_cursor)

    def __init__(self) -> None:
        self.service = UserService(self.cursor)

    @router.post("/create", response_model=UserRead, status_code=201)
    async def create_user(self, user: UserCreate):
        new_user = await self.service.create_user(user)
        return new_user
