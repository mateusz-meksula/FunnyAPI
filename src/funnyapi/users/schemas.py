from datetime import datetime
from typing import Annotated, Literal, TypeAlias

from pydantic import StringConstraints, model_validator
from pydantic.functional_validators import AfterValidator
from typing_extensions import Self

from funnyapi.core.model import BaseModel
from funnyapi.users.utils import validate_password

UsernameType: TypeAlias = Annotated[str, StringConstraints(min_length=4, max_length=15)]
PasswordType: TypeAlias = Annotated[str, AfterValidator(validate_password)]


class UserCreate(BaseModel):
    username: UsernameType
    password1: PasswordType
    password2: PasswordType

    @model_validator(mode="after")
    def check_password_match(self) -> Self:
        if self.password1 != self.password2:
            raise ValueError(
                f"{self.password1!r} is not the same as {self.password2!r}"
            )
        return self


class UserRead(BaseModel):
    user_id: int
    username: str
    is_admin: bool
    is_banned: bool
    created: datetime


class Token(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
