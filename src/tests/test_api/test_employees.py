import pytest

from httpx import AsyncClient
from fastapi import status
from datetime import datetime

from api.auth.responses import AuthDetail
from api.employees.responses import EmployeesDetail
from infrastructure.utils.auth import create_uuid

from tests.test_api.conftest import get_employees_url, get_auth_url


class TestEmployee:

    async def test_get_all_employees(self, client: AsyncClient, superuser_headers: dict):
        resp = await client.get(url="/employees/all", headers=superuser_headers)
        assert resp.status_code == status.HTTP_200_OK

    async def test_get_all_employees_fail(self, client: AsyncClient, common_headers: dict):
        resp = await client.get(url=get_employees_url("get_all_employees"), headers=common_headers)
        assert resp.status_code == status.HTTP_403_FORBIDDEN
        assert resp.json() == {"detail": AuthDetail.no_permissions.value}

    async def test_create_employee(self, client: AsyncClient, superuser_headers: dict,
                                   user_data: dict):
        resp_reg = await client.post(url=get_auth_url("register_user"),
                                     json=user_data)
        user_id = resp_reg.json()['id']
        employee_data = {
            "user_id": user_id,
            "salary": 9172300,
            "promotion_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        }
        resp = await client.post(url=get_employees_url("create_employee"),
                                 json=employee_data,
                                 headers=superuser_headers)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.json()['salary'] == employee_data['salary']
        assert resp.json()['promotion_date'] == employee_data['promotion_date']

    async def test_create_employee_fail(self, client: AsyncClient,
                                        superuser_headers: dict,
                                        user_data: dict):
        employee_data = {
            "user_id": create_uuid(),
            "salary": 9172300,
            "promotion_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        }
        resp = await client.post(url=get_employees_url("create_employee"),
                                 json=employee_data,
                                 headers=superuser_headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {"detail": EmployeesDetail.employee_create_error.value}

    async def test_employee_me(self, client: AsyncClient, common_headers: dict,
                               superuser_headers: dict, user_data: dict):
        resp_reg = await client.get(url=get_auth_url("get_all_users"),
                                    headers=superuser_headers)
        user_id = resp_reg.json()[-1]['id']
        employee_data = {
            "user_id": user_id,
            "salary": 9172300,
            "promotion_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        }
        resp_create = await client.post(url=get_employees_url("create_employee"),
                                        json=employee_data,
                                        headers=superuser_headers)

        resp = await client.get(url=get_employees_url("get_employee"),
                                headers=common_headers)
        assert resp.status_code == status.HTTP_200_OK

    async def test_employee_me_fail(self, client: AsyncClient, common_headers: dict):
        resp = await client.get(url=get_employees_url("get_employee"),
                                headers=common_headers)
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert resp.json() == {'detail': EmployeesDetail.employee_not_found.value}

