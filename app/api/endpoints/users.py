from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_async_session
from app.repositories.user_repository import SqlAlchemyUserRepository, UserRepository
from app.core.security import CredentialsExeption, validate_password, create_jwt_token
from app.api.models.user import UserLogin

router = APIRouter(prefix="/auth", tags=["auth", "user"])


def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserRepository:
    return SqlAlchemyUserRepository(session)


@router.post("/register")
async def register(
    user: UserLogin,
    response: Response,
    repo: UserRepository = Depends(get_user_repository),
):
    user_db = await repo.get_user(user.username)
    if not user_db:
        await repo.create_user(user)
        response.status_code = status.HTTP_201_CREATED
        return
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"User named {user.username} is already registered",
    )


@router.post("/login")
async def login(
    user: OAuth2PasswordRequestForm = Depends(),
    repo: UserRepository = Depends(get_user_repository),
):
    user_db = await repo.get_user(user.username)
    if not user_db:
        raise CredentialsExeption(f"User named {user.username} isn't registered")
    if not validate_password(user.password, user_db.password, user_db.salt):
        raise CredentialsExeption("Invalid username or password")
    return {"access_token": create_jwt_token({"sub": user.username})}
