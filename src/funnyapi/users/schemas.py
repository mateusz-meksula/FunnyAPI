from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=4, max_length=15)
    password: str = Field(min_length=10, max_length=20)


class UserRead(BaseModel):
    user_id: int
    username: str
    is_admin: bool
    is_banned: bool
    created: datetime
