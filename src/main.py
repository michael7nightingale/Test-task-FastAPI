from fastapi import FastAPI

from src.api.routes import main_router, employees_router, auth_router
from src.infrastructure.db import create_sessionmaker, create_engine_
from src.infrastructure.db.utils import create_superuser
from src.config import get_app_settings


def create_app() -> FastAPI:
    """
    Function creates application instance.
    I wanted to write a class, but function is enough.
    """
    import os
    print(os.environ.get("TEST"), os.environ.get("PROD"))
    settings = get_app_settings()
    print(f"Settings: {settings}")
    app_ = FastAPI()
    routers = (main_router, auth_router, employees_router)
    for router in routers:
        app_.include_router(router)

    engine = create_engine_(
        dns=f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
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

