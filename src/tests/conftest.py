import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
import os
from sqlalchemy.orm import Session

from config import get_app_settings
from main import create_app
from infrastructure.db import create_sessionmaker, create_engine_
from api.auth.db.repository import UserRepository
from api.employees.db.repository import EmployeeRepository


def create_test_app():
    os.environ["TEST"] = "1"
    app_ = create_app()

    return app_


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def session_test():
    os.environ["TEST"] = "1"
    settings = get_app_settings()
    # print(settings)
    sessionmaker = create_sessionmaker(create_engine_(
            dns=f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
    ))
    yield sessionmaker


@pytest_asyncio.fixture(scope="function")
async def client(session_test):
    app = create_test_app()
    app.state.pool = session_test
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client_:
        yield client_
    with session_test() as session:
        employee_repo = EmployeeRepository(session)
        employee_repo.clear()
        user_repo = UserRepository(session)
        user_repo.clear()





