from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.exceptions import unauthorized
from app.core.security import decode_access_token
from app.db.database import get_db
from app.db.models import User
from app.repositories import user_repository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DbSession,
) -> User:
    subject = decode_access_token(token)
    if subject is None:
        raise unauthorized()

    try:
        user_id = int(subject)
    except ValueError:
        raise unauthorized() from None

    user = user_repository.get_user_by_id(db, user_id)
    if user is None:
        raise unauthorized()
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
