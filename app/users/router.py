from fastapi import APIRouter, Depends

from app.core.db import get_db
from app.users.schemas import UserIn, UserOut
from app.users.services import create_user

router = APIRouter()


@router.post("/", response_model=UserOut)
def create_user_route(data: UserIn, db=Depends(get_db)) -> UserOut:
    return create_user(data, db)
