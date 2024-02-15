from functools import cache

from pydantic import Field
from pydantic_settings import BaseSettings


class _Config(BaseSettings):
    db_host: str = Field(alias="MYSQL_HOST")
    db_user: str = Field(alias="MYSQL_USER")
    db_password: str = Field(alias="MYSQL_PASSWORD")
    db_name: str = "funnyapi"


@cache
def Config():
    return _Config()  # type: ignore
