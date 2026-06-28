from sqlalchemy.orm import Session

from app.core.exceptions import bad_request, unauthorized
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories import user_repository
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin


def register_user(db: Session, user_in: UserCreate) -> User:
    if user_repository.get_user_by_username(db, user_in.username):
        raise bad_request("Username is already registered")
    if user_repository.get_user_by_email(db, str(user_in.email)):
        raise bad_request("Email is already registered")

    hashed_password = hash_password(user_in.password)
    return user_repository.create_user(
        db,
        user_in=user_in,
        hashed_password=hashed_password,
    )


def authenticate_user(db: Session, login_in: UserLogin) -> Token:
    user = user_repository.get_user_by_username(db, login_in.username)
    if user is None or not verify_password(login_in.password, user.hashed_password):
        raise unauthorized("Invalid username or password")

    access_token = create_access_token(subject=str(user.id))
    return Token(access_token=access_token)
