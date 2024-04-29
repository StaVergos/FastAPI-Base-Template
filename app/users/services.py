from sqlalchemy.exc import IntegrityError

from app.core.exceptions import Conflict
from app.users.schemas import UserIn
from app.users.models import User


def create_user(data: UserIn, db) -> User:
    password = data.password
    hashed_password = "fakehashed_" + password
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_password,
        is_active=data.is_active,
        is_superuser=data.is_superuser,
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        if isinstance(e, IntegrityError):
            raise Conflict(detail="User with this email already exists")
    return user


def get_users(db):
    return db.query(User).all()