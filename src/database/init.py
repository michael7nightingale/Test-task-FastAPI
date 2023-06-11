from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
import asyncio

import os, sys
sys.path.append(os.getcwd() + "\\src\\")

from config import (DB_NAME, DB_USER, DB_HOST, DB_PASSWORD, DB_PORT)


Base = declarative_base()


async def async_main():
    engine: AsyncEngine = create_async_engine(
        url=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    yield Session
    await engine.dispose()


async_gen = async_main()
Session = asyncio.run(anext(async_gen))



async def create_db(local_engine: AsyncEngine):
    """Create tables"""
    async with local_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db(local_engine: AsyncEngine):
    """Drop tables."""
    async with local_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)