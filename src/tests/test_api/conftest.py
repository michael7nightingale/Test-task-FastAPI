from datetime import datetime

import pytest
from httpx import AsyncClient
from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

from config import get_app_settings

from api.auth.db.models import User
from api.employees.db.models import Employee
from infrastructure.utils.auth import create_uuid
from api.auth.routes import auth_router
from api.employees.routes import employees_router
from api.main.routes import main_router


def get_url(router: APIRouter):
    def inner(name: str):
        return router.url_path_for(name)
    return inner


get_auth_url = get_url(auth_router)
get_main_url = get_url(main_router)
get_employees_url = get_url(employees_router)


@pytest.fixture(scope="function")
async def superuser_headers(client: AsyncClient):
    settings = get_app_settings()
    data = {
        "username": settings.SUPERUSER_NAME,
        "password": settings.SUPERUSER_PASSWORD
    }
    resp = await client.post(url='/auth/token', json=data)
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
async def common_headers(client: AsyncClient, user_data: dict):
    resp = await client.post(url="/auth/register", json=user_data)
    login_data = {
        "username": user_data['username'],
        "password": user_data['password']
    }
    resp_log = await client.post(url="/auth/token", json=login_data)
    token = resp_log.json()['access_token']
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope='function')
async def create_user_in_database(session_test):
    async def create_user_in_database_inner(**kwargs):
        with session_test() as session:
            try:
                user = User(**kwargs)
                session.add(user)
                session.commit()
            except IntegrityError:
                pass
    return create_user_in_database_inner


user_id = create_uuid()


@pytest.fixture
async def user_data():
    global user_id
    return {
        "username": "postgres12",
        "email": "vk@gmail.com",
        "password": "qwerty019",
        "first_name": "Mick",
        "last_name": "Jagger"
    }


@pytest.fixture(scope='function')
async def create_employee_in_database(session_test):
    async def create_employee_in_database_inner(**kwargs):
        with session_test() as session:
            try:
                user = Employee(**kwargs)
                session.add(user)
                session.commit()
            except IntegrityError:
                pass
    return create_employee_in_database_inner


@pytest.fixture
async def employee_data():
    return {
        "id": create_uuid(),
        "user_id": user_id,
        "salary": 100023,
        "promotion_date": datetime.datetime.utcnow()
    }

