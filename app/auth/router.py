from fastapi import APIRouter, Depends, status

from app.core.db import get_db
from app.auth.schemas import TokenData, UserLogin
from app.auth.services import authenticate_user

router = APIRouter()


@router.post("/login", response_model=TokenData, status_code=status.HTTP_201_CREATED)
def login(data: UserLogin, db=Depends(get_db)):
    return {"access_token": authenticate_user(data, db)}
