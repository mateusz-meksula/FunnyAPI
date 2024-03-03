from typing import Annotated

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_restful.cbv import cbv

from funnyapi.core.config import Config, get_config
from funnyapi.core.database import Cursor, get_cursor
from funnyapi.users.database import User
from funnyapi.users.dependencies import get_current_user
from funnyapi.users.schemas import Token, UserCreate, UserRead
from funnyapi.users.service import UserService

router = APIRouter(prefix="/user", tags=["user"])


@cbv(router)
class UserView:
    cursor: Cursor = Depends(get_cursor)
    config: Config = Depends(get_config)

    def __init__(self) -> None:
        self.service = UserService(self.cursor, self.config)

    @router.post("/create", response_model=UserRead, status_code=201)
    async def create_user(self, user: UserCreate):
        new_user = await self.service.create_user(user)
        return new_user

    @router.post("/token", response_model=Token)
    async def login_for_token(
        self,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ):
        username = form_data.username
        password = form_data.password

        user = await self.service.authenticate_user(username, password)
        jwt_token = self.service.get_jwt_token(user)
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
        }

    @router.get("/me", response_model=UserRead)
    async def current_user_details(
        self, user: Annotated[User, Depends(get_current_user)]
    ):
        return user
