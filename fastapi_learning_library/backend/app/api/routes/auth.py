from fastapi import APIRouter, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.services import auth_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: DbSession) -> UserRead:
    return auth_service.register_user(db, user_in)


@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: DbSession) -> Token:
    return auth_service.authenticate_user(db, login_in)


@router.get("/me", response_model=UserRead)
def read_me(current_user: CurrentUser) -> UserRead:
    return current_user
