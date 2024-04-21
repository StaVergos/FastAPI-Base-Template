from fastapi import FastAPI, Depends
from typing_extensions import Annotated
from app.core import config

app = FastAPI()


@app.get("/")
def info(settings: Annotated[config.Settings, Depends(config.get_settings)]):
    return {"app_name": settings.app_name}
