from app.core.exceptions import NotAuthenticated, Forbidden


from app.auth.schemas import UserLogin
from app.auth.security import verify_password, create_access_token, get_user_token_limit
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
