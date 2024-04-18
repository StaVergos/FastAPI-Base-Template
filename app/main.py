from functools import lru_cache
from fastapi import FastAPI, Depends
from typing_extensions import Annotated
from app.core import config

app = FastAPI()


@lru_cache()
def get_settings():
    return config.get_settings()


@app.get("/")
def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {"app_name": settings.app_name}
