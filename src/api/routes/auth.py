from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException

from src.package.auth import create_access_token
from src.api.dependencies.auth import login_current_user, get_current_user, get_superuser
from src.infrastructure.db.repositories.repositories import UserRepository
from src.api.dependencies.database import get_repository
from src.schemas.user import UserShow, UserRegister
from src.infrastructure.db.models.models import User


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.get("/all")
async def get_all_users(user_repo: UserRepository = Depends(get_repository(UserRepository)),
                        superuser: UserShow = Depends(get_superuser)):
    users: list[User] = user_repo.all()
    return [u.as_dict() for u in users]


@auth_router.post("/register")
async def register_user(user_repo: UserRepository = Depends(get_repository(UserRepository)),
                        user_schema: UserRegister = Body()) -> UserShow:
    """Register user endpoint. All schema data is needed."""
    registered_user: User = user_repo.create(user_schema)
    return UserShow(**registered_user.as_dict())


@auth_router.post("/token")
async def get_token(user_inst: User = Depends(login_current_user)):
    """Get auth token by login data (username, password) in request Body"""
    to_encode = UserShow(**user_inst.as_dict()).dict()
    token = create_access_token(to_encode)
    return {"access_token": token}
