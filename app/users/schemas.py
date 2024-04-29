from app.core.schemas import CustomModel


class BaseUser(CustomModel):
    username: str
    email: str
    is_active: bool
    is_superuser: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "test",
                    "email": "test@test.com",
                    "password": "password",
                    "is_active": True,
                    "is_superuser": False,
                }
            ]
        }
    }


class UserIn(BaseUser):
    password: str


class UserOut(BaseUser):
    id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "test",
                    "email": "test@test.com",
                    "is_active": True,
                    "is_superuser": False,
                }
            ]
        }
    }
