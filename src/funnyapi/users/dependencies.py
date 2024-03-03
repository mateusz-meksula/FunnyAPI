from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from funnyapi.core.config import Config, get_config
from funnyapi.core.database import Cursor, get_cursor
from funnyapi.users.database import User, UserRepository
from funnyapi.users.utils import CredentialsError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")


async def get_user_repo(cursor: Annotated[Cursor, Depends(get_cursor)]):
    yield UserRepository(cursor)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
    config: Annotated[Config, Depends(get_config)],
) -> User:
    try:
        payload = jwt.decode(
            token=token,
            key=config.jwt_secret_key,
            algorithms=(config.jwt_algorithm,),
        )
    except JWTError:
        raise CredentialsError
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise CredentialsError

    user = await user_repo.get(int(user_id))
    if user is None:
        raise CredentialsError

    return user
