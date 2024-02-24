from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


def convert_datetime(dt: datetime) -> str:
    dt = dt.replace(tzinfo=ZoneInfo("Europe/Warsaw"), microsecond=0)
    return dt.isoformat()


class BaseModel(_BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        str_min_length=1,
        validate_assignment=True,
        json_encoders={datetime: convert_datetime},
    )
