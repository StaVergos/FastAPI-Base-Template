from fastapi import APIRouter, Depends, status

from app.auth.security import JWTBearer
from app.core.db import get_db
from app.auth.schemas import TokenData, UserLogin
from app.auth.services import (
    authenticate_user,
    delete_user_token,
    delete_all_user_tokens,
)

router = APIRouter()


@router.post("/login", response_model=TokenData, status_code=status.HTTP_201_CREATED)
def login(data: UserLogin, db=Depends(get_db)):
    return {"access_token": authenticate_user(data, db)}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(incoming_token: str = Depends(JWTBearer()), db=Depends(get_db)):
    return delete_user_token(incoming_token, db)


@router.post("/signout", status_code=status.HTTP_204_NO_CONTENT)
def signout(incoming_token: str = Depends(JWTBearer()), db=Depends(get_db)):
    return delete_all_user_tokens(incoming_token, db)
