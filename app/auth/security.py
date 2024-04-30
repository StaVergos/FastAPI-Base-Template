import datetime

from passlib.context import CryptContext
from jose import jwt


from app.auth.models import Token
from app.auth.config import config
from app.users.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user_token_limit(user: User) -> bool:
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
