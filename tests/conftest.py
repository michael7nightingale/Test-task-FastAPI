import pytest
import asyncio
from fastapi.testclient import TestClient
import os, sys
sys.path.append("\\".join(os.getcwd().split('\\')[:-1]))
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

from src.config import (DB_NAME_TEST, DB_USER_TEST, DB_HOST_TEST, DB_PASSWORD_TEST, DB_PORT_TEST)
from src.package.database import create_db, drop_db, create_superuser, metadata

from src.main import app

engine: AsyncEngine = create_async_engine(
    url=f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}/{DB_NAME_TEST}"
)
metadata.bind = engine
TestSession = sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=True)


@pytest.fixture(autouse=True, scope='session')
async def create_test_db():
    await create_db(local_engine=engine)
    yield
    await drop_db(local_engine=engine)


@pytest.fixture(autouse=True, scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)




