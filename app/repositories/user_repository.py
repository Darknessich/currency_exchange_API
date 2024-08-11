from abc import ABC, abstractmethod

from sqlalchemy import select
from app.core.security import generate_random_salt, generate_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.models.user import UserLogin
from app.db.models import User


class UserRepository(ABC):
    @abstractmethod
    async def get_users(self) -> list[User]:
        pass

    @abstractmethod
    async def create_user(self, user: UserLogin) -> User:
        pass


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_users(self) -> list[User]:
        result = await self._session.execute(select(User))
        return list(result.scalars().all())

    async def create_user(self, user: UserLogin) -> User:
        user_salt = generate_random_salt()
        user.password = await generate_password_hash(user.password, user_salt)
        new_user = User(salt=user_salt, **user.model_dump())
        self._session.add(new_user)
        await self._session.commit()
        await self._session.refresh(new_user)
        return new_user
