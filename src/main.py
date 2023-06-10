from fastapi import FastAPI
import gunicorn
import uvicorn
from dotenv import load_dotenv
load_dotenv()

from internal.api import main_router, auth_router, employee_router
from package.database import create_superuser


def create_app() -> FastAPI:
    """
    Function creates application instance.
    I wanted to write a class, but function is enough.
    """
    routers = (main_router, auth_router, employee_router)
    app_ = FastAPI()
    for router in routers:
        app_.include_router(router)

    @app_.on_event("startup")
    async def on_startup():
        try:
            await create_superuser()
        except:     # Superuser exists
            pass

    @app_.on_event("shutdown")
    async def on_shutdown():
        # await engine.dispose()
        ...
    return app_


app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        host='localhost',
        port=8000,
        app='main:app'
    )





