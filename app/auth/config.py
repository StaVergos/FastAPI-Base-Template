from pydantic_settings import SettingsConfigDict

from app.core.config import BaseConfig


class AuthConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="AUTH_")

    SECRET_KEY: str
    HASHING_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ACCESS_TOKEN_USER_LIMIT: int


config = AuthConfig()
