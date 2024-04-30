import datetime

from pydantic import EmailStr, ConfigDict

from app.core.schemas import CustomModel


class Token(CustomModel):
    token: str
    expiry: datetime.datetime
    user_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"token": "string", "expiry": "2021-10-07T09:00:00+0000", "user_id": 1}
            ]
        }
    )


class TokenData(CustomModel):
    access_token: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoiYiJ9.jiMyrsmD8AoHWeQgmxZ5yq8z0lXS67_QGs52AzC8Ru8"
                }
            ]
        }
    )


class UserLogin(CustomModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"email": "test@test.com", "password": "password"}]
        }
    )
