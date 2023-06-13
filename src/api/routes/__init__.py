from fastapi import APIRouter

from src.api.routes.auth import auth_router
from src.api.routes.main import main_router
from src.api.routes.employees import employees_router


def url_for(router: APIRouter):
    def inner(name: str):
        return router.url_path_for(name)

    return inner
