from fastapi import Depends, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette.exceptions import HTTPException

from .db.repository import UserRepository
from ..api.dependencies import get_repository
from infrastructure.utils.auth import decode_access_token
from .schemas import UserShow, UserLogin

from .responses import AuthDetail


oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: str = Depends(oauth_scheme)) -> UserShow:
    """Dependency for getting user from token"""
    user_data = decode_access_token(token)
    return UserShow(**user_data)


async def login_current_user(user_repo: UserRepository = Depends(get_repository(UserRepository)),
                             user_data: UserLogin = Body()):    # OAuth2PasswordRequestForm if needed
    """Dependency for getting user by login data from DB."""
    try:
        user = user_repo.login(user_data)
        return user
    except AttributeError:
        raise HTTPException(status_code=403, detail=AuthDetail.login_data_error.value)


async def get_superuser(user: UserShow = Depends(get_current_user)):
    """Checks if current user is superuser"""
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail=AuthDetail.no_permissions.value)
    return user


# ================================= OAuth2PasswordRequestForm ===========================#

async def get_current_user_form(token: str = Depends(oauth_scheme)) -> UserShow:
    """Dependency for getting user from token"""
    user_data = decode_access_token(token)
    return UserShow(**user_data)


async def login_current_user_form(user_repo: UserRepository = Depends(get_repository(UserRepository)),
                                  user_form: OAuth2PasswordRequestForm = Depends()):    # OAuth2PasswordRequestForm if needed
    """Dependency for getting user by login data from DB."""
    try:
        user = user_repo.login_oauth(user_form.username, user_form.password)
        return user
    except AttributeError:
        raise HTTPException(status_code=403, detail=AuthDetail.login_data_error.value)
