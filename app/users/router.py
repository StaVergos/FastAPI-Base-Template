from fastapi import APIRouter, Depends, status
from pydantic import EmailStr

from app.core.db import get_db
from app.users.schemas import UserIn, UserOut, UserUpdate
from app.users.services import (
    create_user,
    get_users,
    get_user_by_email,
    get_user_by_id,
    update_user,
)

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_route(data: UserIn, db=Depends(get_db)) -> UserOut:
    return create_user(data, db)


@router.get("/", response_model=list[UserOut])
def get_users_route(db=Depends(get_db)) -> list[UserOut]:
    return get_users(db)


@router.get("/email/{email}", response_model=UserOut)
def get_user_by_email_route(email: EmailStr, db=Depends(get_db)) -> UserOut:
    return get_user_by_email(email, db)


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id_route(user_id: int, db=Depends(get_db)) -> UserOut:
    return get_user_by_id(user_id, db)


@router.patch("/{user_id}", response_model=UserOut)
def update_user_route(user_id: int, data: UserUpdate, db=Depends(get_db)) -> UserOut:
    return update_user(user_id, data, db)
