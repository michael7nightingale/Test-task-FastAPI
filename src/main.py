import os
import uvicorn
from fastapi import FastAPI

from api.auth.routes import auth_router
from api.main.routes import main_router
from api.employees.routes import employees_router
from infrastructure.db import create_sessionmaker, create_engine_
from infrastructure.db.utils import create_superuser
from config import get_app_settings


def create_app() -> FastAPI:
    """
    Function creates application instance.
    I wanted to write a class, but function is enough.
    """
    import os
    # print(os.environ.get("TEST"), os.environ.get("PROD"))
    settings = get_app_settings()
    # print(f"Settings: {settings}")
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


app = create_app()

if __name__ == '__main__':
    os.environ.update({"TEST": "", "PROD": ""})
    uvicorn.run(
        # reload=True   # if workers=None
        workers=4,
        host='localhost',
        port=8000,
        app='main:app'
    )
