from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine
)
from sqlalchemy.engine.url import make_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.config import Config
from typing import AsyncGenerator


class Base(DeclarativeBase):
    pass


# =========================
# ASYNC (FASTAPI)
# =========================
async_engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=1800
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def create_table():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# =========================
# SYNC (CELERY)
# =========================


sync_engine = create_engine(
    Config.SYNC_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=1800
)

SessionLocal = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False
)