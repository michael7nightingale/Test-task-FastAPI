import pytest
from fastapi import status
from httpx import AsyncClient

from src.api.responses import MainDetail

from tests.test_api.conftest import get_main_url


class TestMain:

    async def test_homepage(self, client: AsyncClient):
        resp = await client.get(url=get_main_url("homepage"))
        assert resp.status_code == status.HTTP_200_OK

