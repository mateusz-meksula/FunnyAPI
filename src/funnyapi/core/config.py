from typing import Any, ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings
from typing_extensions import Self


class Config(BaseSettings):
    _instances: ClassVar[list[Self]] = []

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if not cls._instances:
            instance = super().__new__(cls, *args, **kwargs)
            cls._instances.append(instance)
            return instance
        return cls._instances[0]

    db_host: str = Field(default=..., alias="MYSQL_HOST")
    db_user: str = Field(default=..., alias="MYSQL_USER")
    db_password: str = Field(default=..., alias="MYSQL_PASSWORD")
    db_name: str = "funnyapi"
    #
    jwt_secret_key: str = Field(default=...)
    jwt_algorithm: str = "HS256"


def get_config():
    yield Config()
