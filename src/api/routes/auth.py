from fastapi import APIRouter, Body, Depends

from src.api.dependencies.auth import create_token, get_superuser
from src.api.dependencies.database import get_repository
from src.infrastructure.db.repositories import UserRepository
from src.infrastructure.db.models import User
from src.schemas.user import UserShow, UserRegister


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.get("/all")
async def get_all_users(user_repo: UserRepository = Depends(get_repository(UserRepository)),
                        superuser: UserShow = Depends(get_superuser)):
    """Get list of all registered users. Only for superuser."""
    users: list[User] = user_repo.all()
    return [u.as_dict() for u in users]


@auth_router.post("/register")
async def register_user(user_repo: UserRepository = Depends(get_repository(UserRepository)),
                        user_schema: UserRegister = Body()) -> UserShow:
    """Register user endpoint. All schema data is needed."""
    registered_user: User = user_repo.create(user_schema)
    return UserShow(**registered_user.as_dict())


@auth_router.post("/token")
async def get_token(token: str = Depends(create_token)):
    """Get auth token by login data (username, password) in request Body"""
    return {"access_token": token}
