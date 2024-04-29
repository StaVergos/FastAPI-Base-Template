from fastapi import FastAPI

from app.users.router import router as users_router

app = FastAPI()


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(users_router, prefix="/v1/users", tags=["users"])
