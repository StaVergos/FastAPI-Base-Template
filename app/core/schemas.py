from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class CustomModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        json_encoders={datetime: convert_datetime_to_gmt},
        populate_by_name=True,
        use_enum_values=True,
    )
