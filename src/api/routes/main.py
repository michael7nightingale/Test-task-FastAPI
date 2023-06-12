from fastapi import APIRouter


main_router = APIRouter(prefix='', tags=["Homepage"])


@main_router.get("/")
async def root():
    """Home page"""
    return {"message": "If you see the message, service is working!"}
