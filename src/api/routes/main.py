from fastapi import APIRouter

from ..responses.main import MainDetail


main_router = APIRouter(prefix='', tags=["Homepage"])


@main_router.get("/")
async def homepage():
    """Home page"""
    return {"detail": MainDetail.greeting.value}
