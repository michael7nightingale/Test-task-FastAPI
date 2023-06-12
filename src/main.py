from fastapi import FastAPI

from src.api.routes.main import main_router
from src.api.routes.auth import auth_router
from src.api.routes.employees import employees_router
from src.infrastructure.db import create_sessionmaker, create_engine
from src.infrastructure.db.utils import create_superuser
from src.config import Settings


def create_app() -> FastAPI:
    """
    Function creates application instance.
    I wanted to write a class, but function is enough.
    """
    app_ = FastAPI()
    routers = (main_router, auth_router, employees_router)
    for router in routers:
        app_.include_router(router)

    settings = Settings()
    engine = create_engine(
        url=f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
    )

    pool = create_sessionmaker(engine)
    create_superuser(pool)

    @app_.on_event("startup")
    async def on_startup():
        app_.state.pool = pool

    @app_.on_event("shutdown")
    async def on_shutdown():
        engine.dispose()

    return app_

