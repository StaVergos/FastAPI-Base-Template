from app.core.exceptions import NotAuthenticated, Forbidden


from app.auth.schemas import UserLogin
from app.auth.security import (
    verify_password,
    create_access_token,
    get_user_token_limit,
    get_user_id_from_token,
)
from app.auth.models import Token
from app.users.services import get_user_by_email


def authenticate_user(data: UserLogin, db):
    if user := get_user_by_email(data.email, db):
        if verify_password(data.password, user.hashed_password):
            if not get_user_token_limit(user):
                raise Forbidden(detail="User token limit exceeded")
            access_token = create_access_token(user.id, db)
            return access_token
        else:
            raise NotAuthenticated(detail="Incorrect password")


def delete_user_token(token: str, db):
    db.query(Token).filter(Token.token == token).delete()
    db.commit()
    return None


def delete_all_user_tokens(token, db):
    user_id = get_user_id_from_token(token)
    db.query(Token).filter(Token.user_id == user_id).delete()
    db.commit()
    return None
