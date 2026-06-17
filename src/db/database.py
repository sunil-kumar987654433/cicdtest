from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from src.config import Config
from typing import AsyncGenerator
class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)

async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session()->AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session