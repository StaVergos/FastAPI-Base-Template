import datetime

from fastapi import HTTPException, Depends, Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from passlib.context import CryptContext
from jose import jwt, JWTError


from app.auth.models import Token
from app.auth.config import config
from app.core.exceptions import NotAuthenticated
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user_token_limit(user) -> bool:
    if len(user.tokens) >= config.ACCESS_TOKEN_USER_LIMIT:
        return False
    return True


def create_access_token(
    user_id: int,
    db,
):
    expires_delta = datetime.timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    claims = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(
        claims, config.SECRET_KEY, algorithm=config.HASHING_ALGORITHM
    )
    token = Token(token=encoded_jwt, expiry=expire, user_id=user_id)
    db.add(token)
    db.commit()
    return token.token


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=config.HASHING_ALGORITHM,
        )
    except JWTError:
        raise NotAuthenticated(detail="Could not validate credentials.")

    return payload


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials and decode_access_token(credentials.credentials):
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

    def verify_jwt(self, jwtoken: str, db: Session) -> bool:
        try:
            payload = decode_access_token(jwtoken)
        except JWTError:
            return False

        token_id = payload.get("token_id")
        user_id = payload.get("user_id")

        token = (
            db.query(Token)
            .filter((Token.id == token_id) | (Token.user_id == user_id))
            .first()
        )

        if token and token.expiry > datetime.datetime.now(datetime.timezone.utc):
            return True

        return False


def get_user_token(incoming_token: str = Depends(JWTBearer())):
    return incoming_token


def get_user_id_from_token(incoming_token: str = Depends(JWTBearer())):
    decoded_token = decode_access_token(incoming_token)
    user_id = decoded_token.get("user_id")
    return user_id
