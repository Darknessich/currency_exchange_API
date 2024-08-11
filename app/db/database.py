from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(settings.db.async_database_url)
async_session_marker = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with async_session_marker() as session:
        yield session


class Base(DeclarativeBase):
    pass
